import pickle
import math
import time
import glob
import os
import pandas as pd
import numpy as np
from cryodrgn import mrc
from cryodrgn import analysis
from cryodrgn import utils

### Define relevant variables
results_dir = '../' #change as necessary
output_dir = './' #change as necessary
subunit1 = 'H44' #change as necessary
subunit2 = 'head' #change as necessary
mask_names = {subunit1: '/path/to/subunit1/mask.mrc', subunit2: '/path/to/subunit2/mask.mrc'}
Apix = 5.07 #pixel size in the final downsampled volumes
flip = False #whether or not to flip the handedness of the generated volumes
df_path = '/path/to/cryodrgn_viz_notebook/generated/dataframe.csv'
cuda = 0 #change cuda device for volume generation if desired
bin_thr = 1 #set to None if you don't want to binarize
downsample = 64 #boxsize at which to generate volumes; boxsize 64 is recommended
###

def generate_volumes(zvalues, outdir, **kwargs):
    '''Helper function to call cryodrgn eval_vol and generate new volumes'''
    np.savetxt(f'{outdir}/zfile.txt', zvalues)
    analysis.gen_volumes(f'{results_dir}weights.29.pkl',
                         f'{results_dir}config.pkl',
                         f'{outdir}/zfile.txt',
                         f'{outdir}', **kwargs)
    return

t0 = time.time()

#read in indices and masks
with open(f'{results_dir}z.29.pkl','rb') as f:
    z = pickle.load(f)
df = pd.read_csv(df_path, index_col = 0)
all_inds = df.index
batch_size = 1000
mask_dict = {i: mrc.parse_mrc(mask_names[i])[0].flatten() for i in mask_names}

#define volume generation choices
tmp_vol_dir = './tmp'

#initialize occupancy arrays
sub1_occupancies = np.array([])
sub2_occupancies = np.array([])

#iterate through all particles in batches
for i in range(math.ceil(len(all_inds)/batch_size)):
    ind_selected = all_inds[i*batch_size:(i+1)*batch_size]
    
    #generate volumes within batch
    generate_volumes(z[ind_selected], tmp_vol_dir, Apix=Apix, flip=flip, downsample=downsample, cuda=cuda)
    
    #read in and measure volumes
    vol_list = np.sort(glob.glob(tmp_vol_dir + '/*.mrc'))
    vol_array_sub1 = np.zeros((batch_size, len(mask_dict[subunit1])))
    vol_array_sub2 = np.zeros((batch_size, len(mask_dict[subunit2])))
    for i, vol in enumerate(vol_list):
        if bin_thr:
            data = np.where(mrc.parse_mrc(vol)[0].flatten() > bin_thr, 1, 0)
        else:
            data = mrc.parse_mrc(vol)[0].flatten()
        vol_array_sub1[i] = data*mask_dict[subunit1]
        vol_array_sub2[i] = data*mask_dict[subunit2]
        
    sub1_occupancies = np.concatenate((sub1_occupancies, vol_array_sub1.sum(axis = 1)))
    sub2_occupancies = np.concatenate((sub2_occupancies, vol_array_sub2.sum(axis = 1)))
    
    #delete volumes
    for file in vol_list:
        os.remove(file)
    os.remove(vol_list[0].split('vol')[0] + 'zfile.txt')
    
    #estimate time remaining
    dt = (time.time() - t0)
    est_time = dt/((i+1)*batch_size)*(len(all_inds)-(i+1)*batch_size)
    print(f'{dt/60} min elapsed; estimated time remaining = {est_time/60} min')
    
utils.save_pkl(sub1_occupancies, f'{output_dir}otf_{subunit1}_occupancies.pkl')
utils.save_pkl(sub2_occupancies, f'{output_dir}otf_{subunit2}_occupancies.pkl')

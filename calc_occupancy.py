import argparse
import pandas as pd
import numpy as np
from cryodrgn import mrc
from cryodrgn import analysis
from cryodrgn import utils
import os
import time
import string

def add_args(parser):
    parser.add_argument('--mapdir', type = str, required=True, help = 'Directory where sampled volumes are stored')
    parser.add_argument('--maskdir', type = str, required=True, help = 'Directory where subunit masks are stored')
    parser.add_argument('--refdir', type = str, default = None, help = 'Directory where reference maps from the atomic model are stored')
    parser.add_argument('--outdir', default = './', help = 'Directory in which to store output data')
    return parser

def check_dirname(dirname):
    if not dirname.endswith('/'):
        dirname = dirname + '/'
    return dirname

def parse_name(filename, vol_type):
    assert vol_type in ['map', 'mask', 'ref']
    if vol_type == 'mask':
        parsed = filename.split('.mrc')[0].split('Mask_')[1].split('_chain')
    elif vol_type == 'ref':
        parsed = filename.split('.mrc')[0].split('_chain')
    elif vol_type == 'map':
        parsed = filename.split('.mrc')[0].split('_')
        
    return parsed

def main(args):
    mapdir = check_dirname(args.mapdir)
    maskdir = check_dirname(args.maskdir) 
    if args.refdir:
        refdir = check_dirname(args.refdir)
    else:
        refdir = None
    outdir = check_dirname(args.outdir)
    
    total_vols = len([i for i in os.listdir(mapdir) if i.endswith('.mrc')])
    
    pdb_list = np.unique([parse_name(i, vol_type = 'mask')[0] for i in os.listdir(maskdir)])
    chain_list = list(string.ascii_lowercase)
    iterables = pd.MultiIndex.from_product([pdb_list, chain_list], names=['PDB', 'Chain'])
    occupancies = pd.DataFrame(columns = iterables)

    if not os.path.exists(outdir):
        os.mkdir(outdir)

    print('reading in masks')
    mask_dict = {}
    for maskfile in os.listdir(maskdir):
        pdb_name, chain = parse_name(maskfile, vol_type = 'mask')
        mask_dict['__'.join([pdb_name, chain])] = mrc.parse_mrc(maskdir + maskfile)[0].flatten()
    
    t_start = time.time()
    for i,mapfile in enumerate(os.listdir(mapdir)):
        if mapfile.endswith('.mrc'):
            data = mrc.parse_mrc(mapdir + mapfile)[0].flatten()
            map_num = int(parse_name(mapfile, vol_type = 'map')[-1])
            
            for mask in mask_dict.keys():
                cut = mask_dict[mask]*data
                sum_val = cut.sum()
                pdb_name, chain = mask.split('__')
                
                occupancies.at[map_num, (pdb_name, chain)] = sum_val
                
        if i%10 == 0 and i != 0:
            dt = time.time() - t_start
            est_time = dt/i*(500-i)
            print('working on map ' + str(i) + '/' + str(total_vols))
            print('estimated time remaining: ' + str(est_time) + 's')
            
    if refdir:
        print('normalizing to reference maps')
        for reffile in os.listdir(refdir):
            ref = mrc.parse_mrc(refdir + reffile)[0].flatten()
            pdb_name, chain = parse_name(reffile, vol_type = 'ref')
            ref_val = ref.sum()
        
        occupancies[(pdb_name, chain)] = occupancies[(pdb_name, chain)]/ref_val
            
    print('saving occupancies.csv')
    occupancies.to_csv(outdir + 'occupancies.csv')

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    main(add_args(parser).parse_args())

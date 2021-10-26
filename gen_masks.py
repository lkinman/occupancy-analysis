import os
import argparse
def add_args(parser):
    parser.add_argument('--mrc', required = True, help = 'MRC file used for creating the mask')
    parser.add_argument('--outdir', type = str, required = True, help='Output directory to store the masks in')
    parser.add_argument('--extend', type = str, help = 'Number of angstroms to extend initial mask by')
    return parser

def main(args):
    if not os.path.exists(args.outdir):
        os.mkdir(args.outdir)
    mask_name = str(args.outdir) + '/Mask_' + str(args.mrc).split('/')[-1]
    if not args.extend:
	    os.system('relion_mask_create --i ' + args.mrc + ' --o ' + mask_name)
    else:
        os.system('relion_mask_create --i ' + args.mrc + ' --o ' + mask_name + ' --extend_inimask ' + args.extend)
    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    main(add_args(parser).parse_args())

	

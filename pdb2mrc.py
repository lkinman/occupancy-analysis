import argparse
import os

def add_args(parser):
    parser.add_argument('--map', required=True,  help='Example map that you want to determine the occupancy of')
    parser.add_argument('--pdb', required=True, help='PDB file used for creating the mask')
    parser.add_argument('--chains', type=list, required=True, help='PDB chain used for creating the mask')
    parser.add_argument('--res', type=float, required=True, help='Resolution to filter the maps to')
    parser.add_argument('--out', type=str, required=True, help='Output directory')
    parser.add_argument('--scriptdir', type=str, required=True, help='Directory to store Chimera scripts')
    return parser

def makedir(dirname):
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    if not dirname.endswith('/'):
        dirname = dirname + '/'
    return dirname

def main(args): 
    outdir = makedir(args.out)
    scriptdir = makedir(args.scriptdir)

    script_name = scriptdir + str(args.pdb).split('/')[-1].split('.pdb')[0] + '.py'

    with open(script_name, 'w') as output:
        output.write('from chimera import runCommand as rc\n')

        open_map = '"open ' + args.map + '"'
        open_pdb = '"open ' + args.pdb + '"'
        output.write('rc(' + open_map + ')\n')
        output.write('rc(' + open_pdb + ')\n\n')
        
        num1 = 1000
        num2 = 2000

        for chain in args.chains:
            output.write('rc("sel:.' + str(chain) + '")\n')
            output.write('rc("molmap sel ' + str(args.res) + ' modelId ' + str(num1) + '")\n')
            output.write('rc("vop #' + str(num1) + ' resample onGrid #0 modelId ' + str(num2) + '")\n')
            output.write('rc("volume #' + str(num2) + ' save ' + outdir + '/' +  str(args.pdb).split('/')[-1].split('.pdb')[0] + '_chain' + str(chain) + '.mrc")\n')
            num1 = num1 + 1
            num2 = num2 + 1 

        output.write('rc("close all")\n')	
        output.write('rc("stop all")\n')
        
    command = 'chimera --nogui --script ' + script_name
    os.system(command)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    main(add_args(parser).parse_args())
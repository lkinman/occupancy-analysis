import argparse
import os

def add_args(parser):
    parser.add_argument('--map', required=True,  help='Example map that you want to determine the occupancy of')
    parser.add_argument('--pdb', required=True, help='PDB file used for creating the mask')
    parser.add_argument('--chains', type=list, required=True, help='PDB chains used for creating the mask')
    parser.add_argument('--res', type=float, required=True, help='Resolution to filter the maps to')
    parser.add_argument('--out', type=str, required=True, help='Output directory')
    parser.add_argument('--scriptdir', type=str, required=True, help='Directory to store ChimeraX scripts')
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
        output.write('from chimerax.core.commands import  run\n')

        open_map = '"open ' + args.map + '"'
        open_pdb = '"open ' + args.pdb + '"'
        output.write('run(session, ' + open_map + ')\n')
        output.write('run(session, ' + open_pdb + ')\n\n')

        for chain in args.chains:
            output.write('run(session, "molmap ' + '#2/' + str(chain) + ' ' + str(args.res) +  '")\n')
            output.write('run(session, "volume resample #3 onGrid #1")\n')
            new_name = outdir + str(args.pdb).split('/')[-1].split('.pdb')[0] + '_chain' + str(chain) + '.mrc'
            output.write('run(session, "save ' + new_name + ' #4")\n')
            output.write('run(session, "close #3-4")\n')

        output.write('run(session, "close all")\n')	
        output.write('run(session, "exit")\n')
        
    command = 'chimerax --nogui --script ' + script_name
    os.system(command)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    main(add_args(parser).parse_args())

python ../gen_mrcs.py --map 00_aligned/vol_458.mrc --pdb 00_aligned/prots1.pdb --chains abcdefghijklmnopqrstuvwxyz --res 10 --out 01_PDB_mrc --scriptdir 01_chimera_scripts
for i in ./01_PDB_mrc/*.mrc; do python ../gen_masks.py --mrc $i --outdir 02_masks; done
python ../calc_occupancy.py --mapdir 00_aligned --maskdir 02_masks --refdir 01_PDB_mrc --outdir 03_occupancies


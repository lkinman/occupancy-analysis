### Generate .mrc files from provided .pdb
Expected results stored in 01_PDB_mrc/00_expected for comparison
```
python ../gen_mrcs.py --map 00_aligned/vol_458.mrc --pdb 00_aligned/prots1.pdb --chains abcdefghijklmnopqrstuvwxyz --res 10 --out 01_PDB_mrc --scriptdir 01_chimera_scripts
```

### Generate mask files from .mrc files
Expected results stored in 02_masks/00_expected for comparison
```
for i in 01_PDB_mrc/*.mrc; do python ../gen_masks.py --mrc $i --outdir 02_masks; done
```

### Measure the occupancies of each masked region in each of the provided volumes
Expected occupancies stored at 03_occupancies/occupancies_expected.csv for comparison
```
python ../calc_occupancy.py --mapdir 00_aligned --maskdir 02_masks --refdir 01_PDB_mrc --outdir 03_occupancies
```

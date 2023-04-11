# Subunit occupancy analysis/MAVEn landing page
The software formerly known as subunit occupancy analysis (in the 2023 Nature Protocols publication) is now known as MAVEn, and incorporates several new features, including voxel PCA and on-the-fly occupancy querying of all particles in a cryoDRGN training run. All future versions will be updated in the [MAVEn repository](https://github.com/lkinman/MAVEn) rather than the occupancy-analysis repository. 


# Subunit occupancy analysis
Subunit occupancy analysis is used for the systematic analysis of compositionally-heterogeneous cryo-EM datasets. This code is designed to work downstream of [cryoDRGN](https://github.com/zhonge/cryodrgn), after users have generated a large number of maps (usually 500-1000) systematically sampling the latent space, but can be applied to any ensemble of volumes. 
  
  
## Literature
     
   
   
## Installing  
If you have an existing cryoDRGN conda environment, that environment can be directly used for all occupancy analysis scripts. The scripts require a cryoDRGN installation, so if you do not have cryoDRGN installed, instructions can be found [here](https://github.com/zhonge/cryodrgn). Note that this software is currently compatible with cryoDRGN v0.3.2. 

The additional requirements beyond cryoDRGN's own are SciPy>=1.6.0, which can be installed with:  
```
conda activate cryodrgn
conda install scipy>=1.6.0
```  
as well as RELION (install instructions [here](https://relion.readthedocs.io/en/latest/Installation.html)) and both UCSF Chimera and ChimeraX (install instructions can be found [here](https://www.cgl.ucsf.edu/chimera/download.html) for both)

To install the subunit occupancy code, simply git clone the source code:
```
git clone https://github.com/lkinman/occupancy-analysis.git
```

## Prerequisites
To conduct subunit occupancy analysis, users will need to have input maps they wish to analyze as .mrc files, as well as a PDB file or files containing the corresponding atomic model. This atomic model can be either an existent file from the PDB, or a newly-generated atomic model. The PDB file must be aligned to the experimental maps; this can be done in Chimera or ChimeraX, and should be done with a largely mature/high occupancy volume so as to allow for a good alignment. Additionally, the PDB must be segmented so that each chain represents a subunit to be independently queried for occupancy. Detailed instructions on how to segment the chains of a PDB can be found in the protocol listed in the literature section above. 

## Using  
A step-by-step protocol for using the protocol can be found in the literature listed above. A brief overview of the scripts provided is given below.  

This software comprises 3 scripts and an additional interactive Jupyter notebook. The scripts:  
**1) Take an input pdb file, which is aligned to the experimental maps and segmented into pre-defined chains delineating the subunits of interest, and convert it into a series of .mrc files.** 

The conversion of an aligned, segmented PDB file into a series of .mrc files corresponding to each chain in the PDB file is done in ChimeraX with the ```--nogui``` flag, using [the molmap command](https://www.cgl.ucsf.edu/chimerax/docs/user/commands/molmap.html) that is itself based on [EMAN's pdb2mrc function](https://blake.bcm.edu/emanwiki/PdbToMrc). 
  
```
python gen_mrcs.py --help
usage: gen_mrcs.py [-h] --map MAP --pdb PDB --chains CHAINS --res RES --out
                   OUT --scriptdir SCRIPTDIR

optional arguments:
  -h, --help            show this help message and exit
  --map MAP             Example map that you want to determine the occupancy
                        of
  --pdb PDB             PDB file used for creating the mask
  --chains CHAINS       PDB chains used for creating the mask
  --res RES             Resolution to filter the maps to
  --out OUT             Output directory
  --scriptdir SCRIPTDIR
                        Directory to store ChimeraX scripts
```  
e.g.
  
```
python gen_mrcs.py --map 00_aligned/vol_000.mrc --pdb 00_aligned/atomicmodel.pdb --chains abcdefghijklmnopqrstuvwxyz --res 5 --out 01_PDB_mrc --scriptdir 01_chimera_scripts
```  
Note that the --res flag should be changed depending on the approximate resolution of your maps. The --map flag should just be one of the ensemble of .mrc volumes you have sampled from the latent space.


**2) Take the .mrc files output by step 1 and use RELION to convert them into masks.** 
  
This script is a wrapper for ``` relion_mask_create ``` that iterates through making all the masks and systematically naming them.  
```
python gen_masks.py --help
usage: gen_masks.py [-h] --mrc MRC --outdir OUTDIR [--extend EXTEND]

optional arguments:
  -h, --help       show this help message and exit
  --mrc MRC        MRC file used for creating the mask
  --outdir OUTDIR  Output directory to store the masks in
  --extend EXTEND  Number of angstroms to extend initial mask by
```  
 e.g.   
   
 ```
 for i in ./01_PDB_mrc/*.mrc; do python gen_masks.py --mrc $i --outdir 02_masks; done
 ```  
   
**3) Read in the masks from step 2 and the experimental maps, apply each of the masks to each of the maps, (optionally) normalize to the total volume of the masked region, and finally output an occupancies.csv file containing fractional occupancy measurements for each subunit in each map.**
 
```
 python calc_occupancy.py --help
usage: calc_occupancy.py [-h] --mapdir MAPDIR --maskdir MASKDIR
                         [--refdir REFDIR] [--outdir OUTDIR]

optional arguments:
  -h, --help         show this help message and exit
  --mapdir MAPDIR    Directory where sampled volumes are stored
  --maskdir MASKDIR  Directory where subunit masks are stored
  --refdir REFDIR    Directory where reference maps from the atomic model are
                     stored
  --outdir OUTDIR    Directory in which to store output data
```
e.g.  

```
python calc_occupancy.py --mapdir 00_aligned --maskdir 02_masks --refdir 01_PDB_mrc --outdir 03_occupancies
```
   
Note that we generally recommend normalizing to the reference maps, as otherwise the signal will largely be dominated by the size of the subunit, with larger subunits showing higher occupancy. If the optional ```--refdir``` argument is not supplied, no normalization will be applied. 

## Analysis of results
An interactive Jupyter notebook is also provided to analyze the output results by performing hierarchical clustering on the outputs. This Jupyter notebook also creates scripts to interface with ChimeraX and directly visualize volumes of interest, as well as offers several tools to visualize occupancy distributions on a per-subunit basis to examine occupancy correlations between different subunits.  

## Other uses
Some users may also wish to implement subunit occupancy analysis in the absence of an atomic model, to identify particles with high occupancy of a particular region of a map. This can be done by creating a pseudo-atom or molecule in Chimera/ChimeraX, and using the ```--extend``` flag in the gen_masks.py script. Alternative methods for generating masks including using the volume eraser tool in Chimera, etc.   

Additionally, as mentioned previously, this software was designed to enable systematic analysis of the structural landscapes produced by cryoDRGN training, and requires a functioning cryoDRGN install. However, it should be possible to feed an ensemble of maps from any upstream processing software to this analysis pipeline, provided that they are supplied in the appropriate .mrc format and aligned to the same frame of reference. Depending on the upstream processing, these maps may also need to be amplitude-scaled. This functionality has not been tested. 

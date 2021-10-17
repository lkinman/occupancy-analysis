# Subunit occupancy analysis
Subunit occupancy analysis is used for the systematic analysis of compositionally-heterogeneous cryo-EM datasets. This code is designed to work downstream of [cryoDRGN](https://github.com/zhonge/cryodrgn), after users have generated a large number of maps (usually 500-1000) systematically sampling the latent space, but can be applied to any ensemble of volumes. 

## Literature
     
   
   
## Installing  
If you have an existing cryoDRGN conda environment, that environment can be directly used for all occupancy analysis scripts. The scripts require a cryoDRGN installation, so if you do not have cryoDRGN installed, instructions can be found [here](https://github.com/zhonge/cryodrgn). Note that this software is currently compatible with cryoDRGN v0.3.2. 

The additional requirements beyond cryoDRGN's own are SciPy>=1.6.0, which can be installed with:  
```
conda install scipy>=1.6.0
```  
as well as RELION (install instructions [here](https://relion.readthedocs.io/en/latest/Installation.html)) and Chimera and ChimeraX (install instructions can be found [here](https://www.cgl.ucsf.edu/chimera/download.html) for both)

To install the subunit occupancy code, simply git clone the source code:
```
git clone https://github.com/lkinman/occupancy-analysis.git
```

## Prerequisites
To conduct subunit occupancy analysis, users will need to have input maps they wish to analyze as .mrc files, as well as a PDB file or files containing the corresponding atomic model. This atomic model can be either an existent file from the PDB, or a newly-generated atomic model. The PDB file must be aligned to the experimental maps (this can be done in Chimera or ChimeraX) and must be segmented so that each chain represents a subunit of interest.

## Using  
A step-by-step protocol for using the protocol can be found in the literature listed above. A brief overview of the scripts provided is given below.  

This software comprises 3 scripts and an additional interactive Jupyter notebook. The scripts:  
1) Take an input pdb file, which is aligned to the experimental maps and segmented into pre-defined chains delineating the subunits of interest, and convert it into a series of .mrc files.
2) Take the .mrc files output by step 1 and use RELION to convert them into masks. 
3) Read in the masks from step 2 and the experimental maps, apply each of the masks to each of the maps, (optionally) normalize to the total volume of the masked region, and finally output an occupancies.csv file containing fractional occupancy measurements for each subunit in each map. 

An interactive Jupyter notebook is also provided to analyze the output results by performing hierarchical clustering on the outputs. This Jupyter notebook also creates scripts to interface with ChimeraX and directly visualize volumes of interest, as well as offers several tools to visualize occupancy distributions on a per-subunit basis to examine occupancy correlations between different subunits.  

## Other uses
Some users may also wish to implement subunit occupancy analysis in the absence of an atomic model, to identify particles with high occupancy of a particular region of a map. This can be done by creating a pseudo-atom or molecule in Chimera/ChimeraX, and using the --expand flag in the mrc2mask.py script.  

Additionally, as mentioned previously, this software was designed to enable systematic analysis of the structural landscapes produced by cryoDRGN training, and requires a functioning cryoDRGN install. However, it should be possible to feed an ensemble of maps from any upstream processing software to this analysis pipeline, provided that they are supplied in the appropriate .mrc format. This function has not been tested. 

# Sapienza

## Install

Create the Conda environment with the following command:

    conda env create -f environment.yml

Activate the environment:

    conda activate tesis-sapienza


## Generate mask from GeoTIFF

To generate a mask from a GeoTIFF and some shapefiles use the **shp_to_mask.py** script

First create the right folder structure for the shapefiles as follows:

    <shp root folder>
     -- <shp folder 1>
       -- file1.shp
     -- <shp folder 1>
       -- file2.shp
     -- <shp folder 1>
       -- file3.shp
     ...

Run the following command:

    python shp_to_mask.py <GeoTIFF file path> <shp root folder>

It will create a file named **mask.png** in the current directory


## Create shapefiles from mask

TODO
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 15:13:09 2023
This code seeks to mask multiple raster images using a shapefile
@author: Richmond
"""

import os
import fiona
import rasterio
from rasterio.mask import mask

# Open the shapefile
with fiona.open("Outputs/Vector/B.shp", "r") as shapefile:
    shapes = [feature["geometry"] for feature in shapefile]

# Define directories
dirname = 'Outputs/Raster/'
out_dir = 'Outputs/Raster/'

# Get a list of all .tif files in the directory
filenames = [f for f in os.listdir(dirname) if f.endswith('.tif')]
print(len(filenames))
print(filenames)

# Loop over each .tif file
for filename in filenames:
    # Construct the full file path for the output files
    filepath = os.path.join(dirname, filename)
    print(filepath)
    #rename if your saving in same folder to not overwrite the original data
    filename = 'Clipped_' + filename
    outpath = os.path.join(out_dir, filename)
    print(outpath)
    
    # Open the raster file
    with rasterio.open(filepath) as src:
        # Clip the raster file
        out_image, out_transform = mask(src, shapes, crop=True)
        out_meta = src.meta.copy()

    # Update metadata
    out_meta.update({
        "driver": "GTiff",
        "height": out_image.shape[1],
        "width": out_image.shape[2],
        "transform": out_transform
    })

    # Write the clipped raster to a new file
    print(f'Writing {filename} to {out_dir}')
    with rasterio.open(outpath, "w", **out_meta) as dest:
        dest.write(out_image)

print('Extract by Mask Completed!')

#Print number of files in the output dir
outfiles = [f for f in os.listdir(out_dir) if f.endswith('.tif')]
print(len(outfiles))



# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 15:55:36 2023

@author: Richmond
"""


import os
import rasterio
from rasterio.plot import show
import numpy as np
import matplotlib.pyplot as plt

# Define directories
dirname = 'Clipped/raster/'
out_fn = 'Clipped/raster/2001.tif'

# Get a list of all .tif files in the directory
filenames = [f for f in os.listdir(dirname) if f.endswith('20011201.tif')]
print(len(filenames))
print(filenames)

#Remove items that are not needed
filenames_to_remove = ['gh_landsatthermal_20011201.tif','gh_landsatqa_20011201.tif']
for item in filenames.copy():
    if item in filenames_to_remove:
        filenames.remove(item)
print(filenames)

# Define a custom sorting function
def custom_sort(item):
    # Define the order in a dictionary
    order = {'red': 1, 'green': 2, 'blue': 3, 'nir': 4, 'swir1': 5, 'swir2': 6}
    # Find the key in the item
    for key in order:
        if key in item:
            return order[key]

# Sort the list with the custom function as rasterio uses how bands appear in the list to from the 
            #composite image
filenames.sort(key=custom_sort)

print(filenames)

# Create an empty list for the filepaths
filepaths = []

# Loop over each .tif file and add them to the list
for filename in filenames:
    # Construct the full file path
    filepath = os.path.join(dirname, filename)
    filepaths.append(filepath)

#Create an empty list that will store the read bands
files_to_mosaic = [] 
      
# Open the raster bands and append to the empty list
for file in filepaths:
    src = rasterio.open(file)
    files_to_mosaic.append(src)
   
print(files_to_mosaic)  
      
# Read the data from the red, green and blue bands into numpy arrays
arrays = [src.read(1) for src in files_to_mosaic]
arrays

# Stack the arrays
stacked = np.dstack(arrays) # returns an array with the shape (rows, cols, bands)
stacked.shape

# Move the first axis to the last
#This is because the write method expects the input in a different format. 
#It expects a 3D array with the shape (bands, rows, cols)
stacked = np.moveaxis(stacked, -1, 0)
stacked.shape

# Update the metadata
out_meta = src.meta.copy()
out_meta.update({"driver": "GTiff",
                 "height": stacked.shape[1],
                 "width": stacked.shape[2],
                 "count": len(files_to_mosaic),
                 "dtype": str(stacked.dtype)})

# Write the mosaic raster to disk
with rasterio.open(out_fn, "w", **out_meta) as dest:
    dest.write(stacked)

print('Done Compositing Files')

#Visualize Output Composite Image
with rasterio.open(out_fn) as src:
    img = src.read()
    print(img.shape)
    img = np.transpose(img, (1, 2, 0))  # Move the first axis to the last
    print(img.shape)
    fig, ax = plt.subplots(figsize=(10, 10))
    show(img, ax=ax, transform=src.transform)
    plt.show()
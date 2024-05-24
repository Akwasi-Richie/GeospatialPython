# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 12:41:03 2023

@author: Richmond
"""


import pandas as pd
import numpy as np

df_water = pd.read_excel('water.xls')
df_crops = pd.read_excel('crops.xls')
df_forest = pd.read_excel('forest.xls')
df_settlement = pd.read_excel('settlement.xls')
df_range = pd.read_excel('range.xls')

df_water = df_water[['b1_2020', 'b2_2020', 'b3_2020', 'b4_2020', 'b5_2020', 'b6_2020']]
df_water.sample(5)
df_water= df_water.replace(-9999, np.nan)
df_water = df_water.dropna()
df_water = df_water.assign(LULC_class='water', LULC_value=0)
df_water.sample(5)

df_crops = df_crops[['b1_2020', 'b2_2020', 'b3_2020', 'b4_2020', 'b5_2020', 'b6_2020']]
df_crops= df_crops.replace(-9999, np.nan)
df_crops = df_crops.dropna()
df_crops = df_crops.assign(LULC_class='crops', LULC_value=1)

df_forest = df_forest[['b1_2020', 'b2_2020', 'b3_2020', 'b4_2020', 'b5_2020', 'b6_2020']] 
df_forest= df_forest.replace(-9999, np.nan)
df_forest = df_forest.dropna()
df_forest = df_forest.assign(LULC_class='forest', LULC_value=2)

df_settlement = df_settlement[['b1_2020', 'b2_2020', 'b3_2020', 'b4_2020', 'b5_2020', 'b6_2020']]
df_settlement= df_settlement.replace(-9999, np.nan)
df_settlement = df_settlement.dropna()
df_settlement = df_settlement.assign(LULC_class='settlement', LULC_value=3)

df_range = df_range[['b1_2020', 'b2_2020', 'b3_2020', 'b4_2020', 'b5_2020', 'b6_2020']]
df_range= df_range.replace(-9999, np.nan)
df_range = df_range.dropna()
df_range = df_range.assign(LULC_class='range', LULC_value=4)

frames = [df_water, df_crops, df_forest, df_settlement, df_range]
df = pd.concat(frames)
df.sample(5)

#save to a csv file to be used for training
df.to_csv('training_samples.csv', index=False)

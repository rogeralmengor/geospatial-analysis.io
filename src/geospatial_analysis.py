"""Gives a range of functions and classes to work with raster and vector data."""
import numpy as np 
import geopandas as gpd

def transform_array_to_gdf(in_arr: np.ndarray)->gpd.GeoDataFrame:
    """Transform an array to geopandas.GeoDataFrame object."""
    return 
---
title: Being kind with my future self, using Chat-GPT to explain my past code.
description: Lately, there's been a lot of talk about AI stealing our jobs as software developers. However, I prefer to see it as a tool that takes care of the boring stuff, freeing us up to focus on the more exciting aspects of our work. AI can handle tasks like dealing with documentation, fixing code, coming up with test ideas, and explaining code, allowing us to spend more time understanding what users really need and finding creative solutions. So, in today's blog post, I wanted to try something I've been meaning to do for a while. I'll put Chat-GPT to the test...
---

Lately, there's been a lot of talk about AI stealing our jobs as software developers. However, I prefer to see it as a tool that takes care of the boring stuff, freeing us up to focus on the more exciting aspects of our work. AI can handle tasks like dealing with documentation, fixing code, coming up with test ideas, and explaining code, allowing us to spend more time understanding what users really need and finding creative solutions. 

So, in today's blog post, I wanted to try something I've been meaning to do for a while. I'll put Chat-GPT to the test and use it to explain a code I wrote a couple of years ago. I'll also use some prompts to make the code even better, and improve its overall design and structure. Let's go.

### First code snippets: I was creating test raster files.

I have in an old repo, the following code. I think I used it to create a very simple raster in GeoTiff format for testing purposes.

<details>
  <summary>Code</summary>
```python linenums="1"
#!/usr/bin/env python3

from osgeo import gdal 
import numpy as np 
from osgeo import osr
import os 

# Contants for file creation

dtype = gdal.GDT_Byte
driver_name = "GTiff"
geotransform = [300000, 10, 0, 1000020, 0, -10]
x_size = 5
y_size = 5

def create_value_raster(filename):
    
    """Creates a test raster file"""
    
    driver = gdal.GetDriverByName(driver_name)
    dst_ds = driver.Create(filename, xsize = x_size, ysize= y_size,
                            bands = 1, eType= dtype)
    dst_ds.SetGeoTransform(geotransform)
    srs = osr.SpatialReference()
    srs.SetUTM(17, 1)
    srs.SetWellKnownGeogCS("WGS84")
    dst_ds.SetProjection(srs.ExportToWkt())
    array = np.array([[ x +1 for x in range(x_size)]\
                    for x in range(y_size)])
    dst_ds.GetRasterBand(1).WriteArray(array)

    dst_ds = None

def create_mask_raster(filename): 

    driver = gdal.GetDriverByName(driver_name)
    dst_ds = driver.Create(filename, xsize = 5, ysize = 5,
                            bands = 1, eType= dtype)
    dst_ds.SetGeoTransform(geotransform)
    srs = osr.SpatialReference()
    srs.SetUTM(17, 1)
    srs.SetWellKnownGeogCS("WGS84")
    dst_ds.SetProjection(srs.ExportToWkt())
    array = np.array([[ 101, 101, 0, 0, 0],
            [101, 101, 0, 202, 202],
            [101, 101, 0, 202, 202],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],])
    dst_ds.GetRasterBand(1).WriteArray(array)

    dst_ds = None


def main(): 
    
    try: 
        os.makedirs("output")

    except Exception as e:
        print(e) 

    create_value_raster("output" + "/" + "value_raster.tif")
    create_mask_raster("output" + "/" + "mask_raster.tif")
    

if __name__ == "__main__": 
    main()
```
</details>

The code does its work, however there are things that I could improve. Those improvements come from my future self (that happens all the time, I revisit some code I wrote 5 years ago, and I can only cringe).

Now, the time to ask the first question to Chat-GPT has come. In the following snippet you can find the nice question I just asked (I am always polite and try to do it even with advanced language processing systems... who knows maybe they are concious ;o) ):

<p align="center">
      <img src="./../chat_gpt_1_question.png" alt="Centered Image">
      <br>
</p>

And of course... it did it. And the answer is incredibly accurate, detailed and well documented.

<details>
    <summary>Code</summary>
```python linenums="1" 
#!/usr/bin/env python3

from osgeo import gdal
import numpy as np
from osgeo import osr
import os
```
</details>

This code imports necessary modules from the osgeo package, including gdal for geospatial data processing, osr for spatial reference system operations, and the standard os module for working with the operating system.

<details>
<summary>Code</summary>
```python linenums="1"
dtype = gdal.GDT_Byte
driver_name = "GTiff"
geotransform = [300000, 10, 0, 1000020, 0, -10]
x_size = 5
y_size = 5
```
</details>

Next, some constants are defined:

* dtype represents the data type of the raster, set to gdal.GDT_Byte.

* driver_name specifies the desired driver for creating the raster files, in this case, "GTiff" for GeoTIFF format.

* geotransform defines the geotransform parameters that describe the position and resolution of the raster data.

* x_size and y_size indicate the dimensions (width and height) of the raster.

<details>
<summary>Code</summary>
```python linenums="1"
def create_value_raster(filename):
    """Creates a test raster file"""
    driver = gdal.GetDriverByName(driver_name)
    dst_ds = driver.Create(filename, xsize=x_size, ysize=y_size, bands=1, eType=dtype)
    dst_ds.SetGeoTransform(geotransform)
    srs = osr.SpatialReference()
    srs.SetUTM(17, 1)
    srs.SetWellKnownGeogCS("WGS84")
    dst_ds.SetProjection(srs.ExportToWkt())
    array = np.array([[x + 1 for x in range(x_size)] for x in range(y_size)])
    dst_ds.GetRasterBand(1).WriteArray(array)
    dst_ds = None
```
</details>

The create_value_raster function creates a test raster file with a filename provided as an argument. It uses the GDAL driver to create the raster file, setting its dimensions, number of bands, data type, geotransform, and spatial reference information. It then generates an array with increasing values and writes it to the raster band using WriteArray.

<details>
<summary>Code</summary>
```python linenums="1"
def create_mask_raster(filename):
    driver = gdal.GetDriverByName(driver_name)
    dst_ds = driver.Create(filename, xsize=5, ysize=5, bands=1, eType=dtype)
    dst_ds.SetGeoTransform(geotransform)
    srs = osr.SpatialReference()
    srs.SetUTM(17, 1)
    srs.SetWellKnownGeogCS("WGS84")
    dst_ds.SetProjection(srs.ExportToWkt())
    array = np.array([[101, 101, 0, 0, 0],
                      [101, 101, 0, 202, 202],
                      [101, 101, 0, 202, 202],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0]])
    dst_ds.GetRasterBand(1).WriteArray(array)
    dst_ds = None
    ```
</details>

The create_mask_raster function is similar to create_value_raster but generates a mask raster file with different values.

<details>
<summary>Code</summary>
```python linenums="1"
def main():
    try:
        os.makedirs("output")
    except Exception as e:
        print(e)
    create_value_raster("output" + "/" + "value_raster.tif")
    create_mask_raster("output" + "/" + "mask_raster.tif")
```
</details>

The main function is the entry point of the script. It attempts to create an "output" directory using os.makedirs. If the directory already exists, it will raise an exception which is printed to the console. Then, it calls the create_value_raster and create_mask_raster functions to create the value and mask raster files within the "output" directory.

<details>
<summary>Code</summary>
```python linenums="1"
if __name__ == "__main__":
    main()
```
</details>

Finally, if __name__ == "__main__": ensures that the main function is executed only when the script is run directly, not when imported as a module.

Usefulness: This code is useful for generating test raster files for geospatial data processing tasks. It showcases the use of the GDAL library to create raster files with specific dimensions, data types, geotransform parameters, and spatial reference information. The generated raster files can be used as sample data for testing and developing algorithms, models, or applications that work with geospatial data.

## Improving the code

Now I would like to introduce some improvements in my code. I would like to introduce some type declarations for the functions, and also a nicely formatted docstring with parameters and return values specified. Let's do it.

<p align="center">
      <img src="./../chat_gpt_2_question.png" alt="Centered Image">
      <br>
</p>

<details>
<summary>Code</summary>
```python linenums="1"
#!/usr/bin/env python3

from osgeo import gdal
import numpy as np
from osgeo import osr
import os

# Constants for file creation
dtype: int = gdal.GDT_Byte
driver_name: str = "GTiff"
geotransform: list[float] = [300000, 10, 0, 1000020, 0, -10]
x_size: int = 5
y_size: int = 5


def create_value_raster(filename: str) -> None:
    """
    Creates a test raster file.

    Args:
        filename (str): The name of the output raster file.

    Returns:
        None
    """
    driver: gdal.Driver = gdal.GetDriverByName(driver_name)
    dst_ds: gdal.Dataset = driver.Create(filename, xsize=x_size, ysize=y_size, bands=1, eType=dtype)
    dst_ds.SetGeoTransform(geotransform)
    srs: osr.SpatialReference = osr.SpatialReference()
    srs.SetUTM(17, 1)
    srs.SetWellKnownGeogCS("WGS84")
    dst_ds.SetProjection(srs.ExportToWkt())
    array: np.ndarray = np.array([[x + 1 for x in range(x_size)] for x in range(y_size)])
    dst_ds.GetRasterBand(1).WriteArray(array)
    dst_ds = None


def create_mask_raster(filename: str) -> None:
    """
    Creates a mask raster file.

    Args:
        filename (str): The name of the output raster file.

    Returns:
        None
    """
    driver: gdal.Driver = gdal.GetDriverByName(driver_name)
    dst_ds: gdal.Dataset = driver.Create(filename, xsize=5, ysize=5, bands=1, eType=dtype)
    dst_ds.SetGeoTransform(geotransform)
    srs: osr.SpatialReference = osr.SpatialReference()
    srs.SetUTM(17, 1)
    srs.SetWellKnownGeogCS("WGS84")
    dst_ds.SetProjection(srs.ExportToWkt())
    array: np.ndarray = np.array(
        [
            [101, 101, 0, 0, 0],
            [101, 101, 0, 202, 202],
            [101, 101, 0, 202, 202],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ]
    )
    dst_ds.GetRasterBand(1).WriteArray(array)
    dst_ds = None


def main() -> None:
    """
    Main function that creates the value and mask raster files.

    Returns:
        None
    """
    try:
        os.makedirs("output")
    except Exception as e:
        print(e)
    create_value_raster("output" + "/" + "value_raster.tif")
    create_mask_raster("output" + "/" + "mask_raster.tif")


if __name__ == "__main__":
    main()
```
</details>

Of course the code now looks better with type declarations and a docstring showing the arguments and

their type, as well as the return values. 

Let's see if it can make some changes to a test suite I created within the directory. By now, the test suit runs correctly, however I would like to test Chat-GPT to introduce some changes. 

## Test Code

The next code snippet is the contents of a file called text_pixel_stats.py:

<details>
<summary>Code</summary>
```python linenums="1"
#!/usr/bin/env python3

import unittest
import numpy as np 
from osgeo import gdal
import subprocess
import pandas as pd


def return_index_2D_array(arr, val): 

    """Returns the index for valid data in array,
    as a lists of tuple, with every tuple
    containing the valid coordinate positions
    in image for every pixel""" 
    
    result =  np.where(arr != val)
    rows = result[0].astype("uint8")
    cols = result[1].astype("uint8")
    listOfCoordinates = list(zip(rows, cols))
    return listOfCoordinates

def return_image_coordinate(x, y, gt):

    """
    From pixel coordinates (x,y) returns
    the image coordinate. It needs the
    Geotransform parameters as list (gt)
    """
    xoffset = gt[0]
    px_w = gt[1]
    rot1 = gt[2]
    yoffset = gt[3]
    rot2 = gt[4]
    px_h = gt[5]

    xgeo = px_w * x + rot1 * y + xoffset
    ygeo = rot2 * x + px_h * y + yoffset
    xgeo += px_w / 2.0
    ygeo += px_h / 2

    return xgeo, ygeo 


class TestPixelStats(unittest.TestCase):

    def masking_values(self, arr1, pixel_val):

        """Creates a bool mask, related to invalid
        pixels in an array. True belong a valid
        pixels, where 'pixel_value' is not found"""
        
        mask = ((arr1 != pixel_val))

        return mask 


    def change_dtype_array(self, arr, dtype): 
        
        """Changes the data type of array"""
        return arr.astype(dtype)
       

    def return_index_2D_array(self, arr, val): 

        """Returns the index for valid data in array,
        as a lists of tuple, with every tuple
        containing the valid coordinate positions
        in image for every pixel""" 
        
        result =  np.where(arr != val)
        rows = result[0].astype("uint8")
        cols = result[1].astype("uint8")
        listOfCoordinates = list(zip(rows, cols))
        return listOfCoordinates

    def return_image_coordinate(self, x, y, gt):

        """
        From pixel coordinates (x,y) returns
        the image coordinate. It needs the
        Geotransform parameters as list (gt)
        """
        xoffset = gt[0]
        px_w = gt[1]
        rot1 = gt[2]
        yoffset = gt[3]
        rot2 = gt[4]
        px_h = gt[5]

        xgeo = px_w * x + rot1 * y + xoffset
        ygeo = rot2 * x + px_h * y + yoffset
        xgeo += px_w / 2.0
        ygeo += px_h / 2

        return xgeo, ygeo 


    def setUp(self): 
        
        """ The setup files to run this tests are
        located in the output folder, and they are
        created with the create_test_files.py script
        """

        self.values_path = "output/value_raster.tif" 
        self.mask_path = "output/mask_raster.tif"

        self.in_ds_values = gdal.Open(self.values_path)
        self.in_ds_mask = gdal.Open(self.mask_path)
        
        self.values_arr = np.array(self.in_ds_values.GetRasterBand(1)\
                        .ReadAsArray()) 
        self.mask_arr = np.array(self.in_ds_mask.GetRasterBand(1).\
                        ReadAsArray())


    def test_masking_values(self):
       
        """Tests if after creating a boolean mask
        with True values returned where valid data
        are located, and False whenever the invalid
        value is found in the array. In this case
        we take 0 as the invalid value"""

        mask = self.masking_values(self.mask_arr, 0)
        data = np.where(mask == False, np.nan, self.values_arr)
        data = self.change_dtype_array(data, "uint8")
        should_be = np.array([[1, 2, np.nan, np.nan, np.nan],
                            [1, 2, np.nan, 4, 5],
                            [1, 2, np.nan, 4, 5],
                            [np.nan, np.nan, np.nan, np.nan, np.nan],
                            [np.nan, np.nan, np.nan, np.nan, np.nan]])
        should_be = self.change_dtype_array(should_be, "uint8") 
        self.assertEqual(data.tolist(), should_be.tolist())

    def testing_return_index_2D_array(self): 
            
        """Tests if position coordinates in image are returned
        from a value array. Valid pixels are the ones different
        of 0"""

        mask = self.masking_values(self.mask_arr, 0) 
        data = np.where(mask == False, 0, self.values_arr)
        data = self.change_dtype_array(data, "uint8")
        index_valid_data = self.return_index_2D_array(data, 0)
        list_of_coordinates = [(0,0), (0,1),
                                (1,0), (1,1),(1,3), (1,4),
                                (2,0), (2,1),(2,3), (2,4)]
        self.assertEqual(index_valid_data, list_of_coordinates)


    def testing_return_pos_coordinates_(self):

        """Tests if position coordinates for  a pixel position
        on an image are returned, for valid data. In this case 
        no valid data is 0"""

        mask = self.masking_values(self.mask_arr, 0) 
        data = np.where(mask == False, 0, self.values_arr)
        data = self.change_dtype_array(data, "uint8")
        index_valid_data = self.return_index_2D_array(data, 0)
        list_of_coordinates = [(0,0), (0,1),
                                (1,0), (1,1),(1,3), (1,4),
                                (2,0), (2,1),(2,3), (2,4)]
        gt = self.in_ds_values.GetGeoTransform() 
        test_posx = list_of_coordinates[0][0]
        test_posy = list_of_coordinates[0][1]
        geo_posx, geo_posy = self.return_image_coordinate(test_posx,\
                                                        test_posy,\
                                                        gt)
        self.assertEqual(geo_posx, 300005)
        self.assertEqual(geo_posy, 1000015)


class TestPixelStats(unittest.TestCase):

    def testing_workflow(self): 
        
        values_ds = gdal.Open("output/value_raster.tif")
        mask_ds = gdal.Open("output/mask_raster.tif")
        
        ## Masking out valid data from mask raster 
        ## output/mask_raster.tif plays the role that 
        ## the rasterized version of the vector with 
        ## the "burned" class column, that will become
        ## the raster values 
        
        print("-- Reading arrays for Values, FID and Proximity --")
        values_arr = np.array(values_ds.GetRasterBand(1)\
                        .ReadAsArray())
        mask_arr_original = np.array(mask_ds.GetRasterBand(1)\
                        .ReadAsArray())
        
        print("-- Extracting only valid data and fid --")
        values_arr = values_arr[mask_arr_original != 0] 
        print(values_arr.shape)
        mask_arr = mask_arr_original[mask_arr_original != 0]
        print(mask_arr.shape)

        print("-- Getting xcoor and ycoor for pixels --")
        gt = mask_ds.GetGeoTransform() 
        index_valid_data = return_index_2D_array(mask_arr_original, 0)
        print(index_valid_data) 
        coor_valid_data = np.array([return_image_coordinate(x[0], x[1], gt) for x in index_valid_data])
        x_coor_ = np.array([item[0] for item in coor_valid_data.tolist()])
        y_coor_ = np.array([item[1] for item in coor_valid_data.tolist()])
        
        print(x_coor_)
        print(y_coor_)

        Data = pd.DataFrame(values_arr, columns = ["TF_VALUE"])
        Data["FID"] = mask_arr
        Data["X_coor"] = x_coor_
        Data["Y_coor"] = y_coor_
        print(Data)


if __name__ == '__main__':
    unittest.main()
```
</details>

Even though the function works, there is a couple of things that I don't like about my past code. First I declared some functions, that I copy 1:1 as methods within the Test Suite. I would like to get rid of these code duplication. 

<p align="center">
      <img src="./../chat_gpt_3_question.png" alt="Centered Image">
      <br>
</p>

The following is the code generated by the prompt:

<details>
<summary>Code</summary>
```python linenums="1"
#!/usr/bin/env python3

import unittest
import numpy as np
from osgeo import gdal
import subprocess
import pandas as pd


def return_index_2D_array(arr, val):
    """Returns the index for valid data in an array,
    as a list of tuples, with each tuple containing the
    coordinates of valid data in the image for each pixel"""
    result = np.where(arr != val)
    rows = result[0].astype("uint8")
    cols = result[1].astype("uint8")
    listOfCoordinates = list(zip(rows, cols))
    return listOfCoordinates


def return_image_coordinate(x, y, gt):
    """
    From pixel coordinates (x,y), returns
    the image coordinates. It requires the
    Geotransform parameters as a list (gt).
    """
    xoffset = gt[0]
    px_w = gt[1]
    rot1 = gt[2]
    yoffset = gt[3]
    rot2 = gt[4]
    px_h = gt[5]

    xgeo = px_w * x + rot1 * y + xoffset
    ygeo = rot2 * x + px_h * y + yoffset
    xgeo += px_w / 2.0
    ygeo += px_h / 2

    return xgeo, ygeo


class TestPixelStats(unittest.TestCase):
    def masking_values(self, arr1, pixel_val):
        """Creates a boolean mask related to invalid
        pixels in an array. True belongs to valid
        pixels, where 'pixel_value' is not found"""
        mask = arr1 != pixel_val
        return mask

    def change_dtype_array(self, arr, dtype):
        """Changes the data type of an array"""
        return arr.astype(dtype)

    def setUp(self):
        """The setup files to run these tests are
        located in the output folder and are created
        with the create_test_files.py script"""
        self.values_path = "output/value_raster.tif"
        self.mask_path = "output/mask_raster.tif"

        self.in_ds_values = gdal.Open(self.values_path)
        self.in_ds_mask = gdal.Open(self.mask_path)

        self.values_arr = np.array(self.in_ds_values.GetRasterBand(1).ReadAsArray())
        self.mask_arr = np.array(self.in_ds_mask.GetRasterBand(1).ReadAsArray())

    def test_masking_values(self):
        """Tests if after creating a boolean mask
        with True values returned where valid data
        are located, and False whenever the invalid
        value is found in the array. In this case,
        we take 0 as the invalid value"""
        mask = self.masking_values(self.mask_arr, 0)
        data = np.where(mask == False, np.nan, self.values_arr)
        data = self.change_dtype_array(data, "uint8")
        should_be = np.array(
            [
                [1, 2, np.nan, np.nan, np.nan],
                [1, 2, np.nan, 4, 5],
                [1, 2, np.nan, 4, 5],
                [np.nan, np.nan, np.nan, np.nan, np.nan],
                [np.nan, np.nan, np.nan, np.nan, np.nan],
            ]
        )
        should_be = self.change_dtype_array(should_be, "uint8")
        self.assertEqual(data.tolist(), should_be.tolist())

    def testing_return_index_2D_array(self):
        """Tests if position coordinates in the image are returned
        from a value array. Valid pixels are the ones different
        from 0"""
        mask = self.masking_values(self.mask_arr, 0)
        data = np.where(mask == False, 0, self.values_arr)
        data = self.change_dtype_array(data, "uint8")
        index_valid_data = return_index_2D_array(data, 0)
        list_of_coordinates = [
            (0, 0),
            (0, 1),
            (1, 0),
            (1, 1),
            (1, 3),
            (1, 4),
            (2, 0),
            (2, 1),
            (2, 3),
            (2, 4),
        ]
        self.assertEqual(index_valid_data, list_of_coordinates)

    def testing_return_pos_coordinates(self):
        """Tests if position coordinates for a pixel position
        on an image are returned for valid data. In this case,
        no valid data is 0"""
        mask = self.masking_values(self.mask_arr, 0)
        data = np.where(mask == False, 0, self.values_arr)
        data = self.change_dtype_array(data, "uint8")
        index_valid_data = return_index_2D_array(data, 0)
        list_of_coordinates = [
            (0, 0),
            (0, 1),
            (1, 0),
            (1, 1),
            (1, 3),
            (1, 4),
            (2, 0),
            (2, 1),
            (2, 3),
            (2, 4),
        ]
        gt = self.in_ds_values.GetGeoTransform()
        test_posx = list_of_coordinates[0][0]
        test_posy = list_of_coordinates[0][1]
        geo_posx, geo_posy = return_image_coordinate(test_posx, test_posy, gt)
        self.assertEqual(geo_posx, 300005)
        self.assertEqual(geo_posy, 1000015)


if __name__ == "__main__":
    unittest.main()
```
</details>

And the tests still run:

!!! success
    ```linux
    $ python -m unittest
    ...
    ----------------------------------------------------------------------
    Ran 3 tests in 0.010s
    ```

## Refactoring the test class

Another improvement we can introduce is to remove methods, and make them functions outside of the Test Class body. Let's do it.

<p align="center">
      <img src="./../chat_gpt_4_question.png" alt="Centered Image">
      <br>
</p>

<details>
<summary>Code</summary>
```python linenums="1"
#!/usr/bin/env python3

import unittest
import numpy as np
from osgeo import gdal
import subprocess
import pandas as pd


def masking_values(arr1, pixel_val):
    """Creates a boolean mask related to invalid
    pixels in an array. True belongs to valid
    pixels, where 'pixel_value' is not found"""
    mask = arr1 != pixel_val
    return mask


def change_dtype_array(arr, dtype):
    """Changes the data type of an array"""
    return arr.astype(dtype)


def return_index_2D_array(arr, val):
    """Returns the index for valid data in an array,
    as a list of tuples, with each tuple containing the
    coordinates of valid data in the image for each pixel"""
    result = np.where(arr != val)
    rows = result[0].astype("uint8")
    cols = result[1].astype("uint8")
    listOfCoordinates = list(zip(rows, cols))
    return listOfCoordinates


def return_image_coordinate(x, y, gt):
    """
    From pixel coordinates (x,y), returns
    the image coordinates. It requires the
    Geotransform parameters as a list (gt).
    """
    xoffset = gt[0]
    px_w = gt[1]
    rot1 = gt[2]
    yoffset = gt[3]
    rot2 = gt[4]
    px_h = gt[5]

    xgeo = px_w * x + rot1 * y + xoffset
    ygeo = rot2 * x + px_h * y + yoffset
    xgeo += px_w / 2.0
    ygeo += px_h / 2

    return xgeo, ygeo


class TestPixelStats(unittest.TestCase):
    def setUp(self):
        """The setup files to run these tests are
        located in the output folder and are created
        with the create_test_files.py script"""
        self.values_path = "output/value_raster.tif"
        self.mask_path = "output/mask_raster.tif"

        self.in_ds_values = gdal.Open(self.values_path)
        self.in_ds_mask = gdal.Open(self.mask_path)

        self.values_arr = np.array(self.in_ds_values.GetRasterBand(1).ReadAsArray())
        self.mask_arr = np.array(self.in_ds_mask.GetRasterBand(1).ReadAsArray())

    def test_masking_values(self):
        """Tests if after creating a boolean mask
        with True values returned where valid data
        are located, and False whenever the invalid
        value is found in the array. In this case,
        we take 0 as the invalid value"""
        mask = masking_values(self.mask_arr, 0)
        data = np.where(mask == False, np.nan, self.values_arr)
        data = change_dtype_array(data, "uint8")
        should_be = np.array(
            [
                [1, 2, np.nan, np.nan, np.nan],
                [1, 2, np.nan, 4, 5],
                [1, 2, np.nan, 4, 5],
                [np.nan, np.nan, np.nan, np.nan, np.nan],
                [np.nan, np.nan, np.nan, np.nan, np.nan],
            ]
        )
        should_be = change_dtype_array(should_be, "uint8")
        self.assertEqual(data.tolist(), should_be.tolist())

    def testing_return_index_2D_array(self):
        """Tests if position coordinates in the image are returned
        from a value array. Valid pixels are the ones different
        from 0"""
        mask = masking_values(self.mask_arr, 0)
        data = np.where(mask == False, 0, self.values_arr)
        data = change_dtype_array(data, "uint8")
        index_valid_data = return_index_2D_array(data, 0)
        list_of_coordinates = [
            (0, 0),
            (0, 1),
            (1, 0),
            (1, 1),
            (1, 3),
            (1, 4),
            (2, 0),
            (2, 1),
            (2, 3),
            (2, 4),
        ]
        self.assertEqual(index_valid_data, list_of_coordinates)

    def testing_return_pos_coordinates(self):
        """Tests if position coordinates for a pixel position
        on an image are returned for valid data. In this case,
        no valid data is 0"""
        mask = masking_values(self.mask_arr, 0)
        data = np.where(mask == False, 0, self.values_arr)
        data = change_dtype_array(data, "uint8")
        index_valid_data = return_index_2D_array(data, 0)
        list_of_coordinates = [
            (0, 0),
            (0, 1),
            (1, 0),
            (1, 1),
            (1, 3),
            (1, 4),
            (2, 0),
            (2, 1),
            (2, 3),
            (2, 4),
        ]
        gt = self.in_ds_values.GetGeoTransform()
        test_posx = list_of_coordinates[0][0]
        test_posy = list_of_coordinates[0][1]
        geo_posx, geo_posy = return_image_coordinate(test_posx, test_posy, gt)
        self.assertEqual(geo_posx, 300005)
        self.assertEqual(geo_posy, 1000015)


if __name__ == "__main__":
    unittest.main()
```
</details>

In this re-written version of the test suite by Chat-GPT, the masking_values and change_dtype_array functions are declared outside the TestPixelStats class and are utilized directly within the test methods.

## What if pytest?

My second improvement in the test suite is to change the unittest framework for the pytest framework. I will ask Chat-GPT to translate the unittest to a pytest, use fixtures to replace the setUp method, and finally do some more improvements like creating better docstrings for the functions, and giving better formatted docstrings. The reason behind changing to pytest is personal. Even though unittest is part of the standard library, I find pytest less boiler plate.

<p align="center">
      <img src="./../chat_gpt_5_question.png" alt="Centered Image">
      <br>
</p>

<details>
<summary>Code</summary>
```python linenums="1"
import pytest
import numpy as np
from osgeo import gdal
from typing import List, Tuple


def masking_values(arr1: np.ndarray, pixel_val: int) -> np.ndarray:
    """
    Creates a boolean mask related to invalid pixels in an array.
    True belongs to valid pixels, where 'pixel_value' is not found.
    """
    mask = arr1 != pixel_val
    return mask


def change_dtype_array(arr: np.ndarray, dtype: str) -> np.ndarray:
    """Changes the data type of an array."""
    return arr.astype(dtype)


def return_index_2D_array(arr: np.ndarray, val: int) -> List[Tuple[int, int]]:
    """
    Returns the index for valid data in the array as a list of tuples.
    Each tuple contains the coordinates of valid data in the image for each pixel.
    """
    result = np.where(arr != val)
    rows = result[0].astype("uint8")
    cols = result[1].astype("uint8")
    listOfCoordinates = list(zip(rows, cols))
    return listOfCoordinates


def return_image_coordinate(x: int, y: int, gt: List[float]) -> Tuple[float, float]:
    """
    From pixel coordinates (x,y), returns the image coordinates.
    It requires the Geotransform parameters as a list (gt).
    """
    xoffset, px_w, rot1, yoffset, rot2, px_h = gt

    xgeo = px_w * x + rot1 * y + xoffset
    ygeo = rot2 * x + px_h * y + yoffset
    xgeo += px_w / 2.0
    ygeo += px_h / 2

    return xgeo, ygeo


@pytest.fixture
def test_data():
    values_path = "output/value_raster.tif"
    mask_path = "output/mask_raster.tif"
    in_ds_values = gdal.Open(values_path)
    in_ds_mask = gdal.Open(mask_path)
    values_arr = np.array(in_ds_values.GetRasterBand(1).ReadAsArray())
    mask_arr = np.array(in_ds_mask.GetRasterBand(1).ReadAsArray())
    return values_arr, mask_arr


def test_masking_values(test_data):
    """Tests if after creating a boolean mask with True values returned where valid data
    are located, and False whenever the invalid value is found in the array. In this case,
    we take 0 as the invalid value."""
    values_arr, mask_arr = test_data
    mask = masking_values(mask_arr, 0)
    data = np.where(mask == False, np.nan, values_arr)
    data = change_dtype_array(data, "uint8")
    should_be = np.array(
        [
            [1, 2, np.nan, np.nan, np.nan],
            [1, 2, np.nan, 4, 5],
            [1, 2, np.nan, 4, 5],
            [np.nan, np.nan, np.nan, np.nan, np.nan],
            [np.nan, np.nan, np.nan, np.nan, np.nan],
        ]
    )
    should_be = change_dtype_array(should_be, "uint8")
    assert np.array_equal(data, should_be)


def test_return_index_2D_array(test_data):
    """Tests if position coordinates in the image are returned from a value array.
    Valid pixels are the ones different from 0."""
    values_arr, mask_arr = test_data
    mask = masking_values(mask_arr, 0)
    data = np.where(mask == False, 0, values_arr)
    data = change_dtype_array(data, "uint8")
    index_valid_data = return_index_2D_array(data, 0)
    list_of_coordinates = [
        (0, 0),
        (0, 1),
        (1, 0),
        (1, 1),
        (1, 3),
        (1, 4),
        (2, 0),
        (2, 1),
        (2, 3),
        (2, 4),
    ]
    assert index_valid_data == list_of_coordinates


def test_return_image_coordinate(test_data):
    """Tests if position coordinates for a pixel position on an image are returned
    for valid data. In this case, no valid data is 0."""
    values_arr, mask_arr = test_data
    mask = masking_values(mask_arr, 0)
    data = np.where(mask == False, 0, values_arr)
    data = change_dtype_array(data, "uint8")
    index_valid_data = return_index_2D_array(data, 0)
    list_of_coordinates = [
        (0, 0),
        (0, 1),
        (1, 0),
        (1, 1),
        (1, 3),
        (1, 4),
        (2, 0),
        (2, 1),
        (2, 3),
        (2, 4),
    ]
    gt = gdal.Open("output/value_raster.tif").GetGeoTransform()
    test_posx = list_of_coordinates[0][0]
    test_posy = list_of_coordinates[0][1]
    geo_posx, geo_posy = return_image_coordinate(test_posx, test_posy, gt)
    assert geo_posx == 300005
    assert geo_posy == 1000015
```
</details>

I ran the tests and the feedback is still positive.
!!! success
    ```linux
    $ python -m pytest
    =============================================================== test session starts ================================================================
    platform win32 -- Python 3.10.4, pytest-7.2.0, pluggy-1.0.0
    rootdir: C:\Users\almrog\pixel_stats
    plugins: anyio-3.6.2
    collected 3 items

    test_pixel_stats.py ...                                                                                                                       [100%]

    ================================================================ 3 passed in 0.32s =================================================================
    ```

In this version, the code uses the pytest framework and fixtures to replace the setUp method. The functions masking_values, change_dtype_array, return_index_2D_array, and return_image_coordinate are declared outside the test class and are utilized directly within the test functions. The code includes type hints and improved docstrings for better readability and clarity.

## Conclusion

Chat-GPT (or advanced language processing systems) can indeed be intimidating for software developers. These systems not only provide code solutions but also offer explanations and improvements, almost automatically. However, just like any tool that facilitates work for professionals (such as chainsaws for forestry workers or cranes for construction workers), language processing systems that can translate ideas into code are useful if you have a solid understanding of your work, you know relevant concepts, and know what results you expect. In other words, you could eventually arrive at the same solution on your own, but it would undoubtedly take more time. At present, I am thrilled about these advancements that make our lives as programmers easier and allow us to focus on software design and delivering solutions to our clients.
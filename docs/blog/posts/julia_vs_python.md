---
title: Performance benchmarking for Julia and Python in a geospatial task.
description: This post is more a comparison of two programming languages to perform the same task. One is Python, the language with which I started in this programming world, and the other is Julia, which I am currently ...
---

<p align="center">
    <img src="./../Benchmarking_Python_vs_Julia.png" alt="Centered Image" width="300" height="200">
    <br>
</p>

A little while ago, I was confronted with a question. If you could start again to learn programming for geospatial analysis, where would you start?

Knowing that the big geospatial data domains are raster data on the one hand, and vectors on the other, I would start with raster data first.

Maybe this decision responds to something totally subjective, but I find that raster data allow us to review some topics such as time series analysis, raster algebra, geotransform, geographic vs projected coordinate systems, etc. If you find this statement out of place, or have a preference for vector data over raster data for getting started in the world of geospatial data programming, feel free to weigh in with your opinion to the contrary in the comment box.

With that cleared up. I guess if you ask me what task would be good to start with, I would say a small script to calculate the normalized vegetation index (NDVI). Here we can review the concepts of raster algebra, creating a raster output to contain the results of the calculation and writing the raster to our file system.

This post is more a comparison of two programming languages to perform the same task. One is Python, the language with which I started in this programming world, and the other is Julia, which I am currently exploring in order to see the advantages over interpreted languages like Python.

The promises of Julia have been trumpeting across many programming blogs. A language that combines the syntax of a high level language, with the speed of a low level language, is what we have been promised.

So I wanted to do this benchmarking between these two languages for the following task: calculate two arrays of integer values. The dimension of the array will be incremented in a "FOR" loop of a list of numbers that define the dimension in the x-direction and the y-direction of the array.
Then these two matrices that simulate the values of a red and a near infrared band, will be used to calculate a normalized difference index (simulating the NDVI index), to finally write the results in an output raster. We didn't add any spatial reference to the raster datasets, for this is not the main focus of this post.

The codes are posted here below.

<details>
<summary>Python Code</summary>
```python linenums="1"
#******************************************************************************
#                     Python Code 
#                     NDVI Calculation
#******************************************************************************

from osgeo import gdal
import numpy
import os
import time 
import numpy as np 

array_sizes = [2500, 5000, 10000, 11000, 12000, 13000, 15000,
              16000, 17000, 18000, 19000, 20000]

def main():
    for i in array_sizes: 
        start_time = time.time()

        b3 = np.random.randint(200, 900, size=(i, i))
        b4 = np.random.randint(800, 5000, size=(i, i))

        ndvi = (b4 - b3)/(b4 + b3)

        drv = gdal.GetDriverByName ( "GTiff" )
        output_filename = str(i) +  "_python_NDVI.tif"
        dst_ds = drv.Create (output_filename, i, i, 1, 
               gdal.GDT_Float64)
        dst_ds.GetRasterBand(1).WriteArray ( ndvi.astype (np.float32) )
        dst_ds = None

        proc_time = time.time() - start_time 
        print(f"Processing time {i}x{i}:::" + str(proc_time))

if __name__ == "__main__":
    main()
```
</details>

<details>
<summary>Julia Code</summary>
```julia linenums="1"
#******************************************************************************
#                   Julia Code
#                   NDVI Calculation
#******************************************************************************

using ArchGDAL
using  Glob
using TickTock


print("Current directory: ", pwd()) 


array_sizes = [2500, 5000, 10000, 11000, 12000, 13000, 15000,
              16000, 17000, 18000, 19000, 20000]

#define a function for the raster algebra
function ndviCal(red,nir)
    #ndviArray = (nir - red)/(nir + red)
    ndviArray = Float64.((nir .- red)./(red .+ nir))[:,:,1]
    return(ndviArray)
end

#foreach(array_sizes) do f
for i in array_sizes
    tick()
    redArrayFloat = Float64.(rand(200: 900, i, i))
    nirArrayFloat = Float64.(rand(800: 5000, (i, i)))
    ndviArray = ndviCal(redArrayFloat,nirArrayFloat)
    print(i)
    print("x")
    print(i)
    #print(ndviBand)
    string_array_size = string(i)
    output_name = string_array_size * "_julia_NDVI.tif" 
    ArchGDAL.create(
    output_name,
    driver = ArchGDAL.getdriver("GTiff"),
    width=i,
    height=i,
    nbands=1,
    dtype=Float64
    ) do output_dataset
    ArchGDAL.write!(output_dataset, ndviArray, 1)
    tock()
    end
end
```
</details>


Below we collect the data in a table about the performance in seconds of each of the scripts for a variable input data size.

<p align="center">
      <img src="./../Table.png" alt="Centered Image">
      <br>
</p>

We can observe that as the number of elements to process increases, the difference between the processing time between Julia and Python also increases. We can also observe that there is almost a difference of 5 seconds for a number of 400 million elements which would be a matrix of 20 000 x 20 000.

Finally, we can see graphically in the following figure the plotting of the execution times of each program written in Python and Julia vs. the number of elements to be processed.

<p align="center">
      <img src="./../Benchmarking_Python_vs_Julia.png" alt="Centered Image">
      <br>
</p>

Something interesting is to see that in the first review of the for loop Python recorded a faster execution time than Julia. The explanation for this is the variable type checking that takes place in the for loop. While Python has to know what type of variable it is in each of the cycles of the for loop, this process is done once and just once by Julia. 

In this post, we have been able to see the differences between Julia and Python for a simple geospatial task. Julia's runtime is faster for all but the first input size compared to Python. Some thoughts on why this may be were also given.
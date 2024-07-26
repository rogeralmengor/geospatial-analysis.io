## 💾 **Download imagery using the Asyncio library** 

Python has become the go-to programming language for data analysts and AI professionals in recent years. While it's praised for its simplicity and extensive libraries, developers often criticize its speed. However, by optimizing code and leveraging Python's built-in concurrency features, we can significantly improve performance, especially for I/O-bound tasks.
In this practical tutorial, we'll explore two approaches to downloading satellite imagery using the Google Earth Engine API: a sequential method and an asynchronous method using asyncio. Asyncio, introduced in Python 3.4 (2014), is particularly well-suited for I/O-bound tasks like API calls and file downloads.
We'll demonstrate these concepts by downloading Sentinel-2 satellite images for a region in David, Chiriquí, Panama. Our experiment will compare the performance of both methods, providing insights into the benefits of asynchronous programming for data retrieval tasks.
This tutorial focuses on practical implementation rather than deep theoretical concepts. By the end, you'll have a better understanding of how to optimize Python code for I/O-bound scenarios, enhancing your geospatial data processing toolkit. Let's start with the code explanation:

### 1. Import statements and initialization:
<summary>Code</summary>
```python
import os
import pathlib
import time
import asyncio
from functools import partial

import ee
import geemap
import nest_asyncio

# Apply nest_asyncio to allow running asyncio within Jupyter or similar environments
nest_asyncio.apply()

# Initialize Earth Engine
try:
    ee.Initialize()
except Exception:
    ee.Authenticate()
    ee.Initialize(project="ee-thebeautyofthepixel")
```
### Explanation:

We import necessary Python modules, including os, pathlib, time, and asyncio for file operations, timing, and asynchronous programming.
We import ee (Earth Engine API) and geemap for working with satellite imagery.
nest_asyncio is applied to allow running asyncio in environments like Jupyter notebooks.
We initialize the Earth Engine API, authenticating if necessary.

### 2. Define constants and set up the area of interest:

<summary>Code</summary>
```python
# Define constants
OUT_DIR = os.path.expanduser("~/Downloads")
START_DATE = "2024-01-01"
END_DATE = "2024-07-31"
COLLECTION_ID = "COPERNICUS/S2_SR"
CENTER_LAT, CENTER_LON = 8.3958, -82.4350
SIDE_LENGTH = 0.09  # roughly 10 km in degrees

# Create output directory
pathlib.Path(OUT_DIR).mkdir(parents=True, exist_ok=True)

# Define the bounding box
bbox = ee.Geometry.Rectangle([
    CENTER_LON - SIDE_LENGTH/2,  # min longitude
    CENTER_LAT - SIDE_LENGTH/2,  # min latitude
    CENTER_LON + SIDE_LENGTH/2,  # max longitude
    CENTER_LAT + SIDE_LENGTH/2   # max latitude
])
```

### Explanation:

We define constants for the output directory, date range, satellite collection ID, and geographical area of interest.
The area of interest is centered on David, Chiriquí, Panama (8.3958° N, 82.4350° W).
We create the output directory if it doesn't exist.
A bounding box is defined using Earth Engine's geometry functions.

### 3. Filter image collection:

<summary>Code</summary>
```python
# Filter image collection
collection = ee.ImageCollection(COLLECTION_ID) \
    .filterDate(START_DATE, END_DATE) \
    .filterBounds(bbox) \
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 85))

l2a_images = collection.map(lambda i: i.unmask(-1))
bandNames_l2a = l2a_images.aggregate_array('system:index')
image_ids = [image_id for image_id in bandNames_l2a.getInfo()]
```

### Explanation:

We filter the Sentinel-2 image collection based on date range, geographical bounds, and cloud cover.
The filtered images are unmasked and their IDs are extracted.
image_ids now contains a list of all image IDs that meet our criteria.

### 4. Define download functions:

<summary>Code</summary>
```python
def download_snippet(image_id:str, collection_id:str, roi:ee.Geometry, fc, output_folder)->str:
    """Downloads the 4 images but only for 1 image id"""
    print(f"Downloading {image_id}")
    L2A_image = ee.Image(f"{collection_id}/{image_id}").clip(roi)
    vis_params = {
            'bands': ['B8', 'B4', 'B3'],
            'min': 0,
            'max': 5000,
            'gamma': [1.35, 1.35, 1.35]
        }
    L2A_image_to_export = L2A_image.visualize(**vis_params) \
            .clip(roi) \
            .paint(fc, '0000ffff', 2)
    _out = output_folder + "/" + image_id + "_L2A.tif"
    geemap.download_ee_image(L2A_image_to_export, _out, scale=2)
    return L2A_image_to_export

async def download_snippet_async(image_id: str, collection_id: str, roi: ee.Geometry, fc, output_folder) -> str:
    """Downloads the image for 1 image id asynchronously"""
    print(f"Downloading {image_id}")

    # Create a partial function for the synchronous parts
    sync_func = partial(download_snippet_sync, image_id, collection_id, roi, fc, output_folder)

    # Run the synchronous function in a thread pool
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, sync_func)

    return f"Downloaded {image_id}"

def download_snippet_sync(image_id: str, collection_id: str, roi: ee.Geometry, fc, output_folder) -> str:
    """Synchronous part of the download function"""
    L2A_image = ee.Image(f"{collection_id}/{image_id}").clip(roi)
    vis_params = {
        'bands': ['B8', 'B4', 'B3'],
        'min': 0,
        'max': 5000,
        'gamma': [1.35, 1.35, 1.35]
    }
    L2A_image_to_export = L2A_image.visualize(**vis_params) \
        .clip(roi) \
        .paint(fc, '0000ffff', 2)
    _out = f"{output_folder}/{image_id}_L2A.tif"
    geemap.download_ee_image(L2A_image_to_export, _out, scale=2)
    return L2A_image_to_export

async def download_all_snippets_async(image_ids, collection_id, roi, fc, output_folder):
    tasks = []
    for image_id in image_ids:
        task = asyncio.create_task(download_snippet_async(
            image_id, collection_id, roi, fc, output_folder
        ))
        tasks.append(task)
    return await asyncio.gather(*tasks)
```

### Explanation:

download_snippet: A synchronous function that downloads a single image.
download_snippet_async: An asynchronous wrapper for the download function.
download_snippet_sync: The synchronous part of the download process, separated to work with asyncio.
download_all_snippets_async: An asynchronous function that creates tasks for downloading all images concurrently.

### 5. Running comparison

<summary>Code</summary>
```python 
# Sequential download
start_time_sequential = time.perf_counter()

for image_id in image_ids:
    download_snippet(image_id=image_id, collection_id=COLLECTION_ID,
                     roi=bbox, fc=bbox, output_folder=OUT_DIR)

end_time_sequential = time.perf_counter()
execution_time_sequential = end_time_sequential - start_time_sequential
print(f"Total time taken for sequential download: {execution_time_sequential:.4f} seconds")

# Asynchronous download
start_time_async = time.perf_counter()

loop = asyncio.get_event_loop()
results = loop.run_until_complete(download_all_snippets_async(image_ids, COLLECTION_ID, bbox, bbox, OUT_DIR))

end_time_async = time.perf_counter()
execution_time_async = end_time_async - start_time_async
print(f"Total time taken for asynchronous download: {execution_time_async:.4f} seconds")

# Print results
for result in results:
    print(result)

# Compare performance
speedup = execution_time_sequential / execution_time_async
print(f"Speedup factor: {speedup:.2f}x")
```

### Explanation: 

We perform both sequential and asynchronous downloads, timing each method.
The sequential method uses a simple for loop to download images one by one.
The asynchronous method uses asyncio to download images concurrently.
We compare the execution times and calculate the speedup factor.


<details>
  <summary>Code</summary>
```python title="download_s2_snippets.py" linenums="1"
import os
import pathlib
import time
import asyncio
from functools import partial

import ee
import geemap
import nest_asyncio

# Apply nest_asyncio to allow running asyncio within Jupyter or similar environments
nest_asyncio.apply()

# Initialize Earth Engine
try:
    ee.Initialize()
except Exception:
    ee.Authenticate()
    ee.Initialize(project="ee-thebeautyofthepixel")

# Define constants
OUT_DIR = os.path.expanduser("~/Downloads")
START_DATE = "2024-01-01"
END_DATE = "2024-07-31"
COLLECTION_ID = "COPERNICUS/S2_SR"
CENTER_LAT, CENTER_LON = 8.3958, -82.4350
SIDE_LENGTH = 0.09  # roughly 10 km in degrees

# Create output directory
pathlib.Path(OUT_DIR).mkdir(parents=True, exist_ok=True)

# Define the bounding box
bbox = ee.Geometry.Rectangle([
    CENTER_LON - SIDE_LENGTH/2,  # min longitude
    CENTER_LAT - SIDE_LENGTH/2,  # min latitude
    CENTER_LON + SIDE_LENGTH/2,  # max longitude
    CENTER_LAT + SIDE_LENGTH/2   # max latitude
])

# Filter image collection
collection = ee.ImageCollection(COLLECTION_ID) \
    .filterDate(START_DATE, END_DATE) \
    .filterBounds(bbox) \
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 85))

l2a_images = collection.map(lambda i: i.unmask(-1))
bandNames_l2a = l2a_images.aggregate_array('system:index')
image_ids = [image_id for image_id in bandNames_l2a.getInfo()]

# Define download functions

def download_snippet(image_id:str, collection_id:str, roi:ee.Geometry, fc, output_folder)->str:
    """Downloads the 4 images but only for 1 image id"""
    print(f"Downloading {image_id}")
    L2A_image = ee.Image(f"{collection_id}/{image_id}").clip(roi)
    vis_params = {
            'bands': ['B8', 'B4', 'B3'],
            'min': 0,
            'max': 5000,
            'gamma': [1.35, 1.35, 1.35]
        }
    L2A_image_to_export = L2A_image.visualize(**vis_params) \
            .clip(roi) \
            .paint(fc, '0000ffff', 2)
    _out = output_folder + "/" + image_id + "_L2A.tif"
    geemap.download_ee_image(L2A_image_to_export, _out, scale=2)
    return L2A_image_to_export

async def download_snippet_async(image_id: str, collection_id: str, roi: ee.Geometry, fc, output_folder) -> str:
    """Downloads the image for 1 image id asynchronously"""
    print(f"Downloading {image_id}")
    
    # Create a partial function for the synchronous parts
    sync_func = partial(download_snippet_sync, image_id, collection_id, roi, fc, output_folder)
    
    # Run the synchronous function in a thread pool
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, sync_func)
    
    return f"Downloaded {image_id}"

def download_snippet_sync(image_id: str, collection_id: str, roi: ee.Geometry, fc, output_folder) -> str:
    """Synchronous part of the download function"""
    L2A_image = ee.Image(f"{collection_id}/{image_id}").clip(roi)
    vis_params = {
        'bands': ['B8', 'B4', 'B3'],
        'min': 0,
        'max': 5000,
        'gamma': [1.35, 1.35, 1.35]
    }
    L2A_image_to_export = L2A_image.visualize(**vis_params) \
        .clip(roi) \
        .paint(fc, '0000ffff', 2)
    _out = f"{output_folder}/{image_id}_L2A.tif"
    geemap.download_ee_image(L2A_image_to_export, _out, scale=2)
    return L2A_image_to_export

async def download_all_snippets_async(image_ids, collection_id, roi, fc, output_folder):
    tasks = []
    for image_id in image_ids:
        task = asyncio.create_task(download_snippet_async(
            image_id, collection_id, roi, fc, output_folder
        ))
        tasks.append(task)
    return await asyncio.gather(*tasks)

# Sequential download
start_time_sequential = time.perf_counter()

for image_id in image_ids:
    download_snippet(image_id=image_id, collection_id=COLLECTION_ID,
                     roi=bbox, fc=bbox, output_folder=OUT_DIR)

end_time_sequential = time.perf_counter()
execution_time_sequential = end_time_sequential - start_time_sequential
print(f"Total time taken for sequential download: {execution_time_sequential:.4f} seconds")

# Asynchronous download
start_time_async = time.perf_counter()

loop = asyncio.get_event_loop()
results = loop.run_until_complete(download_all_snippets_async(image_ids, COLLECTION_ID, bbox, bbox, OUT_DIR))

end_time_async = time.perf_counter()
execution_time_async = end_time_async - start_time_async
print(f"Total time taken for asynchronous download: {execution_time_async:.4f} seconds")

# Print results
for result in results:
    print(result)

# Compare performance
speedup = execution_time_sequential / execution_time_async
print(f"Speedup factor: {speedup:.2f}x")
```
</details>
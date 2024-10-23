<h3 id="minera-panama">Google Earth Engine App - Minera Panama</h3>

<p>This project utilizes Earth Engine, a cloud-based platform for geospatial analysis, to process Landsat 7 satellite imagery to create True Color COmposites in the region of Petaquilla, Republic of Panama. The script focuses on an area within Donoso District, which is part of the Mesoamerican Biological Corridor.</p>

<p>This workflow automates the creation, visualization, and export of median composites of Landsat 7 images for monitoring the Petaquilla Minera Panama area over time, including the creation of an annotated GIF animation.</p>

<p align="center">
      <img src="./../MINERA-PANAMA.png" alt="Centered Image">
      <br>
      <i>Landsat Composites over the area of Minera Panama.</i>
      </p>


<h4>Description of Functions and Steps</h4>


<h4>Functions</h4>

<h4>applyScaleFactors(image):</h4>

Adjusts optical and thermal bands of an image using specific scaling factors for accurate representation.

<h4>maskL7srClouds(image):</h4>

Masks out clouds and cloud shadows in Landsat 7 images by using bitwise operations on QA_PIXEL data.

<h4>blendImage(image):</h4>

Applies a focal mean filter to smooth the image and blends it with the original image to reduce noise.

<h4>median_yearly_landsat_7(start, end):</h4>

Creates a median composite of Landsat 7 images for a specified date range, filtered by the AOI and cloud cover threshold.

<h4>Steps for the Application</h4>
<ul>
  <li>Define Area of Interest (AOI):</li>
  <li>Set the AOI to the geometry variable.</li>
  <li>Create a buffered extent around the AOI for analysis.</li>
  <li>Set Cloud Cover Threshold: Define the maximum acceptable cloud cover for images (set to 100%).</li>
  <li>Prepare Date Ranges: Define periods for data collection and segment years into intervals. Concatenate years with periods to generate specific date ranges.</li>
  <li>Generate Composites: For each date range, create median composites of Landsat 7 images using the <code>median_yearly_landsat_7</code> function. Apply cloud masking and image blending to enhance the quality of the composites. Clip the composites to the AOI and add them to the map.</li>
  <li>Export Composites: Export the generated composites to Google Drive as GeoTIFF files with descriptive names.</li>
  <li>Annotate Images: Use the text package to annotate the composites with labels.</li>
  <li>Create a collection of annotated images.</li>
  <li>Create GIF Animation:
    <ul>
      <li>Define GIF parameters, including region, dimensions, and frame rate.</li>
      <li>Generate and display a GIF animation of the annotated image collection.</li>
    </ul>
  </li>
</ul>

<details>
  <summary>Code</summary>
```javascript title="petaquilla_mosaics.js" linenums="1"
/*******************************************************************************
 * Petaquilla Minera Panama 2015 - present
 * Location: Donoso District, Colon, Republic of Panama
 * Author: Roger Almengor González
 * Date 26.11.2023
 * ****************************************************************************/

//var districts_list = ee.List(['Donoso']);
//var districts = table.filter(ee.Filter.inList('NAME_2', districts_list));
//var extent = districts.geometry().bounds();
//var AOI = extent.buffer(ee.Number(10000).sqrt().divide(2), 1).bounds();

var AOI = geometry;

var CLOUD_COVER = 100

var buffered_extent = AOI.buffer(ee.Number(10000)
                                    .sqrt()
                                    .divide(2), 1)
                                    .bounds();


// Elaborating the dates
// Getting Temperatures for Every Month
var period = ['-01-01', '-12-01']; 

var years = [
['2005', '2010'],
['2011', '2015'],
['2016', '2020'],
['2021', '2023'],
];

var add_period = function(year){
var start_date = period[0]; 
var end_date = period[1];
return [year[0] + start_date, year[1] + end_date];
};

var visualization = {
  min: 8000,
  max: 19000,
  gamma: 1.5,
  bands: ['SR_B7_median', 'SR_B5_median', 'SR_B3_median'],
};


var concatenate_year_with_periods = function(years, period){
return years.map(add_period);
};

var Dates = concatenate_year_with_periods(years, period);

print(Dates);


// Applies scaling factors.
function applyScaleFactors(image) {
  var opticalBands = image.select('SR_B.').multiply(0.0000275).add(-0.2);
  var thermalBand = image.select('ST_B6').multiply(0.00341802).add(149.0);
  return image.addBands(opticalBands, null, true)
              .addBands(thermalBand, null, true);
}

function maskL7srClouds(image) {
  var qa = image.select('QA_PIXEL');
  // If the cloud bit (5) is set and the cloud confidence (7) is high
  // or the cloud shadow bit is set (3), then it's a bad pixel.
  var cloud = qa.bitwiseAnd(1 << 5)
                  .and(qa.bitwiseAnd(1 << 7))
                  .or(qa.bitwiseAnd(1 << 3));
  // Remove edge pixels that don't occur in all bands
  var maskL7 = image.mask().reduce(ee.Reducer.min());
  return image.updateMask(cloud.not()).updateMask(maskL7);
}

function blendImage(image) {
  // Apply a focal mean filter to the image
  var focalMeanImage = image.focalMean(1, "square", "pixels", 1);

  // Blend the filtered image with the original image
  var blendedImage = focalMeanImage.blend(image);

  return blendedImage;
}

// Creating composites using median pixel value
var median_yearly_landsat_7 = function(start, end){
print("filtering per dates");
print(start);
print(end);
var dataset_ =  ee.ImageCollection("LANDSAT/LE07/C02/T1_L2")
                 .filterDate(start, end)
                  .filterBounds(AOI)
                  .filterMetadata('CLOUD_COVER', 'less_than', CLOUD_COVER)
                  //.map(applyScaleFactors)
                  .map(maskL7srClouds)
                  .map(blendImage)
                  .map(function(image){return image.clip(AOI)});
print("DATASET_:")
print(dataset_);
var median_yearly = dataset_.reduce(ee.Reducer.median());
return median_yearly;
};

var composite_name_list_l7 = ee.List([]);


var apply_monthly_composite = function(date_list){
var start = date_list[0];
var end = date_list[1]; 
var output_name = start + "TO" + end + "_SENTINEL-2";
var composite = median_yearly_landsat_7(start, end);
print(composite);
composite_name_list_l7 = composite_name_list_l7.add([composite, output_name]);
Map.addLayer(composite, visualization, output_name, false);
Export.image.toDrive({
image: composite,
description: output_name,
fileFormat: 'GeoTIFF',
crs : 'EPSG:4326',
folder : 'LANDSAT_LST_LAS_LOMAS',
region: AOI
});
return 0; 
};

Dates.map(apply_monthly_composite); 


/******************************************************************
// Animation gif 
// Create RGB visualization images for use as animation frames.
/******************************************************************/
var text = require('users/gena/packages:text');
var annotated_collection_list = ee.List([])
var annotations = [
{position: 'left', 
offset: '0.25%', 
margin: '0.25%', 
property: 'label', 
scale: 250} //large scale because image if of the whole world. Use smaller scale
];

var create_annotated_collection = function(image_and_id) {
var img = image_and_id[0];
var image_id = image_and_id[1];
print(image_id);
var img_out = img.visualize(visualization)
//.clip(geometry)//.paint(municipalities, 'FF0000', 2)
.set({'label': image_id});
Map.addLayer(img_out);
var annotated = text.annotateImage(img_out, {}, Bayern, annotations);
annotated_collection.add(annotated);
return 0;
};

var municipalities_geom = geometry;

var n = composite_name_list_l7.size().getInfo();
print(n);
for (var i = 0; i < n; i++) {
var img_info = ee.List(composite_name_list_l7.get(i));
print(img_info);
var img = ee.Image(img_info.get(0));
var img_id = ee.String(img_info.get(1));
var year = ee.String(ee.List(img_id.split("TO").get(1)));
var year = ee.String(year.split("-").get(0));
var month = ee.String(ee.List(img_id.split("-").get(0)));
var img_id_ = year.getInfo() // + "_" + month.getInfo();
var img_out = img.visualize(visualization)
//.paint(geometry, 'FF0000', 2)
.set({'label': img_id_});
var annotated = text.annotateImage(img_out, {}, buffered_extent, annotations);
//Map.addLayer(annotated);
var annotated_collection_list = annotated_collection_list.add(annotated)
}

var annotated_col = ee.ImageCollection(annotated_collection_list)

// Define GIF visualization parameters.
var gifParams = {
'region': buffered_extent,
'dimensions': 500,
 //'crs': 'EPSG:32632',
'framesPerSecond': .4
};

// Print the GIF URL to the console.
print(annotated_col.getVideoThumbURL(gifParams));
// Render the GIF animation in the console.
print(ui.Thumbnail(annotated_col, gifParams));
```
</details>

<h4>Google Earth Engine App</h4>

</html>
<iframe src="https://thebeautyofthepixel.users.earthengine.app/view/gisminerapanama" width="800" height="800" frameborder="0" style="border:0" allowfullscreen></iframe>


<br>
<sup><sub><i>Please Note: All examples provided in this documentation have been created within the Google Earth Engine platform with the intention of ensuring reproducibility. If you encounter any issues or have questions, feel free to reach out to me at rogeralmengor@gmail.com. The code is made available for public use without any legal restrictions, but I would greatly appreciate it if you could acknowledge my efforts in developing these tools. Your recognition would mean a lot to me as a fellow developer.</i></sub></sup>
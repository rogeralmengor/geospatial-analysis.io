
Welcome to the <b>Google Earth Engine</b> section of this documentation. This section is dedicated to providing a solution-based approach to various geospatial analytics problems, complete with code explanations and illustrative outputs. The code presented here is based on the concepts and functionalities offered by the Google Earth Engine (GEE) JavaScript API.

If you are unfamiliar with the GEE JavaScript API or need further information on its usage and capabilities, you can refer to the official [Google Earth Engine JavaScript API documentation](https://developers.google.com/earth-engine/). This documentation serves as a valuable resource for understanding the core functionalities of the GEE platform and its JavaScript API, which form the foundation for the solutions and projects presented in this section. 

Feel free to explore the projects and code examples provided here to gain insights into how GEE can be leveraged for various geospatial analysis tasks.


<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Portfolio</title>
  <style>
    /* Layout for the thumbnails in a flexible grid */
    .portfolio-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); /* Flexible columns */
      gap: 20px; /* Space between items */
      text-align: center; /* Center text below the images */
    }

    /* Styling the individual portfolio items */
    .portfolio-item {
      position: relative;
      width: 100%; /* Make it scale within the grid */
      height: auto;
      padding-bottom: 100%; /* Keep a square aspect ratio */
      border-radius: 10px;
      overflow: hidden;
      margin: 0 auto; /* Center the portfolio items */
    }

    /* Styling the image */
    .portfolio-img {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      object-fit: cover; /* Ensure the image covers the thumbnail area */
      opacity: 0.7; /* Slightly faded by default */
      transition: transform 0.3s ease, opacity 0.3s ease; /* Smooth transition on hover */
    }

    /* Hover effect for image (brighten and scale) */
    .portfolio-item:hover .portfolio-img {
      opacity: 1; /* Brighten the image */
      transform: scale(1.05); /* Slightly zoom the image */
    }

    /* Overlay text container */
    .portfolio-overlay {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      display: flex;
      justify-content: center;
      align-items: center;
      background-color: rgba(0, 0, 0, 0.5); /* Dark overlay */
      opacity: 0; /* Invisible by default */
      transition: opacity 0.3s ease;
    }

    /* Show overlay text on hover */
    .portfolio-item:hover .portfolio-overlay {
      opacity: 1; /* Show overlay text */
    }

    /* Overlay text style */
    .portfolio-overlay p {
      color: white;
      text-align: center;
      font-size: 16px;
      font-weight: bold;
    }

    /* Text below the image */
    .project-description {
      margin-top: 10px; /* Space between the image and text */
      font-size: 14px;
      color: #333;
      text-align: center;
    }

    /* Smooth scrolling behavior */
    html {
      scroll-behavior: smooth;
    }

    /* Media Queries for small devices */
    @media (max-width: 600px) {
      .portfolio-grid {
        grid-template-columns: 1fr; /* 1 column for small screens */
      }

      .portfolio-item {
        width: 100%; /* Make items smaller on small screens */
        margin: 0 auto; /* Center items */;
        height: auto;
      }
    }

    @media (prefers-color-scheme:dark) {
      .project-description {
        color: #ddd;
      }
    }
  </style>
</head>
<body>

<h2>Project Portfolio</h2>

<div class="portfolio-grid">
  <!-- Project 1: Time Lapse (Landsat Images) -->
  <a href="../time_lapse_sentinel-2/" style="text-decoration: none;">
    <div class="portfolio-item">
      <img src="./../time_lapse.gif" alt="Time Lapse" class="portfolio-img">
      <div class="portfolio-overlay">
        <p>Time Lapse (Landsat)</p>
      </div>
    </div>
    <div class="portfolio-description">
    <h6>Time Lapse (Landsat)</h6></div>
  </a>

  <!-- Project 2: Land Surface Temperature (MODIS) -->
  <a href="../modis_temperature/" style="text-decoration: none;">
    <div class="portfolio-item">
      <img src="./../dry_season_20_years_modis.gif" alt="Land Surface Temperature (MODIS)" class="portfolio-img">
      <div class="portfolio-overlay">
        <p>Land Surface Temperature (MODIS)</p>
      </div>
    </div>
    <div class="portfolio-description">
      <h6>Land Surface Temperature (MODIS)</h6></div>
  </a>

  <!-- Project 3: Radar images Panama Canal -->
  <a href="../time-lapse-radar/" style="text-decoration: none;">
    <div class="portfolio-item">
      <img src="./../panama_canal.gif" alt="Time Lapse Radar" class="portfolio-img">
      <div class="portfolio-overlay">
        <p>Time Lapse Cargo Ship Monitoring (Sentinel-1)</p>
      </div>
    </div>
    <div class="portfolio-description">
    <h6>Time Lapse Cargo Ship Monitoring (Sentinel-1)</h6></div>
  </a> 

  <!-- Project 4: Radar images Panama Canal -->
  <a href="#nitrogen-dioxide" style="text-decoration: none;">
    <div class="portfolio-item">
      <img src="./../nitrogen_dioxide_2019_2022.jpg" alt="Monitoring Air Polution" class="portfolio-img">
      <div class="portfolio-overlay">
        <p>Monitoring Nitrogen Dioxide (Sentinel-5P)</p>
      </div>
    </div>
    <div class="portfolio-description">
    <h6>Monitoring Nitrogen Dioxide (Sentinel-5P)</h6></div>
  </a>

  <!-- Project 5: Minera Panama Google App -->
  <a href="#minera-panama" style="text-decoration: none;">
    <div class="portfolio-item">
      <img src="./../MINERA-PANAMA.png" alt="Minera Panama GEE App" class="portfolio-img">
      <div class="portfolio-overlay">
        <p>Minera Panama GEE App (Landsat)</p>
      </div>
    </div>
    <div class="portfolio-description">
    <h6>Minera Panama GEE App (Landsat)</h6></div>
  </a>
</div>


<h3 id="nitrogen-dioxide">💨 Monitoring Nitrogen Dioxide in Panama City with Sentinel-5P Imagery 🏙️ </h3>

<h4>Objective:</h4>

<p>The objective of this analysis is to create composites of Sentinel-5P imagery to measure nitrogen dioxide (NO2) levels in the city of Panama City during the COVID-19 lockdown period. This analysis aims to provide insights into the variations in tropospheric NO2 density over time, particularly during the lockdown period, and visualize these changes using composites and a time-lapse GIF. The analysis also includes the creation of a chart to represent the mean NO2 levels over the selected area of interest.</p>

<h4>Steps:</h4>

<ol>
  <li><strong>Filtering Area of Interest (AOI):</strong> The analysis starts by defining the Area of Interest (AOI) using geographical boundaries data. The AOI encompasses specific districts within the Panama Province, including Arraiján, Panamá, and San Miguelito. The map is centered on the coordinates of this AOI.</li>
  
  <li><strong>Setting Visualization Parameters:</strong> Visualization parameters for the NO2 density are defined, including the minimum, maximum values, and color palette to be used for rendering the imagery.</li>
  
  <li><strong>Setting the Date Range:</strong> The analysis specifies the start and end dates for image collection. In this case, the date range spans from January 1, 2020, to December 31, 2022.</li>
  
  <li><strong>Creating Image Composites:</strong> The script creates monthly image composites of Sentinel-5P tropospheric NO2 density within the defined AOI. These composites are generated for each month of each year in the specified date range.</li>
  
  <li><strong>Renaming Images:</strong> The image composites are renamed to include the year and month information in their system index.</li>
  
  <li><strong>Creating a Time-Lapse GIF:</strong> The script combines the renamed image composites into a time-lapse GIF. It annotates each frame of the GIF with a timestamp to indicate the year and month of the data. The GIF visually shows the changes in tropospheric NO2 density over time within the AOI.</li>
  
  <li><strong>Creating a Chart:</strong> A chart is generated to display the mean tropospheric NO2 column number density for the selected AOI over time. This chart provides a quantitative representation of the NO2 levels during the analysis period.</li>
  
  <p align="center">
    <img src="./../NOx_Panama_City_2019-2022-1024x540.png" alt="Centered Image">
    <br>
    <i>Tropospheric NO2 column – Chart</i>
  </p>
  <br>

  <li><strong>Displaying Yearly Composites:</strong> Finally, yearly composites for 2019, 2020, 2021, and 2022 are added to the map, allowing for a comparison of NO2 levels across these years.</li>

  <p align="center">
    <img src="./../nitrogen_dioxide_2019_2022.jpg" alt="Centered Image">
    <br>
    <i>Nitrogen Dioxide tropospheric column – Panama City – 2019-2022</i>
  </p>
  <br>

</ol>

<p>This analysis provides a comprehensive overview of tropospheric NO2 density changes in Panama City, with a focus on the COVID-19 lockdown period. The time-lapse GIF and chart enhance the visualization and understanding of these changes over time.</p>


<details>
  <summary>Code</summary>
```javascript title="nitrogen_dioxide_monitoring.js" linenums="1"
// Filtering Feature Collection to Area of Interest (AOI)
var GAUL_country_boundaries = ee.FeatureCollection("FAO/GAUL/2015/level2");

var Panama = GAUL_country_boundaries.filter(ee.Filter.eq('ADM1_NAME', 'Panamá'));
print(Panama);
Map.addLayer(Panama, {color: 'green'}, 'Panama Province');
var districts = ee.List(['Arraiján', 'Panamá', 'San Miguelito']);
var AOI = Panama.filter(ee.Filter.inList('ADM2_NAME', districts));
var AOI_ = AOI.union();
Map.addLayer(AOI_, {color: 'blue'}, 'Area of Interest');

// Setting the Map to the coordinates of one of our districts
var centroid_coor =  AOI_.geometry().centroid().coordinates().getInfo();
var x = centroid_coor[0];
var y = centroid_coor[1];
Map.setCenter(x, y, 10);

// Setting visualization parameters
var band_viz = {
  min: 0,
  max: 0.0002,
   palette: ['white', 'orange', 'red', 'cyan', 'purple', 'green']
};

// Setting the start and end date
// and creating the list of month and dates
var date_start = ee.Date('2020-01-01');
var date_end= ee.Date('2022-12-31');

var months = ee.List.sequence(1, 12);//separate by years
var years = ee.List.sequence(date_start.advance(-1,"year")
                                       .get("year"),
                             date_end.get("year"));

// Creating the image composites (monthly time series)
// of Sentinel-5P tropospheric NO2 density
var year_composite = years.map(function(y){
  return months.map(function(m){
    return ee.ImageCollection('COPERNICUS/S5P/OFFL/L3_NO2')
            .select('tropospheric_NO2_column_number_density')
            .filter(ee.Filter.calendarRange(y, y,'year'))
            .filter(ee.Filter.calendarRange(m, m,'month'))
            .median()
            .set('year',y)
            .set('month', m)
            .clip(AOI_);
})});

function decomposeList(l) {
  return ee.ImageCollection.fromImages(l).toList(12);
}

var list_imgs = year_composite.map(decomposeList).flatten();

// Setting as index the year and month 
// of the layer being created
function renameImages(img){
  var img_1 = ee.Image(img);
  var value = ee.Number(img_1.get('year')).format('%04d')
              .cat('_').cat(ee.Number(img_1.get('month')).format('%02d'));
  var img_2 = img_1.set('system:index', value, 'system:id', value);
  return img_2;
}

var list_imgs_renamed = list_imgs.map(renameImages);

var img_collection = ee.ImageCollection.fromImages(list_imgs_renamed);

// Create time lapse 
var text = require('users/gena/packages:text'); // Import gena's package which allows text overlay on image

var annotations = [
 {position: 'left', offset: '0.25%', margin: '0.25%', property: 'label', scale: 1000} //large scale because image if of the whole world. Use smaller scale otherwise
  ];

function addText(image){
  var timeStamp = image.id();
  var image_ = image.visualize(band_viz).set({'label':timeStamp}); // set a property called label for each image
  var annotated = text.annotateImage(image_, {}, AOI_.geometry(), annotations); // create a new image with the label overlayed using gena's package
  return annotated;
}

var extent = AOI_.geometry().bounds();

var buffered_extent = extent.buffer(ee.Number(10000).sqrt().divide(2), 1).bounds();

// Define GIF visualization parameters.
var gifParams = {
  'region': buffered_extent,
  'dimensions': 600,
  //'crs': 'EPSG:3857',
  'framesPerSecond': 1.5
};

var annotated_collection = img_collection.map(addText);


// Print the GIF URL to the console.
print(ui.Thumbnail(annotated_collection, gifParams));
ui.Thumbnail(annotated_collection, gifParams);

// Define the chart and print it to the console.
var chart =
    ui.Chart.image
        .seriesByRegion({
          imageCollection: img_collection,
          band: 'tropospheric_NO2_column_number_density',
          regions: AOI_,
          reducer: ee.Reducer.mean(),
          scale: 500,
          seriesProperty: 'label',
          xProperty: 'system:id'
        })
        .setOptions({
          title: 'tropospheric NO2 column number density Years 2019-2022',
          hAxis: {title: 'Date', titleTextStyle: {italic: false, bold: true},
                   format: 'short'
          },
          vAxis: {
            title: 'NOx µmol/m2',
            titleTextStyle: {italic: false, bold: true},
          },
          lineWidth: 3,
        });
        
//print(chart);

print(img_collection);

// Adding yearly composites

var imgs_2019 = img_collection.filter(ee.Filter.eq('year', 2019));

Map.addLayer(imgs_2019.mean(), band_viz, 'S5P N02_2019');

var imgs_2020 = img_collection.filter(ee.Filter.eq('year', 2020));

Map.addLayer(imgs_2020.mean(), band_viz, 'S5P N02_2020');

var imgs_2021 = img_collection.filter(ee.Filter.eq('year', 2021));

Map.addLayer(imgs_2021.mean(), band_viz, 'S5P N02_2021');

var imgs_2022 = img_collection.filter(ee.Filter.eq('year', 2022));

Map.addLayer(imgs_2022.mean(), band_viz, 'S5P N02_2022');
```
</details>

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

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
      color: #333; /* Default text color */
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
        width: 90%; /* Make items smaller on small screens */
        margin: 0 auto; /* Center items */
      }
    }
  </style>
</head>
<body>

<h2>Project Portfolio</h2>

<div class="portfolio-grid">
  <!-- Project 1: Time Lapse (Landsat Images) -->
  <a href="#time-lapse" style="text-decoration: none;">
    <div class="portfolio-item">
      <img src="./../time_lapse.gif" alt="Time Lapse" class="portfolio-img">
      <div class="portfolio-overlay">
        <p>Time Lapse (Landsat)</p>
      </div>
    </div>
    <div class="project-description">Time Lapse (Landsat Images)</div>
  </a>

  <!-- Project 2: Land Surface Temperature (MODIS) -->
  <a href="#modis-temperature" style="text-decoration: none;">
    <div class="portfolio-item">
      <img src="./../dry_season_20_years_modis.gif" alt="Land Surface Temperature (MODIS)" class="portfolio-img">
      <div class="portfolio-overlay">
        <p>Land Surface Temperature (MODIS)</p>
      </div>
    </div>
    <div class="project-description">Land Surface Temperature (MODIS)</div>
  </a>

  <!-- Project 3: Radar images Panama Canal -->
<a href="#time-lapse-radar" style="text-decoration: none;">
    <div class="portfolio-item">
      <img src="./../panama_canal.gif" alt="Time Lapse Radar" class="portfolio-img">
      <div class="portfolio-overlay">
        <p>Time Lapse Cargo Ship Monitoring (Sentinel-1)</p>
      </div>
    </div>
    <div class="project-description">Time Lapse Cargo Ship Monitoring (Sentinel-1)</div>
  </a> 

  <!-- Project 4: Radar images Panama Canal -->
<a href="#nitrogen-dioxide" style="text-decoration: none;">
    <div class="portfolio-item">
      <img src="./../nitrogen_dioxide_2019_2022.jpg" alt="Monitoring Air Polution" class="portfolio-img">
      <div class="portfolio-overlay">
        <p>Monitoring Nitrogen Dioxide (Sentinel-5P)</p>
      </div>
    </div>
    <div class="project-description">Monitoring Nitrogen Dioxide (Sentinel-5P)</div>
  </a>

<!-- Project 5: Minera Panama Google App -->
<a href="#minera-panama" style="text-decoration: none;">
    <div class="portfolio-item">
      <img src="./../MINERA-PANAMA.png" alt="Minera Panama GEE App" class="portfolio-img">
      <div class="portfolio-overlay">
        <p>Minera Panama GEE App (Landsat)</p>
      </div>
    </div>
    <div class="project-description">Minera Panama GEE App (Landsat)</div>
  </a> 
</div>

<script>
  // Function to calculate the brightness of a color (using the luminance formula)
  function getBrightness(r, g, b) {
    return (r * 0.299 + g * 0.587 + b * 0.114);
  }

  // Function to extract the RGB color of an image and change text color accordingly
  function adjustTextColorForImage(imgElement, textElement) {
    const img = new Image();
    img.crossOrigin = 'Anonymous'; // Enable cross-origin access for external images
    img.src = imgElement.src;

    img.onload = function () {
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      canvas.width = img.width;
      canvas.height = img.height;
      ctx.drawImage(img, 0, 0);

      // Get the average color of the image
      const imageData = ctx.getImageData(0, 0, 1, 1).data;
      const brightness = getBrightness(imageData[0], imageData[1], imageData[2]);

      // Set text color based on brightness
      if (brightness < 128) {
        textElement.style.color = 'white';
      } else {
        textElement.style.color = 'black';
      }
    };
  }

  // Get all portfolio items and their descriptions
  const portfolioItems = document.querySelectorAll('.portfolio-item');
  
  portfolioItems.forEach(item => {
    const imgElement = item.querySelector('.portfolio-img');
    const textElement = item.nextElementSibling; // Get the project-description element

    adjustTextColorForImage(imgElement, textElement);
  });
</script>

<h3 id="time-lapse">Time Lapse (Landsat Images)🌍</h3>
<p>
Time lapse animations, are an interesting tool used to visualize changes on the earth
surface over time. The following animation is created by the code provided, and shows the changes over a 20 years period of time by the construction of a river dam in the province of Chiriqui, Republic of Panamá.
</p>

<p align="center">
  <img src="./../time_lapse.gif" alt="Centered Image">
  <br>
  <i>Time Lapse of Landsat Images from the Google Earth Engine platform.</i>
</p>


<details>
  <summary>Code</summary>
```javascript title="time_lapse.js" linenums="1"

/*******************************************************************************
 * Downloading Image Chips for Hidroelectrica dos Mares
 * Location: El Valle de Las Lomas, Chiriquí, Panamá
 * Author: Roger Almengor González
 * Data 26.09.2022
 * Project: CAP 2022
 * Land: Bayern
 * ****************************************************************************/

 // Feature Collection 
 var municipalities = ee.List(['Bijagual', 'Chiriquí', 'Cochea', 'David',
                            'Las Lomas','Gualaca', 'Rincón', 'Paja de Sombrero', 'Caldera', 'Dos Ríos', 'Los Anastacios', 'Dolega', 'Pedregal', 'San Pablo Viejo', 'San Pablo Nuevo', 
                            'San Carlos', 'Hornito', 'Tinajas'])

var AOI = table.filter(ee.Filter.inList('NAME_3', municipalities));
var municipalities = AOI.filter(ee.Filter.eq('NAME_1', 'Chiriquí'));
var district_list = ee.List(['Gualaca', 'Boquete', 'Dolega', 'David'])
var municipalities = municipalities.filter(ee.Filter.inList('NAME_2', district_list))
print(AOI);
Map.addLayer(municipalities);

var cochea_district = table.filter(ee.Filter.eq('NAME_3', 'Chiriquí'))
var centroid_cochea_coor = cochea_district.geometry().centroid()
                            .coordinates().getInfo()
var x = centroid_cochea_coor[0];
var y = centroid_cochea_coor[1];
print(x); 
print(y);
Map.setCenter(x, y, 12);


// Elaborating the dates
// Getting Temperatures for Every Month
var period = ['-01-01', '-12-01']; 

var years = [['1999', '2000'],
['2000', '2001'],
['2001', '2002'],
['2002', '2003'],
['2003', '2004'],
['2004', '2005'],
['2005', '2006'],
['2006', '2007'],
['2007', '2008'],
['2008', '2009'], 
['2009', '2010'], 
['2010', '2011'],
['2011', '2012'],
['2012', '2013'],
['2013', '2014'],
];

var add_period = function(year){
var start_date = period[0]; 
var end_date = period[1];
return [year[0] + start_date, year[1] + end_date];
};

var visualization = {
bands: ['SR_B4', 'SR_B3', 'SR_B2'],
min: 0.0,
max: 0.4,
};

var visualization_ = {
bands: ['SR_B4_median', 'SR_B3_median', 'SR_B2_median'],
min: 0.0,
max: 0.4,
};

var concatenate_year_with_periods = function(years, period){
return years.map(add_period);
};

var Dates = concatenate_year_with_periods(years, period);

print(Dates);

/***********************************************************************
   Landsat 5
************************************************************************/
// Applies scaling factors.
function applyScaleFactors(image) {
var opticalBands = image.select('SR_B.').multiply(0.0000275).add(-0.2);
var thermalBand = image.select('ST_B6').multiply(0.00341802).add(149.0);
return image.addBands(opticalBands, null, true)
.addBands(thermalBand, null, true);
}

var dataset = ee.ImageCollection('LANDSAT/LT05/C02/T1_L2')
.filterDate('1999-01-01', '2020-12-31')
.filterBounds(municipalities)
.map(applyScaleFactors)
.map(function(image){return image.clip(municipalities)});
/*******************************************************************************
* Downloading Image Chips for Hidroelectrica dos Mares
* Location: El Valle de Las Lomas, Chiriquí, Panamá
* Author: Roger Almengor González
* Data 26.09.2022
* Project: CAP 2022
* Land: Panama
* *****************************************************************************/

// Feature Collection 
//var municipalities = ee.List(['Bijagual', 'Chiriquí', 'Cochea', 'David',
// 'Las Lomas','Gualaca', 'Rincón',
//'Paja de Sombrero', 'Caldera', 'Dos Ríos', 'Los Anastacios', 'Dolega', 
//'Pedregal', 'San Pablo Viejo', 'San Pablo Nuevo', 'San Carlos', 'Hornito', 
// 'Tinajas'])

// Feature Collection 
var municipalities = ee.List(['Bijagual','Cochea','Las Lomas'])
var AOI = table.filter(ee.Filter.inList('NAME_3', municipalities));
var municipalities = AOI.filter(ee.Filter.eq('NAME_1', 'Chiriquí'));
var district_list = ee.List(['Gualaca', 'Boquete', 'Dolega', 'David'])
var municipalities = municipalities.filter(ee.Filter.inList('NAME_2', 
                                        district_list))
// Gets the bounds and create geometry
var extent = municipalities.geometry().bounds();
var buffered_extent = extent.buffer(ee.Number(10000)
                                    .sqrt()
                                    .divide(2), 1)
                                    .bounds();
//var municipalities = geometry
Map.addLayer(municipalities);

var cochea_district = table.filter(ee.Filter.eq('NAME_3', 'Bijagual'))
var centroid_cochea_coor = cochea_district.geometry()
                                            .centroid()
                                            .coordinates()
                                            .getInfo()

var x = centroid_cochea_coor[0];
var y = centroid_cochea_coor[1];
Map.setCenter(x, y, 10);


// Elaborating the dates
// Getting Temperatures for Every Month
var period = ['-01-01', '-12-01']; 

var years = [['1999', '2000'],
['2000', '2001'],
['2001', '2002'],
['2002', '2003'],
['2003', '2004'],
['2004', '2005'],
['2005', '2006'],
['2006', '2007'],
['2007', '2008'],
['2008', '2009'], 
['2009', '2010'], 
['2010', '2011'],
['2011', '2012'],
['2012', '2013'],
['2013', '2014'],
];

var add_period = function(year){
var start_date = period[0]; 
var end_date = period[1];
return [year[0] + start_date, year[1] + end_date];
};

var visualization = {
bands: ['SR_B4', 'SR_B3', 'SR_B2'],
min: 0.0,
max: 0.4,
};

var visualization_ = {
bands: ['SR_B4_median', 'SR_B3_median', 'SR_B2_median'],
min: 0.0,
max: 0.4,
};

var concatenate_year_with_periods = function(years, period){
return years.map(add_period);
};

var Dates = concatenate_year_with_periods(years, period);



/**********************************************************************
    Landsat 7 
***********************************************************************/
var visualization = {
bands: ['B4', 'B3', 'B2'],
min: 0.0,
max: 0.3,
};

var visualization_ = {
bands: ['B4_median', 'B3_median', 'B2_median'],
min: 0.0,
max: 0.5,
gamma: [0.95, 1.1, 1]
};

// Applies scaling factors.
var cloudMaskL7 = function(image) {
var qa = image.select('BQA');
var cloud = qa.bitwiseAnd(1 << 4)
.and(qa.bitwiseAnd(1 << 6))
.or(qa.bitwiseAnd(1 << 8));
var mask2 = image.mask().reduce(ee.Reducer.min());
return image
//.select(['B3', 'B4'], ['Red', 'NIR'])
.updateMask(cloud.not()).updateMask(mask2)
.set('system:time_start', image.get('system:time_start'));
};

var dataset = ee.ImageCollection('LANDSAT/LE07/C01/T1_TOA')
.filterDate('1999-01-01', '2020-12-31')
.filterBounds(AOI)
//.map(applyScaleFactors)
.map(cloudMaskL7)
.map(function(image){return image.clip(municipalities)});

//dataset = dataset.map(applyScaleFactors);

// Creating composites using median pixel value
var median_yearly_landsat_7 = function(start, end){
var dataset_ =  dataset.filter(ee.Filter.date(start, end));
var median_yearly = dataset_.reduce(ee.Reducer.median());
return median_yearly;
};

var composite_name_list_l7 = ee.List([]);

var apply_monthly_composite = function(date_list){
var start = date_list[0];
var end = date_list[1]; 
var output_name = start + "TO" + end + "_LANSAT_7";
var composite = median_yearly_landsat_7(start, end);
composite_name_list_l7 = composite_name_list_l7.add([composite, output_name]);
Map.addLayer(composite, visualization_, output_name, false);
Export.image.toDrive({
image: composite,
description: output_name,
fileFormat: 'GeoTIFF',
crs : 'EPSG:4326',
folder : 'LANDSAT_LST_LAS_LOMAS',
region: municipalities
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
var img_out = img.visualize(visualization_)
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
var year = ee.String(ee.List(img_id.split("-").get(0)));
var month = ee.String(ee.List(img_id.split("-").get(1)));
var img_id_ = year.getInfo() // + "_" + month.getInfo();
var img_out = img.visualize(visualization_)
//.paint(geometry, 'FF0000', 2)
.set({'label': img_id_});
var annotated = text.annotateImage(img_out, {}, buffered_extent, annotations);
Map.addLayer(annotated);
var annotated_collection_list = annotated_collection_list.add(annotated)
}

var annotated_col = ee.ImageCollection(annotated_collection_list)

// Define GIF visualization parameters.
var gifParams = {
'region': buffered_extent,
'dimensions': 508,
//'crs': 'EPSG:32632',
'framesPerSecond': 1
};

// Print the GIF URL to the console.
print(annotated_col.getVideoThumbURL(gifParams));
// Render the GIF animation in the console.
print(ui.Thumbnail(annotated_col, gifParams));
```
</details>

<h3 id="modis-temperature">🌐 Measuring land surface temperature with MODIS data 🌡️🛰️</h3>
<h4>Script Description:</h4>
<p>
This script is designed to analyze temperature changes within the Cochea River watershed using the Google Earth Engine (GEE) platform and MODIS (Moderate Resolution Imaging Spectroradiometer) datasets. Specifically, it focuses on measuring temperature variations during both the rainy and dry seasons over a 20-year period. The primary objectives of this script are to generate an animated GIF, a time series graph depicting the Average Median Temperature (°C) as recorded by the MODIS sensor, and a regional overview of the study area.
</p>

<h4>Script Workflow:</h4>
<p>1. Data Acquisition: The script begins by accessing MODIS datasets, which provide reliable temperature data with global coverage and high temporal resolution.</p>

<p>2. Temporal Selection: It then filters the MODIS data to isolate the specific time periods corresponding to the dry and wet seasons over the 20-year span.</p>

<p>3. Spatial Region Selection: The script defines the study area within the Cochea River watershed, ensuring that the analysis is limited to the relevant geographic scope.</p>

<p>4. Temperature Computation: Using the MODIS temperature data, the script calculates the Average Median Temperature (°C) for each pixel within the study area, both for the dry and wet seasons.</p>

<p>5. Visualization Generation:
   - *Animated GIF:* The script generates an animated GIF, showcasing the temporal evolution of temperature changes over the 20-year period. Each frame of the GIF represents a specific time step, offering a dynamic visual representation of temperature variations.
    <p align="center">
      <img src="./../dry_season_20_years_modis.gif" alt="Centered Image">
      <br>
    <i>Time Lapse of MODIS Land Surface Temperature (Dry Season) from the Google Earth Engine platform.</i>
    </p>
    <br>
    <p align="center">
      <img src="./../rainy_season_20_years_modis.gif" alt="Centered Image">
      <br>
    <i>Time Lapse of MODIS Land Surface Temperature (Rainy Season) from the Google Earth Engine platform.</i>
    </p>
    <br>
  </p>
   
   <h4>Time Series Graph:</h4>
   <p>Additionally, the script creates a time series graph, displaying the Average Median Temperature (°C) as a function of time. This graph provides a clear overview of temperature trends during the dry and wet seasons.
    <p align="center">
      <img src="./../Average_Median_Temp_Dry_Season-1024x422.png" alt="Centered Image">
      <br>
      <i>Average median temperature for the Dry Season measured from MODIS time series.</i>
      </p>
    <br>

    <p align="center">
      <img src="./../Average_Median_Temp_Rainy_Season-768x316.png" alt="Centered Image">
      <br>
      <i>Average median temperature for the Wet Season measured from MODIS time series.</i>
      </p>
    <br>
    </p>

  <h4>Regional View:</h4> <p>Lastly, the script produces a regional view of the study area, allowing users to geospatially contextualize the temperature changes observed in the Cochea River watershed.

    <p align="center">
      <img src="./../Regional_and_country_wide_location.jpg" alt="Centered Image">
      <br>
      <i>Regional view of the study area.</i>
      </p>
    <br>
    </p>

<p>By following this technical script, users can conduct a rigorous analysis of temperature fluctuations within the specified region and timeframes, enabling in-depth insights into environmental changes over the 20-year period.</p>

<details>
  <summary>Code</summary>
```javascript title="land_surface_MODIS.js" linenums="1"
// Feature Collection 
var districts = ee.List(['Bijagual','Cochea','Las Lomas'])
var AOI = table.filter(ee.Filter.inList('NAME_3', districts));
var districts = AOI.filter(ee.Filter.eq('NAME_1', 'Chiriquí'));
Map.addLayer(districts.union())

// Setting the Map to the coordinates of one of our districts
var cochea_district = table.filter(ee.Filter.eq('NAME_3', 'Bijagual'));
var centroid_cochea_coor = cochea_district.geometry().centroid().coordinates().getInfo();
var x = centroid_cochea_coor[0];
var y = centroid_cochea_coor[1];
Map.setCenter(x, y, 10);

// Raster Visualization Parameters
var landSurfaceTemperatureVis = {
  min: 0, max: 40,
  palette: ['blue', 'limegreen', 'yellow', 'darkorange', 'red']};

  // Image Collection MODIS Surface Temperature Median Values 
// (Dry Season January - March)
// (Wet Season April - December)
var startYear = 2001;
var endYear = 2020;
var DrySeasonMedianCollection = ee.ImageCollection(
  ee.List.sequence(startYear, endYear)
    .map(createDrySeasonMedianComposite)
);

var WetSeasonMedianCollection = ee.ImageCollection( 
  ee.List.sequence(startYear, endYear)
  .map(createWetSeasonMedianComposite)
);

function createDrySeasonMedianComposite(year) {
var startDate = ee.Date.fromYMD(year, 1, 1);
var endDate = ee.Date.fromYMD(year, 3, 31);
var description = startDate.format('yyyy-MM-dd')
.cat(' TO ')
.cat(endDate.format('yyyy-MM-dd'));
return ee.ImageCollection('MODIS/061/MOD11A1')
.filterBounds(districts)
.filterDate(startDate, endDate)
.select('LST_Day_1km')
.map(function(img) {
return img
.multiply(0.02)
.subtract(273.15)
.copyProperties(img, ['system:time_start']);
})
.median()
.set('year', year)
.set('description', description);
}

function createWetSeasonMedianComposite(year) {
var startDate = ee.Date.fromYMD(year, 4, 1);
var endDate = ee.Date.fromYMD(year, 12, 31);
var description = startDate.format('yyyy-MM-dd')
.cat(' TO ')
.cat(endDate.format('yyyy-MM-dd'));
return ee.ImageCollection('MODIS/061/MOD11A1')
.filterBounds(districts)
.filterDate(startDate, endDate)
.select('LST_Day_1km')
.map(function(img) {
return img
.multiply(0.02)
.subtract(273.15)
.copyProperties(img, ['system:time_start']);
})
.median()
.set('year', year)
.set('description', description);
}

DrySeasonMedianMultiBandImg = DrySeasonMedianCollection
      .toBands()
      .select('[0-9]{1,2}_LST_Day_1km');

WetSeasonMedianMultiBandImg = WetSeasonMedianCollection
      .toBands()
      .select('[0-9]{1,2}_LST_Day_1km');

// Define a dictionary that associates band names with values 
var TempInfo = {
  '0_LST_Day_1km': {v: 1, f: '2001'},
  '1_LST_Day_1km': {v: 2, f: '2002'},
  '2_LST_Day_1km': {v: 3, f: '2003'},
  '3_LST_Day_1km': {v: 4, f: '2004'},
  '4_LST_Day_1km': {v: 5, f: '2005'},
  '5_LST_Day_1km': {v: 6, f: '2006'},
  '6_LST_Day_1km': {v: 7, f: '2007'},
  '7_LST_Day_1km': {v: 8, f: '2008'},
  '8_LST_Day_1km': {v: 9, f: '2009'},
  '9_LST_Day_1km': {v: 10, f: '2010'},
  '10_LST_Day_1km': {v: 11, f: '2011'},
  '11_LST_Day_1km': {v: 12, f: '2012'},
  '12_LST_Day_1km': {v: 13, f: '2013'},
  '13_LST_Day_1km': {v: 14, f: '2014'},
  '14_LST_Day_1km': {v: 15, f: '2015'},
  '15_LST_Day_1km': {v: 16, f: '2016'},
  '16_LST_Day_1km': {v: 17, f: '2017'},
  '17_LST_Day_1km': {v: 18, f: '2018'},
  '18_LST_Day_1km': {v: 19, f: '2019'},
  '19_LST_Day_1km': {v: 20, f: '2020'},
}

var xPropVals = [];
var xPropLabels = [];

for (var key in TempInfo){
  xPropVals.push(TempInfo[key].v);
  xPropLabels.push(TempInfo[key]);
}

// Apply the dissolve method to the Geometry object.
print(districts)
var geometryDissolve = districts.union();

// Define the chart and print it to the console.
var chartDrySeason = ui.Chart.image
                .regions({
                  image: DrySeasonMedianMultiBandImg,
                  regions: districts.union(),
                  reducer: ee.Reducer.mean(),
                  scale: 500,
                  seriesProperty: 'label',
                  xLabels: xPropVals
                })
                .setChartType('LineChart')
                .setOptions({
                  title: 'Average (Median) Temperature (°C) Dry Season (Jan-Mar)',
                  hAxis: {
                    title: 'Year',
                    titleTextStyle: {italic: false, bold: true},
                    ticks: xPropLabels
                  },
                  vAxis: {
                    title: 'Temperature (°C)',
                    titleTextStyle: {italic: false, bold: true}
                  },
                  colors: ['f0af07', '0f8755', '76b349'],
                  lineSize: 3
});
print(chartDrySeason);

// Define the chart and print it to the console.
var chartWetSeason = ui.Chart.image
                .regions({
                  image: WetSeasonMedianMultiBandImg ,
                  regions: districts.union(),
                  reducer: ee.Reducer.mean(),
                  scale: 500,
                  seriesProperty: 'label',
                  xLabels: xPropVals
                })
                .setChartType('LineChart')
                .setOptions({
                  title: 'Average (Median) Temperature (°C) Rainy Season (Apr-Dec)',
                  hAxis: {
                    title: 'Year',
                    titleTextStyle: {italic: false, bold: true},
                    ticks: xPropLabels
                  },
                  vAxis: {
                    title: 'Temperature (°C)',
                    titleTextStyle: {italic: false, bold: true}
                  },
                  colors: ['0f8755', '76b349'],
                  lineSize: 3
});
print(chartWetSeason);

// Define GIF visualization parameters.
var gifParams = {
  'region': buffered_extent,
  'dimensions': 600,
  'framesPerSecond': 1.5
};

var text = require('users/gena/packages:text'); // Import gena's package which allows text overlay on image

var annotations = [
 {position: 'left', offset: '0.25%', margin: '0.25%', property: 'label', scale: 100} //large scale because image if of the whole world. Use smaller scale otherwise
  ];

function addText(image){
  var image_0 = image.clip(districts.union());
  var timeStamp = image.get('description'); // get the time stamp of each frame. This can be any string. Date, Years, Hours, etc.
  var timeStamp_ = ee.String(timeStamp); //convert time stamp to string 
  var image_ = image_0.visualize(landSurfaceTemperatureVis).set({'label':timeStamp}); // set a property called label for each image
  var annotated = text.annotateImage(image_, {}, extent, annotations); // create a new image with the label overlayed using gena's package
  return annotated;
}

var AnnotatedCollectionWetSeason = WetSeasonMedianCollection.map(addText); //add time stamp to all images
var AnnotatedCollectionDrySeason = DrySeasonMedianCollection.map(addText);

  
print(ui.Thumbnail(AnnotatedCollectionWetSeason,  gifParams));

var AnnotatedCollectionDrySeason = DrySeasonMedianCollection.map(addText);

print(ui.Thumbnail(AnnotatedCollectionDrySeason,  gifParams));

// ui.Map objects can be constructed. Here, a new map is declared.
var newMap = ui.Map({
  center: {lat: 8, lon: -80, zoom: 5.5
  },
  style: {position: 'bottom-right', width: '400px'}
});

var geomLayer = ui.Map.Layer(districts.union(), {color: 'red'}, 'Area of Interest');
var extentLayer = ui.Map.Layer(districts.bounds, {color:'red'}, 'Extent');
newMap.add(geomLayer);
newMap.add(extentLayer);

// Add the newMap to the defaultMap;
Map.add(newMap);

// Other UI widgets can be added to ui.Map objects, for example labels:
defaultMap.add(ui.Label('Countrywide location', {position: 'bottom-left'}));
newMap.add(ui.Label('Regional Location', {position: 'bottom-left'}));

Map.setControlVisibility({all: false});
newMap.setControlVisibility({all: false});
Map.setOptions("SATELLITE");

```
</details>

<h3 id="time-lapse-radar">🌍 Time Lapse (RADAR Images) - Panama Canal 🛶 💧</h3>

<h4>Objective</h4>

<p>To commemorate World Water Day, this analysis explores the significance of freshwater sources within the Panama Canal Zone.
Our primary goal is to gain insights into the role of these water bodies in sustaining the Panama Canal and supporting the surrounding ecosystems and communities.
    <p align="center">
      <img src="./../panama_canal.gif" alt="Centered Image">
      <br>
      <i>Time Series of Radar (Sentinel-1) Imagery. Year 2022, Panama Canal Zone.</i>
      </p>
    <br>
</p>


<h4>Methodology</h4>

<p>In this analysis, we utilize Sentinel-1 imagery due to its exceptional ability to provide clear, all-weather views of the Earth's surface. Our methodology can be broken down into the following key steps:</p>

<ol>
  <li><strong>Filtering Area of Interest (AOI):</strong> We narrow our focus to specific regions, including the Panama Province and select districts.</li>
  
  <li><strong>Date Range Selection:</strong> Images from 2022 are chosen for analysis.</li>
  
  <li><strong>Image Clipping and Masking:</strong> We create buffered extents and apply masks to Sentinel-1 images.</li>
  
  <li><strong>Image Collection and Filtering:</strong> We gather images with precise properties, including polarization, resolution, and instrument mode.</li>
  
  <li><strong>Backscatter Analysis:</strong> Backscatter graphs for VH and VV bands are generated to monitor changes over time.</li>
  
  <li><strong>Image Visualization:</strong> We visualize images and create RGB representations for animations.</li>
</ol>


<details>
  <summary>Code</summary>
``` javascript title="sentinel_1_time_lapse.js" linenums="1"
// Filtering Feature Collection to Area of Interest (AOI)
var GAUL_country_boundaries = ee.FeatureCollection("FAO/GAUL/2015/level2");

var provinces = ee.List(['Panamá', 'Colón'])
var Panama =  GAUL_country_boundaries.filter(ee.Filter.inList('ADM1_NAME', provinces));
print(Panama)

Map.addLayer(Panama, {color: 'green'}, 'Panama Province');
var districts = ee.List(['Arraiján', 'Panamá', 'San Miguelito', 'Colón','Chagres']);
var Panama = Panama.filter(ee.Filter.inList('ADM2_NAME', districts));

Map.addLayer(Panama);


//Parameter: Start and End date for images to be queried
var start = '2022-01-01';
var end = '2022-12-31';
var dateRange = ee.DateRange(start, end); 

// Gets the bounds and create geometry (rectangle around the polygon)
var extent = Panama.geometry().bounds();

//Map.addLayer(extent); // Adds this geometry to the map

// Creating a buffered version of the extent
var buffered_extent = extent.buffer(ee.Number(50000).sqrt().divide(2), 1).bounds();

Map.addLayer(buffered_extent); // Adds this geometry to the map

// Centering the map to our target parcel
Map.centerObject(Panama, 15);

// Function to clip image 
function clip_image(image){
  return image.clip(buffered_extent); 
}

// Function to mask image to certain backscatter signal
function update_s1_mask(image) {
          var edge = image.lt(-30.0);
          var maskedImage = image.mask().and(edge.not());
          return image.updateMask(maskedImage);
        }
        
        

// Getting an image collection of Sentinel-1 GRDH and VV-VH bands
var s1_collection = ee.ImageCollection('COPERNICUS/S1_GRD')
                    .filterDate(dateRange)
                    .filterBounds(buffered_extent)
                    .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))
                    .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH'))
                    .filter(ee.Filter.eq('resolution_meters', 10))
                    .filter(ee.Filter.eq('instrumentMode', 'IW'))
                    .map(update_s1_mask);
                    
var s1_collection_ = s1_collection.select(['VV', 'VH']);

// Dividing the collection according to Orbits (Ascending or Descending)
var desc = s1_collection_.filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING'));
var asc = s1_collection_.filter(ee.Filter.eq('orbitProperties_pass', 'ASCENDING'));

// Checking out how many images are in every batch (ascending, descending)
print('descending tiles ', desc.size());
print('ascending tiles ', asc.size());


// Create backscatter (dB) graph for VH and VV bands of Sentinel-1
var chart =
    ui.Chart.image
        .series({
          imageCollection: desc,
          region: Panama,
          reducer: ee.Reducer.median(),
          scale: 500,
          xProperty: 'system:time_start'
        })
        .setSeriesNames([])
        .setOptions({
          title: 'Median dB for parcel: ' + "Panama_Canal_Zone",
          hAxis: {title: 'Date', titleTextStyle: {italic: false, bold: true}},
          vAxis: {
            title: 'Backscatter (dB)',
            titleTextStyle: {italic: false, bold: true}
          },
          lineWidth: 5,
          colors: ['#00FF7F', '#3CB371'],
          curveType: 'function'
        });
print(chart);

// Paint the edges with different colors and widths.
var empty = ee.Image().byte();

var outlines = empty.paint({
  featureCollection: Panama,
  width: 'NNH'
});

var palette = ['#FFFF00'];

// Adding every image of the image collection on the Map
var s1_vis_params = {bands: ["VV","VH","VV"],
                        min: -25, 
                        max: 5, 
                        gamma:1, 
                        opacity:1};
                        
function addImage(image) { 
  var id = image.id;
  var image_ = ee.Image(image.id);
  Map.addLayer(image_, s1_vis_params, 
                        id)}
  asc.evaluate(function(asc) {  // use map on client-side
  asc.features.map(addImage);
  Map.addLayer(outlines, {palette: palette, max: 14}, 'Panama');
});

// Create RGB visualization images for use as animation frames.
var rgbVis = asc.map(function(img) {
  return img.visualize(s1_vis_params).clip(buffered_extent);
});

//Create an animated GIF
// Define GIF visualization parameters.
var gifParams = {
  'region': buffered_extent,
  'dimensions': 1100,
  'crs': 'EPSG:4326',
  'framesPerSecond': 5
};

// Print the GIF URL to the console.
print(rgbVis.getVideoThumbURL(gifParams));

// Render the GIF animation in the console.
print(ui.Thumbnail(rgbVis, gifParams));
```
</details>

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
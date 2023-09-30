Identifying Anomalies in Crop Growth using NDVI Time Series in Brandenburg

Have you ever wondered how much land a single pixel of Landsat or Sentinel-2 data can cover? I certainly have! And it got me thinking - could I use this data to see a small patch of corn in a cornfield that was dying in the summer of 2017? In this study, we'll be exploring just that. We'll be using ten years of NDVI time series data and in situ observations from the Ministry of Agriculture to identify any unusual patterns or outliers in crop growth, which could indicate crop stress or disease. We'll also be using Google Earth Engine to help us analyze the data and extract spatial statistics. This project is perfect for geospatial developers who want to learn more about how anomaly detection techniques can be used to monitor crop health and management.

The study will be developed in Google Earth Engine, and we will cover topics such as uploading and importing assets, downloading satellite imagery, masking invalid pixel values, extracting spatial statistics, and reducing the data to crop and district-specific zones. This project will provide geospatial developers with a valuable insight into the use of anomaly detection techniques in crop monitoring and management.

Loading Feature Collection (AOI)

// Load the deu_adm3 table as a Feature Collection
var deu_adm3 = ee.FeatureCollection('FAO/GAUL/2015/level3');

// Filter the Feature Collection by the "NAME_1" property where all values are "Brandenburg"
var brandenburg = deu_adm3.filterMetadata('NAME_1', 'equals', 'Brandenburg');

// Define visualization parameters with green fill and black contour lines
var visParams = {
  color: '000000', // black
  fillColor: '00FF00', // green
  width: 1 // line width in pixels
};

// Display the filtered Feature Collection with the defined visualization parameters
Map.addLayer(brandenburg, visParams, 'Brandenburg');

// Zoom the map to the area covered by the Feature Collection
Map.centerObject(brandenburg, 9);

Loading the LPIS Data

// Add the Feature Collections to the Map, with different colors
Map.addLayer(lpis_2013, {color: 'blue'}, 'LPIS 2013');
Map.addLayer(lpis_2014, {color: 'green'}, 'LPIS 2014');
Map.addLayer(lpis_2015, {color: 'red'}, 'LPIS 2015');
Map.addLayer(lpis_2016, {color: 'yellow'}, 'LPIS 2016');
Map.addLayer(lpis_2017, {color: 'cyan'}, 'LPIS 2017');
Map.addLayer(lpis_2018, {color: 'magenta'}, 'LPIS 2018');
Map.addLayer(lpis_2019, {color: 'black'}, 'LPIS 2019');
Map.addLayer(lpis_2020, {color: 'white'}, 'LPIS 2020');
Map.addLayer(lpis_2021, {color: 'orange'}, 'LPIS 2021');
Map.addLayer(lpis_2022, {color: 'purple'}, 'LPIS 2022');

Creating Landsat Composites 2013 - 2022
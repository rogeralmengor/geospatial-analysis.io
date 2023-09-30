---
title: Measuring land surface temperature with satellite imagery
description: In our previous post, we looked at the changes in the Cochea River watershed, and learned the capabilities of the Google Earth Engine to provide us with a visualization of these changes through satellite imagery. In this post, we are going to measure the changes in land temperature in this area in degrees Celsius, using the MODIS datasets, adding a line... 
---

## Introduction

In our [previous post](https://rogeralmengor.github.io/geospatial-analysis.io/blog/posts/river_dam_el_valle/), we looked at the changes in the Cochea River watershed, and learned the capabilities of the Google Earth Engine to provide us with a visualization of these changes through satellite imagery.
In this post, we are going to measure the changes in land temperature in this area in degrees Celsius, using the MODIS datasets, adding a line by line explanation of the code we are going to run to do this exercise.


## Step by step code explanation

The first thing that we need to do is to set our region of interest. We use the same Feature Collection from the shapefile of the province of Chiriquí from our previous post. 

First we filter our Feature collection using the method ee.Filter.inList which find all the records in a feature collection which values for a certain column ('NAME_3' in this case), match a declared list ('districts'). We will work with the municipalities of Bijagual, Cochea and Las Lomas. 

Because there are one than two districs in different provices named 'Bijagual', we apply an additional filter to keep all records for which the province 'Chiriquí' is found (filtering by the column 'NAME_1'). 

We add the layer, by applying an union algorithm, so the vector won't have any boundaries between the selected districts.

```javascript linenums="1"
// Feature Collection 
var districts = ee.List(['Bijagual','Cochea','Las Lomas'])
var AOI = table.filter(ee.Filter.inList('NAME_3', districts));
var districts = AOI.filter(ee.Filter.eq('NAME_1', 'Chiriquí'));
Map.addLayer(districts.union())
```

Now we'll try to center our may view. First we filter our feature collection, and keep only the 'Bijagual' district. Now we get the x, and y coordinate from this district and store it in the centroid_cochea_coor variable, by using the series of methods geometry, centroid, coordinates and getInfo. By array subscript we get the x and y variable. Finally we center the Map view using the x, and y coordinates.

```javascript linenums="1" 
// Setting the Map to the coordinates of one of our districts
var cochea_district = table.filter(ee.Filter.eq('NAME_3', 'Bijagual'));
var centroid_cochea_coor = cochea_district.geometry().centroid().coordinates().getInfo();
var x = centroid_cochea_coor[0];
var y = centroid_cochea_coor[1];
Map.setCenter(x, y, 10);
```

We set the visualization parameters to map values from 0 to a maximum of 40 for degrees Celsius, and pick up a color palette suitable to the range of values we want to represent.

```javascript linenums="1"
// Raster Visualization Parameters
var landSurfaceTemperatureVis = {
  min: 0, max: 40,
  palette: ['blue', 'limegreen', 'yellow', 'darkorange', 'red']};
```

For this analysis we will divide a year into two seasons, the dry season and the rainy season. This is due to the seasonal pattern of the year that predominates in the tropics, which lacks the four seasons of the year that exist in other latitudes of the planet. The temporal analysis will be made for a period of 20 years, counting 2001 as year 1, until 2020.

We declare two variables ("DrySeasonMedianCollection" and "WetSeasonMedianCollection"), which will contain a collection of MODIS Land Surface images. There is no use (or it is not very recommended) of for loops to perform filtering and application of algorithms on a collection, so the body inside the "ee.ImageCollection" with which we create the two variables mentioned above seems a bit counterintuitive.
Google Earth Engine uses an approach more inclined to functional programming than imperative or object-based programming, mapping functions to collections that can be vector data called "Feature Collections", or Images called "ImageCollections" (it can also be applied to another type of Collections, Lists, but these are the most interesting cases for geospatial data analyzers).
What is done is to create a list with ee.List.sequence taking the first year "2001" and the last year 2020, and on that list we are going to apply the function "createDrySeasonMedianComposite", and "createWetSeasonMedianComposite" respectively.

```javascript linenums="1"
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
```

The two functions below have a similar purpose, and the only thing that differentiates them is the time period used to filter the images.
They use as argument "year", and based on that a startDate and endDate are created to delimit a period of time. Then a variable "description" is created, which is basically a data type "string" that comes from the concatenation of "StartDate" + " TO " + EndDate. The function returns an "ImageCollection", to which the "filterBounds" method is applied to obtain the images that intersect our region of interest (ROI). Then we apply to our "ImageCollection" the "filterDate" method, to obtain the images of the period we declared at the beginning, we select the layer "LST_Day_1km" and to that layer (raster layer) we multiply it by 0.02 which is the scale factor that comes in the MODIS products user guide for the transformation of digital numbers (DN) to Kelvin degrees, and finally we subtract the resulting values by 273.15 to transform the Kelvin degrees to Celcius which are the ones we will be working with.
As you can see the same logic is observed in both functions, what changes are the time periods.

```javascript linenums="1"
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
```

To the new imageCollection we apply the method "toBands" to convert it from its "collection" state to a "multi-band" image, using after the method "select" and a regular expression to get the images that come with a numerical prefix, starting by 0, e.g. ("0_LST_Day_1km", "1_LST_Day_1km" ...) .

```javascript linenums="1"
DrySeasonMedianMultiBandImg = DrySeasonMedianCollection
      .toBands()
      .select('[0-9]{1,2}_LST_Day_1km');

WetSeasonMedianMultiBandImg = WetSeasonMedianCollection
      .toBands()
      .select('[0-9]{1,2}_LST_Day_1km');
```

Now we create a dictionary called "TempInfo" which contains as key values the names of the layers in the multi-band images "DrySeasonMedianMultiBandImg" and "WetSeasonMedianMultiBandImg", and the value is a dictionary with ordinal values and the corresponding year for each band.

```javascript linenums="1"
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
```

Now we are going to declare two lists to obtain the values and the dictionary keys that will be used to define the axis values in the graphs.

```javascript linenums="1"
var xPropVals = [];
var xPropLabels = [];

for (var key in TempInfo){
  xPropVals.push(TempInfo[key].v);
  xPropLabels.push(TempInfo[key]);
}
```

To unify the geometries of the different districts, we are going to join them using the "union" method in the "FeatureCollection".

```javascript linenums="1"
// Apply the dissolve method to the Geometry object.
print(districts)
var geometryDissolve = districts.union();
```

Now we are going to define two graphs to print on our console. One will be created for the dry season, and the other for the rainy season. For this we use the ui.Chart.image object and apply the "regions" method. In this method we have to define the multiband image whose values we want to plot. Then the region in which we want to calculate the average temperature values, and a reducer, which in this case will be "mean" because we want to calculate the average of pixels in our study area for the given time period. For the seriesProperty parameter we set it to 'label', and define that the xLabels parameter will take the values from the xPropVals list.
The following are parameters for the elements found in the graph we are going to produce. First we define that it will be a line chart by setting the value of 'LineChart' using the 'setChartType' method.
Among the options we define the title, the name of the X axis (with the font type parameters), and the ticks for the horizontal axis will be the years, taken from the xPropLabels list.
For the vertical axis, we will give it the title Temperature (°C), define the parameters for the font. Finally we define the color that our line will take in the graph and the thickness of it.
We apply the print method to see our graph in the console.

```javascript linenums="1"
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
```

<p align="center">
      <img src="./../Average_Median_Temp_Dry_Season-1024x422.png" alt="Centered Image">
      <br>
      <i>Average Median Temperature (°C) for the Dry Season (Jan-Mar) measured from the MODIS sensor in 20 years period</i>
      </p>
<br>

<p align="center">
      <img src="./../Average_Median_Temp_Rainy_Season-1024x422.png" alt="Centered Image">
      <br>
      <i>Average Median Temperature (°C) for the Wet Season (Apr-Dec) measured from the MODIS sensor in 20 years period</i>
      </p>
<br>

The following lines prepare an annotated collection (with a text showing the time period to which the layer belongs). This annotated collection will be displayed in the console as a GIF, which can be saved on your PC in GIF format.

```javascript linenums="1"
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
```

<p align="center">
      <img src="./../rainy_season_20_years_modis.gif" alt="Centered Image">
      <br>
      <i>Rainy Season (Apr-Dec) MODIS Composites (20 years)</i>
      </p>
<br>

<p align="center">
      <img src="./../dry_season_20_years_modis.gif" alt="Centered Image">
      <br>
      <i>Dry Season (Jan-Mar) MODIS Composites (20 years)</i>
      </p>
<br>

Finally, we present our area of interest. For this we create a map of the regional location of our area of interest and another with the location within the country.  This is done with the help of the ui.Map object. Note how at the end we present the map with the location within the country with satellite images as background.

```javascript linenums="1"
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

<p align="center">
      <img src="./../Regional_and_country_wide_location.jpg" alt="Centered Image">
      <br>
      <i>Regional and country-wide overview of our Area of Interest (AOI)</i>
      </p>
<br>

Google Earth Engine provides scientists, as well as anyone with a google account, the opportunity to perform spatial analysis, which can help us to assess the state of natural resources, demographic evolution and other geospatial phenomena.

## Conclusion

In this blog post, we were able to see how to create a time series graph of temperature data from the MODIS Sensor for a geographic region that has undergone major geomorphological changes in recent years. This analysis could be done for a period of 20 years. In addition, these composites could be added in GIF format, and a regional and country level location map could also be added.
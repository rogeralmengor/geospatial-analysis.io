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
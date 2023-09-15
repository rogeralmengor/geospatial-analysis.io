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
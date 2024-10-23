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
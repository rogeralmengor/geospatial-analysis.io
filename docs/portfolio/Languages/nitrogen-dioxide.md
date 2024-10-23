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
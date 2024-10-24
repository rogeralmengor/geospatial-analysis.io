<h1>Flood Monitoring (Sentinel-1) </h2>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flood Monitoring with Sentinel-1</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 20px;
        }
        h1, h2 {
            color: #333;
        }
        code {
            background-color: #f4f4f4;
            padding: 5px;
            border-radius: 4px;
        }
        pre {
            background-color: #f4f4f4;
            padding: 10px;
            border-radius: 4px;
            overflow: auto;
        }
        summary {
            cursor: pointer;
            font-weight: bold;
        }
    </style>
</head>
<body>

<h1>Flood Monitoring with Sentinel-1: Code Explanation</h1>

<p>The following code utilizes the <strong>Sentinel-1</strong> satellite data within <strong>Google Earth Engine</strong> (GEE) to monitor flooding in <strong>Porto Alegre, Brazil</strong>, particularly during the catastrophic floods of 2024. The code applies speckle reduction, generates composites, and visualizes flood impacts.</p>

<h2>Key Components of the Code:</h2>

<summary>Load Sentinel-1 Data</summary>
<pre><code>
// Load Sentinel-1 data for the specified time period
var raw_collection = ee.ImageCollection('COPERNICUS/S1_GRD')
  .filterBounds(portoAlegrePolygon)
  .filterDate('2023-11-01', '2024-04-30') // Before the flood
  .select('VV');
</code></pre>

<summary>Speckle Reduction</summary>
<pre><code>
// Function to apply Lee filter for speckle reduction
function applyLeeFilter(image) {
  // Apply the Lee filter; adjust the kernel size as necessary
  return image.reduceNeighborhood({
    reducer: ee.Reducer.mean(),
    kernel: ee.Kernel.square(3) // Adjust the kernel size based on the desired smoothing
  }).rename('smoothedVV');
}
</code></pre>

<summary>Median Composites</summary>
<pre><code>
// Create a median composite before the flood using smoothed images
var compositeBeforeVV = smoothedBefore.median().clip(portoAlegrePolygon);

// Load after flood images
var afterFloodVV = ee.ImageCollection('COPERNICUS/S1_GRD')
  .filterBounds(portoAlegrePolygon)
  .filterDate('2024-05-01', '2024-05-31') // After the flood
  .select('VV');

// Apply Lee filter for after flood images
var smoothedAfter = afterFloodVV.map(applyLeeFilter);

// Create a median composite after the flood using smoothed images
var compositeAfterVV = smoothedAfter.median().clip(portoAlegrePolygon);
</code></pre>

<summary>Flood Difference Calculation</summary>
<pre><code>
// Subtract the before flood composite from the after flood composite
var floodDifferenceVV = compositeAfterVV.subtract(compositeBeforeVV);
</code></pre>

<summary>Visualization</summary>
<pre><code>
// Create a visualization to emphasize flooded areas in the red channel
var floodVisualization = {
  min: -5, // Adjust these values based on the expected backscatter range
  max: 5,
  palette: ['blue', 'white', 'red'] // Red for flooded areas
};
</code></pre>

<summary>Create Animation</summary>
<pre><code>
// Create animation
print('GIF URL:', animationFrames.getVideoThumbURL(gifParams));
</code></pre>

<h2>Rationale for Remote Sensing in Flood Monitoring</h2>

<ul>
    <li><strong>Timeliness and Efficiency:</strong> Remote sensing allows for rapid assessments of flood impacts across large areas, providing timely information to response teams.</li>
    <li><strong>Less Pre-processing:</strong> In the context of natural disasters, extensive pre-processing may not be feasible. The code emphasizes using existing GEE preprocessing steps, such as noise reduction and cloud masking, which are essential for reliable analysis during urgent situations.</li>
    <li><strong>Data Availability:</strong> The Sentinel-1 mission provides frequent revisit times and all-weather capabilities, making it invaluable for monitoring floods and other disasters.</li>
    <li><strong>Historical Context:</strong> Given the severity of the <strong>2024 Rio Grande do Sul floods</strong>, which resulted in significant fatalities and damage, this analysis underscores the need for effective monitoring solutions.</li>
</ul>

<h2>Additional Context</h2>

<p>The <strong>2024 Rio Grande do Sul floods</strong> are a series of severe floods that affected not only Brazil but also neighboring areas in Uruguay, causing significant loss of life and property damage. The use of remote sensing data during such events helps improve situational awareness and informs recovery efforts.</p>

<p><strong>Reference:</strong> <a href="https://en.wikipedia.org/wiki/2024_Rio_Grande_do_Sul_floods">2024 Rio Grande do Sul floods - Wikipedia</a></p>

</body>
</html>
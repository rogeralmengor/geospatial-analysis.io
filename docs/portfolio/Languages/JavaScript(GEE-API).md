
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
  <a href="../nitrogen-dioxide/" style="text-decoration: none;">
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
  <a href="../minera-panama/" style="text-decoration: none;">
    <div class="portfolio-item">
      <img src="./../MINERA-PANAMA.png" alt="Minera Panama GEE App" class="portfolio-img">
      <div class="portfolio-overlay">
        <p>Minera Panama GEE App (Landsat)</p>
      </div>
    </div>
    <div class="portfolio-description">
    <h6>Minera Panama GEE App (Landsat)</h6></div>
  </a>

  <!-- Project 6: Flood Monitoring (Sentinel-1) -->
 <a href="../flood_porto_alegre/" style="text-decoration: none;">
  <div class="portfolio-item">
    <img src="./../Flood_Monitoring_Porto_Alegre_small.gif" alt="Flood Monitoring (Sentinel-1)" class="portfolio-img">
    <div class="portfolio-overlay">
      <p>Flood Monitoring (Sentinel-1)</p>
    </div>
  </div>
  <div class="portfolio-description">
    <h6>Flood Monitoring (Sentinel-1)</h6>
  </div>
</a>
</div>

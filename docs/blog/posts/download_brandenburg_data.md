---
title: A database worth downloading for time series analysis 
description: Obtaining ground-truth data for geospatial analysis can be a daunting task for geospatial developers or scientists in general. This is often due to the limited manpower, as well as the limited organization, and limited budget to carry out such large 
---

# A database worth downloading for time series analysis 

Obtaining ground-truth data for geospatial analysis can be a daunting task for geospatial developers or scientists in general. This is often due to the limited manpower, as well as the limited organization, and limited budget to carry out such large tasks as a spatial census of what is happening on the Earth’s surface at a temporal resolution (the time taken between each survey) sufficient to perform time series analysis.

Today I would like to make a parenthesis and leave aside all this discouraging panorama, to present you some geospatial data that seem to me an exception to the situation, and that could be of really interesting for further time series analyses in agriculture.

This dataset are the LPIS Data (Land Parcel Identification System), for the federal state of Brandenburg (Germany), for years 2010 until 2022 (and the years to come). It is outstanding since it contains information of parcels dedicated to agriculture. Some of the information we can derived from it are the crop types, the parcel id (without any personal information of the parcel’s owner), land use code (agriculture, grassland, etc.), and year of cultivation. Although not all parcels in this location are represented, we can assure that a great amount of agricultural parcels can be depicted in this dataset for every year.

With that being said, we will go through to the steps to download the data, and after we will make it available in a Google Earth Engine account.

## How to download the “raw” data

When entering Invekos Brandenburg, we can pin point the result that will lead us to the webpage of the Geoportal with geospatial datasets for the state of Brandenburg. Click on the entry “Daten aus dem Agrarförderantrag”. This is the LPIS Data for Germany. The name Invekos stands for LPIS in Germany.

<p align="center">
      <img src="./../1_google_search.png" alt="Centered Image">
      <i style="font-size: 14px;">01. Google Search</i>
      <br>
</p>

Once in this geoportal, the web page should look like this.

<p align="center">
      <img src="./../2_portal_geodata-1024x949.png" alt="Centered Image">
      <i style="font-size: 14px;">02. Geoportal Brandenburg</i>
      <br>
</p>

Now scroll down and click on the geobrocker link as shown in the yellow highlighted text.

<p align="center">
      <img src="./../3_portal_geodata_link-1024x950.png" alt="Centered Image">
      <i style="font-size: 14px;">03. Link to geobrocker</i>
      <br>
</p>

Once on the geobrocker page, click on the button “Weiter zu Bestellvorgang”.

<p align="center">
      <img src="./../4_portal_geodata_link-1024x802.png" alt="Centered Image">
      <i style="font-size: 14px;">04. Weiter zum Bestellvorgang</i>
      <br>
</p>

On the following page, you can see a small interactive map of the federal state of Brandenburg in Germany. Below you will find the button “Datenauftrag Erzeugen”, click there.

<p align="center">
      <img src="./../5_portal_geodata_link-1024x798.png" alt="Centered Image">
      <i style="font-size: 14px;">05. Button Datenauftrag erzeugen</i>
      <br>
</p>

Now you will see a page with some fields to which you can change the input parameters. For example the example below shows the parameters for downloading agricultural parcel data in Shape format, year 2022 and WGS 84 coordinate system. Then click on the “Weiter” (means “next” in german), button.

<p align="center">
      <img src="./../6_portal_geodata_link-1024x799.png" alt="Centered Image">
      <i style="font-size: 14px;">06. Settings for downloading area</i>
      <br>
      <br>
</p>

Once you see the button “Warenkorb”, which is “cart” in german, you will be redirected to the status your requested data.

<p align="center">
      <img src="./../7_portal_geodata_link-1024x803.png" alt="Centered Image">
      <i style="font-size: 14px;">07. Cart</i>
      <br>
</p>

The status of your shopping cart will be displayed, and you will then be able to check out by pressing the “zu Kasse gehen” button.

<p align="center">
      <img src="./../8_portal_geodata_link-1024x798.png" alt="Centered Image">
      <i style="font-size: 14px;">08. Check out</i>
      <br>
</p>

For me as you can see below, the problem is now that I did not do a log in before making the data request. So immediately when you click on the check out, you will be redirected to the log in page. If you have credentials (user name and password), just enter them. But in this example, we are going to make a request for our username and password. So, click on the “Registrieren” button, so we can start the registering process.

<p align="center">
      <img src="./../9_portal_geodata_link-1024x800.png" alt="Centered Image">
      <i style="font-size: 14px;">09. Log in</i>
      <br>
</p>

## Registration process

Below, you will find an example of the fields as I filled them out. Fill in the necessary fields to become a registered user for this web portal.

<p align="center">
      <img src="./../10_portal_geodata_link-1024x812.png" alt="Centered Image">
      <i style="font-size: 14px;">10. Registering</i>
      <br>
</p>

Accept the terms of use and click on “Eingabe überprüfen”.

<p align="center">
      <img src="./../11_portal_geodata_link-1024x808.png" alt="Centered Image">
      <i style="font-size: 14px;">11. Accepting the terms of use</i>
      <br>
</p>

Check that the information provided is correct, and click on register, to begin the registration process.

<p align="center">
      <img src="./../12_portal_geodata_link-1024x807.png" alt="Centered Image">
      <i style="font-size: 14px;">12. Checking the user information</i>
      <br>
</p>

If everthing goes well, the message “Ihre Registrierung verlief erfolgreich. Sie bekommen Ihr Passwort per Mail zugesendet.”, which means your registration has been successful, you will receive a password by email.

<p align="center">
      <img src="./../13_portal_geodata_link-1024x799.png" alt="Centered Image">
      <i style="font-size: 14px;">13. Registration confirmation</i>
      <br>
</p>

## Log in

Now click on “weiter zur Anmeldung”.

<p align="center">
      <img src="./../14_portal_geodata_link-1024x799.png" alt="Centered Image">
      <i style="font-size: 14px;">14. Next steps to log in</i>
      <br>
</p>

After a few minutes, you will receive an email with your username and password.

<p align="center">
      <img src="./../15_portal_geodata_link-1024x530.png" alt="Centered Image">
      <i style="font-size: 14px;">15. User information received per E-Mail</i>
      <br>
      <br>
</p>

Enter your password and username to enter the geoportal as a registered user. I had to insist sometimes, trying both: copying the information in my clipboard form my E-Mail, or entering my username and password through my keyboard. I persisted until it worked, the same may happen to you. Don’t get discouraged, and keep at it until it works. There might be a delayed until your confirmation is down in your E-Mail, and when you actually can use it to log in.

<p align="center">
      <img src="./../16_portal_geodata_link-768x598.png" alt="Centered Image">
      <i style="font-size: 14px;">16. Log in</i>
      <br>
</p>

# Download data

You can go back to your cart overview, and see the data that is ready to be requested. Click on “Kaufen” again.

<p align="center">
      <img src="./../17_portal_geodata_link-1024x798.png" alt="Centered Image">
      <i style="font-size: 14px;">17. Click on "Kaufen" (Buy) again now, as a registered user</i>
      <br>
</p>

Now your job is to wait until you find a message in your E-Mail box, about the confirmation that your data is downloadable. First you will received a message about the request, and after a message when your data is ready to be downloaded.

<p align="center">
      <img src="./../18_portal_geodata_link-1024x117.png" alt="Centered Image">
      <i style="font-size: 14px;">18. Requested data conirmation</i>
      <br>
</p>

<p align="center">
      <img src="./../19_portal_geodata_link-1024x116.png" alt="Centered Image">
      <i style="font-size: 14px;">19. Download data confirmation</i>
      <br>
</p>

And that’s basically it. By clicking on the download link found in the confirmation message in your E-Mail box, you will be redirected to a page like the one below. By clicking on the highlighted button below, the download process will start.

<p align="center">
      <img src="./../20_portal_geodata_link-1024x737.png" alt="Centered Image">
      <i style="font-size: 14px;">20. Download link available</i>
      <br>
</p>

# Creating an asset in Google Earth Engine

Now that we have downloaded our data in Shape format, let’s go to our Google Earth Engine account and import the dataset for the year 2022 and add a description of the dataset that will help us to highlight its main features. irst of all let’s open the google earth engine home page, and click on the tab code editor to open our google earth engine staff in case we have already created one. For more information about how to open an account for google earth engine visit the following link: [https://developers.google.com/earth-engine/guides/access](https://developers.google.com/earth-engine/guides/access)

<p align="center">
      <img src="./../1-768x272.png" alt="Centered Image">
      <i style="font-size: 14px;">21. Opening Google Earth Engine Code Editor</i>
      <br>
</p>

On the left hand side of the code editor we can see several tabs among which is the Assets tab. Let’s click on this one.

<p align="center">
      <img src="./../2-768x345.png" alt="Centered Image">
      <i style="font-size: 14px;">22. Code editor Interface</i>
      <br>
</p>

When we open it we can see some of the assets we have already uploaded, if we have done so in the past. However, for the sake of this tutorial, we are going to assume that you are new to uploading assets in google earth engine.

<p align="center">
      <img src="./../3-1024x307.png" alt="Centered Image">
      <i style="font-size: 14px;">23. Asset's tab</i>
      <br>
</p>

Now please click on the new tab to start the process of creating a new asset.

<p align="center">
      <img src="./../4_creating_new_asset.png" alt="Centered Image">
      <i style="font-size: 14px;">24. Creating new asset</i>
      <br>
</p>

You will see that you have several formats supported by google earth engine to be uploaded among which are CSV files, images, image collections, folders and shapefiles. This last one is the one we are interested in since the formats we downloaded in the previous section come in this type of format.

<p align="center">
      <img src="./../5-1024x576.png" alt="Centered Image">
      <i style="font-size: 14px;">25. Uploading Shapefile</i>
      <br>
</p>

Under the header source files, you will see a button with the label select, click on it to browse the files that are part of the shapefile and that you will need to upload to create this asset.

<p align="center">
      <img src="./../6_selecting_shapefile_from_local_folder.png" alt="Centered Image">
      <i style="font-size: 14px;">26. Selecting Shapefile from local folder</i>
      <br>
</p>

As you can see I have selected the .shp, .shx, .dbf, and .prj extensions which are the minimum necessary to upload as far as the shapefile is concerned (I did not upload the .cpg file at the time of writing this blog post, as in the past this type of extension was not allowed, it seems it is now. I may have made a mistake and this type of extension was always allowed, but as far as I remember it was the restriction I was aware of with this extension).

<p align="center">
      <img src="./../7-1024x576.png" alt="Centered Image">
      <i style="font-size: 14px;">27. Selecting supported files to create asset</i>
      <br>
</p>

Now press the upload button, to start the process of uploading the file to your account, as a google earth engine asset.

<p align="center">
      <img src="./../8-1024x460.png" alt="Centered Image">
      <i style="font-size: 14px;">28. Pressing upload to trigger the task</i>
      <br>
</p>

You will see the “Task” tab in yellow, which means that the upload process is in progress.

<p align="center">
      <img src="./../9-1024x462.png" alt="Centered Image">
      <i style="font-size: 14px;">29. Task started</i>
      <br>
</p>

By clicking on this tab you will see the progress of the upload process of this file.

<p align="center">
      <img src="./../10-1024x462.png" alt="Centered Image">
      <i style="font-size: 14px;">30. Upload progress</i>
      <br>
</p>

At the end of the upload process, you will see the file listed in your assets.

<p align="center">
      <img src="./../11-1024x298.png" alt="Centered Image">
      <i style="font-size: 14px;">31. Assets uploaded</i>
      <br>
</p>

Now let’s click on this dataset to see what google earth engine has already put at our disposal to describe this asset. We can observe three tabs: description, features and properties. In description we can see that no text describing the dataset has been given.

<p align="center">
      <img src="./../12-1024x602.png" alt="Centered Image">
      <i style="font-size: 14px;">32. Description tab</i>
      <br>
</p>

In features, we can see that google earth engine already provides us with the name of the different columns in the attribute table of this asset, as well as the type of data that each column holds.

<p align="center">
      <img src="./../13-1024x605.png" alt="Centered Image">
      <i style="font-size: 14px;">34. Features tab</i>
      <br>
</p>

When clicking on the properties tab, we can see that is also empty.

<p align="center">
      <img src="./../14-1024x604.png" alt="Centered Image">
      <i style="font-size: 14px;">33. Properties tab</i>
      <br>
</p>

Now I wanted to add information related to this dataset, taking advantage of the Description tab. In this one we can format the text using the markdown syntax, since it is supported by this feature of the asset’s manager of google earth engine. To do this just change the “Edit” option at the top right and start adding the text that best describes the asset you just uploaded. Also at the bottom left you can find the option to add the time period this dataset covers.

<p align="center">
      <img src="./../15-1024x613.png" alt="Centered Image">
      <i style="font-size: 14px;">34. Adding asset's description</i>
      <br>
</p>

When you again disable the edit option, you will be able to see how the description will be rendered for users to view.

<p align="center">
      <img src="./../16_product_description.png" alt="Centered Image">
      <i style="font-size: 14px;">35. Product’s description in viewers mode</i>
      <br>
</p>

And that’s all, you need to upload an asset to your google earth engine account. In this post, you have learned how to download LPIS data for the state of brandenburg, and how to upload it from your locally saved shape format on your computer to your google earth engine account as an asset, as well as add a description that can be rendered in a more apealign way using markdown syntax.
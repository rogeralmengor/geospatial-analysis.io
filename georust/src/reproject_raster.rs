extern crate gdal;

use gdal::raster::{Dataset, Driver};
use gdal::spatial_ref::SpatialRef;

fn reproject_raster(input_path: &str, output_path: &str, target_epsg: &str) -> Result<(), String> {
    // Open the input raster dataset
    let dataset = Dataset::open(input_path).map_err(|e| e.to_string())?;

    // Get the input raster's projection
    let source_srs = dataset.projection();

    // Create a SpatialRef for the target EPSG code
    let mut target_srs = SpatialRef::new();
    target_srs.set_from_epsg(target_epsg.parse().unwrap()).map_err(|e| e.to_string())?;

    // Create a new Dataset for the output raster
    let driver = Driver::get("GTiff").map_err(|e| e.to_string())?;
    let mut output_dataset = driver.create(output_path, dataset.raster_size(), 1, dataset.band_count(), dataset.band_type())
        .map_err(|e| e.to_string())?;

    // Set the output dataset's projection to the target EPSG
    output_dataset.set_projection(&target_srs.to_wkt()).map_err(|e| e.to_string())?;

    // Loop over the bands and reproject each one
    for i in 1..=dataset.band_count() {
        let band = dataset.band(i).unwrap();
        let mut output_band = output_dataset.band(i).unwrap();

        // Reproject the band
        band.reproject_to(&mut output_band, &source_srs, &target_srs)
            .map_err(|e| e.to_string())?;
    }

    Ok(())
}

fn main() {
    let input_path = "path/to/input/raster.tif";
    let output_path = "path/to/output/raster.tif";
    let target_epsg = "4326";  // Example: EPSG code for WGS84

    if let Err(err) = reproject_raster(input_path, output_path, target_epsg) {
        eprintln!("Error: {}", err);
    } else {
        println!("Raster reprojection complete.");
    }
}



// Required dependency: proj crate (https://crates.io/crates/proj)

use proj::Proj;
use std::io::{Error, ErrorKind};

pub fn reproject_raster(input: &[Vec<f64>], src_proj: &str, dst_proj: &str) -> Result<Vec<Vec<f64>>, Error> {
    // Get the transformation object for the source and destination projections
    let src = Proj::new(src_proj)?;
    let dst = Proj::new(dst_proj)?;

    // Reproject each pixel in the input raster
    let mut output = Vec::new();
    for row in input {
        let mut output_row = Vec::new();
        for &value in row {
            // Convert the coordinates and store the reprojected value
            let (x, y) = src
                .proj(&proj::Point::new(value, value))?
                .to_tuple();
            let reprojected_value = dst
                .unproj(&proj::Point::new(x, y))?
                .x;
            output_row.push(reprojected_value);
        }
        output.push(output_row);
    }

    Ok(output)
}


use std::env;
use std::io::{self, Error, ErrorKind};
use proj::Proj;
extern crate proj::Proj;

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

fn main() {
    // Get the command-line arguments
    let args: Vec<String> = env::args().collect();

    // Check if a raster path is provided
    if args.len() < 2 {
        eprintln!("Please enter a raster path.");
        return;
    }

    // Extract the raster path from the command-line arguments
    let raster_path = &args[1];

    // Example usage
    let input: Vec<Vec<f64>> = vec![vec![1.0, 2.0], vec![3.0, 4.0]];
    let src_proj = "+proj=longlat +datum=WGS84 +no_defs";
    let dst_proj = "+proj=utm +zone=32 +datum=WGS84 +units=m +no_defs";

    match reproject_raster(&input, src_proj, dst_proj) {
        Ok(reprojected) => {
            println!("Reprojection successful:");
            for row in reprojected {
                for value in row {
                    print!("{} ", value);
                }
                println!();
            }
        }
        Err(err) => eprintln!("Reprojection error: {}", err),
    }
}


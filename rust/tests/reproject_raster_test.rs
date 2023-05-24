// Test function using Rust's built-in testing framework
#[cfg(test)]

use super::*;

mod tests {

    #[test]
    fn test_reproject_raster() {
        // Define a sample input raster and projections
        let input = vec![
            vec![1.0, 2.0, 3.0],
            vec![4.0, 5.0, 6.0],
            vec![7.0, 8.0, 9.0],
        ];
        let src_proj = "+proj=longlat +ellps=WGS84";
        let dst_proj = "+proj=utm +zone=32 +ellps=WGS84";

        // Define the expected output
        let expected_output = vec![
            vec![363791.378, 364157.266, 364523.153],
            vec![364889.029, 365254.916, 365620.803],
            vec![366986.681, 367352.568, 367718.455],
        ];

        // Call the reproject_raster function
        let result = reproject_raster(&input, src_proj, dst_proj).unwrap();

        // Compare the output with the expected result
        assert_eq!(result, expected_output);
    }
}
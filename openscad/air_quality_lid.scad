use <roundedcube.scad>

FN = 100;  // Used for cylinder accuracy

// Plate properties
plate_thickness = 10; //
plate_width = 165;  // mm
radius_smooth_edge = 8;

// Inner plate properties
inner_plate_thickness = 10; //
inner_plate_width = 140;  // mm
inner_radius_smooth_edge = 5;

// Hole properties
delta_x = 5; // The position for the hole from the edge
cylinder_diameter = 4.3; // hole diameter for the screw
outer_cylinder_diameter = 7.5; // hole diameter for the screw


// DERIVED QUANTITIES
plate_height = plate_width;
inner_plate_height = inner_plate_width;
height_offset = 2 * (radius_smooth_edge - 5);   // It seems that the rounded cube is put down for
                                                // this amount of milimeters when a rounded edge is used
                                                // Not sure if this is always correct.

// Define the location for the holes
hole_location_1 = [delta_x, delta_x];
hole_location_2 = [plate_width - delta_x, delta_x];
hole_location_3 = [delta_x, plate_height - delta_x];
hole_location_4 = [plate_width - delta_x, plate_height - delta_x];

hole_location = [hole_location_1, hole_location_2, hole_location_3, hole_location_4];

module HeadPlate() {
    difference()
        {
        roundedcube([plate_width, plate_height, plate_thickness], radius=radius_smooth_edge, apply_to="zmin");
        union() {
            // Make sure we remove anything below zero
            translate([0, 0, -100]){
                cube([plate_width * 2, plate_height * 2, 100], false);
            }
            // Define an inner cube we want to remove
            translate([plate_width / 2, plate_height / 2, inner_plate_thickness / 2]){
                cube([inner_plate_width, inner_plate_height, inner_plate_thickness], true);
            }
            // Define the holes
            for (i = [0:len(hole_location)-1]) {
                translate(hole_location[i]) {
                    cylinder(h = plate_thickness + 5, r = cylinder_diameter / 2, $fn = FN);
                    translate([0, 0, plate_thickness]) {
                        cylinder(h = cylinder_diameter, r1 = cylinder_diameter / 2, r2 = outer_cylinder_diameter / 2, $fn = FN);
                    }
                    translate([0, 0, plate_thickness + cylinder_diameter]) {
                        cylinder(h = 10, r = outer_cylinder_diameter / 2, $fn = FN);
                    }
                }
            }
        }
    }
}

HeadPlate();

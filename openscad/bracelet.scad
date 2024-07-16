$fn = 60;

width_bracelet = 30;
length_bracelet = 30;

length_hole_bracelet = 0.5 * length_bracelet;
width_hole_bracelet = 2;

pos_x_hole_1 = 0.9 * width_bracelet;
pos_x_hole_2 = 0.1 * width_bracelet;
pos_y_hole = 0.50 * length_bracelet;

small_hole_width = 2;
small_hole_length = 4;
low_s_pos_hole = 0.1 * length_bracelet;
high_s_pos_hole = 0.9 * length_bracelet;
left_s_pos_hole = 0.6 * width_bracelet;
right_s_pos_hole = 0.4 * width_bracelet;

radius_edge = 10;
thickness = 5;

// Create square with holes..
linear_extrude(3) difference(){
    union(){
        difference() {
            // This creates the initial square
            square([width_bracelet, length_bracelet]);
            // This cuts out the square corners
            union() {
                translate([0, 0, 0])
                    square(radius_edge, center = false);
                translate([width_bracelet-radius_edge, 0, 0])
                    square(radius_edge, center = false);
                translate([0, length_bracelet-radius_edge, 0])
                    square(radius_edge, center = false);
                translate([width_bracelet-radius_edge, length_bracelet-radius_edge, 0])
                    square(radius_edge, center = false);
            };
        }
        // This adds the rounds corners
        translate([radius_edge, radius_edge, 0]) circle(r=radius_edge, center=true);
        translate([width_bracelet - radius_edge, radius_edge, 0]) circle(r=radius_edge, center=true);
        translate([radius_edge, length_bracelet - radius_edge, 0]) circle(r=radius_edge, center=true);
        translate([width_bracelet - radius_edge, length_bracelet - radius_edge, 0]) circle(r=radius_edge, center=true);

    }
      // Here we cutout the parts for the rope..linear_extrude
      union(){
            translate([pos_x_hole_2, pos_y_hole, 0])
                square([width_hole_bracelet, length_hole_bracelet], center=true);
            translate([pos_x_hole_1, pos_y_hole, 0])
                square([width_hole_bracelet, length_hole_bracelet], center=true);
            // Tiny holes
            translate([left_s_pos_hole, low_s_pos_hole, 0])
                square([small_hole_width, small_hole_length], center=true);
            translate([right_s_pos_hole, low_s_pos_hole, 0])
                square([small_hole_width, small_hole_length], center=true);
            // Tiny holes
            translate([left_s_pos_hole, high_s_pos_hole, 0])
                square([small_hole_width, small_hole_length], center=true);
            translate([right_s_pos_hole, high_s_pos_hole, 0])
                square([small_hole_width, small_hole_length], center=true);
        };
}

// Okay we've made a drawing... lets build it
// Everything is in mm

delta_w = 1; // mm
bottom_height = 2; // mm


inner_width_box = 55.4;
inner_length_box = 93;
inner_height_box = 55; // Note it should be open at the top

outer_width_box = inner_width_box + 2 * delta_w; // mm
outer_length_box = inner_length_box + 2 * delta_w; // mm
outer_height_box = 57; // mm

// Slanted pannel definition
slanted_pannel_width = 59;
slanted_pannel_offset = 7;
slanted_pannel_angle = 90-68.78;

// Slanted pannel support
x_offset_support = 28.4;

// Mid wall definition
width_mid_wall = 27;
x_offset_mid_wall = 28.4;
y_offset_mid_wall = 44;
height_mid_wall = inner_height_box;

// Subtract the bottom. Because of the rotation, we now have something sticking out of the bottom..
difference(){
    // I know this is cumbersone. I could substract two cubes from each other. But I wanted to try it this way
    // The bottom
    union(){
        cube([inner_width_box, inner_length_box, bottom_height], center = false);
        // left wall
        translate([- delta_w, 0, 0]) {
            cube([delta_w, inner_length_box, inner_height_box], center = false);
        }
        // right wall
        translate([inner_width_box, 0, 0]) {
            cube([delta_w, inner_length_box, inner_height_box], center = false);
        }
        // bottom wall
        translate([- delta_w, - delta_w, 0]) {
            cube([outer_width_box, delta_w, inner_height_box], center = false);
        }
        // top wall
        translate([- delta_w, inner_length_box, 0]) {
            cube([outer_width_box, delta_w, inner_height_box], center = false);
        }

        // This designs the slanted pannel which is used to hold the cards
        translate([slanted_pannel_offset, 0, 0]) {
            rotate([0, slanted_pannel_angle, 0]) {
                cube([delta_w, inner_length_box, slanted_pannel_width], center = false);
            }
        }

        // Now for a wall to separate the player tokens and the tiles
        translate([x_offset_mid_wall, y_offset_mid_wall, 0]) {
            cube([width_mid_wall, delta_w, inner_height_box], center = false);
        }
        // Support for the slanted panel
        translate([x_offset_support, 0, 0]) {
            cube([delta_w, inner_length_box, inner_height_box], center = false);
        }
    };
    translate([0, 0, -bottom_height]) {
        cube([inner_width_box+1, inner_length_box+1, bottom_height], center = false);
    }
}


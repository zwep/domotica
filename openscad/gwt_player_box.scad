// Okay we've made a drawing... lets build it
// Everything is in mm

// Je moet hier nog de zijkant uitsnijden
// En een stuykje uit snijden waar een ander dingejte komt op het schuine stuk

delta_w = 1; // mm
bottom_height = 2; // mm
thickness_cutout = 2;

inner_width_box = 57;
inner_length_box = 95;
inner_height_box = 55; // Note it should be open at the top

outer_width_box = inner_width_box + 2 * delta_w; // mm
outer_length_box = inner_length_box + 2 * delta_w; // mm
outer_height_box = 57; // mm

// Slanted pannel definition
slanted_pannel_width = 59;
slanted_pannel_offset = 7;
slanted_pannel_angle = 90-68.78;
// Used to create a hole in the slanted pannel to fit a piece
slanted_pannel_inner_width = 35;
slanted_pannel_inner_length = 85;

// Slanted pannel support
polygon_x_offset = 28.4;

// Mid wall definition between tokens and tiles
width_mid_wall = inner_width_box - polygon_x_offset;
x_offset_mid_wall = 28.4;
y_offset_mid_wall = 44;
height_mid_wall = inner_height_box;

cylinder_cutout_radius = width_mid_wall / 3;

// Tile podium
height_tile_podium = 8;
// Token podium
height_token_podium = 15;

module BoundaryBox(outer_width_box, inner_width_box, inner_length_box, bottom_height, delta_w) {
    union() {
        // bottom
        cube([inner_width_box, inner_length_box, bottom_height], center = false);

        // left wall
        translate([- delta_w, 0, 0]) {
            cube([delta_w, inner_length_box, inner_height_box], center = false);
        }
        // right wall
        translate([inner_width_box, 0, 0]) {
            cube([delta_w, inner_length_box, inner_height_box], center = false);
        }
        // lower wall
        translate([- delta_w, - delta_w, 0]) {
            cube([outer_width_box, delta_w, inner_height_box], center = false);
        }
        // upper wall
        translate([- delta_w, inner_length_box, 0]) {
            cube([outer_width_box, delta_w, inner_height_box], center = false);
        }
    }
};

module CardHolder (inner_length_box, slanted_pannel_inner_length, slanted_pannel_inner_width, polygon_x_offset, slanted_pannel_offset) {
     difference() {
        // THis designs a polygon that holds the cards
         translate([polygon_x_offset, inner_length_box, 0]) {
             rotate([90, -90, 0]) {
                 linear_extrude(height = inner_length_box) {
                     polygon(points = [[0, 0], [0, polygon_x_offset - slanted_pannel_offset], [inner_height_box, 0]],
                     paths = [[0, 1, 2]]);
                 }
             }
         }
       // This designs the cutout in the slanted pannel which is used to hold a special tile
         translate([slanted_pannel_offset, 0, 0]) {
             rotate([0, slanted_pannel_angle, 0]) {
                 // Added error margin of 5% to cut out
                 translate([0, (inner_length_box - 1.05 * slanted_pannel_inner_length) / 2, (slanted_pannel_width - 1.05 * slanted_pannel_inner_width)]) {
                     cube([thickness_cutout * 1.05, slanted_pannel_inner_length * 1.05, slanted_pannel_inner_width * 1.05], center = false);
                 }
             }
         }
     }
};

module TileHolder(x_offset_mid_wall, y_offset_mid_wall, width_mid_wall, height_tile_podium, inner_height_box, delta_w, cylinder_cutout_radius) {
    // An ellevation for the tile square to more easily grab the tiles
    translate([x_offset_mid_wall, 0, 0]) {
        cube([width_mid_wall, y_offset_mid_wall, height_tile_podium], center = false);
    }
    // Now for a wall to separate the player tokens and the tiles
    translate([x_offset_mid_wall, y_offset_mid_wall, 0]) {
        difference() {
            cube([width_mid_wall, delta_w, inner_height_box], center = false);
            translate([-width_mid_wall/2, -delta_w/2, inner_height_box - cylinder_cutout_radius + 2 * delta_w]) {
                // Factor 2 is used here to make sure we get a clean cut
                cube([width_mid_wall, 2 * delta_w, 2 * cylinder_cutout_radius], center = false);
            }
        }
    }
};



difference(){
    union(){
        BoundaryBox(outer_width_box, inner_width_box, inner_length_box, bottom_height, delta_w);
        color("blue")
        CardHolder(inner_length_box, slanted_pannel_inner_length, slanted_pannel_inner_width, polygon_x_offset, slanted_pannel_offset);
        TileHolder(x_offset_mid_wall, y_offset_mid_wall, width_mid_wall, height_tile_podium, inner_height_box, delta_w, cylinder_cutout_radius);


        // An ellevation for the pieces
//        color("red")
//        translate([x_offset_mid_wall, y_offset_mid_wall, 0]) {
//            cube([width_mid_wall, y_offset_mid_wall, height_token_podium], center = false);
//        }
        color("green")
        // THis designs a polygon that holds the cards
         translate([2*x_offset_mid_wall, 2*y_offset_mid_wall, bottom_height]) {
             rotate([90, -90, 0]) {
                 linear_extrude(height = y_offset_mid_wall) {
                     polygon(points = [[0, 0], [0, width_mid_wall], [height_token_podium, 0]],
                     paths = [[0, 1, 2]]);
                 }
             }}

    }

    // The circular cutout to more easily grab cards..?
    translate([1.5*x_offset_mid_wall, -0.1 * outer_length_box, outer_height_box])
    rotate([0, 90, 90]) {
        cylinder(h = outer_length_box, r = cylinder_cutout_radius);
    }
}

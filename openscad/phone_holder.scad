/*
Everything is in milimeters
 */

width_casing = 82;
height_casing = 20;

width_seb_phone = 77;
width = 2;
width_side = (width_casing - width_seb_phone) / 2;
width_break = 9;
depth_break = 3;

length_side = 29;

hole_width = 5;
hole_depth = 3;
hole_position = length_side - width_break / 2 - hole_width/2;

difference(){
    union()
        {
        // Back side
        translate([-width_casing/2, 0, 0])
            cube([width_casing, width, height_casing]);
        // Right side
        translate([width_casing/2, 0, 0])
            cube([width_side, length_side, height_casing]);
        // Left side
        translate([-width_casing/2, 0, 0])
            cube([width_side, length_side, height_casing]);
        // Left break
        translate([-width_casing/2-depth_break, length_side - width_break, 0])
            cube([depth_break, width_break, height_casing]);
        // Right break
        translate([width_casing/2+width_side, length_side - width_break, 0])
            cube([depth_break, width_break, height_casing]);
    };
    union(){
    // Left hole (for adding more of these things..)
    translate([width_casing/2, hole_position, -1])
        cube([hole_depth, hole_width, 1.1*height_casing]);
    // Right hole (for adding more of these things..)
    translate([-width_casing/2-hole_depth+width_side, hole_position, -1])
        cube([hole_depth, hole_width, 1.1*height_casing]);
}
}
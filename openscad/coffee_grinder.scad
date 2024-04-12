/*

Design to create a coffee grinder adapter for my drill

All sizes are in mm
 */

// Top
//     <     outer diameter top    >
//      ___________________________
//     |____                   ____| <outer_height_top
//         |   (hole width)    |     <inner_height_top
//         |________| |________|     <inner_height_top
//          <inner diameter top>

FN = 50;

inner_diameter_top = 54;
outer_diameter_top = 66;
inner_height_top = 15;
outer_height_top = 3;
// These are the holes in the inner diameter cylinder that
// keep the whole thing in place
hole_width_top = 3;
hole_height_top = 10;
hole_depth_top = 1;


// The hole for the adapter
diameter_hole = 13.5;
// Slight modification
_diameter_hole = diameter_hole - 0.5;
// The width of the bar that is used to drive the grinder
width_driver_grinder = 5;
width_driver_drill = 7.5;
height_driver_grinder = 24;


module grinder_top() {
    /*
    Here we define the top for the grinder. It should have all the same dimensions as the original one
     */
    difference() {
        union() {
            translate([0, 0, inner_height_top]) {
                cylinder(h = outer_height_top, d = outer_diameter_top, $fn = FN);}
            cylinder(h = inner_height_top, d = inner_diameter_top, $fn = FN);
        };

        cylinder(h = inner_height_top + outer_height_top, d = diameter_hole);
        translate([inner_diameter_top / 2, 0, 0]) {
            cube([2 * hole_depth_top, hole_width_top, 2 * hole_height_top], center = true);
        };
        translate([0, inner_diameter_top / 2, 0]) {
            cube([hole_width_top, 2 * hole_depth_top, 2 * hole_height_top], center = true);
        };
        translate([- inner_diameter_top / 2, 0, 0]) {
            cube([2 * hole_depth_top, hole_width_top, 2 * hole_height_top], center = true);
        };
        translate([0, - inner_diameter_top / 2, 0]) {
            cube([hole_width_top, 2 * hole_depth_top, 2 * hole_height_top], center = true);
        };
    }
}


module grinder_adapter() {
    // Now we want to make the adapter between the grinder and the drilling machine
    difference() {
        cylinder(h = 2 * height_driver_grinder, d = _diameter_hole, $fn = FN);
        cube([width_driver_grinder, width_driver_grinder, 2 * height_driver_grinder], center = true);
        translate([0, 0, height_driver_grinder]){
            cylinder(h = height_driver_grinder, d = width_driver_drill, $fn=6);
        }
    }

}



//grinder_top();
grinder_adapter();

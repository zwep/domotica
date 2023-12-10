golden_ratio = 1.618;
FN = 100;

arm_thickness = 3; // Thickness of the arm-plate, this should fit a 3mm screw
plate_thickness = 5; //
arm_distance = 56; // The distance between the arm-plates
delta_x = arm_thickness; // The position for the hole from the edge

// Make hole for the screw + nut
cylinder_diameter = 3; // hole diameter for the screw
cylinder_length = 15; // length of the screw..?
box_width = 5.5; // width of a 3mm hex nut
box_height = 2.5; // ... height of a 3mm hex nut

// DERIVED QUANTITIES
plate_width = arm_distance +  2 * (delta_x + 0.5 * arm_thickness); // Head plate width
plate_height = arm_distance / golden_ratio; // Head plate height
arm_width = plate_height; // Of course, arm plate width should be same as head-plate height
arm_length = plate_height; // I dont know, lets do this..
box_thickness = arm_thickness; //

// Define the location for the holes
hole_location_1 = [delta_x, delta_x];
hole_location_2 = [plate_width - delta_x, delta_x];
hole_location_3 = [delta_x, plate_height - delta_x];
hole_location_4 = [plate_width - delta_x, plate_height - delta_x];

screw_location_1 = [0, delta_x, arm_thickness / 2 ];
screw_location_2 = [0, arm_length - delta_x, arm_thickness / 2 ];

box_location_1 = [cylinder_length / 2, delta_x, arm_thickness / 2 ];
box_location_2 = [cylinder_length / 2, arm_length - delta_x, arm_thickness / 2 ];

module HeadPlate() {
    difference() {
        cube([plate_width, plate_height, plate_thickness]);
        union() {
            translate(hole_location_1) {cylinder(h = arm_thickness + 1, r = cylinder_diameter / 2, $fn=FN);}
            translate(hole_location_2) {cylinder(h = arm_thickness + 1, r = cylinder_diameter / 2, $fn=FN);}
            translate(hole_location_3) {cylinder(h = arm_thickness + 1, r = cylinder_diameter / 2, $fn=FN);}
            translate(hole_location_4) {cylinder(h = arm_thickness + 1, r = cylinder_diameter / 2, $fn=FN);}
        };
    }
}

module ArmPlate(){
    // Now make one arm...
    difference() {
        cube([arm_width, arm_length, arm_thickness]);
        union() {
            // Screw locations
            translate(screw_location_1) {rotate([0, 90, 0]) {cylinder(h = cylinder_length, r = cylinder_diameter / 2, $fn =
            FN);
            }}
            translate(screw_location_2) {rotate([0, 90, 0]) {cylinder(h = cylinder_length, r = cylinder_diameter / 2, $fn =
            FN);
            }}
            // Box locations
            translate(box_location_1) {cube([box_height, box_width, arm_thickness], center = true);}
            translate(box_location_2) {cube([box_height, box_width, arm_thickness], center = true);}
        }}
}



new_plate_width = arm_distance +  2 * arm_thickness;

difference(){
    cube([new_plate_width, arm_width, arm_length]);
    translate([arm_thickness, 0, plate_thickness]){
        cube([arm_distance, arm_width, arm_length]);
    };
}

// HeadPlate();
//ArmPlate();

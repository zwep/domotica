use <ellipse_extrude.scad>

diameter_button = 17.5;
height_button = 5;

// Here we create the part that is attached to the suit
height_feet = 4;
width_feet = 4;
thickness_feet = 3;
wall_thickness = 2;

translate([0, 0, height_feet])
    ellipse_extrude(height_button) 
        circle(d=diameter_button);

translate([0, 0, height_feet/2])
    difference(){
        cube([thickness_feet, width_feet, height_feet], center = true);
        cube([thickness_feet, width_feet-wall_thickness, height_feet-wall_thickness], center = true);
    };
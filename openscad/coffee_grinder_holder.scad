
radius_lid = 20;
width_groove = 3;
height_groove = 2;
overhang_lid = 4;
thickness_lid = 2;

inner_radius_coffee_grinder = 4;
outer_radius_coffee_grinder = 4+1;
inner_height_coffee_grinder = 4;

//
difference(){
    cylinder(h=thickness_lid, d=radius_lid+overhang_lid);
    // Make a groove in the botto of the lid..
    difference(){
    cylinder(h=height_groove, d=radius_lid + width_groove / 2);
        cylinder(h=height_groove, d=radius_lid - width_groove / 2);
    }
    // Cutout the circle for the coffee grinder in the middle of the lid
    cylinder(h=10, d=inner_radius_coffee_grinder);
}
// Now add a cylinder on top of the cutout that acts as a mount for the coffee grinder
// (Only need to add some screw stuff)
 difference(){
    cylinder(h=inner_height_coffee_grinder, d=outer_radius_coffee_grinder);
    cylinder(h=inner_height_coffee_grinder, d=inner_radius_coffee_grinder);
}



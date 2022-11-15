// Functions and stuff
module elrdcyl(
   w, // width of cylinder
   d, // depth of cylinder
   h1,// straight height of cylinder
   h2 // height of rounded top
   ) {
   intersection(){
     union(){
       scale([w/2,d/2,1])cylinder(r=1,h=h1,$fn=36);  // cylinder
       translate([0,0,h1])scale([w/2,d/2,h2])sphere(r=1,$fn=36);  // top
     }
     scale([w/2,d/2,1])cylinder(r=1,h=h1+h2,$fn=36); // only needed if h2>h1
   }
}

bottom_height = 2;
wall_thickness = 2;
// This is the width WITH sleeves
// It is in agreement with the /Retail-Sleeved-Cards.scad
width = 67 + 2 * wall_thickness;
height = 25;
length = 92 + 2 * wall_thickness;

width_outer_box = 2 * width - wall_thickness/2;
width_inner_box = width - 1.5 * wall_thickness;
width_space_box = 0.5 * width;

font_size = 40;

max_width = 206;
max_height = 114;
residual_width = max_width - width_outer_box;
residual_height = max_height - length;

difference(){
   cube([width_outer_box, length, height],center=true);
    // These are two cubes that allow for the space of the two card slots
    union(){
            translate(v=[-(width_inner_box)/2-wall_thickness/2, 0, bottom_height])
                cube([width_inner_box, length-wall_thickness, height],center=true);
            translate(v=[width_inner_box/2+wall_thickness/2, 0, bottom_height])
                cube([width_inner_box, length-wall_thickness, height],center=true);
        }
    // Here are two cubes that allow for an easy grab of the cards
        union(){
            translate(v=[-(width_inner_box)/2-wall_thickness/2, 0, bottom_height])
                cube([width_space_box, 2*length, height],center=true);
            translate(v=[width_inner_box/2+wall_thickness/2, 0, bottom_height])
                cube([width_space_box, 2*length, height],center=true);
        }
    // Here is a text example that I want to use to cutout player signs...
    translate([-width_inner_box/2, 0, -height/2-bottom_height/2]) {
        linear_extrude(height=2*bottom_height){
            text("II", size=font_size, font = "Cambria", halign="center", valign="center");
        }
    }
    translate([width_inner_box/2, 0, -height/2-bottom_height/2]) {
            linear_extrude(height=2*bottom_height){
                text("II+", size=font_size, font = "Cambria", halign="center", valign="center");

            }
        }
}


//Now create the support on the sides..
delta_top_bottom = residual_height/2;
delta_side = residual_width/2;

// Making a rounding thing....
//Left side
translate([-width_outer_box/2, 0, -height/2]) {
    difference() {
        elrdcyl(2 * delta_side, delta_side, 0, height / 2);
        translate([0, - delta_side, - height / 2]) {
            cube([delta_side, 2 * delta_side, 2 * height], center = false);
        }
    }
}
// Right side
translate([width_outer_box/2, 0, -height/2]) {
    difference() {
        elrdcyl(2 * delta_side, delta_side, 0, height / 2);
        translate([-delta_side, -delta_side, -height / 2]) {
            cube([delta_side, 2*delta_side, 2 * height], center = false);
        }
    }
}
// Top side
translate([0, length/2, -height/2]) {
    difference() {
        elrdcyl(delta_side, 2 * delta_top_bottom, 0, height / 2);
        translate([-delta_side, -delta_side, -height / 2]) {
            cube([2 * delta_side, delta_side, 2 * height], center = false);
        }
    }
}
// Bottom side
translate([0, -length/2, -height/2]) {
    difference() {
        elrdcyl(delta_side, 2 * delta_top_bottom, 0, height / 2);
        translate([-delta_side, 0, -height / 2]) {
            cube([2 * delta_side, delta_side, 2 * height], center = false);
        }
    }
}
/*
shower drain

Author  : Dave Borghuis
Email   : contact@twenspace.nl
Website : https://twenspace.nl
Licence : (c) by TwenSpace / Dave Borghuis

If you want to use this model for e.g. commercial user please contact me.

*/
type = "Circle";//[Circle, Square]

lid_diameter = 88;
lid_height = 2;

pipe_diameter = 75;
pipe_length = 30;

/*[Advanced]*/
lid_holes = 32;
//Size of hole in diameter
lid_holes_size = 4.5;


/*[Hidden]*/
$fn=100;

translate([0,0,lid_height]) rotate([0,180,0]) shower_drain();

module shower_drain() {
    
    difference() {        
        if (type=="Circle") {
            cylinder(h=lid_height,r=lid_diameter/2);
        } else {
            translate([0,0,lid_height/2]) cube([lid_diameter,lid_diameter,lid_height],center=true);            
        };
        
        
        //pathRadius=pipe_diameter/2;
        pathRadius=lid_diameter/2 - 1.2 * lid_holes_size/2;
        #for (i=[1:lid_holes])  {
            translate([pathRadius*cos(i*(360/lid_holes)),pathRadius*sin(i*(360/lid_holes)),0]) cylinder(r=lid_holes_size/2,h=lid_height, $fn=20);
        }
    }
    
    
    //make pipe
    translate([0,0,-pipe_length])
    difference() {
        cylinder(h=pipe_length,r=pipe_diameter/2);
        cylinder(h=pipe_length,r=pipe_diameter/2-lid_height);
    }
    
}
diameter_foot = 20;
width_foot = 50;

difference(){
    cylinder(h = width_foot, d = diameter_foot);
    translate([-diameter_foot / 4, -5, 0])   cube([diameter_foot/2, diameter_foot, width_foot]);
};


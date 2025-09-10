module mybox(size, width){
    // size is a 3-element list width the x,y,z dimensions
    // the width is the border width
    x = size[0];
    y = size[1];
    z = size[2];
    difference(){
        cube([x, y, z], center=true);
        translate([0, 0, width])
            cube([x-width, y-width, z], center=true);
    };
}

module myroundrectangle(width, length, radius) {
    // substracting/adding radius so that we set the true width and length
    // with the input parameters
    point_1 = [(width - radius) / 2, (length - radius) / 2];
    point_2 = [(width - radius) / 2, (-length + radius) / 2];
    point_3 = [(-width + radius) / 2, (-length + radius) / 2];
    point_4 = [(-width + radius) / 2, (length - radius) / 2];
    hull() {
        translate(point_1)
            circle(radius, $fn = 100);
        translate(point_2)
            circle(radius, $fn = 100);
        translate(point_3)
            circle(radius, $fn = 100);
        translate(point_4)
            circle(radius, $fn = 100);
    }
}

module myroundwall(width, length, height, wall_width, radius) {
    difference(){
        linear_extrude(height)
            myroundrectangle(width, length, radius);
        linear_extrude(height)
            myroundrectangle(width-wall_width, length-wall_width, radius);
    }
}


module myroundbox(width, length, height, radius) {
    linear_extrude(height)
        myroundrectangle(width, length, radius);
}


// Here are some global varialbes
$fn = 50;
rad = 57.29578;

// These below are globals.. used to call some functions...
MAX_DEGREE = 360;

N_TOOTH = 12; // Yeah its just 12 tooths..
WIDTH_TOOL = 4; // Using 5 millimeter for width of the 'mouth'
HEIGHT_TOOL = 7; // Measured about 8 or so.. again, want an easy fit
INNER_RADIUS = 26.4; // The measured inner radius is about 26.4 mm, using less for an easy fit
OUTER_RADIUS = 28.5;  // The measured part is about 29mm, using less to be sure it fits easily

RADIUS_HOLE = 22; // 20 mm measured. Extra for wiggle room

HEIGHT_ARM = 5; // Dunno, thickness of the arm...
LENGTH_ARM = 200 ; // Some indication for the 'arm' of the tool. Not sure if this works well


module honeywell_gear(n_tooth, inner_radius, outer_radius){
    // This creates a circle with 'Tooths'
    tau = 360/n_tooth;
    union() {
        polygon([for (rot = [0:tau:MAX_DEGREE]) [inner_radius * cos(rot), inner_radius * sin(rot)]]);
        for (rot = [0:tau:MAX_DEGREE]){
            x0 = inner_radius * cos(rot);
            y0 = inner_radius * sin(rot);

            x1 = outer_radius * cos(rot + tau/2);
            y1 = outer_radius * sin(rot + tau/2);

            x2 = inner_radius * cos(rot + tau);
            y2 = inner_radius * sin(rot + tau);
            echo([[x0,y0], [x1, y1], [x2, y2]]);
            polygon([[x0,y0], [x1, y1], [x2, y2]]);
        }
   }
}


module honeywell_gear_hollow(n_tooth, inner_radius, outer_radius, width_tool, height_tool){
    // Here we create the 'mouth' used to get into the tool
    // Adding height of the arm to it, so that netto we still have the desired height.
    linear_extrude(height = height_tool){
        difference(){
            honeywell_gear (n_tooth=n_tooth, inner_radius=inner_radius, outer_radius=outer_radius);
            honeywell_gear (n_tooth=n_tooth, inner_radius=inner_radius - width_tool, outer_radius=outer_radius - width_tool);
        };
    };
}


module tool_arm(){
    // Here we create the handle / arm to rotate it...
    // This is also where the trouble starts..
    difference(){
    translate([0, LENGTH_ARM / 2 - OUTER_RADIUS , 0]){
        cube([2 * OUTER_RADIUS, LENGTH_ARM, HEIGHT_ARM], center=true);
    };
        cylinder(h = 2 * HEIGHT_ARM, center=true, r=RADIUS_HOLE);
}
}

// Creat tool without arm
//honeywell_gear_hollow(max_degree = MAX_DEGREE, n_tooth = N_TOOTH, inner_radius = INNER_RADIUS,
//outer_radius = OUTER_RADIUS, width_tool = WIDTH_TOOL, height_tool = HEIGHT_TOOL + HEIGHT_ARM);


// Create tool with arm
union() {
    tool_arm();
    honeywell_gear_hollow(max_degree = MAX_DEGREE, n_tooth = N_TOOTH, inner_radius = INNER_RADIUS,
    outer_radius = OUTER_RADIUS, width_tool = WIDTH_TOOL, height_tool = HEIGHT_TOOL + HEIGHT_ARM);
}

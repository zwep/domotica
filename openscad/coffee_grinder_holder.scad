include <threads.scad>

$fn = 90;
radius_lid = 110;
width_groove = 2;
height_groove = 2;
overhang_lid = 2;
thickness_lid = 4;

outer_radius_grinder_mount = 46;
width_grinder_mount = 3;
inner_radius_grinder_mount = outer_radius_grinder_mount - width_grinder_mount;

height_grinder_mount = 26; // This is the actual height
height_grinder_mount_thread = 10; // This should replace the top

/*
difference(){
    // This created the main disk and puts the mount on top 
    union(){
        cylinder(h=height_grinder_mount, d=outer_radius_grinder_mount);
        cylinder(h=thickness_lid, d=radius_lid+overhang_lid);
    };
    // This will be subtracted
    union(){
        // This is to make the groove
        difference(){
            cylinder(h=height_groove, d=radius_lid + width_groove / 2);
            cylinder(h=height_groove, d=radius_lid - width_groove / 2);
        }
        // This is to make the cutout in the mount
        cylinder(h=height_grinder_mount, d=inner_radius_grinder_mount);
    };
};
*/ 

// Lets try to cutout some parts...
// cylinder(h=height_grinder_mount, d=inner_radius_grinder_mount);

    
difference(){
ScrewThread(outer_radius_grinder_mount, height_grinder_mount_thread, pitch=4, tooth_angle=50, tip_height=4, tooth_height=2, tip_min_fract=1);
    cylinder(h=height_grinder_mount, d=inner_radius_grinder_mount);
    cube([inner_radius_grinder_mount/3, inner_radius_grinder_mount*3, height_grinder_mount],center=true);
    };


difference(){
    cylinder(h=height_grinder_mount_thread, d=inner_radius_grinder_mount+1);
    cylinder(h=height_grinder_mount_thread, d=inner_radius_grinder_mount);
};





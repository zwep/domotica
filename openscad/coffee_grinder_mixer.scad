include <coffee_grinder.scad>;


rotate([0, 180, 0]){
translate([0, 0, 104+1]){
    rotate([0, 180, 0]){
        grinder_adapter();
    }
}

rotate([0, 180, 0]){
import("/home/bugger/Documents/Thuis/3d_printer/BoschMixer/Links.stl");
}

}
//translate([0, 0, -141]){
//    import("/home/bugger/Documents/Thuis/3d_printer/sword/LoZ_Sword_Guard.stl");
//    import("/home/bugger/Documents/Thuis/3d_printer/sword/LoZ_Sword_Pommel.stl");
//    import("/home/bugger/Documents/Thuis/3d_printer/sword/LoZ_Sword_Grip.stl");
//}

$fn=100;
diameter_bar = 6.25;
diameter_2_diploma_case = 88;
thickness_diploma_case = 2;
diameter_1_diploma_case = diameter_2_diploma_case + 1;
height_diploma_case = 50;
difference() {
    cylinder(h = height_diploma_case + thickness_diploma_case, d = diameter_2_diploma_case + thickness_diploma_case);
    cylinder(h = height_diploma_case, d1 = diameter_1_diploma_case, d2 = diameter_2_diploma_case);
    cylinder(h = 2*height_diploma_case, d = diameter_bar);
}

//import("/home/bugger/Documents/Thuis/3d_printer/sword/LoZ_Sword_Gem.stl");
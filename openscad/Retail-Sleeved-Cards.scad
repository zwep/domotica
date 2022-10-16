use <slidebox.scad>

// This is from a thingiverse product. Not created by me
// Here: https://www.thingiverse.com/thing:3997817/files
$fn = 70;

AddLid = false;
LidHeight = 2.2;
railThickness = 1.4;
lidTolerance = 0.4;
zTolerance = 0.3;

lidPadding = 8;
lidPattern = "Hex";
wallThickness = 1.5;

cardPadding = 1;

stackWidth = 66 + cardPadding;
stackLength = 91 + cardPadding;

NetTotalX = wallThickness * 4 + stackWidth * 3;
NetTotalY = wallThickness * 2 + stackLength;

TotalX = NetTotalX + (AddLid ? (railThickness + LidHeight - wallThickness) * 2: 0);
TotalY = NetTotalY;
TotalZ  = 26.4 - (AddLid ? LidHeight : 0);

GrossTotalY = 111;
addPadding = true;

printBox = true;
printLid = false;

cutoutRadius = 18;
cutoutWallsize = 18;

module halfSideCutout (height) {
    difference () {
        union () {
            translate([0, height - cutoutRadius])
            square([stackWidth / 2 - cutoutWallsize + cutoutRadius, cutoutRadius + 20]);        
            square([stackWidth / 2 - cutoutWallsize, height]);
        }
        
        translate([stackWidth / 2 - cutoutWallsize + cutoutRadius, height - cutoutRadius])
        circle(r = cutoutRadius);
    }
}

module sideCutout(height) {
    difference () {
        translate([0,wallThickness + 0.01,-0.01])
        rotate([90,0,0])
        linear_extrude(height = wallThickness + 50) {
            union() {
                scale([-1,1])
                halfSideCutout(height+0.02);            
                halfSideCutout(height+0.02);
            }
        }        
    }
}



if (printBox) {
    intersection () {
    difference() {
        union() {
            if (AddLid) {
                rotate([0,0,-90])
                translate([-TotalY,0,0])
                rails(TotalY, TotalX, TotalZ, railThickness, LidHeight, true, true, 0); 
            }
            cube([TotalX, TotalY, TotalZ]);
            
            if (addPadding) {
                translate([0,(GrossTotalY - TotalY) / -2,0])
                difference () {
                    cube([TotalX, GrossTotalY, TotalZ]);
                    
                    translate([TotalX / 2 - stackWidth / 2,wallThickness,1.2])
                    cube([stackWidth, GrossTotalY - wallThickness * 2, TotalZ]);
                    
                    translate([TotalX / 2 - stackWidth * 1.5 - wallThickness,wallThickness,1.2])
                    cube([stackWidth, GrossTotalY - wallThickness * 2, TotalZ]);
                    
                    translate([TotalX / 2 + stackWidth * 0.5 + wallThickness,wallThickness,1.2])
                    cube([stackWidth, GrossTotalY - wallThickness * 2, TotalZ]);
                }
            }
        }
        
        translate([TotalX / 2 - stackWidth / 2,wallThickness,1.2])
        cube([stackWidth, stackLength, TotalZ]);
        
        translate([TotalX / 2 - stackWidth * 1.5 - wallThickness,wallThickness,1.2])
        cube([stackWidth, stackLength, TotalZ]);
        
        translate([TotalX / 2 + stackWidth * 0.5 + wallThickness,wallThickness,1.2])
        cube([stackWidth, stackLength, TotalZ]);
        
        translate([TotalX / 2,0,0])
        union () {
            sideCutout(TotalZ);
            translate([0,wallThickness, -1])
            scale([stackWidth - cutoutWallsize - cutoutRadius, stackLength *.6, TotalZ * 2])
            cylinder(r = 0.5, h = 1);
        }
        
        translate([TotalX / 2 - stackWidth - wallThickness,0,0])
        union () {
            sideCutout(TotalZ);
            translate([0,wallThickness, -1])
            scale([stackWidth - cutoutWallsize - cutoutRadius, stackLength *.6, TotalZ * 2])
            cylinder(r = 0.5, h = 1);
        }
        
        translate([TotalX / 2 + stackWidth + wallThickness,0,0])
        union () {
            sideCutout(TotalZ);
            translate([0,wallThickness, -1])
            scale([stackWidth - cutoutWallsize - cutoutRadius, stackLength *.6, TotalZ * 2])
            cylinder(r = 0.5, h = 1);
        }
                
        translate([TotalX / 2,TotalY,0])
        rotate([0,0,180])
        union () {
            sideCutout(TotalZ);
            translate([0,wallThickness, -1])
            scale([stackWidth - cutoutWallsize - cutoutRadius, stackLength *.6, TotalZ * 2])
            cylinder(r = 0.5, h = 1);
        }
        
        translate([TotalX / 2 - stackWidth - wallThickness,TotalY,0])
        rotate([0,0,180])
        union () {
            sideCutout(TotalZ);
            translate([0,wallThickness, -1])
            scale([stackWidth - cutoutWallsize - cutoutRadius, stackLength *.6, TotalZ * 2])
            cylinder(r = 0.5, h = 1);
        }
        
        translate([TotalX / 2 + stackWidth + wallThickness,TotalY,0])
        rotate([0,0,180])
        union () {
            sideCutout(TotalZ);
            translate([0,wallThickness, -1])
            scale([stackWidth - cutoutWallsize - cutoutRadius, stackLength *.6, TotalZ * 2])
            cylinder(r = 0.5, h = 1);
        }
    }
    
    if (addPadding) {
        translate([TotalX / 2, GrossTotalY / 2 + (TotalY - GrossTotalY) / 2, 0])
        RCube(TotalX, GrossTotalY, TotalZ + LidHeight + 10, 2);    
    } else {
        translate([TotalX / 2, TotalY / 2, 0])
        RCube(TotalX, TotalY, TotalZ + LidHeight + 10, 2);
    }

    }
}

if (printLid) {
    rotate([0,0,-90])
    translate([GrossTotalY - TotalY,0,0])
    lid2(lidPattern, TotalY, TotalX, lidPadding, LidHeight, railThickness, lidTolerance, true, 0);
}
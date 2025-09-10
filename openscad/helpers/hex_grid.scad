include <BOSL2/std.scad>
// The Belfry OpenSCAD Library V2
// Source: https://github.com/revarbat/BOSL2
// Edited: by me
// BOSL2 is licensed under BSD 2-Clause License
//    https://github.com/revarbat/BOSL2/blob/master/LICENSE

////////////////////////////////////////////////////////////////////
// cell: takes three parameters and returns a single hexagonal cell
//
////////////////////////////////////////////////////////////////////
module cell(width, height, wall) {
    assert ((width - 2 * wall) >= 0, "Invalid width-wall");
    difference() {
        cyl(d=width,h=height,$fn=6,circum=true);
        cyl(d=width-2*wall,h=height,$fn=6,circum=true);
    }
}

////////////////////////////////////////////////////////////////////
// grid: takes three parameters and returns the initial grid of
//    hexagons
//
//    size: 3-vector (x,y,z) that specifies the  size of the cube
//      that contains the hex grid
////////////////////////////////////////////////////////////////////
module grid(size,cell_width,cell_wall) {
  dx=cell_width*sqrt(3)-cell_wall*sqrt(3);
  dy=cell_width-cell_wall;

  ycopies(spacing=dy,l=size[1])
    xcopies(spacing=dx,l=size[0]) {
      cell(width=cell_width,
           height=size[2],
           wall=cell_wall);
        // Here we make a smart jump diagonally
      right(dx/2)fwd(dy/2)
      // Then add another cell
      cell(width=cell_width,
          height=size[2],
          wall=cell_wall);
    }
 }

module create_border(size, wall_width) {
    b = 2*wall_width;
    difference () {
        cuboid(size=size);
        cuboid(size=[size[0]-b,size[1]-b,size[2]+b]);
    }
}
////////////////////////////////////////////////////////////////////
// create_grid: creates a rectangular grid of hexagons with a border
//   thickness specified in the parameter (wall).
//
//   size: 3-vector (x,y,z) that specifies the length, width, and
//     depth of the final grid
//   cell_width: width of each cell
//   cell_wall: wall thickness of each cell
////////////////////////////////////////////////////////////////////
module create_grid(size, border_width, cell_width, cell_wall, border) {

    //create_border(size, border_width);
    border();
    intersection() {
        grid(size=size,cell_width=cell_width,cell_wall=cell_wall);
        border();
    }
}

////////////////////////////////////////////////////////////////////
// Example
// To use call create_grid with
////////////////////////////////////////////////////////////////////

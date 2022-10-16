// Okay we've made a drawing... lets build it
// Everything is in mm

delta_w = 2; // mm
bottom_height = 2; // mm


outer_width_box = 6; // mm
outer_length_box = 97; // mm
outer_height_box = 57; // mm

inner_width_box = outer_width_box - 2 * delta_w;
inner_length_box = outer_length_box - 2 * delta_w;
inner_height_box = 55; // Note it should be open at the top

// Mid wall definition
width_mid_wall = 27;
height_mid_wall = inner_height_box;

// Triangle/Prism/slope definition
// Calculations come from the following
//     ...
//    ...
//   ...
//  ...
//
// These are the visualization of the cards
// Thickness of card: 7mm
// Width of cards (schuine hoogte heir): 59 mm
// Height of box: 55 mm
// From this we get an angle
// ... x = 55 / (tan(asin(55/59))

width_prism = 2.14;
polyhedron(//pt 0        1        2        3        4        5
          points=[[0,0,0], [l,0,0], [l,w,0], [0,w,0], [0,w,h], [l,w,h]],
          faces=[[0,1,2,3],[5,4,3,2],[0,4,5,1],[0,3,4],[5,2,1]]
          );

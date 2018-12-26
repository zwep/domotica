// This function is used to visualize the tree that is created
// This is all done by d3.js
// Originates from https://bl.ocks.org/mbostock/4339083 (d3 js v3)
// Can be updated by looking at https://bl.ocks.org/d3noob/43a860bc0024792f8803bba8ca0d5ecd (d3 js v4)

var margin = {top: 20, right: 120, bottom: 20, left: 120},
    width = 960 - margin.right - margin.left,
    height = 800 - margin.top - margin.bottom;

var i = 0,
    duration = 750,
    clicks = 0,
    DELAY = 400,
    root;

var tree = d3.layout.tree()
    .size([height, width]);

var diagonal = d3.svg.diagonal()
    .projection(function(d) { return [d.y + 50, d.x]; });

var svg = d3.select("body").append("svg")
    .attr("width", width + margin.right + margin.left)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

root.x0 = height / 2;
root.y0 = 0;

function collapse(d) {
    if (d.children) {
        d._children = d.children;
        d._children.forEach(collapse);
        d.children = null;
    }
}

// root.children.forEach(collapse);
update(root);

d3.select(self.frameElement).style("height", "800px");

// Here we set the colors of the rectangles and hover..
// Is not incorporated in the css, because this was easier...
var color_rect = "#fff";
var color_rect_child = "#b0c4de";
var hover_color_rect = '#fff593';

//This updates our tree
function update(source) {

    // Compute the new tree layout.
    var nodes = tree.nodes(root).reverse(),
        links = tree.links(nodes);

    // Determine the width...
    nodes.forEach(function(d) { d.y = d.depth * 250; });

    // Update the nodes…
    var node = svg.selectAll("g.node")
        .data(nodes, function(d) { return d.id || (d.id = ++i); });

    // What follows is a delicate procedure of
    // Enter a node
    // Transition a node
    // Exit a node
    //
    // By this we can easily update the graph per separate group

    // Enter any new nodes at the parent's previous position.
    var nodeEnter = node.enter().append("g")
        .attr("class", "node")
        .attr("transform", function(d) { return "translate(" + source.y0 + "," + source.x0 + ")"; })
        .on("click", function(d){

            if (d3.event.ctrlKey) {
                celex_id = d.name;
                if (celex_id == last_clicked){
                    // This is a function defined in upload.html...
                    closeNav();
                    last_clicked = 0;
                } else {
                    last_clicked = celex_id;
                    // Make an AJAX call to the database...
                    call_database(d);
                    // This is a function defined in upload.html...
                    setTimeout(function(){openNav(celex_id + ':   ' + d.title); }, DELAY);
                }
            } else {
                click(d);
            }
        });

    // Here we add more nodes to the trees
    nodeEnter.append("rect")
        .attr("class", "rect-class")
        .attr("id", function(d) { return d.name})
        .attr("rx", 10)
        .attr("ry", 10)
        .style("fill", function(d) { return d._children ? color_rect_child  : color_rect; })
        .style("stroke-width", 3)
        .style("stroke", function(d) { return d._stroke_color_id  ? "red" : '#AFBDC4'; })
        .each(function(d){ call_title(d)})
        .on('mouseenter', function(){
            d3.select(this).style('stroke-width', 5);
            d3.select(this).style('fill', hover_color_rect)
        })
        .on('mouseleave', function(){
            d3.select(this).style('stroke-width', 3);
            d3.select(this).style("fill", function(d) { return d._children ? color_rect_child  : color_rect; })
        });

    // Add the text...
    nodeEnter.append("text")
        .attr("dx", ".75em")
        .attr("dy", "1.5em")
        .style("font-size", "16")
        .attr("text-anchor", "start")
        .text(function(d) { return d.name; })
        .style("fill-opacity", 1e-6);

    // Transition nodes to their new position.
    var nodeUpdate = node.transition()
        .duration(duration)
        .attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; });

    // Update accordingly
    nodeUpdate.select("rect")
        .attr("class", "rect-class")
        .style("fill", function(d) { return d._children ? color_rect_child  : color_rect; });

    // Update acoordingly
    nodeUpdate.select("text")
        .style("fill-opacity", 1);

    // Transition exiting nodes to the parent's new position.
    var nodeExit = node.exit().transition()
        .duration(duration)
        .attr("transform", function(d) { return "translate(" + source.y + "," + source.x + ")"; })
        .remove();

    nodeExit.select("rect")
        .attr("class", "rect-class")
        .style("stroke", '#AFBDC4');

    nodeExit.select("text")
        .style("fill-opacity", 1e-6);

    // Update the links… again with the standard Enter, Transition and Exit methods.

    var link = svg.selectAll("path.link")
        .data(links, function(d) { return d.target.id; });

    // Enter any new links at the parent's previous position.
    link.enter().insert("path", "g")
        .attr("class", "link")
        .attr("d", function(d) {
            var orig = {x: (source.x0), y: (source.y0)};
            return diagonal({source: orig, target: orig});
        });

    // Transition links to their new position.
    link.transition()
        .duration(duration)
        .attr("d", diagonal);

    // Transition exiting nodes to the parent's new position.
    link.exit().transition()
        .duration(duration)
        .attr("d", function(d) {
            var orig = {x: source.x, y: (source.y )};
            return diagonal({source: orig, target: orig});
        })
        .remove();

    // Stash the old positions for transition.
    nodes.forEach(function(d) {
        d.x0 = d.x;
        d.y0 = d.y;
    });
}

// This is what happens when we click on a node
function click(d) {

    if (!(d.children) && !(d._children)){
        // call_ref is a function in general_functions.js
        // It asks for the referenced documents and creates children data for this node d
        // When that is done, we can check IF the object d has any children.. and if it has, show them.
        call_ref(d);
    }
    // If the node d already has children (or hidden _children) then we can activate these by calling update()
    if (d.children) {
        d._children = d.children;
        d.children = null;
        update(d);
    } else {
        d.children = d._children;
        d._children = null;
        update(d);
    }
}


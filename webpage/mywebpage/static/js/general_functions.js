// This function file has a lot of cuntion calls back to the server side...
// This is mainly used to send AJAX request, parse responses and set certain attributes of data objects

// Global variable to keep track of the button last clicked.
var last_clicked = 0;

// Here we clean strings given by the RID data..
function clean_string(input_array){
    for(var i=0; i<input_array.length; i++){
        cut_off = input_array[i].search('\\\\')+1;
        input_array[i] = input_array[i].slice(cut_off).replace('\\',': ')
    }
    return input_array;
}

// Here we create buttons for the sidenav component
function create_link_button(input_array){
    str_link = '';
    for(var i=0; i<input_array.length; i++){
        temp_link = "<a class='btn-class-sidenav'>" + input_array[i] + "</a>";
        str_link = str_link + temp_link;
    }
    return str_link;
}

// Parse the response when we called for references
function parse_response_ref(input_dict, d_obj){
    // Here we parse the response that contains refernces to other documents
    // This function is called inside an AJAX request
    //

    var ref_reg = input_dict['Reference regulation'];
    var ref_dir = input_dict['Reference directive'];

    total_ref = [];
    total_ref.push.apply(total_ref, ref_reg);
    total_ref.push.apply(total_ref, ref_dir);

    if(total_ref.length){
        var temp_array = [];
        for(var i=0; i<ref_reg.length; i++){
            temp_array.push({'name': ref_reg[i]})
        }
        d_obj._stroke_color_id = undefined;
        d_obj._children = temp_array;
        // Need this to update color
        update(d_obj);
    } else{
        d_obj._stroke_color_id = 1;
        derp_id = "#" + d_obj.name;
        $(derp_id).css({"stroke":"red"});
    }
}

// Parse the response when we called for the page with annotated words
function parse_response_page(input_html){
    // Here we show the given html (with markedup langauge) ofc
    var w = window.open();
    $(w.document.body).html(input_html);
}

// Parse the response when we called for the sidenav information
function parse_response_sidenav(input_dict, d_obj){
    // Here we parse the response for the sidenav bar
    // This function is called inside an AJAX request.
    // Can be made even more modular if I can format/append the new html content correctly

    // Pretty ugly but reset the content in it..
    $("#Business").html('');
    $("#Functions").html('');

    $("#Keywords").html('');
    $("#NER").html('');
    $("#Trigram").html('');

    var input_bsns = input_dict['Impact on Business (1st LOD)'];
    var input_fnctns = input_dict['Impact on Functions (2nd LOD)'];
    var input_bsns = clean_string(input_bsns);
    var input_fnctns = clean_string(input_fnctns );

    var input_keyw = input_dict['Keywords'];
    var input_ner = input_dict['NER'];
    var input_trigram = input_dict['Trigram'];

    var celex_id = d_obj.name;

    // d_obj.title = title;
    business_buttons = create_link_button(input_bsns);
    functions_buttons = create_link_button(input_fnctns);

    keyword_buttons = create_link_button(input_keyw);
    ner_buttons = create_link_button(input_ner);
    trigram_buttons = create_link_button(input_trigram );

    $("#Business").html(business_buttons);
    $("#Functions").html(functions_buttons);

    $("#Keywords").append(keyword_buttons );
    $("#NER").append(ner_buttons);
    $("#Trigram").append(trigram_buttons);

    // Add on click functionality...
    $('a').on('click', function() {call_page(celex_id, d3.select(this).text())});

}

// AJAX call to get the page content
function call_page(celex_id, x_content){
    // AJAX call to get highlighted page
    $.ajax({
        url: '/getPage',
        data: {'celex_id': celex_id, 'content': x_content},
        type: 'GET',
        success: function(response) {
            parse_response_page(response)
        },
        error: function(error) {
            console.log('FOUT in getPage', error);
        }
    });
}

// AJAX call to get the reference content
function call_ref(d_obj) {
    // AJAX call to get reference documents in thre TREE setting
    x_id = d_obj.name;
    $.ajax({
        url: '/getRef',
        data: x_id,
        type: 'GET',
        success: function(response) {
            parse_response_ref(response, d_obj);
        },
        error: function(error) {
            console.log('FOUT in getRef', error);
        }
    });
}

// AJAX call to get the sidenav data
function call_database(d_obj){
    // AJAX call to get actual content
    //This is needed in order to refer back to the original
    x_id = d_obj.name;
    $.ajax({
        url: '/getData',
        data: x_id,
        type: 'GET',
        success: function(response) {
            parse_response_sidenav(response, d_obj);
        },
        error: function(error) {
            console.log('FOUT in getData', error);
        }
    });
}

// AJAX call to get the title of a document
function call_title(d_obj){
    // AJAX call to get actual content
    //This is needed in order to refer back to the original
    x_id = d_obj.name;
    $.ajax({
        url: '/getTitle',
        data: x_id,
        type: 'GET',
        success: function(response) {
            d_obj.title = response
        },
        error: function(error) {
            console.log('FOUT in getTitle', error);
        }
    });
}


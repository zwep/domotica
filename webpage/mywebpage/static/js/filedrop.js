// This file is here to allow the file-drop functionality
// However, it does not work as great in Chrome as it does in Firefox...
// So there is also a manual way of selecting files.
// It is possible btw to upload multiple files..


// This is check to see if we can perform advanced uploading, is a boolean variable
var isAdvancedUpload = function() {
    var div = document.createElement('div');
    if (window.File && window.FileReader && window.FileList && window.Blob){
        console.log('extra test...');
    }
    return (('draggable' in div) || ('ondragstart' in div && 'ondrop' in div)) && 'FormData' in window && 'FileReader' in window;

}();

// The naming convention of var means locally.
// The dollar-sign means that we are linking to an HTML tag.
var $form = $('.box');

// Here we create drag/drop reactions
if (isAdvancedUpload) {
    // Sign that we can use advanced uploading.
    var droppedFiles = false;
    $form.addClass('has-advanced-upload');

    // Signals that we are hovering over an element or not...
    // And dropping objects.
    $form.on('drag dragstart dragend dragover dragenter dragleave drop', function(e) {
        e.preventDefault();
        e.stopPropagation();
    })
    .on('dragover dragenter', function() {
        console.log('dragover/dragenter');
        $form.addClass('is-dragover');
    })
    .on('dragleave dragend drop', function() {
        console.log('dragleave/dragend/drop');
        $form.removeClass('is-dragover');
    })
    .on('drop', function(e) {
        console.log('drop');
        droppedFiles = e.originalEvent.dataTransfer.files;
    });
} else {
    console.log('WARNING: we have no Advanced Upload..')
}

// This is a small method to show the file names that are selected
// This is only visible if automatic submission is cancelled
var $input    = $form.find('input[type="file"]'),
    $label    = $form.find('label'),
    showFiles = function(files) {
        $label.text(files.length > 1 ? ($input.attr('data-multiple-caption') || '').replace( '{count}', files.length ) : files[ 0 ].name);
    };


// This fires when the files (hovering above) are dropped
// Since this posted some errors, I added some comments for the console log
$form.on('drop', function(e) {
    console.log('dropped a file');
    console.log(e.originalEvent.dataTransfer);
    e.preventDefault();
    console.log('This should contain the files...', e.originalEvent.dataTransfer.files);
    console.log('Drag n drop has been entered');
    droppedFiles = e.originalEvent.dataTransfer.files; // the files that were dropped
    showFiles(droppedFiles);
    $form.trigger('submit');
});

// This fires when a file has been submitted via the normal way..
$input.on('change', function(e) { // when drag & drop is NOT supported
    console.log('Submit form has been entered');
    //showFiles(e.target.files);
    droppedFiles = e.target.files;
    $form.trigger('submit');
});


var selectedProjectInstructions = {};
var currentRow = 0


$("#start-project").on('submit', (evt) => {
    evt.preventDefault();

    const formData = {
        patID: $("#pattern-id").val(),
        sWidth: $("#swatch-width").val(),
        sHeight: $("#swatch-height").val(),
        pWidth: $("#project-width").val(),
        pHeight: $("#project-height").val()
    }
    let url = `/api/instructions`

    $('#start-knitting').append('<button id="advance-row">Start</button>');
    $("#advance-row").on('click', (evt) => {
        
        while(currentRow < selectedProjectInstructions.totalrows){
            for(let i = 0; i < selectedProjectInstructions.knitInstructions.length; i++){
                $('#start-knitting').append(`<ul>Row ${currentRow + 1}</ul><ul>${selectedProjectInstructions.knitInstructions[i]}</ul>`)   
                currentRow++;
            }
        }
    })
    selectedProjectInstructions = {'totalrows': 12,
                                    'knitInstructions': ['line 1', 'line 2', 'line 3', 'line 4']}
    $.post(url, formData, (res) => {
        console.log(res)
        $('#stitchname').html(res['pattern_name']);
        $('#description').html(res['pattern_description']);
        $('#caston').html(res['cast_on']);
        $('#totalrows').html(res['row_total']);
        $('#knitpat').html(res['start']);
        //reassign value of empty object variable
    })
});
  


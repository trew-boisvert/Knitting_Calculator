
 function makePatternFromInput(evt){
    evt.preventDefault();
    console.log('formData:', formData);
    const formData = {
        patID: $("#pattern-id").val(),
        sWidth: $("#swatch-width").val(),
        sHeight: $("#swatch-height").val(),
        pWidth: $("#project-width").val(),
        pHeight: $("#project-height").val()
    }
    let url = `/api/instructions`;
//maybe change append to prepend
    $('#start-knitting').append('<button id="advance-row">Next Row</button>');
    console.log(sessionStorage.stitchInstructions);
    let stitch = sessionStorage.stitchInstructions.split(".,");
    $("#advance-row").on('click', (evt) => {
        console.log('current row', sessionStorage.currentRow);
        console.log('row total', sessionStorage.row_total);
        if(parseInt(sessionStorage.currentRow) === parseInt(sessionStorage.row_total)){
            $('#start-knitting').append(`<ul>That's all!  Cast off and you're done!</ul>`);
        }
        else{
            if(parseInt(sessionStorage.indexer) === stitch.length){
                sessionStorage.setItem('indexer', 0);
            }
            $('#start-knitting').append(`<ul>Row ${parseInt(sessionStorage.currentRow) + 1}</ul><ul>${stitch[parseInt(sessionStorage.indexer)]}</ul>`)
            sessionStorage.setItem('currentRow', parseInt(sessionStorage.currentRow) + 1);
            sessionStorage.setItem('indexer', parseInt(sessionStorage.indexer) + 1);
        }
    })

    $.post(url, formData, (res) => {
        console.log(res);
        $('#stitchname').html(res['pattern_name']);
        $('#description').html(res['pattern_description']);
        $('#caston').html(res['cast_on']);
        $('#totalrows').html(res['row_total']);
        $('#knitpat').html(res['start']);
        
        sessionStorage.setItem('row_total', res['row_total']);
        sessionStorage.setItem('stitchInstructions', res['stitch'])
        sessionStorage.setItem('currentRow', 0)
        sessionStorage.setItem('indexer', 0)
    })
}

$("#start-project").on('submit', makePatternFromInput)
  
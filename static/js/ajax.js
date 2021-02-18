
function MakePatternFromInput(evt){
    evt.preventDefault();

    const formData = {
        patID: $("#pattern-id").val(),
        sWidth: $("#swatch-width").val(),
        sHeight: $("#swatch-height").val(),
        pWidth: $("#project-width").val(),
        pHeight: $("#project-height").val()
    }
    let url = `/api/instructions`

    $.post(url, formData, (res) => {
        console.log(res)
        $('#stitchname').html(res['pattern_name']);
        $('#description').html(res['pattern_description']);
        $('#caston').html(res['cast_on']);
        $('#totalrows').html(res['row_total']);
        $('#knitpat').html(res['pattern_description']);
    })
}
// TODO change line 20 to display calculations  

$("#start-project").on('submit', MakePatternFromInput)

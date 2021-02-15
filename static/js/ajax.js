function MakePatternFromInput(evt){
    evt.preventDefault();

    let patID = $("#pattern-id").val();
    let sWidth = $("#swatch-width").val();
    let sHeight = $("#swatch-height").val();
    let pWidth = $("#project-width").val();
    let pHeight = $("#project-height").val();
    let url = `/api/instructions/${patID}`

    $.get(url, (res) => {
        console.log(res)
        $('#stitchname').html(res['pattern_name']);
        $('#description').html(res['pattern_description']);
        $('#caston').html(res['pattern_name']);
        $('#totalrows').html(res['pattern_name']);
        $('#knitpat').html(res['pattern_instructions']);
    })
}
// TODO change lines 15, 16, and 17 to display calculations  

$("#start-project").on('submit', MakePatternFromInput)
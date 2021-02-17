// const calculateWidth = (swatchWidth, projectWidth, repeatSize) => {
//     let stitches = 0
//     let width = 0
//     console.log(swatchWidth)
//     // while (width < projectWidth){
//     //     stitches += repeatSize;
//     //     width += swatchWidth;
//     // }
//     return "stitches";
// };

function MakePatternFromInput(evt){
    evt.preventDefault();

    // let patID = $("#pattern-id").val();
    // let sWidth = $("#swatch-width").val();
    // let sHeight = $("#swatch-height").val();
    // let pWidth = $("#project-width").val();
    // let pHeight = $("#project-height").val();
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
        $('#knitpat').html(res['pattern_instructions']);
    })
}
// TODO change lines 15, 16, and 17 to display calculations  

$("#start-project").on('submit', MakePatternFromInput)

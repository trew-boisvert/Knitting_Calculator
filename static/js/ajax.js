$("#start-project").on('submit', (evt) => {
    evt.preventDefault();
    
    const formData = {
        patID: $("#pattern-id").val(),
        sWidth: $("#swatch-width").val(),
        sHeight: $("#swatch-height").val(),
        pWidth: $("#project-width").val(),
        pHeight: $("#project-height").val(),
        pName: $("#project-name").val()
    }
    console.log('formData:', formData);
    let url = `/api/instructions`;

    $('#start-knitting').append('<button id="advance-row">Next Row</button>');
    $('#start-knitting').append('<button id="save-pattern">Save Project</button>');

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

    $("#advance-row").on('click', (evt) => {

        let stitch = sessionStorage.getItem('stitchInstructions').split(".,");
        console.log(sessionStorage.getItem('stitchInstructions'));

        console.log('current row', sessionStorage.currentRow);
        console.log('row total', sessionStorage.row_total);
        //maybe change append to prepend?
        if(parseInt(sessionStorage.currentRow) === parseInt(sessionStorage.row_total)){
            $('#start-knitting').append(`<ul>That's all!  Cast off and you're done!</ul>`);
        }
        else{
//bind numbers to variable and use that instead of parseing all the time
            if(parseInt(sessionStorage.indexer) === stitch.length){
                sessionStorage.setItem('indexer', 0);
            }
            $('#start-knitting').append(`<ul>Row ${parseInt(sessionStorage.currentRow) + 1}</ul><ul>${stitch[parseInt(sessionStorage.indexer)]}</ul>`)
            sessionStorage.setItem('currentRow', parseInt(sessionStorage.currentRow) + 1);
            sessionStorage.setItem('indexer', parseInt(sessionStorage.indexer) + 1);
        }
    })

    $("#save-pattern").on('click', (evt) => {
        const currentProgress = {
            currentRow: sessionStorage.getItem('currentRow'), 
            currentIndex: sessionStorage.getItem('indexer')
        }
        $.post('/save_pattern', currentProgress, (res) => {
            console.log(res);
            $('#save-status').html(res['message']);
        })
    })
});

$("#display-project-list").on('click', (evt) => {
    $.post('/api/projects', (res) => {
        console.log(res);
        for(const key in res){
            $('#current-projects').append(`<li><a href="/projectcontinue/${key}">${res[key]}</a><a href="/delete/${key}">Delete Project</a></li>`)
        }
    })
})

$("#resume-knitting").on('click', (evt) => {
    evt.preventDefault();

    $('#keep-knitting').append('<button id="previous-row">Previous Row</button>');
    $('#keep-knitting').append('<button id="next-row">Next Row</button>');

    $.post('/api/projectcontinue', (res) => {
        console.log(res);

        sessionStorage.setItem('row_total', res['row_total']);
        sessionStorage.setItem('stitchInstructions', res['stitch']);
        sessionStorage.setItem('currentRow', res['currentRow']);
        sessionStorage.setItem('indexer', res['currentIndex']);
        sessionStorage.setItem('cast_on', res['cast_on']);
        let stitch = sessionStorage.getItem('stitchInstructions');
        stitch = stitch.split(".,");

        $('#keep-knitting').append(`<p>This project is ${sessionStorage.getItem('cast_on')} stitches wide and will have ${sessionStorage.getItem('row_total')} rows.</p>`)
        $('#keep-knitting-stitch').html(`<p>Row ${parseInt(sessionStorage.currentRow) + 1}:</p><p>${stitch[parseInt(sessionStorage.indexer)]}</p>`)
        console.log('Indexer', sessionStorage.indexer)

        $("#next-row").on('click', (evt) => {
            evt.preventDefault();
            if(sessionStorage.currentRow === sessionStorage.row_total){
                $('#keep-knitting-stitch').html(`<ul>That's all!  Cast off and you're done!</ul>`);
            } 
            else {
                sessionStorage.setItem('currentRow', parseInt(sessionStorage.currentRow) + 1);
                sessionStorage.setItem('indexer', parseInt(sessionStorage.indexer) + 1);

                if(parseInt(sessionStorage.indexer) === stitch.length){
                    sessionStorage.setItem('indexer', 0);
                    sessionStorage.getItem('indexer');
                }

                $('#keep-knitting-stitch').html(`<ul>Row ${parseInt(sessionStorage.currentRow) + 1}:</ul><ul>${stitch[parseInt(sessionStorage.indexer)]}</ul>`)

                const updatedNumbers = {
                    currentRow: sessionStorage.getItem('currentRow'),
                    currentIndex: sessionStorage.getItem('indexer')
                }

                $.post('/api/savecontinue', updatedNumbers, (res) => {
                    console.log(res);
                })
            }
        })
        $("#previous-row").on('click', (evt) => {
            evt.preventDefault();
            if(sessionStorage.currentRow === '0'){
                $('#keep-knitting-stitch').html(`<ul>Cast on ${sessionStorage.cast_on} stitches.</ul>`);
            }
            else {
                sessionStorage.setItem('currentRow', parseInt(sessionStorage.currentRow) - 1);
                sessionStorage.setItem('indexer', parseInt(sessionStorage.indexer) - 1);

                if(parseInt(sessionStorage.indexer) === -1){
                    sessionStorage.setItem('indexer', (stitch.length - 1));
                    sessionStorage.getItem('indexer');
                }

                $('#keep-knitting-stitch').html(`<ul>Row ${parseInt(sessionStorage.currentRow) + 1}:</ul><ul>${stitch[parseInt(sessionStorage.indexer)]}</ul>`)

                const updatedNumbers = {
                    currentRow: sessionStorage.getItem('currentRow'),
                    currentIndex: sessionStorage.getItem('indexer')
                }
                
                $.post('/api/savecontinue', updatedNumbers, (res) => {
                    console.log(res);
                })                
            }
        })
    })
})

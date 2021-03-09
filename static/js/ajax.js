"use strict";

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
    
    let url = `/api/instructions`;

    $.post(url, formData, (res) => {
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

    $('#start-knitting').append('<button id="advance-row">Next Row</button>');
    $('#start-knitting').append('<button id="save-pattern">Save Project</button>');

    $("#advance-row").on('click', (evt) => {
        
        let stitch = sessionStorage.getItem('stitchInstructions').split(".,");
//maybe change append to prepend?
        if(parseInt(sessionStorage.currentRow) === parseInt(sessionStorage.row_total)){
            $('#start-knitting').append(`<ul>That's all!  Cast off and you're done!</ul>`);
        }
        else{
//TODO bind numbers to variable and use that instead of parseing all the time
            if(parseInt(sessionStorage.indexer) === stitch.length){
                sessionStorage.setItem('indexer', 0);
            }
            $('#start-knitting').append(`<ul>Row ${parseInt(sessionStorage.currentRow) + 1}</ul><ul>${stitch[parseInt(sessionStorage.indexer)]}</ul>`)
            sessionStorage.setItem('currentRow', parseInt(sessionStorage.currentRow) + 1);
            sessionStorage.setItem('indexer', parseInt(sessionStorage.indexer) + 1);
        }
    })

    $("#save-pattern").on('click', (evt) => {
        $('#save-pattern').hide();
        $('#advance-row').hide();
    
        const currentProgress = {
            currentRow: sessionStorage.getItem('currentRow'), 
            currentIndex: sessionStorage.getItem('indexer')
        }
        $.post('/save_pattern', currentProgress, (res) => {
            $('#save-status').html(res['message']);
        })
    })
});

$("#logout").on('click', (evt) => {
    $('#logout').hide();
    $('#delete-account').hide();
    $.post('handle-logout', (res) => {
        $('#logout-text').html(res['message'])
    })
})

$("#display-project-list").on('click', (evt) => {
    $('#display-project-list').hide();
    $.post('/api/projects', (res) => {
        for(const key in res){
            $('#current-projects').append(`<li><a href="/projectcontinue/${key}">${res[key]}</a><a href="/delete/${key}">Delete Project</a></li>`)
        }
    })
})

//this deletes projects.  not to be confused with deleting a user profile.
$("#goodbye-forever").on('click', (evt) => {
    $.post('/api/delete', (res) => {
        $('#goodbye-forever').hide();
        $('#say-goodbye').append(`<p>${res['message']}</p>`);
        $('#say-goodbye').append(`<a href="http://0.0.0.0:5000/profile">Return to Profile</a>`);
    })
})

//this deletes a user profile, and their attendant projects.
$("#delete-account").on('click', (evt) => {
    $.post('/api/accountdelete', (res) => {
        $('#delete-account').hide();
        $('#logout').hide();
        $('#delete-account-text').append(`<p>${res['message']}</p>`);
    })
})

$("#resume-knitting").on('click', (evt) => {
    evt.preventDefault();

    $('#resume-knitting').hide();

    $.post('/api/projectcontinue', (res) => {
        sessionStorage.setItem('row_total', res['row_total']);
        sessionStorage.setItem('stitchInstructions', res['stitch']);
        sessionStorage.setItem('currentRow', res['currentRow']);
        sessionStorage.setItem('indexer', res['currentIndex']);
        sessionStorage.setItem('cast_on', res['cast_on']);
        let stitch = sessionStorage.getItem('stitchInstructions');
        stitch = stitch.split(".,");

        $('#keep-knitting').append(`<p>This project is ${sessionStorage.getItem('cast_on')} stitches wide and will have ${sessionStorage.getItem('row_total')} rows.</p>`);
        $('#keep-knitting-stitch').html(`<p>Row ${parseInt(sessionStorage.currentRow) + 1}:</p><p>${stitch[parseInt(sessionStorage.indexer)]}</p>`);
        $('#keep-knitting').append('<button id="previous-row">Previous Row</button>');
        $('#keep-knitting').append('<button id="next-row">Next Row</button>');

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
});

$("#new-stitch-row").on('click', (evt) => {
    evt.preventDefault();
    $('#stitch-instructions-array').append('<input type="text" name="stitch-instructions-list">');
});

async function imageUpload(files) {
    const url = "https://api.cloudinary.com/v1_1/knittr/image/upload";
    const uploadData = new FormData(); 

    let file = files[0];
    uploadData.append("file", file);
    uploadData.append("upload_preset", "r8rsqkah");

    let response = await fetch(url, {
        method: "POST",
        body: uploadData
    });

    let json = await response.json();

    return json.url
}

$('#upload-photos').on('submit', (evt) => {
    evt.preventDefault();

    const media_files = $('#photo_upload').prop('files');
    const cloud_url = imageUpload(media_files);

    cloud_url.then((res_url) => {
        
        const photo_post_data = {
            'post_title': $('#post-title').val(),
            'post_comment': $('#post-comment').val(),
            'img_url': res_url
        }
        console.log(photo_post_data)
        $.post('/api/photos', photo_post_data, (res) => {
            if (res.status === 'ok') {
                $('#photo_upload_success').html(`Your post has been added to the database.`)
            } 
        });  
    });
});
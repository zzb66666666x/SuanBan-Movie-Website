$(document).ready(function () {
    // example: https://getbootstrap.com/docs/4.2/components/modal/
    // show modal
    // the show.bs.modal event in Bootstrap fires when the modal is about to be displayed
    // this modal is called when you want to search, edit table or add entry
    // so use different taskID to differentiate between them
    $('#task-modal').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget) // Button that triggered the modal
        const taskID = button.data('source') // Extract info from data-* attributes
        const content = button.data('content') // Extract info from data-* attributes
        // alert(button.data("bs-toggle"))
        const modal = $(this) // get this modal that triggers the event 
        // selector: . and #
        // .class	$(".intro")	    All elements with class="intro"
        // #id	$("#lastname")	    The element with id="lastname"
        if (taskID === 'New Task') {
            modal.find('.modal-title').text(taskID)
            modal.find('.input-group-text').text('New Task')
            // use xxx.attr("somename", value) to set attribute for future use
            $('#task-form-display').attr('taskID', taskID)
        } 
        else if (taskID === 'Search Task'){
            modal.find('.modal-title').text(taskID)
            modal.find('.input-group-text').text('Search Condition')
            $('#task-form-display').attr('taskID', taskID)
        }
        else {
            modal.find('.modal-title').text('Edit Task ' + taskID)
            modal.find('.input-group-text').text('Task ' + taskID)
            $('#task-form-display').attr('taskID', taskID)
        }

        if (content) {
            modal.find('.form-control').val(content);
        } else {
            modal.find('.form-control').val('');
        }
    })


    $('#submit-task').click(function () {
        // read out attribute by name, which was set when you toggle to modal
        const tID = $('#task-form-display').attr('taskID');
        console.log($('#task-modal').find('.form-control').val())
        var myurl = ''
        if (tID === 'Search Task'){
            myurl = '/search'
        }
        else if (tID === 'New Task'){
            myurl = '/create'
        }
        else{
            myurl = '/edit/' + tID
        }
        // if (tID === 'Search Task'){
        //     $.ajax({
        //         type: 'GET',
        //         url: myurl,
        //         contentType: 'application/json;charset=UTF-8',
        //         data: JSON.stringify({
        //             'description': $('#task-modal').find('.form-control').val()
        //         }),
        //         success: function (res) {
        //             console.log(res.response)
        //             location.reload();
        //         },
        //         error: function () {
        //             console.log('Error');
        //         }
        //     });
        // }

        if (tID !== 'Search Task') {
        $.ajax({
            type: 'POST',
            url: myurl,
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'description': $('#task-modal').find('.form-control').val()
            }),
            success: function (res) {
                console.log(res.response)
                // if (tID === 'Search Task'){
                //     document.getElementById("index_table").innerHTML = "<tr><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td><td>7</td><td>8</td><td>9</td></tr>"
                // } 
                location.reload()
                
            },
            error: function () {
                console.log('Error');
            }
        })}
        else
        {
            // get the value typed in by user in html <input> element by jQuery function .val()
            window.location.href = "/search/" +  $('#task-modal').find('.form-control').val()
        };
        
    });

    $('.remove').click(function () {
        const remove = $(this)
        $.ajax({
            type: 'POST',
            url: '/delete/' + remove.data('source'),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

});
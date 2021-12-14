$(document).ready(function () {
    $('#search-video').click(function () {
        var name = $('#search-video-name').find('.form-control').val()
        if (name == '')
        {
            name = '%'
        }
        var limit = $('#search-video-limit').find('.form-control').val()
        if (limit == '') {
            limit = '10'
        }
        window.location.href = '/video/search/' + name + '/' + limit + ".html"
        // $.ajax({
        //     type: 'GET',
        //     url:'/video/search/' + name + '/' + limit,
        //     success: function (res) {
        //         document.getElementById("table_content").innerHTML = res
        //         //document.getElementById("table_content").innerHTML = "<tr><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td><td>7</td><td>8</td><td>9</td></tr>"
        //         //location.reload();
        //     },
        //     error: function () {
        //         console.log('Error');
        //     }
        // });
    });
});
$(document).ready(function () {
    $('#search-content').click(function () {
        var mv_name = $('#movie-name').find('.form-control').val()
        var act_name = $('#actor-actress-name').find('.form-control').val()

        $.ajax({
            type: 'POST',
            url:'/homesearch',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'user': mv_name,
                'password':act_name
            }),
            success: function (res) {
                console.log("success")
            },
            error: function () {
                console.log('Error')
            }
        });
    });
});

$(window).on('load', function(){
    cookiedata = document.cookie
    // alert(cookiedata)
    if (cookiedata != ""){
        elements = cookiedata.split(";")
        username_cookie = elements[0]
        user = username_cookie.split("=")[1]
        // alert(user)
        document.getElementById("logout").innerHTML = (user + ": Logout")
    }
});
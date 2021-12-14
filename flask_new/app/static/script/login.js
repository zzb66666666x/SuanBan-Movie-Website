$(document).ready(function () {
    $('#login-user').click(function () {
        var user = $('#personal-info').find('.form-control').val()
        var password = $('#user-password').find('.form-control').val()
        console.log(user)
        console.log(password)
        $.ajax({
            type: 'POST',
            url:'/loginvalidation',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'user': user,
                'password':password
            }),
            success: function (res) {
                console.log(res.response)
                // alert(res.response)
                if (res.success){
                    nameofuser = res.UserName
                    idofuser = res.UserId
                    // alert(idofuser)
                    document.cookie = "username=" + nameofuser + "; path=/"
                    document.cookie = "userid=" + idofuser + "; path=/"
                    // alert(document.cookie)
                    window.location.href = "/"
                }else{
                    location.reload()
                }
            },
            error: function () {
                console.log('Error')
            }
        });
    });
});
 function showRegisterForm() {
       ShowHideForm("registerForm","Show");
       ShowHideForm("loginForm","");
       ShowHideForm("forgottenPasswordForm","");
}


function ShowHideForm(FormID,ShoworHide) {
    var Form = document.getElementById(FormID);
    if(ShoworHide == "Show") {
        Form.style.display = 'block';
    }else {
        Form.style.display = 'none';
    }
}

function ShowforgottenPasswordForm() {
    ShowHideForm("registerForm","");
    ShowHideForm("loginForm","");
    ShowHideForm("forgottenPasswordForm","Show");
}
function ShowLoginForm() {
    ShowHideForm("registerForm","");
    ShowHideForm("loginForm","Show");
    ShowHideForm("forgottenPasswordForm","");
}




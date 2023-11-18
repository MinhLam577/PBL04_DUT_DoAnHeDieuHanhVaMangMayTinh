const LoginForm = document.getElementById("LoginForm");
LoginForm.addEventListener("submit", function(event){
    event.preventDefault();
    const formdata = new FormData(LoginForm);
    const data = Object.fromEntries(formdata);
    fetch('/CheckLogin/', {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data),
    })
    .then(Response => Response.json())
    .then(data => {
        Message = document.getElementById("Message");
        if(Message != null){
            Message.remove();
        }
        Message = document.createElement("label");
        Message.setAttribute("id", "Message");
        Message.setAttribute("style", "color: red;");
        if(!data["message"])
            window.location.href = "/Login/" + String(data)
        else{
            Message.innerHTML = data["message"];
        }
        NhapPassword = document.getElementById("NhapPassword");
        NhapPassword.appendChild(Message);
        SetTimeout(function() {
            Message.remove();
        }, 7000);
    })
    .catch(error => console.log(error));
});

const SignUpForm = document.getElementById("SignUpForm");
SignUpForm.addEventListener("submit", function(event){
    event.preventDefault();
    const formdata = new FormData(SignUpForm);
    const data = Object.fromEntries(formdata);
    fetch('/Register/', {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data),
    })
    .then(Response => Response.json())
    .then(data => {
        Message = document.getElementById("Message");
        if(Message != null){
            Message.remove();
        }
        Message = document.createElement("label");
        Message.setAttribute("id", "Message");
        Message.setAttribute("style", "color: red;");
        if(!data["message"])
            Message.innerHTML = "Đăng ký thành công";
        else{
            Message.innerHTML = data["message"];
        }
        NhapLaiPassword = document.getElementById("NhapLaiPassword");
        NhapLaiPassword.appendChild(Message);
        setTimeout(function() {
            Message.remove();
        }, 7000);
    })
    .catch(error => console.log(error));
});

const ForgotPassword = document.getElementById("ForgotPassword");
ForgotPassword.addEventListener("submit", function(event){
    event.preventDefault();
    const formdata = new FormData(ForgotPassword);
    const data = Object.fromEntries(formdata);
    fetch('/ForgotPassword/', {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body:JSON.stringify(data["Gmail"]),
    }).then(Response => Response.json())
    .then(data => {
        Message = document.getElementById("Message");
        if(Message != null){
            Message.remove();
        }
        sendMailDiv = document.getElementById("SendGmailDiv"); 
        Message = document.createElement("label");
        Message.setAttribute("id", "Message");
        Message.setAttribute("style", "color: red;");
        Message.innerHTML = data["message"];
        sendMailDiv.appendChild(Message);
        setTimeout(function() {
            Message.remove();
        }, 7000);
    })
    .catch(error => console.log(error));
});

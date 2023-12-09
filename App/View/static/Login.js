        
const LoginForm = document.getElementById("LoginForm");
LoginForm.addEventListener("submit", function(event){
    event.preventDefault();
    const formdata = new FormData(LoginForm);
    const data = Object.fromEntries(formdata);
    fetch('/CheckLoginJWT/', {
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
        Message.innerHTML = "";
        Message.setAttribute("id", "Message");
        Message.setAttribute("style", "color: red;");
        Token = JSON.stringify(data);
        if(!data["message"]){
            const form_data = new FormData();
            form_data.append("authorization", "Bearer " + Token);
            fetch("/CheckLoginSuccess/", {
                method: "POST",
                body: form_data
            }).then(Response => Response.json())
            .then(data => {
                const userType = data["userType"];
                const Gmail = data["userID"];
                const existingToken = window.sessionStorage.getItem(Gmail);
                if(!existingToken)
                     window.sessionStorage.setItem(Gmail, Token);
                const formdata = new FormData();
                formdata.append("userType", userType);
                formdata.append("token", Token);
                window.location.href = "/LoginSuccess/" + Token;
            });
        }
        else {
            Message.innerHTML = data["message"];
        }
        NhapPassword = document.getElementById("NhapPassword");
        if(Message.innerHTML !== "")
            NhapPassword.appendChild(Message);
            setTimeout(function() { 
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
ForgotPassword.addEventListener("submit", function(event) {
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

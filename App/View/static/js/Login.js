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
        isLogin = false
        Token = JSON.stringify(data);
        if(!data["message"]){
            const form_data = new FormData();
            form_data.append("authorization", "Bearer " + Token);
            fetch("/CheckLoginSuccess/", {
                method: "POST",
                body: form_data
            })
            .then(Response => Response.json())
            .then(data => {
                const Gmail = data["userID"];
                const data_form = new FormData();
                data_form.append("token", Token);
                const existingToken = window.localStorage.getItem(Gmail);
                if(!existingToken){
                    window.localStorage.setItem(Gmail, Token);
                    
                }
                window.sessionStorage.setItem(Gmail, Token);
                const form_submit = document.createElement("form");
                form_submit.setAttribute("method", "POST");
                form_submit.setAttribute("action", "/");
                const input_token = document.createElement("input");
                input_token.setAttribute("type", "hidden");
                input_token.setAttribute("name", "token");
                input_token.setAttribute("value", Token);
                form_submit.appendChild(input_token);
                document.body.appendChild(form_submit);
                form_submit.submit();
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

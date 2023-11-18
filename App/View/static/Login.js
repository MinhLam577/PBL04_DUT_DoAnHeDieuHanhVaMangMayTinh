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
    .then(data =>{
        fetch('/Login/' + String(data), {
            method: "GET",
        }).then(    
            window.location.href = "/Login/" + String(data)
        )
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
    }).then(Response => Response.json())
    .then(alert("Đăng kí thành công"))
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

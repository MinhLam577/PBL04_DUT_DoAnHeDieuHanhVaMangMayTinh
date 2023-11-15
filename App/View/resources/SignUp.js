const SignUpForm = document.getElementById("SignUpForm");
SignUpForm.addEventListener("submit", function(event){
    event.preventDefault();
    const formdata = new FormData(SignUpForm);
    const data = Object.fromEntries(formdata);
    fetch('http://localhost:8000/Register/', {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data),
    }).then(Response => Response.json())
    .then(data => console.log(data))
    .catch(error => console.log(error));
});
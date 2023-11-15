// const ForgotPassword = document.getElementById("ForgotPassword");
// ForgotPassword.addEventListener("submit", function(event){
//     event.preventDefault();
//     const formdata = new FormData(ForgotPassword);
//     const data = Object.fromEntries(formdata);
//     fetch('http://localhost:8000/ForgotPassword/', {
//         method: "POST",
//         headers: {
//             "Content-Type": "application/json"
//         },
//         body: JSON.stringify(data),
//     }).then(Response => Response.json())
//     .then(data => console.log(data))
//     .catch(error => console.log(error));
// });
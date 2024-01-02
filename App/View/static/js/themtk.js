document.querySelector("#add_new").addEventListener("click", function() {
    document.querySelector(".modal").style.display = "flex";
});
document.querySelector(".popup .close-btn").addEventListener("click", function() {
    document.querySelector(".modal").style.display = "none";
});


document.querySelector(".modal2 .close-btn").addEventListener("click", function() {
    document.querySelector(".modal2").style.display = "none";
    document.getElementById("email1").value = "";
    document.getElementById("password1").value = "";
});
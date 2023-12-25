document.querySelector("#add_new").addEventListener("click", function() {
    console.log("Button clicked");
    document.querySelector(".modal").style.display = "flex";
});
document.querySelector(".popup .close-btn").addEventListener("click", function() {
    document.querySelector(".modal").style.display = "none";
});
document.querySelector("#update").addEventListener("click", function() {
    console.log("Button clicked");
    document.querySelector(".modal2").style.display = "flex";
});
document.querySelector(".modal2 .close-btn").addEventListener("click", function() {
    document.querySelector(".modal2").style.display = "none";
});
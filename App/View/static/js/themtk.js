document.querySelector("#add_new").addEventListener("click", function() {
    document.querySelector(".modal").style.display = "flex";
});
document.querySelector(".popup .close-btn").addEventListener("click", function() {
    document.querySelector(".modal").style.display = "none";
});
document.querySelectorAll(".update").forEach(function(element) {
    element.addEventListener("click", function() {
        document.querySelector(".modal2").style.display = "flex";
        var elemet_id = element.getAttribute("id").split("_")[1];
        fetch("/Users/"+elemet_id
        ).then(Response => Response.json())
        .then(data => {
            document.getElementById("email1").value = data.Gmail;
            document.getElementById("password1").value = data.Password;
            document.getElementById("IDUser").value = data.IDUser;
        })
    });
});
document.querySelector(".modal2 .close-btn").addEventListener("click", function() {
    document.querySelector(".modal2").style.display = "none";
    document.getElementById("email1").value = "";
    document.getElementById("password1").value = "";
});
document.getElementById("logout").addEventListener("click", (event) => {
    event.preventDefault();

    // AJAX
    const xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function() {
        if(xhttp.readyState == 4 && xhttp.status == 200) {
            window.location.href = "/";
        }
    }

    xhttp.open("POST", "/logout");
    xhttp.send();
});
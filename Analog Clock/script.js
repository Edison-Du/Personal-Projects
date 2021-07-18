function init() {
    // Adding numbers to clock
    for (let i = 1; i <= 12; i++) {
        let number, reverseRotation;

        number = document.createElement("div");
        number.setAttribute("class","num");
        number.style.transform = `rotate(${i*30}deg)`;

        reverseRotation = document.createElement("div");
        reverseRotation.style.transform = `rotate(${-i*30}deg)`;
        reverseRotation.innerHTML = i;

        number.appendChild(reverseRotation);
        document.getElementById("numbers").appendChild(number);
    }
    // Adding markers to the clock
    for (let i = 1; i <= 60; i++) {
        let marker, markerLine;

        marker = document.createElement("div");
        marker.setAttribute("class", "marker");
        marker.style.transform = `rotate(${i*6}deg)`;

        markerLine = document.createElement("div");
        markerLine.setAttribute("class", "marker-line");

        marker.appendChild(markerLine);
        document.getElementById("numbers").appendChild(marker);
    }
}

init();

// Moving the hands
setInterval(moveHands, 1000);
function moveHands() {
    let time = new Date();
    let hr = document.getElementById("hr");
    let min = document.getElementById("min");
    let sec = document.getElementById("sec");
    let totalSecondsDay = time.getHours()*3600 + time.getMinutes()*60 + time.getSeconds();
    let totalSecondsHour = time.getMinutes()*60 + time.getSeconds();
    hr.style.transform = `translate(-50%) rotate(${totalSecondsDay/43200*360}deg)`;
    min.style.transform = `translate(-50%) rotate(${totalSecondsHour/10}deg)`;
    sec.style.transform = `translate(-50%) rotate(${time.getSeconds()*6}deg)`;
}
moveHands();
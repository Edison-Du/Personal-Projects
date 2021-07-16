// Adding numbers to clock
var numClass = document.getElementsByClassName("numbers");
for (var i = 1; i <= 12; i++) {
    numClass.item(0).innerHTML += "<div class=\"num\" id=\"num-"+i+"\"><div id=\"rev-"+i+"\">"+i+"</div></div>";
}
for (var i = 1; i <= 12; i++) {
    var currentNum = document.getElementById("num-"+i);
    var currentNumReversed = document.getElementById("rev-"+i);
    currentNum.style.transform = "rotate(" + i*30 + "deg)";
    currentNumReversed.style.transform = "rotate(" + -i*30 + "deg)";
}

// Adding markers to the clock
for (var i = 1; i <= 60; i++) {
    numClass.item(0).innerHTML += "<div class=\"marker\" id=\"marker-"+i+"\"><div class=\"marker-line\"></div></div>";
}
for (var i = 1; i <= 60; i++) {
    var currentMarker = document.getElementById("marker-"+i);
    currentMarker.style.transform = "rotate(" + i*6 + "deg)";
}

// Moving the hands
setInterval(moveHands, 1000);
function moveHands() {
    var time = new Date();
    var hr = document.getElementById("hr");
    var min = document.getElementById("min");
    var sec = document.getElementById("sec");
    var totalSecondsDay = time.getHours()*3600 + time.getMinutes()*60 + time.getSeconds();
    var totalSecondsHour = time.getMinutes()*60 + time.getSeconds();
    // Make sure it fits in 12 hours, not 24
    if (totalSecondsDay >= 43200) totalSecondsDay -= 43200;
    hr.style.transform = "translate(-50%) rotate(" + totalSecondsDay/43200*360 + "deg)";
    min.style.transform = "translate(-50%) rotate(" + totalSecondsHour/10 + "deg)";
    sec.style.transform = "translate(-50%) rotate(" + time.getSeconds() * 6 + "deg)";
}
moveHands();
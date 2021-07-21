let playerWins, cpuWins;
let inPlay;

function init() {
    let cpuRow = document.getElementById("cpu-row");
    let playerRow = document.getElementById("player-row");
    
    playerWins = 0, cpuWins = 0;
    inPlay = false;

    for (let i = 0; i < 3; i++) {
        let img = document.createElement("img");
        let div = document.createElement("div");
        let td = document.createElement("td");

        div.setAttribute("class", "img-container");

        img.setAttribute("class", "image");
        img.setAttribute("id", `cpu-${i}`);
        img.setAttribute("src", `images/img-${i}.png`);
        img.setAttribute("alt", ["rock","paper","scissors"][i]);

        div.appendChild(img);
        td.appendChild(div);
        cpuRow.appendChild(td);
    }

    for (let i = 0; i < 3; i++) {
        let img = document.createElement("img");
        let div = document.createElement("div");
        let td = document.createElement("td");

        div.setAttribute("class", "img-container");

        img.setAttribute("class", "image");
        img.setAttribute("id", `player-${i}`);
        img.setAttribute("src", `images/img-${i}.png`);
        img.setAttribute("alt", ["rock","paper","scissors"][i]);
        
        img.onclick = () => onPlay(i);
        img.onmouseenter = () => onMouseEnterImage(img);
        img.onmouseleave = () => onMouseLeaveImage(img);

        div.appendChild(img);
        td.appendChild(div);
        playerRow.appendChild(td);
    }

    updateScore();
}

function onPlay(playerChoice) {
    if (!inPlay) {
        let cpuChoice = Math.floor(Math.random() * 3);
        let playerImage = document.getElementById(`player-${playerChoice}`);
        let cpuImage = document.getElementById(`cpu-${cpuChoice}`)

        inPlay = true;

        if ((cpuChoice + 1) % 3 == playerChoice) playerWins++;
        else if (playerChoice != cpuChoice) cpuWins++;

        enlargeImage(playerImage);
        setTimeout(() => enlargeImage(cpuImage), 100);
        setTimeout(() => shrinkImage(cpuImage), 1500);
        setTimeout(() => shrinkImage(playerImage), 1500);
        setTimeout(() => updateScore(), 1500);
        setTimeout(() => {inPlay = false}, 2000);
    }
}

function onMouseEnterImage(img) {
    if (!inPlay) enlargeImage(img);
}

function onMouseLeaveImage(img) {
    if (!inPlay) shrinkImage(img);
}

function enlargeImage(img) {
    img.style.width = "90%";
    img.style.height = "90%";
    img.style.filter = "opacity(100%)";
}

function shrinkImage(img) {
    img.style.width = "";
    img.style.height = "";
    img.style.filter = "";
}

function updateScore() {
    let cpuScore = document.getElementById("cpu-score");
    let playerScore = document.getElementById("player-score");
    cpuScore.innerText = `CPU : ${cpuWins}`;
    playerScore.innerText = `YOU : ${playerWins}`;
}

init();
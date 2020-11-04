// Much obliged for Jamie Uttariello JS stopwatch script in https://medium.com/@olinations/an-accurate-vanilla-js-stopwatch-script-56ceb5c6f45b

var timerDisplay = document.getElementById('study_timer');
var startTime;
var updateTime;
var difference;
var tInterval;
var savedTime;
var paused = 0;
var running = 0;
var toggle = false;


function startTimer() {
    if (!running) {
        startTime = new Date().getTime();
        tInterval = setInterval(getShowTime, 1000);
        paused = 0;
        running = 1;
    }
}

function pauseTimer() {
    if (!difference) {

    } else if (!paused) {
        clearInterval(tInterval);
        savedTime = difference;
        paused = 1;
        running = 0;
    } else {
        startTimer();
    }
}

function resetTimer() {
    clearInterval(tInterval);
    savedTime = 0;
    difference = 0;
    paused = 0;
    running = 0;
    timerDisplay.innerHTML = '00:00:00'
}

function getShowTime() {
    updateTime = new Date().getTime();
    if (savedTime) {
        difference = (updateTime - startTime) + savedTime;
    } else {
        difference = updateTime - startTime;
    }
    var hours = Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    var minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((difference % (1000 * 60)) / 1000);
    hours = (hours < 10) ? "0" + hours : hours;
    minutes = (minutes < 10) ? "0" + minutes : minutes;
    seconds = (seconds < 10) ? "0" + seconds : seconds;
    timerDisplay.innerHTML = hours + ':' + minutes + ':' + seconds;
    if (hours == 23 & minutes == 59 & seconds == 59) {
        resetTimer();
    }
}

function videoToggle() {
    var video = document.getElementById('embed_video');
    if (toggle == false) {
        video.style.width = "560px";
        video.style.height = "315px";
        toggle = true;
    } else {
        video.style.width = "0";
        video.style.height = "0";
        toggle = false;
    }
}
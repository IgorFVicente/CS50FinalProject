var timerDisplay = document.querySelector("#study_timer");
var startTime;
var updateTime;
var difference;
var tInterval;
var savedTime;
var paused = 0;
var running = 0;

function startTimer() {
    if (!running) {
        startTime = new Date().getTime();
        tInterval = setInterval(getShowTime, 1);
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
    updateTime = new Date().getTime();
    if (savedTime) {
        difference = (updateTime - startTime) + savedTime;
    } else {
        difference = updateTime - startTime;
    }
    var days = Math.floor(difference / (1000 * 60 * 60 * 24));
    var hours = Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    var minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((difference % (1000 * 60)) / 1000);
    var milliseconds = Math.floor((difference % (1000 * 60)) / 100);
    hours = (hours < 10) ? "0" + hours : hours;
    minutes = (minutes < 10) ? "0" + minutes:minutes;
}
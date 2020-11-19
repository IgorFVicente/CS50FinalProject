// Much obliged for Jamie Uttariello JS stopwatch script in https://medium.com/@olinations/an-accurate-vanilla-js-stopwatch-script-56ceb5c6f45b

var timerDisplay = document.getElementById('study_timer');
var timerRepeat = document.getElementById('timer_repeat');
var startTime;
var updateTime;
var difference;
var tInterval;
var savedTime;
var paused = 0;
var running = 0;
var toggle = false;
var saving = false;


function outOfPage() {
    if (timerDisplay.innerText != '00:00:00') {
        if (saving == false) {
            return "warning"
        }
    } 
}

window.onbeforeunload = outOfPage;

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
    pauseTimer();
    var confirmation = confirm('Are you sure you want to reset your timer?')
    if (confirmation == true) {
        clearInterval(tInterval);
        savedTime = 0;
        difference = 0;
        paused = 0;
        running = 0;
        timerDisplay.innerHTML = '00:00:00';
        timerRepeat.value = '00:00:00';
    } else {
        startTimer();
    }
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
    timerRepeat.value = hours + ':' + minutes + ':' + seconds;
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

function save() {
    saving = true;
    pauseTimer();
    var timer_form = document.getElementById('timer_form');
    if (confirm('Do you want to register this record and reset the timer?')) {
        timer_form.submit();
    } else {
        startTimer();
        return false;
    }
}
document.addEventListener('DOMContentLoaded', function () {
    let timerLabel = document.getElementById('timer-label'); // all these r variable references DOM elements whic is like the labels and buttons in the interface
    let timeDisplay = document.getElementById('time');
    let shortBreakButton = document.getElementById('short-break-btn');
    let longBreakButton = document.getElementById('long-break-btn');       
    let startButton = document.getElementById('start-btn');
    let pauseButton = document.getElementById('pause-btn');
    let resetButton = document.getElementById('reset-btn');
    let studyTimeInput = document.getElementById('study-time');

    let timer; // 'timer' holds the reference to the interval timer
    let isRunning = false; // 'isRunning' can keep track if the timer running or not
    let seconds = 25 * 60; // 'seconds' is like the default time which is 25 minutes
    let studyTime = seconds; // Store what time the user wants to study at

    // this function converts seconds into minutes and also remaining seconds thats why it has the modulus %
    function updateDisplay() {
        let minutes = Math.floor(seconds / 60);
        let secs = seconds % 60;
        timeDisplay.textContent = `${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
    } // this is event listener for DOMContentLoaded, it makes the javascript code runs only after the HTML document
      // has been fully loaded and parsed

    
    // this func starts a timer with specified DURATION and LABEL, updates the display every second bc if not then how u gonna see
    // how much time u have left lol, it also alerts the user when time reaches 0
    function startTimer(duration, label) {
        if (isRunning) return;
        isRunning = true;
        timerLabel.textContent = label;
        seconds = duration * 60;
        updateDisplay();
        timer = setInterval(() => {
            if (seconds > 0) {
                seconds--;
                updateDisplay();
            } else {
                clearInterval(timer);
                isRunning = false;
                alert('TIME IS UP!');
            }
        }, 1000);
    }

    //this func reads the study time from the user input, it also starts the startTimer
    function startStudy() {
        studyTime = parseInt(studyTimeInput.ariaValueMax, 10);
        startTimer(studyTime, 'STUDY')
    }

    //this func starts a 5-minute break after using startTimer, cannot change the break
    function startShortBreak() {
        startTimer(5, 'SHORT BREAK');
    }

    //this func starts a 10-minute break, same like startShortBreak, but its now a 10 minute break
    function startLongBreak() {
        startTimer(10, 'LONG BREAK');
    }

    //this func basically just pause the timer la, it also clears the interval if its running
    function pauseTimer() {
        if (!isRunning) return;
        clearInterval(timer);
        isRunning = false;
    }

    //this func stops timer, and resets the timer to the time inputted by the user
    //updates the display
    function resetTimer() {
        clearInterval(timer);
        isRunning = false;
        seconds = studyTime * 60;
        updateDisplay();
    }

    //This is Event Listeners for buttons, so that if u click it then the functions will trigger
    startButton.addEventListener('click', startTimer);
    pauseButton.addEventListener('click', pauseTimer);
    resetButton.addEventListener('click', resetTimer);
    shortBreakButton.addEventListener('click', startShortBreak);
    longBreakButton.addEventListener('click', startShortBreak);


    //This is like initial display update, it calls updateDisplay to show the default timer value when the page loads :)
    updateDisplay();
});

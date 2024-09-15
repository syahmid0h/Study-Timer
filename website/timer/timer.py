from flask import Flask, render_template_string, jsonify, request
import time

app = Flask(__name__)

# To manage the countdown timer
start_time = None
total_time = 0
is_running = False

@app.route('/')
def index():
    return render_template_string('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Countdown Timer with Breaks</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #f5f5dc;
        }

        .container {
            text-align: center;
        }

        #timer {
            font-size: 4rem;
            margin-bottom: 20px;
            color: #87CEEB;
        }

        .buttons {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 20px;
        }

        .buttons button {
            font-size: 1rem;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            background-color: #87CEEB;
            color: white;
            cursor: pointer;
            min-width: 120px;
        }

        .buttons button:hover {
            background-color: #4682B4;
        }

        input[type="text"] {
            font-size: 1rem;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <input type="text" id="inputTime" placeholder="Your desired time !(eg,in minutes)">
        <div id="timer">00:00:00</div>
        <div class="buttons">
            <button id="start">Start</button>
            <button id="stop">Stop</button>
            <button id="reset">Reset</button>
            <button id="shortBreak">Short Break </button>
            <button id="longBreak">Long Break </button>
        </div>
    </div>
    <script>
        let interval;

        function updateTime() {
            fetch('/time')
            .then(response => response.json())
            .then(data => {
                document.getElementById('timer').innerText = data.time;
            });
        }

        document.getElementById('start').addEventListener('click', function() {
            const inputTime = document.getElementById('inputTime').value;
            fetch('/start', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ "time": inputTime })
            });
            if (!interval) {
                interval = setInterval(updateTime, 1000);
            }
        });

        document.getElementById('stop').addEventListener('click', function() {
            fetch('/stop', {method: 'POST'});
            clearInterval(interval);
            interval = null;
        });

        document.getElementById('reset').addEventListener('click', function() {
            fetch('/reset', {method: 'POST'});
            document.getElementById('timer').innerText = "00:00:00";
            clearInterval(interval);
            interval = null;
        });

        document.getElementById('shortBreak').addEventListener('click', function() {
            fetch('/start', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ "time": 5 })  // 5 minutes for short break
            });
            if (!interval) {
                interval = setInterval(updateTime, 1000);
            }
        });

        document.getElementById('longBreak').addEventListener('click', function() {
            fetch('/start', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ "time": 10 })  // 10 minutes for long break
            });
            if (!interval) {
                interval = setInterval(updateTime, 1000);
            }
        });
    </script>
</body>
</html>
''')

# Helper function to convert minutes to seconds
def minutes_to_seconds(minutes):
    return int(minutes) * 60

# Helper function to format seconds into "hh:mm:ss"
def format_time(seconds):
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

# Start the timer
@app.route('/start', methods=['POST'])
def start():
    global start_time, total_time, is_running
    data = request.get_json()
    input_time = data.get('time')

    if input_time:
        total_time = minutes_to_seconds(input_time)  # Convert minutes to total seconds
    else:
        total_time = 0  # Default to 0 if no time is provided

    if not is_running:
        start_time = time.time()
        is_running = True

    return jsonify({"status": "started"})

# Stop the timer
@app.route('/stop', methods=['POST'])
def stop():
    global total_time, is_running
    if is_running:
        elapsed = time.time() - start_time
        total_time -= int(elapsed)  # Subtract the elapsed time from the total time
        is_running = False
    return jsonify({"status": "stopped"})

# Reset the timer
@app.route('/reset', methods=['POST'])
def reset():
    global start_time, total_time, is_running
    start_time = None
    total_time = 0
    is_running = False
    return jsonify({"status": "reset"})

# Get remaining time
@app.route('/time', methods=['GET'])
def get_time():
    global is_running
    if is_running:
        elapsed = time.time() - start_time
        remaining_time = total_time - int(elapsed)  # Subtract the elapsed time from the total time
        if remaining_time <= 0:
            remaining_time = 0
            is_running = False
    else:
        remaining_time = total_time

    return jsonify({"time": format_time(remaining_time)})

if __name__ == '__main__':
    app.run(debug=True)

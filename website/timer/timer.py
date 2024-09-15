from flask import Flask, render_template_string, jsonify
import time

app = Flask(__name__)

# Global variables to manage the stopwatch state
start_time = None
elapsed_time = 0
is_running = False

@app.route('/')
def index():
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stopwatch</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #f5f5dc; /* Beige background */
        }

        .container {
            text-align: center;
        }

        #stopwatch {
            font-size: 4rem;
            margin-bottom: 20px;
            color: #87CEEB; /* Baby blue color for the stopwatch text */
        }

        .buttons button {
            font-size: 1rem;
            padding: 10px 20px;
            margin: 5px;
            border: none;
            border-radius: 5px;
            background-color: #87CEEB; /* Baby blue color for buttons */
            color: white;
            cursor: pointer;
        }

        .buttons button:hover {
            background-color: #4682B4; /* Slightly darker baby blue on hover */
        }
    </style>
</head>
<body>
    <div class="container">
        <div id="stopwatch">00:00:00</div>
        <div class="buttons">
            <button id="start">Start</button>
            <button id="stop">Stop</button>
            <button id="reset">Reset</button>
        </div>
    </div>
    <script>
        let interval;

        function updateTime() {
            fetch('/time')
            .then(response => response.json())
            .then(data => {
                document.getElementById('stopwatch').innerText = data.time;
            });
        }

        document.getElementById('start').addEventListener('click', function() {
            fetch('/start', {method: 'POST'});
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
            document.getElementById('stopwatch').innerText = "00:00:00";
            clearInterval(interval);
            interval = null;
        });
    </script>
</body>
</html>
''')

@app.route('/start', methods=['POST'])
def start():
    global start_time, is_running
    if not is_running:
        start_time = time.time() - elapsed_time
        is_running = True
    return jsonify({"status": "started"})

@app.route('/stop', methods=['POST'])
def stop():
    global elapsed_time, is_running
    if is_running:
        elapsed_time = time.time() - start_time
        is_running = False
    return jsonify({"status": "stopped"})

@app.route('/reset', methods=['POST'])
def reset():
    global start_time, elapsed_time, is_running
    start_time = None
    elapsed_time = 0
    is_running = False
    return jsonify({"status": "reset"})

@app.route('/time', methods=['GET'])
def get_time():
    if is_running:
        current_time = time.time() - start_time
    else:
        current_time = elapsed_time
    minutes, seconds = divmod(int(current_time), 60)
    hours, minutes = divmod(minutes, 60)
    return jsonify({"time": f"{hours:02}:{minutes:02}:{seconds:02}"})

if __name__ == '__main__':
    app.run(debug=True)

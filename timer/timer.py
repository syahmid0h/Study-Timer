from flask import Flask, render_template_string, redirect, url_for, jsonify
import time

app = Flask(__name__)

start_time = 0
elapsed_time = 0
running = False

# Helper function to convert elapsed time to a string
def time_to_string(elapsed):
    hrs, rem = divmod(elapsed, 3600)
    mins, secs = divmod(rem, 60)
    return f"{int(hrs):02}:{int(mins):02}:{int(secs):02}"

@app.route('/')
def index():
    global elapsed_time
    if running:
        elapsed_time = time.time() - start_time
    return render_template_string(html_template, time=time_to_string(elapsed_time))

@app.route('/start', methods=['POST'])
def start_timer():
    global start_time, running
    if not running:
        start_time = time.time() - elapsed_time
        running = True
    return redirect(url_for('index'))

@app.route('/stop', methods=['POST'])
def stop_timer():
    global elapsed_time, running
    if running:
        elapsed_time = time.time() - start_time
        running = False
    return redirect(url_for('index'))

@app.route('/reset', methods=['POST'])
def reset_timer():
    global start_time, elapsed_time, running
    start_time = 0
    elapsed_time = 0
    running = False
    return redirect(url_for('index'))

@app.route('/status')
def timer_status():
    global elapsed_time
    if running:
        elapsed_time = time.time() - start_time
    return jsonify({"time": time_to_string(elapsed_time)})

html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Study Timer</title>
    <style>
        body { font-family: Arial, sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; background-color: #f0f0f0; }
        .timer-display { font-size: 3rem; margin-bottom: 20px; }
        .timer-controls button { font-size: 1rem; padding: 10px 20px; margin: 5px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="timer-display" id="timerDisplay">{{ time }}</div>
    <div class="timer-controls">
        <form action="/start" method="post"><button type="submit">Start</button></form>
        <form action="/stop" method="post"><button type="submit">Stop</button></form>
        <form action="/reset" method="post"><button type="submit">Reset</button></form>
    </div>
    <script>
        setInterval(async function() {
            const response = await fetch('/status');
            const data = await response.json();
            document.getElementById("timerDisplay").innerHTML = data.time;
        }, 1000);
    </script>
</body>
</html>
'''

if __name__ == '_main_':
    app.run(debug=True)
from flask import Blueprint, render_template, jsonify, request
import time

views = Blueprint('views', __name__)

# Timer variables
timer_running = False
timer_duration = 0
timer_start_time = 0
paused_time = 0
is_paused = False
is_on_break = False
break_duration = 5 * 60

# Helper functions
def minutes_to_seconds(minutes):
    return minutes * 60

def format_time(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:02d}"

@views.route('/')
def index():
    return render_template('index.html')

@views.route('/start', methods=['POST'])
def start_timer():
    global timer_running, timer_duration, timer_start_time, is_paused, is_on_break
    data = request.get_json()
    if data and 'time' in data:
        timer_duration = minutes_to_seconds(int(data['time']))  # Time in minutes from the user
        if not is_paused:
            timer_start_time = time.time()  # Record the current time
        else:
            # If paused, adjust start time to account for paused time
            timer_start_time = time.time() - paused_time
        timer_running = True
        is_paused = False
        is_on_break = False  # Reset break status when starting a new timer
        return jsonify({"status": "Timer started"})
    return jsonify({"status": "Invalid request"}), 400

@views.route('/pause', methods=['POST'])
def pause_timer():
    global timer_running, paused_time, is_paused
    if timer_running:
        timer_running = False
        paused_time = time.time() - timer_start_time  # Record the paused time
        is_paused = True
        return jsonify({"status": "Timer paused"})
    return jsonify({"status": "Timer is not running"}), 400

@views.route('/reset', methods=['POST'])
def reset_timer():
    global timer_running, timer_duration, timer_start_time, paused_time, is_paused, is_on_break
    timer_running = False
    timer_duration = 0
    timer_start_time = 0
    paused_time = 0
    is_paused = False
    is_on_break = False  # Ensure the break flag is reset when the timer is reset
    return jsonify({"status": "Timer reset"})

@views.route('/time', methods=['GET'])
def get_time():
    global timer_duration, timer_start_time, timer_running, is_paused, is_on_break, break_duration
    if not timer_running and not is_paused:
        return jsonify({"time": format_time(timer_duration)})
    elif timer_running:
        elapsed_time = time.time() - timer_start_time
        remaining_time = timer_duration - int(elapsed_time)

        if remaining_time <= 0 and not is_on_break:
            timer_running = True  
            timer_start_time = time.time()
            timer_duration = break_duration 
            is_on_break = True  
            return jsonify({"time": "BREAK TIME!"})
        
        elif remaining_time <= 0 and is_on_break:
            timer_running = False
            remaining_time = 0
            return jsonify({"time": "BREAK'S OVER!"})

        return jsonify({"time": format_time(remaining_time)})
    else:
        elapsed_time = time.time() - timer_start_time
        remaining_time = timer_duration - int(elapsed_time)
        return jsonify({"time": format_time(remaining_time)})
    

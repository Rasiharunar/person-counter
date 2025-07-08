#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import subprocess
import sys
import os
import threading
# import cv2
# from flask import Response

app = Flask(__name__)
app.secret_key = 'rahasia-super-aman'  # ganti di produksi

# Dummy user
users = {
    "admin": "admin123"                                                                                  
}

# Status tracking (simulasi)
status = {
    "camera_active": False,
    "video_streaming": False,
    "person_count": 0
}

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        if uname in users and users[uname] == pwd:
            session['username'] = uname
            return redirect(url_for('index'))
        else:
            flash('Username atau password salah')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/get_stream_status')
def get_stream_status():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    return jsonify(status)

@app.route('/start_camera', methods=['POST'])
def start_camera():
    status['camera_active'] = True
    return jsonify({'status': 'success', 'message': 'Camera started'})

@app.route('/stop_camera', methods=['POST'])
def stop_camera():
    status['camera_active'] = False
    return jsonify({'status': 'success', 'message': 'Camera stopped'})

@app.route('/start_video_stream', methods=['POST'])
def start_video_stream():
    status['video_streaming'] = True
    return jsonify({'status': 'success', 'message': 'Video streaming started'})

@app.route('/stop_video_stream', methods=['POST'])
def stop_video_stream():
    status['video_streaming'] = False
    return jsonify({'status': 'success', 'message': 'Video streaming stopped'})

@app.route('/test_api')
def test_api():
    return jsonify({'status': 'success', 'response_code': 200})

@app.route('/send_frame', methods=['POST'])
def send_frame():
    status['person_count'] += 1  # Simulasi: tambah orang
    return jsonify({'status': 'success', 'message': 'Frame sent'})

@app.route('/record_data')
def record_data():
    event_name = request.args.get('event_name')
    if not event_name:
        return jsonify({'status': 'error', 'message': 'No event name provided'})
    # Simulasi rekam event
    print(f"Event: {event_name}, Count: {status['person_count']}")
    return jsonify({'status': 'success', 'message': 'Event recorded'})


# camera = cv2.VideoCapture(0)

# def generate_frames():
#     while True:
#         success, frame = camera.read()
#         if not success:
#             break
#         else:
#             # Encode ke JPEG
#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# @app.route('/video_feed')
# def video_feed():
#     if 'username' not in session:
#         return redirect(url_for('login'))
#     return Response(generate_frames(),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')



# Jalankan Flask app
if __name__ == "__main__":
    app.run(debug=True)

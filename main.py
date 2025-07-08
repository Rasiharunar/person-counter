#!/usr/bin/env python3
"""
Script untuk menjalankan Flask app tanpa ngrok (karena menggunakan Cloudflare Tunnel)
"""
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import subprocess
import sys
import os
import threading


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
def install_requirements():
    """Install dependencies dari requirements.txt"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        sys.exit(1)

def run_flask_app():
    """Jalankan Flask app"""
    try:
        os.environ['FLASK_ENV'] = 'production'
        os.environ['FLASK_DEBUG'] = '0'
        subprocess.run([sys.executable, "app4.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running Flask app: {e}")
    except KeyboardInterrupt:
        print("\n🛑 Flask app stopped by user")

def main():
    print("🏠 Smart Room Person Counter - Cloudflare Tunnel Setup")
    print("=" * 50)

    print("📦 Installing requirements...")
    install_requirements()

    os.makedirs("templates", exist_ok=True)

    print("\n🎯 Setup complete!")
    print("🌐 Make sure your Cloudflare Tunnel is running (e.g. using `cloudflared tunnel run <tunnel-name>`)")
    
    choice = input("\nDo you want to run the Flask app now? (y/n): ").lower()
    
    if choice == 'y':
        print("\n🚀 Starting Flask app...")
        flask_thread = threading.Thread(target=run_flask_app)
        flask_thread.daemon = True
        flask_thread.start()
        flask_thread.join()

    print("\n✅ Flask app exited.")

if __name__ == "__main__":
    main()

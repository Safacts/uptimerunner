from flask import Flask, jsonify, request, redirect, render_template
import threading
import time
import requests
import json
import os

app = Flask(__name__)
URLS_FILE = "urls.json"

# Redirect / to /dashboard
@app.route('/')
def root():
    return redirect('/dashboard')

@app.route('/ping')
def ping():
    return "pong", 200

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

@app.route('/api/urls', methods=['GET', 'POST'])
def handle_urls():
    if not os.path.exists(URLS_FILE):
        with open(URLS_FILE, 'w') as f:
            json.dump([], f)

    if request.method == 'GET':
        with open(URLS_FILE) as f:
            urls = json.load(f)
        statuses = []
        for url in urls:
            try:
                r = requests.get(url, timeout=3)
                statuses.append({
                    "url": url,
                    "status": "✅ Online" if r.status_code < 400 else "❌ Error"
                })
            except:
                statuses.append({
                    "url": url,
                    "status": "❌ Error"
                })
        return jsonify(statuses)

    if request.method == 'POST':
        new_url = request.json.get('url')
        with open(URLS_FILE, 'r+') as f:
            urls = json.load(f)
            if new_url not in urls:
                urls.append(new_url)
                f.seek(0)
                f.truncate()
                json.dump(urls, f)
        return jsonify({"message": "URL added"}), 201

@app.route('/api/urls/<int:index>', methods=['DELETE'])
def delete_url(index):
    if os.path.exists(URLS_FILE):
        with open(URLS_FILE, 'r+') as f:
            urls = json.load(f)
            if 0 <= index < len(urls):
                urls.pop(index)
                f.seek(0)
                f.truncate()
                json.dump(urls, f)
    return jsonify({"message": "URL removed"}), 200


# 🔁 Background self-pinger thread
def keep_alive():
    while True:
        try:
            print("🔁 Pinging self to stay awake...")
            requests.get("https://uptimerunner.onrender.com/ping", timeout=5)
        except Exception as e:
            print("❌ Ping failed:", e)
        time.sleep(300)  # every 5 minutes


if __name__ == '__main__':
    # Start self-ping thread
    threading.Thread(target=keep_alive, daemon=True).start()

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

from flask import Flask, render_template, request, jsonify
import json, os

app = Flask(__name__)

URLS_FILE = "urls.json"

@app.route('/')
def home():
    return "Uptime runner running!"

@app.route('/dashboard')
def dashboard():
    return open('dashboard.html').read()

@app.route('/api/urls', methods=['GET', 'POST', 'DELETE'])
def api_urls():
    if not os.path.exists(URLS_FILE):
        with open(URLS_FILE, 'w') as f:
            json.dump([], f)

    if request.method == 'GET':
        with open(URLS_FILE) as f:
            return jsonify(json.load(f))

    if request.method == 'POST':
        new_url = request.json.get('url')
        with open(URLS_FILE, 'r+') as f:
            urls = json.load(f)
            if new_url not in urls:
                urls.append(new_url)
                f.seek(0)
                json.dump(urls, f)
        return jsonify({"message": "URL added"}), 201

    if request.method == 'DELETE':
        del_url = request.json.get('url')
        with open(URLS_FILE, 'r+') as f:
            urls = json.load(f)
            urls = [u for u in urls if u != del_url]
            f.seek(0)
            f.truncate()
            json.dump(urls, f)
        return jsonify({"message": "URL removed"}), 200

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)


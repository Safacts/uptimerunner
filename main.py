from flask import Flask, request, jsonify, redirect
import json, os, requests

app = Flask(__name__)
URLS_FILE = "urls.json"

# Redirect root to /dashboard
@app.route('/')
def home():
    return redirect('/dashboard')

# Serve dashboard.html from same folder
@app.route('/dashboard')
def dashboard():
    return open('dashboard.html').read()

# API for managing URLs and checking status
@app.route('/api/urls', methods=['GET', 'POST', 'DELETE'])
def api_urls():
    if not os.path.exists(URLS_FILE):
        with open(URLS_FILE, 'w') as f:
            json.dump([], f)

    if request.method == 'GET':
        with open(URLS_FILE) as f:
            urls = json.load(f)

        result = []
        for url in urls:
            try:
                response = requests.head(url, timeout=5)
                status = '✅ Online' if response.status_code < 400 else f'❌ Error {response.status_code}'
            except Exception:
                status = '❌ Unreachable'
            result.append({ "url": url, "status": status })
        return jsonify(result)

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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

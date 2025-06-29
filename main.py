from flask import Flask
import threading, time, requests

app = Flask(__name__)

# Add all the project URLs you want to keep alive
URLS = [
    "https://jnwn.onrender.com/portal/dashboard/",
    "https://your-second-app.vercel.app",
    # Add more here
]

def ping_all():
    for url in URLS:
        try:
            res = requests.get(url, timeout=5)
            print(f"[{url}] → {res.status_code}")
        except Exception as e:
            print(f"[{url}] → Failed: {e}")

    # Wait 10 minutes before pinging again
    time.sleep(600)
    
    # Self-ping to restart the loop
    try:
        print("Self-pinging...")
        requests.get("https://uptime-runner.onrender.com/ping")
    except Exception as e:
        print("Self-ping failed:", e)

@app.route('/')
def home():
    return "✅ Uptime Keeper is Active"

@app.route('/ping')
def ping():
    threading.Thread(target=ping_all).start()
    return "🔁 Ping cycle started"

if __name__ == '__main__':
    app.run(debug=True)

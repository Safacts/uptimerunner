# uptime-runner
# 🌐 Uptime Runner

**Uptime Runner** is a self-hosted Flask web application that monitors and keeps other URLs alive — and even pings itself to stay awake, perfect for free-tier deployment platforms like [Render](https://render.com) that auto-sleep inactive services.

---

## 📌 Features

* ✅ **Monitor External URLs** for availability
* 🔄 **Ping Itself Automatically** every 5 minutes (self-alive mechanism)
* 🧠 Simple **Dashboard UI** to add/delete URLs
* 📊 Real-time **Status Checker** (Online ❁️ / Error ❌)
* 📂 URL data stored persistently in `urls.json`
* 🧠 Smart redirect: `/` → `/dashboard`

---

## 🧱 Folder Structure

```plaintext
.
├── main.py              # Main Flask server
├── templates/
│   └── dashboard.html   # HTML frontend UI
├── urls.json            # Stores all user-monitored URLs
├── requirements.txt     # Required Python packages
└── README.md            # This documentation
```

---

## 🚀 How It Works

### 1. **Dashboard UI**

* Located at `/dashboard`
* Allows users to:

  * Enter a URL to monitor
  * View current status (Online/Error)
  * Remove a URL

### 2. **Backend Logic**

* `/api/urls`: Handles all GET/POST for fetching and saving URLs
* `/api/urls/<index>`: DELETE a specific URL by index
* `/ping`: Returns "pong", used by Render and internal self-pings
* `/`: Redirects to `/dashboard`

### 3. **Self-Alive Thread**

* Inside `main.py`, a **background thread** is launched on server start
* It calls `https://uptimerunner.onrender.com/ping` every 5 minutes
* This prevents Render from sleeping the app

---

## 🔧 Setup Instructions

### 1. Requirements

```bash
python >= 3.9
Flask
requests
```

Install with:

```bash
pip install -r requirements.txt
```

### 2. Run Locally

```bash
python main.py
```

Then visit: `http://localhost:5000`

---

## 📊 API Overview

| Endpoint                | Method | Purpose                               |
| ----------------------- | ------ | ------------------------------------- |
| `/`                     | GET    | Redirects to `/dashboard`             |
| `/dashboard`            | GET    | Shows the web UI                      |
| `/ping`                 | GET    | Returns `pong` for uptime checks      |
| `/api/urls`             | GET    | Get list of monitored URLs + statuses |
| `/api/urls`             | POST   | Add a new URL to monitor              |
| `/api/urls/<int:index>` | DELETE | Delete a URL by index from list       |

---

## 📡 Self-Alive Mechanism

Located in:

```python
def keep_alive():
    while True:
        requests.get("https://uptimerunner.onrender.com/ping")
        time.sleep(300)  # 5 minutes
```

* Automatically runs in a background thread
* Keeps the Render server "warm" so your app stays alive

---

## 🔄 Future Upgrades Ideas

* ⏱ Ping interval settings
* 📨 Optional email alerts
* 📊 Uptime logs/history
* 📉 Graphical statistics for downtime
* 🔐 User authentication

---

## 🧑‍💻 Developed By

**Aadi** – for fun, uptime, and a little chaos 🪫
Made with 🖤, Python & Render.

---

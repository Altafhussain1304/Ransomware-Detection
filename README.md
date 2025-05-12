
# 🛡️ RansomSaver

**RansomSaver** is a real-time, AI-powered, cross-platform ransomware detection and prevention system. It combines behavioral monitoring, file/network inspection, machine learning classification, and a modern Flutter frontend — all backed by a modular Python backend.

---

## 🔧 Features 

- ✅ Real-time file, process, and network monitoring
- ✅ Early-stage ransomware detection based on API behavior
- ✅ Anomaly detection using Isolation Forest
- ✅ AI classification using RNN/SVM models
- ✅ YARA-based signature matching
- ✅ Quarantine system for malicious files
- ✅ Auto-delete toggle for automatic threat removal
- ✅ Restore quarantined files with backup option
- ✅ Simulation mode for testing detection without real threats
- ✅ JSON-formatted logs and full threat history
- ✅ VirusTotal upload endpoint (optional)
- ✅ Summary statistics and visual insights via `/api/summary`
- ✅ FastAPI backend exposing modular REST APIs
- ✅ Flutter frontend integration ready

---

## 📁 Folder Structure

```

RansomSaver/
├── api\_server.py               # FastAPI backend server
├── main.py                     # Central runtime to start backend logic
├── monitoring/
│   ├── file\_monitor.py
│   ├── process\_monitor.py
│   └── network\_monitor.py
├── detection/
│   ├── yara\_scanner.py
│   ├── anomaly\_detector.py
│   └── ml\_classifier.py
├── quarantine/
│   ├── quarantine\_utils.py
│   └── quarantine\_folder/      # Stores quarantined files
├── logs/
│   ├── finalsummary.json
│   └── events\_log.json
├── utils/
│   ├── config.py
│   ├── logger.py
│   └── simulation.py
├── requirements.txt
└── README.md

````

---

## 🚀 How to Run the Backend

### 1. Install Requirements

Make sure you have Python 3.8+ installed. Then run:

```bash
pip install -r requirements.txt
````

### 2. Start the FastAPI Server

```bash
uvicorn api_server:app --reload
```

### 3. Start RansomSaver Backend Engine

```bash
python main.py
```

---

## 📡 API Endpoints (Used by Flutter Frontend)

| Endpoint                  | Method | Description                           |
| ------------------------- | ------ | ------------------------------------- |
| `/api/summary`            | GET    | Get the latest ransomware summary     |
| `/api/quarantine/list`    | GET    | List all quarantined files            |
| `/api/quarantine/restore` | POST   | Restore a file from quarantine        |
| `/api/quarantine/delete`  | POST   | Permanently delete a quarantined file |
| `/api/toggle-auto-delete` | POST   | Toggle automatic deletion of threats  |

---

## 🧪 Simulation Mode

For safe testing, use `utils/simulation.py` to simulate file creation/modification events mimicking ransomware behavior.

You can toggle simulation mode in `config.py`.

---

## 📈 Logs and Analysis

* `logs/finalsummary.json`: Daily summary of detections
* `logs/events_log.json`: Real-time log of all system events
* Flutter will visualize this data in graphs, threat feeds, and dashboards.

---

## 👥 Contributors

* **Backend (Python + FastAPI)**: Altaf
* **Frontend (Flutter + Dart)**: Azim

## 💡 Project Goal

RansomSaver aims to be a lightweight, real-time anti-ransomware solution inspired by research papers and designed with practical features such as early detection, offline operation, cross-platform support, and full visibility into system behavior.

---

```

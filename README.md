# ✈️ QueuePilot  
A scalable, fault-tolerant distributed task scheduling system powered by **Python**, **Flask**, and **Redis**.  
QueuePilot dynamically distributes tasks across worker nodes, ensures automatic recovery from worker failures, and includes a real-time monitoring dashboard.  

---

## 🔧 Features

- ✅ **Distributed Workers** – Run multiple workers in parallel for high throughput.  
- ⟲ **Fault Tolerance** – Heartbeat checks with auto-requeue on worker failure.  
- ⚖️ **Load Balancing** – Tasks routed to the least loaded active worker.  
- 🔍 **Real-Time Dashboard** – Monitor queues, workers, and task states.  
- 📦 **Queue Architecture** – Redis-backed dual-queue design (`task_queue` + `processing:*`).  
- 🧠 **Monitor Node** – Detects stale workers and reassigns their unfinished tasks.  

---

## 📂 Project Structure

```
distributed-task-scheduling-system/
|
├── backend/
│   ├── client_interface/
│   │   └── api.py              # Flask API for submitting and tracking tasks
│   ├── master_node/
│   │   └── scheduler.py        # Scheduler assigns tasks based on load
│   ├── monitor/
│   │   └── monitor.py          # Monitor detects dead workers and requeues tasks
│   ├── task_queue/
│   │   └── redis_queue.py      # Redis queue logic (BRPOPLPUSH, LREM)
│   ├── worker_node/
│   │   └── worker.py           # Worker that processes tasks and sends heartbeats
│   ├── utils/
│   │   └── logger.py           # Logging utility
│   └── venv/                   # Python virtual environment
|
├── frontend/
│   └── dashboard.html          # Real-time dashboard interface
```

---

## 🚀 How It Works

1. **Submit a task** using the dashboard or API.
2. **Master Node** checks worker heartbeats and assigns tasks to the least-loaded.
3. Task is **pushed to the worker's `processing:<id>` queue**.
4. **Worker** picks task, processes it, removes from queue.
5. If worker fails, **Monitor** detects via stale heartbeat and requeues the task to `task_queue`.
6. **Dashboard** updates every 3 seconds from `/queue_status` API.

---

## 💡 Key Components

- **Master Node (Scheduler):** Handles assignment of tasks to workers using live Redis stats.
- **Worker Nodes:** Fetch and execute tasks, and send periodic heartbeats.
- **Redis Queues:** `task_queue` for incoming tasks and `processing:<worker_id>` queues for in-process tasks.
- **Monitor Node:** Detects heartbeat expiry and safely requeues unprocessed tasks.
- **Dashboard:** User interface for submitting and monitoring tasks in real time.

---

## 🧪 Setup Instructions

### 1. Clone Repository
```bash
git clone https://github.com/xuniquepatel/Queue-Pilot.git
cd distributed-task-scheduling-system/backend
```

### 2. Setup Virtual Environment
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Run Redis
Make sure Redis is installed and running on localhost:6379.
```bash
brew install redis
redis-server
```

### 4. Start Each Component
Run these in separate terminals:

#### Master Scheduler
```bash
export PYTHONPATH=$(pwd)
python -m master_node.scheduler
```

#### Monitor Node
```bash
python -m monitor.monitor
```

#### Worker Nodes
```bash
WORKER_INDEX=1 python -m worker_node.worker
WORKER_INDEX=2 python -m worker_node.worker
```

#### Flask API
```bash
python -m client_interface.api
```

#### Frontend Dashboard
```bash
cd frontend
python3 -m http.server 9090
```
Visit: `http://localhost:9090/dashboard.html`

---

## 🌐 REST API Endpoints

| Endpoint         | Method | Description                      |
|------------------|--------|----------------------------------|
| `/submit_task`   | POST   | Submit a new task to scheduler   |
| `/queue_status`  | GET    | View pending tasks & worker info |
| `/system_status` | GET    | Internal system-wide state       |

---

## 🎓 Concepts Used

- Multithreaded task submission
- Redis-backed persistent queues
- Worker heartbeat monitoring
- Fault recovery (auto-reassignment)
- Load-based task distribution

---

## 🤖 Future Enhancements

- Task retry limit / exponential backoff
- Store results to database
- WebSocket live dashboard
- Docker-based deployment
- RESTful logs & history endpoints

---

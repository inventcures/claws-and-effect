# Claws & Code (Claws and Effect) 🦞⚡

[![DeepWiki Indexed](https://img.shields.io/badge/DeepWiki-Indexed-8a2be2.svg)](https://deepwiki.com)

**Transforming programming from typing code into orchestrating cognitive processes.**

Inspired by the shift towards "Agentic Engineering," this repository implements the **Orchestrator-Worker** paradigm. It shifts the human role to defining high-level objectives in English, while a long-running Orchestrator ("Claw") manages multiple parallel execution instances ("Code") via a reactive Pub/Sub event router.

---

## 🌟 Core Architecture

### 1. The Orchestrator ("Claw")
The "Cognitive Brain." It receives a high-level English objective, breaks it down into a dynamic graph of tasks, and manages the execution lifecycle. Instead of a rigid DAG, the Claw uses a **Triage Router** to handle complex, real-world workflows dynamically.

### 2. The Workers ("Code Instances")
The "Specialized Hands." Atomic, ephemeral, and focused. Each worker executes a **Tenacity Loop** (Research -> Strategize -> Act -> Verify). They don't know about each other; they simply do their job and loudly emit domain events (e.g., `invoice:parsed`, `env:ready`) when successful.

### 3. Event-Driven Triage Router (Pub/Sub)
A fully reactive event broker. Downstream agents subscribe to events. When an upstream worker finishes, it publishes an event to the queue, instantly waking up any relevant downstream workers. This allows for massive decoupling, infinite branching, and dynamic workflows without changing the core orchestrator logic.

### 4. The Shared Memory Ledger
A persistent "Notes for Self" system. Since workers are ephemeral, they use the Memory Ledger to brief newly spawned Code instances with necessary context without overflowing their active token windows.

---

## 🖥️ The Perceptive UI: "The Swimlane Matrix"

When managing parallel AI agents, a linear chat feed is the wrong UX. We built a bespoke, high-density, industrial-cybernetic interface focusing on **Parallelism**.

*   **The Swimlane Architecture:** The main workspace is filled with horizontal "Swimlanes", each representing an active parallel Code Instance.
*   **Keyboard-Driven Focus Mode (`↑`/`↓` & `Space`):** Use the arrow keys to quickly cycle through active parallel workers. Press `Space` to expand a focused swimlane and reveal its raw, internal Tenacity Loop logs in a built-in terminal window.
*   **Real-time Event Streaming:** The backend uses WebSockets to stream granular internal state changes, thought streams, and pub/sub events directly to the UI without polling.
*   **The Claw Hub:** A persistent left sidebar showing the Orchestrator's high-level logic and the shared Memory Ledger.

---

## 🚀 Getting Started

This project is built for extreme speed and low overhead using `FastAPI` and `uv`.

### Prerequisites
*   Python 3.10+
*   [uv](https://github.com/astral-sh/uv) (Recommended for lightning-fast dependency management)

### Installation & Execution

```bash
# Clone the repository
git clone https://github.com/inventcures/claws-and-effect.git
cd claws-and-effect

# Create a virtual environment and install dependencies
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

# Start the Perceptive UI Server
uvicorn main:app --host 0.0.0.0 --port 8000
```

Open your browser to `http://localhost:8000`. 
Type an objective into the Architect's Command Bar, hit **Execute**, and watch the parallel agent matrices spin up in real-time!

---

## 🧠 Philosophy: The Human-in-the-Loop (HITL)

The human is the **Director and Architect**, not the **Coder**:
*   **Judgment:** Evaluating output against "taste" and usability standards.
*   **Direction:** Correcting the Claw's strategy if it heads down a suboptimal path.
*   **Hints:** Providing specific domain knowledge or injecting context into the Memory Ledger mid-flight.

*Programming is becoming unrecognizable. You're spinning up AI agents, giving them tasks in English, and managing their work in parallel. The leverage achievable via top-tier agentic engineering feels very high right now.*

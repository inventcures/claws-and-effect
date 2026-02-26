# Claws & Code (Claws and Effect) 🦞⚡

[![DeepWiki Indexed](https://img.shields.io/badge/DeepWiki-Indexed-8a2be2.svg)](https://deepwiki.com)

**Transforming programming from typing code into orchestrating cognitive processes.**

Inspired by the shift towards "Agentic Engineering," this repository implements a highly resilient **Orchestrator-Worker** paradigm. It features an event-driven triage system, adversarial quality gates, and a multi-provider "Bring Your Own Key" (BYOK) fallback architecture.

---

## 🌟 Core Architecture

### 1. The Orchestrator ("Claw")
The "Cognitive Brain." It receives a high-level English objective and decomposes it into a dynamic graph of tasks. Instead of a rigid DAG, the Claw uses a **Triage Router** to handle complex, reactive workflows where agents trigger each other dynamically.

### 2. The Workers ("Code Instances")
The "Specialized Hands." Each worker executes a **Tenacity Loop** (Research -> Strategize -> Act -> Verify). They are ephemeral and decoupled; they simply perform their task and emit domain events (e.g., `env:ready`, `ui:scaffolded`) to trigger downstream logic.

### 3. Adversarial Quality Gates (Reviewers)
Inspired by "Pair Programming" philosophies, every sub-task must pass a dedicated **Reviewer Agent** before finalization. This adversarial loop ensures that hallucinations or edge cases are caught and sent back for revision before they cascade into the broader system.

### 4. Event-Driven Triage Router (Pub/Sub)
A fully reactive event broker. This allows for massive decoupling and infinite branching. Agents subscribe to specific event patterns. When a "Worker" finishes, it publishes an event, instantly waking up the "Reviewer" or the next relevant "Worker" in the pipeline.

### 5. Multi-Provider BYOK with Fallback
A resilient, zero-persistence security model. Users provide their own API keys (Google, OpenAI, Anthropic) directly in the UI. 
*   **Zero-Liability:** Keys are stored exclusively in the browser's `localStorage` and never touch the backend disk.
*   **Prioritized Fallback:** If a primary provider fails (rate limits, downtime), the Orchestrator automatically pivots to your secondary and tertiary keys mid-execution to ensure mission completion.

---

## 🖥️ The Perceptive UI: "The Swimlane Matrix"

A bespoke, high-density dashboard designed for **Parallelism** rather than linear conversation.

*   **The Swimlane Architecture:** Monitor multiple parallel Code Instances in their own dedicated horizontal streams.
*   **Keyboard-Driven Focus Mode (`↑`/`↓` & `Space`):** Cycle through active workers and press `Space` to expand a focused swimlane, revealing its raw, internal logs and cognitive "thoughts."
*   **Weighted Memory Visualizer:** A sidebar feed of the **Memory Ledger** which uses a hybrid scoring algorithm (`0.6 * recency + 0.4 * importance`) to ensure critical context is always surfaced to the agents.
*   **Real-time HUD:** A WebSocket-driven head-up display that pulses and changes state based on whether workers are `Researching`, `Reviewing`, or `Stuck` (triggering escalation).

---

## 🚀 Getting Started

Built for speed and low overhead using `FastAPI` and `uv`.

### Prerequisites
*   Python 3.10+
*   [uv](https://github.com/astral-sh/uv) (Recommended)

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

1.  Open `http://localhost:8000`.
2.  Click the **⚙️ Settings** icon to configure your API Provider fallback list.
3.  Define your objective and hit **Execute**.

---

## 🧠 Philosophy: Agentic Engineering

The human is the **Director and Architect**, not the **Coder**. By ascending layers of abstraction and managing parallel intelligent instances with high-quality oversight, the leverage achievable in modern software engineering becomes exponential.

*Programming is no longer about typing syntax; it's about spinning up orchestrators that manage multiple parallel instances of intelligence for you.*

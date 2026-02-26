# Specification: Claws & Code - Perceptive UI Scaffold
## Visualizing the Agentic Orchestrator

### 1. Vision & Core Philosophy
The shift to "Agentic Engineering" requires a shift from text editors to **Orchestration Dashboards**. The human is no longer typing code; they are managing parallel intelligent processes. The UI must be **perceptive**: it must make the invisible cognitive and execution loops of the AI agents visible, understandable, and controllable.

**Core Tenets:**
*   **Extreme Observability:** Real-time visibility into the Orchestrator's strategy, the parallel workers' Tenacity Loops, and the shared Memory Ledger.
*   **Architectural Control:** The human must be able to pause, inspect, redirect, or assist any agent at any time (Human-in-the-Loop).
*   **Progressive Disclosure:** Hide raw terminal output by default, showing high-level status (Researching, Coding, Verifying), but allow deep-dives into raw logs with a single click.

### 2. UI Architecture & Layout
The interface should be structured into four distinct, persistent zones to monitor the entire lifecycle.

#### Zone A: The Command Deck (Top / Header)
*   **Function:** Where the Human Architect provides the high-level objective and controls the overall session.
*   **Components:**
    *   **Objective Input Prompt:** A large, multi-line text area for the initial English directive.
    *   **Global Controls:** Start, Pause All, Abort, Generate Report.
    *   **High-Level Status:** Overall progress bar (e.g., "Decomposing...", "Executing 4 Sub-Tasks...", "Verifying...").

#### Zone B: The Claw Hub (Left Sidebar / Top Panel)
*   **Function:** Visualizing the Orchestrator's ("Claw") cognitive process and strategic plan.
*   **Components:**
    *   **Task Tree / DAG:** A visual representation of the decomposed sub-tasks and their dependencies.
    *   **Claw Thought Stream:** A live feed of the Orchestrator's reasoning (e.g., "Worker 2 failed SSH setup, allocating new worker to research networking...").
    *   **Synthesis Panel:** Shows the final aggregation of worker outputs.

#### Zone C: The Worker Matrix (Center / Main Canvas)
*   **Function:** Real-time monitoring of parallel Code Instances.
*   **Components:**
    *   **Grid of Worker Cards:** Each card represents a `CodeInstance`.
    *   **Worker Card Anatomy:**
        *   **Header:** Task Name (e.g., "Setup vLLM") and Status Pill (Idle, Researching, Acting, Verifying, Success, Failed).
        *   **Tenacity Loop Indicator:** A circular or stepped progress bar showing the current phase of the loop (Attempt 1/3: Verifying).
        *   **Live Output Snippet:** The last 2-3 lines of stdout/stderr or internal logging.
        *   **Intervene Button:** Allows the human to jump into a specific worker's context to provide a hint or fix an environment issue manually.

#### Zone D: The Memory Ledger (Right Sidebar)
*   **Function:** The persistent "Notes for Self" shared across agents.
*   **Components:**
    *   **Chronological Feed:** A scrolling list of notes, discoveries, and context markers added by the Claw and Workers.
    *   **Tag Filtering:** Ability to filter memory by `[success]`, `[error]`, `[context]`, or specific `task_id`.
    *   **Architect Injection:** A small input field for the human to manually inject context or constraints into the global memory ledger mid-flight.

### 3. Interaction Design (User Journey)
1.  **Initiation:** User types "Set up local video dashboard..." and hits "Deploy Claw".
2.  **Decomposition:** The UI animates the Task Tree appearing in the Claw Hub.
3.  **Parallel Spawning:** Worker Cards pop into the Worker Matrix, immediately entering the "Researching" phase.
4.  **Monitoring:** The user watches the Tenacity Loops cycle. If a worker hits "Attempt 3/3", its card pulses yellow, drawing the user's attention to a potential blocker.
5.  **Intervention (HITL):** User clicks "Intervene" on a failing worker, reads its specific error log, types a hint ("Use port 8080 instead, 80 is blocked"), and resumes the worker.
6.  **Completion:** The UI collapses the matrix, brings the final Markdown Report to the center canvas, and highlights key memory ledger takeaways.

### 4. Technical Implementation Stack

To bridge the asynchronous Python backend with a perceptive real-time UI:

#### Backend (Python / FastAPI)
*   **Framework:** FastAPI to serve the UI and handle WebSocket connections.
*   **State Management:** An asynchronous event bus (using `asyncio.Queue` or Redis pub/sub) that the `ClawOrchestrator` and `CodeInstance`s push state changes to.
*   **API:**
    *   `POST /api/orchestrate`: Start a new objective.
    *   `WS /ws/events`: Real-time WebSocket stream of logs, status changes, and memory updates.

#### Frontend (Web Technologies)
*   **Framework:** React (TypeScript) for robust component state management, or vanilla HTML/JS/CSS for maximum simplicity and zero-build overhead if running locally as a lightweight tool.
*   **Styling:** Vanilla CSS (or Tailwind if configured in the project) using CSS Grid for the Worker Matrix and Flexbox for sidebars.
*   **Real-time:** Native WebSocket API to consume the backend event stream.
*   **Visualization:** Consider lightweight graphing libraries (like `react-flow` or D3) for the Task Tree DAG if complexity increases, otherwise simple nested DOM elements.

### 5. Phases of Development
*   **Phase 1: Headless API & CLI TUI (Terminal UI):** Wrap the current `main.py` in the `rich` library to create a beautiful, multi-panel terminal dashboard (Live displays, Layouts, Panels). This is the fastest way to get real-time observability.
*   **Phase 2: WebSocket Event Bus:** Refactor the backend to emit structured JSON events (e.g., `{"type": "worker_status", "id": "w1", "status": "researching"}`) instead of standard `print()` statements.
*   **Phase 3: Web Dashboard:** Build the React/Vanilla JS frontend based on the 4-Zone layout described above, connecting it to the WebSocket stream.

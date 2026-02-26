# Specification: Claws & Code - The Agentic Orchestrator Paradigm
## Coding Cognitive Pair Partners in the True Sense

### 1. Vision
Transform programming from a manual "typing code" activity into a high-level orchestration of specialized AI agents. This paradigm shifts the human role to defining objectives in English, providing judgment, taste, and high-level direction, while long-running orchestrators ("Claws") manage parallel execution instances ("Code") to solve complex, multi-step engineering tasks.

### 2. Core Architecture: The Orchestrator-Worker Model

#### 2.1 The Orchestrator ("Claw")
*   **Role:** The "Cognitive Brain" and strategic manager.
*   **Characteristics:** Long-running, high-coherence, tenacious, and context-aware.
*   **Responsibilities:**
    *   Decompose high-level English tasks into actionable sub-tasks.
    *   Initialize and manage multiple parallel "Code" instances.
    *   Maintain a "Memory Ledger" of progress, failures, and discoveries.
    *   Perform high-level verification and "judgment" on worker output.
    *   Research solutions online when stuck and adjust strategy dynamically.

#### 2.2 The Worker ("Code Instance")
*   **Role:** The "Specialized Hands" and tactical execution units.
*   **Characteristics:** Atomic, fast, focused, and ephemeral.
*   **Responsibilities:**
    *   Execute specific sub-tasks (e.g., "Install vLLM", "Write web UI", "Set up SSH").
    *   Provide detailed execution logs and status reports to the Claw.
    *   Self-correct small syntax or environment errors during execution.

### 3. Capabilities & Tooling

#### 3.1 Integrated Toolbelt
Both Claws and Code instances must have access to a standardized environment:
*   **Shell/Execution:** Full access to the local/target filesystem and terminal.
*   **Web Research:** Tools for browsing documentation and troubleshooting (e.g., Exa, Google Search).
*   **Memory Store:** A shared or hierarchical memory system (vector DB or persistent JSON logs) to store "memory notes".
*   **Verification:** Native ability to run tests, linters, and type-checkers as a primary success metric.

#### 3.2 Memory & Coherence
*   **Short-term:** Active context window for the current task.
*   **Long-term:** Persistent "Notes for Self" that survive process restarts or sub-agent handoffs.
*   **Knowledge Transfer:** The ability for a Claw to "brief" a new Code instance with relevant context without overwhelming its context window.

### 4. Operational Workflow: "Agentic Engineering"

1.  **Objective Definition:** Human provides a high-level goal in natural language (e.g., "Set up a local video analysis dashboard").
2.  **Strategic Decomposition:** The Claw analyzes the goal, checks the current environment, and drafts a multi-step plan.
3.  **Parallel Delegation:** The Claw spins up multiple Code instances for independent sub-tasks (e.g., one for backend setup, one for UI scaffolding).
4.  **Autonomous Resolution:** Workers encounter issues, research them, fix them, and report back.
5.  **Synthesis & Verification:** The Claw integrates the work, runs system-wide tests, and performs the final "hand-off" to the human.
6.  **Reporting:** The Claw provides a markdown report of what was done, issues encountered, and future recommendations.

### 5. The Human-in-the-Loop (HITL)
The human is the **Director and Architect**, not the **Coder**:
*   **Judgment:** Evaluating if the UI meets "taste" and "usability" standards.
*   **Direction:** Correcting the Claw's strategy if it heads down a suboptimal path.
*   **Hints:** Providing specific domain knowledge that the AI might lack.
*   **Iteration:** Refining the high-level objective based on the agent's findings.

### 6. Technical Requirements for "True Cognitive Pairing"
*   **Tenacity:** The agent must not give up after one error; it must loop (Research -> Strategy -> Action -> Verify).
*   **Verification-First:** No task is complete without a verification script or test run.
*   **Observability:** The human must be able to view the Claw's "thought process" and worker logs in real-time or via detailed history.

# Implementation Plan: Advanced Quality & Resilience Protocols (Inspired by OpenSwarm)

## Approach
Taking inspiration from the philosophies of OpenSwarm, we want to upgrade the Orchestrator to be more than just a task executor. We want to add **adversarial quality control** and **anti-loop resilience**. 

The current Claws & Code orchestrator runs workers in parallel and trusts their output if their internal "Verify" step passes. However, AI is prone to hallucinations and getting stuck in loops. We will implement three core concepts:
1.  **The Adversarial Reviewer:** Every sub-task must pass a dedicated `ReviewerAgent` before being marked as a final success.
2.  **The "Stuck" Detector & Escalation:** If a worker hits its max retries, instead of just failing, the Orchestrator "escalates" the context to the human or a higher-tier reasoning agent.
3.  **Weighted Memory Recall:** Enhance the `MemoryLedger` to prioritize context not just by recency, but by "importance" flags.

**Why this solution:**
- Greatly increases the reliability of the generated output.
- Prevents workers from burning tokens in infinite failure loops.
- Makes the Memory Ledger smarter.

## Steps

1. **Implement the Adversarial Reviewer** (30 min)
   - Files to create: `src/worker/reviewer_instance.py`
   - Files to modify: `src/orchestrator/claw.py`
   - Create a new type of worker that subscribes to `task:completed` events. It takes the output of a `CodeInstance`, analyzes it against the original objective, and emits either `review:approved` or `review:rejected`.

2. **Implement the Stuck Detector (Anti-Loop)** (20 min)
   - Files to modify: `src/worker/code_instance.py`
   - In the Tenacity Loop, if `attempt == max_retries`, emit a specific `worker:stuck` event instead of just `failed`.
   - Update the UI (`static/index.html`) to prominently display a "⚠️ STUCK - ESCALATION REQUIRED" state, prompting the Architect for a hint.

3. **Upgrade the Memory Ledger Scoring** (20 min)
   - Files to modify: `src/memory/ledger.py`
   - Add `importance` (1-5) and `frequency` counters to memory notes.
   - Update `get_context()` to sort notes by a hybrid score (`0.6 * recency + 0.4 * importance`) rather than purely chronological limits.

4. **UI Integration for Review & Escalation** (20 min)
   - Files to modify: `static/index.html`
   - Add visual indicators in the Swimlanes for when a task is in the "Review" phase.
   - Add a prominent "Escalate / Unstick" action button for stuck workers.

## Timeline
| Phase | Duration |
|-------|----------|
| Adversarial Reviewer | 30 min |
| Stuck Detector | 20 min |
| Memory Scoring | 20 min |
| UI Integration | 20 min |
| **Total** | **1.5 hours** |

## Rollback Plan
1. Revert `src/orchestrator/claw.py` to remove the Reviewer subscription logic.
2. Revert `src/worker/code_instance.py` to its standard failure emission.
3. Revert `src/memory/ledger.py` to use simple chronological slicing.

## Security Checklist
- [ ] Ensure Reviewer prompts are strictly sandboxed and cannot execute arbitrary code themselves (pure analysis).
- [ ] Implement strict token limits on the memory retrieval to prevent the new scoring system from pulling in too much context and causing token overflow.
- [ ] Ensure the "Escalation" mechanism gracefully pauses execution without crashing the asyncio event loop.

---
Save to: `plans/advanced-quality-protocols-20260226.md`

## NEXT STEPS
```bash
# Ready? Run:
/cook @plans/advanced-quality-protocols-20260226.md
```
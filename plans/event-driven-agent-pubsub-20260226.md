# Implementation Plan: Event-Driven Agent Pub/Sub (Triage Logic)

## Approach
Currently, the Orchestrator executes a hardcoded, static DAG of tasks in parallel. To support complex, real-world workflows (like the invoice processing example you mentioned), we need a reactive, **Event-Driven Architecture (Pub/Sub)**.

Instead of the Claw "managing" workers directly and synchronously, workers will subscribe to specific **Event Topics** via a central Triage Router. When an agent finishes a task, it emits a new event, which the Triage Router distributes to the next relevant worker(s).

**Why this solution:**
- **Decoupling:** Agents don't need to know about each other. An `EmailAgent` just emits an `email:received` event; it doesn't care who processes it.
- **Scalability:** You can easily add a new agent (e.g., `SlackNotifierAgent`) that just listens for the `invoice:processed` event without modifying the core logic.
- **Dynamic Workflows:** Tasks can loop, branch, or halt organically based on the actual events emitted, rather than a pre-planned static list.

## Steps
1. **Core PubSub Infrastructure** (30 min)
   - Create `src/orchestrator/router.py`.
   - Implement an internal `TriageRouter` (Pub/Sub broker) using `asyncio.Queue`.
   - It needs `subscribe(topic_pattern, handler)` and `publish(event_name, payload)`.

2. **Agent Refactoring (Event Emitters)** (45 min)
   - Modify `src/worker/code_instance.py` (or create specific Agent classes like `InvoiceAgent`, `ERPAgent`).
   - Inject the `TriageRouter` into the workers.
   - Update workers to `publish()` domain events upon completion (e.g., `invoice:parsed`, `erp:updated`) in addition to their standard UI status updates.

3. **Orchestrator Refactoring (The Triage Logic)** (45 min)
   - Modify `src/orchestrator/claw.py`.
   - Instead of a static `asyncio.gather()`, the Claw will setup the subscriptions (e.g., "When `email:received` occurs, route to `InvoiceAgent`").
   - The Claw kicks off the process by publishing the initial `objective:started` event.
   - The Orchestrator stays alive as long as there are pending events in the queue or active workers.

4. **UI Integration (Visualizing the Event Stream)** (30 min)
   - Update `src/events.py` to intercept these new internal Pub/Sub events and broadcast them to the frontend.
   - Update `static/index.html` to visually represent these downstream triggers (perhaps showing the event flow in the Claw Hub or visually linking swimlanes when one triggers another).

## Timeline
| Phase | Duration |
|-------|----------|
| PubSub Router | 30 min |
| Agent Refactoring | 45 min |
| Orchestrator Refactoring | 45 min |
| UI Event Visualization | 30 min |
| **Total** | **2.5 hours** |

## Rollback Plan
1. Revert `src/orchestrator/claw.py` to use `asyncio.gather` over the static task list.
2. Remove `src/orchestrator/router.py`.
3. Remove event emission from the end of the `CodeInstance.execute()` block.

## Security Checklist
- [ ] Prevent infinite event loops (add a TTL or max-depth counter to event envelopes).
- [ ] Ensure event payloads are validated (Pydantic models) before routing to prevent injection or malformed data crashes.
- [ ] Implement Dead-Letter Queues (DLQ) for unhandled events (e.g., if an event is emitted but no agent is subscribed to it).

---
Save to: `plans/event-driven-agent-pubsub-20260226.md`

## NEXT STEPS
```bash
# Ready? Run:
/cook @plans/event-driven-agent-pubsub-20260226.md
```

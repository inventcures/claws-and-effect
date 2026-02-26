import asyncio
from typing import Callable, Dict, List, Any, Set
import fnmatch

class TriageRouter:
    def __init__(self):
        self.queue = asyncio.Queue()
        self.subscriptions: List[Dict[str, Any]] = []
        self._task = None
        self.active_tasks: Set[asyncio.Task] = set()

    def subscribe(self, topic_pattern: str, handler: Callable):
        """Subscribe a handler to an event topic pattern (e.g., 'invoice:*' or 'env:ready')."""
        self.subscriptions.append({"pattern": topic_pattern, "handler": handler})

    async def publish(self, topic: str, payload: dict = None):
        """Publish an event to the queue."""
        payload = payload or {}
        await self.queue.put({"topic": topic, "payload": payload})

    async def _process_events(self):
        """Background task to route events from the queue to subscribers."""
        while True:
            event = await self.queue.get()
            topic = event["topic"]
            payload = event["payload"]
            
            # Find matching subscriptions
            handlers = []
            for sub in self.subscriptions:
                if fnmatch.fnmatch(topic, sub["pattern"]):
                    handlers.append(sub["handler"])
            
            # Execute handlers concurrently
            if handlers:
                for handler in handlers:
                    task = asyncio.create_task(handler(payload))
                    self.active_tasks.add(task)
                    task.add_done_callback(self.active_tasks.discard)
            else:
                print(f"[Router DLQ] No subscribers for event: {topic}")
            
            self.queue.task_done()

    def start(self):
        """Start the event processing loop."""
        if not self._task:
            self._task = asyncio.create_task(self._process_events())

    async def stop(self):
        """Wait for queue to empty and stop the loop."""
        while True:
            await self.queue.join()
            if not self.active_tasks:
                if self.queue.empty():
                    break
            else:
                # Wait for current active tasks, which may queue more events
                await asyncio.gather(*self.active_tasks)
                
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

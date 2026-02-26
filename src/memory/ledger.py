import json
import os
from datetime import datetime
from typing import List, Dict, Any

class MemoryLedger:
    def __init__(self, filename="ledger.json"):
        self.filename = filename
        self.memory: List[Dict[str, Any]] = self._load()

    def _load(self) -> List[Dict[str, Any]]:
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def _save(self):
        with open(self.filename, 'w') as f:
            json.dump(self.memory, f, indent=4)

    def add_note(self, agent_id: str, note: str, tags: List[str] = None):
        """Persistent 'Notes for Self'."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "agent_id": agent_id,
            "note": note,
            "tags": tags or []
        }
        self.memory.append(entry)
        self._save()

    def get_context(self, tags: List[str] = None) -> str:
        """Retrieves recent notes, optionally filtered by tags, to brief a new Code instance."""
        filtered = self.memory
        if tags:
            filtered = [m for m in self.memory if any(tag in m.get("tags", []) for tag in tags)]
        
        # Return the last 10 relevant notes to prevent context window overflow
        recent = filtered[-10:]
        if not recent:
            return "No previous context."
        
        context_str = "Prior Context from Memory Ledger:\n"
        for entry in recent:
            context_str += f"[{entry['timestamp']}] Agent {entry['agent_id']}: {entry['note']}\n"
        return context_str

    def clear(self):
        self.memory = []
        self._save()

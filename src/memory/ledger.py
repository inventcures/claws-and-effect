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

    def add_note(self, agent_id: str, note: str, tags: List[str] = None, importance: int = 1):
        """Persistent 'Notes for Self'."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "agent_id": agent_id,
            "note": note,
            "tags": tags or [],
            "importance": importance,
            "frequency": 1
        }
        self.memory.append(entry)
        self._save()

    def get_context(self, tags: List[str] = None) -> str:
        """Retrieves recent notes, optionally filtered by tags, using a hybrid score."""
        filtered = self.memory
        if tags:
            filtered = [m for m in self.memory if any(tag in m.get("tags", []) for tag in tags)]
        
        if not filtered:
            return "No previous context."

        total_notes = len(filtered)
        def score(index, note):
            recency = (index + 1) / total_notes
            importance_norm = note.get("importance", 1) / 5.0
            return 0.6 * recency + 0.4 * importance_norm

        scored_notes = [(score(i, note), note) for i, note in enumerate(filtered)]
        scored_notes.sort(key=lambda x: x[0], reverse=True)
        
        # Return the top 10 relevant notes
        top_notes = [n[1] for n in scored_notes[:10]]
        # Sort back chronologically for readable briefing
        top_notes.sort(key=lambda x: x["timestamp"])
        
        context_str = "Prior Context from Memory Ledger:\n"
        for entry in top_notes:
            context_str += f"[{entry['timestamp']}] Agent {entry['agent_id']}: {entry['note']}\n"
        return context_str

    def clear(self):
        self.memory = []
        self._save()

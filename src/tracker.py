import json
import os
from typing import Dict, Any
import logging
from .config import CONFIG

log = logging.getLogger("PolyCopy.tracker")


class StateTracker:
    """Track and persist market positions and state"""

    def __init__(self, state_file: str = CONFIG.state_file):
        self.state_file = state_file
        self.state: Dict[str, Any] = {}
        self._load()

    def _load(self):
        """Load state from JSON file"""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    self.state = json.load(f)
                log.info(f"Loaded state from {self.state_file}")
            except Exception as e:
                log.warning(f"Failed to load state: {e}, starting fresh")
                self.state = {}
        else:
            self.state = {}

    def _save(self):
        """Save state to JSON file"""
        try:
            dir_path = os.path.dirname(self.state_file)
            if dir_path:  # Only create if path is not empty
                os.makedirs(dir_path, exist_ok=True)
            with open(self.state_file, 'w') as f:
                json.dump(self.state, f, indent=2)
            log.debug(f"State saved to {self.state_file}")
        except Exception as e:
            log.error(f"Failed to save state: {e}")

    def set_position(self, market_id: str, position: Dict[str, Any]):
        """Set a market position"""
        self.state[market_id] = position
        self._save()

    def get_position(self, market_id: str) -> Dict[str, Any]:
        """Get a market position"""
        return self.state.get(market_id, {})

    def get_all_positions(self) -> Dict[str, Any]:
        """Get all positions"""
        return self.state.copy()

    def update_position(self, market_id: str, updates: Dict[str, Any]):
        """Update a position with new data"""
        if market_id not in self.state:
            self.state[market_id] = {}
        self.state[market_id].update(updates)
        self._save()

    def clear_position(self, market_id: str):
        """Remove a position"""
        if market_id in self.state:
            del self.state[market_id]
            self._save()

    def clear_all(self):
        """Clear all state"""
        self.state = {}
        self._save()


# Global tracker instance
tracker = StateTracker()

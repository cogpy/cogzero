"""
OpenCog AtomSpace Manager

This module provides a singleton AtomSpace manager to ensure all OpenCog tools
and extensions share the same AtomSpace instance across an agent's lifecycle.
"""

from typing import Optional
import threading


class OpenCogManager:
    """
    Singleton manager for OpenCog AtomSpace instances.
    
    This ensures that all OpenCog tools and extensions within an agent
    share the same AtomSpace, enabling knowledge to persist and be shared
    across different tool invocations.
    """
    
    _instance = None
    _lock = threading.Lock()
    _atomspaces = {}  # Dictionary mapping agent contexts to atomspaces
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        # Only initialize once
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self._atomspace_class = None
            self._type_constructors = None
            self._opencog_available = False
            self._initialize_opencog()
    
    def _initialize_opencog(self):
        """Initialize OpenCog imports if available."""
        try:
            from opencog.atomspace import AtomSpace, types
            from opencog import type_constructors
            
            self._atomspace_class = AtomSpace
            self._types = types
            self._type_constructors = type_constructors
            self._opencog_available = True
            
        except ImportError:
            self._opencog_available = False
    
    def is_available(self) -> bool:
        """Check if OpenCog is available."""
        return self._opencog_available
    
    def get_atomspace(self, agent_id: str = "default") -> Optional['AtomSpace']:
        """
        Get or create an AtomSpace for the given agent.
        
        Args:
            agent_id: Unique identifier for the agent (defaults to "default")
            
        Returns:
            AtomSpace instance or None if OpenCog is not available
        """
        if not self._opencog_available:
            return None
        
        with self._lock:
            if agent_id not in self._atomspaces:
                self._atomspaces[agent_id] = self._atomspace_class()
                # Set as default atomspace for type constructors
                self._type_constructors.set_default_atomspace(
                    self._atomspaces[agent_id]
                )
            
            # Always set the default for the current context
            self._type_constructors.set_default_atomspace(
                self._atomspaces[agent_id]
            )
            
            return self._atomspaces[agent_id]
    
    def get_types(self):
        """Get OpenCog types module."""
        return self._types if self._opencog_available else None
    
    def get_type_constructors(self):
        """Get OpenCog type constructors module."""
        return self._type_constructors if self._opencog_available else None
    
    def clear_atomspace(self, agent_id: str = "default"):
        """
        Clear the AtomSpace for a given agent.
        
        Args:
            agent_id: Unique identifier for the agent
        """
        with self._lock:
            if agent_id in self._atomspaces:
                self._atomspaces[agent_id].clear()
    
    def remove_atomspace(self, agent_id: str = "default"):
        """
        Remove the AtomSpace for a given agent.
        
        Args:
            agent_id: Unique identifier for the agent
        """
        with self._lock:
            if agent_id in self._atomspaces:
                del self._atomspaces[agent_id]
    
    def get_all_agent_ids(self):
        """Get list of all agent IDs with active AtomSpaces."""
        return list(self._atomspaces.keys())
    
    def get_stats(self):
        """Get statistics about managed AtomSpaces."""
        if not self._opencog_available:
            return {
                "opencog_available": False,
                "atomspaces": 0
            }
        
        stats = {
            "opencog_available": True,
            "atomspaces": len(self._atomspaces),
            "agents": {}
        }
        
        for agent_id, atomspace in self._atomspaces.items():
            try:
                # Get UUID if available (may not be in all OpenCog versions)
                uuid_str = str(atomspace.get_uuid()) if hasattr(atomspace, 'get_uuid') else "N/A"
            except AttributeError:
                uuid_str = "N/A"
            
            stats["agents"][agent_id] = {
                "atom_count": len(atomspace),
                "uuid": uuid_str
            }
        
        return stats


# Global singleton instance
_opencog_manager = OpenCogManager()


def get_opencog_manager() -> OpenCogManager:
    """Get the global OpenCog manager instance."""
    return _opencog_manager

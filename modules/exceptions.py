class ACRDError(Exception):
    """Base exception for ACRD errors."""


class AIError(ACRDError):
    """Errors raised by AI integration."""


class DatabaseError(ACRDError):
    """Errors raised by database operations."""


class ToolError(ACRDError):
    """Errors raised by device tooling wrappers."""

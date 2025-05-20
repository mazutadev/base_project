"""
Enums for working with commands.
"""

# Imports from standard library
from enum import Enum


# ------------------------------------
# Enums
# ------------------------------------


class CommandStatus(Enum):
    """Command statuses"""

    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    TIMEOUT = "TIMEOUT"

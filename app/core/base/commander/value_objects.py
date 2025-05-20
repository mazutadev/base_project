"""
Models for working with commands.
"""

# Imports from standard library
from dataclasses import dataclass

# Imports from enums
from .enums import CommandStatus


# ------------------------------------
# Models
# ------------------------------------


@dataclass
class CommandResult:
    """Command execution result"""

    status: CommandStatus
    stdout: str
    stderr: str
    return_code: int
    command: str

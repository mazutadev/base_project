"""
Logger models.
"""

# Imports from standard library
from dataclasses import dataclass, field
from typing import Dict, Any, List

# Imports from third party libraries
import logging


@dataclass
class LogConfig:
    """
    Log configuration.
    """

    name: str = "app"
    level: int = logging.INFO
    handlers: List[str] = field(default_factory=lambda: ["console"])
    file_config: Dict[str, Any] = field(
        default_factory=lambda: {
            "path": "logs",
            "name": "app.log",
            "max_bytes": 10 * 1024 * 1024,
            "backup_count": 5,
        }
    )
    fmt: str = None
    datefmt: str = None
    propagate: bool = False
    use_colors: bool = True

    def __post_init__(self) -> None:
        # Set file name
        if self.file_config is not None:
            self.file_config["name"] = f"{self.name}.log"

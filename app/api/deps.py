"""
Module for API dependencies.
"""

# Imports from standard library
from typing import TYPE_CHECKING

# Imports from core application
from app.core.application import get_core_application


if TYPE_CHECKING:
    # Imports from core application
    from app.core.application import CoreApplication


# Get CoreApplication instance
def get_core_application() -> "CoreApplication":
    """
    Get CoreApplication instance.
    """

    return get_core_application()

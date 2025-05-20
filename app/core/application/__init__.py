# Imports from standard library
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .application import CoreApplication


def get_core_application() -> "CoreApplication":
    """
    Get the application instance.
    """

    from .application import CoreApplication

    return CoreApplication()

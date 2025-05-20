"""
Module for dependency injection.
"""

# Imports from standard library
import os
from typing import List, TYPE_CHECKING

# Imports from third party libraries
from dependency_injector import containers, providers

# Imports from API server
from app.api.server.server import create_api_server as API

# Imports for TYPE_CHECKING
if TYPE_CHECKING:

    # Imports from third party libraries
    from logging import Logger


# Define function for finding project root directory
def _find_project_root() -> str:
    """
    Find the project root directory

    Returns:
        str: The project root directory

    Raises:
        FileNotFoundError: If .root file is not found
        in any parents directory
    """
    # Get the current working directory
    current_dir = os.getcwd()

    # Search for .root file in any parent directory
    while current_dir != os.path.dirname(current_dir):
        if ".root" in os.listdir(current_dir):
            return current_dir
        current_dir = os.path.dirname(current_dir)

    # Raise if .root file is not found
    raise FileNotFoundError(
        "Project root directory not found. Make sure .root file"
        "is present in the project root directory."
    )


# Define Logger core service
def _init_logger(configuration: providers.Configuration) -> providers.Singleton:
    """
    Initialize Singleton logger core service
    """

    # Imports from logger core service package
    from app.core.base.logger import get_logger, LogConfig

    # Register logger provider
    logger_configuration = providers.Factory(
        LogConfig,
        level=configuration.logging.level,
        handlers=configuration.logging.handlers,
        file_config=configuration.logging.file_config,
        fmt=configuration.logging.format,
        datefmt=configuration.logging.datefmt,
        use_colors=configuration.logging.use_colors,
    )

    # Create and return logger provider
    return providers.Singleton(get_logger, logger_configuration)


# Define Commander core service:
def _init_commander(
    configuration: providers.Configuration,
    logger: providers.Singleton,
) -> providers.Singleton:
    """
    Initialize Singleton commander core service
    """

    # Imports from commander core service package
    from app.core.base.commander import CommandExecutor

    # Create and return commander provider
    return providers.Singleton(
        CommandExecutor,
        logger=logger,
        timeout=configuration.commander.timeout,
    )


# Define API server core service
def _init_api_server(
    configuration: providers.Configuration,
    logger: providers.Singleton,
) -> providers.Singleton:
    """
    Initialize Singleton API server core service
    """

    # Create and return API server provider
    return providers.Singleton(
        API,
        logger=logger,
        configuration=configuration,
    )


# Define Container class
class Container(containers.DeclarativeContainer):
    """
    Base container for dependency injection
    """

    # Define project root directory
    project_root = providers.Singleton(_find_project_root)

    # Define configuration path
    configuration_path = None

    # Define scripts path
    scripts_path = None

    # Configuration provider
    configuration = providers.Configuration()

    # Singleton logger
    logger = _init_logger(configuration)

    # Singleton commander
    commander = _init_commander(configuration, logger)

    # Singleton API server
    api_server = _init_api_server(configuration, logger)

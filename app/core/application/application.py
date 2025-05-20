"""
CORE Application module.
"""

# Imports from standard library
import os
import threading
from pathlib import Path
from logging import Logger

# Imports from third party libraries
from dependency_injector import providers
from fastapi import FastAPI

# Imports from base core services
from app.core.base.container import Container
from app.core.base.commander import CommandExecutor


# Loads configuration to container configuration provider
def _load_configuration(container: Container) -> None:
    """
    Loads configuration to container configuration provider
    """

    # Define root configuration path directory
    configuration_path = Path(container.project_root()) / "config"
    container.configuration_path = configuration_path

    # Define scripts path directory
    scripts_path = Path(container.project_root()) / "app/scripts"
    container.scripts_path = scripts_path

    # Define safe load configuration function
    def safe_load_configuration(
        configuration_provider: providers.Configuration,
        path: Path,
    ) -> None:
        """
        Safe load configuration
        """
        if path.exists() and path.stat().st_size > 0:
            configuration_provider.from_yaml(path)
        else:
            raise FileNotFoundError(f"Configuration file not found: {path}")

    # Load configuration from root configuration file.yaml
    safe_load_configuration(
        container.configuration, configuration_path / "root_config/root_config.yaml"
    )

    # Load configuration to configuration provider in memory
    container.configuration.from_dict(
        {
            "application": {
                "project_root": container.project_root,
                "configuration_path": container.configuration_path,
                "scripts_path": container.scripts_path,
            }
        }
    )


def init_container() -> Container:
    """
    Initialize container
    """

    # Initialize container
    container = Container()

    # Load configuration to container configuration provider
    _load_configuration(container)

    # Return container
    return container


# Core application class
class CoreApplication(FastAPI):
    """
    Core application class
    """

    _instance: "CoreApplication" = None
    _lock: threading.Lock = threading.Lock()

    # Singleton pattern
    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls, *args, **kwargs)
                cls._instance._initialized = False

            return cls._instance

    def __init__(self, *args, **kwargs):
        if self._initialized:
            return

        # Initialize Dependency Injector container
        self._container = init_container()
        self.__inner_logger = self._container.logger().getChild("CoreApplication init")

        self.__inner_logger.info("Initializing CoreApplication")

        # Log project root path
        self.__inner_logger.info("Root project path: %s", self._container.project_root)

        # Log configuration path
        self.__inner_logger.info(
            "Configuration path: %s", self._container.configuration_path
        )
        self.__inner_logger.debug("Configuration: %s", self._container.configuration())

        # Log scripts path
        self.__inner_logger.info("Scripts path: %s", self._container.scripts_path)

        # Initialize logger
        self._logger = self._container.logger()
        self.__inner_logger.info("Logger initialized")

        # Initialize Commander
        self._commander = self._container.commander()
        self.__inner_logger.info("Commander initialized")

        # Initialize API Server
        self._api_server = self._container.api_server
        self.__inner_logger.info("API server initialized")

        # Set initialized flag
        self._initialized = True
        self.__inner_logger.info("CoreApplication initialized")

    @classmethod
    def _initialized(self) -> bool:
        return self._initialized

    @property
    def container(self) -> Container:
        return self._container

    @property
    def logger(self) -> Logger:
        return self._logger

    @property
    def commander(self) -> CommandExecutor:
        return self._commander

    @property
    def api_server(self) -> FastAPI:
        return self._api_server

"""
Module for API server.
"""

# Imports from standard library
import threading
from typing import TYPE_CHECKING

# Imports from third party libraries
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager


# Imports from local routes
from app.api.routes.root import router as root_router

if TYPE_CHECKING:
    # Imports from standard library
    import logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.core.application import get_core_application

    app_ctx = get_core_application()
    configuration = app_ctx.container.configuration.api()
    # ADDS threads for api server
    # if config["name_of_service"]:
    #     threading.Thread(target=app_ctx.name_of_service.start, daemon=True).start()
    yield


# Create FastAPI app
def create_api_server(configuration: dict, logger: "logging.Logger") -> FastAPI:
    """
    Create FastAPI app.
    """
    logger = logger.getChild("api.server")
    logger.info("Creating FastAPI app")
    api_config = configuration["api"]

    try:
        # Create FastAPI app
        app = FastAPI(lifespan=lifespan)

        # Include routers
        app.include_router(root_router, prefix="/api/v1")

        # Configs CORS
        cors_config = api_config["cors"]
        if not cors_config:
            logger.warning("CORS configuration not found, using default settings")
            cors_config = {
                "allow_origins": ["*"],
                "allow_credentials": True,
                "allow_methods": ["*"],
                "allow_headers": ["*"],
            }

        app.add_middleware(
            CORSMiddleware,
            allow_origins=cors_config["allow_origins"],
            allow_credentials=cors_config["allow_credentials"],
            allow_methods=cors_config["allow_methods"],
            allow_headers=cors_config["allow_headers"],
        )

        # Register routes

        logger.info("API server created successfully")
        return app

    except Exception as e:
        logger.error("Failed to create API server: %s", str(e))
        raise

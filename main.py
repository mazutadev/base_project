from app.core.application import get_core_application
import uvicorn


def main():
    """
    Main function
    """

    # Get core application
    APP = get_core_application()


def run_api_server():
    """
    Run API server
    """

    # Get core application
    APP = get_core_application()

    api_server = APP.api_server

    uvicorn.run(
        api_server,
        host=APP.container.configuration.api.host(),
        port=APP.container.configuration.api.port(),
    )


if __name__ == "__main__":
    run_api_server()

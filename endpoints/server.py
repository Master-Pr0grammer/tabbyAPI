import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from common.logger import UVICORN_LOG_CONFIG
from common.networking import add_request_id
from endpoints.OAI.router import router as OAIRouter

app = FastAPI(
    title="TabbyAPI",
    summary="An OAI compatible exllamav2 API that's both lightweight and fast",
    description=(
        "This docs page is not meant to send requests! Please use a service "
        "like Postman or a frontend UI."
    ),
    dependencies=[Depends(add_request_id)],
)

# ALlow CORS requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def setup_app():
    """Includes the correct routers for startup"""

    app.include_router(OAIRouter)


def export_openapi():
    """Function to return the OpenAPI JSON from the API server"""

    setup_app()
    return app.openapi()


async def start_api(host: str, port: int):
    """Isolated function to start the API server"""

    # TODO: Move OAI API to a separate folder
    logger.info(f"Developer documentation: http://{host}:{port}/redoc")
    logger.info(f"Completions: http://{host}:{port}/v1/completions")
    logger.info(f"Chat completions: http://{host}:{port}/v1/chat/completions")

    # Setup app
    setup_app()

    config = uvicorn.Config(
        app,
        host=host,
        port=port,
        log_config=UVICORN_LOG_CONFIG,
    )
    server = uvicorn.Server(config)

    await server.serve()

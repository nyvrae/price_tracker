import sys
import logging
from contextlib import asynccontextmanager

from uvicorn import Config, Server
from fastapi import FastAPI

if sys.platform == "win32":
    from asyncio.windows_events import ProactorEventLoop
    import asyncio

from .db import init_db
from .routers import products, auth, dashboard

from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application starting up...")
    init_db()
    logger.info("Database initialized")
    yield
    logger.info("Application shutting down...")

app = FastAPI(
    lifespan=lifespan,
    title="Price Tracker API",
    version="1.0.0",
    description="API for tracking product prices."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Price Tracker API is running"}

app.include_router(products.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(dashboard.router, prefix="/api/v1")

if __name__ == "__main__":
    logger.info("Starting server directly from main.py")
    config = Config(app=app, host="0.0.0.0", port=8000, reload=True)

    if sys.platform == "win32":
        class ProactorServer(Server):
            def run(self, sockets=None):
                loop = ProactorEventLoop()
                asyncio.set_event_loop(loop)
                logger.info("Running with ProactorEventLoop on Windows")
                asyncio.run(self.serve(sockets=sockets))
        server = ProactorServer(config=config)
    else:
        server = Server(config=config)
        logger.info("Running with default Uvicorn server")

    server.run()
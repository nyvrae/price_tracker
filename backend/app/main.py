import sys
import asyncio
import logging
from contextlib import asynccontextmanager

from uvicorn import Config, Server

if sys.platform == "win32":
    from asyncio.windows_events import ProactorEventLoop

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from typing import List

from .parsers import AmazonParser
from .db import init_db, get_db
from .services import save_products
from . import models
from . import schemas

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application starting up...")
    init_db()
    logger.info("Database initialized")
    yield
    logger.info("Application shutting down...")

app = FastAPI(lifespan=lifespan, title="Price Tracker API", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Price Tracker API is running"}

@app.get("/search")
async def search(query: str, pages: int = 3, db: Session = Depends(get_db)):
    logger.info(f"Starting search for query: '{query}'")
    try:
        async with AmazonParser(search_query=query, max_pages=pages) as parser:
            results = await parser.run()

        if not results:
            logger.warning(f"No results found for query: '{query}'")
            return {"status": "no_results"}

        save_products(db, results)
        logger.info(f"Found and saved {len(results)} results for query: '{query}'.")
        return {"status": "success", "results_count": len(results)}

    except Exception as e:
        logger.error(f"An error occurred during search for query '{query}': {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An internal error occurred during scraping.")

@app.get("/products", response_model=List[schemas.Product])
def get_products_list(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products

@app.get("/products/{product_id}/prices", response_model=List[schemas.Price])
def get_product_prices_list(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product.prices

if sys.platform == "win32":
    class ProactorServer(Server):
        def run(self, sockets=None):
            loop = ProactorEventLoop()
            asyncio.set_event_loop(loop)
            logger.info("Running with ProactorEventLoop on Windows")
            asyncio.run(self.serve(sockets=sockets))

if __name__ == "__main__":
    logger.info("Starting server directly from main.py")
    
    config = Config(app=app, host="0.0.0.0", port=8000, reload=True)

    if sys.platform == "win32":
        server = ProactorServer(config=config)
    else:
        server = Server(config=config)
        logger.info("Running with default Uvicorn server")

    server.run()

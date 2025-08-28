import asyncio
import logging
from fastapi import FastAPI, HTTPException, Depends
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from app.parsers import AmazonParser
from app.db import init_db, SessionLocal
from app.services import save_products
from app.models import Product, Price

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    logger.info("Database initialized")
    yield
    logger.info("Application shutdown")

app = FastAPI(lifespan=lifespan, title="Price Tracker API", version="1.0.0")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Price Tracker API is running"}

@app.get("/search")
async def search(query: str, pages: int = 3):
    async with AmazonParser(search_query=query, max_pages=pages) as parser:
        try:
            results = await parser.run()
            if results:
                session = SessionLocal()
                save_products(session, results)
                session.close()

                logger.info(f"Found {len(results)} results. Data saved to database.")
                return {"status": "success", "results_count": len(results)}
            else:
                logger.warning("No results found.")
                return {"status": "no_results"}
        except Exception as e:
            logger.error(f"Error during search: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/products")
async def get_products(db: Session = Depends(get_db)):
    try:
        products = db.query(Product).all()
        return {"products": [{"id": p.id, "title": p.title, "url": p.url, "image_url": p.image_url} for p in products]}
    except Exception as e:
        logger.error(f"Error getting products: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/products/{product_id}/prices")
async def get_product_prices(product_id: int, db: Session = Depends(get_db)):
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        prices = db.query(Price).filter(Price.product_id == product_id).order_by(Price.date.desc()).all()
        return {
            "product": {"id": product.id, "title": product.title, "url": product.url},
            "prices": [{"price": float(p.price), "date": p.date.isoformat(), "site": p.site} for p in prices]
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting product prices: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def main():
    init_db()
    logger.info("Database initialized")
    
    query = input("Enter a search query: ")
    await search(query)

if __name__ == "__main__":
    asyncio.run(main())

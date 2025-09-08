import logging
from typing import List, Optional
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session

from .. import models, schemas, crud
from ..db import get_db, SessionLocal
from ..parsers import AmazonParser
from ..services import save_products

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

async def run_parsing_and_save(query: str, pages: int):
    logger.info(f"Background task started for query: '{query}'")
    db: Session = SessionLocal()
    try:
        async with AmazonParser(search_query=query, max_pages=pages) as parser:
            results = await parser.run()
        if results:
            save_products(db, results)
            logger.info(f"Background task finished. Saved {len(results)} results for query: '{query}'.")
        else:
            logger.warning(f"No results found in background for query: '{query}'")
    except Exception as e:
        logger.error(f"Error in background task for query '{query}': {e}", exc_info=True)
    finally:
        db.close()
        logger.info(f"Database session closed for background task query: '{query}'")

@router.get("/all", response_model=List[schemas.Product])
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products

@router.post("/search", status_code=202)
async def start_products_search(
    query: str,
    background_tasks: BackgroundTasks,
    pages: int = Query(3, ge=1, le=10),
):
    logger.info(f"Adding search task for query: '{query}' to background.")
    background_tasks.add_task(run_parsing_and_save, query, pages)
    return {"status": "accepted", "message": "Parsing task started in the background."}


@router.get("/filter", response_model=List[schemas.Product])
def get_filtered_products(
    title: Optional[str] = None,
    min_price: Optional[Decimal] = None,
    max_price: Optional[Decimal] = None,
    sort_by_price: Optional[str] = Query(None, description="asc or desc", regex="^(asc|desc)$"),
    db: Session = Depends(get_db)
):
    products = crud.search_products(
        db=db,
        title=title,
        min_price=min_price,
        max_price=max_price,
        sort_by_price=sort_by_price
    )
    return products


@router.get("/{product_id}/prices", response_model=List[schemas.Price])
def get_product_prices_history(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product.prices
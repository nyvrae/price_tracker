from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from decimal import Decimal

from ..db import get_db

from ..services import get_current_user
from .. import models, schemas, crud
from app.core.celery_app import celery_app
from app.tasks.update_prices import update_product_price

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
    dependencies=[Depends(get_current_user)]
)

@router.get("/products", response_model=List[schemas.Product])
async def get_dashboard_products(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    user_products = db.query(models.UserProducts).filter(
        models.UserProducts.user_id == current_user.id
    ).all()
    
    products = [up.product for up in user_products]
    return products

@router.post("/products", response_model=schemas.Product)
async def add_product_to_dashboard(
    product_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    existing = db.query(models.UserProducts).filter(
        models.UserProducts.user_id == current_user.id,
        models.UserProducts.product_id == product_id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=400, 
            detail="Product already in dashboard"
        )
    
    user_product = models.UserProducts(
        user_id=current_user.id,
        product_id=product_id
    )
    
    try:
        celery_app.send_task("app.tasks.update_prices.update_product_price", args=[product_id])
    except Exception:
        pass
    
    db.add(user_product)
    db.commit()
    db.refresh(user_product)

    return user_product.product

@router.delete("/products/{product_id}", status_code=204)
async def remove_product_from_dashboard(
    product_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    exists = db.query(models.UserProducts).filter(
        models.UserProducts.user_id == current_user.id,
        models.UserProducts.product_id == product_id
    ).first()
    
    if not exists:
        raise HTTPException(
            status_code=400,
            detail="Product doesn't exist in dashboard"
        )
    db.delete(exists)
    db.commit()
    
    return "Item removed from dashboard"

@router.get("/compare", response_model=List[schemas.ProductWithPrices])
async def compare_products(
    product_id: List[int] = Query(..., description="List of product IDs to compare"),
    db: Session = Depends(get_db)
):
    pass

@router.get("/products/{product_id}/history", response_model=List[schemas.Price])
async def get_product_price_history(
    product_id: int,
    db: Session = Depends(get_db),
):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return product.prices

@router.get("/filter", response_model=List[schemas.Product])
def get_filtered_products(
    title: Optional[str] = None,
    min_price: Optional[Decimal] = None,
    max_price: Optional[Decimal] = None,
    sort_by_price: Optional[str] = Query(None, description="asc or desc", regex="^(asc|desc)$"),
    db: Session = Depends(get_db)
):
    pass

@router.patch("/products/{product_id}/favorite", response_model=schemas.Product)
async def toggle_favorite(
    product_id: int,
    favorite: bool,
    db: Session = Depends(get_db)
):
    pass
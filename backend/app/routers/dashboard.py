from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, models
from ..db import get_db

# Представим, что у вас есть функция для получения текущего пользователя по токену
# from ..auth import get_current_user 

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
    # dependencies=[Depends(get_current_user)] # Раскомментируйте, когда будет готова аутентификация
)

@router.get("/products", response_model=List[schemas.Product])
async def get_dashboard_products(db: Session = Depends(get_db)):
    pass

@router.post("/products", response_model=schemas.Product)
async def add_product_to_dashboard(product_id: int, db: Session = Depends(get_db)):
    pass

@router.delete("/products/{product_id}", status_code=204)
async def remove_product_from_dashboard(product_id: int, db: Session = Depends(get_db)):
    pass

@router.get("/compare", response_model=List[schemas.ProductWithPrices])
async def compare_products(
    product_ids: List[int] = Query(..., description="List of product IDs to compare"),
    db: Session = Depends(get_db)
):
    pass
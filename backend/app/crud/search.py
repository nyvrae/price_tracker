from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from decimal import Decimal
from ..models import Product, Price

def search_products(
    db: Session,
    title: Optional[str] = None,
    min_price: Optional[Decimal] = None,
    max_price: Optional[Decimal] = None,
    sort_by_price: Optional[str] = None
) -> List[Product]:

    query = db.query(Product)

    if title:
        query = query.filter(Product.title.ilike(f"%{title}%"))

    subq = (
        db.query(
            Price.product_id,
            func.max(Price.date).label("latest_date")
        )
        .group_by(Price.product_id)
        .subquery()
    )

    latest_prices = db.query(Price).join(
        subq,
        (Price.product_id == subq.c.product_id) & (Price.date == subq.c.latest_date)
    ).subquery()

    query = query.join(latest_prices, Product.id == latest_prices.c.product_id)

    if min_price is not None:
        query = query.filter(latest_prices.c.price >= min_price)
    if max_price is not None:
        query = query.filter(latest_prices.c.price <= max_price)

    if sort_by_price == "asc":
        query = query.order_by(latest_prices.c.price.asc())
    elif sort_by_price == "desc":
        query = query.order_by(latest_prices.c.price.desc())

    return query.all()

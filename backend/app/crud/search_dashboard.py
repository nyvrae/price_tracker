from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from decimal import Decimal
from ..models import Product, Price, UserProducts, User


def search_dashboard_products(
    db: Session,
    user_id: int,
    title: Optional[str] = None,
    min_price: Optional[Decimal] = None,
    max_price: Optional[Decimal] = None,
    sort_by_price: Optional[str] = None,
    only_favorites: bool = False
) -> List[Product]:
    query = (
        db.query(Product)
        .join(UserProducts, UserProducts.product_id == Product.id)
        .filter(UserProducts.user_id == user_id)
    )

    if only_favorites:
        query = query.filter(UserProducts.favorite == True)

    if title:
        query = query.filter(Product.title.ilike(f"%{title}%"))

    subq = (
        db.query(
            Price.product_id,
            func.max(Price.created_at).label("latest_date")
        )
        .group_by(Price.product_id)
        .subquery()
    )

    latest_prices = db.query(Price).join(
        subq,
        (Price.product_id == subq.c.product_id) & (Price.created_at == subq.c.latest_date)
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

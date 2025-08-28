import logging
from sqlalchemy.orm import Session
from decimal import Decimal
from app.models.product import Product, Price
import re

logger = logging.getLogger(__name__)

def parse_price(price_str: str) -> Decimal:
    try:
        clean_str = re.sub(r"[^\d.]", "", price_str)
        return Decimal(clean_str) if clean_str else Decimal("0.00")
    except Exception as e:
        logger.warning(f"Failed to parse price '{price_str}': {e}")
        return Decimal("0.00")

def save_products(session: Session, products: list[dict]):
    try:
        saved_count = 0
        for p in products:
            try:
                product = session.query(Product).filter_by(url=p["url"]).first()
                if not product:
                    product = Product(
                        title=p["title"], 
                        url=p["url"], 
                        image_url=p.get("image_url", "")
                    )
                    session.add(product)
                    session.flush()
                    logger.info(f"Added new product: {p['title'][:50]}...")

                price_value = parse_price(p["price"])
                if price_value > 0:
                    price = Price(
                        product_id=product.id, 
                        site="amazon.com", 
                        price=price_value
                    )
                    session.add(price)
                    saved_count += 1
                else:
                    logger.warning(f"Skipping product with zero price: {p['title'][:50]}...")
                    
            except Exception as e:
                logger.error(f"Error saving product {p.get('title', 'Unknown')}: {e}")
                continue
        
        session.commit()
        logger.info(f"Successfully saved {saved_count} price records")
        
    except Exception as e:
        logger.error(f"Error in save_products: {e}")
        session.rollback()
        raise

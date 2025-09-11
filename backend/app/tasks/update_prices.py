from app.core.celery_app import celery_app
from app.db import SessionLocal
from app import models
from app.parsers import AmazonParser
import asyncio

@celery_app.task(name="app.tasks.update_prices.update_product_price")
def update_product_price(product_id: int):
    async def main():
        db = SessionLocal()
        try:
            product = db.query(models.Product).filter(models.Product.id == product_id).first()
            if not product:
                return {"status": "error", "message": "Product not found"}

            async with AmazonParser(search_query=product.title, max_pages=1) as parser:
                prices = await parser.run()

            if prices:
                first_result = prices[0]
                price_value_str = first_result.get("price")
                if price_value_str and isinstance(price_value_str, str):
                    cleaned_price = ''.join(filter(lambda x: x.isdigit() or x in '.,', price_value_str.replace(',', '.')))
                    if cleaned_price:
                        price = models.Price(
                            product_id=product.id,
                            site="Amazon",
                            price=cleaned_price
                        )
                        db.add(price)
                        db.commit()
            return {"status": "success", "product_id": product_id}
        finally:
            db.close()

    return asyncio.run(main())


@celery_app.task(name="app.tasks.update_prices.update_all_products")
def update_all_products():
    db = SessionLocal()
    try:
        products = db.query(models.Product).all()
        for product in products:
            update_product_price.delay(product.id)
        return {"status": "queued", "count": len(products)}
    finally:
        db.close()

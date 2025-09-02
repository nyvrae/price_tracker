from sqlalchemy.orm import Session
from playwright.async_api import async_playwright

from app.models import Price, Product

async def update_prices(db: Session, limit: int = 10):
    products = db.query(Product).all()
    
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.amazon.com/")
        
        for product in products[:limit]:
            price = await fetch_price(page, product_url)
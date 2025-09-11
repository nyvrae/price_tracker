from sqlalchemy.orm import Session
from playwright.async_api import async_playwright

from app.models import Price, Product

async def update_prices(db: Session, limit: int = 10):
    products = db.query(Product).all()
    
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        if browser is None:
            raise RuntimeError("Не удалось запустить Chromium")
        page = await browser.new_page()
        if page is None:
            raise RuntimeError("Не удалось создать страницу")
        await page.goto("https://www.amazon.com/")

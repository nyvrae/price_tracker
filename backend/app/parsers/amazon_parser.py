import asyncio
import json
import logging
import random
from typing import List, Dict, Optional

from playwright.async_api import async_playwright, Browser, BrowserContext, Page, Locator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AmazonParser:
    BASE_URL = "https://www.amazon.com"
    SEARCH_BAR_SELECTOR = "input#twotabsearchtextbox"
    LISTITEM_SELECTOR = 'div.s-main-slot div[data-component-type="s-search-result"]'
    NEXT_BTN_SELECTOR = "a.s-pagination-next:not(.s-pagination-disabled)"
    COOKIES_FILE = "app/data/amazon_cookies.json"

    def __init__(self, search_query: str, max_pages: int = 3, headless: bool = True):        
        self.search_query = search_query
        self.max_pages = max_pages
        self.headless = headless
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
    
    async def __aenter__(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)
        self.context = await self.browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/237.84.2.178 Safari/537.36",
            locale="en-US",
            java_script_enabled=True,
            viewport={"width": 1920, "height": 1080},
        )
        
        try:
            with open(self.COOKIES_FILE, "r") as f:
                cookies = json.load(f)
            await self.context.add_cookies(cookies)
            logger.info("Cookies uploaded")
        except FileNotFoundError:
            logger.info("Cookies not found, continue without them")

        self.page = await self.context.new_page()
        return self
    
    async def _extract_item(self, item: Locator) -> Optional[Dict[str, str]]:
        title_el = item.locator("h2.a-size-medium.a-spacing-none.a-color-base.a-text-normal")
        title = await title_el.inner_text() if await title_el.count() else ""
        if not title:
            return None
        
        link_el = item.locator("a.a-link-normal.s-line-clamp-2.s-link-style.a-text-normal")
        relative_url = await link_el.get_attribute("href") if await link_el.count() else ""
        url = f"{self.BASE_URL}{relative_url}" if relative_url else "N/A"

        image_el = item.locator("img.s-image").first
        image_url = await image_el.get_attribute("src") if await image_el.count() else "N/A"
        
        price = "N/A"
        if await item.locator("span.a-price span.a-offscreen").count():
            price = await item.locator("span.a-price span.a-offscreen").first.inner_text()
        elif await item.locator("span.a-price-whole").count():
            whole = await item.locator("span.a-price-whole").first.inner_text()
            fraction = await item.locator("span.a-price-fraction").first.inner_text() if await item.locator("span.a-price-fraction").count() else "00"
            price = f"${whole}.{fraction}"

        return {
            "title": title.strip(),
            "image_url": image_url.strip() if image_url else "",
            "price": price.strip() if price else None,
            "url": url.strip()
        }

    async def run(self) -> List[Dict[str, str]]:
        logger.info(f"Start parsing using query: '{self.search_query}'")
        try:
            await self.page.goto(self.BASE_URL, timeout=60000)
            await self.page.wait_for_selector(self.SEARCH_BAR_SELECTOR, timeout=30000)
        except TimeoutError:
            error_file = "error_screenshot.png"
            await self.page.screenshot(path=error_file, full_page=True)
            logger.error(f"Failed to find search bar. Amazon might be showing a CAPTCHA. See {error_file}")
        except Exception as e:
            logger.error(f"Failed to open Amazon: {e}")
            return []

        await self.page.locator(self.SEARCH_BAR_SELECTOR).fill(self.search_query)
        await self.page.keyboard.press("Enter")
        await self.page.wait_for_load_state('domcontentloaded')
        await asyncio.sleep(random.uniform(2, 5))

        all_results = []
        for page_num in range(1, self.max_pages + 1):
            logger.info(f"Collecting data from page {page_num}...")
            try:
                await self.page.wait_for_selector(self.LISTITEM_SELECTOR, timeout=30000)
            except TimeoutError:
                error_file = f"error_page_{page_num}.png"
                await self.page.screenshot(path=error_file, full_page=True)
                logger.warning(f"Could not find items on page {page_num}. Possibly the end or a CAPTCHA. See {error_file}")
                break
            
            count = await self.page.locator(self.LISTITEM_SELECTOR).count()
            logger.info(f"Items on page: {count}")
            
            items = await self.page.locator(self.LISTITEM_SELECTOR).all()
            tasks = [self._extract_item(item) for item in items]
            results = [r for r in await asyncio.gather(*tasks) if r]
            all_results.extend(results)
            
            if page_num < self.max_pages:
                next_button = self.page.locator(self.NEXT_BTN_SELECTOR)
                if await next_button.count() > 0:
                    await next_button.click()
                    await self.page.wait_for_load_state('domcontentloaded')
                    await asyncio.sleep(random.uniform(2, 5))
                else:
                    logger.info("No next btn found.")
                    break

        return all_results

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            cookies = await self.context.cookies()
            with open(self.COOKIES_FILE, "w") as f:
                json.dump(cookies, f)
                logger.info("Cookies saved")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")

        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        logger.info("Playwright stopped.")

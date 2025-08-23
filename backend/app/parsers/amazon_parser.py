import asyncio
from playwright.async_api import async_playwright

import json
import random

async def extract_item(item):
    title_el = item.locator("h2.a-size-medium.a-spacing-none.a-color-base.a-text-normal")
    title = await title_el.inner_text() if await title_el.count() else ""

    image_el = item.locator("img.s-image").first  
    image_url = await image_el.get_attribute("src") if await image_el.count() else ""
    
    price_el = item.locator("span.a-price span.a-offscreen")
    price = await price_el.inner_text() if await price_el.count() else ""

    if title:
        return {
            "title": title.strip(),
            "image_url": image_url.strip() if image_url else "",
            "price": price.strip(),
        }
    return None

async def parse_amazon(search_query: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/237.84.2.178 Safari/537.36"
        )
        page = await browser.new_page()

        try:
            await page.goto("https://www.amazon.com/")
            await page.wait_for_selector('input#twotabsearchtextbox')
        except:
            print("Failed to open Amazon")
            await browser.close()
            return []

        await page.locator("#twotabsearchtextbox").fill(search_query)
        await page.keyboard.press("Enter")
                
        last_height = await page.evaluate("document.body.scrollHeight")
        for _ in range(5):
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await asyncio.sleep(random.uniform(1, 2))
            new_height = await page.evaluate("document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
        await page.wait_for_selector('div.s-main-slot div[data-component-type="s-search-result"]', timeout=30000)
        items = await page.locator('div.s-main-slot div[data-component-type="s-search-result"]').all()
        
        tasks = [extract_item(item) for item in items]
        results =  [r for r in await asyncio.gather(*tasks) if r]

        await browser.close()
        return results

async def main():
    user_input = input("Enter a search query: ")
    results = await parse_amazon(user_input)
    
    if results:
        with open("amazon_results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
        
        print(f"Find {len(results)} results")
    
    else:
        print("No results found")

if __name__ == "__main__":
    asyncio.run(main())

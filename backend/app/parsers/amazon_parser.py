import asyncio
from playwright.async_api import async_playwright

async def parse_amazon(search_query: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto("https://www.amazon.com/")
        await page.locator("#twotabsearchtextbox").fill(search_query)
        await page.keyboard.press("Enter")
        
        await page.wait_for_load_state("networkidle")
        
        last_height = await page.evaluate("document.body.scrollHeight")
        for _ in range(5):
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await asyncio.sleep(1)
            new_height = await page.evaluate("document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
        await page.wait_for_selector('div.s-main-slot div.s-result-item[role="listitem"]')

        items = await page.locator('div.s-main-slot div.s-result-item[role="listitem"]').all()
        

        
        results = []

        for item in items:
            title_el = item.locator("h2.a-size-medium.a-spacing-none.a-color-base.a-text-normal")
            title = await title_el.inner_text() if await title_el.count() else ""

            image_el = item.locator("img.s-image").first  
            image_url = await image_el.get_attribute("src") if await image_el.count() else ""

            price_whole = item.locator("span.a-price-whole")
            price_fraction = item.locator("span.a-price-fraction")
            price = ""
            if await price_whole.count():
                whole = (await price_whole.inner_text()).replace("\n.", "").replace(",", "")
                fraction = (await price_fraction.inner_text()).replace("\n", "") if await price_fraction.count() else "00"
                price = f"{whole}.{fraction}"

            if title:
                results.append({
                    "title": title.strip(),
                    "image_url": image_url.strip(),
                    "price": price.strip(),
                })

        
        for r in results:
            print(r)

        await browser.close()


if __name__ == "__main__":
    user_input = input("Введите товар для поиска на Amazon: ")
    asyncio.run(parse_amazon(user_input))

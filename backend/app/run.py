import asyncio
import logging
from app.db import init_db, SessionLocal
from app.parsers import AmazonParser
from app.services import save_products

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

async def cli_mode():
    init_db()
    logger.info("Database initialized")

    query = input("Enter a search query: ")
    async with AmazonParser(search_query=query, max_pages=3) as parser:
        results = await parser.run()
        if results:
            session = SessionLocal()
            save_products(session, results)
            session.close()
            logger.info(f"Saved {len(results)} products to DB")
        else:
            logger.warning("No results found.")

if __name__ == "__main__":
    asyncio.run(cli_mode())

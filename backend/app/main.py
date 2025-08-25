import asyncio
import json
import logging
from fastapi import FastAPI
from app.parsers import AmazonParser

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/search")
async def search(query: str, pages: int = 3):
    async with AmazonParser(search_query=query, max_pages=pages) as parser:
        try:
            results = await parser.run()
            if results:
                output_file = "amazon_results.json"
                with open("app/data/" + output_file, "w", encoding="utf-8") as f:
                    json.dump(results, f, ensure_ascii=False, indent=4)
                logger.info(f"Found {len(results)} results. Data saved to {output_file}")
                return {"status": "success", "results_count": len(results), "file": output_file}
            else:
                logger.warning("No results found.")
                return {"status": "no_results"}
        except Exception as e:
            logger.error(f"Error during search: {e}", exc_info=True)
            return {"status": "error", "message": str(e)}

async def main():
    query = input("Enter a search query: ")
    await search(query)

if __name__ == "__main__":
    asyncio.run(main())

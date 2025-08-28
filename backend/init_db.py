#!/usr/bin/env python3
"""
Скрипт для инициализации базы данных
"""
import logging
from app.db import init_db

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def main():
    logger.info("Initializing database...")
    init_db()
    logger.info("Database initialized successfully!")

if __name__ == "__main__":
    main()

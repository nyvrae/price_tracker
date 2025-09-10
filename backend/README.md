# Price Tracker Backend

Backend API for tracking prices of products on Amazon.

## Installation

1.  Make sure you have **Python 3.13+** and **Poetry** installed.
2.  Install the dependencies:

```bash
poetry install
```

3.  Install the browsers for Playwright:

```bash
poetry run playwright install chromium
```

---

## Running the Application

### Running the Development Server

```bash
poetry run python run.py
```

```bash
docker compose up --build
```

Or run directly with uvicorn:

```bash
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Running in Production

```bash
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Running Product Search (Console Mode)

```bash
poetry run python -m app.main
```

---

## API Endpoints

- `GET /` - Check API status.
- `GET /search?query={query}&pages={pages}` - Search for products on Amazon.
- `GET /products` - Get all products from the database.
- `GET /products/{product_id}/prices` - Get the price history for a specific product.
- ...

---

## Usage Examples

### Searching for Products

```bash
curl "http://localhost:8000/search?query=laptop&pages=2"
```

### Getting All Products

```bash
curl "http://localhost:8000/products"
```

### Getting Price History

```bash
curl "http://localhost:8000/products/1/prices"
```

---

## Environment variables

Create a `.env` file in `backend/` (or copy from `.env.example`) and adjust values. Docker Compose will load it automatically.

Defaults for local Docker:

- `CELERY_BROKER_URL=redis://redis:6379/0`
- `CELERY_RESULT_BACKEND=redis://redis:6379/1`
- `REDIS_HOST=redis`

## Run with Docker

Build and start API, Redis, Celery worker/beat, and Flower:

```bash
cd backend
docker compose up -d --build
```

Open Flower at http://localhost:5555

Follow logs:

```bash
docker compose logs -f backend celery_worker celery_beat
```

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py             # FastAPI application
│   ├── db.py               # Database settings
│   ├── models/             # SQLAlchemy models
│   ├── parsers/            # Website parsers
│   ├── services/           # Business logic
│   └── data/               # Data (cookies, results)
├── logs/                   # Application logs
├── run.py                  # Server startup script
├── init_db.py              # DB initialization script
├── pyproject.toml          # Poetry dependencies
└── README.md
```

---

## Database

The application uses an SQLite database named `price_tracker.db`. The database is automatically created on the first run.

### Data Models

- **Product**: Stores product information (name, URL, image).
- **Price**: Stores product prices (price, date, website).

### Database Initialization

The database is automatically initialized when:

- The FastAPI server starts.
- Console mode is run (`python -m app.main`).
- The `python init_db.py` script is run manually.

---

## Logging

Logs are saved to the `logs/` folder and also output to the console.

---

## Troubleshooting

### "no such table: products" Error

If you encounter a missing tables error, run:

```bash
poetry run python init_db.py
```

### Playwright Issues

If you have issues with the browser, try reinstalling it:

```bash
poetry run playwright install chromium
```

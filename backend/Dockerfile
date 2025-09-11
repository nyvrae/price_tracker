FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    curl \
    wget \
    unzip \
    libnss3 \
    libnspr4 \
    libgbm1 \
    libatk-bridge2.0-0 \
    libdrm2 \
    libcups2 \
    libdbus-1-3 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libxtst6 \
    libexpat1 \
    libxcb1 \
    libxkbcommon0 \
    libasound2 \
    fonts-liberation \
    libgtk-3-0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN groupadd -r appuser && useradd -r -g appuser -u 1000 appuser

ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

RUN mkdir -p /ms-playwright && chown -R appuser:appuser /ms-playwright

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install playwright \
    && playwright install --with-deps chromium

COPY . .

RUN mkdir -p /celerybeat_data && chown -R appuser:appuser /app /celerybeat_data

USER appuser

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

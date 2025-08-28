# Price Tracker Backend

Backend API для отслеживания цен товаров с Amazon.

## Установка

1. Убедитесь, что у вас установлен Python 3.13+ и Poetry
2. Установите зависимости:
```bash
poetry install
```

3. Установите браузеры для Playwright:
```bash
poetry run playwright install chromium
```

4. Инициализируйте базу данных:
```bash
poetry run python init_db.py
```

## Запуск

### Запуск сервера разработки
```bash
poetry run python run.py
```

Или с uvicorn напрямую:
```bash
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Запуск в продакшене
```bash
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Запуск поиска товаров (консольный режим)
```bash
poetry run python -m app.main
```

## API Endpoints

- `GET /` - Проверка статуса API
- `GET /search?query={query}&pages={pages}` - Поиск товаров на Amazon
- `GET /products` - Получить все товары из базы данных
- `GET /products/{product_id}/prices` - Получить историю цен для товара

## Примеры использования

### Поиск товаров
```bash
curl "http://localhost:8000/search?query=laptop&pages=2"
```

### Получение всех товаров
```bash
curl "http://localhost:8000/products"
```

### Получение истории цен
```bash
curl "http://localhost:8000/products/1/prices"
```

## Структура проекта

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI приложение
│   ├── db.py            # Настройки базы данных
│   ├── models/          # SQLAlchemy модели
│   ├── parsers/         # Парсеры для сайтов
│   ├── services/        # Бизнес-логика
│   └── data/            # Данные (cookies, результаты)
├── logs/                # Логи приложения
├── run.py               # Скрипт запуска сервера
├── init_db.py           # Скрипт инициализации БД
├── pyproject.toml       # Зависимости Poetry
└── README.md
```

## База данных

Приложение использует SQLite базу данных `price_tracker.db`. База создается автоматически при первом запуске.

### Модели данных

- **Product**: Товары (название, URL, изображение)
- **Price**: Цены товаров (цена, дата, сайт)

### Инициализация базы данных

База данных автоматически инициализируется при:
- Запуске FastAPI сервера
- Запуске консольного режима (`python -m app.main`)
- Ручном запуске `python init_db.py`

## Логирование

Логи сохраняются в папку `logs/` и выводятся в консоль.

## Устранение неполадок

### Ошибка "no such table: products"
Если возникает ошибка с отсутствующими таблицами, выполните:
```bash
poetry run python init_db.py
```

### Проблемы с Playwright
Если возникают проблемы с браузером, переустановите:
```bash
poetry run playwright install chromium
```

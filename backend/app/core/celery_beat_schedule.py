from datetime import timedelta
from .celery_app import celery_app

celery_app.conf.beat_schedule = {
    "update-all-products-daily": {
        "task": "app.tasks.update_prices.update_all_products",
        "schedule": timedelta(days=1),
        "args": (),
    },
}

web: daphne Gemini_API.asgi:application --port 8000 --bind 0.0.0.0 -v2
celery: celery -A Gemini_API.celery worker -l info

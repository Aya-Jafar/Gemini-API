web: daphne daphne Gemini_API.asgi.asgi:channel_layer --port 8000 --bind 0.0.0.0 -v2
worker: python manage.py runworker -v2
celery: celery -A Gemini_API.settings worker -l info

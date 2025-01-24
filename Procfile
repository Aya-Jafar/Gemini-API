web: uvicorn Gemini_API.asgi:application --host 0.0.0.0 --port 8000 --workers 4
worker: python manage.py runworker -v2
celery: celery -A Gemini_API.settings worker -l info

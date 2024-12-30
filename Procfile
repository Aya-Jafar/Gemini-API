web: daphne -b 0.0.0.0 -p 8000 Gemini_API.asgi:application
worker: python manage.py runworker chatbot
celery: celery -A Gemini_API worker --loglevel=info

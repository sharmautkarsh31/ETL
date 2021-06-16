release: python manage.py migrate
web: gunicorn config.wsgi:application --timeout 5000 --keep-alive 5 --log-level debug
worker: celery worker --app=config.celery_app --loglevel=info --concurrency=4 -P gevent

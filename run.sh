nginx -g 'daemon on;'
gunicorn --bind=0.0.0.0:8000 application:app

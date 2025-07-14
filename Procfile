web: python manage.py migrate && python manage.py collectstatic --noinput && gunicorn --bind 0.0.0.0:$PORT mpls.wsgi:application --workers 1 --timeout 300 --log-level debug

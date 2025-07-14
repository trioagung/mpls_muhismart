web: python manage.py migrate && python manage.py createcachetable && python manage.py collectstatic --noinput && gunicorn --bind 0.0.0.0:$PORT mpls.wsgi:application --workers 2 --timeout 120

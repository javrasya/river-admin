release: python manage.py migrate && python manage.py bootstrap_shipping_example && python manage.py bootstrap_issue_tracker_example && python manage.py bootstrap_river_admin_demo
web: gunicorn demo.wsgi

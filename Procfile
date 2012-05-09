web: python penncycle/manage.py run_gunicorn -b "0.0.0.0:$PORT" -w 3
worker: python penncycle/manage.py celeryd -E -B --loglevel=INFO

apt-get install libgomp1 &
python manage.py process_tasks &
gunicorn --bind=0.0.0.0 --timeout 600 PlantDBBrowser.wsgi --access-logfile '-' --error-logfile '-'

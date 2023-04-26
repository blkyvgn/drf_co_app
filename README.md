$ mkdir log media static log cache locale\
$ touch .env\
(SECRET_KEY,DEBUG...)

# commands
$ py manage.py migrate\
$ py manage.py collectstatic\
$ py manage.py createsuperuser

# celery
$ celery -A ecomm worker -l info

web: gunicorn -b :$PORT -e DEBUG=0 --log-file - project.wsgi
runserver: DEBUG=1 python manage.py runserver 0.0.0.0:$PORT --insecure
migrate: python manage.py makemigrations -e nav pages news && python manage.py migrate
collectstatic: python manage.py collectstatic --noinput
makeprod: npm run prod && honcho start collectstatic && honcho start migrate
env: ./ansible/prepare-env.sh

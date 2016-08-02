web: gunicorn -w 4 -b :$PORT -e DEBUG=0 --log-file - project.wsgi
runserver: DEBUG=1 python manage.py runserver 0.0.0.0:$WEB_PORT
devserver: node webpack/server.js --inline --hot
migrate: python manage.py makemigrations -e nav nodes news && python manage.py migrate
collectstatic: python manage.py collectstatic --noinput
makeprod: npm run prod && honcho start collectstatic && honcho start migrate
env: ./ansible/prepare-env.sh

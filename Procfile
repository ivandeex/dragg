runserver: DEBUG=1 python manage.py runserver 0.0.0.0:$PORT --insecure
migrate: python manage.py makemigrations -e nav pages news && python manage.py migrate
env: ./ansible/prepare-env.sh

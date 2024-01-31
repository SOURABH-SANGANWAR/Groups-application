docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d


docker-compose exec main_server python manage.py migrate

docker-compose exec sub_server_ind python manage.py migrate


docker-compose exec sub_server_us python manage.py migrate


docker-compose exec sub_server_eu python manage.py migrate


docker-compose exec sub_server_africa python manage.py migrate


docker-compose exec sub_server_china python manage.py migrate

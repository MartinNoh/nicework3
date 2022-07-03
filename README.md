env : python3.6, docker20.10.7, docker-compose1.29.2

--------------------------------------------------------------------------

container up
```
$ docker-compose -f docker-compose.prod.yml up --build -d
$ docker-compose -f docker-compose.prod.yml up -d
```

container down
```
$ docker-compose -f docker-compose.prod.yml down -v
$ docker-compose -f docker-compose.prod.yml down
```

container logs
```
$ docker-compose -f docker-compose.prod.yml logs -f
```

docker-compose.yml과 init-letsencrypt.sh 파일은 ssl 인증서 발급을 위한 것.  
docker-compose.dev.yml은 django, postgresql 테스트 용도.  
  
create superuser
$ docker-compose -f docker-compose.dev.yml exec web python manage.py createsuperuser

--------------------------------------------------------------------------

web logs : /home/ubuntu/code/web_nicework/nicework/logs

all: 
	make build && make run

run:
	docker-compose up -d

build:
	docker-compose build

stop:
	docker-compose stop

cli: 
	docker exec -it assestment-2xt-flask /bin/bash
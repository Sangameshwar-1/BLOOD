# Makefile
.PHONY: build up down logs test clean

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f backend

test:
	docker-compose exec backend python test_simple.py

test-api:
	docker-compose exec backend python test_api_endpoints.py

test-db:
	docker-compose exec backend python test_db.py

clean:
	docker-compose down -v
	docker system prune -f
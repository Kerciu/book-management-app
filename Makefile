init:
	make build
	docker compose exec backend python manage.py makemigrations authentication
	make migrate
	docker compose exec backend python manage.py makemigrations book
	make migrate
	docker compose exec backend python manage.py makemigrations shelf
	make migrate
	make makemigrations
	make migrate

build:
	docker compose up -d --build


clean:
	docker compose down -v

test:
	@if [ -z "$(argument)" ]; then \
		echo "Error: argument is required"; \
		exit 1; \
	fi
	docker compose exec backend python manage.py test $(argument)

docker_run:
	@if [ -z "$(argument)" ]; then \
		echo "Error: argument is required"; \
		exit 1; \
	fi
	docker compose exec backend python manage.py $(argument)


migrate:
	make docker_run argument="migrate"

makemigrations:
	make docker_run argument="makemigrations"

runserver:
	make docker_run argument="runserver 0.0.0.0:8000"

backend_logs:
	docker compose logs backend

createsuperuser:
	docker compose exec backend python manage.py createsuperuser

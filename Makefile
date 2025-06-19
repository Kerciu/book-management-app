init:
	make build
	docker compose exec backend python manage.py makemigrations authentication
	docker compose exec backend python manage.py migrate authentication
	docker compose exec backend python manage.py makemigrations book
	docker compose exec backend python manage.py migrate book
	docker compose exec backend python manage.py makemigrations shelf
	docker compose exec backend python manage.py migrate shelf
	docker compose exec backend python manage.py makemigrations admin
	docker compose exec backend python manage.py migrate admin
	docker compose exec backend python manage.py makemigrations token_blacklist
	docker compose exec backend python manage.py migrate token_blacklist
	docker compose exec backend python manage.py makemigrations sessions
	docker compose exec backend python manage.py migrate sessions
	docker compose exec backend python manage.py makemigrations sites
	docker compose exec backend python manage.py migrate sites
	docker compose exec backend python manage.py makemigrations notification
	docker compose exec backend python manage.py migrate notification
	docker compose exec backend python manage.py makemigrations review
	docker compose exec backend python manage.py migrate review
	docker compose exec backend python manage.py makemigrations social
	docker compose exec backend python manage.py migrate social
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

runmigrations:
	docker compose exec backend python manage.py makemigrations authentication
	docker compose exec backend python manage.py migrate authentication
	docker compose exec backend python manage.py makemigrations book
	docker compose exec backend python manage.py migrate book
	docker compose exec backend python manage.py makemigrations shelf
	docker compose exec backend python manage.py migrate shelf
	docker compose exec backend python manage.py makemigrations admin
	docker compose exec backend python manage.py migrate admin
	docker compose exec backend python manage.py makemigrations token_blacklist
	docker compose exec backend python manage.py migrate token_blacklist
	docker compose exec backend python manage.py makemigrations sessions
	docker compose exec backend python manage.py migrate sessions
	docker compose exec backend python manage.py makemigrations sites
	docker compose exec backend python manage.py migrate sites
	docker compose exec backend python manage.py makemigrations notification
	docker compose exec backend python manage.py migrate notification
	docker compose exec backend python manage.py makemigrations review
	docker compose exec backend python manage.py migrate review
	docker compose exec backend python manage.py makemigrations social
	docker compose exec backend python manage.py migrate social
	make makemigrations
	make migrate

fillDB:
	docker compose exec backend python scripts/fillDB.py
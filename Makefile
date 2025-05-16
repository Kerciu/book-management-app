init:
	make build
	
	# I honestly have no idea what's wrong with django and 
	# why the fuck does it require manually making migrations and migrating
	# but frankly I'm mad and I don't plan to do shit to fix it properly 
	# except for copying it and pasting it all the time
	# Regards 
	# Maciej Kozłowski

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
	docker compose exec backend python manage.py makemigrations review
	docker compose exec backend python manage.py migrate review
	docker compose exec backend python manage.py makemigrations rating
	docker compose exec backend python manage.py migrate rating
	make makemigrations
	make migrate

build:
	docker compose up -d --build


clean:
	docker compose down -v

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

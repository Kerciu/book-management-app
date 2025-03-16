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

init:
	make build
	make makemigrations
	make migrate
	make runserver
	
backend_logs:
	docker compose logs backend

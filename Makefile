build:
	docker compose up -d --build


clean:
	docker compose down -v

migrate:
	docker compose exec backend python manage.py migrate --verbosity 2

makemigrations:
	docker compose exec backend python manage.py makemigrations bookService --verbosity 2

createsuperuser:
	docker compose exec backend python manage.py createsuperuser

init:
	make build
	make makemigrations
	make migrate
	make createsuperuser


# BD2_25L
Databases 2 @ WUT

Requirements:
  - docker
  - compose V2

Running:
  $ make init

Makefile commands:
  make backend_logs - returns logs from backend container
  make runserver - runs app on 0.0.0.0:8000
  make makemigrations - runs django makemigrations command
  make migrate - runs django migrate command
  make docker_run argument="$(argument)" - runs django command specified by argument

# Aplikacja do Zarządzania Kolekcjami Książek
Umożliwia użytkownikom dodawanie książek do własnej kolekcji, ocenianie, recenzowanie oraz dzielenie się rekomendacjami ze znajomymi. Funkcje mogą obejmować filtrowanie według gatunków, autorów, oraz śledzenie postępów czytelniczych.

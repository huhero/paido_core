# paido_backend


# Poetry commands

create new project.

`poetry new [name project]`


init project.

`poetry install`

install dependences

`poetry add [name]`

init virtual enviroment

`eval $(poetry env activate)`


# FastAPI commands

Init dev server

`fastapi dev src/paido_core/app.py`


# Tasks del proyecto

lint: revisar buenas practicas de codigo

`task lint`

pre_format: correciones de buenas practicas

`task pre_format`

format: ejecuta formato en el codigo segun las convenciones en el toml

`task format`

run: ejecuta servidor de desarrollo FastAPI

`task run`

pre_test: ejecuta linter antes de los test

`task pre_test`

test: ejecuta los tests

`task test`

post_test: genera reporte de coverage

`task post_test`


# Alembic commands

iniciar sistema de migraciones

`alembic init [nombre]`

Generar una migración

`alembic revision --autogenerate -m "[name migration]"`


Aplicar la última migración

`alembic upgrade head`

Devolver estado aterior

`alembic downgrde`

ver migraciones aplicadas

`alembic history`


Devolver estado especifico

`alembic downgrde [idmigration]`

# Docker commands

construir imagen

`docker build -t "paido_core" .`

iniciar imagen

`docker run -it --name paido_core -p 8000:8000 paido_core:latest`

- it: modo interactivo
- name: nombre a la imagen
- p: puerto


# levantar aplicacion y buildear

`docker-compose up --build`

# levantar aplicacion

`docker-compose up`

# bajar aplicacion 

`docker-compose down`

# Fly.io commands

login

`flyctl auth login`

deploy

`flyctl deploy`

Set enviroment variables

`flyctl secrets set DATABASE_URL`

Show server


`flyctl ssh console`
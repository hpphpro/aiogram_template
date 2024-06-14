## Aiogram 3 template

Simple template to improve your development



DIRECTORY STRUCTURE
-------------------

```
locales/ there is your locales, like en/ru
src/
    common/
        ...
        Here is actually can be your interfaces or dto/entity/any
    filters/      there is your filters
    keyboards/    there is your keyboards
    middlewares/  there is your middlewares
    core/
        app.py        Your Application
        loader.py     here is your bot configurations
        settings.py   your settings for whole app
    database/
        core/         here is your connection or main class
        models/       your db models
        repositories/ your repo for work with db models and queries
    routers/          your handlers/routers to interact with users
    services/         your business-logic
    __main__.py       entry point
     
```
## Download
```
git clone git@github.com:hpphpro/aiogram_template.git
```
## ENV_FILE
First of all rename your `.env_example` to `.env`
```

BOT_TOKEN=yourtoken
BOT_ADMINS=[] # optional
DB_URI=sqlite+aiosqlite:///{} # or any other driver 
DB_HOST=yourdbhost  # optional
DB_PORT=yourdbport # optional
DB_USER=yoourdbuser # optional
DB_NAME=mysuperdb.db
DB_PASSWORD=yourdbpassword # optional
REDIS_HOST=127.0.0.1 # optional
REDIS_PORT=6379 # optional

```
# Installation
```
pip install -r requirements.txt
```
Create db and tables. By default db is sqlite
```
alembic revision --autogenerate -m 'initial' && alembic upgrade head
```
To create locale, for example `en`:
```
pybabel init -i locales/messages.pot -d locales -D messages -l en -> Windows
make babel_init -> Unix
```
Extract text/update/compile:
## Unix
```
make babel_extract
```
```
make babel_update
```
```
make babel_compile
```
## Windows
```
pybabel extract --input-dirs=src -o locales/messages.pot
```
```
pybabel update -d locales -D messages -i locales/messages.pot
```
```
pybabel compile -d locales -D messages
```
Start app:

for Windows:
```
python -m src
```
for Unix:
```
python3 -m src
```
And thats it!
# Docker. With postgresql db example
## Unix:
```
make docker_build
```
Add migrations:
```
docker-compose run --rm migrate
```
```
make docker_up
```
## Windows:
```
docker-compose build && docker-compose run --rm migrate && docker-compose up -d
```


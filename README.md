Tube
====

### System requirements

```bash
python       --version >= 3.5.*  # Python
psql         --version >= 9.5.*  # PostgreSQL
redis-server --version >= 4.0.*  # Redis
```

### Installation

```bash
git clone https://github.com/kxnes/tube.git

cd ./tube

cp ./src/settings/local.example.py ./src/settings/local.py
# replace all `--PLACEHOLDER--`-s with present values

pip install -r requirements.txt

python manage.py migrate

# create superuser if needed
python manage.py createsuperuser
```

### Development server

```bash
python manage.py runserver
```

### Workers

```bash
celery -A src.app beat --detach
celery -A src.app worker
```

### Docker

```bash
# service will be available on 8000 port, admin site enabled with admin - admin credentials
docker-compose up --build
```

### API

1. All requests to `/api/words/` must contain `Authorization` Header with `Token --token--`
2. `JSON` examples below contains types of fields

```
Method | Endpoint                        | Request data                                 | Response
--------------------------------------------------------------------------------------------------------------------------------------------------------
POST   | /api/auth/                      | {"username": "string", "password": "string"} | {"token": "string"}
POST   | /api/words/                     | {"key_word": "string"}                       | {"key_word": "string", "id": "int"}
GET    | /api/words/                     |                                              | [{"key_word": "string", "id": "int"}, ...]
DELETE | /api/words/{key_word_id}/       |                                              |                        
GET    | /api/words/{key_word_id}/video/ |                                              | {"key_word": "string", "id": "int", "urls": ["string", ...]}
--------------------------------------------------------------------------------------------------------------------------------------------------------
```

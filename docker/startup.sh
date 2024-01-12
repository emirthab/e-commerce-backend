#!/bin/bash
# dockerize -wait tcp://db:3306 -timeout 20s
# alembic upgrade head && gunicorn --bind 0.0.0.0:8000 -w 4 -k uvicorn.workers.UvicornWorker src.server:app
dockerize -wait tcp://db:3306 -timeout 20s
alembic upgrade head && gunicorn --bind 0.0.0.0:8000 -w 4 -k uvicorn.workers.UvicornWorker src.server:app
#celery -A src.celery_task worker --loglevel=info

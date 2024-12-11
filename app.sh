#!/bin/bash

sleep 15
alembic upgrade head
cd src
uvicorn main:app --reload --workers 1 --host 0.0.0.0 --port 8000
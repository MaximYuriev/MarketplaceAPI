import os
import pathlib

from dotenv import load_dotenv


load_dotenv()

POSTGRES_USER=os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD=os.environ.get("POSTGRES_PASSWORD")
POSTGRES_HOST=os.environ.get("POSTGRES_HOST")
POSTGRES_PORT=os.environ.get("POSTGRES_PORT")
POSTGRES_DB=os.environ.get("POSTGRES_DB")

PRIVATE_KEY_PATH=pathlib.Path(os.environ.get("PRIVATE_KEY_PATH"))
PUBLIC_KEY_PATH=pathlib.Path(os.environ.get("PUBLIC_KEY_PATH"))

CRYPT_ALGORITHM=os.environ.get("CRYPT_ALGORITHM")

COOKIE_KEY=os.environ.get("COOKIE_KEY")

REDIS_HOST=os.environ.get("REDIS_HOST")
REDIS_PORT=os.environ.get("REDIS_PORT")
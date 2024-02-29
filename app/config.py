from dotenv import load_dotenv
import os
from fastapi.templating import Jinja2Templates



load_dotenv()

DB_PATH = os.environ.get("DB_PATH")

base_url = 'http://127.0.0.1:8000'

SECRET_AUTH = os.environ.get("SECRET_AUTH")

templates = Jinja2Templates(directory="templates")

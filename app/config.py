from dotenv import load_dotenv
import os
from fastapi.templating import Jinja2Templates



load_dotenv()

DB_PATH = os.environ.get("DB_PATH")


SECRET_AUTH = os.environ.get("SECRET_AUTH")


templates = Jinja2Templates(directory="app/templates")

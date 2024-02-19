from dotenv import load_dotenv
import os
load_dotenv()

DB_PATH = os.environ.get("DB_PATH")


SECRET_AUTH = os.environ.get("SECRET_AUTH")
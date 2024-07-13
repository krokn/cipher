from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST=os.environ.get("DB_HOST")
DB_PORT=os.environ.get("DB_PORT")
DB_NAME=os.environ.get("DB_NAME")
DB_USER=os.environ.get("DB_USER")
DB_PASS=os.environ.get("DB_PASS")
SECRET_FOR_TOKEN=os.environ.get("SECRET_FOR_TOKEN")
SMTP_HOST=os.environ.get("SMTP_HOST")
SMTP_PORT=os.environ.get("SMTP_PORT")
SMTP_USER=os.environ.get("SMTP_USER")
SMTP_PASSWORD=os.environ.get("SMTP_PASSWORD")

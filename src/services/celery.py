import random
import smtplib
from email.mime.text import MIMEText
from email.header import Header

from celery import Celery
from loguru import logger

from config import SMTP_USER, SMTP_PORT, SMTP_PASSWORD
from src.services.redis import create_code_for_email_and_save_code

celery = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')


@celery.task
def send_email(email: str):
    msg = MIMEText(f'{create_code_for_email_and_save_code(email)}', 'plain', 'utf-8')
    msg['Subject'] = Header('Мобильная игра Шифр', 'utf-8')
    msg['From'] = SMTP_USER
    msg['To'] = ', '.join(email)

    try:
        with smtplib.SMTP_SSL('smtp.yandex.ru', SMTP_PORT) as s:
            s.login(SMTP_USER, SMTP_PASSWORD)
            s.sendmail(msg['From'], email, msg.as_string())
    except Exception as ex:
        print(f'Failed to send email: {ex}')




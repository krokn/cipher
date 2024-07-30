import random
import smtplib
from email.mime.text import MIMEText
from email.header import Header

from celery import Celery
from celery.schedules import crontab
from loguru import logger

from config import SMTP_USER, SMTP_PORT, SMTP_PASSWORD
from src.services.redis import create_code_for_email_and_save_code

celery = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

celery.conf.timezone = 'UTC'


celery.conf.beat_schedule = {
    'reset-weekly-reputation': {
        'task': 'src.services.tasks.reset_weekly_reputation',
        'schedule': crontab(day_of_week='tue', hour='8', minute='59'),  # Каждое воскресенье в 9:55 UTC
    },
    'reset-monthly-reputation': {
        'task': 'src.services.tasks.reset_monthly_reputation',
        'schedule': crontab(day_of_month='1', hour='0', minute='0'),  # 1-го числа каждого месяца в полночь UTC
    },
}


celery.autodiscover_tasks(['src.services.tasks'])


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




from celery import shared_task

from src.repositories.rating import RatingRepository


@shared_task
def reset_weekly_reputation():
    RatingRepository().reset_weekly_reputation()
    return 'Weekly reputation reset complete'


@shared_task
def reset_monthly_reputation():
    RatingRepository().reset_monthly_reputation()

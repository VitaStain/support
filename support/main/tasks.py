from celery import shared_task

from .service import send


@shared_task
def send_user_email(email):
    send(email)

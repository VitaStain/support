from celery import shared_task


@shared_task
def addq():
    print(' ')

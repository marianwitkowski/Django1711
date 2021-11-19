# definicje funkcji wykonywanych przez celery

from celery import shared_task
import time


@shared_task(bind=True)
def task_send_email(self):
    print("Start sending...")
    time.sleep(20)
    print("End sending...")
    return "OK"


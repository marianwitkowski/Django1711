# definicje funkcji wykonywanych przez celery

from celery import shared_task, states
import time

@shared_task(bind=True)
def long_task(self):
    self.update_state(state=states.PENDING, meta={"stage":1})
    time.sleep(10)
    self.update_state(state=states.RECEIVED, meta={"stage":1})
    time.sleep(10)
    self.update_state(state=states.SUCCESS, meta={"stage":1})
    return True

@shared_task(bind=True)
def task_send_email(self):
    print("Start sending...")
    time.sleep(20)
    print("End sending...")
    return "OK"


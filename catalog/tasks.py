from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from celery.decorators import task
logger = get_task_logger(__name__)


@periodic_task(run_every=(crontab(minute='*/1')), name="some_task", ignore_result=True)
def some_task():
    print("hello")
    logger.info("minute")
    # do something

@task(name="send")
def send():
    """sends an email when feedback form is filled successfully"""
    logger.info("Sent feedback email")
from __future__ import absolute_import

from celery import shared_task
from celery.utils.log import get_task_logger
from sigia.models import BugReport

logger = get_task_logger(__name__)


@shared_task
def hello_celery():
    logger.info("Task executed...")
    #BugReport(gravity="H", name="Celery", description="celery test", state="C").save()
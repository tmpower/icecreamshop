import time
import logging
import random


logger = logging.getLogger(__name__)


def _slow_payment() -> str:
    # randomly returns either 'success' (99%) or 'failed' (1%) after sleeping for 60 seconds
    logger.info('payment processing started on 3rd party')
    time.sleep(60)
    if random.random() < 0.99:
        return 'success'
    else:
        return 'failed'


def pay() -> str:
    return _slow_payment()

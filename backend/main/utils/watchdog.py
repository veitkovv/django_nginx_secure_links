import logging
import threading
import time

from django.conf import settings
from backend.main.utils.modules.wd import observer, Handler


def serve_forever():
    observer.schedule(Handler(), path=settings.MEDIA_ROOT, recursive=True)
    observer.start()
    # observer.join()
    while True:
        # Если вся валидация прошла успешно, запускаем бесконечный observer
        time.sleep(0.1)


def run_observer():
    print('running observer')
    # t = threading.Thread(target=serve_forever())
    # t.daemon = True
    # t.start()

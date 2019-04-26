import os

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

observer = Observer()


class Handler(FileSystemEventHandler):
    """
    Реакция на различные события FS. Нас интересует создание, удаление, изменение файлов.
    В каждом методе отправка логов, и отправка сообщения в телеграм.
    """

    def on_created(self, event):
        if not event.is_directory:
            pass

    def on_deleted(self, event):
        if not event.is_directory:
            pass

    def on_modified(self, event):
        if not event.is_directory:
            pass

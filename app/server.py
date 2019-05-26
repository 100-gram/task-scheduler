from flask import Flask
from view.interface import ConsoleInterface
from config.config import clear, shutdown_server
import threading
import time

"""
This app module is wrapper for base flask application.

Here interface module is importing to initialize you want in background in separate thread.
Just set your code after run_job
"""


class Server(Flask):
    def __init__(self, *args, **kwargs):
        super(Server, self).__init__(*args, **kwargs)
        self._activate_background_job()

    @staticmethod
    def _activate_background_job():
        def run_job():
            time.sleep(1)
            clear()
            ConsoleInterface.console_init()
            shutdown_server()

        t = threading.Thread(target=run_job)
        t.start()

from flask import Flask
from view.interface import ConsoleInterface
from config.config import clear, shutdown_server
import threading
import time


class Server(Flask):
    def __init__(self, *args, **kwargs):
        super(Server, self).__init__(*args, **kwargs)
        self._activate_background_job()

    @staticmethod
    def _activate_background_job():
        def run_job():
            time.sleep(1)
            clear()
            interface = ConsoleInterface()
            interface.console_init()

        t = threading.Thread(target=run_job)
        t.start()
        t.join()
        shutdown_server()

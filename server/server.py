from flask import Flask
from view.interface import ConsoleInterface
from config.config import shutdown_server
import threading
import time

"""
This server module is wrapper for base flask application.

Here interface module is importing to initialize cui in background in separate thread.
Just calling needed method in run_job function 
"""


class Server(Flask):
    def __init__(self, *args, **kwargs):
        """
        Constructor for Server

        :param args: arguments
        :param kwargs: arguments with keys
        """
        super(Server, self).__init__(*args, **kwargs)
        self._activate_background_job()

    @staticmethod
    def _activate_background_job():
        """
        Start Console interface in other thread

        :return:None
        """
        def run_job():
            time.sleep(1)
            console_interface = ConsoleInterface()
            console_interface.console_init()
            shutdown_server()

        t = threading.Thread(target=run_job)
        t.start()

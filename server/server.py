from flask import Flask
from view.interface import ConsoleInterface
import threading
import signal
import time
import sys
import os


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
            os.kill(os.getpid(), signal.SIGQUIT)

        t = threading.Thread(target=run_job, daemon=True)
        try:
            t.start()
        except (KeyboardInterrupt, SystemExit):
            sys.exit()

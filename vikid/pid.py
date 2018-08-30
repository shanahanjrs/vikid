# coding: utf-8

"""
pid.py
~~~~~~

ProcessId library - internal to Viki
:license: Apache2, see LICENSE for more details
"""

import os
from vikid.application.app import App

class Lock():
    """ Lock/pid file library for viki """


    def __init__(self):
        """
        Initialize lockfile handler
        """

        application = App()

        self.pidfile_name = "vikid.pid"
        self.pid_file_abs_path = "{home_dir}/{filename}".format(home_dir=application.home, filename=self.pidfile_name)
        self.pid = os.getpid()


    def pid_file_exists(self):
        """
        Check if a current Vikid PID file exists
        """
        if os.path.exists(self.pid_file_abs_path):
            return True

        return False


    def pid_file_create(self):
        """
        Create a new PID file
        """
        with open(self.pid_file_abs_path, mode='w') as pid_file_obj:
            pid_file_obj.write(self.pid)
            pid_file_obj.close()


    def pid_file_match(self):
        """
        Checks the PID file to make sure the written process id
        matches the current process id.
        :returns int
          -1 Mismatch process id
           0 Missing PID file
           1 Matching process id
        """
        if not self.pid_file_exists():
            return 0

        with open(self.pid_file_abs_path, 'r') as pid_file_obj:
            process_id = pid_file_obj.read()
            pid_file_obj.close()

        if str(self.pid) == process_id:
            return 1
        else:
            return -1

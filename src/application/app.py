# -*- coding: utf-8 -*-  

""" 
app.py
 ~~~~~~

  This module implements the App class for main application details and system checks / maintenance.
:license: Apache2, see LICENSE for more details. 
"""

# --- Imports

import os
import src._version
import src._conf
import logging

# Provide version
version = src._version.__version__

# Viki home directory
home = src._conf.__config_home__

# Path to the jobs directory
jobs_path = src._conf.__config_jobs_dir__

# Name of viki conf file
job_config_filename = src._conf.__config_filename__

# Abs path to conf file
job_config_path = src._conf.__config_file_path__

# Abs path to logs file
logfile_path = src._conf.__logfile_path__

# File permissions
file_perms = 0o755

# Logging configuration
logging_config = dict(
    version = 1,
    formatters = {
        'f': {'format':
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'}
    },
    handlers = {
        'h': {'class': 'logging.FileHandler',
        'formatter': 'f',
        'filename': logfile_path + '/viki.log',
        'level': logging.DEBUG}
    },
    root = {
        'handlers': ['h'],
        'level': logging.DEBUG,
    },
)

def check_system_setup():
    """ This will be run every time viki starts up
    It will check to make sure the home directory exists,
    the configuration file in viki-home exists, and
    that the jobs directory exists.
    If those are not setup correctly you will need to run viki with sudo to create them.
    """
    dirs = [home, jobs_path, job_config_path, job_config_filename, logfile_path]

    for j in dirs:
        if not os.path.exists(j):
            return False

    return True


def create_home_dir():
    """ Creates the home directory """
    print('Creating home directory...')

    if not home:
        return False

    if os.path.exists(home):
        return False

    os.mkdir(home, mode=file_perms)

    return True


def generate_config_file():
    """ Generates a starter viki configuration file """
    print('Generating configuration file...')

    if not job_config_path:
        return False

    if os.path.exists(job_config_path):
        return False

    tmp_conf_file = """
    {
        "name": "viki"
    }
    """

    with open(job_config_path, mode='w', encoding='utf-8') as conf_file_obj:
        conf_file_obj.write(tmp_conf_file)
        conf_file_obj.close()

    os.chmod(job_config_path, mode=file_perms)

    return True


def generate_log_file():
    """ Generates a blank viki log file """
    print('Generating log file...')

    if not logfile_path:
        return False

    if os.path.exists(logfile_path):
        return False

    tmp_logfile = ''

    with open(logfile_path, mode='w', encoding='utf-8') as logfile_obj:
        logfile_obj.write(tmp_logfile)
        logfile_obj.close()

    os.chmod(logfile_path, mode=file_perms)

    return True


def create_jobs_dir():
    """ Create the jobs directory under viki home """
    print('Creating jobs directory...')

    if not jobs_path:
        return False

    if os.path.exists(jobs_path):
        return False

    os.mkdir(jobs_path, mode=file_perms)

    return True

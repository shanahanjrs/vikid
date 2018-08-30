# coding: utf-8

"""
app.py
~~~~~~

This module implements the App class for main application details and system checks / maintenance.
:license: Apache2, see LICENSE for more details
"""

import os
import vikid._version
import vikid._conf
import logging

"""
    "home_dir",
    "jobs_dir",
    "config_filename",
    "config_file_abs_path",
    "logs_dir"
"""

# Provide version
version = vikid._version.__version__

from vikid._conf import home_dir, jobs_dir, config_filename, config_file_abs_path, logs_dir

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
        'filename': logs_dir + '/viki.log',
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
    # TODO some of these aren't required, create a list of those that we can accept when missing
    dirs = [home_dir, jobs_dir, config_file_abs_path, logs_dir]

    for j in dirs:
        if not os.path.exists(j):
            print('Missing file [{}]...'.format(j))
            return False

    return True


def create_system_setup():
    """
    Creates the required files/directories
    """
    dirs = [
        home_dir, jobs_dir, logs_dir
    ]
    files = [
        config_file_abs_path
    ]

    for j in dirs:
        if not os.path.exists(j):
            print('Creating dir [{}]...'.format(j))
            os.mkdir(j)

    # TODO use the helper funcs below to create these files the right way
    for k in files:
        if not os.path.exists(k):
            with open(k, 'w') as file_obj:
                print('Creating file [{}]...'.format(k))
                file_obj.write('')


def create_home_dir():
    """ Creates the home directory """
    print('Creating home directory...')

    if not home_dir:
        return False

    if os.path.exists(home_dir):
        return False

    os.mkdir(home_dir, mode=file_perms)

    return True


def generate_config_file():
    """ Generates a starter viki configuration file """
    print('Generating configuration file...')

    if not config_file_abs_path:
        return False

    if os.path.exists(config_file_abs_path):
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

    if not jobs_dir:
        return False

    if os.path.exists(jobs_dir):
        return False

    os.mkdir(jobs_dir, mode=file_perms)

    return True

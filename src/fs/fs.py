# -*- coding: utf-8 -*-  

""" 
fs.py
 ~~~~~

Filesystem library - internal to Viki
:license: Apache2, see LICENSE for more details. 
"""

from src.application import app

import os
import subprocess
import json

home = app.home
jobs_path = "{}/jobs".format(home)
job_output_file = "output.txt"
job_config_filename = "config.json"


# --- Main library

def write_job_file(job_file, text):
    """ _write_job_file
    Takes a filename and textblob and
    attempts to write the text to that file
    """

    if not job_file or not text:
        return False

    # This will not work if the directory does not exist
    with open(job_file, 'w') as file_obj:
        file_obj.write(json.dumps(text))
        file_obj.close()

    return True


def read_job_file(job_file):
    """ _read_job_file
    Takes a job name (abs path) and returns the string version of .../jobs/job_name/config.json
    Filename must be the full path of the file, not just the name
    contents of that file or False if it does not exist
    """
    if not job_file:
        return False

    if not os.path.exists(job_file):
        return False

    with open(job_file, 'r') as file_obj:
        ret = file_obj.read()
        file_obj.close()

    return ret


def dirty_rm_rf(directory_name):
    """ Executes a quick and dirty `rm -rf directory_name'
    Works on directories or files
    Use subprocess because its easier to let bash do this than Python
    :param directory_name:
    :returns bool:
    """

    subprocess.call(
        [u'/bin/bash', u'-c', u'rm -rf ' + directory_name]
    )

    return True


def job_exists(job_name):
    """ Simple internal function to quickly tell you if
    a job actually exists or not
    :param job_name:
    :returns bool:
    """
    path = '{}/{}'.format(jobs_path, job_name)

    return os.path.exists(path)


def read_last_run_output(output_file_path):
    """ _read_last_run_output
    Takes output_file_path (abs path) and returns the entire output of the last job run's output
    """
    if not output_file_path:
        return False

    output_filename = output_file_path.split('/')[-1]

    # Check the file exists and is actually named correctly
    if not os.path.exists(output_file_path) or output_filename != job_output_file:
        return False

    with open(output_file_path, 'r') as file_obj:
        ret = file_obj.read()
        file_obj.close()

    return ret

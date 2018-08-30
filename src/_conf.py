# coding: utf-8

"""
_conf.py
~~~~~~~~

Provides Viki default configuration

use ~/.viki/vikid.json to override these options.

:license: Apache2, see LICENSE for more details
"""

import os

home_dir = "{}/.viki".format(os.path.expanduser("~"))
jobs_dir = home_dir + "/jobs"
logs_dir = home_dir + "/logs"
config_filename = "viki.json"
config_file_abs_path = home_dir + "/" + config_filename

__all__ = [
    "home_dir",
    "jobs_dir",
    "config_filename",
    "config_file_abs_path",
    "logs_dir"
]

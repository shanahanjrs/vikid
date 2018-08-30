# coding: utf-8

import json

def read_config(filepath='~/.vikid/config.json'):
    with open(filepath, 'r') as file_obj:
        return json.loads(file_ojb.read())

def run_system_setup():
    # Make vikid home dir
    # Make all required JSON config files
    # Make example job

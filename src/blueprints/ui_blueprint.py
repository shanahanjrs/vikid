# -*- coding: utf-8 -*-  

""" 
ui_blueprint.py
~~~~~~~~~~~~~~~~~

This module implements the main ui for Viki.
:license: Apache2, see LICENSE for more details. 
"""

# --- Imports
from flask import Blueprint, render_template

# --- Vars
blueprint_name = 'ui_blueprint'
template_folder_name = 'templates'

ui_blueprint = Blueprint(blueprint_name,
                         __name__,
                         template_folder=template_folder_name)

# --- UI routes

@ui_blueprint.route("/")
def root():
    """ Home """

    ret = {"name": "viki", "version": '0.0.0.1'}

    return render_template('home.html', data=ret)

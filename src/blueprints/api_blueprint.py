# -*- coding: utf-8 -*-  

""" 
api_blueprint.py
~~~~~~~~~~~~~~~~~

This module implements the main Job api for Viki.
:license: Apache2, see LICENSE for more details. 
"""

# --- Imports
from flask import Blueprint, jsonify, request
from src.job.job import Job

# --- Vars
blueprint_name = 'api_blueprint'
template_folder_name = 'templates'

job = Job()

api_blueprint = Blueprint(blueprint_name, __name__,
                          template_folder=template_folder_name)

# --- Api endpoints

@api_blueprint.route("/jobs", methods=['GET'])
def jobs():
    """ List all jobs """
    return jsonify(job.get_jobs())


@api_blueprint.route("/job/<string:job_name>", methods=['GET', 'POST', 'PUT', 'DELETE'])
def get_job(job_name):
    """ Show single job details by name """

    ret = None

    if request.method == 'GET':
        # Retrieve a jobs details
        ret = job.get_job_by_name(job_name)

    if request.method == 'POST':
        # Create job
        # Requires "application/json" mime type and valid JSON body
        # containing description, and steps
        job_config = str(request.get_json())
        ret = job.create_job(job_name, job_config)

    if request.method == 'PUT':
        # Updated a job
        # Requires "application/json" mime type and valid JSON body
        # containing field/s to be updated
        ret = job.update_job(job_name)

    if request.method == 'DELETE':
        # Deletes a job from the repository
        ret = job.delete_job(job_name)

    if ret is None:
        ret = {"success":0, "message":"Failed"}

    return jsonify(ret)


@api_blueprint.route("/job/<string:job_name>/run", methods=['POST'])
def run_job(job_name):
    """ Run specific job by name """
    return jsonify(job.run_job(job_name))


@api_blueprint.route("/job/<string:job_name>/output", methods=['GET'])
def output_job(job_name):
    """ Get the last run's output of a specific job """
    return jsonify(job.output_job(job_name))


@api_blueprint.route("/3laws", methods=['GET'])
def three_laws():
    """ The three laws of robotics easter-egg """
    return jsonify('A robot may not injure a human being or, through inaction, allow a human being to come to harm. ' +
        'A robot must obey the orders given it by human beings except where such orders would conflict with the First Law. ' +
        'A robot must protect its own existence as long as such protection does not conflict with the First or Second Laws.')

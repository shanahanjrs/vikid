# coding: utf-8

"""
job.py
~~~~~~

This module implements the main Job api for Viki
:license: Apache2, see LICENSE for more details
"""

import ast
import os
import subprocess
import json
import uuid
from typing import Any, Dict, Tuple, List, IO, Optional, Union

from vikid import fs as filesystem


class Job:
    """ Job library for viki """

    debug = False

    def __init__(self):
        """ Initialize jobs handler
        Vars for use:
        home: Viki's home directory. Usually /usr/local/viki
        jobs_path: Path to Viki's jobs directory. Usually /usr/local/viki/jobs
        job_config_filename: Name of the config for each individual job. Usually 'config.json'
        """

        # TODO Move this to a central place so all classes can use it

        # Change to just /home/viki eventually
        self.home: str = os.path.expanduser("~") + "/.viki"

        # Path to the jobs directory relative to self.home
        self.jobs_path: str = self.home + "/" + "jobs"

        # Path to the jobs STDOUT file
        self.job_output_file: str = "output.txt"

        # Name of job configuration file
        self.job_config_filename: str = "config.json"


    # --- Job internals


    @staticmethod
    def _quote_string(string: str, single_quote: bool = True) -> str:
        """ Takes a string and returns it
        back surrounded by quotes
        """
        quote: str

        if single_quote:
            quote = "'"
        else:
            quote = '"'

        return quote + string + quote


    def _run_shell_command(self, command: str, output_filename: str,
                           job_arguments: Optional[List[str]] = None) -> Tuple[bool, int]:
        """ _run_shell_command
        string:command Shell command to run
        string:file path Where the command results (stdout) are stored
        array:arguments to be given to the command
        Runs the given command and stores results in a file
        Returns Tuple (True|False, Return code)
        """
        output_file_obj: IO[Any]
        sh_script_name: str
        child_process: List[str]

        # Generate output file for run results
        output_file_obj = open(output_filename, 'a')

        # Generate a tmp sh file to run command from
        sh_script_name = 'viki-' + str(uuid.uuid4())
        with open(sh_script_name, 'w') as sh_script_obj:
            sh_script_obj.write(command)
            sh_script_obj.close()

        # Create the bash command
        child_process = [u'/bin/bash', u'-xe', sh_script_name]

        # If the job was passed any args, send them into the child process as well
        if job_arguments is not None and len(job_arguments) > 0:
            for argument in job_arguments:
                child_process.append(str(argument))

        # *!* DEBUG - show the list that is about to get piped into Popen
        if self.debug:
            print('Func: _run_shell_command; Var: child_process: ' + str(child_process))

        process = subprocess.Popen(
            child_process,
            stdout=output_file_obj,
            stderr=subprocess.STDOUT
        )

        while process.poll() is None:
            # Not finished
            pass

        return_code = process.poll()

        output_file_obj.close()
        filesystem.dirty_rm_rf(sh_script_name)

        return (True, return_code) if return_code == 0 else (False, return_code)


    # --- Job functions


    def get_jobs(self) -> Dict[str, Any]:
        """
        List jobs in /usr/local/viki/jobs
        Takes no parameters
        """
        message: str = "Ok"
        success: int = 1

        try:
            # Get all job dirs
            jobs_dir_ls = next(os.walk(self.jobs_path))
            jobs_list: List[str] = jobs_dir_ls[1]

        except OSError as error:
            message = str(error)
            success = 0

        ret: Dict[str, Any] = {"success": success, "message": message, "jobs": jobs_list}

        return ret


    def get_job_by_name(self, job_name: str) -> Dict[str, Any]:
        """
        Get details of a single job by name
        string:name Name of specific job
        """
        message: str = "Ok"
        success: int = 1
        contents: str = ""

        try:
            if job_name is None:
                raise ValueError('Missing required field: job_name')

            job_dir: str = self.jobs_path + "/" + job_name

            if os.path.isdir(job_dir) and os.path.exists(job_dir + "/" + self.job_config_filename):
                contents = filesystem.read_job_file(job_dir + "/" + self.job_config_filename)
            else:
                raise OSError('Job directory not found')

        except (OSError, ValueError) as error:
            message = str(error)
            success = 0

        ret: Dict[str, Any] = {"success": success, "message": message, "name": job_name, "config_json": contents}

        return ret


    def output_job(self, name: str) -> Dict[str, Any]:
        """
        Get the output file of a specific job and return the contents of the file
        """
        message: str = "Ok"
        success: int = 1
        contents: str = ""

        try:

            if name is None:
                raise ValueError('Missing required field: job_name')

            job_directory: str = self.jobs_path + "/" + name
            output_file: str = job_directory + "/" + self.job_output_file

            if os.path.isdir(job_directory) and os.path.exists(output_file):
                contents = filesystem.read_last_run_output(output_file)
            else:
                raise OSError('Job directory not found')

        except (OSError, ValueError) as error:
            message = str(error)
            success = 0

        return {"success": success, "message": message, "name": name, "output": contents}


    def create_job(self, new_name: str, data: Dict[str, Union[str, int]]) -> Dict[str, Any]:
        """ Adds a job """
        message: str = "Job created successfully"
        success: int = 1

        try:

            # Generate path and file name
            job_dir: str = self.jobs_path + "/" + new_name
            job_filename: str = job_dir + "/" + self.job_config_filename

            # Bail if
            if os.path.exists(job_dir):
                raise SystemError('Job directory already exists')
            else:
                os.mkdir(job_dir)

            if 'description' not in  data.keys():
                raise ValueError('Missing description')

            if 'steps' not in  data.keys():
                raise ValueError('Missing steps')

            data['runNumber'] = 0
            data['lastSuccessfulRun'] = 0
            data['lastFailedRun'] = 0
            data['name'] = new_name

            # Create job file
            filesystem.write_job_file(job_filename, data)

        except (ValueError, SystemError) as error:
            message = str(error)
            success = 0

        ret = {"success": success, "message": message}

        return ret


    def update_job(self, name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """ Update an existing job """
        message: str = "Job successfully updated"
        success: int = 1

        try:

            # Check required fields first
            #     description
            #     steps

            # Find job
            if not filesystem.job_exists(name):
                raise ValueError('Job {} not found'.format(name))

            # Prep new config

        except ValueError as error:
            message = str(error)
            success = 0

        return {"success": success, "message": message}


    def run_job(self, name: str, job_args: Optional[List[str]] = None):
        """ Run a specific job """
        message: str = "Run successful"
        success: int = 1
        return_code: int = 0

        # Construct job directory and file path names
        job_dir: str = self.jobs_path + "/" + name
        job_config_json_file: str = job_dir + "/" + "config.json"

        # Generate a tmp directory to work in
        # Use uuid4() because it creates a truly random uuid
        # and doesnt require any arguments and uuid1 uses
        # the system network addr.
        tmp_cwd: str = "/tmp/viki-" + str(uuid.uuid4())
        os.mkdir(tmp_cwd)

        try:

            # Check job directory exists
            # Otherwise raise OSError
            if not os.path.isdir(job_dir):
                raise OSError('Job not found')

            # Check config json file exists
            # Otherwise raise OSError
            if not os.path.isfile(job_config_json_file):
                raise OSError('Job file not found')

            # Read the file and load the json inside it
            # Otherwise raise OSError
            job_json = json.loads(filesystem.read_job_file(job_config_json_file))
            if job_json is False or job_json is None:
                raise OSError('Job file could not be read')

            # Create filename path for output file
            # todo: Move this to store the output in each individual build dir
            filename: str = job_dir + "/" + "output.txt"

            # Grab the json array "steps" from jobs/<jobName>/config.json
            job_steps: str = job_json['steps']

            # Execute them individually
            # If any of these steps fail then we stop execution
            for step in job_steps:
                success_bool, return_code = self._run_shell_command(step, filename, job_args)

                # If unsuccessful stop execution
                if not success_bool:
                    raise SystemError('Build step failed')

        except (OSError, subprocess.CalledProcessError, SystemError) as error:
            message = str(error)
            success = 0
        except KeyError:
            message = 'Job has no steps'
            success = 0

        # Clean up tmp workdir
        filesystem.dirty_rm_rf(tmp_cwd)

        return {"success": success, "message": message, "return_code": return_code}


    def delete_job(self, name: str) -> Dict[str, Any]:
        """ Removes a job by name
        Takes a job's name and removes the directory that the job lives in
        """
        message: str = "Job deleted"
        success: int = 1

        try:

            job_dir: str = self.jobs_path + '/' + name

            # Check job directory exists
            # Otherwise raise OSError
            if not os.path.isdir(job_dir):
                raise OSError('Job not found')

            # Remove the job directory
            filesystem.dirty_rm_rf(job_dir)

        except (OSError, ValueError) as error:
            message = str(error)
            success = 0

        return {"success": success, "message": message}

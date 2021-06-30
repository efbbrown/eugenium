import os
import json
from shlex import split, quote
from subprocess import check_output, CalledProcessError
from shutil import copyfile


class GoogleCloudInteractor():
    def __init__(self, *args, **kwargs):
        self.cloud_functions_root_dir = "cloud_functions"

    def compile_script_for_cloud_functions(self,
                                           cloud_function_name: str,
                                           interactor_script: str,
                                           table_name : str,
                                           data_collector_method : str,
                                           data_collector_class : str = None):
        interactor_script_name = interactor_script.replace(".py", "")
        if data_collector_class is None:
            data_collector_class = interactor_script_name
        local_function_dir = os.path.join(self.cloud_functions_root_dir,
                                          cloud_function_name)
        file_main = os.path.join(local_function_dir, "main.py")
        file_requirements = os.path.join(local_function_dir, "requirements.txt")
        # Create a directory for the files
        os.makedirs(local_function_dir, exist_ok=True)
        # Copy config.yaml, models.py, requirements.txt, interactor script into dir
        for script in ["config.yaml", "models.py", "requirements.txt", interactor_script]:
            copyfile(script, os.path.join(local_function_dir, script))
        # Create a main.py file
        with open(file_main, "w") as f:
            f.write(
                f"from {interactor_script_name} import {data_collector_class}, models\n\n\n")
            f.write(f"def {cloud_function_name}(request):\n\t")
            f.write(f"interactor = {data_collector_class}(driver_path='')\n\t")
            f.write(
                f"interactor.data_to_sql(data_collector=interactor.{data_collector_method}, con=models.engine, schema=interactor.schema, if_exists='append')\n"
            )

    def deploy_to_cloud_functions(self,
                                  project_id: str,
                                  cloud_function_name: str,
                                  region: str,
                                  timeout: int = 240,
                                  runtime: str = 'python37',
                                  source: str = None):
        """Deploy to cloud functions
        Read docs here ,https://googleapis.dev/python/cloudfunctions/latest/functions_v1/cloud_functions_service.html>
        Read source here <https://github.com/googleapis/python-functions/>
        Parameters
        ----------
        timeout : int
            An integer defining the number of seconds from the initialisation
            of the cloud function after which it will timeout
        source : str
            Source location of the function directory
        """
        # Check that the current project is the one you want to use
        current_project = self.gcloud_config_get_value_project()
        if current_project != project_id:
            self.gcloud_config_set_project(project_id)
        # Default source location is the location the method
        # compile_script_for_cloud_functions saves to
        if source is None:
            source = f"cloud_functions/{cloud_function_name}"
        # Deploy to cloud functions
        self.call_subprocess(
            f"gcloud beta functions deploy {cloud_function_name} --region={region} --timeout={timeout} --source={source} --runtime {runtime} --trigger-http"
        )

    def schedule_cloud_function(self,
                                cloud_function_name: str,
                                schedule: str,
                                region: str,
                                project_id: str):
        """Schedule a cloud function
        Read docs here <https://googleapis.dev/python/cloudscheduler/latest/scheduler_v1/cloud_scheduler.html>
        """
        # Schedule a cloud function
        self.call_subprocess(
            f"gcloud beta scheduler jobs create http {cloud_function_name} --schedule='{schedule}' --uri=https://{region}-{project_id}.cloudfunctions.net/{cloud_function_name}"
        )

    def call_subprocess(self, command, split_command=True, shell=True):
        if split_command:
            command = split(command)
        try:
            output = check_output(command, shell=shell).strip()
        except CalledProcessError as e:
            raise RuntimeError(
                f"command '{quote(e.cmd)}' return with error (code {e.returncode}): {e.output}"
            )
        return output

    def gcloud_config_get_value_project(self):
        current_project = self.call_subprocess("gcloud config get-value project")
        return current_project

    def gcloud_config_set_project(self, project_id):
        self.call_subprocess(f"gcloud config set project {project_id}")

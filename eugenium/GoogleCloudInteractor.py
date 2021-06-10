import os
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
            f.write(f"def {interactor_script_name}(request):\n\t")
            f.write(f"interactor = {data_collector_class}(driver_path='')\n\t")
            f.write(
                f"interactor.data_to_sql(data_collector=interactor.{data_collector_method}, con=models.engine, schema=interactor.schema, if_exists='append')\n"
            )

    def deploy_to_cloud_functions(self):
        # Deploy to cloud functions
        pass

    def deploy_to_cloud_scheduler(self):
        # Deploy to cloud scheduler
        pass

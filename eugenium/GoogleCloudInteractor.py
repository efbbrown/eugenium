import os


class GoogleCloudInteractor():
    def __init__(self, *args, **kwargs):
        self.cloud_functions_root_dir = "cloud_functions"

    def compile_script_for_cloud_functions(self, cloud_function_name: str,
                                           data_collector_class, data_collector_method):
        local_function_dir = os.path.join(self.cloud_functions_root_dir,
                                          cloud_function_name)
        # Create a directory for the files
        os.makedirs(local_function_dir, exist_ok=True)
        # Create a main.py file
        # Create a requirements.txt file

    def deploy_to_cloud_functions(self):
        # Deploy to cloud functions
        pass

    def deploy_to_cloud_scheduler(self):
        # Deploy to cloud scheduler
        pass

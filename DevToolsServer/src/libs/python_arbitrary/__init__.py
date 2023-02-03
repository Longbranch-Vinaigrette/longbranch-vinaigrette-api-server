import os
import subprocess


class PythonArbitrary:
    output = ""
    error = ""

    def __init__(self, user_folder_name: str, debug: bool = False):
        self.debug = debug

        # Where the scripts will be stored
        self.cache_path = f"{os.getcwd()}{os.path.sep}.cache"
        self.python_arbitrary_path = f"{self.cache_path}{os.path.sep}pythonArbitrary"
        self.user_path = f"{self.python_arbitrary_path}{os.path.sep}{user_folder_name}"

        # Check if the folders exist, if not just make them.
        if not os.path.exists(self.cache_path):
            os.mkdir(self.cache_path)
        if not os.path.exists(self.python_arbitrary_path):
            os.mkdir(self.python_arbitrary_path)
        if not os.path.exists(self.user_path):
            os.mkdir(self.user_path)

    def mkfile(self):
        """Make the file to run"""

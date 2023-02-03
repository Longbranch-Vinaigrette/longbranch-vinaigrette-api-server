import os
import subprocess
import importlib.util


class PythonArbitrary:
    output = ""
    error = ""

    def __init__(self,
                 user_folder_name: str,
                 session_id: str,
                 code: str,
                 debug: bool = False):
        # User folder files contains ':'(colon) so I have to change the name to '_'
        user_folder_name = user_folder_name.replace(":", "_")
        self.session_id = session_id
        self.code = code
        self.debug = debug

        # Where the scripts will be stored
        self.cache_path = f"{os.getcwd()}{os.path.sep}.cache"
        self.python_arbitrary_path = f"{self.cache_path}{os.path.sep}pythonArbitrary"
        self.user_path = f"{self.python_arbitrary_path}{os.path.sep}{user_folder_name}"
        self.session_path = f"{self.user_path}{os.path.sep}{session_id}"
        self.filename = f"{self.session_path}{os.path.sep}main.py"

        # Check if the folders exist, if not just make them.
        if not os.path.exists(self.cache_path):
            os.mkdir(self.cache_path)
        if not os.path.exists(self.python_arbitrary_path):
            os.mkdir(self.python_arbitrary_path)
        if not os.path.exists(self.user_path):
            os.mkdir(self.user_path)
        if not os.path.exists(self.session_path):
            os.mkdir(self.session_path)

    def mkfile(self, code: str):
        """Make the file to run"""
        with open(self.filename, "w") as f:
            f.write(code)

    def end(self):
        """When it ends remove the session folder and file"""
        subprocess.run(["/bin/bash", "-c", f"rm -r {self.session_path}"])

    def run(self):
        """Run the script"""
        # The first argument, is the module relative import
        # The second argument is the path where the module will be found
        spec = importlib.util.spec_from_file_location("main", self.user_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

    def mkfile_and_run(self):
        """Make files and run"""
        self.mkfile(self.code)
        # Call this when a new file is created on runtime, so it can be detected
        # and it should be called to remove items from sys.modules maybe)?
        importlib.invalidate_caches()


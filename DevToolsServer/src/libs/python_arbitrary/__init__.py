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
                 arguments: list = [],
                 folder_name: str = "PYTHON_ARBITRARY",
                 debug: bool = False):
        # User folder may contain weird characters so let's replace em all for '_'
        user_folder_name = user_folder_name.replace(":", "_")
        user_folder_name = user_folder_name.replace(".", "_")
        self.session_id = session_id
        self.code = code
        self.arguments = arguments
        self.debug = debug

        # Where the scripts will be stored
        self.cache_path = f"{os.getcwd()}{os.path.sep}{folder_name}"
        self.user_path = f"{self.cache_path}{os.path.sep}{user_folder_name}"
        self.session_path = f"{self.user_path}{os.path.sep}{session_id}"
        self.filename = f"{self.session_path}{os.path.sep}main.py"

        # Check if the folders exist, if not just make them.
        if not os.path.exists(self.cache_path):
            os.mkdir(self.cache_path)
        if not os.path.exists(self.user_path):
            os.mkdir(self.user_path)
        if not os.path.exists(self.session_path):
            os.mkdir(self.session_path)

        # Import template
        with open(f"{os.getcwd()}{os.path.sep}spec{os.path.sep}template") as f:
            self.template = f.read()

    def encode_script(self, code: str) -> str:
        """Encode the script into the template"""
        template_copy = self.template

        # Insert arguments
        arguments: str = ""
        for index, el in enumerate(self.arguments):
            arguments += f"DEVTOOLS_ARG_{str(index + 1)} = {str(el)}\n"
        template_copy = template_copy.replace("$DEVTOOLS_ARGS", arguments)

        # Insert code
        template_copy = template_copy.replace("$USER_CODE", code)
        return template_copy

    def mkfile(self, code: str):
        """Make the file to run"""
        with open(self.filename, "w") as f:
            f.write(self.encode_script(code))

    def end(self):
        """When it ends remove the session folder and file"""
        subprocess.run(["/bin/bash", "-c", f"rm -r {self.session_path}"])

    def run(self):
        """Run the script and get its result"""
        # The first argument, is the module relative import
        # The second argument is the path where the module will be found
        spec = importlib.util.spec_from_file_location("main", self.user_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Try to get the result
        try:
            # The result is in the module object
            return module.DEVTOOLS_RESULT
        except:
            raise Exception("No result found")

    def mkfile_and_run(self):
        """Make files and run"""
        self.mkfile(self.code)

        # Call this when a new file is created on runtime, so it can be detected
        # and it should be called to remove items from sys.modules maybe)?
        importlib.invalidate_caches()

        # Run the script
        try:
            result = self.run()
        except:
            result = {
                "debug": {
                    "message": "Successfully loaded and ran the script.",
                    "state": "success",
                    "error": False,
                }
            }

        # self.end()
        return result

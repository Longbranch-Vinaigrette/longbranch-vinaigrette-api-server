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
                 remove_at_the_end: bool = True,
                 debug: bool = False):
        # User input may contain weird characters so let's replace em all for '_'
        user_folder_name = user_folder_name.replace(":", "_")
        user_folder_name = user_folder_name.replace(".", "_")
        user_folder_name = user_folder_name.replace("-", "_")

        session_id = session_id.replace(":", "_")
        session_id = session_id.replace(".", "_")
        session_id = session_id.replace("-", "_")

        # In case it starts with a number, which is not allowed by python standards
        user_folder_name = f"user_{user_folder_name}"
        session_id = f"sid_{session_id}"

        self.code = self.add_tabs_to_every_line(code)
        self.arguments = arguments
        self.remove_at_the_end: bool = remove_at_the_end
        self.debug = debug

        self.filename = "main"

        # Get the current folder
        current_folder = os.path.dirname(os.path.realpath(__name__))

        # Absolute import from the project root folder
        self.absolute_python_import = f"{folder_name}.{user_folder_name}.{session_id}.{self.filename}"

        # Where the scripts will be stored
        self.cache_path = f"{current_folder}{os.path.sep}{folder_name}"
        self.user_path = f"{self.cache_path}{os.path.sep}{user_folder_name}"
        self.session_path = f"{self.user_path}{os.path.sep}{session_id}"
        self.file_path = f"{self.session_path}{os.path.sep}{self.filename}.py"

        # Check if the folders exist, if not just make them.
        if not os.path.exists(self.cache_path):
            os.mkdir(self.cache_path)
        if not os.path.exists(self.user_path):
            os.mkdir(self.user_path)
        if not os.path.exists(self.session_path):
            os.mkdir(self.session_path)

        # Make it a module
        with open(f"{self.session_path}{os.path.sep}__init__.py", "w") as f:
            f.write("\n")

        # Import template
        with open(f"{os.getcwd()}{os.path.sep}spec{os.path.sep}template.py") as f:
            self.template = f.read()

    def add_tabs_to_every_line(self, string: str):
        """Add a tab to every line of the given string"""
        lines = string.splitlines()
        new_str: str = ""

        # Add a tab to every line
        for index, line in enumerate(lines):
            if not (index == 0):
                new_str += f"    {line}\n"
            else:
                new_str += f"{line}\n"

        return new_str

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
        with open(self.file_path, "w") as f:
            f.write(self.encode_script(code))

    def end(self):
        """When it ends remove the session folder and file"""
        subprocess.run(["/bin/bash", "-c", f"rm -r {self.session_path}"])

    def run(self):
        """Run the script and get its result"""
        # The first argument, is the module relative import
        # The second argument is the path where the module will be found
        module = importlib.import_module(self.absolute_python_import)

        # Try to get the result
        try:
            result = module.DEVTOOLS_RESULT

            # The result is in the module object
            return result
        except Exception as ex:
            print("Exception on run: ", ex)
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
        except Exception as ex:
            print("Exception: ", ex)
            result = {
                "debug": {
                    "message": "Successfully loaded and ran the script.",
                    "state": "success",
                    "error": False,
                }
            }

        # Remove files and folders
        if self.remove_at_the_end:
            self.end()
        return result

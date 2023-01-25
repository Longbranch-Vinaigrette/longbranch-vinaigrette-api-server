import json
import subprocess

from django.http import HttpResponse, HttpRequest

from src.submodules.dev_tools_utils.django_utils import DjangoUtils
from src.submodules.dev_tools_utils.Debug import Debug
from src.submodules.dev_tools_utils.data_configuration.ProjectInfo import ProjectInfo
from src.submodules.dev_tools_utils.dbs.RepositorySettings import RepositorySettings
from src.submodules.dev_tools_utils.app_manager import AppManager


class Main:
    def __init__(self, route: str):
        self.route = route

    def post(self, request: HttpRequest):
        """Check whether an app is DevTools compatible"""
        data = DjangoUtils().validate_json_content_type(request)

        # If there is "debug" in data it means that there was an error
        if not "debug" in data:
            body = json.loads(request.body.decode("utf-8"))

            # Check if the required data was given
            try:
                app_path = body["path"]
                command_name = body["commandName"]
            except Exception as ex:
                print("Exception: ", ex)
                data = {
                    "debug": Debug("Bad data format a key was not given correctly, the key: "
                                   f"{str(ex)}",
                                   state="danger").get_message(),
                }
                res = HttpResponse(json.dumps(data))
                res.headers["Content-Type"] = "application/json"
                return res

            try:
                # It raises an exception if the app is not devtools compatible
                project_info = ProjectInfo(app_path)
                commands = project_info.get_commands()

                if command_name == "stop":
                    if "stop" in commands:
                        app_manager = AppManager(app_path)
                        app_manager.stop_app()
                        data = {
                            "debug": Debug("Stop command run successfully.",
                                           state="success").get_message(),
                        }
                    else:
                        app_manager = AppManager(app_path)
                        app_manager.stop_app()
                        data = {
                            "debug": Debug("The app doesn't have a stop command, nevertheless it was "
                                           "attempted to terminate the app with the kill command, which "
                                           "is not recommended behaviour, and this should be considered "
                                           "a bug.",
                                           state="danger").get_message(),
                        }
            except Exception as ex:
                print("Exception: ", ex)
                data = {
                    "debug": Debug("The command couldn't be run.",
                                   state="danger").get_message(),
                }

        res = HttpResponse(json.dumps(data))
        res.headers["Content-Type"] = "application/json"
        return res

    def handle_request(self, req: HttpRequest):
        """Handle request"""
        if req.method == "POST":
            return self.post(req)
        else:
            raise Exception("This route doesn't handle the given method.")

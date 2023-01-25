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
        res = HttpResponse()
        res.headers["Content-Type"] = "application/json"

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

                # Start
                if command_name == "start":
                    if "start" in commands:
                        app_manager = AppManager(app_path)
                        app_manager.start_app()
                        data = {
                            "debug": Debug("App is starting.",
                                           state="success").get_message(),
                        }
                        res.write(data)
                        return res
                    else:
                        data = {
                            "debug": Debug("The app doesn't have a start command.", error=True,
                                           state="error").get_message(),
                        }
                        res.write(data)
                        return res
                # Stop
                elif command_name == "stop":
                    if "stop" in commands:
                        app_manager = AppManager(app_path)
                        # The app commands are always a priority in AppManager
                        app_manager.stop_app()
                        data = {
                            "debug": Debug("Stop command run successfully.",
                                           state="success").get_message(),
                        }
                        res.write(data)
                        return res
                    else:
                        app_manager = AppManager(app_path)
                        app_manager.stop_app()
                        data = {
                            "debug": Debug("The app doesn't have a stop command, nevertheless it was "
                                           "attempted to terminate the app with the kill command.",
                                           state="danger").get_message(),
                        }
                        res.write(data)
                        return res
                # Restart
                elif command_name == "restart":
                    # Whether a restart command exists or not is not a concern to me
                    app_manager = AppManager(app_path)
                    # The app commands are always a priority in AppManager
                    app_manager.restart_app()
                    data = {
                        "debug": Debug("App restarting.",
                                       state="success").get_message(),
                    }
                    res.write(data)
                    return res
                # Setup
                elif command_name == "setup":
                    # If the setup command exists, it will be run
                    app_manager = AppManager(app_path)
                    app_manager.setup_app()
                    data = {
                        "debug": Debug("Success, if the setup command exists, it will run.",
                                       state="success").get_message(),
                    }
                    res.write(data)
                    return res

                data = {
                    "debug": Debug("Command not found.", error=True,
                                   state="error").get_message(),
                }
                res.write(data)
                return res
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

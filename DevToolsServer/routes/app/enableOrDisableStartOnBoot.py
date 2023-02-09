import json

from django.http import HttpResponse, HttpRequest

from src.submodules.dev_tools_utils.dbs.RepositorySettings import RepositorySettings
from src.submodules.dev_tools_utils.os_stuff.DesktopEntry import DesktopEntry
from src.submodules.dev_tools_utils.data_configuration.ProjectInfo import ProjectInfo


def process_request(request: HttpRequest):
    try:
        if "Content-Type" in request.headers:
            if request.headers["Content-Type"] == "application/json":
                # Reference/s:
                # https://stackoverflow.com/questions/606191/convert-bytes-to-a-string
                body = json.loads(request.body.decode("utf-8"))
                username = body["user"]
                repository_name = body["name"]

                # Update data in repository settings
                rep_settings = RepositorySettings()
                prev_settings = rep_settings.get_repository(username, repository_name)
                start_on_boot = prev_settings["start_on_boot"]
                rep_settings.upsert({
                    "start_on_boot": not start_on_boot,
                }, {
                    "user": username,
                    "name": repository_name,
                })

                # Create .desktop shortcut on autostart folder
                try:
                    # Get app data
                    app_path = prev_settings["path"]
                    project_info = ProjectInfo(app_path)
                    commands = project_info.get_commands()
                    if "globalStart" in commands:
                        # Global start is to start the app from anywhere
                        app_start_command = commands["globalStart"]
                    else:
                        # Cd to the app path and run start
                        app_start_command = f'/bin/bash -c "cd {app_path}; {commands["start"]};"'

                    app_name = repository_name

                    # Create shortcut
                    desktop_entry = DesktopEntry(app_path, app_name, app_start_command)
                    desktop_entry.toggle_start_on_boot()
                except:
                    return {
                        "debug": {
                            "message": "Failed, couldn't create .desktop file",
                            "error": True,
                            "field": "",
                            "state": "error"
                        }
                    }

                data = {
                    "debug": {
                        "message": "Success"
                    },
                }
            else:
                msg = f"Content-Type not supported, given " \
                      f"Content-Type: {request.headers['Content-Type']}"
                data = {
                    "debug": {
                        "message": msg,
                        "error": True,
                        "field": "",
                        "state": "error"
                    }
                }
        else:
            data = {
                "debug": {
                    "message": "Content-Type not given",
                    "error": True,
                    "field": "",
                    "state": "error"
                }
            }
    except Exception as ex:
        if ex is KeyError:
            data = {
                "debug": {
                    "message": f"Key error: {str(ex)}.",
                    "error": True,
                    "field": "",
                    "state": "error"
                }
            }
        else:
            data = {
                "debug": {
                    "message": "Unknown error, it's likely that the table doesn't exist.",
                    "error": True,
                    "field": "",
                    "state": "error"
                }
            }
        print("Exception: ")
        print(ex)
    return data


class Main:
    def __init__(self, route: str):
        self.route = route

    def post(self, request: HttpRequest):
        """Enable start on boot for the given app"""
        # print(f"\n{self.route} -> post():")

        data = process_request(request)

        res = HttpResponse(json.dumps(data))
        res.headers["Content-Type"] = "application/json"
        return res

    def handle_request(self, req: HttpRequest):
        """Handle request"""
        if req.method == "POST":
            return self.post(req)
        else:
            raise Exception("This route doesn't handle the given method.")

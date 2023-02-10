import json

from django.http import HttpRequest

from DevToolsServer.submodules.py_dev_tools_utils.django_utils import DjangoUtils
from DevToolsServer.submodules.py_dev_tools_utils.Debug import Debug
from DevToolsServer.submodules.py_dev_tools_utils.data_configuration.ProjectInfo \
    import ProjectInfo


class Main:
    def __init__(self, route: str):
        self.route = route
        self.debug = False

    def post(self, request: HttpRequest):
        """Get project settings"""
        dj_utils = DjangoUtils(request)
        data = dj_utils.validate_json_content_type(request)

        # If there is "debug" in data it means that there was an error
        if not "debug" in data:
            body: dict = json.loads(request.body.decode("utf-8"))

            # Check if the required data was given
            try:
                # Inform the user in case the data is in a bad format.
                path = body["path"]

                if not path:
                    raise Exception("No path given, or the data is in bad format.")
            except Exception as ex:
                print("Exception: ", ex)
                data = {
                    "debug": Debug("Bad data format a key was not given correctly, the key: "
                                   f"{str(ex)}", error=True,
                                   state="danger").get_message(),
                }
                return dj_utils.get_json_response(data)

            try:
                project_info = ProjectInfo(path)
                return dj_utils.get_json_response({
                    "data": project_info.get_info(),
                })
            except Exception as ex:
                print("Exception: ", ex)
                data = {
                    "debug": Debug("Unknown error.", error=True,
                                   state="error").get_message(),
                }

        return dj_utils.get_json_response(data)

    def get(self, request: HttpRequest):
        raise Exception("This route doesn't handle the given method.")

    def handle_request(self, req: HttpRequest):
        """Handle request"""
        if req.method == "POST":
            return self.post(req)
        elif req.method == "GET":
            return self.get(req)
        else:
            raise Exception("This route doesn't handle the given method.")

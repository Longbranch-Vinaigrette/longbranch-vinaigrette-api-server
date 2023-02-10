import json

from django.http import HttpResponse, HttpRequest

from DevToolsServer.submodules.py_dev_tools_utils.django_utils import DjangoUtils
from DevToolsServer.submodules.py_dev_tools_utils.Debug import Debug
from DevToolsServer.submodules.py_dev_tools_utils.data_configuration.ProjectInfo \
    import ProjectInfo
from DevToolsServer.submodules.py_dev_tools_utils.dbs.RepositorySettings \
    import RepositorySettings


class Main:
    def __init__(self, route: str):
        self.route = route

    def post(self, request: HttpRequest):
        """Check whether an app is DevTools compatible"""
        data = DjangoUtils().validate_json_content_type(request)
        keywordA = "devtoolsCompatible"
        data[keywordA] = False

        # If there is "debug" in data it means that there was an error
        if not "debug" in data:
            body = json.loads(request.body.decode("utf-8"))

            app_path = body["path"]
            try:
                # It raises an exception if the app is not devtools compatible
                project_info = ProjectInfo(app_path)

                data = {
                    "debug": Debug("The app is DevTools compatible.",
                                   state="success").get_message(),
                    keywordA: True,
                }

                # Update data in repository_settings so the website can know when its loaded
                rep_settings = RepositorySettings()
                rep_settings.upsert({ "dev_tools": True, }, { "path": app_path, })
            except Exception as ex:
                print("Exception: ", ex)
                data = {
                    "debug": Debug("The app is not DevTools compatible.",
                                   state="danger").get_message(),
                    keywordA: False,
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

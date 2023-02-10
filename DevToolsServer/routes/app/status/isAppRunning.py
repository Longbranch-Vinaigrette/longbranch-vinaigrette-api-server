import json

from DevToolsServer.submodules.py_dev_tools_utils.django_utils.route_object.Main \
    import Main \
    as RouteHandler
import DevToolsServer.submodules.py_dev_tools_utils.django_utils as dj_utils
from DevToolsServer.submodules.py_dev_tools_utils.app_manager import AppManager


class Main(RouteHandler):
    def __init__(self, route: str):
        super().__init__(route, post_fn=self.post_req)
        self.set_data_dependencies(["path"])

    def post_req(self, request):
        """Post request"""
        body: dict = json.loads(request.body.decode("utf-8"))
        path = body["path"]
        print("Given path: ", path)
        return dj_utils.get_json_response({
            "data": {
                "isAppRunning": AppManager(path).is_app_running(),
            }
        })

import json
import pprint

from src.submodules.dev_tools_utils.django_utils.route_object.Main import Main as RouteHandler
import src.submodules.dev_tools_utils.django_utils as dj_utils
from src.submodules.dev_tools_utils.data_configuration.ProjectSettings import ProjectSettings


class Main(RouteHandler):
    def __init__(self, route: str):
        super().__init__(route, post_fn=self.post_req)
        self.set_data_dependencies(["path"])

    def post_req(self, request):
        """Post request"""
        body: dict = json.loads(request.body.decode("utf-8"))
        path = body["path"]
        app_settings = ProjectSettings(path).get_settings()
        print("App settings: ")
        pprint.pprint(app_settings)

        return dj_utils.get_json_response(app_settings)

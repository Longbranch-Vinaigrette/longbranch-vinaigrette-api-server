import json

from src.submodules.dev_tools_utils.django_utils.route_object.Main import Main as RouteHandler
import src.submodules.dev_tools_utils.django_utils as dj_utils
import src.submodules.dev_tools_utils.data_configuration.LocalData as LocalData


class Main(RouteHandler):
    def __init__(self, route: str):
        super().__init__(route, post_fn=self.post_req)
        self.set_data_dependencies(["path"])

    def post_req(self, request):
        """Post request"""
        body: dict = json.loads(request.body.decode("utf-8"))
        path = body["path"]
        return dj_utils.get_json_response({
            "localData": LocalData(path).load_data()
        })

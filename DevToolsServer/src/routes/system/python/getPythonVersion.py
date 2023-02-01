import sys

from src.submodules.dev_tools_utils.django_utils.route_object.Main import Main as RouteHandler
import src.submodules.dev_tools_utils.django_utils as dj_utils


class Main(RouteHandler):
    def __init__(self, route: str):
        super().__init__(route, get_fn=self.get_req)

    def get_req(self, request):
        """Post request"""
        version_list: list = []
        python_version = sys.version_info
        for i, e in enumerate(python_version):
            if i <= 2:
                version_list.append(e)
        return dj_utils.get_json_response({
            "data": {
                "version": version_list
            }
        })

from src.submodules.dev_tools_utils.django_utils.route_object.Main import Main as RouteHandler
import src.submodules.dev_tools_utils.django_utils as dj_utils

from src.libs.packages import Packages


class Main(RouteHandler):
    def __init__(self, route: str):
        super().__init__(route, get_fn=self.get_req)

    def get_req(self, request):
        """Get installed packages"""
        return dj_utils.get_json_response({
            "data": {
                "packages": Packages().get_packages_list(),
            }
        })

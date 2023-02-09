from django.http import HttpRequest

from src.submodules.dev_tools_utils.django_utils.route_object.Main import Main as RouteHandler
import src.submodules.dev_tools_utils.django_utils as dj_utils
from src.submodules.dev_tools_utils.Debug import Debug
from src.submodules.dev_tools_utils.local_repository_manager import LocalRepositoryManager


class Main(RouteHandler):
    def __init__(self, route: str):
        super().__init__(route, get_fn=self.get_req)

    def get_req(self, request: HttpRequest):
        """Get users locally on /home/USERNAME/.devtools/repositories

        It returns a list of folder names in /home/USERNAME/.devtools/repositories.
        """
        try:
            # Get users
            local = LocalRepositoryManager()
            return dj_utils.get_json_response({
                "users": local.get_users()
            })
        except Exception as ex:
            print("Exception: ", ex)
            data = {
                "debug": Debug(f"Error when trying to fetch data: {ex}.", error=True,
                               state="error").get_message(),
            }
        return dj_utils.get_json_response(data)

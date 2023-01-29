import json

from django.http import HttpResponse, HttpRequest

from src.submodules.dev_tools_utils.Debug import Debug
from src.submodules.dev_tools_utils.local_repository_manager import LocalRepositoryManager


def send_response(data: dict):
    res = HttpResponse(json.dumps(data))
    res.headers["Content-Type"] = "application/json"
    return res


class Main:
    def __init__(self, route: str):
        self.route = route

    def get(self, request: HttpRequest):
        """Get users locally on /home/USERNAME/.devtools/repositories

        It returns a list of folder names in /home/USERNAME/.devtools/repositories.
        """
        # Try to execute the command
        try:
            local = LocalRepositoryManager()
            print("Local: ", local)
            return send_response({
                "users": local.get_users()
            })
        except Exception as ex:
            print("Exception: ", ex)
            data = {
                "debug": Debug("Data not set.", error=True,
                               state="error").get_message(),
            }

        return send_response(data)

    def post(self, request: HttpRequest):
        raise Exception("This route doesn't handle the given method.")

    def handle_request(self, req: HttpRequest):
        """Handle request"""
        if req.method == "POST":
            return self.post(req)
        elif req.method == "GET":
            return self.get(req)
        else:
            raise Exception("This route doesn't handle the given method.")

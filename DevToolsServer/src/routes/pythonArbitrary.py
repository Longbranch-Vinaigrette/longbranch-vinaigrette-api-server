"""Arbitrary implementation on python

This is so I don't have to code a whole programming language, which I might
do later."""
from django.http import HttpRequest

from src.submodules.dev_tools_utils.django_utils.route_object.Main import Main as RouteHandler
import src.submodules.dev_tools_utils.django_utils as dj_utils

from ..libs.python_arbitrary import PythonArbitrary


class Main(RouteHandler):
    def __init__(self, route: str):
        super().__init__(route, post_fn=self.post_req, get_fn=self.get_req)
        self.set_data_dependencies(["path"])

    def post_req(self, request: HttpRequest):
        """Post request"""
        print("Host: ", request.get_host())
        print("Port: ", request.get_port())
        folder_name = request.get_host() + request.get_port()
        print("Folder name: ", folder_name)
        return dj_utils.get_json_response({"status": "Not implemented."})

    def get_req(self, request: HttpRequest):
        """Get request"""
        python_arbitrary = PythonArbitrary(request.get_host())
        return dj_utils.get_json_response({"status": "Not implemented."})

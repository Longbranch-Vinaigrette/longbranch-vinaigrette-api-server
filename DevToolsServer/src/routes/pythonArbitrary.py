"""Arbitrary implementation on python

This is so I don't have to code a whole programming language, which I might
do later."""
import uuid

from django.http import HttpRequest

from src.submodules.dev_tools_utils.django_utils.route_object.Main import Main as RouteHandler
import src.submodules.dev_tools_utils.django_utils as dj_utils

from src.libs.python_arbitrary import PythonArbitrary


class Main(RouteHandler):
    def __init__(self, route: str):
        super().__init__(route, post_fn=self.post_req, mime_type="text/plain")

    def post_req(self, request: HttpRequest):
        """Post request"""
        print(f"Route {self.route}")
        folder_name = request.get_host()
        print("Folder name: ", folder_name)

        return dj_utils.get_json_response({"status": "Not implemented."})

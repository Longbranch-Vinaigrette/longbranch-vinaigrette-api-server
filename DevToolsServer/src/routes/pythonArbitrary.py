"""Arbitrary implementation on python

This is so I don't have to code a whole programming language, which I might
do later."""
import uuid

from django.http import HttpRequest

from src.submodules.dev_tools_utils.django_utils.route_object.Main import Main as RouteHandler
import src.submodules.dev_tools_utils.django_utils as dj_utils
from src.submodules.dev_tools_utils.Debug import Debug

from src.libs.python_arbitrary import PythonArbitrary


class Main(RouteHandler):
    def __init__(self, route: str):
        super().__init__(route, post_fn=self.post_req, mime_type="text/plain")

    def post_req(self, request: HttpRequest):
        """Post request"""
        folder_name = request.get_host()

        script = request.body.decode("utf-8")
        arbitrary = PythonArbitrary(
            folder_name,
            str(uuid.uuid4()),
            script,
            arguments=[
                {
                    "host": request.get_host(),
                    "port": request.get_port(),
                    "route": request.get_full_path()
                },
                {
                    "Content-Type": "text/plain"
                }
            ],
            remove_at_the_end=False
        )
        result = arbitrary.mkfile_and_run()
        if isinstance(result, list) or isinstance(result, dict):
            return dj_utils.get_json_response(result)
        else:
            return dj_utils.get_json_response(
                Debug().get_full_message(
                    "The code was run, but no result was returned from it."
                    "This may be an error too.",
                    error=False,
                    state="success"
                )
            )

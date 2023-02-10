import json

from DevToolsServer.submodules.py_dev_tools_utils.django_utils.route_object.Main \
    import Main \
    as RouteHandler
import DevToolsServer.submodules.py_dev_tools_utils.django_utils as dj_utils
from DevToolsServer.submodules.py_dev_tools_utils.dbs.SettingsTable import SettingsTable
from DevToolsServer.submodules.py_dev_tools_utils.Debug import Debug


class Main(RouteHandler):
    def __init__(self, route: str):
        super().__init__(route, post_fn=self.post_req)
        self.set_data_dependencies(["key", "value"])

    def post_req(self, request):
        """Post request"""
        body: dict = json.loads(request.body.decode("utf-8"))
        key = body["key"]
        value = body["value"]

        # Upsert the data
        table = SettingsTable()
        table.upsert({
            "key": key,
            "value": value
        }, {
            "key": key,
        })

        return dj_utils.get_json_response(Debug("Success.", error=False).get_full_message())

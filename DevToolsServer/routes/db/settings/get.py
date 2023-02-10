import json

from DevToolsServer.submodules.py_dev_tools_utils.django_utils.route_object.Main \
    import Main \
    as RouteHandler
import DevToolsServer.submodules.py_dev_tools_utils.django_utils \
    as dj_utils
from DevToolsServer.submodules.py_dev_tools_utils.dbs.SettingsTable \
    import SettingsTable


class Main(RouteHandler):
    def __init__(self, route: str):
        super().__init__(route, post_fn=self.post_req)

        # Note the data dependencies
        self.set_data_dependencies(["key"])

    def post_req(self, request):
        """Post request"""
        body: dict = json.loads(request.body.decode("utf-8"))
        key = body["key"]
        print("Get key: ", key)

        # Upsert the data
        table = SettingsTable()
        data = table.get(key)
        print("Data: ", data)

        return dj_utils.get_json_response({"value": data, })

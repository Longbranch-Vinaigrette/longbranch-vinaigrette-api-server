"""
Create app
python3.10 manage.py startapp APP_NAME
"""
import os
import pprint

from DevToolsServer.submodules.py_dev_tools_utils.dynamic_imports.django_routes \
    import DjangoRoutes


routes_path = f"{os.getcwd()}{os.path.sep}DevToolsServer{os.path.sep}routes"
djroutes = DjangoRoutes(routes_path, handle_request=False)
urlpatterns = djroutes.get_routes_as_urlpatterns()

debug = False
if debug:
    print("Urlpatterns:")
    pprint.pprint(urlpatterns)

import json

from django.http import HttpRequest

from src.submodules.dev_tools_utils.django_utils import DjangoUtils
from src.submodules.dev_tools_utils.Debug import Debug
from src.submodules.dotenv5 import DotEnv5


class Main:
    def __init__(self, route: str):
        self.route = route
        self.debug = False

    def post(self, request: HttpRequest):
        """Insert or replace .env variables"""
        dj_utils = DjangoUtils(request)
        data = dj_utils.validate_json_content_type(request)

        # If there is "debug" in data it means that there was an error
        if not "debug" in data:
            body: dict = json.loads(request.body.decode("utf-8"))

            # Check if the required data was given
            try:
                # Inform the user in case the data is in a bad format.
                # Set error message to give to the user
                msg = "Key error, path was not given."

                # Get the path
                path = body["path"]
                if not path or not isinstance(path, str):
                    msg = "No path given, path is not a string or bad format."
                    raise Exception(msg)

                # Set error message to give to the user
                msg = "Key error, env was not given."

                # Get the env variables
                env = body["env"]
                if not env or not isinstance(env, dict):
                    msg = "No env given, env is not an object/dictionary or bad format."
                    raise Exception(msg)
            except Exception as ex:
                print("Exception: ", ex)
                data = {
                    "debug": Debug(msg, error=True,
                                   state="danger").get_message(),
                }
                return dj_utils.get_json_response(data)

            try:
                # DotEnv5
                dotenv = DotEnv5(path=path)

                # Upsert data
                dotenv.upsert_dot_env(env)

                return dj_utils.get_json_response({
                    "debug": Debug("Data upserted(Updated or Inserted).", state="success").get_message()
                })
            except Exception as ex:
                print("Exception: ", ex)
                data = {
                    "debug": Debug("Unknown error.", error=True,
                                   state="error").get_message(),
                }

        return dj_utils.get_json_response(data)

    def get(self, request: HttpRequest):
        raise Exception("This route doesn't handle the given method.")

    def handle_request(self, req: HttpRequest):
        """Handle request"""
        if req.method == "POST":
            return self.post(req)
        elif req.method == "GET":
            return self.get(req)
        else:
            raise Exception("This route doesn't handle the given method.")

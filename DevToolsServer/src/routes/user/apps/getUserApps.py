import json

from django.http import HttpResponse, HttpRequest

from src.submodules.dev_tools_utils.django_utils import DjangoUtils
from src.submodules.dev_tools_utils.Debug import Debug
from src.submodules.dev_tools_utils.local_repository_manager import LocalRepositoryManager
from src.submodules.dev_tools_utils.dbs.RepositorySettingsTable import RepositorySettingsTable


def send_response(data: dict):
    res = HttpResponse(json.dumps(data))
    res.headers["Content-Type"] = "application/json"
    return res


def get_item_index(l, value):
    """Get the index of an item in a given list"""
    try:
        for i, val in enumerate(l):
            if val == value:
                return i
    except:
        return None


class Main:
    def __init__(self, route: str):
        self.route = route
        self.debug = True

    def post(self, request: HttpRequest):
        """Get user apps"""
        data = DjangoUtils().validate_json_content_type(request)

        # If there is "debug" in data it means that there was an error
        if not "debug" in data:
            body: dict = json.loads(request.body.decode("utf-8"))

            # Check if the required data was given
            try:
                # Inform the user in case the data is in a bad format.
                user = body["user"]

                if not user:
                    raise Exception("No user given, or the data is in bad format.")
            except Exception as ex:
                print("Exception: ", ex)
                data = {
                    "debug": Debug("Bad data format a key was not given correctly, the key: "
                                   f"{str(ex)}",
                                   state="danger").get_message(),
                }
                return send_response(data)

            # Try to execute the command
            try:
                # Start the database connection
                repository_settings_table = RepositorySettingsTable()
                old_user_repositories = repository_settings_table.get_user_repositories(user)
                old_repositories_names = [repository["name"] for repository in old_user_repositories]

                # Update data in case there's a new repository not register in
                # repository settings
                updated_repository_info = LocalRepositoryManager().get_user_repos_info(user)
                if self.debug:
                    print(f"User: {user}")
                    print("Repositories: ", old_repositories_names)
                for repository in updated_repository_info:
                    name = repository["name"]
                    if self.debug:
                        print(f"--- Repository name: {name}")

                    # Check if the name is in the list of old_repositories_name
                    if name in old_repositories_names:
                        if self.debug:
                            print("\t[Yes] Name does exist in old repositories")
                        # Remove that name from the list
                        repository_index = get_item_index(old_repositories_names, name)
                        if self.debug:
                            print(f"\tIts index is {str(repository_index)}")
                            print(f"\tIts value is {old_repositories_names[repository_index]}")
                        if repository_index is not None:
                            del old_repositories_names[repository_index]
                    else:
                        if self.debug:
                            print("\t[No] Name does exist in old repositories")
                            print("\tInserting it.")

                        # The name wasn't found, insert it
                        repository_settings_table.upsert(repository, {
                            "user": user,
                            "name": name,
                        })

                # Remove the repositories that weren't found on the RepositorySettingsTable
                if self.debug:
                    print("Repositories not found: ", old_repositories_names)
                for name in old_repositories_names:
                    if self.debug:
                        print(f"Deleting: {user}/{name}")
                    repository_settings_table.delete_row(user, name)


                return send_response(data)
            except Exception as ex:
                print("Exception: ", ex)
                data = {
                    "debug": Debug("Data not set.", error=True,
                                   state="error").get_message(),
                }

        return send_response(data)

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

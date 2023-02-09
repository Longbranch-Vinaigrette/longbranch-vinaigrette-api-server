import os

from .DotEnvLines import DotEnvLines
from .DotEnvParser import DotEnvParser


class DotEnvEncoder:
    def __init__(self,
                 data: dict,
                 path: str = os.getcwd(),
                 with_comments: bool = False,
                 with_endlines: bool = True,
                 debug: bool = False):
        self.data = data
        self.path = path
        self.with_comments = with_comments
        self.with_endlines = with_endlines
        self.debug = debug

        if self.debug:
            print("\nDotEnvEncoder -> __init__():")
            print("Given path: ", self.path)

    def dot_env_encode_data(self, data: dict):
        """Get encoded data"""
        if self.debug:
            print(f"\nDotEnvEncoder -> dot_env_encode_data():")

        encoded_environment_variables = ""

        for key, value in data.items():
            key: str = key

            # It's a comment
            if key.startswith(DotEnvLines.comments_keyword):
                encoded_environment_variables += value
                continue

            # It's an endline
            if key.startswith(DotEnvLines.endlines_keyword):
                encoded_environment_variables += value
                continue

            # It's a variable
            encoded_environment_variables += f"{key}={value}\n"

        return encoded_environment_variables

    def upsert_dot_env(self):
        """Upsert environment variables"""
        if self.debug:
            print(f"\nDotEnvEncoder -> upsert_dot_env():")

        # Merge given data + data in the .env file
        dot_env_parser = DotEnvParser(
            path=self.path,
            with_comments=self.with_comments,
            with_endlines=self.with_endlines,
            debug=self.debug)
        previous_dot_env_data: dict = dot_env_parser.get_dot_env_data()
        dot_env_data: dict = {
            **previous_dot_env_data,
            **self.data,
        }

        # Encode data
        encoded_data = self.dot_env_encode_data(dot_env_data)

        if self.debug:
            print("Encoded data: ", encoded_data)

        # Save the data
        dot_env_path = f"{self.path}{os.path.sep}.env"
        with open(dot_env_path, "w") as f:
            f.write(encoded_data)
            if self.debug:
                print(f"Data written to: {dot_env_path}")

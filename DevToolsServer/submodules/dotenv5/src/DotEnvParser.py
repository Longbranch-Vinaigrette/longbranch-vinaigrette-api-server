import os
import pprint

from .DotEnvLines import DotEnvLines


class DotEnvParser:
    raw_env_data: str = ""
    parsed_data: dict = {}

    def __init__(self,
                 path: str = os.getcwd(),
                 with_comments: bool = False,
                 with_endlines: bool = False,
                 debug: bool = False,
                 ):
        self.path = path
        self.with_comments = with_comments
        self.with_endlines = with_endlines
        self.debug = debug

    def get_dot_env_raw(self) -> str:
        """Get raw data on .env in the project root"""
        if self.debug:
            print("\nDotEnvParser -> get_dot_env_raw():")
        try:
            with open(f"{self.path}{os.path.sep}.env") as f:
                self.raw_env_data = f.read()
                return self.raw_env_data
        except:
            return ""

    def parse_dot_env(self, raw_data: str) -> dict:
        """Convert dot env raw data into dictionary data"""
        if self.debug:
            print("\nDotEnvParser -> parse_dot_env():")
        env_vars: dict = {}

        # Use cached data if possible
        if len(list(env_vars.keys())) > 0:
            if self.debug:
                print("Cached data found, returning it.")
            return self.parsed_data

        if self.debug:
            print("Cached data not found, parsing data.")

        # Raw data might be an empty string
        if raw_data:
            lines_list: list = raw_data.splitlines()
            if self.debug:
                print("Lines list: ")
                pprint.pprint(lines_list)
            dot_env_lines = DotEnvLines(
                lines_list,
                with_comments=self.with_comments,
                with_endlines=self.with_endlines,
                debug=self.debug)
            env_vars = dot_env_lines.parse_lines()

        if self.debug:
            print("Result: ", env_vars)
        self.parsed_data = env_vars
        return env_vars

    def get_dot_env_data(self) -> dict:
        """Get dot env data as a dictionary"""
        if self.debug:
            print("\nDotEnvParser -> get_dot_env_data():")
        raw_data: str = self.get_dot_env_raw()
        return self.parse_dot_env(raw_data)

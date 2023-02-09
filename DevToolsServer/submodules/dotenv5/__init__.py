import os

from .src.DotEnvLine import DotEnvLine
from .src.DotEnvLines import DotEnvLines
from .src.DotEnvParser import DotEnvParser
from .src.DotEnvEncoder import DotEnvEncoder


class DotEnv5:
    def __init__(self, path: str = os.getcwd(), debug: bool = False):
        self.path = path
        self.debug = debug

    def get_parsed_dot_env(self, with_comments: bool = False, with_endlines: bool = False):
        """Get parsed data in .env"""
        if self.debug:
            print("\nDotEnv5 -> get_parsed_dot_env():")
        dot_env_parser = DotEnvParser(
            path=self.path,
            with_comments=with_comments,
            with_endlines=with_endlines,
            debug=self.debug)
        return dot_env_parser.get_dot_env_data()

    def parse_dot_env(self, raw_data: str) -> dict:
        """Parse dot env"""
        if self.debug:
            print("\nDotEnv5 -> parse_dot_env():")
        dot_env_parser = DotEnvParser()
        return dot_env_parser.parse_dot_env(raw_data)

    def encode_dot_env(self, data: dict) -> str:
        """Encode dictionary"""
        if self.debug:
            print("\nDotEnv5 -> encode_dot_env():")
        dot_env_encoder = DotEnvEncoder(data, path=self.path, debug=self.debug)
        return dot_env_encoder.dot_env_encode_data(data)

    def upsert_dot_env(self, data: dict):
        """Insert or replace data in the given path"""
        if self.debug:
            print("\nDotEnv5 -> upsert_dot_env():")
        dot_env_encoder = DotEnvEncoder(
            data,
            path=self.path,
            with_comments=True,
            with_endlines=True,
            debug=self.debug)
        return dot_env_encoder.upsert_dot_env()

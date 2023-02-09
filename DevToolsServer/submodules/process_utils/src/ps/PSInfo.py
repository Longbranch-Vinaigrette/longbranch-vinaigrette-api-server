class PSInfo:
    def __init__(self, info: str, debug: bool = False):
        self.info = info
        self.debug = debug

    def get_info(self):
        return self.info

    def set_info(self, info: str):
        self.info = info

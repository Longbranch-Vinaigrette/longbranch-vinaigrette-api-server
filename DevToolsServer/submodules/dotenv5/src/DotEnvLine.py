class DotEnvLine:
    line_continuation_character = "\\"

    def __init__(self, line: str):
        self.line = line

    def get_var_name(self) -> str:
        """Get the var name"""
        return self.line.split("=")[0]

    def get_value(self) -> str:
        """Get the value"""
        return self.line.split("=", 1)[1]

    def is_line_empty(self) -> bool:
        """Check if the line is empty or not"""
        if self.line:
            return False
        else:
            return True

    def does_line_continues(self) -> bool:
        """Check if the line continue or not"""
        if self.line.endswith(self.line_continuation_character):
            return True
        else:
            return False

    def is_line_a_comment(self) -> bool:
        """Check if the line is a comment"""
        if self.line.startswith("#"):
            return True
        else:
            return False

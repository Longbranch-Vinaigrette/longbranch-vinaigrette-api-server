import os
import uuid

from __init__ import PythonArbitrary

# Import code
with open(f"{os.getcwd()}{os.path.sep}test_user_code.py") as f:
    code = f.read()

# Instantiate arbitrary
arbitrary = PythonArbitrary(
    "192.168.1.1:42356",
    str(uuid.uuid4()),
    code,
    arguments=[
        {
            "origin": "http://perseverancia.ar",
            "host": "192.168.1.1:42356",
            "port": "42356"
        },
        {
            "Content-Type": "application/json"
        },
        {
            "path": "/home/USERNAME/.devtools/repositories"
        }
    ]
)
result = arbitrary.mkfile_and_run()
print("Result given: ", result)

import os
import pprint

from __init__ import Gitconfig

config = Gitconfig(f"{os.getcwd()}/.gitconfig")
print("Parsed gitconfig: ")
pprint.pprint(config.loads())
print("Adding some fields: ")
config.data["new_field"] = "something"

# Add a new field to every 'region'
for region in config.regions:
    config.data[region]["new_field"] = "Hello there"

# Are there submodules?
config.has_submodules()

config.dumps(f"{os.getcwd()}/.gitresult")

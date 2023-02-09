import pprint

from __init__ import Packages

packages = Packages(debug=True)

print("Packages as a dictionary: ")
pprint.pprint(packages.get_packages_list())

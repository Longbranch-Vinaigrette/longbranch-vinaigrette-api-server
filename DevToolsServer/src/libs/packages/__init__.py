import pprint
import subprocess


class Packages:
    packages: list = []

    def __init__(self, debug: bool = False):
        self.debug = debug

        if self.debug:
            print("\nPackages -> __init__():")

        raw_cmds = f"""
                    pip3 freeze
                    """
        parsed_cmds = bytes(raw_cmds, 'utf8')

        # For subprocess.Popen()
        # It's recommended to use fully qualified paths, or
        # some things might be overriden
        process: subprocess.Popen = subprocess.Popen(["/bin/sh"],
                                                     stdin=subprocess.PIPE,
                                                     stdout=subprocess.PIPE,
                                                     shell=True)
        out, err = process.communicate(parsed_cmds)
        raw_packages_listed = out.decode("utf-8")
        self.raw_packages_listed = raw_packages_listed
        if self.debug:
            print("Raw packages listed: ", raw_packages_listed)

    def get_packages_list(self) -> list:
        """Get packages list"""
        if self.debug:
            print("\nPackages -> get_packages_list():")

        # The list looks like this
        # bcrypt==3.2.0
        # beautifulsoup4==4.10.0
        # beniget==0.4.1
        lines: list = self.raw_packages_listed.splitlines()
        packages_list: list = []
        for line in lines:
            # Let's split by the '=='
            package_name, package_version = line.split("==")

            # Append package to the list
            packages_list.append({
                "name": package_name,
                "version": package_version
            })

        # Cache packages
        self.packages = packages_list

        if self.debug:
            print("Result: ")
            pprint.pprint(packages_list)
        return packages_list

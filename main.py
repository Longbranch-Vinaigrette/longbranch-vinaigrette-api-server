import argparse
import os
import signal
import subprocess

from DevToolsServer.src.submodules.dev_tools_utils.app_manager.SelfAppManager import SelfAppManager


# Instantiate the parser
parser = argparse.ArgumentParser(description="DevTools description")
parser.add_argument("--start", action="store_true",
                    help="Start server in the background.")
parser.add_argument("--stop", action="store_true",
                    help="Stop server in the background.")

# Parse args
args = parser.parse_args()


# Reference/s:
# https://stackoverflow.com/questions/320232/ensuring-subprocesses-are-dead-on-exiting-python-program
# Create new process group, become its leader
os.setpgrp()


# Reference/s
# https://stackoverflow.com/questions/1112343/how-do-i-capture-sigint-in-python
def signal_handler(sig, frame):
    # subprocess.run(["/bin/bash", "-c", f"cd {os.getcwd()}; echo 'Soft shutdown' > ./exit.txt"])
    os.killpg(0, signal.SIGTERM)


signal.signal(signal.SIGTERM, signal_handler)

start_cmds = f"""
cd DevToolsServer && python3.10 manage.py runserver 37000;
"""
self_app_management = SelfAppManager(start_cmds)

# App operations
if args.start:
    self_app_management.start_app()

if args.stop:
    self_app_management.stop_app()


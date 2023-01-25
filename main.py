import argparse
import os
import signal

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
    os.killpg(0, signal.SIGKILL)


signal.signal(signal.SIGTERM, signal_handler)


# Start or stop the app
try:
    start_cmds = f"""
    cd DevToolsServer && python3.10 manage.py runserver 37000;
    """

    self_app_management = SelfAppManager(start_cmds)
    if args.start:
        self_app_management.start_app()

    if args.stop:
        self_app_management.stop_app()
finally:
    # Not usually executed, unreliable
    os.killpg(0, signal.SIGKILL)

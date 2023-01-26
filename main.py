import argparse
import os
import signal


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
    if args.start:
        pass

    if args.stop:
        pass
finally:
    # Not usually executed, unreliable
    os.killpg(0, signal.SIGKILL)

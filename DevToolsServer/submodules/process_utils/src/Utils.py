import subprocess


def run_subprocess(cmd: str, debug: bool = False):
    """Run a subprocess"""
    try:
        process = subprocess.run([
            "bash", "-c", cmd
        ],
            check=True,  # If there's an error raise an exception
            capture_output=True,  # Store output on process.stdout
        )

        # Store data
        process_info = process.stdout.decode("utf-8")
        return process_info
    except FileNotFoundError as exc:
        if debug:
            print(f"Process failed because the executable could not be found.\n{exc}")
    except subprocess.CalledProcessError as exc:
        if debug:
            print(
                f"Process failed because did not return a successful return code. "
                f"Returned {exc.returncode}\n{exc}"
            )
    except subprocess.TimeoutExpired as exc:
        if debug:
            print(f"Process timed out.\n{exc}")
    return None

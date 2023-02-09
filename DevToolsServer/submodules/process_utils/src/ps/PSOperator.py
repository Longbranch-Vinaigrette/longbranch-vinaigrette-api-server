from .. import Utils


def get_cwd_by_pid(pid: str):
    """Get cwd by pid"""
    cwd = Utils.run_subprocess(f"readlink /proc/{pid}/cwd")

    if cwd:
        # The [:-1] is because it comes with a f*ing space at the end, I've wasted 20 minutes
        # of my life trying to figure it out.
        cwd = cwd[:-1]
    return cwd

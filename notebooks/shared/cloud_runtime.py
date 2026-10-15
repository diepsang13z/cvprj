"""Cloud-only entry guard and isolated artifact directories (stdlib only)."""
import os
from datetime import datetime, timezone
from pathlib import Path
from contextlib import contextmanager, redirect_stdout, redirect_stderr
import sys
import traceback


def require_cloud():
    # Hosted-runtime markers, not import google.colab (also installable locally).
    colab = bool(os.environ.get("COLAB_RELEASE_TAG")) and Path("/content").is_dir()
    kaggle = bool(os.environ.get("KAGGLE_KERNEL_RUN_TYPE")) and Path("/kaggle/working").is_dir()
    if not (colab or kaggle):
        raise RuntimeError("RULES.md §8: chỉ chạy trên Colab/Kaggle hosted runtime; cấm máy cá nhân/local runtime.")


def new_run(output_root, job):
    require_cloud()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    target = Path(output_root) / job / stamp
    target.mkdir(parents=True, exist_ok=False)
    return target


@contextmanager
def job_log(output_root, job):
    """Capture printed metrics and errors beside this job's artifacts."""
    folder = new_run(output_root, job)
    class Tee:
        def __init__(self, terminal, logfile):
            self.terminal, self.logfile = terminal, logfile

        def write(self, text):
            self.terminal.write(text)
            self.logfile.write(text)
            self.logfile.flush()
            return len(text)

        def flush(self):
            self.terminal.flush()
            self.logfile.flush()

    with (folder / "run.log").open("w", encoding="utf-8") as logfile:
        with redirect_stdout(Tee(sys.stdout, logfile)), redirect_stderr(Tee(sys.stderr, logfile)):
            try:
                yield folder
            except BaseException:
                traceback.print_exc()
                raise

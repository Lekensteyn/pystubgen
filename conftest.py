
import sys

def pytest_ignore_collect(path, config):
    basename = path.basename
    # Ignore files with 'py3' in their name on older Python versions
    if sys.version_info[0] < 3 and "py3" in basename:
        return True
    return False

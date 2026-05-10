import os
import sys

tests_dir = os.path.join(os.path.dirname(__file__), "tests")
if tests_dir not in sys.path:
    sys.path.append(tests_dir)

from tests.utils import *  # noqa: F401,F403

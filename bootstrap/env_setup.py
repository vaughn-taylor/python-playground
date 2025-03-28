import os
import sys

def configure_paths():
    current_dir = os.path.dirname(__file__)
    root_dir = os.path.abspath(os.path.join(current_dir, ".."))
    if root_dir not in sys.path:
        sys.path.insert(0, root_dir)
    return root_dir

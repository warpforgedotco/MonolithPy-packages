import __mp__
import glob
import os
import shutil
import sys


def run(wheel_directory):
    yaml_root = __mp__.find_dep_root("yaml")
    env = os.environ.copy()
    # Without libyaml PyYAML quietly installs as pure Python; make that an error.
    env["PYYAML_FORCE_LIBYAML"] = "1"
    env["CPATH"] = os.path.join(yaml_root, "include") + os.pathsep + env.get("CPATH", "")
    env["LIBRARY_PATH"] = os.path.join(yaml_root, "lib") + os.pathsep + env.get("LIBRARY_PATH", "")

    __mp__.run_with_output(sys.executable, "-m", "build", "-w", "--no-isolation", "-o", ".", env=env)

    wheel_location = glob.glob("pyyaml-*.whl")[0]
    wheel_name = os.path.basename(wheel_location)
    shutil.copy(wheel_location, os.path.join(wheel_directory, wheel_name))
    return os.path.join(wheel_directory, wheel_name)

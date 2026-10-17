import __mp__
from typing import *

import os
import platform
import stat
from wheel.wheelfile import WheelFile


def run(wheel_directory):
    archive = "ninja-linux-aarch64.zip" if platform.machine() == "aarch64" else "ninja-linux.zip"
    __mp__.download_extract("https://github.com/ninja-build/ninja/releases/download/v1.12.1/" + archive, os.getcwd())
    os.chmod(os.path.join(os.getcwd(), "ninja"), os.stat(os.path.join(os.getcwd(), "ninja")).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    result_wheel = os.path.join(wheel_directory, __mp__.get_wheel_name("mpy-tool-ninja", "1.12.1"))
    with WheelFile(result_wheel, 'w') as w:
        __mp__.add_wheel_manifest(w, "mpy-tool-ninja", "1.12.1")
        __mp__.add_wheel_build_tool(w, "ninja", os.path.join(os.getcwd(), "ninja"))

    return result_wheel

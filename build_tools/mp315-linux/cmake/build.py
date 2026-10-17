import __mp__
from typing import *

import glob
import os
import platform
import tempfile
from wheel.wheelfile import WheelFile


def run(wheel_directory):
    # The source is the x86_64 release; other machines get theirs.
    tool_dir = os.getcwd()
    if platform.machine() == "aarch64":
        tool_dir = tempfile.mkdtemp()
        __mp__.download_extract("https://github.com/Kitware/CMake/releases/download/v3.31.4/cmake-3.31.4-linux-aarch64.tar.gz",
                                tool_dir)
        tool_dir = glob.glob(os.path.join(tool_dir, "cmake-*"))[0]

    result_wheel = os.path.join(wheel_directory, __mp__.get_wheel_name("mpy-tool-cmake", "3.31.4"))
    with WheelFile(result_wheel, 'w') as w:
        __mp__.add_wheel_manifest(w, "mpy-tool-cmake", "3.31.4")
        __mp__.add_wheel_build_tool(w, "cmake", os.path.join(tool_dir, "*"))

    return result_wheel

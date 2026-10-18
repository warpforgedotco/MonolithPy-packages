import __mp__
from typing import *

import os
from wheel.wheelfile import WheelFile


def run(wheel_directory):
    src_dir = os.getcwd()

    os.environ["PATH"] = os.path.dirname(__mp__.find_build_tool_exe("ninja", "ninja")) + os.pathsep + os.environ["PATH"]

    build_dir = os.path.join(src_dir, "build")
    os.mkdir(build_dir)
    os.chdir(build_dir)

    install_dir = os.path.join(src_dir, "install")
    os.mkdir(install_dir)

    # libyaml 0.2.5 asks for CMake 3.0, which CMake 4 no longer accepts.
    __mp__.run_build_tool_exe("cmake", "cmake", "-G", "Ninja",
                              "-DCMAKE_BUILD_TYPE=Release", "-DBUILD_SHARED_LIBS=OFF",
                              "-DBUILD_TESTING=OFF", "-DCMAKE_POLICY_VERSION_MINIMUM=3.5",
                              "-DCMAKE_INSTALL_PREFIX=" + install_dir, "-DCMAKE_INSTALL_LIBDIR=lib", src_dir)
    __mp__.run_build_tool_exe("ninja", "ninja", "install")

    result_wheel = os.path.join(wheel_directory, __mp__.get_wheel_name("mpy_dep_yaml", "0.2.5"))
    with WheelFile(result_wheel, 'w') as w:
        __mp__.add_wheel_manifest(w, "mpy-dep-yaml", "0.2.5")
        __mp__.add_wheel_dep_libs(w, "yaml", os.path.join(install_dir, "lib", "*.a"))
        __mp__.add_wheel_dep_include(w, "yaml", os.path.join(install_dir, "include", "*"))

    return result_wheel

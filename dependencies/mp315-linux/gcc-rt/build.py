import __mp__
from typing import *

import os
import subprocess
from wheel.wheelfile import WheelFile


def run(wheel_directory):
    # The static Fortran runtime of the system gfortran, which built the
    # Fortran code that the interpreter relink links in.
    libs = []
    for name in ["libgfortran.a", "libquadmath.a"]:
        path = subprocess.check_output(["gfortran", "-print-file-name=" + name], text=True).strip()
        if not os.path.isabs(path) or not os.path.isfile(path):
            raise FileNotFoundError(f"gfortran has no {name}")
        libs.append(path)

    result_wheel = os.path.join(wheel_directory, __mp__.get_wheel_name("mpy-dep-gcc-rt", "15"))
    with WheelFile(result_wheel, 'w') as w:
        __mp__.add_wheel_manifest(w, "mpy-dep-gcc-rt", "15")
        __mp__.add_wheel_dep_libs(w, "gcc-rt", *libs)

    return result_wheel

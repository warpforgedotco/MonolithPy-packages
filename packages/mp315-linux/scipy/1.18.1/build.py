import __mp__
import glob
import shutil
import sys
import os
from tempfile import TemporaryDirectory

import setuptools.build_meta
from wheel.wheelfile import WheelFile


def run(wheel_directory):
    __mp__.run_with_output("patch", "-p1", "-ui",
                           os.path.join(os.path.dirname(__file__), "scipy-static-patch.patch"))

    os.environ["PATH"] = (os.path.dirname(__mp__.find_build_tool_exe("cmake", "cmake")) + os.pathsep +
                   os.path.dirname(__mp__.find_build_tool_exe("ninja", "ninja")) + os.pathsep + os.environ["PATH"])
    # The system gfortran; gcc-rt ships its static runtime for the relink.
    os.environ["FC"] = shutil.which("gfortran")
    # meson finds OpenBLAS by linking against it; the compiler searches
    # LIBRARY_PATH and CPATH.
    os.environ["LIBRARY_PATH"] = os.pathsep.join(filter(None, [__mp__.find_dep_libs("openblas"),
                                                               os.environ.get("LIBRARY_PATH")]))
    os.environ["CPATH"] = os.pathsep.join(filter(None, [__mp__.find_dep_include("openblas"),
                                                        os.environ.get("CPATH")]))
    os.environ["CMAKE_PREFIX_PATH"] = __mp__.find_dep_root("openblas")
    os.environ["FFLAGS"] = "-static-libgcc"
    os.environ["PKG_CONFIG"] = "/disabled"
    # The static OpenBLAS needs libm, and libpthread, which glibc before
    # 2.34 keeps out of libc; meson's OpenBLAS check links only -lopenblas.
    os.environ["LDFLAGS"] = " ".join(filter(None, [os.environ.get("LDFLAGS"), "-pthread -lm"]))

    job_args = []
    if "MP_JOBS" in os.environ:
        job_args += ["-Ccompile-args=-j" + os.environ["MP_JOBS"]]
    __mp__.run(sys.executable, "-m", "build", "-w", "--no-isolation",
               "-Csetup-args=-Dprefer_static=True", "-Csetup-args=-Dblas=openblas",
               "-Csetup-args=-Dlapack=openblas",
               "-Csetup-args=-Dfortran_link_args=-static-libgcc",
               "-Cbuild-dir=build",
               *job_args)

    wheel_location = glob.glob(os.path.join("dist", "scipy-*.whl"))[0]

    wheel_files = []
    with TemporaryDirectory() as tmpdir:
        with WheelFile(wheel_location) as wf:
            for filename in wf.namelist():
                wheel_files.append(filename)
                wf.extract(filename, tmpdir)
        __mp__.analyze_and_rename_library_symbols(tmpdir,
                                                  "scipy",
                                                  symbol_mapping={
                                                      "d1mach_": {
                                                          "use_definition_from": "libmach_lib.a"
                                                      },
                                                      "cdotc_": {
                                                          "use_definition_from": "libarnaud.a",
                                                          "for_libraries": ["libdummy_g77_abi_wrappers.a"]
                                                      },
                                                      "zdotc_": {
                                                          "use_definition_from": "libarnaud.a",
                                                          "for_libraries": ["libdummy_g77_abi_wrappers.a"]
                                                      }},
                                                  write_debug=True
                                                  )

        with WheelFile(wheel_location, 'w') as wf:
            for filename in wheel_files:
                wf.write(os.path.join(tmpdir, filename), filename)

    wheel_name = os.path.basename(wheel_location)
    shutil.copy(wheel_location, os.path.join(wheel_directory, wheel_name))
    return os.path.join(wheel_directory, wheel_name)

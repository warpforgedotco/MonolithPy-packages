import __mp__
import glob
import os
import shutil
import sys


# propcache builds its C extensions only on CPython, which it tells apart from
# PyPy by sys.implementation.name; MonolithPy's is "monolithpy", so without
# this it installs as pure Python.
#
# It also ships the extension it builds in place as package data, which
# lists *.so; under MonolithPy the extension is a static *.a.
EDITS = [
    ('packaging/pep517_backend/_backend.py', '_system_implementation.name == "cpython"', '_system_implementation.name in ("cpython", "monolithpy")'),
    ('setup.cfg', '[options.package_data]\n* = \n\t*.so\n', '[options.package_data]\n* = \n\t*.so\n\t*.a\n'),
]


def run(wheel_directory):
    for path, old, new in EDITS:
        with open(path) as f:
            text = f.read()
        if old not in text:
            raise RuntimeError(f"{path} no longer has {old!r}; update this recipe")
        with open(path, "w") as f:
            f.write(text.replace(old, new))

    __mp__.run_with_output(sys.executable, "-m", "build", "-w", "--no-isolation", "-o", ".")

    wheel_location = glob.glob('propcache-*.whl')[0]
    wheel_name = os.path.basename(wheel_location)
    shutil.copy(wheel_location, os.path.join(wheel_directory, wheel_name))
    return os.path.join(wheel_directory, wheel_name)

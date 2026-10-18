"""Checks that PyYAML's libyaml bindings are linked in."""
import sys

import yaml

assert yaml.__with_libyaml__
assert "yaml._yaml" in sys.builtin_module_names
assert yaml.load("a: [1, 2]", Loader=yaml.CSafeLoader) == {"a": [1, 2]}
assert yaml.dump({"a": 1}, Dumper=yaml.CSafeDumper) == "a: 1\n"

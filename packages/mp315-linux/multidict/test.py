"""Checks that the C extensions are linked in, not the pure-Python fallback."""
import multidict, multidict._multidict
assert multidict.MultiDict(a=1)['a'] == 1

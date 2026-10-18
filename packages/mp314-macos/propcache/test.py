"""Checks that the C extensions are linked in, not the pure-Python fallback."""
import propcache, propcache._helpers_c
assert propcache.__version__

"""Checks that the C extensions are linked in, not the pure-Python fallback."""
import frozenlist, frozenlist._frozenlist
assert list(frozenlist.FrozenList([1, 2])) == [1, 2]

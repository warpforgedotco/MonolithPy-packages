"""Checks that the C extensions are linked in, not the pure-Python fallback."""
import yarl, yarl._quoting_c
assert yarl.URL('https://example.com/a?b=1').query['b'] == '1'

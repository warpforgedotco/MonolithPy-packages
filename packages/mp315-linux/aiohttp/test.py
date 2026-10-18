"""Checks that the C extensions are linked in, not the pure-Python fallback."""
import aiohttp, aiohttp._http_parser
assert aiohttp.__version__

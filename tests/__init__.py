"""
from .cases import *
"""

import unittest

from . import oauth

suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(oauth.TestCase),
])

def run():
    return unittest.TextTestRunner(verbosity=2).run(suite)


"""
from .cases import *
"""

import unittest

from . import cases

suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(cases.TestOAuth),
])

def run():
    return unittest.TextTestRunner(verbosity=2).run(suite)

import pystubgen
import sys
import pytest

from sample import Sample

try:
    from sample_py3 import Py3Sample
except SyntaxError:
    Py3Sample = None

def check_source(object):
    """Invokes make_source and tries to compile it (checking its syntax)."""
    source = pystubgen.make_source(object)
    obj = compile(source, 'dummy.py', 'exec')
    return obj

def test_sample():
    obj = check_source(Sample)

@pytest.mark.skipif(Py3Sample is None, reason='not supported before Python 3')
def test_sample_py3():
    obj = check_source(Py3Sample)

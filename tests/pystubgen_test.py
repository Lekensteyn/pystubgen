import pystubgen
import pytest

import inspect
from sample import Sample

try:
    from sample_py3 import Py3Sample
except SyntaxError:
    Py3Sample = None

def check_source(object):
    """Invokes make_source and tries to compile it (checking its syntax)."""
    source = pystubgen.make_source(object)
    obj = compile(source, 'dummy.py', 'exec')
    obj_globals = {}
    exec(obj, obj_globals)
    return obj_globals

def test_sample():
    g = check_source(Sample)
    assert 'Sample' in g
    s = g['Sample']
    assert inspect.getdoc(s) == 'For testing purposes.'
    assert inspect.getdoc(s.strip) == 'Strip  some\ndocumentation.'

@pytest.mark.skipif(Py3Sample is None, reason='not supported before Python 3')
def test_sample_py3():
    g = check_source(Py3Sample)
    assert 'Py3Sample' in g
    s = g['Py3Sample']
    assert inspect.getdoc(s) == None
    assert inspect.getdoc(s.argstest) == 'z is unsupported syntax in Python 2.'

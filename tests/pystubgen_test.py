import pystubgen
import pytest

import inspect
import sample

try:
    import sample_py3
except SyntaxError:
    sample_py3 = None

def check_source(object):
    """Invokes make_source and tries to compile it (checking its syntax)."""
    source = pystubgen.make_source(object)
    obj = compile(source, 'dummy.py', 'exec')
    obj_globals = {}
    exec(obj, obj_globals)
    return obj_globals

def test_sample():
    g = check_source(sample)
    assert 'Sample' in g
    s = g['Sample']
    assert inspect.cleandoc(g['__doc__']) == \
        "This file contains definitions that should be processed without error."
    assert inspect.getdoc(s) == 'For testing purposes.'
    assert inspect.getdoc(s.strip) == 'Strip  some\ndocumentation.'

@pytest.mark.skipif(sample_py3 is None, reason='not supported before Python 3')
def test_sample_py3():
    g = check_source(sample_py3)
    assert 'Py3Sample' in g
    s = g['Py3Sample']
    assert inspect.cleandoc(g['__doc__']) == \
        'This file contains sample definitions that work only in Python 3.'
    assert inspect.getdoc(s) == None
    assert inspect.getdoc(s.argstest) == 'z is unsupported syntax in Python 2.'

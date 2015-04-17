import pystubgen
import pytest

import inspect
import sample

try:
    import sample_py3
except SyntaxError:
    sample_py3 = None

def check_source(object, **kwargs):
    """Invokes make_source and tries to compile it (checking its syntax)."""
    source = pystubgen.make_source(object, **kwargs)
    obj = compile(source, 'dummy.py', 'exec')
    obj_globals = {}
    exec(obj, obj_globals)
    return source, obj_globals

def test_sample():
    source, g = check_source(sample)
    assert 'Sample' in g
    s = g['Sample']
    assert inspect.cleandoc(g['__doc__']) == \
        "This file contains definitions that should be processed without error."
    assert inspect.getdoc(s) == 'For testing purposes.'
    assert inspect.getdoc(s.strip) == 'Strip  some\ndocumentation.'
    assert inspect.getdoc(s.prop) == 'Property documentation.'
    assert s.weirdchars == '"\'\n\\'
    assert s.rawchars == r'\x'

def test_sample_class_inheritance():
    source, g = check_source(sample.Sample)
    assert 'class Sample(str):' in source.splitlines()

@pytest.mark.skipif(sample_py3 is None, reason='not supported before Python 3')
def test_sample_py3():
    source, g = check_source(sample_py3)
    assert 'Py3Sample' in g
    s = g['Py3Sample']
    assert inspect.cleandoc(g['__doc__']) == \
        'This file contains sample definitions that work only in Python 3.'
    assert inspect.getdoc(s) == None
    assert inspect.getdoc(s.argstest) == 'z is unsupported syntax in Python 2.'

@pytest.mark.skipif(sample_py3 is None, reason='not supported before Python 3')
def test_sample_py3_func_params():
    source, g = check_source(sample_py3.Py3Sample)
    assert '    def argstest(self, x: int, y, z=1):' in source.splitlines()

def test_make_source_on_function():
    source, g = check_source(sample.function_without_params)
    assert 'def function_without_params():' in source.splitlines()
    assert inspect.getdoc(g['function_without_params']) == 'Single quotes'

def test_make_source_on_instance():
    sample_instance = sample.Sample()
    source, g = check_source(sample_instance)
    assert 'Sample' in g
    s = g['Sample']
    assert inspect.getdoc(s) == 'For testing purposes.'

def test_sample_class_classmethod():
    source, g = check_source(sample.Sample.classmeth)
    assert inspect.getdoc(g['classmeth']) == 'This is a class method.'
    assert 'def classmeth(cls, arg):' in source.splitlines()

def test_sample_class_staticmethod():
    source, g = check_source(sample.Sample.staticmeth)
    assert inspect.getdoc(g['staticmeth']) == 'This is a static method.'
    assert 'def staticmeth(arg=42):' in source.splitlines()

def test_empty_class():
    source, g = check_source(sample.Empty, include_header=False)
    assert source == 'class Empty(object):\n    pass\n'

def test_doc_only_class():
    source, g = check_source(sample.OnlyDoc, include_header=False)
    assert source == 'class OnlyDoc(object):\n    """\n    One line.\n    """\n'

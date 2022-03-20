
"""
This file contains definitions that should be processed without error.
"""

class Sample(str):
    """For testing purposes."""

    def strip(self):
        """Strip indentation.

            After first
            line.
        """

    def foo(self):
        pass

    def __add__(self):
        pass

    lamb = lambda x: x**2
    lamb0 = lambda: 2
    weirdchars = '"\'\n\\'
    rawchars = r'\x'

    @property
    def prop(self): """Property documentation."""

    @prop.setter
    def prop(self, val): pass

    @prop.deleter
    def prop(self): pass

    @classmethod
    def classmeth(cls, arg):
        """This is a class method."""

    @staticmethod
    def staticmeth(arg=42):
        """This is a static method."""

def function_without_params():
    'Single quotes'

class Empty(object):
    pass

class OnlyDoc(object):
    """
    One line.
    """

class ClassBase:
    """Testing inheritance where the order of names is important."""

class ClassA(ClassBase):
    pass

class ClassY(ClassBase):
    pass

class ClassX(ClassY):
    pass

class ClassZ(ClassY):
    pass

def function_with_params(a, b=1, *, c, d='x'):
    pass

# It is not possible to add documentation to variables, so the best we can do is
# exposing the variable name.
global_var = 42

some_dict = {'foo': 1, 'bar': {}, 1: True}

some_list = [0, ['x', True], None]

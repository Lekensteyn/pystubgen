
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

def function_with_params(a, b=1, *, c, d='x'):
    pass


"""
This file contains definitions that should be processed without error.
"""

class Sample(str):
    """For testing purposes."""
    def strip(self):
        pass

    def foo(self):
        pass

    def __add__(self):
        pass

    lamb = lambda x: x**2
    lamb0 = lambda: 2

    @property
    def prop(self): pass

    @prop.setter
    def prop(self, val): pass

    @prop.getter
    def prop(self): pass

    @prop.deleter
    def prop(self): pass

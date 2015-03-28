#!/usr/bin/env python
import pydoc
import inspect
import sys
import textwrap

class SourceDoc(pydoc.Doc):
    def indent(self, text, level):
        prefix = '    ' * level
        return textwrap.indent(text, prefix)

    def formatdoc(self, object, level=1):
        docstring = pydoc.getdoc(object).replace('"""', r'\"\"\"')
        if docstring:
            return self.indent('"""\n%s\n"""\n' % docstring, level)
        return ''

    def docmodule(self, object, name=None, mod=None):
        lines = ''
        for key, value in inspect.getmembers(object, inspect.isclass):
            lines += self.docclass(value, key, mod) + '\n'
        return lines

    def docclass(self, object, name=None, mod=None, *ignored):
        realname = object.__name__
        bases = object.__bases__

        def makename(c, m=object.__module__):
            return pydoc.classname(c, m)
        def kind_order(attr_desc):
            kind = attr_desc[1]
            order = 'method,static method,class method,property,data'.split(',')
            try:
                return order.index(kind)
            except ValueError:
                return len(order)

        lines = 'class %s' % realname
        if bases:
            lines += '(' + ', '.join(map(makename, bases)) + ')'
        lines += ':\n'
        lines += self.formatdoc(object)

        hasdefs = False
        for aname, kind, cls, value in \
            sorted(inspect.classify_class_attrs(object), key=kind_order):
            if cls != object:
                # Ignore inherited attributes
                continue
            if aname in ('__doc__', '__dict__', '__weakref__'):
                # Ignore documentation which has been printed before and other
                # uninteresting keys
                continue

            if kind.endswith('method'):
                if kind == 'static method':
                    block = '@staticmethod\n'
                elif kind == 'class method':
                    block = '@classmethod\n'
                else:
                    block = ''
                block += self.docroutine(value, aname, mod)
            elif kind == 'property':
                block = self.docproperty(value, aname, mod)
            elif kind == 'data':
                block = self.docdata(value, aname, mod)
            else:
                # Unknown?!
                block = '# Unhandled %s %s\n' % (kind, aname)
                lines += self.indent(block, 1)
                continue

            if block:
                lines += self.indent(block, 1)
                lines += '\n'
                hasdefs = True
        if not hasdefs:
            lines += '    pass\n\n'
        return lines

    def docroutine(self, object, name=None, mod=None, cl=None):
        try:
            realname = object.__name__
        except AttributeError:
            # Fallback for staticmethod and classmethods (as created by
            # namedtuple and found in inspect.ArgInfo)
            realname = name

        try:
            if hasattr(inspect, 'getfullargspec'):
                # New in Python 3
                argspec = inspect.getfullargspec(object)
            else:
                argspec = inspect.getargspec(object)
            signature = inspect.formatargspec(*argspec)
        except (ValueError, TypeError):
            signature = '(__unknown_params__)'

        if realname == '<lambda>':
            lines = '%s = lambda' % name
            args = signature[1:-1]
            lines += ' ' + args if args else ''
            lines += ': None\n'
            lines += self.formatdoc(object, level=0)
        else:
            lines = 'def %s%s:\n' % (realname, signature)
            block = self.formatdoc(object)
            lines += block if block else '    pass\n'
        return lines

    def docproperty(self, object, name=None, mod=None, cl=None):
        lines = '@property\n'
        lines += 'def %s(self):\n' % name
        block = self.formatdoc(object)
        lines += block if block else '    pass\n'
        return lines

    def docdata(self, object, name=None, mod=None, cl=None):
        val = repr(object)
        if not val[:1] in '"\'':
            val = '"%s"' % val
        lines = '%s = %s # DATA\n' % (name, val)
        if type(object) != str:
            lines += self.formatdoc(object, level=0)
        return lines

    def docother(self, object, name=None, mod=None, parent=None, maxlen=None, doc=None):
        # NOTE: if this is triggered, a bug has probably occurred since it is
        # called as fallback by Doc.document().
        val = repr(object)
        if not val[:1] in '"\'':
            val = '"%s"' % val
        lines = '%s = %s # OTHER\n' % (name, val)
        if type(object) != str:
            lines += self.formatdoc(object, level=0)
        return lines

sourcecode = SourceDoc()

def make_source(thing, include_header=False):
    source = pydoc.render_doc(thing, renderer=sourcecode,
            title='# Generated from %s')
    return source

class F(str):
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
    # Unsupported syntax in Python 2:
    #def argstest(self, x : int, y, z=1):
    #    pass

if __name__ == '__main__':
    _name = sys.argv[1]
    if _name in globals():
        _thing = globals()[_name]
    else:
        _thing = _name
    print(make_source(_thing, True))

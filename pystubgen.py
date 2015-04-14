#!/usr/bin/env python
# pystubgen - Generates Python source code from a module for documentation
# purposes.
#
# Copyright (C) 2015 Peter Wu <peter@lekensteyn.nl>
# Licensed under the MIT license. See the LICENSE file for details.

import pydoc
import inspect
import sys

class SourceDoc(pydoc.Doc):
    def _indent(self, text, level):
        prefix = '    ' * level
        def makeline(line):
            return prefix + line if line.strip() else line
        return ''.join(makeline(line) for line in text.splitlines(True))

    def _formatdoc(self, object, level=1):
        docstring = pydoc.getdoc(object).replace('"""', r'\"\"\"')
        if docstring:
            return self._indent('"""\n%s\n"""\n' % docstring, level)
        return ''

    def _document(self, object, name=None, *args):
        """Generate documentation for an object, propagating errors."""
        args = (object, name) + args
        # pydoc.document ignores exceptions... so try these first.
        if inspect.ismodule(object): return self.docmodule(*args)
        if inspect.isclass(object): return self.docclass(*args)
        if inspect.isroutine(object): return self.docroutine(*args)
        return super(SourceDoc, self).document(object, name, *args)
    document = _document

    def docmodule(self, object, name=None, mod=None):
        lines = ''
        lines += self._formatdoc(object, level = 0)
        if lines:
            lines += '\n'
        for key, value in inspect.getmembers(object, inspect.isclass):
            lines += self.docclass(value, key, mod) + '\n'
        return lines

    def docclass(self, object, name=None, mod=None, *ignored):
        realname = object.__name__
        bases = object.__bases__

        def makename(c):
            m = c.__module__
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
        lines += self._formatdoc(object)

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
                lines += self._indent(block, 1)
                continue

            if block:
                lines += self._indent(block, 1)
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
            lines += self._formatdoc(object, level=0)
        else:
            lines = 'def %s%s:\n' % (realname, signature)
            block = self._formatdoc(object)
            lines += block if block else '    pass\n'
        return lines

    def docproperty(self, object, name=None, mod=None, cl=None):
        lines = '@property\n'
        lines += 'def %s(self):\n' % name
        block = self._formatdoc(object)
        lines += block if block else '    pass\n'
        return lines

    def docdata(self, object, name=None, mod=None, cl=None):
        val = repr(object)
        if not val[:1] in '"\'':
            val = '"%s"' % val
        lines = '%s = %s # DATA\n' % (name, val)
        if type(object) != str:
            lines += self._formatdoc(object, level=0)
        return lines

    def docother(self, object, name=None, mod=None, parent=None, maxlen=None, doc=None):
        # NOTE: if this is triggered, a bug has probably occurred since it is
        # called as fallback by Doc.document().
        if not name:
            raise RuntimeError('Invalid call to docother')
        val = repr(object)
        if not val[:1] in '"\'':
            val = '"%s"' % val
        lines = '%s = %s # OTHER\n' % (name, val)
        if type(object) != str:
            lines += self._formatdoc(object, level=0)
        return lines

sourcecode = SourceDoc()

def _is_string(thing):
    """Whether the object is exactly a string (and not a subclass)"""
    try:
        return type(thing) in (str, unicode)
    except:
        return type(thing) == str

def resolve(thing):
    """Given an object or a path to an object, get the object and its name."""
    # Based on pydoc.resolve, but check for exact str type, not a subclass
    if _is_string(thing):
        object = pydoc.locate(thing)
        if not object:
            raise ImportError('no Python documentation found for %r' % thing)
        return object, thing
    else:
        name = getattr(thing, '__name__', None)
        return thing, name if isinstance(name, str) else None

def make_source(thing, include_header=True):
    """Produce source code with documentation strings attached.

    Args:
        thing: a Python object such as modules, classes, fields, functions, etc.
            Class instances are resolved to their type. Strings are resolved to
            the object.
        include_header: when True, a preceding comment will be added that notes
            where the source code is generated from.

    Returns:
        A str containing the source code for the given object.
    """
    object, name = resolve(thing)
    desc = pydoc.describe(object)
    if not (inspect.ismodule(object) or
            inspect.isclass(object) or
            inspect.isroutine(object) or
            inspect.isgetsetdescriptor(object) or
            inspect.ismemberdescriptor(object) or
            isinstance(object, property)):
        # If the passed object is a piece of data or an instance,
        # document its available methods instead of its value.
        object = type(object)
        desc += ' object'
    source = ''
    if include_header:
        source += '# Generated from {0} using pystubgen\n\n'.format(desc)
    source += sourcecode.document(object, name)
    return source

def main():
    _name = sys.argv[1]
    if _name in globals():
        _thing = globals()[_name]
    else:
        _thing = _name
    print(make_source(_thing, True))

if __name__ == '__main__':
    main()

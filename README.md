pystubgen
=========

Generates Python source code from a module for documentation purposes.

When supplied with a module, it will extract all classes, functions and
variables from the file and output a valid Python script with just documentation
strings preserved. (Implementation detail: properties are also available).

Usage
-----
The API to produce code is pretty straightforward:

    import pystubgen

    # Produce the source code str with structure and documentation
    # for the 'pystubgen' module
    source = pystubgen.make_source(pystubgen)
    print(source)

The same functionality via the command-line interface (subject to change):

    pystubgen pystubgen

The [original motivation][export-module-question] behind pystubgen was the
ability to produce documentation from gdb's Python interface. An example session
where `gdb.py` is created using pystubgen from the current directory:

    pystubgen$ PYTHONPATH=$PWD gdb -q
    (gdb) python
    >import pystubgen
    >open('gdb.py', 'w').write(pystubgen.make_source(gdb))
    >end
    (gdb) quit

Features
--------
Definitions and docstrings are outputted for:

 - Modules.
 - Classes.
 - Methods, static methods and class methods for classes.
 - Fields for classes (without docstrings though).
 - Global variables (without docstrings though).
 - Functions and lambda functions including parameters (caveat: built-ins and
   other C functions have `(__unknown_params__)` as parameter signature).

Testing
-------
pystubgen uses the [pytest][pytest] framework for acceptance testing. Once
installed, you can invoke `py.test` to run the tests using your current python
interpreter.

To test with multiple Python interpreters, install [tox][tox] and invoke `tox`.
pystubgen has been tested with Python 2.6.9, 2.7.9, 3.2.6 and 3.4.3 and pytest
2.7.0 on Arch Linux.

License
-------
This project ("pystubgen") is licensed under the MIT license. See the LICENSE
file for more details.

 [export-module-question]: https://stackoverflow.com/q/29316044/427545
 [pytest]: https://pytest.org/latest/
 [tox]: https://tox.readthedocs.org/en/latest/

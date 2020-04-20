Contribution Guidelines
=======================

Whether reporting bugs, discussing improvements and new ideas: Contributions
to ES21 are welcome! Here's how to get started:

1. Check for open issues or open a fresh issue to start a discussion around
   a feature idea or a bug
2. Fork `the repository <https://github.com/Unviray/ES21/>`_ on GitHub,
   create a new branch off the `master` branch and start making your changes
3. Send a pull request and bug the maintainer until it gets merged and
   published :)


Philosophy of ES21
------------------

ES21 aims to be simple and fun to use. Flask application is very modulable.
These modularity will contradict each other from time to time. In these cases,
try using as little magic as possible. In any case don't forget documenting code
that isn't clear at first glance.


Code Conventions
----------------

In general the ES21 source should always follow `PEP 8 <http://legacy.python.org/dev/peps/pep-0008/>`_.
Exceptions are allowed in well justified and documented cases. However we make
a small exception concerning docstrings:

When using multiline docstrings, keep the opening and closing triple quotes
on their own lines and add an empty line after it.

.. code-block:: python

    def some_function():
        """
        Documentation ...
        """

        # implementation ...


Version Numbers
---------------

ES21 follows the `SemVer versioning guidelines <http://semver.org/>`_.
This implies that backwards incompatible changes in the API will increment
the major version. So think twice before making such changes.

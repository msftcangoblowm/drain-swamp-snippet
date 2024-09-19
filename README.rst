drain-swamp-snippet
===================

Change portions of static config files

|  |kit| |codecov| |license|
|  |last-commit| |test-status| |quality-status| |docs|
|  |versions| |implementations|
|  |platforms| |black|
|  |downloads| |stars|
|  |mastodon-msftcangoblowm|

.. PYVERSIONS

\* Python 3.9 through 3.13, PyPy

**New in 1.0.x**

integration with drain-swamp-action; all badges;

**New in 0.0.x**

move snip from package drain-swamp;

Whats a snippet?
-----------------

Within a configuration, there are times when some bit of text needs to be changed.

The only requirement is the file format should recognize pound symbol ``#`` as a comment.

A snippet **without** an snippet code (id)

.. code:: text

   before snippet
   # @@@ editable
   code block
   # @@@ end
   after snippet

A snippet **with** an snippet code (id)

.. code:: text

   before snippet
   # @@@ i_am_a_snippet_co
   code block
   # @@@ end
   after snippet

`[read more] <https://drain-swamp-snippet.readthedocs.io/en/stable/snippets.html>`_

What batteries are included?
-----------------------------

None

This is a base package. Other authors are encouraged to:

- not reinvent the wheel

- avoid packages with snippet implementations, when only just want the base class, Snip

Packages using drain-swamp-snippet-pypi_
------------------------------------------

- drain-swamp-pypi_

.. _drain-swamp-pypi: https://pypi.org/project/drain-swamp
.. _drain-swamp-snippet-pypi: https://pypi.org/project/drain-swamp-snippet

Acknowledgement
---------------

The technique and initial implementation is from
`Ned Batchelder <https://github.com/nedbat>`_

Ned Batchelder is also the author of `cog <https://cog.readthedocs.io/en/latest/>`_
which creates content by embedding both Python code and output in the original file.

Check out `introduction to cog <https://nedbatchelder.com/blog/202409/cogged_github_profile.html>`_

.. note::

   `[original code] <https://github.com/nedbat/coveragepy/blob/0db5d1826d246955b96617a2b7118a40deaf8bb9/igor.py#L385>`_
   supports replacing one snippet per file, not idiot proof, nor unittested.

   `[coverage LICENSE:Apache-2.0] <https://github.com/nedbat/coveragepy/blob/0db5d1826d246955b96617a2b7118a40deaf8bb9/LICENSE.txt>`_

.. |last-commit| image:: https://img.shields.io/github/last-commit/msftcangoblowm/drain-swamp-snippet/master
    :target: https://github.com/msftcangoblowm/drain-swamp-snippet/pulse
    :alt: last commit to gauge activity
.. |test-status| image:: https://github.com/msftcangoblowm/drain-swamp-snippet/actions/workflows/testsuite.yml/badge.svg?branch=master&event=push
    :target: https://github.com/msftcangoblowm/drain-swamp-snippet/actions/workflows/testsuite.yml
    :alt: Test suite status
.. |quality-status| image:: https://github.com/msftcangoblowm/drain-swamp-snippet/actions/workflows/quality.yml/badge.svg?branch=master&event=push
    :target: https://github.com/msftcangoblowm/drain-swamp-snippet/actions/workflows/quality.yml
    :alt: Quality check status
.. |docs| image:: https://readthedocs.org/projects/drain-swamp-snippet/badge/?version=latest&style=flat
    :target: https://drain-swamp-snippet.readthedocs.io/
    :alt: Documentation
.. |kit| image:: https://img.shields.io/pypi/v/drain-swamp-snippet
    :target: https://pypi.org/project/drain-swamp-snippet/
    :alt: PyPI status
.. |versions| image:: https://img.shields.io/pypi/pyversions/drain-swamp-snippet.svg?logo=python&logoColor=FBE072
    :target: https://pypi.org/project/drain-swamp-snippet/
    :alt: Python versions supported
.. |license| image:: https://img.shields.io/github/license/msftcangoblowm/drain-swamp-snippet
    :target: https://pypi.org/project/drain-swamp-snippet/blob/master/LICENSE
    :alt: License
.. |mastodon-msftcangoblowm| image:: https://img.shields.io/mastodon/follow/112019041247183249
    :target: https://mastodon.social/@msftcangoblowme
    :alt: msftcangoblowme on Mastodon
.. |stars| image:: https://img.shields.io/github/stars/msftcangoblowm/drain-swamp-snippet.svg?logo=github
    :target: https://github.com/msftcangoblowm/drain-swamp-snippet/stargazers
    :alt: GitHub stars
.. |codecov| image:: https://codecov.io/gh/msftcangoblowm/drain-swamp-snippet/branch/master/graph/badge.svg?token=13dL2Owydg
    :target: https://codecov.io/gh/msftcangoblowm/drain-swamp-snippet
    :alt: drain-swamp coverage percentage
.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/ambv/black
.. |downloads| image:: https://img.shields.io/pypi/dm/drain-swamp-snippet
.. |implementations| image:: https://img.shields.io/pypi/implementation/drain-swamp-snippet
.. |platforms| image:: https://img.shields.io/badge/platform-windows%20%7C%20macos%20%7C%20linux-lightgrey

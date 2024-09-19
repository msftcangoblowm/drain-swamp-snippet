.. raw:: html

   <div style="visibility: hidden;">

Overview
=========

.. raw:: html

   </div>

|feature banner|

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

:doc:`[read more] <snippets>`

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

.. seealso::

   `[original code] <https://github.com/nedbat/coveragepy/blob/0db5d1826d246955b96617a2b7118a40deaf8bb9/igor.py#L385>`_
   supports replacing one snippet per file, not idiot proof, nor unittested.

   `[coverage LICENSE:Apache-2.0] <https://github.com/nedbat/coveragepy/blob/0db5d1826d246955b96617a2b7118a40deaf8bb9/LICENSE.txt>`_

.. |feature banner| image:: _static/drain-swamp-snippet-banner-640-320.*
   :alt: drain-swamp-snippet content replacement

"""
.. moduleauthor:: Dave Faulkmore <https://mastodon.social/@msftcangoblowme>

|project_name| is standalone, not a general utility. There are no dependencies.
Keep this way to keep minimize dependencies of build backend, ``drain-swamp``.

``is_ok`` is a frequently used general utility that can also be found in
``logging_strict.util.check_type``. Use that one instead.

.. py:data:: __all__
   :type: tuple[str]
   :value: ("is_ok",)

"""

__all__ = ("is_ok",)


def is_ok(test):
    """Check if non-empty str

    Edge case: contains only whitespace --> ``False``

    :param test: variable to test
    :type test: typing.Any | None
    :returns: ``True`` if non-empty str otherwise ``False``
    :rtype: bool

    """
    ret = False
    is_str = test is not None and isinstance(test, str)
    if is_str:
        # Edge case: contains only whitespace
        str_stripped = test.strip()
        ret = len(str_stripped) != 0
    else:
        ret = False

    return ret

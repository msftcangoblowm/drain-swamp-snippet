"""
.. moduleauthor:: Dave Faulkmore <https://mastodon.social/@msftcangoblowme>

Unittest for module, check_type

Unit test -- Module

.. code-block:: shell

   python -m coverage run --source='drain_swamp_snippet.check_type' -m pytest \
   --showlocals tests/test_check_type.py && coverage report \
   --data-file=.coverage --include="**/check_type.py"

Integration test

.. code-block:: shell

   make coverage
   pytest --showlocals --cov="drain_swamp_snippet" --cov-report=term-missing \
   --cov-config=pyproject.toml tests

"""

import pytest

from drain_swamp_snippet.check_type import is_ok


@pytest.mark.parametrize(
    "mystr, expected",
    (
        pytest.param(
            None,
            False,
            id="not-str",
        ),
        pytest.param(
            "",
            False,
            id="empty-string",
        ),
        pytest.param(
            0.123,
            False,
            id="not-str",
        ),
        pytest.param(
            "    ",
            False,
            id="contains-only-whitespace",
        ),
        pytest.param(
            "Hello World!",
            True,
            id="non-empty-string",
        ),
    ),
)
def test_is_ok(mystr, expected):
    """Test is_ok check"""
    # pytest --showlocals --log-level INFO -k "test_type_narrowing_is_ok" tests
    actual = is_ok(mystr)
    assert actual == expected

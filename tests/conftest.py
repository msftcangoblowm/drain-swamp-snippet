"""
.. moduleauthor:: Dave Faulkmore <https://mastodon.social/@msftcangoblowme>

drain-swamp pytest conftest.py
"""

import re
import shutil
from collections.abc import Sequence
from pathlib import PurePath
from typing import Any

import pytest

from .logger import (  # noqa: F401
    get_logger,
    has_logging_occurred,
)


class FileRegression:
    """Compare previous runs files.

    :ivar file_regression: file to compare against?
    :vartype file_regression: typing.Self

    .. todo:: when Sphinx<=6 is dropped

       Remove line starting with re.escape(" translation_progress=

    .. todo:: when Sphinx<7.2 is dropped

       Remove line starting with original_url=

    """

    ignores = (
        # Remove when support for Sphinx<=6 is dropped,
        re.escape(" translation_progress=\"{'total': 0, 'translated': 0}\""),
        # Remove when support for Sphinx<7.2 is dropped,
        r"original_uri=\"[^\"]*\"\s",
    )

    def __init__(self, file_regression: "FileRegression") -> None:
        """FileRegression constructor."""
        self.file_regression = file_regression

    def check(self, data: str, **kwargs: dict[str, Any]) -> str:
        """Check previous run against current run file.

        :param data: file contents
        :type data: str
        :param kwargs: keyword options are passed thru
        :type kwargs: dict[str, typing.Any]
        :returns: diff of file contents?
        :rtype: str
        """
        return self.file_regression.check(self._strip_ignores(data), **kwargs)

    def _strip_ignores(self, data: str) -> str:
        """Helper to strip ignores from data.

        :param data: file contents w/o ignore statements
        :type data: str
        :returns: sanitized file contents
        :rtype: str
        """
        cls = type(self)
        for ig in cls.ignores:
            data = re.sub(ig, "", data)
        return data


@pytest.fixture()
def file_regression(file_regression: "FileRegression") -> FileRegression:
    """Comparison files will need updating.

    .. seealso::

       Awaiting resolution of `pytest-regressions#32 <https://github.com/ESSS/pytest-regressions/issues/32>`_

    """
    return FileRegression(file_regression)


@pytest.fixture()
def prepare_folders_files(request):
    """Prepare folders and files within folder."""

    set_folders = set()

    def _method(seq_rel_paths, tmp_path):
        """Creates folders and empty files

        :param seq_rel_paths: Relative file paths. Creates folders as well
        :type seq_rel_paths:

           collections.abc.Sequence[str | pathlib.Path] | collections.abc.MutableSet[str | pathlib.Path]

        :param tmp_path: Start absolute path
        :type tmp_path: pathlib.Path
        """
        set_abs_paths = set()
        is_seq = seq_rel_paths is not None and (
            isinstance(seq_rel_paths, Sequence) or isinstance(seq_rel_paths, set)
        )
        if is_seq:
            for posix in seq_rel_paths:
                if isinstance(posix, str):
                    abs_path = tmp_path.joinpath(*posix.split("/"))
                elif issubclass(type(posix), PurePath):
                    if not posix.is_absolute():
                        abs_path = tmp_path / posix
                    else:  # pragma: no cover
                        # already absolute
                        abs_path = posix
                else:
                    abs_path = None

                if abs_path is not None:
                    set_abs_paths.add(abs_path)
                    set_folders.add(abs_path.parent)
                    abs_path.parent.mkdir(parents=True, exist_ok=True)
                    abs_path.touch()
        else:
            abs_path = None

        return set_abs_paths

    yield _method

    # cleanup
    if request.node.test_report.outcome == "passed":
        for abspath_folder in set_folders:
            shutil.rmtree(abspath_folder, ignore_errors=True)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach each test's TestReport to the test Item.

    Fixtures can decide how to finalize based on the test result.

    Fixtures can access the TestReport from the `request` fixture at
    `request.node.test_report`.

    .. seealso::

       https://stackoverflow.com/a/70598731

    """
    test_report = (yield).get_result()
    if test_report.when == "call":
        item.test_report = test_report

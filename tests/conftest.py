"""
.. moduleauthor:: Dave Faulkmore <https://mastodon.social/@msftcangoblowme>

drain-swamp-snippet pytest conftest.py
"""

import shutil
from collections.abc import Sequence
from pathlib import PurePath
from typing import (
    TYPE_CHECKING,
    cast,
)

import pytest

from .fr import FileRegression

if TYPE_CHECKING:
    from collections.abc import (
        Callable,
        MutableSet,
    )
    from pathlib import Path

pytest_plugins = [
    "logging_strict",
]


@pytest.fixture()
def file_regression(file_regression: "FileRegression") -> FileRegression:
    """Comparison files will need updating.

    .. seealso::

       Awaiting resolution of `pytest-regressions#32 <https://github.com/ESSS/pytest-regressions/issues/32>`_

    """
    return FileRegression(file_regression)


@pytest.fixture()
def prepare_folders_files(
    request: pytest.FixtureRequest,
) -> "Callable[[Sequence[str | Path] | MutableSet[str | Path], Path], set[Path]]":
    """Prepare folders and files within folder."""

    set_folders = set()

    def _method(
        seq_rel_paths: "Sequence[str | Path] | MutableSet[str | Path]",
        tmp_path: "Path",
    ) -> "set[Path]":
        """Creates folders and empty files

        :param seq_rel_paths: Relative file paths. Creates folders as well
        :type seq_rel_paths:

           collections.abc.Sequence[str | pathlib.Path] | collections.abc.MutableSet[str | pathlib.Path]

        :param tmp_path: Start absolute path
        :type tmp_path: pathlib.Path
        :rtype: set[pathlib.Path]
        """
        if TYPE_CHECKING:
            optabs_path: Path | None

        set_abs_paths = set()
        # is_seq
        if seq_rel_paths is not None and isinstance(seq_rel_paths, Sequence | set):
            for optposix in seq_rel_paths:
                if optposix is None:
                    optabs_path = None
                else:
                    posix = optposix
                    if isinstance(posix, str):
                        optabs_path = cast(
                            "Path | None",
                            tmp_path.joinpath(*posix.split("/")),
                        )
                    elif issubclass(type(posix), PurePath):
                        if not posix.is_absolute():
                            optabs_path = cast("Path | None", tmp_path / posix)
                        else:  # pragma: no cover
                            # already absolute
                            optabs_path = posix
                    else:
                        optabs_path = None

                if optabs_path is not None:
                    abs_path = optabs_path
                    set_abs_paths.add(abs_path)
                    set_folders.add(abs_path.parent)
                    abs_path.parent.mkdir(parents=True, exist_ok=True)
                    abs_path.touch()
        else:
            optabs_path = None

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

import importlib.metadata
import re
import sys
from pathlib import Path

from packaging.version import parse
from sphinx_pyproject import SphinxConfig

from drain_swamp_snippet import package_name

path_docs = Path(__file__).parent
path_package_base = path_docs.parent
sys.path.insert(0, str(path_package_base))  # Needed ??

# Not dynamic. Not using setuptools-scm
release = importlib.metadata.version(package_name)
v = parse(release)
version_short = f"{v.major}.{v.minor}"
version_xyz = f"{v.major}.{v.minor}.{v.micro}"
version_long = str(v)

# drain-swamp is a drain-swamp-snippet implementation for editting the below
copyright = "2024–2024, Dave Faulkmore"
# The short X.Y.Z version.
version = version_xyz
# The full version, including alpha/beta/rc tags.
# release = release
# The date of release, in "monthname day, year" format.
release_date = "October 4, 2024"

config = SphinxConfig(
    # Path(__file__).parent.parent.joinpath("pyproject.toml"),
    path_package_base / "pyproject.toml",
    globalns=globals(),
    config_overrides={"version": version_long},
)

# This project is a fork from "Sphinx External ToC"
proj_project = config.name
proj_description = config.description
proj_authors = config.author

slug = re.sub(r"\W+", "-", proj_project.lower())
proj_master_doc = config.get("master_doc")
project = f"{proj_project} {version_xyz}"

###############
# Dynamic
###############
rst_epilog = """
.. |project_name| replace:: {slug}
.. |package-equals-release| replace:: drain_swamp_snippet=={release}
""".format(
    release=release, slug=slug
)

html_theme_options = {
    "description": proj_description,
    "show_relbars": True,
    "logo_name": False,
    "logo": "snip-logo.svg",
    "show_powered_by": False,
}

latex_documents = [
    (
        proj_master_doc,
        f"{slug}.tex",
        f"{proj_project} Documentation",
        proj_authors,
        "manual",  # manual, howto, jreport (Japanese)
        True,
    )
]
man_pages = [
    (
        proj_master_doc,
        slug,
        f"{proj_project} Documentation",
        [proj_authors],
        1,
    )
]
texinfo_documents = [
    (
        proj_master_doc,
        slug,
        f"{proj_project} Documentation",
        proj_authors,
        slug,
        proj_description,
        "Miscellaneous",
    )
]

#################
# Static
#################
ADDITIONAL_PREAMBLE = r"""
\DeclareUnicodeCharacter{20BF}{\'k}
"""

latex_elements = {
    "sphinxsetup": "verbatimforcewraps",
    "extraclassoptions": "openany,oneside",
    "preamble": ADDITIONAL_PREAMBLE,
}

html_sidebars = {
    "**": [
        "about.html",
        "searchbox.html",
        "navigation.html",
        "relations.html",
    ],
}

intersphinx_mapping = {
    "python": (  # source https://docs.python.org/3/objects.inv
        "https://docs.python.org/3",
        ("objects-python.inv", None),
    ),
    "dss": (
        "https://drain-swamp-snippet.readthedocs.io/en/stable",
        ("objects-dss.inv", "objects-dss.txt"),
    ),
}
intersphinx_disabled_reftypes = ["std:doc"]

extlinks = {
    "pypi_org": (  # url to: aiologger
        "https://pypi.org/project/%s",
        "%s",
    ),
}

# spoof user agent to prevent broken links
# curl -A "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:24.0) Gecko/20100101 Firefox/24.0" --head "https://github.com/python/cpython/blob/3.12/Lib/unittest/case.py#L193"
linkcheck_request_headers = {
    "https://github.com/": {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:24.0) Gecko/20100101 Firefox/24.0",
    },
    "https://docs.github.com/": {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:24.0) Gecko/20100101 Firefox/24.0",
    },
}

# Ignore unfixable WARNINGS
# in pyproject.toml --> nitpicky = true
# in conf.py --> nitpicky = True
nitpick_ignore = [
    ("py:class", "ValidatorType"),
]

favicons = [
    {"rel": "icon", "href": "icon-drain-swamp-200x200.svg", "type": "image/svg+xml"},
    {
        "rel": "apple-touch-icon",
        "sizes": "180x180",
        "href": "apple-touch-icon-180x180.png",
        "type": "image/png",
    },
]

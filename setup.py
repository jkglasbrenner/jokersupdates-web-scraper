#!/usr/bin/env python

import sys
from collections import OrderedDict

import setuptools

name = "jokersupdates"
version = "0.1"
release = "0.1.0"
url_github = "https://github.com/jkglasbrenner/jokersupdates-web-scraper"
description = "A web scraper for the Joker's Updates forums."

dependencies = [
    "beautifulsoup4>=4.7.1",
    "cerberus>=1.3.1",
    "lxml>=4.3.4",
    "numpy>=1.16.4",
    "python-dotenv>=0.10.3",
    "pytz>=2019.1",
    "selenium>=3.141.0",
]
cmdclass = {}
extras_dependencies = {
    "docs": [
        "sphinx>=2.1.2",
        "sphinx-rtd-theme==0.4.3",
        "sphinx-autodoc-typehints==1.6.0",
    ],
    "dev": [
        "autopep8==1.4.4",
        "black==19.3b0",
        "entrypoints==0.3",
        "flake8-bugbear==19.3.0",
        "flake8==3.7.7",
        "grip==4.5.2",
        "ipython>=7.6.1",
        "jupyter==1.0.0",
        "jupyterlab==0.35.6",
        "jupyterlab_code_formatter==0.2.3",
        "mypy==0.720",
        "pre-commit==1.17.0",
        "pydocstyle==3.0.0",
        "pytoml==0.1.21",
        "seed-isort-config==1.9.2",
    ],
}
tests_dependencies = (["pytest==5.0.1", "pytest-runner==5.1"],)

needs_pytest = {"pytest", "test", "ptr"}.intersection(sys.argv)
pytest_runner = ["pytest-runner"] if needs_pytest else []

setup_requires = pytest_runner

try:
    from sphinx.setup_command import BuildDoc

    cmdclass["build_sphinx"] = BuildDoc

except ImportError:
    print("WARNING: sphinx not available, not building docs")

setuptools.setup(
    name=name,
    author="James K. Glasbrenner",
    author_email="jglasbr2@gmu.edu",
    license="MIT",
    version=release,
    url=url_github,
    project_urls=OrderedDict((("Code", url_github),)),
    description=description,
    python_requires=">=3.7",
    packages=setuptools.find_packages(),
    include_package_data=True,
    setup_requires=setup_requires,
    zip_safe=False,
    install_requires=dependencies,
    extras_require=extras_dependencies,
    tests_require=tests_dependencies,
    cmdclass=cmdclass,
    command_options={
        "build_sphinx": {
            "project": ("setup.py", name),
            "version": ("setup.py", version),
            "release": ("setup.py", release),
            "source_dir": ("setup.py", "docs"),
            "build_dir": ("setup.py", "docs/_build"),
        }
    },
)

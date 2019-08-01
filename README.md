# Jokersupdates web scraper

A web scraper for the [Joker's Updates](https://www.jokersupdates.com/) forums.

## Getting started

To interact with or modify the files in the project, you'll need to use `conda` to set up a virtual environment using the `environment.yml` file, install the JupyterLab extensions, and install the pre-commit hooks.
This is easy to do if you are working on a Linux machine and have Anaconda installed, just run,

    make conda
    conda activate jokersupdates
    make jupyter_extensions
    make hooks

If you close your terminal and come back to the project later, remember to run `conda activate jokersupdates` to reactivate your virtual environment.

## Available make rules

There are several rules defined in the project `Makefile` that you are able to run from the project root using `make`.
If you run `make` by itself, it will display the following help menu,

    Available rules:

    beautify            Reformat Python code with black
    clean               Remove temporary files (preserves development installation)
    conda               Create/update conda-based virtual environment
    docs                Generate documentation
    hooks               Install pre-commit hooks
    jupyter_extensions  Install and enable extensions for JupyterLab
    lint                Lint using flake8
    veryclean           Remove all temporary files

## Project organization

    .
    ├── .flake8                             <- Configuration file for linting Python code with flake8.
    ├── .gitignore                          <- Configuration file that defines the files git should ignore.
    ├── .isort.cfg                          <- Configuration file for isort pre-commit hook.
    ├── .pre-commit-config.yaml             <- Configuration file for installing project's pre-commit hooks.
    ├── jokersupdates                       <- Project source code.
    │   ├── elements
    │   ├── fileio
    │   ├── locators
    │   ├── pages
    │   ├── schema
    │   │   ├── custom
    │   │   ├── pages
    │   │   ├── scrapers
    │   │   └── tables
    │   ├── scrapers
    │   └── transformers
    ├── environment.yml                     <- Conda environment file to create virtual environment.
    ├── LICENSE                             <- License file for repository.
    ├── Makefile                            <- Top-level Makefile. Type make for a list of valid commands.
    ├── MANIFEST.in                         <- Configuration file used when building project with setup.py.
    ├── mypy.ini                            <- Mypy configuration file for analyzing type hints.
    ├── pyproject.toml                      <- Project configuration file, used with black code formatter.
    ├── README.md                           <- The top-level README for this project.
    └── setup.py                            <- Used to install project in environment.yml.

## License

Unless otherwise noted, the contents of this repository is released under the MIT license.

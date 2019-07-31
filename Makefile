.PHONY: beautify clean conda docs help hooks jupyter_extensions lint veryclean

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROJECT_NAME = jokersupdates

RM = rm
COPY = cp
FIND = find

CONDA = conda
CONDA_ENV_FILE = environment.yml

PIP = pip

PY ?= python3
PY_SETUP = setup.py
PY_SETUP_DOCS = build_sphinx

PRECOMMIT = pre-commit

JUPYTER = jupyter
JUPYTERLAB_EXTENSIONS = \
    @jupyter-widgets/jupyterlab-manager \
    @jupyterlab/katex-extension \
    @mflevine/jupyterlab_html \
    @ryantam626/jupyterlab_code_formatter \
    jupyter-matplotlib \
    jupyterlab-python-file \
    jupyterlab_vim
JUPYTERLAB_SERVEREXTENSION = \
    jupyterlab_code_formatter

BLACK = black
BLACK_OPTS = -t py37

FLAKE8 = flake8

CLEAN_FILES = build/ *_cache/ docs/_build/ dist/
FULL_CLEAN_FILES = *.egg-info/ pip-wheel-metadata/ .pytest_cache/

#################################################################################
# FUNCTIONS                                                                     #
#################################################################################

define python_black
    $(BLACK) $(BLACK_OPTS) $(PROJECT_NAME)
endef

define cleanup
    $(FIND) -name "__pycache__" -type d -exec $(RM) -rf {} +
    $(FIND) -name "*.py[co]" -type f -exec $(RM) -rf {} +
    $(FIND) -name ".ipynb_checkpoints" -type d -exec $(RM) -rf {} +
    -$(RM) -rf $(CLEAN_FILES)
endef

define full_cleanup
    $(call cleanup)
    -$(RM) -rf $(FULL_CLEAN_FILES)
endef

define install_jupyterlab_extension
    $(JUPYTER) labextension install $(1)
endef

define install_serverextension
    $(JUPYTER) serverextension enable --py $(1)
endef

define install_jupyter_extensions
    $(foreach extension,$(JUPYTERLAB_EXTENSIONS),\
        $(call install_jupyterlab_extension,--no-build $(extension));)

    $(JUPYTER) lab build

    $(foreach serverextension,$(JUPYTERLAB_SERVEREXTENSION),\
        $(call install_serverextension,$(serverextension));)
endef

define lint
    $(FLAKE8) $(PROJECT_NAME)
endef

define make_subdirectory
    mkdir -p "$@"
endef

define pip_cmd
    $(PIP) $(1)
endef

define precommit_cmd
    $(PRECOMMIT) $(1)
endef

define run_setup_py
    $(PY) ./$(PY_SETUP) $(1)
endef

define update_conda_env
    $(CONDA) env update --file $(CONDA_ENV_FILE)
endef

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Reformat Python code with black
beautify:
	$(call python_black)

## Remove temporary files (preserves development installation)
clean:
	$(call cleanup)

## Create/update conda-based virtual environment
conda:
	$(call update_conda_env)

## Generate documentation
docs:
	$(call run_setup_py, $(PY_SETUP_DOCS))

## Install pre-commit hooks
hooks:
	$(call precommit_cmd, install)

## Install and enable extensions for JupyterLab
jupyter_extensions:
	$(call install_jupyter_extensions)

## Lint using flake8
lint:
	$(call lint)

## Remove all temporary files
veryclean:
	$(call full_cleanup)

#################################################################################
# PROJECT RULES                                                                 #
#################################################################################



#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')

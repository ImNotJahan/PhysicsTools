# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os, sys
sys.path.insert(0, os.path.abspath('..'))

extensions = [
  "myst_parser",
  "sphinx.ext.autodoc",
  "sphinx.ext.autosummary",
  "sphinx.ext.napoleon",
  "sphinx.ext.mathjax",
  "sphinx_autodoc_typehints",
]

html_theme = "furo"

autosummary_generate           = True
autosummary_generate_overwrite = True

napoleon_numpy_docstring  = True
napoleon_google_docstring = True

project = 'physics_utils'
copyright = '2025, Jahan Rashidi'
author = 'Jahan Rashidi'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
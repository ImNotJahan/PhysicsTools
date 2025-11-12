rm -rf docs/_build docs/api/generated
sphinx-build -b html -a -E docs/ docs/_build/html

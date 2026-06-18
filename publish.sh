#!/bin/bash

set -e

cd "$(dirname "$0")"

echo "Running tests before publishing..."
./run_tests.sh

echo "Tests passed! Building package..."
rm -rf dist/
rm -rf build/
rm -rf src/*.egg-info/

python -m pip install --upgrade build twine
python -m build

echo "Publishing to PyPI..."
python -m twine upload dist/* --verbose

echo "Successfully published!"

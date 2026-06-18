#!/bin/bash

set -e

cd "$(dirname "$0")"

mkdir -p tests

if [ ! -d "venv" ]; then
    echo "Creating virtual environment in venv/..."
    python -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies and packages..."
pip install --upgrade pip
pip install pytest
pip install -e .

echo "Running pytest..."
cd tests
pytest

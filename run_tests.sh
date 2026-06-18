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
pip install pytest beautifulsoup4
pip install -e .

echo "Building NBT schema..."
python tests/build_nbt_schema.py

echo "Running pytest..."
cd tests
pytest

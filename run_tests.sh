#!/bin/bash

if [ -z "$VIRTUAL_ENV" ]; then
    echo "Sourcing venv/bin/activate..."
    source venv/bin/activate
fi

echo "Running tests..."

flare cli_test/main.py --run=1 2>/dev/null > tests/actual_output.raw.txt

cat tests/actual_output.raw.txt | grep -v "Error parsing" | grep -v "Objective" | grep -v "Scoreboard division" | grep -v "Scoreboard modulo" | grep -v "Float(exp" | grep -v "^'$" | grep -v "Compiling" | grep -v "\[Score " | grep -v "Successfully built" | grep -v "\-\-\- Starting mcemu \-\-\-" | sed -E 's/!print_[0-9]+/!print_X/g' | sed '/^$/d' | sed -E 's/\x1b\[[0-9;]*m//g' > tests/actual_output.txt

diff -u --strip-trailing-cr tests/expected_output.txt tests/actual_output.txt
DIFF_EXIT=$?

rm tests/actual_output.raw.txt tests/actual_output.txt

if [ $DIFF_EXIT -eq 0 ]; then
    echo "Tests passed!"
    exit 0
else
    echo "Tests failed! See diff above."
    exit 1
fi

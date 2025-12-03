#!/bin/bash

# Create dir
day=$(printf "%02d\n" "$1")
dir="day${day}"
mkdir "$dir"

# Copy and create files
touch "${dir}/input.txt"
cp "template.py" "${dir}/silver.py"
touch "${dir}/gold.py"
cp "template.md" "${dir}/comments.md"

# Activate python venv
source .venv/bin/activate

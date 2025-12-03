#!/bin/bash

# Create dir
day=$(printf "%02d\n" "$1")
dir="day${day}"
mkdir -p "$dir"

# Copy and create files
touch "${dir}/test_input.txt"
cp "template.py" "${dir}/silver.py"
touch "${dir}/gold.py"
cp "template.md" "${dir}/comments.md"

# Fetch and save input
token=$(cat AoC_token.txt)
curl -b "session=${token}" "https://adventofcode.com/2025/day/$1/input" > "${dir}/input.txt"

# Edit day number in python script
sed -i "s|\"InsertDayNumberHere\"|$1|" "${dir}/silver.py"

# Activate python venv
source .venv/bin/activate

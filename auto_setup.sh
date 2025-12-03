#!/bin/bash

year=2025
day=$1

token=$(cat AoC_token.txt)
dir="day$(printf "%02d\n" "${day}")"

# Create dir
mkdir -p "${dir}"

# Copy and create files
cp "template.py" "${dir}/silver.py"
touch "${dir}/gold.py"
cp "template.md" "${dir}/comments.md"

# Fetch and save input
curl -sb "session=${token}" "https://adventofcode.com/${year}/day/${day}/input" > "${dir}/input.txt"

# Fetch, scrap and save test input (aka, the biggest code snippet inside the subject page)
curl -sb "session=${token}" "https://adventofcode.com/${year}/day/${day}" | sed -n '/<code>/,/<\/code>/p' | awk 'BEGIN{RS="</code>"; FS="<code>"} { gsub(/\r/,""); block=$2; sub(/\n$/,"",block); if(length(block)>max){max=length(block); s=block} } END{print s}' > "${dir}/test_input.txt"

# Edit day number in python script
sed -i "s|\"InsertDayNumberHere\"|${day}|" "${dir}/silver.py"

# Activate python venv
source .venv/bin/activate

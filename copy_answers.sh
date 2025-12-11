
newroot=$1
year=2025

# Copy silver solutions
find */silver.py | while read f; do
    d=$(dirname "$f")                # e.g., day01
    n=${d#day}                       # e.g., 01
    n=$(echo "$n" | sed 's/^0*//')   # e.g., 1
    mkdir -p "${newroot}${year}/day$n"
    cp "$f" "${newroot}${year}/day$n/solution1.py"
    sed -i "s|intest = |# intest = |" "${newroot}${year}/day$n/solution1.py"
    sed -i "s|inreal = |# inreal = |" "${newroot}${year}/day$n/solution1.py"
    sed -i "s|input = inreal|input = incustom|" "${newroot}${year}/day$n/solution1.py"
done

# Copy gold solutions
find */gold.py | while read f; do
    d=$(dirname "$f")                # e.g., day01
    n=${d#day}                       # e.g., 01
    n=$(echo "$n" | sed 's/^0*//')   # e.g., 1
    mkdir -p "${newroot}${year}/day$n"
    cp "$f" "${newroot}${year}/day$n/solution2.py"
    sed -i "s|intest = |# intest = |" "${newroot}${year}/day$n/solution2.py"
    sed -i "s|inreal = |# inreal = |" "${newroot}${year}/day$n/solution2.py"
    sed -i "s|input = inreal|input = incustom|" "${newroot}${year}/day$n/solution2.py"
done

# Copy comments
find */comments.md | while read f; do
    d=$(dirname "$f")                # e.g., day01
    n=${d#day}                       # e.g., 01
    n=$(echo "$n" | sed 's/^0*//')   # e.g., 1
    mkdir -p "${newroot}${year}/day$n"
    cp "$f" "${newroot}${year}/day$n/"
done

# Copy other non-sensible files
cp .gitignore ${newroot}
cp auto_setup.sh ${newroot}
cp copy_answers.sh ${newroot}
cp README.md ${newroot}
cp template.md ${newroot}
cp template.py ${newroot}

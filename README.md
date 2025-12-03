# Advent of Code 2025

Hi! So here is my python code for the [2025 AoC](https://adventofcode.com/2025/) puzzles :)

For each day, you can find my solutions in the dayXX/ folder. I decided this year to have my solutions in two files for simplicity: `silver.py` for part 1 and `gold.py` for part 2.

I **comment** my code to try and make it as understandable as I can. You can also find some more information in `comments.md` each day; they contain stuff like my **times**, the **difficulties** I experienced, and an explanation of my **strategy** whenever I feel like it is needed!

If you want to **run** it on your input (please only do it to check by how far you're off :), you can simply add an `input.txt` file in the directory and paste your own. Then at the project root, simply create a python venv with `python3 -m venv .venv`, activate it with `source .venv/bin/activate`, and run your desired solution with `python day[00-12]/[silver|gold].py`!

Also, I wrote a bash tool that **generates everything** that I need each day (what would a dev do for convenience, lol). It even fetches the **daily example input** (or at least, it does its best to), and the **daily puzzle input**. To use this, simply copy your *session token* in `AoC_token.txt` at the project root, and run `source auto_setup.sh <day_with_no_extra_zero>`.

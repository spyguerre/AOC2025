# Day 09

## Times

- Silver: 07:52

- Gold: ~06:00:00 (officially 11:09:52)


## Gold puzzle strategy

The real issue with this puzzle is that the coordinates are spread on an integer range too large to compute in finite time and space.

So in order to keep the visual aspect of the subject and not get lost in coordinate mess; let's just reduce that range! Instead of doing the computations on the original map that would be way too large, let's create a **compressed matrix**:
- It should have as few rows and columns as possible.
- We want each cell of the compressed matrix to represent a *rectangle* of cells in the original map.

So let's use the red tiles' coordinates and follow this approach:
- Create and sort the list of y (resp. x) coordinates of red tiles independently.
- Create a row (resp. column) for each red tile coordinate, and a row (resp. column) for each range of coordinates strictly between two red tiles.

Any cell in the compressed matrix that is horizontally and vertically strictly within a range of coordinates, will then represent a rectangle of these ranges in the original map. For example:

```
#----#
|....|
|....|
|....|
|....|
#----#
```

Will be compressed into:

```
#-#
|.|
#-#
```

And:

```
.....#---#
.....|...|
#----#...|
|........|
#------#.|
.......|.|
.......#-#
```

Will only be compressed into:

```
..#---#
..|...|
#-#...|
|.....|
#---#.|
....|.|
....#-#
```
Since we can't compress red tiles indices that are separated by only 1 tile.

<br>

We can complete this matrix by padding one row and column on either side and run an exploration only through the points ".", starting on the outside of the polygon (typically in the border created with the padding). Thus, the tiles that remain unseen by the exploration match the tiles of, and inside of the polygon!

<br>

After having built this matrix, we can simply brute-force through the pairs of possible red-tiles corners that would form a rectangle like in part 1, and compute the one with the largest area that remains in the polygon!


## Experience

Today was... definitely a big gap in difficulty.

<br>

Silver was relatively easy (bruteforce worked well), and apparently I ranked second of my school for that, so why not :)

<br>

Gold though... I spent two entire hours not writing much code just to understand the problem better and find a solution that wouldn't take too long to write and debug. I thought of several approaches, including building small rectangles with adjacent red tiles and regrouping them later, processing a certain amount of spread points in the map to try and grow a plausible rectangle, excluding the rectangles with a red tile inside of them, creating a compressed matrix of the problem's original map... Turns out that only the last two would actually work.

I started writing the penultimate one (which you can find uncommented in a precedent commit; even though there are untreated edge-cases), got a result that looked good but was still wrong, and decided that it was too cumbersome (even if it ran faster), so I completely switched my point of view and went for the last solution instead.

And to my *surprise*, I got the *same exact result*. Which I couldn't explain other than by an issue with my input at first.

Returned to the problem after some school work when a friend told me that his mistake was to compute the distances for the area wrong (like `abs(a-b+1)`, instead of `abs(a-b) + 1`). So I checked my code and it turns out I had exactly the same problem somehow.

So technically I spent most of my time looking for a typo today... nice :')

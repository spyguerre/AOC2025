# Day 05

## Times

- Silver: 16:28

- Gold: 33:56

## Gold puzzle Strategy

We have a list of ranges, out of which we want to remove the duplicates ids.

By sorting the ranges by start id, it ensures that when treating a range, all the ids treated later will be greater than the current start id.

We can then create a cursor that equals the smallest id not yet discovered, that is greater than any other id we have acknowledged already. Since the ranges are sorted, we can safely assume that any new id will be greater or equal to the cursor.

Then, let's compute the number of unseen ids in the current range. Any unseen id that must be added must respect these conditions:
- Be in the range: `s <= id <= e`,
- Be unseen: `cursor <= id`.

Which is equivalent to: `max(cursor, s) <= id <= e`.

If there are any, there are actually `e - max(cursor, s) + 1` integers that respect the previous condition. Since this value can be strictly negative (e.g., `cursor > e + 1`, in which case there is no id to add), we'll only take the positive value of this formula: `max(e - max(cursor, s) + 1, 0)`.

Once we have added this to the result, we have to update the cursor so that it meets its definition: `cursor = max(cursor, id_e + 1)`, and proceed to the next iteration!

## Experience

Started on the wrong track today. Struggled quite a lot to format the data from the input, that took me quite a lot of time already. For silver, I began trying with an approach in which I stored all the fresh IDs in a dict, since I didn't expect both the ranges to be so wide and the two lists to be not so big. When trying to run my program while coding a more efficient solution, my OS completely crashed because my memory probably exploded lol. So I lost quite a lot of time rebooting again.
I'm pretty happy with gold puzzle though. Only not for the fact that what I spent the most time on was debugging unnecessary type or data structure issues. I found the solution explained above pretty quickly intuitively, and quickly checked on a sheet of paper. The only thing I was really missing was the missing edge case in the puzzle input; a range that is strictly contained in another one. Pretty fun puzzle :)

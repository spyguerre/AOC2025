# Day 10

## Times

- Silver: 01:18:59

- Gold: ~02:40:00 (officially 08:34:29)

## Experience

I thought of a very straightforward algorithm for silver pretty quickly, but implementing all of it still took me about an hour, since all the indices and many multi-dimentional data structures that I used soon became tricky. My real mistake was that I wanted to implement optimizations in the wrong place. For instance, I wrote the triangle search in the wrong direction without thinking because it usually doesn't matter, but in order to find the optimal solution first, it did. So that cost me about 20 min, and I only understood why it behaved that way tonight while commenting my code haha.

As I saw gold puzzle, I first updated my code quickly to make sure the complexity was ideed too high (you never know, right?...). Then tried to think about other solutions that didn't involve another big library, and quickly gave up and caught up on commenting my code for day 09. Came back a little while later, wrote an example of the problem formally, learnt about scipy's solvers online, solved the rest of it really fast with almost no issue, so that almost felt like cheating. And most other people that I got to talk with about today's gold puzzle felt kind of the same way :')

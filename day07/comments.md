# Day 07

## Times

- Silver: 24:08

- Gold: 01:17:35

## Experience

AAAAAAAAA - This was definitely *not* supposed to be that hard.

<br>

Spent a lot of time on silver figuring out why I had duplicate paths already. Worst thing is I had read the example that showed the beam being split into two but didn't realize it could be an issue in my program at first. Also spent too much time figuring out what operation could/should be performed in which order, that was already a mess but I managed to make everything work well.

<br>

For gold...
- The first strategy I though of was **bottom-up**: i.e. computing the tree like in silver, then assigning every "|" node at the bottom a value 1, transfering the value upward, and whenever we find a splitter next to the current beam, add its value to the beam above it, and get the result in the start node at the end
- As this would have worked but would have forced me to make other loops below, I thought of another approach that could have been quicker, **top-down**: i.e. assigning value 1 to the start node, transfering the value to beams downward; whenever we reach a splitter, add the value of the beam above the splitter to both of the nodes next to the splitter, and finally get the result by summing the value of all the nodes in the bottom row.
- Both streategies sound easy, but I had countless problems about nodes that would be added multiple times in the queue, nodes that would be added to the queue after they had already been treated, nodes that transfered only half of their values downward, splitters that didn't transfer their beam value to neightbour nodes and other that would add the value twice... At some point instead of the committed way to detect already treated nodes, I even converted lists of coordinates into strings to put them into a set, I think I was starting to get crazy :')

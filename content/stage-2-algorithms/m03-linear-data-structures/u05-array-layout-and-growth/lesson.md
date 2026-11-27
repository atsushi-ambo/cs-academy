# Fixed, multidimensional, and dynamic arrays (amortized growth)

A fixed array has a fixed number of slots. Imagine those slots next to
each other in memory. With equal-size slots, the index tells you how
far to move from the start. An index access takes O(1) time.

A 2D array has rows and columns. Put the rows end to end in **row-major order**.
For 3 columns, row 1 column 2 is at index 1 × 3 + 2 = 5. Python lists of
lists store references to separate rows. They do not need one flat block.

A dynamic array can grow. This lesson models one that doubles its capacity
when full. Size counts used slots. Capacity counts all slots.
The slot copies needed to reach capacity 8 are 1 + 2 + 4 = 7.
With n appends, a doubling array starting at capacity 1 copies fewer than
2n old slots in total. The cost per append over that sequence is amortized O(1).
One append can still take O(n) when it grows the buffer. Python lists also
leave spare room but are not required to use our doubling rule.

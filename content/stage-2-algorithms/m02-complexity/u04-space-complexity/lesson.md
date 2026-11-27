# Space complexity: counting the memory an algorithm needs

Memory is like space on a work table. Count the most you need at one moment.
Name what you include. Here, **extra space** leaves out the original input and
the required output. A fresh copy used only to help with a search is extra space.

| Job on n items | Extra space |
| --- | --- |
| Keep a running count in a loop | O(1) |
| Save every item in a scratch list | O(n) |
| Make one recursive call for each item without copying the list | O(n) |
| Recurse on slices of lengths n − 1, n − 2, …, 1 | O(n²) |

A frame holds the work of one active call. A recursive call can keep its
parent's data live. A loop with one scratch list at a time may use much less peak space.

# Measuring cost: Big-O

A library needs to check a list of returned books. Will the work still fit in one day
if the list gets ten times longer? Let `n` be the number of books. Count one check
as one step, using the same rule for every input size.

| Checks | Tight growth class | When n doubles |
| --- | --- | --- |
| 7 | O(1) | Same |
| 3n + 7 | O(n) | Close to twice as many at large n |
| n × n | O(n²) | Four times as many |

Big-O gives an upper bound on growth. In this course we normally name the
tightest class from our list. A fixed factor like 3 changes the exact cost.
It does not change the class. Two full passes add their costs. An inner
loop with n passes for each of n outer passes multiplies them.

# Complexity classes: constant, log, linear, polynomial, exponential, factorial

The size n may be the number of files or the number of choices.

| Growth | An example count | Meaning |
| --- | --- | --- |
| Constant | 1 | Read one slot |
| Logarithmic | log₂ n | Halve one group until size 1 |
| Linear | n | Check each file once |
| Polynomial | n² or n³ | Choose two or three slots |
| Exponential | 2ⁿ | Choose yes or no for each file |
| Factorial | n! | Try every possible order |

Think of a row of switches. Each extra switch doubles the number of full settings.
For task orders, the choices start at n, then fall to n − 1 and so on.
A count of possible outcomes is different from the work to compute that count.

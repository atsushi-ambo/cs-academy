# Hash functions and collisions (chaining, open addressing)

A route table needs a way to store both keys when one slot number is shared.

    a -> bucket 1 <- e
         [(a, 4), (e, 8)]

Both keys lead to bucket 1. The two pairs keep their own keys and values.

**Example.** In four slots, c and g both start at 3. Probing puts the second pair at 0.

**Common mistake.** A full ring has no empty slot to stop the search. Limit the probes.

**Real work.** A small task registry can map route names to settings without scanning all names.

**Summary.** Chains share a bucket. Probing searches other slots. A resize must
compute new positions for saved keys.

## Model answer

The slot index is a remainder that uses capacity. A larger capacity can give a different slot for the same key. I rehash each key so a later lookup can find it.

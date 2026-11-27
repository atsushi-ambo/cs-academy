# Hash tables

A hash table helps a log tool find a service by name.

    "api" -> hash -> slot -> ("api", 503)

The arrows show how a key leads to a stored entry. Check the key after reaching its slot.

**Example.** A count dict maps api to 2. The next api event raises the count to 3.

**Common mistake.** Test a key with in. A value of zero is still a valid value.

**Real work.** Count log types or collect each service's response times in one pass.

**Summary.** Use a set for membership and a dict for a key with a value.
Good hash distribution makes common lookups O(1) on average.

## Model answer

The dict stores the first position of each earlier value. I look up the complement before saving the current value. That way an item can never match itself.

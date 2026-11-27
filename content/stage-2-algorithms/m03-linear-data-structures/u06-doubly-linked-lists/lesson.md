# Doubly linked lists: insert, delete, and the prev/next invariant

A maintenance tool can walk a job list in either direction.

    None <- [scan] <-> [mail] -> None

The middle arrows show both links between scan and mail. The outer links are empty.

**Example.** To put sync between them, join scan to sync and then sync to mail.
In each join, set both the forward and backward link.

**Common mistake.** Fixing only scan.next leaves a wrong path when you walk back.

**Real work.** A job editor may move or drop a known job without scanning all jobs.

**Summary.** A known-node edit takes O(1) time. The full link check takes O(n) time.
Two links per node still take O(n) total space.

## Model answer

A known node gives me both neighbors. I can join them in constant time. To check the whole chain, I walk from the head and compare each prev link with the node I just left.

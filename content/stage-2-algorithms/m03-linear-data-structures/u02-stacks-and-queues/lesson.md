# Stacks and queues

A worker queue can keep jobs in order while new jobs arrive.

    incoming [newer, newest]    outgoing [older, oldest]
                         top                        top

Each right edge is its stack top. The output stack serves oldest first.

**Example.** Push scan, then mail onto input. Move both to output. Scan is now on top.

**Common mistake.** Moving new input onto a nonempty output lets new jobs cut in line.

**Real work.** Bounded log buffers can reuse a fixed group of slots as events leave.

**Summary.** A stack uses LIFO and a queue uses FIFO. Two stacks give amortized
O(1) queue edits. A fixed ring gives O(1) edits and can refuse extra items.

## Model answer

New jobs go onto the input stack. When the output stack is empty, I move all input jobs to it. This puts the oldest job on top of the output stack.

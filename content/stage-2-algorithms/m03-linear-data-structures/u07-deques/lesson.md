# Deques: both ends in O(1)

A deque lets you update a small view of a busy stream from both ends.

    left  [index 2: load 9] [index 4: load 6]  right

Index 2 has the highest load. Index 4 is newer and has a lower load.

**Example.** If the window starts at 3, remove index 2. Index 4 now gives the peak.

**Common mistake.** Values alone do not tell you which measurement left the window.
Keep indexes so you can use the window's left edge.

**Real work.** A monitoring tool can show the highest load over the last 60 readings.

**Summary.** A ring deque edits either end in O(1) time. A window scan takes O(n)
time because each index enters and leaves at most once.

## Model answer

I drop indexes from the left when they leave the window. A larger new value stays in the window longer, so I drop weaker values from the right. The leftmost candidate now gives the peak.

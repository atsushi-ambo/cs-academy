# Solutions

## `exit_log`

The same list travels back up the frames. O(n + 1) time, O(n + 1) frame space, and O(n + 1) output space.

## `loop_total`

The loop does O(n + 1) work and uses O(1) extra space. The long test catches a direct recursive solution that runs out of frames.

## `fast_power`

There are O(log(n + 1) + 1) calls, frames, and multiplications. This counts operations and frames. The cost of multiplying big integers and the bytes for their values grow with the exponent.

def read_cell(cells, cols, row, col):
    """Read row, col from flat row-major storage with cols columns.
    Inputs: 1 to 20 rows and 1 to 20 columns of integers, with valid row and col.
    Use one index calculation and one slot read. Leave cells unchanged.
    Sample: read_cell([4, 5, 6, 7, 8, 9], 3, 1, 0) -> 7
    """
    raise NotImplementedError


def copies_for_appends(count):
    """Return the total old slots copied for count appends, starting with an empty block of capacity 1.
    Input: an integer from 0 to 1,000,000. Use a loop over resizes only. Do not build a block.
    Sample: copies_for_appends(9) -> 15
    """
    raise NotImplementedError


def make_array():
    """Finish DynamicArray.append. make_array() returns a fresh empty array each time.
    Append stores value at the next slot, then increases size by one.
    When full, make a block with twice the capacity. Read and copy each old slot
    in order and increase copies once per old slot. Switch to the new block.
    Use slot writes by index. Do not use list resizing methods or slice copies.
    Values may be any object, including None. There are up to 100 appends per array.
    Sample: after appending 5, 8, and 2, slots is [5, 8, 2, None], size is 3, and copies is 3.
    """
    class DynamicArray:
        def __init__(self):
            self.slots = [None]
            self.size = 0
            self.copies = 0

        def append(self, value):
            raise NotImplementedError

    return DynamicArray()

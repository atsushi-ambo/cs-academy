def size_total(sizes, i=0):
    if i == len(sizes):
        return 0
    return sizes[i] + size_total(sizes, i + 1)


def reverse_label(label):
    if not label:
        return ""
    return reverse_label(label[1:]) + label[0]


def is_mirror(label, left=0, right=None):
    if right is None:
        right = len(label) - 1
    if left >= right:
        return True
    if label[left] != label[right]:
        return False
    return is_mirror(label, left + 1, right - 1)


def flatten_sizes(batch, out=None):
    if out is None:
        out = []
    for item in batch:
        if isinstance(item, list):
            flatten_sizes(item, out)
        else:
            out.append(item)
    return out

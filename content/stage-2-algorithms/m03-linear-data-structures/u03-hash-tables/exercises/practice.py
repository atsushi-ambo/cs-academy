def count_codes(codes):
    """Return a fresh dict of counts for a list of up to 1,000 integer status codes.
    Use one pass and a dict. Leave the list unchanged. Do not call Counter or list.count.
    Example: count_codes([503, 200, 503]) gives {503: 2, 200: 1}."""
    raise NotImplementedError


def group_times(rows):
    """Rows are up to 1,000 (service, milliseconds) pairs. Return a new dict
    with one fresh list per service. Keep sample order and duplicates. Leave rows unchanged.
    Example: [('api', 4), ('db', 9), ('api', 2)] gives {'api': [4, 2], 'db': [9]}."""
    raise NotImplementedError


def two_sum(values, target):
    """Values is a list of up to 1,000 integers. Return (left, right) of two
    different positions summing to target, or None. Choose the smallest right index.
    If several left indexes work, choose the smallest left. Leave values unchanged.
    Use one pass and a dict of earlier positions. Example: two_sum([4, 4, 6], 10) gives (0, 2)."""
    raise NotImplementedError

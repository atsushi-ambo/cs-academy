def error_count(codes):
    """Return how many status codes are from 500 through 599 inclusive.
        codes holds 0 to 200 integers from 100 to 599. Leave it unchanged.
        Use a loop. Sample: error_count([200, 500, 599, 404]) -> 2
        Sample: error_count([]) -> 0
    """
    raise NotImplementedError


def first_recovery(codes):
    """Return the index of the first 200, or -1 if there is no 200.
        codes holds 0 to 200 integers. Leave it unchanged. Use a loop.
        Sample: first_recovery([503, 200, 200]) -> 1
        Sample: first_recovery([503, 404]) -> -1
    """
    raise NotImplementedError


def large_files(folders, limit):
    """folders is a list of lists of file sizes in MB. Count the sizes at
        least limit. Use two loops, and leave all input lists unchanged.
        There are 0 to 30 folders and 0 to 30 files per folder.
        Sizes and limit are integers from 0 to 1000.
        Sample: large_files([[4, 10], [], [12, 3]], 10) -> 2
    """
    raise NotImplementedError

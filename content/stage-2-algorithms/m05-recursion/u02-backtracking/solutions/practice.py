def service_groups(services):
    result = []
    path = []

    def visit(index):
        if index == len(services):
            result.append(path[:])
            return
        visit(index + 1)
        path.append(services[index])
        visit(index + 1)
        path.pop()

    visit(0)
    return result


def job_orders(jobs):
    used = [False] * len(jobs)
    path = []
    result = []

    def visit():
        if len(path) == len(jobs):
            result.append(path[:])
            return
        for index in range(len(jobs)):
            if not used[index]:
                used[index] = True
                path.append(jobs[index])
                visit()
                path.pop()
                used[index] = False

    visit()
    return result


def count_boards(n):
    columns = set()
    down = set()
    up = set()

    def place(row):
        if row == n:
            return 1
        count = 0
        for col in range(n):
            left_label = row - col
            right_label = row + col
            if col in columns or left_label in down or right_label in up:
                continue
            columns.add(col)
            down.add(left_label)
            up.add(right_label)
            count += place(row + 1)
            columns.remove(col)
            down.remove(left_label)
            up.remove(right_label)
        return count

    return place(0)

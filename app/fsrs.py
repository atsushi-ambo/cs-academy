import math
from dataclasses import dataclass, replace
from datetime import date, timedelta
from enum import IntEnum

# https://github.com/open-spaced-repetition/awesome-fsrs/wiki/The-Algorithm#fsrs-5
W = (0.40255, 1.18385, 3.173, 15.69105, 7.1949, 0.5345, 1.4604, 0.0046,
     1.54575, 0.1192, 1.01925, 1.9395, 0.11, 0.29605, 2.2698, 0.2315, 2.9898,
     0.51655, 0.6621)
DECAY = -0.5
FACTOR = 19 / 81


class Grade(IntEnum):
    AGAIN = 1
    HARD = 2
    GOOD = 3
    EASY = 4


@dataclass(frozen=True)
class Memory:
    stability: float
    difficulty: float
    last_day: date


def answer_grade(correct, hints=0):
    return Grade(max(Grade.AGAIN, Grade.GOOD - hints)) if correct else Grade.AGAIN


def retrievability(elapsed, stability):
    return (1 + FACTOR * elapsed / stability) ** DECAY


def initial_difficulty(grade):
    return W[4] - math.expm1(W[5] * (grade - 1))


def clamped_difficulty(value):
    return min(10.0, max(1.0, value))


def update(memory, grade, today):
    if memory is None:
        return Memory(W[grade - 1], clamped_difficulty(initial_difficulty(grade)), today)

    s, d = memory.stability, memory.difficulty
    elapsed = max(0, (today - memory.last_day).days)
    delta = -W[6] * (grade - 3) * (10 - d) / 9
    difficulty = W[7] * initial_difficulty(Grade.EASY) + (1 - W[7]) * (d + delta)
    recall = retrievability(elapsed, s)
    if not elapsed:
        stability = s * math.exp(W[17] * (grade - 3 + W[18]))
    elif grade == Grade.AGAIN:
        lapse = W[11] * d ** -W[12] * ((s + 1) ** W[13] - 1) * math.exp(W[14] * (1 - recall))
        stability = min(s, lapse)
    else:
        bonus = {Grade.HARD: W[15], Grade.EASY: W[16]}.get(grade, 1)
        growth = math.exp(W[8]) * (11 - d) * s ** -W[9] * math.expm1(W[10] * (1 - recall))
        stability = s * (1 + bonus * growth)
    return replace(memory, stability=max(0.01, stability),
                   difficulty=clamped_difficulty(difficulty), last_day=today)


def due_date(memory, retention=0.9):
    interval = memory.stability / FACTOR * (retention ** (1 / DECAY) - 1)
    days = min(36500, max(1, math.floor(interval + 0.5)))
    return memory.last_day + timedelta(days=days)

import ast
import re
from dataclasses import dataclass, field
from hashlib import sha256
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
STEP_TYPES = frozenset("read predict try parsons fix code terminal explain boss".split())
PLAY_TYPES = STEP_TYPES - {"terminal", "boss"}
SOURCE_LIMIT = 16 * 1024
STDIN_LIMIT = 4 * 1024
ID = re.compile(r"[a-z0-9][a-z0-9.-]{0,79}")


class ContentError(ValueError):
    pass


class ContentYAML(yaml.SafeLoader):
    def construct_mapping(self, node, deep=False):
        self.flatten_mapping(node)
        result = super().construct_mapping(node, deep)
        if len(result) != len(node.value):
            raise ContentError("Duplicate YAML key")
        return result


def require(condition, context):
    if not condition:
        raise ContentError(context)


def mapping(value):
    require(isinstance(value, dict), "Expected a YAML mapping")
    return value


def sequence(value):
    require(isinstance(value, list), "Expected a YAML list")
    return value


def string(value):
    require(isinstance(value, str) and bool(value.strip()), "Expected non-empty text")
    return value


def yaml_file(path):
    try:
        return mapping(yaml.load(path.read_text(encoding="utf-8"), Loader=ContentYAML))
    except (yaml.YAMLError, ContentError, OSError) as error:
        raise ContentError(f"{path}: {error}") from error


def register(identifier, seen):
    require(ID.fullmatch(string(identifier)) and identifier not in seen,
            f"Invalid or duplicate ID: {identifier}")
    seen.add(identifier)
    return identifier


def asset(directory, relative, section, suffix):
    parts = Path(string(relative))
    path = (directory / parts).resolve()
    base = directory.resolve()
    allowed = base / section
    require(
        len(parts.parts) == (2 if section else 1)
        and not parts.is_absolute()
        and path.is_relative_to(allowed)
        and path.is_relative_to(base)
        and path.suffix == suffix
        and path.is_file(),
        f"Invalid unit asset: {relative}",
    )
    return path.read_text(encoding="utf-8")


def definition(source, kind, name):
    try:
        tree = ast.parse(source)
    except SyntaxError as error:
        raise ContentError(f"Invalid Python in content: {error}") from error
    matches = [node for node in tree.body if isinstance(node, kind) and node.name == name]
    require(len(matches) == 1, f"Missing or duplicate Python definition: {name}")
    return matches[0]


def function_source(source, name):
    node = definition(source, ast.FunctionDef, name)
    return ast.get_source_segment(source, node) + "\n"


@dataclass(frozen=True)
class Problem:
    starter: str
    solution: str = ""
    explanation: str = ""
    test_body: str = ""
    test_class: str = ""
    module: str = ""
    hints: tuple[str, ...] = ()


@dataclass
class Catalog:
    stages: dict = field(default_factory=dict)
    modules: dict = field(default_factory=dict)
    units: dict = field(default_factory=dict)
    steps: dict = field(default_factory=dict)
    play: dict = field(default_factory=dict)
    cards: dict = field(default_factory=dict)
    problems: dict = field(default_factory=dict)
    placements: dict = field(default_factory=dict)
    resources: dict = field(default_factory=dict)


def code_problem(step, directory):
    hints = tuple(map(string, sequence(step.get("hint_levels", []))))
    if step["type"] == "try":
        check = mapping(step.get("check"))
        require(set(check) in ({"stdout_contains"}, {"stdout_line"}),
                f"{step['id']}: expected one stdout check")
        if "stdout_line" in check:
            line = string(check["stdout_line"])
            require(line.splitlines() == [line], f"{step['id']}: stdout_line must be one line")
        else:
            string(check["stdout_contains"])
        return Problem(starter=string(step.get("starter")))
    require(len(hints) == 3, f"{step['id']}: expected three hints")
    if step["type"] == "fix":
        return Problem(
            starter=string(step.get("starter")),
            solution=string(step.get("solution")),
            explanation=string(step.get("explanation")),
            test_body=string(step.get("tests")),
            hints=hints,
        )

    exercise = string(step.get("exercise"))
    filename = Path(exercise).name
    module = Path(filename).stem
    function = string(step.get("function"))
    test_class = string(step.get("test_class"))
    require(module.isidentifier() and test_class.isidentifier(), f"Invalid test target: {step['id']}")
    starter_file = asset(directory, exercise, "exercises", ".py")
    test_body = asset(directory, f"tests/test_{filename}", "tests", ".py")
    solution_file = asset(directory, f"solutions/{filename}", "solutions", ".py")
    definition(test_body, ast.ClassDef, test_class)

    explanation = asset(directory, "solutions/solutions.md", "solutions", ".md")
    sections = re.split(r"(?m)^## ", explanation)
    section = next((entry for entry in sections[1:] if entry
                    and f"`{function}`" in entry.splitlines()[0]), "")
    require(section, f"No solution explanation: {function}")
    return Problem(
        starter=function_source(starter_file, function),
        solution=function_source(solution_file, function),
        explanation=f"## {section.rstrip()}",
        test_body=test_body,
        test_class=test_class,
        module=module,
        hints=hints,
    )


def load_unit(catalog, directory, metadata):
    uid = metadata.get("id")
    require(isinstance(uid, str) and uid in catalog.units, f"Unknown unit: {uid}")
    require(uid not in catalog.play, f"Duplicate unit definition: {uid}")
    unit = catalog.units[uid]
    version = metadata.get("version")
    require(type(version) is int and version > 0, f"Invalid unit version: {uid}")
    require(
        metadata.get("stage") == catalog.modules[unit["module_id"]]["stage"]
        and metadata.get("module") == catalog.modules[unit["module_id"]]["title"]
        and metadata.get("title") == unit["title"],
        f"Unit metadata does not match curriculum: {uid}",
    )
    status = metadata.get("status")
    require(status in ("draft", "published"), f"Invalid unit status: {uid}")
    prerequisites = tuple(map(string, sequence(metadata.get("prerequisites", []))))
    require(uid not in prerequisites and len(set(prerequisites)) == len(prerequisites)
            and all(key in catalog.units for key in prerequisites), f"Invalid prerequisites: {uid}")
    unit.update(version=version, status=status, prerequisites=prerequisites)
    play_file = yaml_file(directory / "steps.yaml")
    require(play_file.get("unit") == uid, f"Wrong unit in steps.yaml: {uid}")

    seen = set()
    playable = []
    read_count = 0
    for raw in sequence(play_file.get("steps")):
        step = mapping(raw)
        sid = register(step.get("id"), seen)
        kind = string(step.get("type"))
        require(kind in STEP_TYPES, f"Unknown step type: {kind}")
        read_count = read_count + 1 if kind == "read" else 0
        require(read_count <= 2, f"{uid}/{sid}: more than two consecutive read steps")
        if "choices" in step or kind == "predict":
            choices = sequence(step.get("choices"))
            require(len(choices) == 4, f"{uid}/{sid}: expected four choices")
            for choice in choices:
                string(mapping(choice).get("text"))
                string(choice.get("why"))
            answer = step.get("answer")
            require(type(answer) is int and 0 <= answer < len(choices), f"Invalid answer: {sid}")
        if kind == "predict" and "hint_levels" in step:
            hints = tuple(map(string, sequence(step["hint_levels"])))
            require(len(hints) == 3, f"{sid}: expected three hints")
        if kind == "read":
            string(step.get("body"))
        if kind == "explain":
            string(step.get("prompt"))
            require(bool(sequence(step.get("rubric"))), f"Missing rubric: {sid}")
            for item in step["rubric"]:
                string(item)
        if kind == "parsons":
            lines = tuple(map(string, sequence(step.get("lines"))))
            require(len(lines) >= 2 and len(set(lines)) == len(lines), f"Invalid lines: {sid}")
            string(step.get("expected_stdout"))
        key = f"{uid}/{sid}"
        catalog.steps[key] = step
        if kind in {"code", "fix", "try"}:
            catalog.problems[key] = code_problem(step, directory)
        if kind in PLAY_TYPES and not (kind == "explain" and step.get("optional") is True):
            playable.append(key)

    require(playable, f"No playable steps: {uid}")
    catalog.play[uid] = playable
    review = mapping(play_file.get("review_cards"))
    card_ids = set()
    for sid in sequence(review.get("from_steps")):
        card_key = f"{uid}/{register(sid, card_ids)}"
        require(card_key in catalog.steps and catalog.steps[card_key]["type"] == "predict",
                f"Invalid review step: {card_key}")
        catalog.cards[card_key] = {"unit": uid, "step": card_key, "kind": "predict"}
    if review.get("vocab"):
        load_vocab(catalog, uid, metadata.get("vocab"))
    catalog.resources[uid] = {
        "lesson": asset(directory, "lesson.md", "", ".md"),
        "vocab": metadata.get("vocab", []),
        **{
            "handson": asset(directory, step["guide"], "", ".md")
            for key, step in catalog.steps.items()
            if key.startswith(uid + "/") and step["type"] == "terminal"
        },
    }

    if "placement" in play_file:
        placement = mapping(play_file["placement"])
        questions = [f"{uid}/{register(sid, set())}" for sid in sequence(placement.get("questions"))]
        require(questions and len(set(questions)) == len(questions)
                and all(q in catalog.cards for q in questions), f"Invalid placement questions: {uid}")
        minimum = placement.get("minimum_correct")
        require(type(minimum) is int and 1 <= minimum <= len(questions),
                f"Invalid placement threshold: {uid}")
        key = f"{uid}/placement"
        require(key not in catalog.steps, f"Reserved placement ID: {key}")
        catalog.problems[key] = Problem(
            starter=string(placement.get("starter")), test_body=string(placement.get("tests")),
        )
        catalog.placements[uid] = {
            "questions": questions, "problem": key, "title": string(placement.get("title")),
            "minimum_correct": minimum,
        }


def load_vocab(catalog, uid, entries):
    entries = [(string(mapping(item).get("en")), string(item.get("ja")))
               for item in sequence(entries)]
    require(len(entries) >= 4 and len({en for en, _ in entries}) == len(entries)
            and len({ja for _, ja in entries}) == len(entries), f"Invalid vocabulary: {uid}")
    for index, (english, _) in enumerate(entries):
        offsets = [(index - index % 4 + n) % len(entries) for n in range(4)]
        term_id = sha256(english.encode("utf-8")).hexdigest()[:16]
        key = f"{uid}/vocab-{term_id}"
        require(key not in catalog.steps and key not in catalog.cards,
                f"Duplicate vocabulary ID: {key}")
        choices = [
            {"text": entries[n][1], "why": f"{entries[n][0]} = {entries[n][1]}"}
            for n in offsets
        ]
        catalog.cards[key] = {
            "unit": uid, "kind": "vocab", "title": english, "choices": choices,
            "answer": offsets.index(index),
        }


def load_catalog(root=ROOT / "content"):
    catalog = Catalog()
    seen = set()
    for stage in sequence(yaml_file(root / "curriculum.yaml").get("stages")):
        stage = mapping(stage)
        number = stage.get("stage")
        require(type(number) is int and number >= 0 and number not in catalog.stages,
                f"Invalid or duplicate stage: {number}")
        catalog.stages[number] = string(stage.get("title"))
        for module in sequence(stage.get("modules")):
            module = mapping(module)
            mid = register(module.get("id"), seen)
            catalog.modules[mid] = {"stage": number, "title": string(module.get("title"))}
            for raw in sequence(module.get("units")):
                unit = mapping(raw)
                uid = register(unit.get("id"), seen)
                catalog.units[uid] = {"module_id": mid, "title": string(unit.get("title")),
                                      "version": 1, "status": "outline"}
    for path in sorted(root.rglob("unit.yaml")):
        load_unit(catalog, path.parent, yaml_file(path))
    ready = set(catalog.units) - set(catalog.play)
    for _ in catalog.play:
        ready.update(uid for uid in catalog.play
                     if all(key in ready for key in catalog.units[uid]["prerequisites"]))
    require(len(ready) == len(catalog.units), "Cyclic unit prerequisites")
    return catalog

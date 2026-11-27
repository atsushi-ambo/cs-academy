import {markdown} from "/markdown.js";

const main = document.querySelector("#main");
const xp = document.querySelector("#xp");
const kinds = {read: "Read", predict: "Predict", try: "Try it", parsons: "Parsons",
  fix: "Fix the bug", code: "Code", explain: "Explain"};
const questNames = {step: "ステップを進める", code: "コード課題に合格", review: "今日の復習"};
let busy = false;

function node(tag, text, className) {
  const item = document.createElement(tag);
  if (text !== undefined) item.textContent = text;
  if (className) item.className = className;
  return item;
}

function link(text, page, className = "button") {
  const item = node("a", text, className);
  item.href = `#${page}`;
  return item;
}

function button(text, click, className = "button") {
  const item = node("button", text, className);
  item.type = "button";
  item.addEventListener("click", click);
  return item;
}

function card(title, label) {
  const section = node("section", undefined, "card");
  if (label) section.append(node("p", label, "kind"));
  section.append(node("h1", title));
  return section;
}

function status() {
  const item = node("p", "", "status");
  item.setAttribute("role", "status");
  return item;
}

function codeBlock(source) {
  const pre = node("pre");
  pre.append(node("code", source));
  return pre;
}

function meter(value, total, label) {
  const item = node("progress");
  item.value = value;
  item.max = total;
  item.setAttribute("aria-label", label);
  return item;
}

async function api(path, body) {
  const options = {cache: "no-store"};
  if (body !== undefined) {
    options.method = "POST";
    options.headers = {"Content-Type": "application/json", "X-CS-Academy": "1"};
    options.body = JSON.stringify(body);
  }
  const response = await fetch(`/api/${path}`, options);
  const result = await response.json();
  if (!response.ok && response.status !== 503) throw new Error(result.error ?? "リクエストに失敗しました。");
  return result;
}

async function hud() {
  const data = await api("today");
  xp.textContent = `${data.xp} XP`;
  return data;
}

async function act(control, message, callback) {
  if (busy) return;
  busy = true;
  control.disabled = true;
  try {
    await callback();
  } catch (error) {
    message.textContent = error.message;
  } finally {
    control.disabled = false;
    busy = false;
  }
}

async function today(view) {
  const data = await hud();
  const unit = data.unit;
  const panel = card(unit?.title ?? "学習パス", "Today");
  if (unit) {
    const percent = Math.round(100 * unit.completed / unit.total);
    const state = unit.status === "completed" ? "修了" : unit.skipped ? "実力診断でスキップ済み" : "進捗";
    panel.append(node("p", `${state} · ${percent}% · ${unit.completed} / ${unit.total} ステップ`, "meta"),
      meter(unit.completed, unit.total, "Unit の進捗"),
      link(unit.status === "completed" ? "修了を表示" : unit.completed ? "続きから" : "ユニットを開く",
        `play/${unit.id}`),
      link("教材を読む", `reference/${unit.id}`, "button secondary"));
  } else {
    panel.append(link("Path を開く", "path"));
  }
  for (const recommendation of data.recommended) {
    const item = node("p", "復習で間違えた内容を確認する ");
    item.append(link(recommendation.title, `play/${recommendation.id}`, "button secondary"));
    panel.append(item);
  }

  const stats = node("div", undefined, "stats");
  for (const [value, label] of [[data.due, "今日の復習"], [data.streak, "学習ストリーク（日）"]]) {
    const stat = node("div");
    stat.append(node("strong", value), node("span", label));
    stats.append(stat);
  }
  const arena = link("Review Arena を開く", "review", "button secondary");
  stats.append(arena);

  const quests = node("section", undefined, "card compact");
  quests.append(node("h2", "Daily quest"));
  const compact = node("input");
  compact.type = "checkbox";
  compact.checked = localStorage.getItem("academy-15-min") === "1";
  const label = node("label", undefined, "toggle");
  label.append(compact, document.createTextNode(" 15分モード"));
  const list = node("ul", undefined, "quests");
  function draw() {
    localStorage.setItem("academy-15-min", compact.checked ? "1" : "0");
    if (!compact.checked) sessionStorage.removeItem("academy-15-deadline");
    const focus = ["review", "step", "code"].find((key) => {
      const {progress, target} = data.quests[key];
      return progress < target;
    });
    const keys = compact.checked ? (focus ? [focus] : [])
      : Object.keys(questNames).filter((key) => data.quests[key].target > 0);
    list.replaceChildren(...keys.map((key) => {
      const {progress, target} = data.quests[key];
      const item = node("li");
      item.append(node("span", questNames[key]), node("strong", `${progress} / ${target}`));
      return item;
    }));
    if (!focus) list.append(node("li", "今日取り組めるクエストはありません。"));
  }
  compact.addEventListener("change", draw);
  draw();
  quests.append(label, list);
  view.append(panel, stats, quests);
}

async function path(view) {
  const {stages} = await api("path");
  const panel = card("Path");
  const labels = {outline: "目次のみ", draft: "下書き", published: "公開済み", completed: "修了"};
  for (const stage of stages) {
    const section = node("details");
    section.open = stage.modules.some((module) => module.units.some((unit) => unit.total));
    section.append(node("summary", `Stage ${stage.number} · ${stage.title}`));
    for (const module of stage.modules) {
      const list = node("ul", undefined, "path-units");
      for (const unit of module.units) {
        const item = node("li");
        item.append(node("strong", unit.title), node("span",
          `${labels[unit.status]}${unit.skipped ? " · スキップ済み" : ""}`, "meta"));
        if (unit.blockers.length) {
          item.append(node("p", `先に修了またはスキップ: ${unit.blockers.map((other) => other.title).join("、")}`));
        } else if (unit.total) {
          item.append(link(unit.status === "completed" ? "振り返る" : "開く", `play/${unit.id}`));
        }
        if (unit.placement) item.append(link("実力診断", `placement/${unit.id}`, "button secondary"));
        list.append(item);
      }
      section.append(node("h2", module.title), list);
    }
    panel.append(section);
  }
  view.append(panel);
}

function choices(parent, values, select) {
  const group = node("div", undefined, "choices");
  const buttons = values.map((value, i) => {
    const item = button(value, () => select(i, item), "choice");
    group.append(item);
    return item;
  });
  parent.append(group);
  return buttons;
}

function feedback(buttons, chosen, result) {
  buttons.forEach((item, index) => {
    item.disabled = true;
    if (index === result.answer) item.classList.add("correct");
    if (index === chosen && !result.correct) item.classList.add("incorrect");
    const label = index === result.answer ? "正解 — " : index === chosen ? "選択した回答 — " : "";
    item.append(node("span", label + result.why[index], "why"));
  });
}

function nextButton(view, resume) {
  const next = button("次のステップ", resume);
  view.append(next);
  next.focus();
}

function hints(parent, step, message, send) {
  if (!step.max_hints) return null;
  const list = node("ol", undefined, "hints");
  list.append(...step.hints.map((hint) => node("li", hint)));
  const ask = button("ヒント", () => act(ask, message, async () => {
    const result = await send("hint", {level: list.children.length + 1});
    list.append(node("li", result.hint));
    update();
  }), "button secondary");
  function update() {
    const level = list.children.length + 1;
    ask.hidden = level > step.max_hints;
    ask.textContent = `ヒント ${level} / ${step.max_hints}`;
  }
  update();
  parent.append(list, ask);
  return ask;
}

function parsons(panel, step, send, message, resume) {
  const hint = hints(panel, step, message, send);
  const placed = node("ol", undefined, "placed");
  const order = [];
  const buttons = choices(panel, step.lines, (index, item) => {
    order.push(index);
    item.disabled = true;
    placed.append(node("li", step.lines[index]));
    check.disabled = order.length !== step.lines.length;
  });
  const reset = button("やり直す", () => {
    order.length = 0;
    placed.replaceChildren();
    buttons.forEach((item) => { item.disabled = false; });
    check.disabled = true;
    message.textContent = "";
  }, "button secondary");
  const check = button("順序を確認", () => act(check, message, async () => {
    const result = await send("order", {order});
    message.textContent = result.complete ? "正しい順序です。" : "コードの順序を見直してください。";
    if (!result.complete) return;
    if (hint) hint.hidden = true;
    check.hidden = reset.hidden = true;
    panel.append(codeBlock(result.stdout));
    nextButton(panel, resume);
    await hud();
  }));
  check.disabled = true;
  panel.append(placed, reset, check);
}

function textarea(label, value, rows, code = false) {
  const box = node("label", label, "editor-label");
  const area = node("textarea", undefined, code ? "editor" : "stdin");
  area.rows = rows;
  area.spellcheck = false;
  area.autocomplete = "off";
  area.setAttribute("autocapitalize", "off");
  area.value = value;
  box.append(area);
  return [box, area];
}

function output(result) {
  const container = node("div", undefined, "output");
  const labels = {passed: "成功", failed: "失敗", timeout: "10秒でタイムアウト", unavailable: "ランナーを起動できません"};
  container.append(node("strong", labels[result.status]));
  for (const [name, value] of [["stdout", result.stdout], ["stderr", result.stderr]]) {
    if (value) container.append(node("p", name, "meta"), codeBlock(value));
  }
  if (result.truncated) container.append(node("p", "出力の上限を超えた部分を省略しました。"));
  return container;
}

function editor(panel, step, send, message, resume) {
  const draft = `academy-draft-${step.id}`;
  const [sourceLabel, source] = textarea("Python", sessionStorage.getItem(draft) ?? step.starter, 12, true);
  source.addEventListener("input", () => sessionStorage.setItem(draft, source.value));
  const [stdinLabel, stdin] = textarea("標準入力（Run 用）", "", 2);
  const fields = node("fieldset");
  fields.append(sourceLabel, stdinLabel);
  const controls = node("div", undefined, "actions");
  const hintPanel = node("div");
  const showHint = hints(hintPanel, step, message, send);
  const resultBox = node("div");
  resultBox.setAttribute("aria-live", "polite");
  function runButton(title, name) {
    const trigger = button(title, () => act(trigger, message, async () => {
      message.textContent = "Docker で実行中…";
      const payload = {source: source.value};
      if (name === "run") payload.stdin = stdin.value;
      const result = await send(name, payload);
      resultBox.replaceChildren(output(result));
      message.textContent = name === "tests" ? `Run tests の失敗回数 ${result.failures}`
        : step.type === "try" && result.status === "passed" && !result.complete
          ? "課題の指示どおりに編集して、もう一度 Run を押してください。" : "";
      if (result.can_open_solution) showSolution.hidden = false;
      if (result.complete) {
        fields.disabled = true;
        if (showHint) showHint.hidden = true;
        sessionStorage.removeItem(draft);
        nextButton(panel, resume);
        await hud();
      }
    }), name === "run" && step.tests ? "button secondary" : "button");
    return trigger;
  }
  controls.append(runButton("Run", "run"));
  if (step.tests) controls.append(runButton("Run tests", "tests"));
  fields.append(controls);
  panel.append(fields, hintPanel, resultBox);
  const showSolution = solutionButton(panel, step, send, message);
}

function solutionButton(panel, step, send, message) {
  const solution = node("div");
  const showSolution = button("模範解答を開く", () => act(showSolution, message, async () => {
    const result = await send("solution");
    solution.replaceChildren(codeBlock(result.solution), markdown(result.explanation));
    showSolution.hidden = true;
  }), "button secondary");
  showSolution.hidden = !step.can_open_solution;
  panel.append(showSolution, solution);
  return showSolution;
}

function sessionTimer() {
  const now = Date.now();
  const stored = Number(sessionStorage.getItem("academy-15-deadline"));
  const deadline = Number.isFinite(stored) && stored > now ? stored : now + 900000;
  sessionStorage.setItem("academy-15-deadline", String(deadline));
  const label = node("span");
  const tick = () => {
    const seconds = Math.max(0, Math.ceil((deadline - Date.now()) / 1000));
    label.textContent = `15分モード · 残り ${minutes(seconds)}`;
    return seconds;
  };
  tick();
  const timer = setInterval(() => {
    if (!label.isConnected || !tick()) clearInterval(timer);
  }, 1000);
  return label;
}

function minutes(seconds) {
  return `${Math.floor(seconds / 60)}:${String(seconds % 60).padStart(2, "0")}`;
}

async function play(view, uid, selected, open) {
  if (!uid) uid = (await hud()).unit?.id;
  if (!uid) {
    view.append(link("Path を開く", "path"));
    return;
  }
  const url = `play?unit=${encodeURIComponent(uid)}`;
  if (open) await api("play", {unit: uid, action: "start"});
  const {step, unit, index, total, completed_steps: completed} = await api(
    selected ? `${url}&step=${encodeURIComponent(selected)}` : url);
  const resume = () => load("play", uid);
  if (completed.length) {
    const label = node("label", "完了したステップを振り返る ");
    const select = node("select");
    const latest = node("option", completed.length === total ? "修了画面" : "続きから");
    latest.value = "";
    select.append(latest);
    for (const {id, title} of completed) {
      const option = node("option", title);
      option.value = id;
      select.append(option);
    }
    select.value = selected ?? "";
    select.addEventListener("change", () => load("play", uid, select.value));
    label.append(select);
    view.append(label);
  }
  if (!step) {
    const done = card(unit, "Unit 修了");
    done.append(node("p", "四択の復習は、出題日に Review Arena に表示されます。"),
      link("Review Arena", "review"), link("教材を読む", `reference/${uid}`, "button secondary"));
    view.append(done);
    return;
  }
  const header = node("div", undefined, "unit-progress");
  header.append(node("span", unit), node("span", `${index} / ${total}`));
  if (localStorage.getItem("academy-15-min") === "1") header.append(sessionTimer());
  header.append(meter(completed.length, total, "完了したステップ"));
  const panel = card(step.title, kinds[step.type]);
  const message = status();
  panel.append(message);
  const links = node("div");
  links.append(link("Path", "path", "button secondary"),
    link("教材を読む", `reference/${uid}`, "button secondary"));
  view.append(links, header, panel);
  const send = (action, data = {}) => api("play", {unit: uid, step: step.id, action, ...data});
  if (step.body) panel.append(markdown(step.body));
  if (step.task) panel.append(node("p", step.task));
  if (step.code) panel.append(codeBlock(step.code));
  if (step.type === "explain") {
    explain(panel, step, send, message, resume);
  } else if (step.complete) {
    if (step.choices) feedback(choices(panel, step.choices, () => {}), -1, step.feedback);
    if (step.lines) panel.append(codeBlock(step.lines.join("\n")));
    if (step.starter) panel.append(codeBlock(step.starter));
    if (step.can_open_solution) solutionButton(panel, step, send, message);
  } else if (step.type === "read") {
    const next = button("次のステップ", () => act(next, message, async () => {
      await send("continue");
      await resume();
    }));
    panel.append(next);
  } else if (step.type === "predict") {
    const hint = hints(panel, step, message, send);
    const buttons = choices(panel, step.choices, (choice, control) => act(control, message, async () => {
      const result = await send("answer", {choice});
      feedback(buttons, choice, result);
      if (hint) hint.hidden = true;
      message.textContent = result.correct ? "正解です。" : "解説を確認してください。";
      nextButton(panel, resume);
      await hud();
    }).then(() => { if (buttons[choice].querySelector(".why")) control.disabled = true; }));
  } else if (step.type === "parsons") {
    parsons(panel, step, send, message, resume);
  } else {
    editor(panel, step, send, message, resume);
  }
}

function explain(panel, step, send, message, resume) {
  const draft = `academy-draft-${step.id}`;
  panel.append(node("p", step.prompt));
  const checklist = node("ul", undefined, "rubric");
  const checks = step.rubric.map((criterion) => {
    const item = node("li");
    const label = node("label", undefined, "radio");
    const check = node("input");
    check.type = "checkbox";
    check.disabled = step.complete;
    check.checked = step.complete;
    label.append(check, document.createTextNode(criterion));
    item.append(label);
    checklist.append(item);
    return check;
  });
  const [label, response] = textarea("英語での説明（このタブに保存）", sessionStorage.getItem(draft) ?? "", 5);
  response.readOnly = step.complete;
  panel.append(label, checklist);
  if (step.complete) return;
  response.addEventListener("input", () => sessionStorage.setItem(draft, response.value));
  const finish = button("自己評価を完了", () => act(finish, message, async () => {
    if (!response.value.trim() || checks.some((check) => !check.checked)) {
      message.textContent = "説明を書き、評価項目を確認してください。";
      return;
    }
    await send("explain", {response: response.value, self_checked: true});
    await resume();
    await hud();
  }));
  panel.append(finish);
}

async function review(view) {
  let queue = await api("reviews");
  const round = card("Review Arena");
  const progress = node("p", "", "meta");
  const questionBox = node("div");
  round.append(progress, questionBox);
  view.append(round);
  let combo = 0;
  let answered = 0;
  const start = Date.now();
  function clock() {
    const seconds = Math.max(0, 300 - Math.floor((Date.now() - start) / 1000));
    progress.textContent = `${answered} 問回答 · ${combo} コンボ · 残り ${minutes(seconds)}`;
    return seconds;
  }
  function draw() {
    const retry = !queue.due.length;
    const question = (retry ? queue.retries : queue.due)[0];
    questionBox.replaceChildren();
    clock();
    if (!question) {
      questionBox.append(node("p", answered ? "今日のラウンドが終わりました。" : "今日の復習はありません。"),
        link("Today", "today", "button secondary"));
      return;
    }
    questionBox.append(node("p", question.unit, "meta"), node("h2", question.title));
    if (retry) questionBox.append(node("p", "間違えた問題をもう一度"));
    if (question.code) questionBox.append(codeBlock(question.code));
    const message = status();
    const buttons = choices(questionBox, question.choices, (choice, control) => {
      act(control, message, async () => {
        const result = await api("review", {card: question.id, choice, retry});
        feedback(buttons, choice, result);
        combo = result.correct ? combo + 1 : 0;
        answered += 1;
        clock();
        const next = button("続ける", () => act(next, message, async () => {
          queue = await api("reviews");
          draw();
        }));
        questionBox.append(next);
        next.focus();
        await hud();
      }).then(() => { if (buttons[choice].querySelector(".why")) control.disabled = true; });
    });
    questionBox.append(message);
  }
  draw();
  const timer = setInterval(() => {
    if (!queue.due.length && !queue.retries.length || !progress.isConnected || !clock()) clearInterval(timer);
  }, 1000);
}

async function placement(view, uid) {
  const url = `placement?unit=${encodeURIComponent(uid)}`;
  const data = await api(url);
  const panel = card(data.unit, "Placement");
  const message = status();
  const resultBox = node("div");
  const actions = node("div", undefined, "actions");
  function showResult(result, canSkip, skipped) {
    resultBox.replaceChildren();
    actions.replaceChildren();
    if (result?.passed) {
      const summary = skipped ? "スキップを選択済み" : canSkip ? "合格 · スキップ候補" : "合格";
      resultBox.append(node("p", `${result.correct} / ${result.questions} 問正解 · ${summary}`, "notice"));
    } else if (result && "correct" in result) {
      resultBox.append(node("p", `${result.correct} / ${result.questions} 問正解 · 再挑戦できます。`, "notice"));
    }
    if (result?.execution) resultBox.append(output(result.execution));
    if (canSkip) {
      const skip = button("このユニットをスキップする", () => act(skip, message, async () => {
        await api("placement/skip", {unit: uid});
        showResult(result, false, true);
        message.textContent = "今日から1日2枚ずつ、このユニットの四択が復習に追加されます。";
      }), "button secondary");
      actions.append(skip);
    }
  }
  panel.append(node("p", `四択${data.questions.length}問とコード課題1問に取り組みます。合格ラインは四択${data.minimum_correct}問以上の正解とコード課題の合格です。`));
  const selections = [];
  data.questions.forEach((question, index) => {
    const group = node("fieldset", undefined, "placement-question");
    group.append(node("legend", `${index + 1}. ${question.title}`));
    if (question.code) group.append(codeBlock(question.code));
    const items = question.choices.map((value, i) => {
      const item = node("label", undefined, "radio");
      const input = node("input");
      input.type = "radio";
      input.name = `q${index}`;
      input.addEventListener("change", () => { selections[index] = i; });
      item.append(input, document.createTextNode(value));
      return item;
    });
    group.append(...items);
    panel.append(group);
  });
  const [label, source] = textarea(data.title, data.starter, 10, true);
  const submit = button("診断を提出", () => act(submit, message, async () => {
    const answers = data.questions.map((_, i) => selections[i]);
    if (answers.some((answer) => answer === undefined)) {
      message.textContent = "四択のすべてに回答してください。";
      return;
    }
    message.textContent = "診断のコードを Docker で実行中…";
    const result = await api("placement", {unit: uid, answers, source: source.value});
    const placementState = await api(url);
    showResult({...placementState.result, execution: result.execution}, placementState.can_skip, placementState.skipped);
    message.textContent = "";
  }));
  showResult(data.result, data.can_skip, data.skipped);
  panel.append(label, submit, message, resultBox, actions, link("Path に戻る", "path", "button secondary"));
  view.append(panel);
}

async function backups(view) {
  const panel = card("バックアップと復元");
  const message = status();
  const existing = node("div");
  const create = button("バックアップを作成", () => act(create, message, async () => {
    const saved = await api("backup", {});
    message.textContent = `保存しました · ${saved.backup}`;
    await refresh();
  }));
  async function refresh() {
    const {backups: ids} = await api("backups");
    existing.replaceChildren(node("h2", "保存済みバックアップ"));
    if (!ids.length) {
      existing.append(node("p", "バックアップはまだありません。"));
      return;
    }
    const label = node("label", "復元するバックアップ");
    const select = node("select");
    for (const id of ids) {
      const option = node("option", id);
      option.value = id;
      select.append(option);
    }
    const restore = button("復元する", () => {
      if (!confirm("選んだバックアップに復元しますか？ 現在のデータは先に別のバックアップへ保存されます。")) return;
      act(restore, message, async () => {
        const result = await api("restore", {backup: select.value, confirm: true});
        for (const key of Object.keys(sessionStorage)) {
          if (key.startsWith("academy-draft-")) sessionStorage.removeItem(key);
        }
        message.textContent = `復元しました。${result.saved_previous ? ` 復元前のバックアップ · ${result.saved_previous}` : ""}`;
        await refresh();
        await hud();
      });
    }, "button secondary");
    label.append(select);
    existing.append(label, restore);
  }
  panel.append(node("p", "学習履歴と復習予定をこの Mac に保存します。"), create, message, existing);
  view.append(panel);
  await refresh();
}

async function reference(view, uid) {
  const data = await api(`reference?unit=${encodeURIComponent(uid)}`);
  const panel = card(data.title);
  panel.append(link("Play", `play/${uid}`));
  for (const [name, text] of [["レッスンの参照シート", data.lesson], ["端末でのハンズオン", data.handson]]) {
    if (!text) continue;
    const section = node("details");
    section.append(node("summary", name), markdown(text));
    panel.append(section);
  }
  const vocabulary = node("details");
  const terms = node("dl");
  for (const term of data.vocab) terms.append(node("dt", term.en), node("dd", term.ja));
  vocabulary.append(node("summary", "英単語"), terms);
  if (data.vocab.length) panel.append(vocabulary);
  view.append(panel);
}

const pages = {today, path, play, review, placement, backups, reference};
async function load(page, uid, selectedStep, open = false) {
  const selected = Object.hasOwn(pages, page) ? page : "today";
  for (const item of document.querySelectorAll("nav a")) {
    if (item.hash === `#${selected}`) item.setAttribute("aria-current", "page");
    else item.removeAttribute("aria-current");
  }
  const view = node("div", undefined, "view");
  const loading = status();
  loading.textContent = "読み込み中…";
  view.append(loading);
  main.replaceChildren(view);
  try {
    await pages[selected](view, uid, selectedStep, open);
    loading.remove();
  } catch (error) {
    loading.textContent = error.message;
  }
}

function route() {
  const [page, uid] = location.hash.slice(1).split("/");
  return load(page, uid, undefined, true);
}

window.addEventListener("hashchange", route);
route();
hud().catch(() => {});

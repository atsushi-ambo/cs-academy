import assert from "node:assert/strict";
import {readFile} from "node:fs/promises";
import test from "node:test";
import vm from "node:vm";

class Element {
  children = [];
  events = {};
  textContent = "";

  constructor(tag) { this.tag = tag; }
  append(...children) { this.children.push(...children); }
  replaceChildren(...children) { this.children = children; }
  addEventListener(name, callback) { this.events[name] = callback; }
  setAttribute() {}
  remove() {}

  all(tag) {
    return [...(this.tag === tag ? [this] : []), ...this.children.flatMap((child) => child.all(tag))];
  }
}

const now = 1_000_000;
const zeroQuest = {progress: 0, target: 0};
const uid = "s1.m03.u01";
const summary = {
  unit: {id: uid, title: "Lists", completed: 2, total: 2, status: "completed"},
  recommended: [], xp: 0, due: 0, streak: 0,
  quests: {step: zeroQuest, code: zeroQuest, review: zeroQuest},
};

async function boot(responses) {
  const main = new Element("main");
  const xp = new Element("span");
  const session = new Map();
  const context = vm.createContext({
    Date: {now: () => now},
    document: {
      querySelector: (selector) => selector === "#main" ? main : xp,
      querySelectorAll: () => [],
      createElement: (tag) => new Element(tag),
      createTextNode: (text) => Object.assign(new Element("#text"), {textContent: text}),
    },
    window: {addEventListener() {}},
    location: {hash: "#today"},
    localStorage: {getItem: () => "1", setItem() {}},
    sessionStorage: {
      getItem: (key) => session.get(key), setItem: (key, value) => session.set(key, value),
    },
    setInterval() {},
    fetch: async (path, options) => {
      const response = responses(options.method ?? "GET", path, options.body);
      assert.ok(response, `Unexpected request ${path}`);
      return {ok: true, json: async () => response};
    },
  });
  const source = await readFile(new URL("../web/app.js", import.meta.url), "utf8");
  const markdown = await readFile(new URL("../web/markdown.js", import.meta.url), "utf8");
  const app = new vm.SourceTextModule(source + "\nexport {load};", {context});
  await app.link(() => new vm.SourceTextModule(markdown, {context}));
  await app.evaluate();
  return {main, session, load: app.namespace.load};
}

test("Play replaces an expired deadline and keeps an active deadline", async () => {
  let index = 1;
  const {main, session, load} = await boot((_, path) => path === "/api/today" ? summary : {
    completed_steps: [], unit: "Lists", index, total: 2, step: {type: "read", title: "Read"},
  });
  const key = "academy-15-deadline";
  session.set(key, String(now));
  await load("play");
  assert.equal(session.get(key), String(now + 900_000));
  assert.ok(main.all("span").some((item) => item.textContent === "15分モード · 残り 15:00"));
  session.set(key, String(now + 60_000));
  index = 2;
  await load("play");
  assert.equal(session.get(key), String(now + 60_000));
  assert.ok(main.all("span").some((item) => item.textContent === "15分モード · 残り 1:00"));
});

test("Today only selects quests with work left in 15-minute mode", async () => {
  let data = summary;
  const {main, load} = await boot(() => data);
  await load("today");
  assert.ok(main.all("li").some((item) => item.textContent === "今日取り組めるクエストはありません。"));
  assert.equal(main.all("li").length, 1);
  data = {...summary, unit: {...summary.unit, completed: 1, status: "draft"}, quests: {
    step: {progress: 0, target: 1}, code: zeroQuest, review: {progress: 1, target: 1},
  }};
  await load("today");
  assert.deepEqual(main.all("li").flatMap((item) => item.all("span").map((span) => span.textContent)),
    ["ステップを進める"]);
});

test("Play reopens a completed code solution in read-only mode", async () => {
  const id = "s1.m03.u01/st14";
  const title = "<strong>Code</strong>";
  const play = {completed_steps: [{id, title}], unit: "Lists", total: 1};
  const solution = "def last_and_first(items): ...";
  const {main, load} = await boot((method, path, body) => {
    if (path === "/api/today") return summary;
    if (method === "POST") {
      assert.deepEqual(JSON.parse(body), {unit: uid, step: id, action: "solution"});
      return {solution, explanation: "Explanation"};
    }
    if (path === `/api/play?unit=${uid}&step=${encodeURIComponent(id)}`) return {
      ...play, index: 1, step: {
        id, type: "code", title, starter: "pass", complete: true, can_open_solution: true,
      },
    };
    if (path === `/api/play?unit=${uid}`) return {...play, step: null};
  });
  await load("play");
  const [select] = main.all("select");
  assert.equal(select.all("option")[1].textContent, title);
  select.value = id;
  await select.events.change();
  assert.equal(main.all("h1")[0].textContent, title);
  assert.equal(main.all("textarea").length, 0);
  const [open] = main.all("button");
  assert.equal(open.textContent, "模範解答を開く");
  await open.events.click();
  assert.ok(main.all("code").some((item) => item.textContent === solution));
});


test("Path shows prerequisites and only links playable units that are open", async () => {
  const stages = [{number: 1, title: "Python", modules: [{title: "Control flow", units: [
    {id: "outline", title: "Conditions", status: "outline", blockers: [], total: 0},
    {id: "for", title: "For loops", status: "published", blockers: [], total: 20, placement: true},
    {id: "while", title: "While loops", status: "draft", blockers: [{id: "for", title: "For loops"}], total: 20},
  ]}]}];
  const {main, load} = await boot((_, path) => path === "/api/today" ? summary : {stages});
  await load("path");
  assert.deepEqual(main.all("strong").map((item) => item.textContent), ["Conditions", "For loops", "While loops"]);
  assert.deepEqual(main.all("a").map((item) => item.href), ["#play/for", "#placement/for"]);
  assert.ok(main.all("p").some((item) => item.textContent.includes("For loops")));
});

test("Opening a unit and submitting a checked explanation use the same unit ID", async () => {
  const unit = "s2.m05.u01";
  const step = {
    id: unit + "/st21", type: "explain", title: "Explain", prompt: "Write 2–3 sentences.",
    rubric: ["Name the base case."],
  };
  const posts = [];
  const {main, load} = await boot((method, path, body) => {
    if (path === "/api/today") return summary;
    if (method === "POST") {
      posts.push(JSON.parse(body));
      return {complete: true};
    }
    assert.equal(path, `/api/play?unit=${unit}`);
    return {unit: "Thinking recursively", total: 1, index: 1, completed_steps: [], step};
  });
  await load("play", unit, undefined, true);
  main.all("textarea")[0].value = "The base case ends the work. Here it returns zero.";
  const [finish] = main.all("button");
  await finish.events.click();
  assert.equal(posts.length, 1);
  main.all("input")[0].checked = true;
  await finish.events.click();
  assert.deepEqual(posts, [
    {unit, action: "start"},
    {unit, step: step.id, action: "explain", self_checked: true,
      response: "The base case ends the work. Here it returns zero."},
  ]);
});

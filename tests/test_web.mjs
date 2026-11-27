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
const summary = {
  unit: "Lists", xp: 0, completed: 2, total: 2, due: 0, streak: 0,
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
  data = {...summary, completed: 1, quests: {
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
      assert.deepEqual(JSON.parse(body), {step: id, action: "solution"});
      return {solution, explanation: "Explanation"};
    }
    if (path === `/api/play?step=${encodeURIComponent(id)}`) return {
      ...play, index: 1, step: {
        id, type: "code", title, starter: "pass", complete: true, can_open_solution: true,
      },
    };
    if (path === "/api/play") return {...play, step: null};
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

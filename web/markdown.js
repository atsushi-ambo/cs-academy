function element(tag, value) {
  const node = document.createElement(tag);
  if (value !== undefined) node.textContent = value;
  return node;
}

function inline(node, text) {
  const token = /`([^`]+)`|\*\*([^*]+)\*\*|\*([^*]+)\*/g;
  let end = 0;
  for (const match of text.matchAll(token)) {
    node.append(document.createTextNode(text.slice(end, match.index)));
    const [, code, strong, emphasis] = match;
    node.append(element(code ? "code" : strong ? "strong" : "em", code ?? strong ?? emphasis));
    end = match.index + match[0].length;
  }
  node.append(document.createTextNode(text.slice(end)));
  return node;
}

function cells(line) {
  return line.trim().slice(1, -1).split("|").map((value) => value.trim());
}

export function markdown(source) {
  const root = element("div");
  root.className = "markdown";
  const lines = source.split(/\r?\n/);
  const startsBlock = /^(?:```|#{1,6} |[-*] |\d+\. |> |\|)/;
  while (lines.length) {
    const line = lines.shift();
    if (!line.trim()) continue;
    if (line.startsWith("```")) {
      const body = [];
      while (lines.length && !lines[0].startsWith("```")) body.push(lines.shift());
      if (lines.length) lines.shift();
      const pre = element("pre");
      pre.append(element("code", body.join("\n")));
      root.append(pre);
      continue;
    }
    const heading = /^(#{1,6}) (.+)$/.exec(line);
    if (heading) {
      root.append(inline(element(`h${Math.min(6, heading[1].length + 1)}`), heading[2]));
      continue;
    }
    const bullet = /^([-*]|\d+\.) (.+)$/.exec(line);
    if (bullet) {
      const numbered = /\d/.test(bullet[1]);
      const list = element(numbered ? "ol" : "ul");
      const prefix = numbered ? /^\d+\. (.+)$/ : /^[-*] (.+)$/;
      list.append(inline(element("li"), bullet[2]));
      while (prefix.test(lines[0] ?? "")) {
        list.append(inline(element("li"), prefix.exec(lines.shift())[1]));
      }
      root.append(list);
      continue;
    }
    if (line.startsWith("|") && /^\|[\s|:-]+\|\s*$/.test(lines[0] ?? "")) {
      lines.shift();
      const table = element("table");
      const head = table.createTHead().insertRow();
      for (const cell of cells(line)) head.append(inline(element("th"), cell));
      const body = table.createTBody();
      while ((lines[0] ?? "").startsWith("|")) {
        const row = body.insertRow();
        for (const cell of cells(lines.shift())) row.append(inline(element("td"), cell));
      }
      const wrapper = element("div");
      wrapper.className = "table-scroll";
      wrapper.append(table);
      root.append(wrapper);
      continue;
    }
    if (line.startsWith("> ")) {
      root.append(inline(element("blockquote"), line.slice(2)));
      continue;
    }
    const paragraph = [line];
    while (lines[0]?.trim() && !startsBlock.test(lines[0])) paragraph.push(lines.shift());
    root.append(inline(element("p"), paragraph.join(" ")));
  }
  return root;
}

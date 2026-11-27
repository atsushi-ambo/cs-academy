# Hands-on: A Tiny Server Health Report

Time: about 30 minutes. You will type every command yourself. Do not copy and
paste: typing builds memory.

## Goal

At the end, you will have a script that takes a list of servers and their
response times, and prints a short report. You will also save your work with Git.

## Before you start (first time only)

- You need Python 3.9 or newer. Check with `python3 --version`. On a new Mac,
  the first `python3` or `git` command may ask you to install the
  "Command Line Tools". Click **Install** and wait until it finishes.
- Use a code editor such as **VS Code**. Do not use TextEdit: it saves rich
  text by default, and Python cannot read it.
- Tell Git your name and email once (Git writes them in every commit):

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

## Step 1. Explore in the Python REPL

Open a terminal and start Python:

```bash
python3
```

You will see `>>>`. This is the **REPL** (Read–Eval–Print Loop). Type each
line and look at the result before you type the next one.

```python
>>> servers = ["web01", "web02", "db01"]
>>> servers[0]
'web01'
>>> servers[-1]
'db01'
>>> len(servers)
3
>>> servers.append("cache01")
>>> servers
['web01', 'web02', 'db01', 'cache01']
>>> servers[1:3]
['web02', 'db01']
>>> "db01" in servers
True
>>> servers[10]
Traceback (most recent call last):
  ...
IndexError: list index out of range
```

Type only the lines that start with `>>>`. The other lines show what Python
should answer.

The last line gives an `IndexError`. Read the message. What is the last valid
index? Write the answer in your notes.

Now try the aliasing surprise:

```python
>>> a = [1, 2, 3]
>>> b = a
>>> b.append(4)
>>> a
>>> c = a.copy()
>>> c.append(5)
>>> a
>>> c
```

Explain to yourself, out loud in English, why `a` changed the first time but
not the second time. Type `exit()` to leave.

## Step 2. Create a project folder with Git

```bash
mkdir -p ~/cs-academy-work/s1-lists
cd ~/cs-academy-work/s1-lists
git init
```

## Step 3. Write the script

Open the folder in VS Code (`code .`, or File → Open Folder), and create a
file named `report.py` there:

```python
servers = ["web01", "web02", "db01", "cache01"]
response_ms = [120, 950, 80, 1500]

print(f"Servers checked: {len(servers)}")

slow = []
for i in range(len(servers)):
    if response_ms[i] > 500:
        slow.append(servers[i])

print(f"Slow servers (> 500 ms): {slow}")
print(f"Fastest response: {min(response_ms)} ms")
print(f"Average response: {sum(response_ms) / len(response_ms):.1f} ms")
```

Run it:

```bash
python3 report.py
```

Expected output:

```text
Servers checked: 4
Slow servers (> 500 ms): ['web02', 'cache01']
Fastest response: 80 ms
Average response: 662.5 ms
```

If your output is different, compare your code line by line. Typos are the
most common cause.

## Step 4. Make it better with `zip`

Using `range(len(...))` and two indexes works, but it is easy to mix up.
Python's `zip()` walks through two lists together:

```python
for server, ms in zip(servers, response_ms):
    if ms > 500:
        slow.append(server)
```

Change your script to use `zip`. Run it again. The output must be the same.
This is called **refactoring**: improving the code without changing what it does.

## Step 5. Break it on purpose

Remove the last item from `response_ms` only (so the lists have different
lengths). Run the script. What happens with `zip`? What would happen with the
`range(len(servers))` version? Write down both answers, then restore the item.

> Lesson: when two lists must match, check their lengths. Real data is often
> broken in exactly this way.

## Step 6. Save your work

```bash
git add report.py
git commit -m "Add server health report using lists"
```

Your commit is the **evidence** for this hands-on. In the app, press
"Check" on this step: the app runs `git log -1` and `python3 report.py` in
`~/cs-academy-work/s1-lists` (read-only) and compares the output.

## Done when

- [ ] `python3 report.py` prints the expected output.
- [ ] The script uses `zip`.
- [ ] You can explain, in English, what happens when the lists have different lengths.
- [ ] The work is committed with Git.

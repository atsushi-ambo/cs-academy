# 🐉 World 12: The Language Forge — Compilers and Programming Languages

> Behind the library, there is a forge run by a dragon.
> The dragon devours the incantations humans write (source code) and breathes out the language of machines.
> "You want to see what's inside my belly? Very well.
> **One who can build a language can never be fooled by any language.** The truth behind error messages,
> the traps of performance — all of it will become visible to you."

**Corresponding university courses**: Stanford **CS143 Compilers** / Berkeley **CS164** / MIT **6.035** / upstream [Compilers section](https://github.com/jwasham/coding-interview-university#compilers)
**Prerequisites**: World 3 (trees), World 6 (recursion), cross-referenced with World 13 (regular languages & CFGs)

**What you'll learn in this chapter**
- The big picture of the compiler pipeline
- Lexical analysis (tokenization)
- Parsing (grammars, ASTs, recursive descent)
- Semantic analysis and type checking
- Intermediate representations, optimization, code generation
- Runtime: stack frames and garbage collection

---

## 📖 Lecture 1: The Dragon's Digestive Tract — The Whole Pipeline (15 XP)

```
Source code
   │ ① Lexical analysis (lexer)  …… string → token stream
   ▼
Token stream
   │ ② Parsing (parser)          …… token stream → syntax tree (AST)
   ▼
AST
   │ ③ Semantic analysis         …… name resolution & type checking
   ▼
Checked AST
   │ ④ Intermediate representation (IR) generation → ⑤ optimization
   ▼
   │ ⑥ Code generation           …… register allocation & machine code emission
   ▼
Machine code / bytecode
```

Stages ①–③ are called the **frontend** (per language), and ④–⑥ the **backend** (per CPU).
The greatness of LLVM lies in decoupling the two via a "shared IR" — so m languages × n CPUs need only m + n components instead of m × n.

## 📖 Lecture 2: Chewing the Incantation — Lexical Analysis (15 XP)

`let x = 42 + y;` → `[LET] [IDENT "x"] [EQ] [NUM 42] [PLUS] [IDENT "y"] [SEMI]`

The shape of each token can be written as a **regular expression** (numbers are `[0-9]+`, identifiers are `[a-zA-Z_][a-zA-Z0-9_]*`).
And a regular expression can be converted into a **DFA (deterministic finite automaton)** that decides membership simply by feeding it one character at a time
— we'll prove this theoretical guarantee in World 13. A lexer is "a machine that lines up DFAs and cuts at the longest match."

## 📖 Lecture 3: The Grammar of the Incantation — Parsing and the AST (15 XP)

We check whether the token stream conforms to the grammar and assemble an **abstract syntax tree (AST)**. The grammar is written as a **context-free grammar (CFG)**:

```
Expr   → Term (('+' | '-') Term)*
Term   → Factor (('*' | '/') Factor)*
Factor → NUM | IDENT | '(' Expr ')'
```

This notation (BNF) has **operator precedence baked right in**:
since `*` lives at a deeper level of the grammar than `+`, `1 + 2 * 3` naturally yields the tree for `1 + (2 * 3)`.

```
      (+)
     /   \
    1    (*)
        /   \
       2     3
```

**Recursive descent parser**: the easiest style to hand-write, mapping one grammar rule to one function.
`parse_expr` calls `parse_term`, which calls `parse_factor` — the recursion of the grammar becomes the recursion of the functions directly (the moment World 6's recursion gives birth to a language).

## 📖 Lecture 4: The Meaning of the Incantation — Semantic Analysis and Types (15 XP)

Syntactically correct doesn't mean meaningful ("colorless green ideas sleep furiously").

- **Name resolution**: which declaration does each identifier refer to. **Scope** is implemented as a stack of symbol tables (push when entering a block, pop when leaving)
- **Type checking**: descend the AST recursively, computing types and checking they satisfy the rules.
  `if e1 then e2 else e3` ⇒ e1 must be bool, e2 and e3 must be the same type, and the whole expression has that type — a collection of such **typing rules**

| | Static typing (Java, Rust, TS) | Dynamic typing (Python, JS) |
|---|---|---|
| When checking happens | Compile time | Run time |
| Strength | Catches bugs early, enables optimization | Flexible, quick to start writing |

**Type inference** (Hindley-Milner) is the magic of "types get determined even without writing them." The bloodline of OCaml/Haskell now flows into TypeScript and Rust.

## 📖 Lecture 5: The Dragon's Refinement — Optimization and Code Generation (15 XP)

Optimization is a transformation that makes things faster **without changing observable behavior**. Classic techniques:

- **Constant folding**: compute `2 * 3.14 * r` → `6.28 * r` at compile time
- **Common subexpression elimination**: don't do the same computation twice
- **Dead code elimination** / **function inlining** / **loop-invariant code motion**

**Register allocation**: there are infinitely many variables but only a dozen or so registers.
Solved as a **graph coloring problem on the interference graph** (World 5's graph theory!), where variables that are "live at the same time" are joined by an edge.
If it can't be colored with k colors, the overflow variables go to memory (spill).

## 📖 Lecture 6: Where the Incantation Lives — Runtime and GC (15 XP)

- **Stack frame**: on each function call, "arguments, return address, local variables" get pushed (the concrete form of World 6's call stack). The calling convention dictates "who saves which registers"
- **Heap**: a place for data whose lifetime doesn't match the call. Manual management (C's malloc/free) suffers the triple curse of forgotten frees, double frees, and use-after-free

### Garbage Collection (GC)

| Method | Mechanism | Weakness |
|---|---|---|
| Reference counting | Reclaim immediately when the reference count hits 0 (Python's main mechanism) | Can't reclaim **cyclic references** (needs separate detection) |
| Mark & sweep | Mark everything reachable from the roots (stack, globals) → reclaim the unmarked | Pause time (stop-the-world) |
| **Generational GC** | Based on the empirical rule that "**most objects die young**," frequently does small collections of just the young generation (battle-hardened in the JVM and V8) | Tuning runs deep |

---

## ⚔️ Quests

### Quest 1: The Forge Connoisseur (30 XP)

1. Whether `1 - 2 - 3` becomes `(1-2)-3` or `1-(2-3)` is determined by what property of the grammar?
2. Syntax errors and type errors — at which stage of the pipeline is each detected? Write one example error of each.
3. Explain "why LLVM IR exists" in terms of the m languages × n architectures multiplication.

<details>
<summary>📜 Answer</summary>

1. Associativity. With left recursion like `Expr → Expr '-' Term` (or a left fold in a loop), it's left-associative.
2. Syntax error (② parser): `let x = ;`. Type error (③ semantic analysis): `"abc" * true`.
3. Without an IR you'd need m × n compilers. Insert a shared IR and you need only m frontends + n backends.
</details>

### Quest 2: 💻 The Grand Implementation Quest — "Give Birth to Your Own Language" (120 XP)

**Write a calculator-language interpreter from full scratch.** This is the capstone project of this world.

Spec:
- The four arithmetic operations, parentheses, unary minus, integers and decimals
- Variables (`x = 3 + 4` assigns, then `x * 2` references)
- Stages: ① lexer (string → token stream) ② recursive descent parser (token stream → AST) ③ evaluator (recursively evaluate the AST)
- `1 + 2 * 3` should give 7, and `(1 + 2) * 3` should give 9 (precedence emerging from the grammar)
- If you have the energy: adding a `print` statement, comparison operators, and `if`/`while` turns it into **a real programming language**

<details>
<summary>📜 Design hints</summary>

The AST is a class (or algebraic data type): `Num(value)`, `BinOp(left, op, right)`, `Var(name)`, `Assign(name, expr)`.
The evaluator is a single recursion `def eval(node, env)`. `env` is a dictionary mapping variable names → values (World 2's hash table).
</details>

### Quest 3: Catechism of the GC (30 XP)

1. Draw a diagram showing an example where reference counting can't reclaim a cyclic reference.
2. "Most objects die young" — give two concrete examples from your own code.
3. Even in a GC language, memory leaks happen. When?

<details>
<summary>📜 Answer</summary>

1. A → B and B → A referencing each other. Even with nothing pointing at them from outside, each one's count stays at 1.
2. Temporary strings inside a loop, intermediate lists created in a function but not returned, temporary objects during request handling, and so on.
3. When you keep holding "reachable but never used again" references (a global cache, forgetting to deregister a listener, etc.). GC only looks at reachability.
</details>

---

## 👹 Boss Battle: The Forge Master "Compiler Dragon" (150 XP)

Close your notes and challenge it. 70%+ to win.

1. List the 6 stages of the compiler pipeline in order, and state the input and output of each.
2. Why can lexical analysis be written with regular expressions (DFAs), while parsing needs a CFG? (Hint: matching parentheses)
3. Draw the AST of `2 + 3 * (4 - 1)` under the calculator grammar above.
4. Give one example of an optimization that static typing makes possible.
5. Explain the mechanism by which register allocation reduces to graph coloring.
6. What are the "roots" in mark & sweep GC? State the two phases of the algorithm.
7. When adding `if` to your calculator language, list all the stages that need to change.

<details>
<summary>📜 Skeleton of the answer</summary>

1. Lexical analysis (string → tokens), parsing (tokens → AST), semantic analysis (AST → checked AST), IR generation, optimization (IR → IR), code generation (IR → machine code).
2. The shape of tokens is a regular language decidable with finitely many states. But "matching parentheses" requires counting nesting of arbitrary depth, which is impossible with finite states (proven by World 13's pumping lemma). A CFG can handle nesting with a stack (recursion).
3. Root (+), left 2, right (*), whose left is 3 and right is (−) with 4 and 1.
4. With types fixed you can eliminate dynamic type-tag checks and dispatch, fix field offsets, emit numeric operations directly as machine instructions, etc.
5. Make each variable a vertex and join variables whose live ranges overlap (are live at the same time) with an edge. Allocating to k registers = k-coloring the interference graph. Vertices that can't be colored spill to memory.
6. Roots = "references the program holds directly," such as local variables on the stack, global variables, and registers. The mark phase marks every object reachable from the roots; the sweep phase frees the unmarked ones.
7. lexer (token for the `if` keyword), parser (add a grammar rule and an AST node), evaluator (evaluate the If node). And semantic analysis too, if you have type checking — in other words, the entire frontend.
</details>

---

🏆 **Victory reward**: Badge "🐉 Language Smith" + 150 XP (one who has finished the grand implementation quest is no longer merely "a user of languages")

➡️ Next: [World 13: The Oracle of Computation (Theory of Computation)](world-13-computation-theory.md)

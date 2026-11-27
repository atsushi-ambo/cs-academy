# SQL injection: break it, then fix it

## Why

A host search should store and look up names with normal punctuation.
A query made by string joining lets the input change where SQL sees a quoted value.

## Boundary

```text
fixed SQL with ? ---> SQLite statement
              name -> bound value slot
```

SQLite receives the command and the search value separately.

## Example

Bind the text O'Neil in a one-item tuple. SQLite compares the full string, including the quote.
If the client chooses a sort order, map it to a fixed clause.

## Common mistakes

- Manual escaping depends on context. Bind values instead.
- Binding a column name gives a value, even in an ORDER BY.
- A bound LIKE pattern still uses pattern rules.

## At work

Use a DB role with only the permissions its service needs.
Check team filters as well as query binding, especially on read-only routes.

## Summary

Bind data, choose dynamic syntax from fixed options, and limit database permissions.

## Model answer

A bound name is passed as a value, so a quote stays inside the name. For sorting, I map the requested choice to a fixed column name. The client never supplies SQL syntax.

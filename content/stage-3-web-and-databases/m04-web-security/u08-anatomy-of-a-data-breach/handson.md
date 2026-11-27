# Hands-on in the Python sandbox

Use the unit’s Python editor with the sample below. Use only the supplied toy data.

## Flag a risk in a fictitious config

Change patched to False. The audit should report one issue.

Completed sample

```python
config = {"patched": False}
issues = []
if not config["patched"]:
    issues.append("dependency")
print(len(issues))
```

Expected output line

```text
1
```

Run the final Code tests. Check the allowed case and the rejected case.

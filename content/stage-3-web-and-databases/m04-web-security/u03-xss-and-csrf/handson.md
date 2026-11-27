# Hands-on in the Python sandbox

Use the unit’s Python editor with the sample below. Use only the supplied toy data.

## Keep angle brackets in the label

Set label to <b>ready</b>. Keep html.escape in the print call.

Completed sample

```python
from html import escape

label = "<b>ready</b>"
print(escape(label))
```

Expected output line

```text
&lt;b&gt;ready&lt;/b&gt;
```

Run the final Code tests. Check the allowed case and the rejected case.

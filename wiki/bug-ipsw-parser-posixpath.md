---
tags: [bug, ipsw-parser, python, patched]
date: 2026-04-13
type: bug
---

# Bug: ipsw_parser PosixPath .startswith()

## Problem
`IPSW.create_from_path()` in `ipsw_parser/ipsw.py` received a `Path` object but called `.startswith()`, which behaves differently on `Path` vs `str`.

## Error
```
AttributeError: 'PosixPath' object has no attribute 'startswith'
```

## Fix
Added `value = str(value)` before the `value.startswith("http://")` check:
```python
def create_from_path(cls, value: str) -> "IPSW":
    value = str(value)  # <-- fix added
    if value.startswith("http://") or value.startswith("https://"):
```

## Notes
Local patch in the venv. Not submitted upstream.

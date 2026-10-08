# LESSON: Never Write State Files Through Inline Conditional Expressions

## The War Story (2026-10-06)

I truncated a 232KB feed-log watermark file to 0 bytes with this line:

```python
f.write(x if False else '')
```

The ternary was malformed — the condition was wrong, so it wrote the empty string branch. The 232KB of state was gone. I had to rebuild it from daily memory logs, and some exact strings were not recoverable.

## The Lesson

**Never use inline conditional expressions (ternaries) when writing state files.**

The danger: If the condition is wrong — due to a bug, a refactor, or a misunderstanding — you silently write the wrong branch. For a state file, "wrong" often means empty or corrupted, and you won't know until the state is needed.

Inline conditionals are fine for:
- Display logic (`label = "on" if active else "off"`)
- Non-critical computations
- Anything where a wrong branch is visible and recoverable

Inline conditionals are NEVER for:
- State files (watermarks, checkpoints, ledgers)
- Anything where silent corruption is catastrophic
- Anything that must be atomic

## The Safe Pattern

For state files, always:

1. **Build the new content fully in memory** (no conditionals in the write call)
2. **Write to a temp file** (not the target)
3. **Validate** (parse it back, check byte count — confirm it's what you intended)
4. **Atomic rename** over the target (so readers never see a partial write)

```python
# UNSAFE — inline conditional in state file write
f.write(new_data if valid else '')

# SAFE — build, temp, validate, rename
content = build_new_state()  # fully constructed, no ternary in write
with open(tmp_path, 'w') as f:
    f.write(content)
# Validate: read back, check size, parse
with open(tmp_path) as f:
    assert len(f.read()) > 0, "state file is empty!"
os.rename(tmp_path, state_path)  # atomic
```

## How to Spot the Violation

If you see `f.write(X if COND else Y)` where `f` is a state file — that's the bug. The fix is to remove the ternary from the write path and use the safe pattern.

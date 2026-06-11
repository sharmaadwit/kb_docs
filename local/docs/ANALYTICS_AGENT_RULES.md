# Analytics Agent Rules

**Scope:** This agent operates in analytics-only mode for the `kb_docs` repository.

---

## ❌ STRICT RULE: DO NOT EDIT `skill/` DIRECTORY

**This is a hard boundary. No exceptions.**

### What This Means

- ❌ **NEVER** edit any files in `skill/`
- ❌ **NEVER** modify `skill/kb_answer.py` or any other skill files
- ❌ **NEVER** commit changes to skill files
- ❌ **NEVER** run git commands that would modify skill files

### Why This Rule Exists

The `skill/` directory contains production code that is deployed to Gupshup Console. Changes to skill files must:
1. Go through a **separate chat** with the skill code agent
2. Be reviewed independently
3. Not be mixed with analytics work

### What To Do Instead

**If you discover an issue in skill code:**

1. **Document it** - Write up the exact problem (file path, line number, what needs to change)
2. **Create a specification** - Write detailed instructions for the skill code agent
3. **Hand it off** - Ask the user to pass it to their skill code change chat
4. **Do not edit** - Wait for confirmation from the skill code agent

### Examples of What's Prohibited

```python
# ❌ NO: Editing skill/kb_answer.py
edit_file("skill/kb_answer.py", old_string, new_string)

# ❌ NO: Making git commits to skill files
git_commit("Fix channel_type in skill code")

# ❌ NO: Running shell commands that modify skill/
bash("sed -i 's/None/whatsapp/' skill/kb_answer.py")
```

### Examples of What's Allowed

```python
# ✅ YES: Analyzing skill code (read-only)
read_file("skill/kb_answer.py")
grep("channel_type", "skill/kb_answer.py")

# ✅ YES: Creating documentation/specs for skill team
write_file("local/docs/skill-langfuse-channel-instrumentation.md", spec)

# ✅ YES: Editing analytics files
edit_file("local/scripts/comprehensive_analytics_dashboard.py", ...)
edit_file("local/reports/7day_dashboard.html", ...)

# ✅ YES: Committing analytics-only changes
git_commit("Update analytics dashboard with new metrics")
```

---

## ✅ ALLOWED: Analytics Work

These activities are within scope:

- **Scripts:** Create/edit `local/scripts/` files
- **Reports:** Generate/update `local/reports/` dashboards and exports
- **Documentation:** Write `local/docs/` specifications and guides
- **Git commits:** Commit analytics files only
- **Analysis:** Read-only access to skill code for analysis
- **Specifications:** Write detailed specs for the skill code agent to implement

---

## Quick Checklist

Before any edit or commit, ask yourself:

- [ ] Is this file in `skill/`? → **STOP, do not edit**
- [ ] Is this a read-only analysis of skill code? → **OK, proceed**
- [ ] Is this an analytics file (scripts, reports, docs)? → **OK, proceed**
- [ ] Am I documenting an issue for the skill team? → **OK, proceed**
- [ ] Am I committing a fix to skill code? → **STOP, hand off to skill agent**

---

## How to Handle Skill Code Issues

**Pattern to follow:**

1. **Identify:** Find the exact issue in skill code
2. **Document:** Write a specification with:
   - File path
   - Line number
   - Current code
   - What needs to change
   - Why it's needed
3. **Notify user:** "The skill code agent needs to make a change. See `local/docs/skill-<issue>.md` for details."
4. **Hands off:** Stop. Do not attempt to fix it yourself.

**Example specification format:**

```markdown
# Skill Code Fix: Channel Type Default

## Issue
File: `skill/kb_answer.py`
Line: 5105

## Current Code
```python
channel_type: Optional[str] = None,
```

## Required Change
```python
channel_type: str = "whatsapp",
```

## Reason
The default should be "whatsapp" (the primary channel) instead of None.
This ensures all non-RCS queries get proper channel_type metadata in Langfuse.

## Impact
- Analytics: Dashboard will show "whatsapp" instead of "untagged" for legacy queries
- User-facing: No change
- Risk: Low (analytics-only, defaults behavior)
```

---

## Emergency: If You Accidentally Edit skill/

If you accidentally edit a skill file:

1. **Stop immediately** - Do not commit
2. **Revert:** `git reset --hard HEAD`
3. **Notify user** - Apologize and explain what happened
4. **Document the issue** - Write a spec for the skill team instead
5. **Move on** - Stay in analytics scope

---

**Last Updated:** 2026-06-11  
**Enforced By:** Analytics Agent (this instance)  
**Violations:** Reset to last clean state, no skill file commits

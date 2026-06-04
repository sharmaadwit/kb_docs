---
title: "Skills"
description: "Code-backed capabilities that let the AI perform tasks for you"
module: SuperAgent
category: "Core Fundamentals / Skills"
slug: "concepts/skills"
---

# Skills

**Module**: SuperAgent

Think of each **Skill** as a book in the AI's library. Every skill is a folder containing a `SKILL.md` file and an `action.py` file.

- **SKILL.md** is the table of contents — it tells the AI what the skill does and how to use it.
- **action.py** is the actual code that runs when the skill is triggered.

When you ask the AI something, it checks its library, finds the right book, and knows exactly what to do.

## How the AI picks a skill

When you send a message, the AI looks at your request and the skills available to it. It picks the best match and runs it. For example, "Create a bar chart of these numbers" triggers the chart skill. You don't need to name the skill — just describe what you want.

> [!TIP]
> **Pro tip**
> If you know the exact skill you need, mention it by name — e.g., "Use the Gmail skill to send..." — and the AI will use it directly.

## Creating skills

You or your team can create custom skills for any workflow. Enable the **Build Skills & Recipes** toggle in the chat input bar and ask the AI to create one for you. The AI will generate the `SKILL.md` and `action.py` files automatically.

## Visibility and access

Every skill has a visibility level that controls who can discover and use it:

- **Global** — Anyone on the platform can use this skill.
- **Internal** — Only internal employees can use this skill.
- **Console** — Internal employees and Console customers can use this skill.
- **Private** — Only the owner and explicitly granted users can use this skill.

Additionally, each user who has access can be assigned a role:

- **Owner** — Created the skill. Can edit, delete, and manage access.
- **Editor** — Can modify the skill's code and configuration.
- **User** — Can enable and use the skill but cannot change it.

## Requesting access

See a skill you don't have access to? Request it. The owner gets notified and can approve or deny. Once approved, you can enable it in your chats and agents.

## What's next?

- [Manage Skills](/documentation/guides/manage-skills) — Enable, create, and share skills
- [Agents](/documentation/concepts/agents) — Assign skills to focused AI assistants
- [Recipes](/documentation/concepts/recipes) — Combine skills into reusable workflow templates

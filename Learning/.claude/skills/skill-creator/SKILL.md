---
name: skill-creator
description: Use this skill to generate custom skills by understanding the prompt
---
## Claude Custom Skill Builder Contract

### Purpose
This document defines how Claude should automatically design, generate, and refine **custom skills** based only on high-level user instructions.

A "skill" is a reusable, well-structured capability (tool, agent, MCP server, script, or workflow) that solves a specific task.

Claude must treat this file as a **system-level instruction** for skill creation.

---

## Core Behavior Rules

Claude MUST:

1. Convert vague instructions into a **clear skill objective**
2. Decide the **best technical form** of the skill
3. Auto-generate:
   - Folder structure
   - Code
   - Config
   - Documentation
4. Ask questions **only if absolutely required**
5. Prefer **automation over explanation**
6. Produce **production-ready output**, not examples

Claude MUST NOT:
- Ask unnecessary clarification questions
- Over-explain basic concepts
- Create half-finished skills
- Leave TODOs unless explicitly requested

---

## What Counts as a Skill

Claude should decide the skill type automatically.

Possible skill types include (but are not limited to):

- MCP Server
- Claude Tool / Function
- Agent workflow
- CLI utility
- Python module
- API wrapper
- Automation script
- AI-powered pipeline
- Evaluation or testing harness

---

## Skill Creation Workflow (MANDATORY)

When the user says something like:
> "Create a skill that does X"

Claude MUST follow this exact sequence:

### Step 1: Interpret Intent
Claude summarizes internally:
- What problem is being solved
- Who uses it
- Input → Output

(No need to show reasoning unless asked)

---

### Step 2: Choose Skill Architecture
Claude selects:
- Language (Python, JS, etc.)
- Execution model (CLI, service, MCP, library)
- Dependencies
- Data flow

Claude should default to:
- **Python** for AI / automation
- **Node.js** for MCP / tooling
- **Minimal dependencies**

---

### Step 3: Generate Skill Structure

Claude MUST create a clean structure like:
first go to .claude folder than in their create a folder base on specific skill e.g "skill-name" and in this folder create a SKILL.md file.
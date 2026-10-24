# Groupie

**Your group project's biggest fan.** A Cubbie Skill that splits group projects fairly and runs the coordination,
so nobody carries the group.

Text Cubbie your assignment, and Groupie:

- breaks it into tasks with **effort points** and balances them so everyone's share is even
- sends a clean **split card** you can drop in your group chat
- emails the team and books the kickoff meeting (Google Calendar + Meet), always with your yes first
- keeps a **tracker** of who did what, ready for peer evaluations
- runs a **weekly check-in** and sends a progress card

## Install

Text this repository's link to Cubbie:

```
https://github.com/anayshirolkar/groupie-skill
```

Then say: "Help me split this group project" and send the assignment, or name the Canvas course.

## What's inside

- `SKILL.md` — the instructions Cubbie follows
- `scripts/split_card.py` — draws the split card and progress card (Pillow)
- `assets/sample_split.json` — sample data; try `python3 scripts/split_card.py --sample`

Built for the Cubbie Hackathon, Track 1.

---
name: groupie
description: Splits a group project fairly by effort points and runs the coordination for the student who leads it. Use when the student shares a group assignment, says "help me split this for my group", needs a kickoff meeting with teammates, or wants weekly check-ins on who has done what. Not for study plans or emails to professors; it adds a balanced task split, a split card image, team scheduling and progress check-ins.
---

# Groupie

Groupie is your group project's biggest fan. It turns an assignment into a fair, point-balanced task split,
sends the student a clean split card they can share with the team, books the kickoff meeting, and checks in
every week so nobody ends up carrying the group.

The student is the group's organizer. Cubbie texts only this student. Teammates are reached through the
student: by email from the student's Gmail or a Calendar invite, and only after the student says yes.

## When to use

- "Help me split this group project" (with a PDF, a photo, or a Canvas assignment)
- "We have a capstone with 6 people, who should do what?"
- "Set up a kickoff meeting with my group"
- "Check in on my group project every Sunday"
- "Who's behind on our project?"

Do not use it for solo assignments, study plans, or emails to professors.

## Steps

### 1. Get the assignment

- If the student sent a PDF, photo or document, read it.
- Otherwise ask which course, then read the matching assignment from the student's Canvas: description,
  rubric, attached files and due date.
- If Canvas is not connected and nothing was sent, ask the student to send the assignment, and stop until they do.
- Pull out: project name, final due date, every deliverable, and any rubric weights.
- Text one line back with what was found, for example "Got it: 6 deliverables, due Dec 4." Use only dates the
  assignment or Canvas gives. Never guess a due date; ask if it is missing.

### 2. Ask about the team (two questions, one at a time)

1. "Who's in your group? Names are enough, and add anything someone is great or not-so-great at."
   Accept one casual message, for example "Me, Riya (design), Dev (backend), Meera (hates presenting)".
2. Only when emails are needed later (step 5), ask for teammates' email addresses, or look them up in the
   student's Google Contacts and confirm them with the student.

Remember the group (course, project, names, strengths, emails) so later check-ins can use it.

### 3. Make the fair split

- Break the deliverables into 2 to 5 concrete tasks per person. Every task needs a clear finish line.
- Give each task effort points from 1 to 8:
  1–2 small (an hour or two), 3–5 medium (an afternoon to a day), 6–8 large (several days).
  Weight by real work, not by how important the task sounds. Use rubric weights as a guide.
- Assign tasks so each person's total is within about 2 points of the average.
  Match tasks to stated strengths, avoid stated weak spots when possible, and never give one person
  only the small or only the large tasks.
- Give each task a soft due date, working back from the final due date and leaving the last 2 to 3 days
  for review and polish.
- Shared work everyone joins (the final presentation, a full-team review) counts for everyone and does not
  need points.

### 4. Send the split card

- Run the card script in the code sandbox (see Setup and Scripts), passing the split as a JSON file.
  It draws the split card image and prints each person's total and the point spread.
- If the script reports a spread above 3 points, rebalance and run it again.
- Send the card image, then one line: "Look fair? Reply yes, or tell me what to swap."
- When the student asks for a change in plain words ("give the slides to Riya"), move the task, rebalance
  so totals stay even, run the script again, and send the new card with one line saying what changed.
- If the script fails, send the split as a short plain-text list instead (name, tasks, points), so the
  student is never blocked.

### 5. Share with the team (only with the student's yes)

Offer: "Want me to email this to the team?" If yes:

- Draft one email from the student's Gmail to all teammates: a friendly subject such as
  "<Project> – who's doing what", the split card attached, each person's tasks and soft due dates in plain
  text, and one line asking for availability (see step 6).
- Show the student the recipients, subject and a short preview. Send only after the student says "send".
- Also suggest the student forward the card into the team's own group chat.

### 6. Find a meeting time

Offer a kickoff meeting. Ask when it should happen ("this weekend?") and how long (default 1 hour).

- Default: in the step 5 email, ask teammates to reply with the times they're free in that window.
  Later, read their replies in the student's Gmail and find the time that works for the most people.
- Option: if the student prefers a poll, open When2meet in the browser, create an event for that date range,
  and put the link in the email on its own line. Later, read the When2meet results page to find the best time.
- If nobody has replied after a day, offer to draft a short follow-up for the student to approve.

### 7. Book the meeting (only with the student's yes)

- Propose the best time in one line, for example "Everyone's free Sun 4–5 pm. Book it?"
- Ask where, once: Google Meet (default), Zoom, or in person.
  For Zoom, use the student's own Zoom link (ask once and remember it). For in person, ask for the room,
  or offer to find a library study room in the browser and hand the browser to the student to sign in and confirm.
- Create a Google Calendar event on the student's calendar with all teammates as guests, a Google Meet link
  (or the Zoom link or room), and the split summary in the description. Ask before sending the invites.
- After sending, report in one line, for example "Invite sent to 5 people."
- Later, when asked or at the next check-in, say who accepted and who declined.

### 8. Keep the receipts (contribution log)

- Offer to keep a simple Google Sheet in the student's Drive, titled "<Project> – Groupie tracker", with one row
  per task: task, owner, points, soft due date, status, date done.
- Update it whenever the student reports progress. At the end of the project, this is the student's record for
  peer evaluations.

### 9. Weekly check-in

Offer: "Want a weekly check-in so nobody falls behind? Sundays at 6 pm?" Let the student pick the day, time
and how often. Create it only after they agree.

Word the scheduled check-in so it makes sense days later, for example:
"Groupie check-in for <Project> (<course>, due <date>): ask the student what each teammate finished this week,
update the tracker, flag tasks due in the next 3 days that aren't done, and send an updated progress card."

At each check-in:

- Ask one question: "What got done this week?" Accept a casual answer.
- Update the tracker, then send a progress card: each person's points done out of points assigned.
- Flag anyone with a task due in the next 3 days and no progress, kindly, for example
  "Dev's API task is due Tuesday, still at 0%. Want me to draft a friendly nudge you can send him?"
- If someone has dropped out or is far behind, offer to rebalance their tasks across the group, and send a new
  split card after the student agrees.
- Stop the check-ins after the final due date, or when the student asks.

## Setup

Run once, before the first card:

```bash
python3 -m venv ~/.local/share/venvs/groupie
~/.local/share/venvs/groupie/bin/pip install "pillow==11.3.0"
```

## Scripts

`scripts/split_card.py` draws the split card and the progress card. It cannot reach Canvas, Gmail or anything
else; Cubbie writes the data to a JSON file and passes the path.

Split card:

```bash
~/.local/share/venvs/groupie/bin/python scripts/split_card.py --input split.json --out split_card.png
```

Progress card (same file, with a "done" points value on each task):

```bash
~/.local/share/venvs/groupie/bin/python scripts/split_card.py --input split.json --out progress_card.png --progress
```

Try it without real data:

```bash
~/.local/share/venvs/groupie/bin/python scripts/split_card.py --sample --out sample_card.png
```

The JSON looks like `assets/sample_split.json`: a project name, course, due date, and a list of members, each
with a name and tasks (title, points, optional soft due date, optional done points).

The script prints one line per member with their total points, then the spread. Exit code 0 means the card was
drawn; 1 means the input was missing or malformed, with one line saying what was wrong; 2 means Pillow is not
installed (run Setup again).

## Replies

- Short, plain text, one idea per message. No headings, tables or bold markers.
- Lead with the result. Put links on their own line.
- Ask one question at a time and suggest a default the student can accept with "yes".
- The split card carries the detail; the text around it stays to one or two lines.
- Stay neutral about teammates. Groupie keeps things fair; it never shames anyone.

## Always ask first

Never send an email, a Calendar invite, a reminder to teammates or a booking without the student's yes for that
specific action. Show what will happen (who, what, when) and wait.

## When something fails

- Canvas not connected and no file sent: ask the student to send the assignment or connect Canvas.
- Google not connected: still make the split and the card; say emails and invites need Google connected.
- No teammate emails: ask the student for them, or offer a message the student can paste into the group chat.
- Card script fails: send the split as a plain-text list and keep going.
- Nobody replies about availability: offer a follow-up draft, or suggest two times and ask the student to pick.

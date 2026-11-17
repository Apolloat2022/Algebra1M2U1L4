"""Teacher script for Tue Nov 17, Topic 1 Test Review day (test Wed Nov 18).
Students take the Test Review on EDIA (the Topic 1 Review, Q1-15), then the teacher walks through the questions most of the
class missed. Includes the answer key and a worked walkthrough for every question, so any item can be the one that's missed.
Run:  python make_m3t1_review_day_script.py [password]
  ->  Module 3 topic 1/LESSON PLANS/M3T1-Tue-11-17-Review-Script-ANSWER-KEY.pdf  (answer-key password; or lock with lock_keys.py)"""
import sys
from pathlib import Path

import make_m3t1_review as RV
import make_m3t1_walkthroughs as W   # REVIEW walkthroughs, card(), pdf()
from make_m3t1_l2_script import say, ask, board, part, tip, CSS

RV.KEY = True
OUT = Path(__file__).parent / "Module 3 topic 1" / "LESSON PLANS" / "M3T1-Tue-11-17-Review-Script-ANSWER-KEY.pdf"

# question -> (skill, lesson it comes from)
SKILL = ["Equation from a word problem", "No solution (distribute both sides)", "Inequality with a negative x-term",
         "Decimals, x on both sides", "One, none or infinite?", "Fixed cost + changing cost", "Standard form → y = mx + b",
         "Solve a formula for h", "Inequality + number line", "Point-slope → y = mx + b", "Equal areas",
         "Pick the no-solution equation", "Flip the sign", "Solve P = 2ℓ + 2w for w", "“At most” word problem"]
LESSON = [3, 1, 3, 1, 1, 3, 2, 2, 3, 2, 1, 1, 3, 2, 3]


def answer(n, q):  # printed letter for multiple choice, same order as the review PDF and EDIA
    if q["kind"] != "mc":
        return q["ans"]
    return f'{("ABCD" if n % 2 else "FGHJ")[min(q["pos"], len(q["choices"]) - 1)]}. {q["choices"][0]}'


def html():
    qs = RV.items()
    assert len(qs) == len(SKILL) == len(LESSON) == len(W.REVIEW) == 15
    td = lambda *c: "<tr>" + "".join(f"<td>{x}</td>" for x in c) + "</tr>"
    tally = ("<table class=kt><tr><th>Q</th><th>Skill</th><th>Lesson</th><th>EDIA % correct</th><th>Walk it?</th></tr>"
             + "".join(td(n, SKILL[n - 1], LESSON[n - 1], "", "") for n in range(1, 16)) + "</table>")
    key = ("<table class=kt><tr><th>Q</th><th>Answer</th><th>Q</th><th>Answer</th></tr>"
           + "".join(td(n, answer(n, qs[n - 1]), n + 8 if n + 8 <= 15 else "", answer(n + 8, qs[n + 7]) if n + 8 <= 15 else "")
                     for n in range(1, 9)) + "</table>")
    plan = [
        part("0–3", "Walk in · agenda slide up (daily plan deck, Tue 11/17)",
             say("Today is test review day. The test is tomorrow. You'll take the Test Review on EDIA first, then we'll go over "
                 "the questions most of you missed. Show your work on paper. I want to see how you got each answer.")),
        part("3–30", "Test Review on EDIA (Questions 1–15)",
             say("Questions 1 to 11 are just like tomorrow's test, in the same order. 12 to 15 are extra practice. "
                 "Work alone and quietly, like a real test. When you finish, check your work. Don't start talking."),
             board("IEP and 504: their own EDIA version (tips + steps · one question per screen · read aloud on request)."),
             tip("students racing. Walk the room and look at the paper, not the screen. No work shown → “Show me how you got it.”")),
        part("30–33", "Find the most-missed questions",
             say("Pencils down. Let's look at how the class did."),
             board("EDIA → Test Review → item analysis → sort by % correct (lowest first).",
                   "Write the % in the tally table below. Walk through anything under <b>70%</b>, lowest first. "
                   "Plan on 3–4 questions (about 5 minutes each)."),
             tip("putting student names on screen. Show the question and the class %, never who missed it.")),
        part("33–53", "Walk through the most-missed questions (same routine for each)",
             board("1. Put the question on the screen. “Cover your answer.”",
                   "2. <b>Spot it</b>: read the 🔍 line from its card below. What kind of problem is this?",
                   "3. <b>ASK</b> the first step. Whiteboards up, then do it on the board together.",
                   "4. Finish with the ⚡ steps. Students copy the steps on their paper.",
                   "5. <b>Check</b> it (✔ line): put the answer back in.",
                   "6. <b>Trap</b> (⚠ line): “If you got this wrong answer, here's what happened.”"),
             ask("Thumbs: do you know what went wrong on yours?", "Thumbs down → that student goes to Look → Watch → Ask during fix-it time."),
             tip("more than one rule per question. Name the one move (the 7 moves are at the top of the cards).")),
        part("53–58", "Fix it",
             say("On your paper, make a fix-it list. For every question you missed: the number, what went wrong, and the right answer. "
                 "Then try it again. Missed one we didn't go over? Look, Watch, Ask: reread it, watch that lesson's video, ask a partner, then me. "
                 "Goal: 80% or higher.")),
        part("58–60", "Wrap up",
             say("Tonight: redo only the questions you missed on EDIA and bring your fix-it list. Tomorrow is the test: "
                 "charged Chromebook and a pencil. Remember the flip rule, and get one side of the equation to match before you compare."),
             board("Note who is still below 70% for a test-day reminder card and Thursday's retake group.")),
    ]
    cards = "".join(W.card(n if n <= 11 else f"{n} (extra practice)", q["q"], answer(n, q), *W.REVIEW[n - 1],
                           RV.numline(-10, 2, -6, True, True) if n == 9 else "") for n, q in enumerate(qs, 1))
    moves = "".join(f"<li><b>{a}.</b> {b}</li>" for a, b in W.MOVES)
    css = CSS + (  # script styles + tables + the walkthrough cards' styles
        ".kt{width:100%;border-collapse:collapse;margin:6px 0 12px}.kt td,.kt th{border:1px solid #bcc8d6;padding:3px 7px;text-align:left}"
        ".kt th{background:#e8eef5}.brk{break-before:page}" + W.CSS[W.CSS.index(".moves"):].replace(".lb{display", ".item .lb{width:auto;color:#111;background:none;text-align:left;display") + ".moves h2{background:none;padding:0}")
    return (f'<!doctype html><html><head><meta charset="utf-8"><title>M3T1 Review Day Script</title><style>{css}</style></head><body>'
            '<h1>Module 3 Topic 1 · Tue Nov 17 · Test Review Day Script + Answer Key</h1>'
            '<p class="sub">Algebra I · Mr. Pandey · Test Wed Nov 18 · Retakes Thu Nov 19 · The Test Review on EDIA is the Topic 1 Review '
            '(REVIEW/T1-Review.pdf): Q1–11 mirror the test, Q12–15 are extra practice. '
            '<b>SAY</b> = read to class · <b>ASK</b> = question with the answer to listen for · blue boxes = board / screen.</p>'
            f'<h2 class=first>Plan (60 minutes)</h2>{"".join(plan)}'
            f'<h2>Answer key</h2>{key}<h2 class=first>Tally: most-missed questions</h2>{tally}'
            f'<h2>Walkthrough cards · every question</h2><div class="moves"><h2 class=first>The 7 moves for all of Topic 1</h2><ol>{moves}</ol></div>'
            f'{cards}</body></html>')


if __name__ == "__main__":
    W.pdf(html(), OUT, sys.argv[1] if len(sys.argv) > 1 else None)

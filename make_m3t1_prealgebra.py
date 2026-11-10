"""Pre-algebra plan for M3T1, Tue Nov 10 - Tue Nov 17, built from the M2T2 test results.
Daily 60 min: 0-10 bell work + side-board practice (3 levels), 10-15 pre-algebra mini-lesson, 15-60 Tier 1 Bluebonnet (compressed).
One data set -> two PDFs in Module 3 topic 1/LESSON PLANS/:
  M3T1-PreAlgebra-Teacher-Plan.pdf   (answers, scripts, Tier 1 pacing; password-protected)
  M3T1-PreAlgebra-Board-Work.pdf     (student pages to project or print; no answers)
Run:  python make_m3t1_prealgebra.py <password>"""
import sys
from pathlib import Path

from make_m3t1_l2_script import say, ask, board, prob, part, tip, CSS
import make_m3t1_walkthroughs as W   # pdf(): print + optional encrypt
import make_m3t1_review as RV

RV.KEY = True
nl = RV.numline  # (lo, hi, mark, shade left?, open circle?)
DIR = Path(__file__).parent / "Module 3 topic 1" / "LESSON PLANS"

# Each day: bell (q, a) pairs, boards = [(level title, [(q, a)])], mini = teacher script parts, tier1 = 45-min block.
DAYS = [
    dict(
        date="Tuesday, Nov 10", tier="Lesson 2 · finish Activity 2.1 (rewriting forms of a line)",
        skill="Distribute (watch the negative) and divide EVERY term",
        why="M2T2 items 1 and 9 (slope with negatives) and Lesson 2: 3x − 2y = 8 and 8x − 2y = 12 need you to divide every term by a negative.",
        bell=[("−3 − (−8)", "5"), ("y = −2x + 5. Find y when x = −3.", "y = −2(−3) + 5 = 6 + 5 = 11")],
        boards=[("Level 1 · Integers", [("−6 + 10", "4"), ("4 − 9", "−5"), ("−7 − (−3)", "−4"), ("(−5)(−4)", "20"), ("−18 ÷ 3", "−6")]),
                ("Level 2 · Distribute", [("3(x − 4)", "3x − 12"), ("−2(x + 5)", "−2x − 10"), ("−4(x − 3)", "−4x + 12"), ("½(6x − 10)", "3x − 5")]),
                ("Level 3 · Divide every term", [("(6x + 12) ÷ 3", "2x + 4"), ("(−10x + 20) ÷ (−5)", "2x − 4"),
                                                 ("(−6x − 9) ÷ (−3)", "2x + 3"), ("−4y = 8x − 12. Get y alone.", "y = −2x + 3")])],
        mini=[say("Two moves you need in the next 45 minutes. <b>Move 1: the number outside the parentheses multiplies EVERY term inside, sign included.</b>"),
              board("−3(x − 4) = −3·x + (−3)(−4) = <b>−3x + 12</b> &nbsp;(negative × negative = positive)"),
              say("<b>Move 2: when you divide, divide EVERY term, sign included.</b>"),
              board("(−8x + 12) ÷ (−2) → −8x ÷ −2 = 4x, &nbsp;12 ÷ −2 = −6 → <b>4x − 6</b>"),
              ask("We do: −5(x − 2)", "−5x + 10"), ask("We do: −3y = 9x − 6. Get y alone.", "divide every term by −3: y = −3x + 2"),
              say("Yesterday's Q3, 3x − 2y = 8, is exactly this: subtract 3x, then divide every term by −2.")],
        tier1=[part("15–20", "Re-do Activity 2.1 Q3 together (where we stopped)",
                    board("3x − 2y = 8 → −2y = −3x + 8 → divide every term by −2 → <b>y = (3/2)x − 4</b>",
                          "slope 3/2 · y-intercept (0, −4) · x-intercept: y = 0 → 3x = 8 → (8/3, 0)"),
                    say("Point at the mini-lesson board: this is Move 2.")),
               part("20–25", "✪ Q4 and Q6–Q7 · Name the forms (quick)",
                    board("y = mx + b → slope-intercept · y − y₁ = m(x − x₁) → point-slope · Ax + By = C → standard",
                          "Slope or y-intercept fastest from slope-intercept · a point from point-slope · calculators need y = …")),
               part("25–37", "✪ Q8–Q9 · Rewrite (I do Q8a, we do Q8b, you do Q9b)",
                    prob("Q8a · y − 2 = 5(x − 7)", board("y − 2 = 5x − 35 (Move 1) → <b>y = 5x − 33</b>")),
                    prob("Q8b · 8x − 2y = 12", board("−2y = −8x + 12 → ÷(−2) every term (Move 2) → <b>y = 4x − 6</b>")),
                    prob("Q9b · y = −4x + 3 → standard", board("<b>4x + y = 3</b> (add 4x)")),
                    tip("students who divide only the x-term by −2. Ask: \"Did EVERY term get divided?\"")),
               part("37–41", "Test move (like End of Topic Q7 and Q10)",
                    board("4x + 3y = 12 → 3y = −4x + 12 → <b>y = −(4/3)x + 4</b>", "y + 4 = 3(x − 2) → y + 4 = 3x − 6 → <b>y = 3x − 10</b>")),
               part("41–45", "Exit ticket",
                    board("1. 6x + 3y = 12 → <b>y = −2x + 4</b>", "2. y − 4 = 3(x + 2) → <b>y = 3x + 10</b>"),
                    say("Homework: Practice 1a–d, SE p. 369. Skipped today: Q5 (general case), Q9a and Q10; Q10 is a review-day stretch."))]),
    dict(
        date="Wednesday, Nov 11", tier="Lesson 2 · Activities 2.2–2.3 and Talk the Talk (solving formulas for a letter)",
        skill="Undo in reverse order (shoes off before socks) and multiply by the reciprocal",
        why="M2T2 items 7, 8 and 9 (find b with a point) and Lesson 2: C = 5/9(F − 32) is solved by undoing in reverse.",
        bell=[("8x − 4y = 20. Get y alone.", "−4y = −8x + 20 → y = 2x − 5"), ("5 − (−2)", "7")],
        boards=[("Level 1 · Two-step equations", [("2x + 5 = 17", "x = 6"), ("3x − 7 = 14", "x = 7"), ("x/4 + 2 = 5", "x = 12"), ("−2x + 3 = 11", "x = −4")]),
                ("Level 2 · Fractions: multiply by the flip", [("(2/3)x = 8", "x = 8 · 3/2 = 12"), ("(3/4)x = −9", "x = −9 · 4/3 = −12"),
                                                              ("−(1/2)x = 6", "x = 6 · (−2) = −12"), ("(5/9)x = 10", "x = 10 · 9/5 = 18")]),
                ("Level 3 · Find b", [("y = 2x + b goes through (3, 10)", "10 = 6 + b → b = 4"), ("y = −3x + b goes through (2, 1)", "1 = −6 + b → b = 7"),
                                      ("y = ½x + b goes through (−4, 5)", "5 = −2 + b → b = 7"), ("Solve y = mx + b for b", "b = y − mx")])],
        mini=[say("You put on socks, then shoes. To take them off you go backwards: shoes first. <b>Equations work the same way.</b>"),
              board("3x − 7: first ×3, then −7 &nbsp;→ undo backwards: <b>+7 first, then ÷3</b>",
                    "2x + 6 = 20 → 2x = 14 → <b>x = 7</b>"),
              say("A fraction in front of x? Multiply by its flip (reciprocal). (2/3) · (3/2) = 1."),
              ask("We do: (2/3)x − 1 = 7", "add 1: (2/3)x = 8 → multiply by 3/2 → x = 12"),
              say("Today's formula C = 5/9(F − 32): F had −32 done first, then ×5/9. Undo backwards: ×9/5, then +32.")],
        tier1=[part("15–18", "Literal equation: what it is",
                    say("A <b>literal equation</b> is a formula you can solve for any one of its letters. Letters you are not solving for act like numbers.")),
               part("18–28", "✪ Activity 2.2 Q1–Q2 · Temperature",
                    prob("Q1 · Solve C = 5/9(F − 32) for F", board("× 9/5: (9/5)C = F − 32 → +32: <b>F = (9/5)C + 32</b>")),
                    prob("Q2 · 77°F or 30°C?", board("F = (9/5)(30) + 32 = 54 + 32 = 86°F &gt; 77°F → <b>30°C is warmer</b>"))),
               part("28–31", "✪ Q3b · Ethan's error only", board("He wrote C = (5/9)F − 32: he did <b>not</b> multiply the 32 by 5/9.")),
               part("31–40", "✪ Activity 2.3 Q1 and Q3",
                    prob("Q1 · V = Bh", board("÷B → <b>h = V/B</b>; V = 450, B = 75 → <b>h = 6 in</b>")),
                    prob("Q3 · A = ½h(b₁ + b₂)", board("×2: 2A = h(b₁ + b₂) → ÷(b₁ + b₂): <b>h = 2A/(b₁ + b₂)</b>; A = 24, b₁ = 9, b₂ = 7 → h = 48/16 = <b>3 cm</b>")),
                    tip("students who \"move\" a letter. Make them say what they did to BOTH sides.")),
               part("40–45", "Exit ticket · Talk the Talk Q1–Q2 (use 3.14 for π)",
                    board("S = 2πrh for h → <b>h = S/(2πr)</b>", "S = 37.68, r = 1.5 → 2(3.14)(1.5) = 9.42 → h = 37.68/9.42 = <b>4 in</b>",
                          "Test move: V = ℓwh → <b>w = V/(ℓh)</b>"),
                    say("Homework: Practice 2–3, SE p. 370. Skipped: Q3a, Q3c, Q4, Activity 2.3 Q2 and Q4, Talk the Talk Q3–Q4."))]),
    dict(
        date="Thursday, Nov 12", tier="Lesson 3 · Getting Started, Activity 3.1, start of 3.2 (inequalities from a graph)",
        skill="Number lines: compare negatives, read the four symbols, open vs closed",
        why="Lesson 3 is all number lines. Students who can't put −8 and −5 in order can't shade an inequality.",
        bell=[("V = ℓwh. Solve for h.", "h = V/(ℓw)"), ("Which is greater, −7 or −2?", "−2 (it is farther right)")],
        boards=[("Level 1 · &lt; or &gt;", [("−3 __ 2", "&lt;"), ("−8 __ −5", "&lt;"), ("−1 __ −10", "&gt;"), ("0 __ −4", "&gt;")]),
                ("Level 2 · Words to symbols", [("at least 5", "x ≥ 5"), ("no more than 12", "x ≤ 12"), ("more than −2", "x &gt; −2"), ("under 30", "x &lt; 30")]),
                ("Level 3 · Is it a solution?", [("x + 4 &gt; 1 · try x = −3", "1 &gt; 1 is false → No"), ("x + 4 &gt; 1 · try x = 0", "4 &gt; 1 → Yes"),
                                                ("2x − 1 ≤ 5 · try x = 3", "5 ≤ 5 → Yes (≤ includes =)"), ("2x − 1 ≤ 5 · try x = 4", "7 ≤ 5 is false → No")])],
        mini=[say("On a number line, <b>left is less</b>. −8 is farther left than −5, so −8 &lt; −5."),
              board("○ open circle: &lt; or &gt; (the number is NOT included) · ● closed circle: ≤ or ≥ (it IS included)",
                    "−3 ≤ x means the same as x ≥ −3: read it starting from the x."),
              say("I do: x &gt; −2: open circle at −2, shade right."), nl(-6, 4, -2, False, True),
              say("I do: x ≤ 1: closed circle at 1, shade left."), nl(-4, 6, 1, True, False),
              ask("We do: x ≥ −4", "closed circle at −4, shade right"), nl(-8, 2, -4, False, False)],
        tier1=[part("15–22", "✪ Getting Started · Fundraising function",
                    board("$25 credit + $3.75 per box → <b>f(b) = 3.75b + 25</b>", "slope 3.75 = dollars per box · y-intercept (0, 25) = the credit")),
               part("22–33", "✪ Activity 3.1 Q1–Q4 · Read it off the graph",
                    prob("Q1 · Exactly $1600", board("3.75b + 25 = 1600 → 3.75b = 1575 → <b>b = 420</b>")),
                    prob("Q2 · $1600 or less", board("<b>b ≤ 420</b>: closed circle, shade left")),
                    prob("Q3 · More than $1600", board("<b>b &gt; 420</b>: open circle, shade right")),
                    prob("Q4 · Open vs closed", board("Point back at the mini-lesson board."))),
               part("33–40", "✪ Activity 3.2 Q1 · Solve like an equation, then round",
                    board("3.75b + 25 ≥ 1100 → 3.75b ≥ 1075 → b ≥ 286.66… → <b>at least 287 boxes</b> (round up)"),
                    tip("rounding the wrong way. \"At least\" rounds up; \"at most\" rounds down. Plug it back in.")),
               part("40–45", "Exit ticket",
                    board("1. $40 + $12 per hour → <b>y = 12x + 40</b>", "2. At most $1150: 3.75b + 25 ≤ 1150 → <b>b ≤ 300</b>, closed circle, shade left"),
                    say("Homework: Practice 1a–d, SE p. 383. Skipped: Q5b–c, 3.2 Q2–Q3."))]),
    dict(
        date="Monday, Nov 16", tier="Lesson 3 · Activities 3.3–3.4 (the flip, variables on both sides, distributing)",
        skill="Multiplying and dividing by a negative, and why it flips the order",
        why="Lesson 3's one new rule (flip the sign) only makes sense if students trust −2 &gt; −5.",
        bell=[("3.75b + 25 ≥ 400", "3.75b ≥ 375 → b ≥ 100"), ("(−6)(−2) and −15 ÷ (−3)", "12 and 5")],
        boards=[("Level 1 · Signs", [("−4 · 3", "−12"), ("−20 ÷ (−4)", "5"), ("18 ÷ (−6)", "−3"), ("(−1)(−9)", "9")]),
                ("Level 2 · One step with negatives", [("−3x = 12", "x = −4"), ("−5x = −35", "x = 7"), ("x/(−2) = 6", "x = −12"), ("−x = 8", "x = −8")]),
                ("Level 3 · Does the sign flip?", [("3 &lt; 7 · multiply both by −2", "−6 &gt; −14 · flips"), ("−4 &lt; 8 · divide both by −4", "1 &gt; −2 · flips"),
                                                  ("10 &gt; 5 · multiply both by −1", "−10 &lt; −5 · flips"), ("2 &lt; 6 · add −3 to both", "−1 &lt; 3 · no flip")])],
        mini=[say("2 &lt; 5. Multiply both by −1: −2 and −5. On the number line −2 is to the RIGHT of −5, so <b>−2 &gt; −5</b>. The order turned around."),
              board("<b>Rule: multiply or divide both sides by a NEGATIVE → flip the sign.</b> Adding or subtracting never flips."),
              board("I do: −2x &lt; 10 → ÷(−2), flip → <b>x &gt; −5</b>"),
              ask("We do: −3x ≥ 12", "÷(−3), flip → x ≤ −4")],
        tier1=[part("15–22", "✪ Activity 3.3 Q1–Q2 · The hike",
                    board("Starts 4800 ft, drops 20 ft per minute → <b>h(m) = −20m + 4800</b>", "slope −20 · y-intercept (0, 4800) · sea level when m = 240")),
               part("22–30", "✪ Q3–Q4, Q6 · Below 3200 ft",
                    board("−20m + 4800 &lt; 3200 → −20m &lt; −1600 → ÷(−20), flip → <b>m &gt; 80</b>", "Graph agrees: below 3200 ft to the right of 80 minutes."),
                    say("That's the mini-lesson rule, now in a real problem.")),
               part("30–38", "✪ Activity 3.4 Q1a and Q3a",
                    prob("Q1a · 5x + 2 ≥ 3x − 10", board("Move the smaller x-term (3x): 2x + 2 ≥ −10 → 2x ≥ −12 → <b>x ≥ −6</b> (no flip needed)")),
                    prob("Q3a · −4(x − 6) &lt; 22", board("−4x + 24 &lt; 22 → −4x &lt; −2 → ÷(−4), flip → <b>x &gt; ½</b>"))),
               part("38–45", "Exit ticket (like End of Topic Q3 and Q9)",
                    board("1. −3x + 4 ≥ 19 → −3x ≥ 15 → <b>x ≤ −5</b> (flip)", "2. 2.5p − 4 &gt; −1.5(p + 8) → 2.5p − 4 &gt; −1.5p − 12 → 4p &gt; −8 → <b>p &gt; −2</b>"),
                    nl(-6, 4, -2, False, True),
                    say("Homework: Practice 3a–d, SE p. 385. Skipped: Q5, Q1b, Q3b, Talk the Talk (use it in tomorrow's review)."))]),
    dict(
        date="Tuesday, Nov 17", tier="Topic 1 review (test tomorrow)",
        skill="Slope from two points with negatives (subtract in the same order)",
        why="The two weakest M2T2 skills (items 1, 6, 9) for any M2T2 retake, and the same integer moves the Topic 1 test needs.",
        bell=[("−2(x − 3)", "−2x + 6"), ("5 − 3x &gt; 11", "−3x &gt; 6 → x &lt; −2 (flip)")],
        boards=[("Level 1 · Slope", [("(1, 2) and (3, 8)", "6/2 = 3"), ("(−2, 5) and (2, −3)", "−8/4 = −2"), ("(−3, 1) and (3, −3)", "−4/6 = −2/3"), ("(0, −3) and (5, −3)", "0/5 = 0")]),
                ("Level 2 · Parallel and perpendicular slopes", [("parallel to y = 4x − 1", "4"), ("perpendicular to y = 2x + 3", "−½"),
                                                                 ("perpendicular to y = −(3/5)x + 1", "5/3"), ("perpendicular to y = x", "−1")]),
                ("Level 3 · Substitute, then plot", [("g(x) = 2x for x = −1, 0, 1, 2", "−2, 0, 2, 4"), ("h(x) = −x + 3 for x = −2, 0, 3", "5, 3, 0"),
                                                     ("Plot both. Which is steeper?", "g(x), slope 2 vs −1")])],
        mini=[board("slope = (y₂ − y₁) ÷ (x₂ − x₁) &nbsp;· same order top and bottom · minus a negative = plus"),
              board("I do: (−3, 4) and (1, −4) → (−4 − 4) ÷ (1 − (−3)) = −8 ÷ 4 = <b>−2</b>"),
              ask("We do: (−2, −1) and (2, 7)", "(7 − (−1)) ÷ (2 − (−2)) = 8 ÷ 4 = 2"),
              say("Perpendicular: flip the fraction and change the sign. 2 → −½.")],
        tier1=[part("15–45", "Topic 1 review",
                    say("Use the Topic 1 review (15 items) and the How to Solve walkthrough already linked on the End of Topic 1 card. "
                        "Start with Lesson 2–3 items: those are the newest and least practiced."),
                    tip("students who stop when they divide by a negative. Point at Monday's rule box."))]),
]

STUDENT_CSS = """@page{size:letter landscape;margin:.45in}body{font:17pt/1.35 'Segoe UI',Arial,sans-serif;color:#111}
section{break-after:page}h1{font-size:22pt;margin:0 0 4px;color:#1d3557}.sk{font-size:14pt;color:#444;margin:0 0 10px}
.cols{display:flex;gap:16px}.box{flex:1;border:2px solid #457b9d;border-radius:8px;padding:6px 12px}h2{font-size:16pt;margin:2px 0 6px;color:#457b9d}
ol{margin:0;padding-left:26px}li{margin:6px 0}"""


def teacher_day(d):
    bell = board(*[f"Bell {i}. {q} → <b>{a}</b>" for i, (q, a) in enumerate(d["bell"], 1)])
    levels = "".join(prob(t, board(*[f"{chr(97 + i)}. {q} → <b>{a}</b>" for i, (q, a) in enumerate(qs)])) for t, qs in d["boards"])
    return (f'<h2>{d["date"]} · Tier 1: {d["tier"]}</h2>'
            f'<p class="sub"><b>Pre-algebra skill:</b> {d["skill"]}. <b>Why:</b> {d["why"]}</p>'
            + part("0–10", "Bell work at desks (3 min), then side boards (7 min)", bell,
                   say("Everyone starts at Level 1. Students who passed M2T2 (10+) start at Level 2. Level 3 leads straight into today's lesson."), levels)
            + part("10–15", f"Pre-algebra mini-lesson · {d['skill']}", *d["mini"])
            + "".join(d["tier1"]))


def student_day(d):
    bell = "".join(f"<li>{q}</li>" for q, _ in d["bell"])
    levels = "".join(f'<div class="box"><h2>{t}</h2><ol type="a">{"".join(f"<li>{q}</li>" for q, _ in qs)}</ol></div>' for t, qs in d["boards"])
    return (f'<section><h1>{d["date"]} · Bell work and side boards</h1><p class="sk">Today\'s skill: {d["skill"]}</p>'
            f'<div class="box" style="margin-bottom:12px"><h2>Bell work (at your desk)</h2><ol>{bell}</ol></div><div class="cols">{levels}</div></section>')


def overview():
    rows = "".join(f"<tr><td>{d['date']}</td><td>{d['skill']}</td><td>{d['tier']}</td></tr>" for d in DAYS)
    return ('<h1>M3T1 · Pre-Algebra + Tier 1 Plan · Nov 10–17</h1>'
            '<p class="sub">Algebra I · Mr. Pandey · built from the M2T2 results · test date fixed: Wed Nov 18 · '
            '<b>SAY</b> = read to class · <b>ASK</b> = question with the answer to listen for · blue boxes = board work, fully solved.</p>'
            '<h3>What the M2T2 scores say</h3>'
            '<p>All periods together: about 1 in 3 students scored 6 or less out of 13. Group 3 is the most urgent (20 of 44 at 6 or less, average 6.9).</p>'
            + board("Weakest items (share correct): 6 · f(bx) graph 32% · 9 · point-slope 42% · 5 · shift a table 47% · 7 · perpendicular 48% · 1 · slope 52% · 8 · parallel 54%",
                    "Strongest: 2 · domain and range 87% · 10 · key attributes 73%",
                    "Same gaps under all of them: <b>subtracting negatives, fractions and reciprocals, substituting, solving for one letter</b>. Lesson 2 needs the exact same moves, "
                    "which is why most students were lost by Activity 2.1 Q3.")
            + '<h3>Every day</h3>'
            + board("0–10 · Bell work (2 at desks) → side boards: Level 1 everyone · Level 2 if 10+ on M2T2 · Level 3 bridges into today's lesson",
                    "10–15 · Pre-algebra mini-lesson: one skill, I do, we do, then link to the lesson",
                    "15–60 · Tier 1 Bluebonnet, starred (✪) problems only, compressed to 45 minutes")
            + f'<h3>The week</h3><table border="1" cellpadding="4" style="border-collapse:collapse;font-size:10pt"><tr><th>Day</th><th>Pre-algebra</th><th>Tier 1</th></tr>{rows}</table>'
            + '<p class="sub">Lesson 3 goes from 3 days to 2 (Thu + Mon). What each day skips is listed in its exit-ticket box. '
              'The student pages (Board Work PDF) have the same problems with no answers, one page per day, to project or print.</p>')


def check():
    """The arithmetic behind the answers."""
    assert -3 - (-8) == 5 and -2 * -3 + 5 == 11 and -7 - (-3) == -4 and (-5) * (-4) == 20
    assert all(2 * x + 5 == 17 for x in [6]) and 3 * 7 - 7 == 14 and 12 / 4 + 2 == 5 and -2 * -4 + 3 == 11
    assert 2 / 3 * 12 == 8 and 3 / 4 * -12 == -9 and -0.5 * -12 == 6 and abs(5 / 9 * 18 - 10) < 1e-9
    assert 6 + 4 == 10 and -6 + 7 == 1 and 0.5 * -4 + 7 == 5 and (2 / 3) * 12 - 1 == 7
    assert 3.75 * 100 + 25 == 400 and -3 * -4 == 12 and -5 * 7 == -35 and -12 / -2 == 6
    assert (8 - 2) / (3 - 1) == 3 and (-3 - 5) / (2 + 2) == -2 and (-3 - 1) / (3 + 3) == -2 / 3 and (-4 - 4) / (1 + 3) == -2 and (7 + 1) / (2 + 2) == 2
    assert -3 * -5 + 4 == 19 and 2.5 * -2 - 4 == -1.5 * (-2 + 8) and -4 * (0.5 - 6) == 22 and -20 * 80 + 4800 == 3200
    assert 3.75 * 286 + 25 < 1100 <= 3.75 * 287 + 25 and 3.75 * 300 + 25 == 1150 and 9 / 5 * 30 + 32 == 86
    assert abs(37.68 / (2 * 3.14 * 1.5) - 4) < 1e-9 and 48 / 16 == 3 and 450 / 75 == 6


if __name__ == "__main__":
    check()
    T = f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{overview()}{"".join(teacher_day(d) for d in DAYS)}</body></html>'
    S = f'<!doctype html><html><head><meta charset="utf-8"><style>{STUDENT_CSS}</style></head><body>{"".join(student_day(d) for d in DAYS)}</body></html>'
    W.pdf(T, DIR / "M3T1-PreAlgebra-Teacher-Plan.pdf", sys.argv[1])
    W.pdf(S, DIR / "M3T1-PreAlgebra-Board-Work.pdf")

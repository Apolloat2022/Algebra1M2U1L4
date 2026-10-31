"""Module 3 Topic 1 lesson plans, Mon 11/9 - Thu 11/19 (district calendar, AHS row).
Same one-page layout as T1-Lesson-Plan-Thu-11-05.html. Stars = 150-day pacing guide p. 3.
Run: python make_m3t1_plans.py   -> HTML + PDF in "Module 3 topic 1/LESSON PLANS"."""
import subprocess
from pathlib import Path

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
OUT = Path(__file__).parent / "Module 3 topic 1" / "LESSON PLANS"
A = lambda s: f'<span class="ans">{s}</span>'
CSS = """@page{size:letter;margin:.35in}
body{font-family:Segoe UI,Arial,sans-serif;font-size:9.3pt;color:#111;margin:0}
h1{font-size:17pt;margin:0;color:#0b6b3a}.sub{color:#444;margin:2px 0 10px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:8px 18px}
h2{font-size:11.5pt;margin:8px 0 3px;color:#0b6b3a;border-bottom:1px solid #cfe3d6}
ul{margin:0;padding-left:16px}li{margin:1px 0}
table{width:100%;border-collapse:collapse;margin-top:4px}
th,td{border:1px solid #bbb;padding:3px 5px;vertical-align:top;text-align:left}
th{background:#e8f3ec}td:first-child{white-space:nowrap;width:42px}
.ans{color:#b00000}.note{font-size:9pt;color:#444;margin-top:8px}"""
IEP = "IEP/504: read aloud on request, properties/notes card, extra time."

L2 = "Lesson 2: Literal Equations"
L3 = "Lesson 3: Modeling Linear Inequalities"
DAYS = [
 dict(file="Mon-11-09", date="Monday, November 9", lesson=L2 + " (Day 1 of 2)",
  obj=["Find the slope, x-intercept, and y-intercept from slope-intercept, point-slope, and standard form.",
       "Pick the most efficient form for each feature.",
       "Rewrite linear equations from one form to another."],
  teks=["<b>A.3A</b> slope from an equation in y = mx + b, Ax + By = C, y − y₁ = m(x − x₁)", "A.2B write linear equations in different forms",
        "A.12E literal equations", "Process: A.1D"],
  terms="slope-intercept form · point-slope form · standard form",
  mat=["Student Edition pp. 357–361 (Getting Started, Activity 2.1)", "Lesson 1 homework (SE pp. 355–356) to check",
       "Anchor chart: Key Characteristics of Linear Functions (slope, x-int, y-int)", "Whiteboards; exit ticket half sheets"],
  bell=[("2(x + 3) = x − 4", "x = −10"), ("3x + 1 = 3x − 5: one, none, or infinite?", "no solution"),
        ("Slope of y = −2x + 7", "−2"), ("y-intercept of y = −2x + 7", "(0, 7)")],
  rows=[("0–5", "Bell work", "Q1–2 review Lesson 1; Q3–4 preview today."),
   ("5–10", "Homework check", "Lesson 1 Assignment Practice 2: a " + A("none") + ", b " + A("x = 7") + ", d " + A("infinite") + ", f " + A("infinite") + ". Collect questions for later."),
   ("10–25", "✪ Getting Started: Perimeter Perspectives · SE p. 358",
    "Read the park scenario. Pairs write each perimeter equation: Juan " + A("w = P/2 − ℓ") + ", Mia " + A("ℓ = P/2 − w") +
    ". Q2: multiply each by 2 to get back to " + A("2ℓ + 2w = P") + ".<br><b>Say:</b> same formula, solved for the variable each person needs."),
   ("25–50", "✪ Activity 2.1: Equations in Different Forms · SE pp. 359–361",
    "Q1 y = −⅔x + 4: " + A("slope −⅔, (0, 4), (6, 0)") + ". Q2 y = 4(x − 2): " + A("slope 4, (0, −8), (2, 0)") +
    ". Q3 3x − 2y = 8: " + A("slope 3/2, (0, −4), (8/3, 0)") + ".<br>Explicit teach the three forms (Q4). Q5 Ax + By = C: " +
    A("slope −A/B, x-int (C/A, 0), y-int (0, C/B)") + ". Q6: slope → slope-intercept or point-slope; a point → point-slope; y-int → slope-intercept.<br>"
    "Pairs Q8: y − 2 = 5(x − 7) " + A("y = 5x − 33") + "; 8x − 2y = 12 " + A("y = 4x − 6") +
    ". Q9: y + 7 = 0.5(x − 1) " + A("x − 2y = 15") + "; y = −4x + 3 " + A("4x + y = 3") + ". Q10 if time."),
   ("50–58", "Exit ticket", "1. Write 6x − 3y = 9 in slope-intercept form; give slope and both intercepts. " +
    A("y = 2x − 3; slope 2; (0, −3); (3/2, 0)") + "<br>2. Write y − 1 = 3(x + 2) in slope-intercept form. " + A("y = 3x + 7") + "<br>" + IEP),
   ("58–60", "Wrap up", "Homework: Lesson 2 Assignment Practice 1a–d (SE p. 369). Tomorrow: literal equations (formulas).")],
  cfu=["Whiteboards: \"Which form shows the y-intercept fastest?\" " + A("slope-intercept"),
       "Thumbs: \"Standard form can have A = ½.\" " + A("Down: A, B, C are integers"), "Activity 2.1 Q4–6 are the TE's check points."],
  after=["Missed exit Q1 → Skills Practice Set A (standard → slope-intercept).", "Missed exit Q2 → Skills Practice Set B (point-slope →).",
         "Both correct → Skills Practice Set C."],
  note="All of Day 1 is starred. TE pacing is 2 days, and the district calendar matches (11/9–11/10)."),

 dict(file="Tue-11-10", date="Tuesday, November 10", lesson=L2 + " (Day 2 of 2)",
  obj=["Define literal equation.", "Solve formulas for a specified variable and justify the steps.",
       "Use a rewritten formula to find an unknown measure."],
  teks=["<b>A.12E</b> solve formulas and other literal equations for a specified variable", "A.3A, A.2B", "Process: A.1A"],
  terms="literal equation",
  mat=["Student Edition pp. 362–367 (Activities 2.2, 2.3, Talk the Talk)", "Calculators (3.14 for π)", "Whiteboards"],
  bell=[("Write 4x + 2y = 10 in slope-intercept form", "y = −2x + 5"), ("3x − 7 = 11", "x = 6"),
        ("P = 2ℓ + 2w. Find ℓ when P = 30, w = 5", "ℓ = 10"), ("C = 5/9(F − 32). Find C when F = 50", "C = 10")],
  rows=[("0–5", "Bell work", "Q3–4 lead into today: we keep solving the same formula for different letters."),
   ("5–25", "✪ Activity 2.2: Rewriting Literal Equations · SE pp. 362–364",
    "Define <i>literal equation</i>. Q1 solve C = 5/9(F − 32) for F: " + A("F = 9/5 C + 32") + ". Q2 77°F vs 30°C: " +
    A("Mateo is warmer: 30°C = 86°F") + ".<br>Q3 error analysis: Ethan " + A("didn't distribute 5/9 to the 32") + "; Minh " +
    A("multiplied by 9 wrong (45F, 1440)") + ". Worked Example (clear fractions), then Q4: " + A("9C − 5F = −160") + "."),
   ("25–45", "✪ Activity 2.3: Solving Literal Equations for Specific Variables · SE pp. 365–366",
    "Q1 V = Bh → " + A("h = V/B") + "; V = 450, B = 75 → " + A("6 in.") + " Q2 cone V = ⅓πr²h → " + A("h = 3V/(πr²)") +
    ".<br>Q3 trapezoid A = ½h(b₁ + b₂) → " + A("h = 2A/(b₁ + b₂)") + "; A = 24, bases 9 and 7 → " + A("3 cm") +
    ".<br>Q4 Z = A/B + C/D for A: " + A("A = BZ − BC/D") + " (part b, solve for D, is the challenge)."),
   ("45–57", "✪ Talk the Talk: Rearrange It · SE p. 367 (exit ticket)",
    "Independent. 1. S = 2πrh for h " + A("h = S/(2πr)") + " 2. S = 37.68, r = 1.5 " + A("h = 4 in.") +
    "<br>3. S = 2πr² + 2πrh for h " + A("h = (S − 2πr²)/(2πr)") + " 4. S = 51.81, r = 1.5 " + A("h = 4 in.") + "<br>" + IEP),
   ("57–60", "Wrap up", "Essential Question (SE p. 357). Homework: Lesson 2 Assignment Practice 2–3 and Prepare (SE p. 370). Prepare previews inequalities.")],
  cfu=["Whiteboards: \"Solve A = ℓw for w.\" " + A("w = A/ℓ"), "Thumbs: \"To get F alone, subtract 32 first.\" " + A("Down: multiply by 9/5 first"),
       "Activity 2.3 Q1–4 are the TE's check points."],
  after=["Missed Talk the Talk 1 or 3 → Skills Practice Set D (literal equations).", "Missed 2 or 4 only → calculator/substitution check, small group.",
         "Prepare answers: x = 5, x > 7, x ≤ −3, x < −4."],
  note="All of Day 2 is starred. Prepare Q4 (−x > 4 → x < −4) sets up flipping the sign in Lesson 3."),

 dict(file="Wed-11-11", date="Wednesday, November 11", lesson=L3 + " (Day 1 of 3)",
  obj=["Write and analyze a linear function from a context (rate of change, y-intercept).", "Use a graph to solve inequalities.",
       "Graph solution sets on a number line with open or closed circles."],
  teks=["<b>A.2C</b> write linear equations from a context", "<b>A.5B</b> solve linear inequalities in one variable", "Process: A.1A, A.1D"],
  terms="linear inequality",
  mat=["Student Edition pp. 371–375 (Getting Started, Activity 3.1)", "Inequality-words chart (at least ≥, at most ≤, more than >, fewer than <)",
       "Rulers for the horizontal-line method", "Whiteboards"],
  bell=[("\"at least\" means which symbol?", "≥"), ("\"no more than\" means which symbol?", "≤"),
        ("\"fewer than\" means which symbol?", "<"), ("Solve 3.75b + 25 = 400", "b = 100")],
  rows=[("0–5", "Bell work", "Build the inequality-words chart on the board from Q1–3 (TE EB tip). Leave it up for all of Lesson 3."),
   ("5–20", "✪ Getting Started: Fundraising Function · SE p. 372",
    "Elijah: $25 credit + $3.75 per box. Q1 " + A("f(b) = 3.75b + 25") + ". Q2 independent " + A("boxes sold") + ", dependent " + A("total sales ($)") +
    "; slope " + A("3.75, dollars per box") + "; y-intercept " + A("25, the starting credit") + "."),
   ("20–45", "✪ Activity 3.1: Modeling Linear Inequalities · SE pp. 373–375",
    "Q1 goal $1600: horizontal line → " + A("420 boxes") + ". Define <i>linear inequality</i>.<br>Q2 below the line: " + A("f(b) ≤ 1600, b ≤ 420, closed circle") +
    "; only whole numbers of boxes make sense. Q3 above: " + A("b > 420, open circle") + ". Q4 open = not included, closed = included.<br>Q5 at least $925 " +
    A("b ≥ 240") + "; less than $2050 " + A("b < 540") + "; exactly $700 " + A("b = 180") + "."),
   ("45–55", "Exit ticket", "f(b) = 3.75b + 25. Write an inequality and graph it on a number line.<br>1. sales of at most $1150 " +
    A("b ≤ 300, closed circle, shade left") + " 2. sales of more than $475 " + A("b > 120, open circle, shade right") + "<br>" + IEP),
   ("55–60", "Wrap up", "Homework: Lesson 3 Assignment Practice 1a–d (SE p. 383). Tomorrow: solve inequalities with algebra.")],
  cfu=["Whiteboards: \"Open or closed for x < 3?\" " + A("open"), "Point to the graph: \"Where is f(b) > 1600?\" " + A("above the line"),
       "Activity 3.1 Q1–5 are the TE's check points."],
  after=["Missed circles/shading → Skills Practice Set B (number lines).", "Missed writing the inequality → Skills Practice Set A.",
         "Re-teach the words chart at tomorrow's bell work."],
  note="Getting Started and 3.1 are starred. TE pacing is 3 days (11/11, 11/12, 11/16), matching the district calendar."),

 dict(file="Thu-11-12", date="Thursday, November 12", lesson=L3 + " (Day 2 of 3)",
  obj=["Solve two-step linear inequalities algebraically.", "Round answers sensibly in context (whole boxes).",
       "Explain why dividing by a negative reverses the inequality sign."],
  teks=["<b>A.5B</b> solve linear inequalities in one variable", "<b>A.2C</b>", "Process: A.1A"],
  terms="solve an inequality",
  mat=["Student Edition pp. 376–379 (Activities 3.2, 3.3)", "Inequality-words chart from Wednesday", "Whiteboards"],
  bell=[("2x + 5 = 17", "x = 6"), ("Graph x ≥ 2 on a number line", "closed circle at 2, shade right"),
        ("Open or closed for x < 3?", "open"), ("Is x = −5 a solution of −x > 4?", "yes, 5 > 4")],
  rows=[("0–5", "Bell work", "Q4 previews today: the sign flips when the x has a negative coefficient."),
   ("5–25", "✪ Activity 3.2: Solving Two-Step Linear Inequalities · SE pp. 376–377",
    "Define <i>solve an inequality</i>. Worked Example: 3.75b + 25 ≥ 1100 → b ≥ 286.6… → Q1 " + A("at least 287 boxes") +
    ".<br>Q2a still under $600: " + A("b < 153.3…, at most 153 boxes") + ". Q2b at least $1500: " + A("b ≥ 393.3…, at least 394 boxes") +
    ".<br>Q3: same steps as an equation, whatever the form."),
   ("25–50", "✪ Activity 3.3: Reversing Inequality Signs · SE pp. 378–379",
    "Hike from 4800 ft down 20 ft/min: Q1 " + A("h(m) = −20m + 4800") + ". Q2 slope " + A("−20") + ", y-int " + A("4800") + ", x-int " + A("240 min") +
    ", domain " + A("0 ≤ m ≤ 240") + ".<br>Q3 graph: below 3200 ft → " + A("m > 80") + ". Q4 algebra: −20m + 4800 < 3200 → −20m < −1600 → " +
    A("m > 80 (flip!)") + ".<br>Q6 table: every row's sign reverses. <b>Board rule:</b> multiply or divide by a negative → flip the sign."),
   ("50–58", "Exit ticket", "1. −3x + 4 ≥ 19 " + A("x ≤ −5") + " 2. 5 − 2x < 11 " + A("x > −3") +
    "<br>3. Tire at 26 psi loses 0.1 psi/min; stay at or above 22 psi: " + A("26 − 0.1t ≥ 22 → t ≤ 40 min") + "<br>" + IEP),
   ("58–60", "Wrap up", "Homework: Lesson 3 Assignment Practice 1e–g and 2a–b (SE pp. 384–385).")],
  cfu=["Whiteboards: \"−2x < 8. Answer?\" " + A("x > −4"), "Thumbs: \"Subtracting a negative flips the sign.\" " + A("Down: only × or ÷ by a negative"),
       "Activity 3.3 Q1–7 are the TE's check points."],
  after=["Forgot to flip (exit Q1–2) → Skills Practice Set C.", "Missed context Q3 → pair with a partner on Monday's bell work.",
         "All correct → Skills Practice Set D."],
  note="3.2 and 3.3 are starred. Rounding in context: \"at least\" rounds up (287), \"at most\" rounds down (153)."),

 dict(file="Mon-11-16", date="Monday, November 16", lesson=L3 + " (Day 3 of 3)",
  obj=["Solve inequalities with variables on both sides.", "Solve inequalities that need the distributive property.",
       "Graph each solution set on a number line."],
  teks=["<b>A.5B</b> solve linear inequalities, including distributive property and variables on both sides", "Process: A.1F"],
  terms="(review) linear inequality · solve an inequality",
  mat=["Student Edition pp. 380–382 (Activity 3.4, Talk the Talk)", "Topic 1 Self-Reflection SE pp. 387–388 (for homework)", "Whiteboards"],
  bell=[("−4x > 12", "x < −3"), ("2x + 3 ≤ x − 1", "x ≤ −4"), ("Is −6 ≤ x the same as x ≥ −6?", "yes"), ("3(x − 2) = 9", "x = 5")],
  rows=[("0–5", "Bell work", "Q3 sets up Kai's answer in 3.4."),
   ("5–30", "✪ Activity 3.4: Solving Other Linear Inequalities · SE pp. 380–381",
    "5x + 2 ≥ 3x − 10: Victoria moves x left → " + A("x ≥ −6") + "; Kai moves x right, divides by −2 → " + A("−6 ≤ x, same answer") +
    ". Q2: same as equations, but watch the sign.<br>−4(x − 6) < 22: Aaliyah distributes first, Ava divides by −4 first → both " +
    A("x > ½") + ". Q4: distributing works the same way."),
   ("30–50", "✪ Talk the Talk: It's About Solutions, More or Less · SE p. 382",
    "Solve and graph: a −⅔x ≥ 7 " + A("x ≤ −21/2") + " b 32 > 23 − x " + A("x > −9") + " c 15 − 4x ≤ 3x − 6 " + A("x ≥ 3") +
    " d 2(x + 6) < 14 + 4x " + A("x > −1") + "<br>Q2 if A < B: A + C < B + C " + A("always") + "; AC > BC " + A("only when C < 0") +
    "; −A < −B " + A("never") + "."),
   ("50–58", "Exit ticket", "1. −2(x + 1) ≥ 8 " + A("x ≤ −5") + " 2. 4x − 3 < 6x + 5 " + A("x > −4") + " (graph both)<br>" + IEP),
   ("58–60", "Wrap up", "Essential Question (SE p. 371). Homework: Lesson 3 Assignment Practice 3a–d (SE p. 385) + Topic 1 Self-Reflection. Review tomorrow, test Wed 11/18.")],
  cfu=["Whiteboards: \"Which side do you put the x on to avoid flipping?\" " + A("the side with the bigger coefficient"),
       "Thumbs: \"2(x + 6) < 14 + 4x: the sign flips.\" " + A("Down if you keep x on the right"), "Activity 3.4 Q1–4 are the TE's check points."],
  after=["Use exit tickets + Self-Reflection to group students for Tuesday's review.", "Practice 3 answers: x > −1, x < 7, d ≤ 11, k ≤ −24.",
         "Missed both exit items → Skills Practice Set D."],
  note="3.4 and Talk the Talk are starred. That finishes Lesson 3."),

 dict(file="Tue-11-17", date="Tuesday, November 17", lesson="Topic 1 Review",
  obj=["Solve linear equations and classify one / no / infinite solutions.", "Rewrite linear equations and solve literal equations.",
       "Solve and graph linear inequalities, including context problems."],
  teks=["<b>A.5A</b>, <b>A.5B</b>, <b>A.2C</b>, <b>A.3A</b>, A.2B, A.12E"],
  terms="solution · no solution · infinite solutions · literal equation · linear inequality",
  mat=["Review problems below (project or copy)", "Topic 1 Summary SE pp. 389–390", "Students' Self-Reflections (SE pp. 387–388)", "Whiteboards"],
  bell=[("Self-Reflection: rate yourself 1–4 on Lessons 1, 2, 3", "use to seat review groups"), ("5x − 2 = 5x + 7", "no solution"),
        ("Solve A = ℓw for ℓ", "ℓ = A/w"), ("−x ≥ 3", "x ≤ −3")],
  rows=[("0–5", "Bell work", "Collect ratings; seat 1–2s near you."),
   ("5–20", "Round 1 · Lesson 1 (whiteboards, I do / we do / you do)",
    "1. 4(x − 1) = 2x + 6 " + A("x = 5") + " 2. 3(2x + 1) = 6x + 3 " + A("infinite") + " 3. 7x − 1 = 7x + 4 " + A("no solution") +
    "<br>Name a property for each step in #1."),
   ("20–35", "Round 2 · Lesson 2",
    "4. 2x + 5y = 20 in slope-intercept; intercepts " + A("y = −⅖x + 4; (10, 0), (0, 4)") + "<br>5. y + 3 = 2(x − 1) in standard form " +
    A("2x − y = 5") + " 6. A = ½bh for h; A = 30, b = 12 " + A("h = 2A/b = 5")),
   ("35–50", "Round 3 · Lesson 3",
    "7. 3x − 4 > 11 " + A("x > 5") + " 8. −5x + 2 ≤ 17 " + A("x ≥ −3") + " 9. 2(x − 3) ≥ 4x + 2 " + A("x ≤ −4") +
    "<br>10. Phone plan: $30 + $0.10 per text, budget at most $45. " + A("30 + 0.10t ≤ 45 → t ≤ 150 texts") + "<br>Graph 7–9."),
   ("50–58", "Independent check", "Students redo the problem type they rated lowest without notes. Check answers at the door. " + IEP),
   ("58–60", "Wrap up", "Test tomorrow. Study: Topic 1 Summary SE pp. 389–390 and Lesson 1–3 homework.")],
  cfu=["Whiteboards every problem; re-teach any item under 70% right away.", "Thumbs on the flip rule before Round 3."],
  after=["Note who still misses the flip rule or no/infinite solutions; give them a test-day reminder card.", "Re-teach list for Thursday retakes."],
  note="No publisher M3T1 test is in materials/ yet; these review problems follow the TEKS for Lessons 1–3."),

 dict(file="Wed-11-18", date="Wednesday, November 18", lesson="Topic 1 End of Topic Assessment",
  obj=["Show mastery of Topic 1: linear equations, literal equations, linear inequalities."],
  teks=["<b>A.5A</b>, <b>A.5B</b>, <b>A.2C</b>, <b>A.3A</b>, A.2B, A.12E"], terms="(none new)",
  mat=["End of Topic 1 Assessment copies + answer key (district / Edia)", "IEP and 504 versions", "Calculators, scratch paper"],
  bell=[("Quiet start: write the flip rule and the 3 forms of a line on scratch paper", "allowed as a brain dump")],
  rows=[("0–5", "Settle", "Desks apart, phones away, calculators out. Brain dump on scratch paper."),
   ("5–55", "End of Topic 1 Assessment", "Independent. IEP/504 per plan: small group, read aloud, extra time, reminders card. Early finishers: check work, then Skills Practice from any lesson (no talking)."),
   ("55–60", "Collect", "Collect tests and scratch paper. Retakes tomorrow for scores below the district cut.")],
  cfu=["Walk the room; note common errors for tomorrow's re-teach."],
  after=["Score by question; group by lesson (1, 2, 3) for Thursday re-teach.", "Make a retake list."],
  note="Test date is fixed by the district. Test copies are not in this repo yet; add them to assessment/ once you have them."),

 dict(file="Thu-11-19", date="Thursday, November 19", lesson="Topic 1 Retakes + Re-teach",
  obj=["Fix the errors from the Topic 1 test.", "Retake for students below the cut; enrichment for everyone else."],
  teks=["<b>A.5A</b>, <b>A.5B</b>, <b>A.2C</b>, <b>A.3A</b>, A.2B, A.12E"], terms="(review)",
  mat=["Graded tests", "Retake form + key", "Activity 1.3 Tic-Tac-Bingo expression cards and boards (TE pp. 345M, 353)"],
  bell=[("Find your most-missed question and write the correct step", "error analysis")],
  rows=[("0–10", "Return tests", "Students correct one missed item per lesson in a different color."),
   ("10–30", "Re-teach in 3 small groups", "Group 1: no/infinite solutions. Group 2: rewriting forms + literal equations. Group 3: flip rule + context inequalities. Rotate while others correct."),
   ("30–55", "Retake / enrichment", "Below the cut: retake (" + IEP + ")<br>Everyone else: Activity 1.3 Tic-Tac-Bingo (skipped on 11/5)."),
   ("55–60", "Wrap up", "Collect retakes. Thanksgiving break 11/23–11/26. Next: Module 3 Topic 2, Lesson 1 (Mon 11/30).")],
  cfu=["Each student shows one corrected item per lesson before starting the retake."],
  after=["Record the higher score.", "Students still below → Skills Practice in Module 3 Topic 2 warm-ups."],
  note="Tic-Tac-Bingo gives the skipped Lesson 1 activity a home as enrichment."),
]


def ul(xs):
    return "<ul>" + "".join(f"<li>{x}</li>" for x in xs) + "</ul>"


def page(d):
    bell = ul(f"{q} {A(a)}" for q, a in d["bell"])
    rows = "".join(f"<tr><td>{t}</td><td>{act}</td><td>{what}</td></tr>" for t, act, what in d["rows"])
    return f"""<!doctype html>
<html><head><meta charset="utf-8"><title>Lesson Plan {d['file']}</title><style>{CSS}</style></head><body>
<h1>Lesson Plan · {d['date']}</h1>
<div class="sub">Algebra I · Mr. Pandey · Module 3, Topic 1, {d['lesson']} · essentials only (✪)</div>
<div class="grid">
<div><h2>Objectives (students will…)</h2>{ul(d['obj'])}</div>
<div><h2>TEKS</h2>{ul(d['teks'])}<h2>Key terms</h2><ul><li>{d['terms']}</li></ul></div>
<div><h2>Materials</h2>{ul(d['mat'])}</div>
<div><h2>Bell work (on the board)</h2>{bell}</div>
</div>
<h2>Agenda (60 minutes)</h2>
<table><tr><th>Time</th><th>Activity</th><th>What to do / say</th></tr>{rows}</table>
<div class="grid">
<div><h2>Check for understanding</h2>{ul(d['cfu'])}</div>
<div><h2>After class</h2>{ul(d['after'])}</div>
</div>
<p class="note">{d['note']}</p>
</body></html>"""


def materials(d):
    """Lesson days: bell work and exit ticket come from make_m3t1_lessons.py (the printed and online copies), so the plan,
    the slides and the handouts always match. Also lists every file for the day."""
    import re
    import make_m3t1_lessons as L
    key = next((k for k, v in L.DATES.items() if v == d["file"]), None)
    if not key:
        return d
    n, day = key
    plain = lambda s: re.sub(r"\[\[|\]\]", "", s)
    bell = []
    for k, q in enumerate(L.BELL[n, day], 1):
        order = L.print_order(q["choices"], (k + day + n) % 4)
        bell.append((plain(q["q"]), f"{('FGHJ' if k % 2 == 0 else 'ABCD')[order.index(q['choices'][0])]}. {plain(q['choices'][0])}"))
    ex = " ".join(f"{k}. {plain(it['short'])} {A(plain(it['answer']))}" for k, it in enumerate(L.EXIT[n, day], 1))
    rows = [(t, act, f"{ex}<br>{IEP}") if "xit ticket" in act else (t, act, what) for t, act, what in d["rows"]]
    date, stem = L.DATES[n, day], L.LESSONS[n]["stem"]
    mat = [f"Slides: {stem} (.html/.pptx) · publisher slides with answers: BLMathematics_AlgI_M3_T1_L{n}_LessonSlides_ENG_with_answers.pptx",
           f"Bell work: BELL WORK/T1-Bell-Work-{date}.pdf + key (online: m3t1-lesson{n}-bellwork-day{day})",
           f"Exit ticket: EXIT TICKET/T1-Exit-Ticket-{date}.pdf + key (written like the End of Topic 1 test)",
           f"Video: videos/{L.VIDEO_NAMES[n]} · IEP and 504 versions of all of these: IEP/, Section 504/, and the -IEP / -504 PDFs"]
    return dict(d, bell=bell, rows=rows, mat=mat + d["mat"])


if __name__ == "__main__":
    import fitz
    OUT.mkdir(parents=True, exist_ok=True)
    for d in DAYS:
        d = materials(d)
        src = OUT / f"T1-Lesson-Plan-{d['file']}.html"
        pdf = src.with_suffix(".pdf")
        for size in ("9.3pt", "8.8pt", "8.3pt"):  # shrink until the plan fits on one page
            src.write_text(page(d).replace("font-size:9.3pt", f"font-size:{size}"), encoding="utf-8")
            subprocess.run([EDGE, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={pdf}", src.as_uri()],
                           check=True, capture_output=True)
            if len(fitz.open(pdf)) == 1:
                break
        print(pdf.name, size)

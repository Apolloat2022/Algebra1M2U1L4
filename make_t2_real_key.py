# Detailed answer key for the publisher's End of Topic 2 Assessment (assessment/M2 TOPIC 2/AlgI_Assessments_SE.pdf, pp. 19-23).
# Quick key, then per item: worked solution, check, what each wrong answer means, partial credit, re-teach move;
# last page: item-analysis tally + retake groups by TEKS.   Run: python make_t2_real_key.py
import subprocess
from pathlib import Path

import make_t2_review_test as RT

RT.KEY = True
fr, grid, RED = RT.fr, RT.grid, RT.RED
OUT = Path(__file__).parent / "assessment" / "M2 TOPIC 2" / "Topic2-End-of-Topic-Assessment-ANSWER-KEY"
i = lambda s: f"<i>{s}</i>"
x, y, f, g, m, a, b = (i(c) for c in "xyfgmab")

# (num, type, answer, TEKS, lesson, prompt, steps, check, wrong answers, partial credit, re-teach, extra html)
ITEMS = [
    (1, "Fill in", f"{a} = −{fr(1, 2)}", "A.3E", "Lesson 1 · a·f(x)",
     f"The graph of {m} passes through (−6, 3) and (4, −2). Given {f}({x}) = {x} and {m}({x}) = {a}{f}({x}), find {a}.",
     [f"{m}({x}) = {a}·{f}({x}) = {a}{x}, so {a} is the <b>slope</b> of the line (the line goes through the origin).",
      f"slope = {fr('−2 − 3', '4 − (−6)')} = {fr('−5', '10')} = −{fr(1, 2)}",
      f"So {a} = −{fr(1, 2)} &nbsp;(also accept −0.5)."],
     f"Plug in a point: −½(−6) = 3 ✓ and −½(4) = −2 ✓. The line falls left to right, so {a} must be negative ✓.",
     [("−2", "Used run ÷ rise (10 ÷ −5) instead of rise ÷ run."),
      ("½ or 0.5", "Sign error: subtracted y-values in one order and x-values in the other."),
      ("−5 or 10", "Stopped at the rise or the run; didn't divide."),
      ("3 or −6", "Read a coordinate of a labeled point instead of finding the slope.")],
     "2 pts: −½. 1 pt: correct slope setup with one arithmetic or sign slip, or ½ with work that shows rise/run.",
     "Slope triangle on the grid between the two labeled points; say \"a stretches f(x) = x, so a IS the slope.\"", ""),
    (2, "Multiple choice", "B. 100 ≤ " + y + " ≤ 250", "A.2A", "Lesson 4 · domain and range in context",
     "Lawn service: $100 fixed + $25 per hour, at most 6 hours. What is the range for one day?",
     [f"Range = the possible <b>costs</b> ({y}-values). Domain = the hours ({x}-values).",
      "Least cost: 0 hours → 100 + 25(0) = $100.", "Greatest cost: 6 hours → 100 + 25(6) = 100 + 150 = $250.",
      f"Range: 100 ≤ {y} ≤ 250 → <b>B</b>."],
     "Two choices (C, D) are about x, so they describe domain, not range. Of A and B, only B starts at the $100 fixed fee.",
     [("A. 25 ≤ y ≤ 400", "Started at the $25 hourly rate instead of the $100 fixed fee; the maximum is too high (6 hours costs $250)."),
      ("C. 0 ≤ x ≤ 6", "This is the <b>domain</b> (hours). Mixed up domain and range."),
      ("D. 0 ≤ x ≤ 8", "Domain idea with the wrong maximum (8-hour work day assumption).")],
     "Multiple choice: all or nothing.", "Two-column chart: Domain = inputs = x = hours | Range = outputs = y = dollars. Evaluate at both ends.", ""),
    (3, "Multiple choice", f"G. {y} = 10; slope is zero", "A.2G", "Lesson 3 · horizontal and vertical lines",
     "What are the equation and slope of the horizontal line through y = 10?",
     [f"Every point on the line has {y}-value 10: (−40, 10), (0, 10), (40, 10). So the equation is {y} = 10.",
      "Rise between any two points = 10 − 10 = 0, so slope = 0 ÷ run = <b>0</b>.", "Answer <b>G</b>."],
     "Horizontal = \"y = number, slope zero\". Vertical = \"x = number, slope undefined\".",
     [("F. x = 10; slope is 10", "Wrong variable and treated the 10 as the slope."),
      ("H. x = 10; slope is zero", "Right slope, but named the line by x (that would be a vertical line)."),
      ("J. y = 10; slope is undefined", "Right equation, but mixed up zero (horizontal) and undefined (vertical) slope.")],
     "Multiple choice: all or nothing.", "\"HOY / VUX\": Horizontal, 0 slope, y = · Vertical, Undefined slope, x = .", ""),
    (4, "Multiple choice", "D. translated left 1 unit", "A.3E", "Lesson 2 · f(x − h)",
     f"Catalina graphed {f}({x}) and {g}({x}) = {f}({x} + 1). How are the graphs related?",
     [f"A change <b>inside</b> the parentheses moves the graph sideways.",
      f"{f}({x} + 1) = {f}({x} − (−1)), so {i('h')} = −1: the graph moves <b>left</b> 1.",
      f"Test a point: {g} reaches {f}'s value at {x} = 0 when {x} = −1, one unit to the left. Answer <b>D</b>."],
     "Make a quick table with f(x) = x: g(x) = x + 1 goes through (−1, 0), f goes through (0, 0): left 1 ✓ (it is also up 1 for this f, but the general rule is left).",
     [("A. up 1", "Treated + 1 inside like + 1 outside (vertical shift)."),
      ("B. down 1", "Vertical shift and wrong direction."),
      ("C. right 1", "Followed the sign: + → right. Inside the parentheses the direction is opposite.")],
     "Multiple choice: all or nothing.", "\"Inside lies\": inside the parentheses the graph moves opposite the sign. Desmos slider on h.", ""),
    (5, "Fill in", "5", "A.3E", "Lesson 2 · translating a table",
     f"Table for {f}: (−2, 7), (−1, 5), (0, 3), (1, 1), (2, −1), (3, −3). Translate {f} 1 unit right. What is the new {y}-intercept?",
     ["Right 1 means add 1 to every x; the y-values stay the same.",
      "The new y-intercept is where the new x is 0. The old point with x = −1 is (−1, 5); it moves to (0, 5).",
      f"Or by rule: {f}({x}) = −2{x} + 3, so {g}({x}) = {f}({x} − 1) = −2({x} − 1) + 3 = −2{x} + 5. y-intercept <b>5</b>."],
     "New table: (−1, 7), (0, 5), (1, 3)… still drops by 2 each step ✓.",
     [("1", "Moved the wrong way (left), so the point (1, 1) landed at (0, 1)."),
      ("3", "Gave the original y-intercept; didn't translate."),
      ("4", "Added 1 to the y-intercept (treated \"right\" as \"up\")."),
      ("(0, 5)", "Correct; accept the point form.")],
     "2 pts: 5 or (0, 5). 1 pt: correct new table or g(x) = −2x + 5 but wrong intercept read off.",
     "Have students rewrite the table with x + 1 in a new column, then find the row where x = 0.", ""),
    (6, "Graph", f"{g}({x}) = 3{x}: line through (0, 0), (1, 3), (2, 6), (−1, −3)", "A.3E", "Lesson 2 · f(bx)",
     f"{f}({x}) = {x} is graphed. Graph {g}({x}) = {f}(3{x}).",
     [f"{f}(3{x}): replace {x} with 3{x} in {f}({x}) = {x}, so {g}({x}) = 3{x}.",
      "Table: x = −2 → −6, x = −1 → −3, x = 0 → 0, x = 1 → 3, x = 2 → 6.",
      "Plot and connect: a steeper line through the origin (slope 3)."],
     "g should be 3 times as steep as f and still pass through (0, 0). At x = 2 it reaches 6, f only reaches 2.",
     [("Line with slope ⅓", "Thought f(3x) makes the graph wider by 3; for f(x) = x the graph gets steeper."),
      ("y = x + 3 (shifted up 3)", "Treated 3x as + 3."),
      ("y = x shifted left 3", "Treated f(3x) like f(x + 3).")],
     "2 pts: correct line through the origin with slope 3 (at least two correct points). 1 pt: correct table or equation g(x) = 3x, graph off.",
     "Table first, graph second. Compare f(2x), f(3x), f(½x) on one grid.",
     grid(-8, 8, 1, 2, [((-8, -8), (8, 8), "#000", True, "f(x)"), ((-8 / 3, -8), (8 / 3, 8), RED, False, "g(x) = 3x")],
          [(1, 3, "(1, 3)"), (2, 6, "(2, 6)"), (-1, -3, "(−1, −3)")], size=300)),
    (7, "Fill in", f"{y} = {fr(3, 2)}{x} − 6", "A.2F", "Lesson 3 · perpendicular lines",
     f"Line crosses the x-axis at 4 and is perpendicular to {y} = −{fr(2, 3)}{x} + 4. Write it in slope-intercept form.",
     [f"Given slope −{fr(2, 3)}. Perpendicular slope = negative reciprocal = <b>{fr(3, 2)}</b>.",
      "\"Crosses the x-axis at 4\" is the point (4, 0).",
      f"0 = {fr(3, 2)}(4) + {b} → 0 = 6 + {b} → {b} = −6.", f"{y} = {fr(3, 2)}{x} − 6 &nbsp;(also accept {y} = 1.5{x} − 6)."],
     f"Slopes multiply to −1: −{fr(2, 3)} × {fr(3, 2)} = −1 ✓. Point: {fr(3, 2)}(4) − 6 = 0 ✓.",
     [(f"y = −⅔x + 8/3", "Used the same slope (parallel, not perpendicular)."),
      (f"y = −3/2x + 6", "Took the reciprocal but kept the negative sign."),
      (f"y = 3/2x + 4", "Kept the original y-intercept instead of using (4, 0)."),
      (f"y = 3/2x − 4 or point (0, 4)", "Read \"crosses the x-axis at 4\" as the y-intercept.")],
     "2 pts: y = 3/2x − 6. 1 pt: correct slope 3/2 with a wrong b, or correct b from a wrong slope with work shown.",
     "Flip-and-switch drill on whiteboards (2/3 → −3/2), then \"x-axis at 4 means (4, 0)\".", ""),
    (8, "Fill in", f"{y} = 3.2{x} + 9.6", "A.2E", "Lesson 3 · parallel lines",
     f"Line through (−3, 0) parallel to {y} = 3.2{x} + 7.3. Write it in slope-intercept form.",
     ["Parallel lines have the <b>same slope</b>: 3.2.", f"0 = 3.2(−3) + {b} → 0 = −9.6 + {b} → {b} = 9.6.", f"{y} = 3.2{x} + 9.6"],
     "3.2(−3) + 9.6 = −9.6 + 9.6 = 0 ✓.",
     [("y = 3.2x + 7.3", "Copied the given line; didn't use the point."),
      ("y = 3.2x − 9.6", "Sign error solving for b (0 = −9.6 + b)."),
      ("y = −0.3125x + …", "Used the perpendicular slope (−1/3.2)."),
      ("y − 0 = 3.2(x + 3)", "Correct line in point-slope form: give 1 pt (question asks for slope-intercept).")],
     "2 pts: y = 3.2x + 9.6. 1 pt: correct point-slope form, or correct slope with an arithmetic slip in b.",
     "Same slope, new point, solve for b: three-step frame on an index card.", ""),
    (9, "Fill in", f"{y} − 2 = {fr(1, 4)}{x} &nbsp;or&nbsp; {y} = {fr(1, 4)}({x} + 8) &nbsp;or&nbsp; {y} − 4 = {fr(1, 4)}({x} − 8)", "A.2C",
     "Lesson 3 · point-slope form (Topic 1 skill)",
     "Write an equation in point-slope form for the graphed line.",
     ["Read two exact grid points: (−8, 0) and (0, 2). (The line also passes through (8, 4).)",
      f"slope = {fr('2 − 0', '0 − (−8)')} = {fr(2, 8)} = {fr(1, 4)}",
      f"Point-slope form {y} − {y}₁ = {m}({x} − {x}₁) with (−8, 0): {y} − 0 = {fr(1, 4)}({x} + 8).",
      "Any point on the line is correct: (0, 2) gives y − 2 = ¼(x − 0); (8, 4) gives y − 4 = ¼(x − 8)."],
     f"All three forms simplify to {y} = {fr(1, 4)}{x} + 2. Rises 1 for every 4 across on the grid ✓.",
     [("slope 4", "Run ÷ rise."), ("y − 0 = ¼(x − 8)", "Sign error with the point (−8, 0): x − (−8) = x + 8."),
      ("y = ¼x + 2", "Correct line, but slope-intercept form, not point-slope: 1 pt."),
      ("slope −¼", "Line rises left to right; slope must be positive.")],
     "2 pts: any correct point-slope equation. 1 pt: correct slope with a sign slip on the point, or the correct line in another form.",
     "Circle two lattice points first, slope triangle, then fill y − __ = __(x − __).",
     grid(-8, 8, 1, 2, [((-8, 0), (8, 4), RED, False, "")], [(-8, 0, "(−8, 0)"), (0, 2, "(0, 2)"), (8, 4, "(8, 4)")], size=280)),
    (10, "Select TWO", "H and K", "A.3C", "Lesson 4 · key attributes (Topic 1 skill)",
     "Line through (0, 4) and (8, 0). Which TWO statements describe it?",
     ["The line crosses the y-axis at (0, 4) → <b>H is true</b>.", "It crosses the x-axis at (8, 0), so the zero is 8 → <b>K is true</b>.",
      f"slope = {fr('0 − 4', '8 − 0')} = −{fr(1, 2)}: negative, so the graph is decreasing (F and G are false).",
      "J is false: 4 is the y-intercept, not the zero."],
     "Exactly two answers. Falls left to right ✓ (decreasing); y = −½x + 4 → y = 0 when x = 8 ✓.",
     [("F. increasing", "Read the line right to left."), ("G. slope ½", "Dropped the negative sign."),
      ("J. zero is 4", "Mixed up the zero (x-intercept) and the y-intercept.")],
     "STAAR scores select-two items all or nothing (both H and K). Optional classroom partial credit: 1 of 2 pts for one correct, no wrong.",
     "\"Zero = where y is zero = x-intercept\". Hands-on: trace the line left to right for increasing/decreasing.",
     grid(-8, 8, 1, 2, [((-8, 8), (8, 0), "#000", False, "")], [(0, 4, "(0, 4)"), (8, 0, "(8, 0)")], size=280)),
]

CSS = RT.CSS + """
.q{min-height:0;display:block;border-bottom:none;padding:0;break-inside:auto}
.item{break-inside:avoid;border:1.5px solid #111;border-radius:8px;padding:8px 12px;margin:0 0 12px}
.item h2{font-size:14pt;margin:0 0 4px;display:flex;justify-content:space-between}.tag{font-size:10pt;font-weight:normal;color:#555}
.big{border:2px solid #c8102e;border-radius:6px;padding:4px 10px;color:#c8102e;font-weight:bold;font-size:14pt;display:inline-block;margin:4px 0}
.prompt{color:#333;font-style:italic;margin:2px 0}.item ol{margin:4px 0 4px 18px;padding:0}.item li{margin:2px 0}
h3{font-size:11pt;margin:6px 0 2px;color:#0b4f8a}table.k,table.w,table.ia{border-collapse:collapse;width:100%;font-size:10.5pt}
.k td,.k th,.w td,.ia td,.ia th{border:1px solid #888;padding:3px 6px;text-align:left;vertical-align:top}.k th,.ia th{background:#eee}
.k td.a{color:#c8102e;font-weight:bold}.w td:first-child{width:28%;font-weight:bold}.cols{display:flex;gap:14px;align-items:flex-start}
.small{font-size:10pt;color:#444}.ia td{height:18px}
"""


def page():
    quick = "".join(f'<tr><td>{n}</td><td>{t}</td><td class="a">{ans}</td><td>{teks}</td><td>{les}</td></tr>'
                    for n, t, ans, teks, les, *_ in ITEMS)
    h = (f"<header><h1>End of Topic 2 Assessment · ANSWER KEY (detailed)</h1>"
         "<p class='sub'>Algebra I · Module 2, Topic 2: Transforming and Comparing Linear Functions · publisher test, Assessments book pp. 19–23 · given Tue Nov 3</p></header>"
         "<h3>Quick key</h3><table class='k'><tr><th>#</th><th>Type</th><th>Answer</th><th>TEKS</th><th>Lesson</th></tr>" + quick + "</table>"
         "<p class='small'><b>Suggested scoring</b> (the publisher gives no point values): 10 points per question = 100. Multiple choice and select-two are all or nothing. "
         "Open items (1, 5, 6, 7, 8, 9): full credit for the answer in any equivalent form; half credit as described under each item. "
         "TEKS on this test (TE p. 144D): A.2A, A.2C, A.2E, A.2F, A.2G, A.3C, A.3E. Readiness standards: A.2C, A.3C.</p>")
    for n, t, ans, teks, les, prompt, steps, check, wrong, partial, reteach, extra in ITEMS:
        sol = "<ol>" + "".join(f"<li>{s}</li>" for s in steps) + "</ol>"
        body = f'<div class="cols"><div style="flex:1">{sol}</div>{f"<div>{extra}</div>" if extra else ""}</div>'
        h += (f'<div class="item"><h2><span>Question {n} · {t}</span><span class="tag">{teks} · {les}</span></h2>'
              f'<p class="prompt">{prompt}</p><div class="big">{ans}</div><h3>Solution</h3>{body}'
              f'<h3>Check</h3><p>{check}</p><h3>If a student chose / wrote…</h3><table class="w">'
              + "".join(f"<tr><td>{w}</td><td>{why}</td></tr>" for w, why in wrong) + "</table>"
              f'<h3>Partial credit</h3><p>{partial}</p><h3>Re-teach (Wed Nov 4 retakes)</h3><p>{reteach}</p></div>')
    groups = [("Transformations (A.3E)", "1, 4, 5, 6", "Inside vs. outside; a = slope; table shifts"),
              ("Domain and range (A.2A)", "2", "Inputs vs outputs in context, evaluate at both ends"),
              ("Horizontal / vertical lines (A.2G)", "3", "HOY / VUX"),
              ("Parallel and perpendicular (A.2E, A.2F)", "7, 8", "Same slope / flip-and-switch, then solve for b"),
              ("Writing equations from a graph (A.2C)", "9", "Two lattice points, slope triangle, point-slope frame"),
              ("Key attributes (A.3C)", "10", "Zero vs y-intercept; increasing vs decreasing")]
    h += ('<div style="break-before:page"><h1 style="font-size:16pt">Item analysis and retake groups</h1>'
          "<p class='small'>Tally the number of students who missed each question. A question missed by 30% or more = whole-class re-teach on Nov 4; otherwise small group.</p>"
          "<table class='ia'><tr><th>#</th>" + "".join(f"<th>{n}</th>" for n in range(1, 11)) + "</tr>"
          "<tr><td>Answer</td>" + "".join(f"<td style='color:#c8102e;font-weight:bold'>{v}</td>" for v in ["−½", "B", "G", "D", "5", "y = 3x", "y = 1.5x − 6", "y = 3.2x + 9.6", "y = ¼(x + 8)", "H, K"]) + "</tr>"
          + "".join(f"<tr><td>Per. {p}</td>" + "<td></td>" * 10 + "</tr>" for p in range(1, 8))
          + "<tr><td>% missed</td>" + "<td></td>" * 10 + "</tr></table>"
          "<h3>Retake groups by skill</h3><table class='k'><tr><th>Group</th><th>Questions</th><th>Re-teach focus</th><th>Students</th></tr>"
          + "".join(f"<tr><td>{a_}</td><td>{q}</td><td>{fz}</td><td style='width:30%'></td></tr>" for a_, q, fz in groups) + "</table>"
          "<p class='small'>Retake form + key: Module 2 topic 2/Topic2-Retake(-ANSWER-KEY).pptx (IEP and 504 versions in IEP/ and Section 504/).</p></div>")
    return h


if __name__ == "__main__":
    src = OUT.with_suffix(".html")
    src.write_text(f"<!doctype html><meta charset='utf-8'><title>{OUT.name}</title><style>{CSS}</style>{page()}", encoding="utf-8")
    pdf = OUT.with_suffix(".pdf")
    subprocess.run([RT.EDGE, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={pdf}", src.as_uri()], check=True, capture_output=True)
    src.unlink()
    print(pdf)

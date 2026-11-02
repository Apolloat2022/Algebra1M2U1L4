# Topic 2 review day (Mon Nov 2), for the publisher End of Topic 2 Assessment on Tue Nov 3.
# The printed review is assessment/M2 TOPIC 2/Topic2-Review-Test*.pdf (make_t2_review_test.py: mirrors the real test item for item).
# This script adds what goes with it:
#   - review slides that work through review questions 1-10 step by step (.html + .pptx)
#   - an online self-check of all 14 review questions (General / IEP / 504)
#   - bell work + exit ticket PDFs (General / 504 / IEP, each with a key), test style
#   - the one-page lesson plan
# Run: python make_t2_review_day.py
import json, re, subprocess, sys
from pathlib import Path

import make_t2_decks as D
import make_t2_practice as MP
import make_accom_lessons as A
import make_m3t1_plans as PL

ROOT = Path(__file__).parent
OUT = ROOT / "Module 2 topic 2"
FOLDER = {"504": ROOT / "Section 504", "IEP": ROOT / "IEP"}
EDGE = PL.EDGE
DATE = "Mon-11-02"
M, mt, eq, ans, st, p, sec, row, card, graph, L, GO = D.M, D.mt, D.eq, D.ans, D.st, D.p, D.sec, D.row, D.card, D.graph, D.L, D.GO
C, P = D.C, D.P

REF = ["Slope = (y₂ − y₁) ÷ (x₂ − x₁) · y = mx + b · point-slope: y − y₁ = m(x − x₁)",
       "Parallel: same slope · Perpendicular: flip the fraction and change the sign (product −1)",
       "Outside f(x) + k: up/down · Inside f(x − h): right h, f(x + h): left h (opposite the sign)",
       "Horizontal: y = #, slope 0 · Vertical: x = #, slope undefined (HOY VUX)",
       "Domain = inputs (x) · Range = outputs (y) · Zero = x-intercept"]

# ------------------------------------------------------------------ bell work + exit ticket (first choice correct)
BELL = [
    dict(q="Kai graphed [[f(x)]] and [[g(x) = f(x + 5)]]. Which statement describes how the graphs are related?",
         choices=["translated left 5 units", "translated right 5 units", "translated up 5 units", "translated down 5 units"],
         why="Inside the parentheses the graph moves opposite the sign: + 5 → left 5.", tip="Inside the parentheses: move the opposite way of the sign."),
    dict(q="A pool rental costs $50 plus $30 per hour, for at most 4 hours. What is the range for one rental?",
         choices=["50 ≤ y ≤ 170", "0 ≤ x ≤ 4", "30 ≤ y ≤ 170", "50 ≤ y ≤ 200"],
         why="Range = costs. 0 hours: $50. 4 hours: 50 + 30(4) = $170.", tip="Range = the y-values (dollars). Find the cost at 0 hours and at 4 hours."),
    dict(q="What is the slope of a line perpendicular to [[y = −4/5x + 2]]?",
         choices=["5/4", "−5/4", "4/5", "−4/5"],
         why="Flip −4/5 to −5/4 and change the sign: 5/4. Check: (−4/5)(5/4) = −1.", tip="Flip the fraction and change the sign."),
    dict(q="A line passes through (0, −3) and (6, 0). What is the zero of the function?",
         choices=["6", "−3", "1/2", "−6"],
         why="The zero is where y = 0: the point (6, 0). −3 is the y-intercept.", tip="The zero is the x-value where the line crosses the x-axis."),
]
EXIT = [
    dict(q="What are the equation and slope of the vertical line through (−7, 2)?",
         choices=["x = −7; slope is undefined", "y = 2; slope is zero", "x = −7; slope is zero", "y = −7; slope is undefined"],
         why="Vertical: every point has x = −7. Slope = rise ÷ 0: undefined (VUX).", tip="HOY VUX: Vertical → Undefined slope → x = #."),
    dict(q="Write the equation in slope-intercept form of the line through (−1, 0) that is parallel to [[y = 5x − 2]].",
         answer="y = 5x + 5", why="Same slope 5. 0 = 5(−1) + b → b = 5.", tip="Parallel → same slope. Then put in the point and solve for b.",
         frames=["Slope = ______", "0 = ___(−1) + b → b = ______", "y = ______x + ______"]),
    dict(q="[[f(x) = 2x + 1]] is translated 3 units left. What is the y-intercept of the new function?",
         answer="7", why="g(x) = f(x + 3) = 2(x + 3) + 1 = 2x + 7. y-intercept 7.", tip="Left 3 means f(x + 3). Put (x + 3) in for x.",
         frames=["g(x) = 2(x + 3) + 1", "g(x) = 2x + ______ + 1 = 2x + ______", "y-intercept = ______"]),
]


def plainm(s):
    return re.sub(r"\[\[(.+?)\]\]", lambda g: M(g.group(1)), s)


SHEET_CSS = """@page{size:letter;margin:.5in}body{font-family:Segoe UI,Arial,sans-serif;font-size:12pt;color:#111;margin:0}
.top{background:#e6eefc;padding:6px 10px;font-size:15pt}.top b{color:#3050b8;font-size:10pt;letter-spacing:.5px}
.hdr{display:flex;justify-content:space-between;font-size:9pt;color:#444;margin-bottom:4px}.nm{margin:10px 0 12px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:0 26px}.one{display:block}.it{min-height:3in;break-inside:avoid;padding-top:6px}
.it.mc{min-height:2.3in}.ch{margin:8px 0 0 18px}.ch div{margin:7px 0}.big{font-size:15pt}.big .it{min-height:3.6in}
.tip{border-left:5px solid #2f6fdd;background:#eef3fc;padding:5px 10px;margin:8px 0;font-size:11.5pt}
.ref{border:1.5px solid #2f6fdd;border-radius:6px;padding:6px 12px;margin-bottom:10px;font-size:11pt}.ref p{margin:3px 0}
.fr{margin:12px 0 0 10px;line-height:2.1}.ans{color:#b00000;font-weight:600}.why{color:#b00000;font-size:10pt;margin-top:6px}"""


def sheet(name, what, items, key, kind, title=None):
    blocks = []
    for k, it in enumerate(items, 1):
        letters = "ABCD" if k % 2 else "FGHJ"
        b = f'<div class="it{" mc" if it.get("choices") else ""}"><b>{k}.</b> {plainm(it["q"])}'
        if kind == "IEP":
            b += f'<div class="tip"><b>Tip:</b> {it["tip"]}</div>'
        if it.get("choices"):
            ch = it["choices"][:3] if kind == "IEP" else it["choices"]
            pos = (k + 1) % len(ch)  # rotate where the right answer prints
            order = ch[1:pos + 1] + [ch[0]] + ch[pos + 1:]
            b += '<div class="ch">' + "".join(f'<div><b>{l}.</b> <span class="{"ans" if key and c == ch[0] else ""}">{plainm(c)}</span></div>'
                                              for l, c in zip(letters, order)) + "</div>"
        else:
            if kind == "IEP":
                b += '<div class="fr">' + "<br>".join(it["frames"]) + "</div>"
            if key:
                b += f'<div class="ans" style="margin-top:8px">{M(it["answer"])}</div>'
        if key:
            b += f'<div class="why">{it["why"]}</div>'
        blocks.append(b + "</div>")
    lab = {"504": " · SECTION 504 VERSION", "IEP": " · IEP VERSION"}.get(kind, "")
    ref = ('<div class="ref"><b>Reminders</b>' + "".join(f"<p>{r}</p>" for r in REF) + "</div>") if kind else ""
    html = (f'<!doctype html><meta charset="utf-8"><title>{name}</title><style>{SHEET_CSS}</style>'
            f'<div class="hdr"><span>MODULE 2 • TOPIC 2 • REVIEW DAY • {(title or what).upper()}{lab}</span><span>{"ANSWER KEY" if key else ""}</span></div>'
            f'<div class="top"><b>TOPIC 2</b> Transforming and Comparing Linear Functions</div>'
            f'<div class="nm">Name ____________________________ &nbsp; Date __________</div>{ref}'
            f'<div class="{"one big" if kind else "grid"}">{"".join(blocks)}</div>')
    folder = OUT / what
    src = folder / f"{name}.html"
    src.write_text(html, encoding="utf-8")
    subprocess.run([EDGE, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={src.with_suffix('.pdf')}", src.as_uri()],
                   check=True, capture_output=True)
    src.unlink()


def sheets():
    for kind in (None, "504", "IEP"):
        sfx = f"-{kind}" if kind else ""
        for key in (False, True):
            k2 = "-ANSWER-KEY" if key else ""
            sheet(f"T2-Bell-Work-{DATE}{sfx}{k2}", "BELL WORK", BELL, key, kind)
            sheet(f"T2-Exit-Ticket-{DATE}{sfx}{k2}", "EXIT TICKET", EXIT, key, kind)
    print("bell work + exit ticket PDFs")


def letter(items, k):  # printed letter of the right answer (general version)
    ch = items[k - 1]["choices"]
    pos = (k + 1) % len(ch)
    return ("ABCD" if k % 2 else "FGHJ")[pos]


# ------------------------------------------------------------------ online self-check: the 14 review-test questions
ONLINE = [
    ("The graph of linear function [[m]] passes through (−6, 4) and (3, −2). Given [[f(x) = x]] and [[m(x) = af(x)]], what is the value of [[a]]?",
     ["−2/3", "−3/2", "2/3", "3/2"], "a is the slope: (−2 − 4) ÷ (3 − (−6)) = −6/9 = −2/3.", "a is the slope of m(x) = a·x."),
    ("A bounce house costs $75 plus $20 per hour, for at most 5 hours. What is the range for one day?",
     ["75 ≤ y ≤ 175", "0 ≤ x ≤ 5", "20 ≤ y ≤ 175", "0 ≤ x ≤ 7"], "Range = costs: 0 hours $75, 5 hours 75 + 20(5) = $175.", "Range = y-values."),
    ("A horizontal line passes through (0, −20). What are its equation and slope?",
     ["y = −20; slope is zero", "x = −20; slope is undefined", "y = −20; slope is undefined", "x = −20; slope is zero"],
     "Horizontal: y = number, slope 0 (HOY).", "HOY: Horizontal → 0 slope → y = #."),
    ("Marcus graphed [[f(x)]] and [[g(x) = f(x − 3)]]. How are the graphs related?",
     ["translated right 3 units", "translated left 3 units", "translated up 3 units", "translated down 3 units"],
     "Inside the parentheses: opposite the sign. x − 3 → right 3.", "Inside: move opposite the sign."),
    ("[[f(x)]] has the table (−2, −7), (−1, −4), (0, −1), (1, 2). Translate it 2 units right. What is the new y-intercept?",
     ["−7", "−1", "5", "1"], "The point (−2, −7) moves to (0, −7). Or g(x) = 3(x − 2) − 1 = 3x − 7.", "Right 2: add 2 to each x. Find the point where x = 0."),
    ("[[f(x) = x]] and [[g(x) = f(2x)]]. Which equation is [[g(x)]]?",
     ["g(x) = 2x", "g(x) = ½x", "g(x) = x + 2", "g(x) = x − 2"], "Put 2x in for x: g(x) = 2x, a steeper line through (0, 0).", "f(2x): replace x with 2x."),
    ("Which line crosses the x-axis at −6 and is perpendicular to [[y = 3/2x − 1]]?",
     ["y = −2/3x − 4", "y = −2/3x + 4", "y = 3/2x + 9", "y = −3/2x − 9"],
     "Slope −2/3. Point (−6, 0): 0 = −2/3(−6) + b → b = −4.", "Flip and change the sign; x-axis at −6 = the point (−6, 0)."),
    ("Which line passes through (5, 0) and is parallel to [[y = −2.4x + 1.6]]?",
     ["y = −2.4x + 12", "y = −2.4x − 12", "y = −2.4x + 1.6", "y = 2.4x − 12"], "Same slope −2.4. 0 = −2.4(5) + b → b = 12.", "Parallel → same slope, then solve for b."),
    ("A line passes through (−2, −3) and (2, 5). Which is an equation in point-slope form?",
     ["y − 5 = 2(x − 2)", "y − 5 = 2(x + 2)", "y + 5 = 2(x − 2)", "y − 5 = ½(x − 2)"], "Slope = 8 ÷ 4 = 2. With (2, 5): y − 5 = 2(x − 2).", "y − y₁ = m(x − x₁)."),
    ("A line passes through (−4, 0) and (0, 2). Which statement is true?",
     ["It is increasing and its zero is −4.", "It is increasing and its zero is 2.", "Its slope is 2 and its zero is −4.", "It is decreasing and its zero is −4."],
     "It rises left to right (slope ½). It crosses the x-axis at −4. The y-intercept is 2.", "Zero = x-intercept. Increasing = goes up left to right."),
    ("Let [[f(x) = x − 1]], [[g(x) = f(2x)]] and [[h(x) = 2f(x)]]. Which is true?",
     ["Same slope, different y-intercepts", "They are the same function", "Different slopes, same y-intercept", "Different slopes and y-intercepts"],
     "g(x) = 2x − 1 and h(x) = 2x − 2: slope 2 both, intercepts −1 and −2.", "f(2x): put in 2x. 2f(x): multiply the whole thing by 2."),
    ("Which pair of equations represents perpendicular lines?",
     ["y = −1/3x + 4 and y = 3x − 2", "y = 5x + 1 and y = −5x + 2", "y = 4/5x and y = 5/4x − 1", "y = 2x + 3 and y = 2x − 3"],
     "−1/3 × 3 = −1. (The last pair is parallel.)", "Multiply the slopes: −1 means perpendicular."),
    ("[[f(x) = 2x + 1]] and [[g(x) = f(x) − 4]]. Which describes [[g]]?",
     ["g(x) = 2x − 3; down 4 units", "g(x) = 2x + 5; up 4 units", "g(x) = 2x − 3; right 4 units", "g(x) = 2x − 4; down 4 units"],
     "Subtract 4 from every output: 2x + 1 − 4 = 2x − 3, down 4.", "Outside the function: up or down."),
    ("A 300-gallon tank drains 15 gallons per minute until empty. What is the domain?",
     ["0 ≤ x ≤ 20", "0 ≤ x ≤ 300", "0 ≤ y ≤ 300", "15 ≤ x ≤ 300"], "Domain = minutes. 300 ÷ 15 = 20 minutes.", "Domain = x-values (minutes)."),
]


def online(base="t2-test-review", items=ONLINE, title="Topic 2 Test Review",
           intro="Questions 1–10 are the same as the printed review, which is written just like Tuesday's test; 11–14 are extra practice. "
                 "Pick an answer to see if you are right and why."):
    data = [{"q": q, "choices": ch, "why": why} | ({"letters": "FGHJ"} if j % 2 else {}) for j, (q, ch, why, _) in enumerate(items)]
    MP.OUT = OUT
    name = f"{base}.html"
    MP.page(name, f"{title} · Self-Check", "Module 2 · Topic 2 · Review Day · Mon Nov 2", title, intro, "homework", data)
    s = (OUT / name).read_text(encoding="utf-8")
    for kind, lab in (("504", "Section 504"), ("IEP", "IEP")):
        accom = {"readAloud": True}
        if kind == "IEP":
            accom["choices"] = 3
            accom["add"] = [{"extra": f'<p style="margin:8px 0 2px;padding:6px 12px;border-left:4px solid #2f6fdd;background:rgba(47,111,221,.08);border-radius:4px"><b>Tip:</b> {tip}</p>'}
                            for *_, tip in items]
        t = s.replace("</title>", f" · {lab}</title>", 1).replace('<div class="wrap">', '<div class="wrap big">', 1)
        t = re.sub(r'(<p class="eyebrow">.*?)</p>', lambda g: f"{g.group(1)} · {lab} Version</p>", t, count=1)
        t = re.sub(r'(<p class="muted">.*?</p>)', lambda g: g.group(1) + f'\n  <div class="card ref"><p>{A.HELP[kind]}</p>' + "".join(f"<p>{r}</p>" for r in REF) + "</div>", t, count=1)
        t = t.replace('</script>\n<script src="../mc.js">', f'window.MC.accom = {json.dumps(accom, ensure_ascii=False)};\n</script>\n<script src="../mc.js">')
        assert "window.MC.accom" in t
        (FOLDER[kind] / f"{base}-{kind}.html").write_text(t, encoding="utf-8")
    print("online pages", base)


# ------------------------------------------------------------------ Test Review 2: for students who finish Review 1 (same 10 test skills, new numbers + 2 extra)
# first choice correct; "answer"/"frames" = the item is open response on paper (like the test), multiple choice online
REVIEW2 = [
    dict(q="The graph of linear function [[m]] passes through (−4, 6) and (2, −3). Given [[f(x) = x]] and [[m(x) = af(x)]], what is the value of [[a]]?",
         choices=["−3/2", "−2/3", "3/2", "2/3"], answer="a = −3/2", why="a is the slope: (−3 − 6) ÷ (2 − (−4)) = −9/6 = −3/2.",
         tip="a is the slope. Use (y₂ − y₁) ÷ (x₂ − x₁).", frames=["Slope = (−3 − 6) ÷ (2 − (−4)) = ____ ÷ ____", "a = ______"]),
    dict(q="A food truck rents for $120 plus $45 per hour, for at most 6 hours. What is the range for one rental?",
         choices=["120 ≤ y ≤ 390", "0 ≤ x ≤ 6", "45 ≤ y ≤ 390", "120 ≤ y ≤ 270"], why="Range = costs. 0 hours: $120. 6 hours: 120 + 45(6) = $390.",
         tip="Range = the y-values (dollars). Find the cost at 0 hours and at 6 hours."),
    dict(q="A vertical line passes through (8, −3). What are its equation and slope?",
         choices=["x = 8; slope is undefined", "y = −3; slope is zero", "x = 8; slope is zero", "y = 8; slope is undefined"],
         why="Vertical: every point has x = 8. Slope = rise ÷ 0: undefined (VUX).", tip="HOY VUX: Vertical → Undefined slope → x = #."),
    dict(q="Lena graphed [[f(x)]] and [[g(x) = f(x + 4)]]. Which statement describes how the graphs are related?",
         choices=["translated left 4 units", "translated right 4 units", "translated up 4 units", "translated down 4 units"],
         why="Inside the parentheses the graph moves opposite the sign: + 4 → left 4.", tip="Inside the parentheses: move the opposite way of the sign."),
    dict(q="[[f(x)]] has the table (−1, 8), (0, 5), (1, 2), (2, −1). The graph is translated 3 units left. What is the y-intercept of the new function?",
         choices=["−4", "5", "14", "−1"], answer="−4", why="f(x) = −3x + 5. Left 3: g(x) = f(x + 3) = −3x − 4. Check: the point at x = 3, (3, −4), moves to (0, −4).",
         tip="Left 3: subtract 3 from each x. Which point lands on x = 0?", frames=["Left 3: g(x) = f(x + 3)", "g(0) = f(____) = ______", "y-intercept = ______"]),
    dict(q="[[f(x) = x]] and [[g(x) = f(½x)]]. Write the equation for [[g(x)]].",
         choices=["g(x) = ½x", "g(x) = 2x", "g(x) = x + ½", "g(x) = x − 2"], answer="g(x) = ½x", why="Put ½x in for x: g(x) = ½x, a less steep line through (0, 0).",
         tip="f(½x): replace x with ½x.", frames=["f(x) = x, so f(½x) = ______", "g(x) = ______"]),
    dict(q="Write the equation in slope-intercept form of the line that crosses the x-axis at 8 and is perpendicular to [[y = 4x + 1]].",
         choices=["y = −1/4x + 2", "y = −1/4x − 2", "y = 4x − 32", "y = 1/4x − 2"], answer="y = −1/4x + 2", why="Slope −1/4. Point (8, 0): 0 = −1/4(8) + b → b = 2.",
         tip="Flip the slope and change the sign. Crosses the x-axis at 8 = the point (8, 0).", frames=["Slope = ______", "0 = ____(8) + b → b = ______", "y = ______x + ______"]),
    dict(q="Write the equation in slope-intercept form of the line through (−6, 0) that is parallel to [[y = 1.5x − 4]].",
         choices=["y = 1.5x + 9", "y = 1.5x − 9", "y = −1.5x − 9", "y = 1.5x − 4"], answer="y = 1.5x + 9", why="Same slope 1.5. 0 = 1.5(−6) + b → b = 9.",
         tip="Parallel → same slope. Then put in the point and solve for b.", frames=["Slope = ______", "0 = 1.5(−6) + b → b = ______", "y = ______x + ______"]),
    dict(q="A line passes through (1, −2) and (4, 7). Write an equation of the line in point-slope form.",
         choices=["y − 7 = 3(x − 4)", "y + 7 = 3(x + 4)", "y − 7 = 3(x + 4)", "y − 7 = ⅓(x − 4)"], answer="y − 7 = 3(x − 4)  (or y + 2 = 3(x − 1))",
         why="Slope = (7 − (−2)) ÷ (4 − 1) = 9 ÷ 3 = 3. With (4, 7): y − 7 = 3(x − 4).", tip="Find the slope, then use y − y₁ = m(x − x₁).",
         frames=["Slope = (7 − (−2)) ÷ (4 − 1) = ______", "y − 7 = ____(x − 4)"]),
    dict(q="A line passes through (0, 6) and (3, 0). Which statement is true?",
         choices=["It is decreasing and its zero is 3.", "It is decreasing and its zero is 6.", "It is increasing and its zero is 3.", "Its slope is −1/2 and its zero is 3."],
         why="It falls left to right (slope −6/3 = −2). It crosses the x-axis at 3. The y-intercept is 6.", tip="Zero = x-intercept. Decreasing = goes down left to right."),
    dict(q="Which pair of equations represents perpendicular lines?",
         choices=["y = 2/3x − 1 and y = −3/2x + 4", "y = 2/3x + 1 and y = 2/3x − 4", "y = 2/3x and y = 3/2x + 2", "y = −2/3x + 1 and y = −3/2x"],
         why="2/3 × (−3/2) = −1. (The second pair is parallel.)", tip="Multiply the slopes: −1 means perpendicular."),
    dict(q="A phone is at 80% battery and loses 4% per hour until it is empty. What is the domain?",
         choices=["0 ≤ x ≤ 20", "0 ≤ x ≤ 80", "0 ≤ y ≤ 80", "4 ≤ x ≤ 80"], why="Domain = hours. 80 ÷ 4 = 20 hours.", tip="Domain = x-values (hours). How long until 0%?"),
]


def review2():
    paper = [{k: v for k, v in it.items() if k != "choices"} if it.get("answer") else it for it in REVIEW2]
    (OUT / "REVIEW").mkdir(exist_ok=True)
    for kind in (None, "504", "IEP"):
        sfx = f"-{kind}" if kind else ""
        for key in (False, True):
            sheet(f"T2-Review-2{sfx}{'-ANSWER-KEY' if key else ''}", "REVIEW", paper, key, kind, title="Test Review 2")
    print("review 2 PDFs")
    online("t2-test-review-2", [(it["q"], it["choices"], it["why"], it["tip"]) for it in REVIEW2], "Topic 2 Test Review 2",
           "Finished Review 1? Try this one. Questions 1–10 are written like Tuesday's test with new numbers; 11–12 are extra practice. "
           "Pick an answer to see if you are right and why.")


# ------------------------------------------------------------------ slides
def bell_slide():
    items = "".join(f'<p{" style=\"margin-top:12px\"" if k % 2 == 0 else ""}>{k}. {D.mq(q["q"])}</p>{ans(letter(BELL, k) + ". " + q["choices"][0])}'
                    for k, q in enumerate(BELL, 1))
    return sec("Mon Nov 2 · Bell Work · Test Warm-Up", "Warm up: work these on your own", f'<div class="col" style="gap:4px;font-size:24px">{items}</div>',
               "Printed copy: BELL WORK/T2-Bell-Work-Mon-11-02.pdf (IEP and 504 versions too). About 5 minutes while you take attendance. "
               + " ".join(f"{k}. {q['why']}" for k, q in enumerate(BELL, 1)))


def agenda_slide():
    items = [("1", "Bell Work", "Four test warm-ups. Start as soon as you sit down."),
             ("2", "Test Review", "Review 1 together, then on your own. Finished? Grab <b>Test Review 2</b>."),
             ("3", "Get Ready for Tomorrow!", "Topic 2 Test is <b>Tuesday, Nov 3</b>. Know your 7 skills and test tips.")]
    body = ('<div class="col" style="gap:16px;font-size:28px">' + "".join(
        f'<p style="margin:0"><b style="display:inline-block;width:46px;height:46px;line-height:46px;text-align:center;border-radius:50%;background:#2f6fdd;color:#fff;margin-right:14px">{n}</b>'
        f'<b>{t}</b> · {w}</p>' for n, t, w in items) + '</div><p style="font-size:34px;margin-top:22px;text-align:center"><b>Let’s get busy! 💪</b></p>')
    return sec("Monday, November 2 · Welcome back!", "Welcome back! Today’s Agenda", body,
               "Leave this up as students walk in. Same agenda all 6 periods. Point to the bell work, then go.")


def g8(lines, pts=(), alt=""):
    return graph(300, 300, [-8, 8], [-8, 8], [1, 2], [1, 2], lines, pts, alt)


def deck():
    T = "Bluebonnet Algebra I · Module 2 · Topic 2 · Review"
    s = [f'<section class="slide">\n  <p class="eyebrow">{T} · Mon Nov 2 · Test Tue Nov 3</p>\n'
         f'  <h1 style="margin-top:6px;font-size:56px">Topic 2 Test Review</h1>\n  <div class="eq" style="margin-top:8px;font-size:36px">Transforming and Comparing Linear Functions</div>\n'
         f'  <p style="font-size:24px;margin-top:6px">Self-check: <b><a class="go" href="t2-test-review.html" {GO}>Topic 2 Test Review →</a></b></p>\n'
         f'  <p class="muted small">Click, or press → / Space, to reveal each step. ← goes back. F = full screen.</p>\n  {D.FOOT}\n'
         '  <aside class="notes">Review for the publisher End of Topic 2 Assessment (10 questions). Students have the printed Topic 2 Review Test '
         '(assessment/M2 TOPIC 2/Topic2-Review-Test.pdf): questions 1–10 are written just like the test, in the same order. These slides work through 1–10.</aside>\n</section>\n',
         agenda_slide(), bell_slide()]
    s.append(sec("Today", "Plan for the review", '<div class="col" style="gap:10px;font-size:26px">' + "".join(
        f'<p class="step">{t}</p>' for t in ["1. Bell work: four test warm-ups", "2. Review questions 1–3 together (I do)", "3. Questions 4–8 in pairs, whiteboards up (we do)",
                                              "4. Questions 9–10 alone, like the test (you do)", "5. Finished? Test Review 2 (printed or online)", "6. Exit ticket"]) + "</div>",
        "Hand out the printed review now. The test tomorrow has 10 questions in this same order."))
    s.append(sec("The 7 skills on the test", "What tomorrow's test asks", row(
        card("Transformations (A.3E)", p("Q1, 4, 5, 6: a·f(x), f(x − h), f(bx), shifting a table")) + card("Domain and range (A.2A)", p("Q2: costs are the range")),
        card("Lines (A.2E, A.2F, A.2G)", p("Q3, 7, 8: horizontal, perpendicular, parallel")) + card("Equations and features (A.2C, A.3C)", p("Q9, 10: point-slope form, zero, increasing")), gap=24),
        "Readiness standards (most points on STAAR): A.2C and A.3C."))
    s.append(sec("Review Q1 · like test Q1 · I do", f"Find {mt('a')} when {mt('m(x) = af(x)')} and {mt('f(x) = x')}",
                 row(st(f"{mt('m(x) = a · x')}, so {C(mt('a'))} is the <b>slope</b> of the line.") + eq("slope = (−2 − 4) ÷ (3 − (−6))", "sm", True)
                     + eq("= −6 ÷ 9 = −2/3", "sm", True) + ans("a = −2/3") + st("Check: the line falls, so a is negative."),
                     g8([L((-6, 4), (3, -2))], [[-6, 4, "(−6, 4)"], [3, -2, "(3, −2)"]], "Line through (−6, 4) and (3, −2)")),
                 "Most common error: run over rise (−3/2). Draw the slope triangle between the two labeled points."))
    s.append(sec("Review Q2 · like test Q2 · I do", "Bounce house: $75 + $20 per hour, at most 5 hours. Range?",
                 row(st("<b>Range</b> = the outputs = the <b>costs</b> (y). <b>Domain</b> = the hours (x).") + eq("0 hours: 75 + 20(0) = 75", "sm", True)
                     + eq("5 hours: 75 + 20(5) = 175", "sm", True) + ans("C. 75 ≤ y ≤ 175", True),
                     card("Cross out", p("Choices about x are the domain, not the range.") + p("A range must start at the fixed fee."))),
                 "Students cross out the two x-choices first. Two choices left, then evaluate at both ends."))
    s.append(sec("Review Q3 · like test Q3 · I do", "Equation and slope of the line shown",
                 row(st("Every point has y-value −20: (−40, −20), (0, −20), (40, −20).") + ans("y = −20") + st("Rise = 0, so slope = 0.")
                     + ans("H. y = −20; slope is zero", True) + st("<b>HOY VUX</b>: Horizontal → 0 slope → y = # · Vertical → Undefined → x = #."),
                     graph(300, 300, [-40, 40], [-40, 40], [10, 20], [10, 20], [L((-40, -20), (40, -20))], [], "Horizontal line y = −20")),
                 "The real test uses y = 10. Same idea."))
    s.append(sec("Review Q4 · like test Q4 · We do", f"{mt('g(x) = f(x − 3)')}. How did the graph move?",
                 row(st("A change <b>inside</b> the parentheses moves the graph left or right.") + st(f"It moves the <b>opposite</b> way of the sign: {P(mt('x − 3'))} → right 3.")
                     + ans("C. translated right 3 units", True) + st("Outside, f(x) − 3, would be down 3."),
                     card("Inside vs. outside", p(f"{mt('f(x) + 3')}: up 3") + p(f"{mt('f(x − 3)')}: right 3") + p(f"{mt('f(x + 3)')}: left 3"))),
                 "The real test uses f(x + 1): left 1. Ask: which way does + 1 inside move it?"))
    s.append(sec("Review Q5 · like test Q5 · We do", "Translate the table 2 units right. New y-intercept?",
                 row(D.table(["x", "f(x)", "x + 2", "new point"], [["−2", "−7", "0", "(0, −7)"], ["−1", "−4", "1", "(1, −4)"], ["0", "−1", "2", "(2, −1)"]], 24, (2, 3))
                     + ans("y-intercept = −7"),
                     st("Right 2: add 2 to every x. The y-values don't change.") + st("Find the new point where x = 0: (−2, −7) → (0, −7).")
                     + st(f"Rule check: {mt('f(x) = 3x − 1')}, {mt('g(x) = 3(x − 2) − 1 = 3x − 7')}.")),
                 "The real test translates 1 unit right."))
    s.append(sec("Review Q6 · like test Q6 · We do", f"Graph {mt('g(x) = f(2x)')} when {mt('f(x) = x')}",
                 row(st(f"Put 2x in for x: {mt('g(x) = 2x')}.") + D.table(["x", "−2", "−1", "0", "1", "3"], [["g(x)", "−4", "−2", "0", "2", "6"]], 24, (1, 2, 3, 4, 5))
                     + st("Plot and connect: a steeper line through (0, 0)."),
                     g8([L((-8, -8), (8, 8), "f(x)", dash=True), L((-4, -8), (4, 8), "g(x)", "a", True)], [[1, 2, "(1, 2)"], [3, 6, "(3, 6)"]], "f(x) = x dashed and g(x) = 2x")),
                 "The real test uses f(3x). Common error: drawing slope ½."))
    s.append(sec("Review Q7 · like test Q7 · We do", f"Crosses the x-axis at −6, perpendicular to {mt('y = 3/2x − 1')}",
                 '<div class="col" style="gap:8px">' + st(f"Perpendicular slope: flip and change the sign: {C(mt('3/2'))} → {C(mt('−2/3'))}.")
                 + st("x-axis at −6 means the point (−6, 0).") + eq("0 = −2/3(−6) + b → 0 = 4 + b → b = −4", "sm", True) + ans("y = −2/3x − 4") + "</div>",
                 "Real test: crosses the x-axis at 4, perpendicular to y = −2/3x + 4 (answer y = 3/2x − 6). Don't give that away today."))
    s.append(sec("Review Q8 · like test Q8 · We do", f"Through (5, 0), parallel to {mt('y = −2.4x + 1.6')}",
                 '<div class="col" style="gap:8px">' + st("Parallel: <b>same</b> slope, −2.4.") + eq("0 = −2.4(5) + b → 0 = −12 + b → b = 12", "sm", True)
                 + ans("y = −2.4x + 12") + st("Check: −2.4(5) + 12 = 0 ✓") + "</div>", "Common error: b = −12 (sign slip)."))
    s.append(sec("Review Q9 · like test Q9 · You do", "Write an equation in point-slope form",
                 row(st("Pick two exact grid points: (−2, −3) and (2, 5).") + eq("slope = (5 − (−3)) ÷ (2 − (−2)) = 8 ÷ 4 = 2", "sm", True)
                     + ans("y − 5 = 2(x − 2)") + st("Also right: y + 3 = 2(x + 2)."),
                     g8([L((-2, -3), (2, 5))], [[-2, -3, "(−2, −3)"], [2, 5, "(2, 5)"]], "Line through (−2, −3) and (2, 5)")),
                 "On the real test the points are not labeled: find two lattice points first."))
    s.append(sec("Review Q10 · like test Q10 · You do", "Select TWO correct statements",
                 row(st("The line rises left to right: <b>increasing</b>.") + st("It crosses the x-axis at −4: the <b>zero</b> is −4.")
                     + st("Slope = 2 ÷ 4 = ½ (not 2). y-intercept (0, 2) (not −4).") + ans("F and J", True),
                     g8([L((-4, 0), (0, 2))], [[-4, 0, "(−4, 0)"], [0, 2, "(0, 2)"]], "Line through (−4, 0) and (0, 2)")),
                 "Select TWO: both must be right for the point. Zero = x-intercept, never the y-intercept."))
    s.append(sec("Test tips", "Before tomorrow", '<div class="col" style="gap:10px;font-size:26px">' + "".join(f'<p class="step">{t}</p>' for t in [
        "Cross out the choices about the wrong variable (domain vs range).", "Inside the parentheses: move opposite the sign.",
        "Perpendicular: flip and change the sign. Parallel: same slope.", "x-axis at 4 means the point (4, 0).",
        "Select TWO means exactly two.", "Check every equation with a point."]) + "</div>", "Students copy these on an index card to read tonight."))
    ex = "".join(f'<p>{k}. {D.mq(q["q"])}</p>{ans((letter(EXIT, k) + ". " + q["choices"][0]) if q.get("choices") else q["answer"], True)}' for k, q in enumerate(EXIT, 1))
    s.append(sec("Exit Ticket", "Show what you know", f'<div class="col" style="gap:8px;font-size:24px">{ex}</div>',
                 "Printed copy: EXIT TICKET/T2-Exit-Ticket-Mon-11-02.pdf. 5 minutes. Anyone who misses 2 or more gets a reminders card for the test. "
                 + " ".join(f"{k}. {q['why']}" for k, q in enumerate(EXIT, 1))))
    name = "t2-test-review-slides"
    head = re.sub(r"<title>.*?</title>", "<title>Topic 2 Test Review</title>", D.HEAD, count=1)
    path = OUT / f"{name}.html"
    path.write_text(head + '<div id="stage">\n\n' + "\n".join(s) + D.TAIL, encoding="utf-8")
    r = subprocess.run([sys.executable, str(ROOT / "make_pptx.py"), path.relative_to(ROOT).as_posix()], capture_output=True, text=True)
    print("slides:", (r.stdout.strip().splitlines() or ["?"])[-1])
    for l in r.stdout.splitlines():
        if "WARNING" in l:
            print("  ", l)


# ------------------------------------------------------------------ lesson plan
def agenda_deck(name, title, eyebrow, h, items, end, color, notes):  # one projector slide
    body = ('<div class="col" style="gap:14px;font-size:28px">' + "".join(
        f'<p style="margin:0"><b style="display:inline-block;width:46px;height:46px;line-height:46px;text-align:center;border-radius:50%;background:{color};color:#fff;margin-right:14px">{n}</b>'
        f'<b>{t}</b> · {w}</p>' for n, (t, w) in enumerate(items, 1)) + f'</div><p style="font-size:36px;margin-top:20px;text-align:center"><b>{end}</b></p>')
    head = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", D.HEAD, count=1)
    path = OUT / f"{name}.html"
    path.write_text(head + '<div id="stage">\n\n' + sec(eyebrow, h, body, notes) + D.TAIL, encoding="utf-8")
    r = subprocess.run([sys.executable, str(ROOT / "make_pptx.py"), path.relative_to(ROOT).as_posix()], capture_output=True, text=True)
    print(name, (r.stdout.strip().splitlines() or ["?"])[-1])


def test_day():
    agenda_deck("t2-test-day-agenda", "Test Day Agenda", "Tuesday, November 3 · Test Day", "📝 Topic 2 Test · Today’s Agenda",
                [("Clear your desk", "Only a pencil stays out."), ("Chromebook ready", "You will enter your answers on it."),
                 ("Calculator + formula sheet", "Get them now."), ("Take the test", "10 questions. Read carefully, check your work.")],
                "Good luck! You’ve got this! 🍀", "#b00020", "Leave this up as students walk in. Same for all 6 periods. Retakes Wed Nov 4.")


def retake_day():
    agenda_deck("t2-retake-day-agenda", "Retake Day Agenda", "Wednesday, November 4 · Retake Day", "🔁 Retake Day · Today’s Agenda",
                [("Retaking? Get set up", "Clear desk, Chromebook ready, calculator + formula sheet."),
                 ("Not retaking? Lesson 4", "Comparing Linear Functions: slides, then the homework on your Chromebook."),
                 ("Quiet room", "Work silently so retakers can focus. Raise your hand for help."),
                 ("Done early?", "Take the Lesson 4 quiz.")],
                "Second chance, best effort! 💪", "#1f8a4c", "Leave this up as students walk in. Same for all 6 periods. Module 3 Topic 1 starts Thu Nov 5.")


def plan():
    A_ = PL.A
    d = dict(file=DATE, date="Monday, November 2", lesson="Topic 2 Review (test Tue Nov 3)",
             obj=["Practice every question type on the End of Topic 2 Assessment, in test order.", "Fix the two biggest errors: inside vs. outside shifts and domain vs. range.",
                  "Write parallel and perpendicular lines through a point, and read zeros and slopes from graphs."],
             teks=["<b>A.2C</b>, <b>A.3C</b> (readiness), A.2A, A.2E, A.2F, A.2G, A.3E"],
             terms="translation · dilation · domain · range · parallel · perpendicular · zero · point-slope form",
             mat=["Topic 2 Review Test: assessment/M2 TOPIC 2/Topic2-Review-Test.pdf + key (IEP and 504 versions)",
                  "Slides: Module 2 topic 2/t2-test-review-slides (.html/.pptx) · online self-check: t2-test-review.html",
                  f"Bell work and exit ticket: BELL WORK/T2-Bell-Work-{DATE}.pdf, EXIT TICKET/T2-Exit-Ticket-{DATE}.pdf + keys (IEP/504 too)",
                  "Test Review 2 for early finishers: REVIEW/T2-Review-2.pdf + key (IEP/504), online t2-test-review-2.html",
                  "Whiteboards, index cards (test tips)"],
             bell=[(re.sub(r"\[\[|\]\]", "", q["q"]), f"{letter(BELL, k)}. {q['choices'][0]}") for k, q in enumerate(BELL, 1)],
             rows=[("0–5", "Agenda + bell work", "Welcome-back agenda (slide 2) up as they walk in. Four test warm-ups (slide 3). Hand out the printed review."),
                   ("5–15", "I do · Review Q1–3", "Q1 " + A_("a = −2/3") + " Q2 " + A_("C. 75 ≤ y ≤ 175") + " Q3 " + A_("H. y = −20; slope zero") + "<br>Model crossing out the domain choices on Q2."),
                   ("15–32", "We do · Q4–8 (pairs, whiteboards)", "Q4 " + A_("C. right 3") + " Q5 " + A_("−7") + " Q6 " + A_("g(x) = 2x") + " Q7 " + A_("y = −2/3x − 4") + " Q8 " + A_("y = −2.4x + 12")
                    + "<br>Re-teach any item under 70% on the spot."),
                   ("32–45", "You do · Q9–10 (silent, test conditions)", "Q9 " + A_("y − 5 = 2(x − 2)") + " Q10 " + A_("F and J") + "<br>Pull a small group for Q4–6 (transformations)."),
                   ("45–53", "Extra practice", "Q11–14, then <b>Test Review 2</b> (REVIEW/T2-Review-2.pdf or t2-test-review-2.html) for anyone finished. " + PL.IEP),
                   ("53–58", "Exit ticket + test tips card", "1. " + A_(f"{letter(EXIT, 1)}. x = −7; slope undefined") + " 2. " + A_("y = 5x + 5") + " 3. " + A_("7")
                    + "<br>Students copy the 6 test tips (last slide) on an index card."),
                   ("58–60", "Wrap up", "Test tomorrow: 10 questions, same order as the review. Bring a pencil and calculator.")],
             cfu=["Whiteboards on Q4–8; re-teach any item under 70%.", "Exit ticket: 2 or more wrong → reminders card on test day."],
             after=["Sort exit tickets: who needs a reminders card or small-group seating tomorrow.", "Retakes Wed Nov 4: use the real test key's item analysis page."],
             note="The printed review mirrors the publisher End of Topic 2 Assessment item for item (same skill, format and order; new numbers).")
    html = PL.page(d).replace("Module 3, Topic 1", "Module 2, Topic 2")
    src = OUT / "LESSON PLANS" / f"T2-Lesson-Plan-{DATE}.html"
    import fitz
    for size in ("9.3pt", "8.8pt", "8.3pt"):
        src.write_text(html.replace("font-size:9.3pt", f"font-size:{size}"), encoding="utf-8")
        subprocess.run([EDGE, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={src.with_suffix('.pdf')}", src.as_uri()],
                       check=True, capture_output=True)
        if len(fitz.open(src.with_suffix(".pdf"))) == 1:
            break
    src.unlink()
    print("plan", size)


if __name__ == "__main__":
    sheets()
    online()
    review2()
    test_day()
    retake_day()
    deck()
    plan()

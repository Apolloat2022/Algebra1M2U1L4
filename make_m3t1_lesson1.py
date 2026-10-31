"""Module 3 Topic 1 Lesson 1 (Solving Linear Equations, Thu Nov 5): slide deck, online bell work, printable bell work +
exit ticket (with keys), narrated video. Bell work and exit ticket items are written like the End of Topic 1 Assessment
(materials/Secondary Mathematics Algebra Module 3 Topic 1 Assements Student Edition.pdf): Lesson 1 there is Q2, Q4, Q5, Q11.
Run:  python make_m3t1_lesson1.py [video]      then  python make_pptx.py "Module 3 topic 1/m3t1-lesson1-solving-linear-equations.html" """
import re, subprocess, sys
from pathlib import Path

import make_t2_decks as D
import make_t2_practice as MP

ROOT = Path(__file__).parent
OUT = ROOT / "Module 3 topic 1"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
STEM = "m3t1-lesson1-solving-linear-equations"
BELL_PAGE = "m3t1-lesson1-bellwork.html"
M, mt, eq, ans, st, p, sec, row, card, table = D.M, D.mt, D.eq, D.ans, D.st, D.p, D.sec, D.row, D.card, D.table

# ---------------------------------------------------------------- items (first choice = correct; pos = its printed slot)
BELL = [
    MP.Q("Marcus has $35 and saves $15 per week. Which equation gives the amount he has saved, [[y]], after [[x]] weeks?",
         ["[[y = 15x + 35]]", "[[y = 35x + 15]]", "[[y = −15x + 35]]", "[[y = 50x]]"],
         "Start at $35 ([[b]]) and add $15 each week ([[m]]): [[y = 15x + 35]]. Like test Q1."),
    MP.T("What value of [[x]] makes [[3(x − 2) = 12]] true?", ["[[6]]", "[[4⅔]]", "[[2]]", "[[10]]"],
         "Distribute: [[3x − 6 = 12]], so [[3x = 18]] and [[x = 6]]. 4⅔ forgets to multiply the 2."),
    MP.Q("Is [[x = 2]] a solution of [[5x − 1 = 9]]?", ["Yes, because [[9 = 9]]", "No, because [[10 ≠ 9]]", "Yes, because [[x = 9]]", "No, because [[11 ≠ 9]]"],
         "Substitute: [[5(2) − 1 = 10 − 1 = 9]]. A true statement means 2 is a solution."),
    MP.T("Which expression is equivalent to [[4(x + 2) − x]]?", ["[[3x + 8]]", "[[3x + 2]]", "[[5x + 8]]", "[[4x + 6]]"],
         "Distribute: [[4x + 8 − x = 3x + 8]]."),
]
BELL_POS = [1, 2, 0, 3]
EXIT = [  # (kind, stem, choices or None, answer, work)
    ("mc", "What value of [[p]] makes the equation [[7 − 3(p + 2) = 10 − (2p + 5)]] true?", ["[[−4]]", "[[4]]", "[[−6]]", "No solution"], 0,
     "[[1 − 3p = 5 − 2p]] → [[−p = 4]] → [[p = −4]]"),
    ("open", "Solve the equation shown.<br>[[0.5(4x − 6) = −1.5x + 4]]", None, "[[x = 2]]",
     "[[2x − 3 = −1.5x + 4]] → [[3.5x = 7]] → [[x = 2]]"),
    ("open", "Does the equation shown below have one solution, no solution, or an infinite number of solutions? Explain your reasoning.<br>"
             "[[½(8x + 6) = 2(2x + 1) + 2]]", None, "No solution",
     "[[4x + 3 = 4x + 4]]: same [[x]]-coefficient, different constants, so [[3 = 4]] is never true"),
    ("open", "A triangle has a height of [[(x + 5)]] inches and a base of 6 inches. A rectangle has a length of 4 inches and a width of "
             "[[(x − 1)]] inches. The area of the triangle equals the area of the rectangle. What is the value of [[x]]?", None, "[[x = 19]]",
     "[[½(6)(x + 5) = 4(x − 1)]] → [[3x + 15 = 4x − 4]] → [[x = 19]]"),
]
EXIT_LIKE = "Like test Q2, Q4, Q5 and Q11."


def mq(s):
    return D.mq(s)


# ---------------------------------------------------------------- slide deck
def title_slide():
    bw = f'<b><a class="go" href="{BELL_PAGE}" {D.GO}>Bell work →</a></b>'
    return (f'<section class="slide">\n  <p class="eyebrow">Bluebonnet Algebra I · Module 3 · Topic 1 · Lesson 1 · Student Edition pp. 345–356</p>\n'
            f'  <h1 style="margin-top:6px;font-size:56px">Solving Linear Equations</h1>\n  <div class="eq" style="margin-top:8px;font-size:40px">'
            f'one solution · no solution · infinite solutions</div>\n  <p style="font-size:24px;margin-top:6px">{bw}</p>\n'
            f'  <p class="muted small">Click, or press → / Space, to reveal each step. ← goes back. F = full screen.</p>\n  {D.FOOT}\n'
            '  <aside class="notes">One day on the 150-day calendar (Thu Nov 5): Getting Started, Activities 1.1 and 1.2 (all starred). '
            'Activity 1.3 Tic-Tac-Bingo is not starred and is saved for the Nov 19 retake day. Talk the Talk is included as a short test-style '
            'area problem because it matches End of Topic Assessment question 11.</aside>\n</section>\n')


def deck():
    MP.BELL[("m3l1", 1)] = BELL  # D.bell reads the same dict
    s = [title_slide(), D.bell("m3l1", 1, "Review")]
    s.append(D.today(1, 345, ["Write equivalent equations using properties of equality.",
                              "Use properties of equality to solve linear equations and justify a solution method.",
                              "Determine whether an equation has one solution, no solution, or infinite solutions.",
                              "Solve linear equations with variables on both sides."], "New key terms: solution · no solution · infinite solutions"))
    s.append(D.eq_slide(1, 345, "You know that equations are one way to represent a linear function.",
                        "How can you use equations to solve for unknown input values of a function?"))
    s.append(sec("Getting Started · Equation Creation · SE p. 346", f"Build harder equations from {mt('x = 2')}",
                 row(p("A <b>solution</b> to an equation is a value for the variable that makes the equation a true statement.", "")
                     + st("a. Add 3 to each side: " + mt("x + 3 = 5"))
                     + st("b. Multiply each side by 4: " + mt("4x + 12 = 20"))
                     + st("c. Subtract " + mt("2x") + ": " + mt("2x + 12 = −2x + 20"))
                     + st("d. Divide each side by 2: " + mt("x + 6 = 10 − x")),
                     card("2. Partner check", p("Substitute 2 into your partner's last equation.") + ans("2 + 6 = 10 − 2 → 8 = 8 ✓")
                          + st("Same operation on <b>both</b> sides, to <b>every</b> term, keeps the solution.", "small muted"))),
                 "Getting Started, 15 minutes. Look for students who multiply or divide only the x-term instead of every term (TE common misconception). Algebra tiles help."))
    s.append(sec("Activity 1.1 · Using Properties to Justify Solutions · SE p. 347", "Properties of equality",
                 table(["Property", "For all numbers a, b, and c"], [["addition", M("If a = b, then a + c = b + c.")], ["subtraction", M("If a = b, then a − c = b − c.")],
                                                                     ["multiplication", M("If a = b, then ac = bc.")], ["division", M("If a = b and c ≠ 0, then a/c = b/c.")]], 26)
                 + st("These rules keep both sides balanced while you isolate the variable."),
                 "Explicit instruction. TE suggestion: make a poster of both property tables; Lessons 2 and 3 use them again."))
    s.append(sec("Activity 1.1 · Question 1 · SE p. 347", "Harper and Sofia both started from " + mt("x = 2"),
                 row(card("Harper", eq("−3x + 14 = 18 − 5x", "sm") + st("Substitute: " + mt("−6 + 14 = 18 − 10")) + ans("8 = 8 ✓")
                          + st("Properties: add " + mt("5x") + ", subtract 14 → " + mt("2x = 4") + " → " + mt("x = 2"))),
                     card("Sofia", eq("2x = 5 − ½x", "sm") + st("Substitute: " + mt("4 = 5 − 1")) + ans("4 = 4 ✓")
                          + st("Properties: add " + mt("½x") + " → " + mt("5/2 x = 5") + ", multiply by " + mt("2/5") + " → " + mt("x = 2"))), gap=24),
                 "Question 1. Assistance for All: multiply Sofia's equation by 2 first to clear the fraction (4x = 10 − x)."))
    s.append(sec("Activity 1.1 · Question 2 · SE p. 348", "Solve, check, and name each property",
                 row(eq("b. &nbsp;0.6(2x + 1) = 4x + 6.2", "sm") + st(mt("1.2x + 0.6 = 4x + 6.2") + " &nbsp;distributive")
                     + st(mt("−2.8x + 0.6 = 6.2") + " &nbsp;subtraction") + st(mt("−2.8x = 5.6") + " &nbsp;subtraction") + ans("x = −2 &nbsp; (division)", True),
                     eq("c. &nbsp;½x − 6 = 2 + (2x + 1)", "sm") + st(mt("½x − 6 = 3 + 2x") + " &nbsp;commutative, associative")
                     + st(mt("−9 = 3/2 x") + " &nbsp;subtraction") + ans("x = −6 &nbsp; (multiplication by ⅔)", True)),
                 "Number properties (commutative, associative, distributive) are on SE p. 348. Check b: 0.6(−3) = −1.8 and 4(−2) + 6.2 = −1.8. "
                 "Questions 2 and 3 are the TE's check point; for more practice assign Skills Practice Set A."))
    s.append(sec("Activity 1.1 · Question 3 · SE p. 349", "Daniel and Chloe: same equation, different first step",
                 row(card("Daniel", eq("4(3x + 2) = 8x + 4", "sm") + st(mt("12x + 8 = 8x + 4") + " distributive first") + st(mt("4x = −4")) + ans("x = −1")),
                     card("Chloe", eq("4(3x + 2) = 8x + 4", "sm") + st(mt("3x + 2 = 2x + 1") + " divide by 4 first") + st(mt("x = −1")) + ans("x = −1")), gap=24)
                 + st("More than one correct path. Both finish with subtraction and division properties."),
                 "Ask: Why do you think Chloe chose 4 as the divisor? Whose method do you prefer?"))
    s.append(sec("Activity 1.2 · Solutions to Linear Equations · SE pp. 349–350", "Can you change the truth of a sentence?",
                 row(card("1. " + mt("2 = 2"), st("Add " + mt("x") + ": " + mt("2 + x = 2 + x")) + st("Multiply by 5: " + mt("10 + 5x = 10 + 5x")) + st("Still always true.")),
                     card("2. " + mt("2 = 3"), st("Add " + mt("x") + ": " + mt("2 + x = 3 + x")) + st("Multiply by 5: " + mt("5(2 + x) = 5(3 + x)")) + st("Still always false.")), gap=24)
                 + st("<b>No solution</b>: no value makes the equation true. <b>Infinite solutions</b>: every value makes it true."),
                 "Questions 1–3. Common misconception: 8 = 8 does not mean x = 8; it means the value we substituted works."))
    s.append(sec("Activity 1.2 · Question 4 + Seeing Structure", "Simplify each side, then compare",
                 table(["Equation", "Simplified", "Solutions"], [[M("2x + 5 = 2x + 5"), "same coefficient, same constant", "<b>infinite</b>"],
                                                                [M("2x + 5 = 2x + 7"), "same coefficient, different constant", "<b>none</b>"],
                                                                [M("2x + 5 = 3x + 5"), "different coefficients", M("one: x = 0")],
                                                                [M("2x = 3x"), "different coefficients", M("one: x = 0")]], 24, (2,)),
                 "Question 4 and the TE's Seeing Structure questions. Stamp the learning: a linear equation has one solution, no solution, or infinite solutions. "
                 "Question 3 is the TE's check point; Skills Practice Set B."))
    s.append(sec("Test Practice · Like End of Topic Questions 2 and 5", "Which kind of solution?",
                 row(p("1. What value of " + mt("m") + " makes " + mt("6 − 4(m + 2) = 3 − 2(2m + 1)") + " true?", "")
                     + st(mt("−4m − 2 = −4m + 1")) + ans("No solution (−2 ≠ 1)", True),
                     p("2. One solution, no solution, or infinite? " + mt("¼(8x + 12) = 2(x + 2) − 1"), "")
                     + st(mt("2x + 3 = 2x + 3")) + ans("Infinite solutions: the two sides are equivalent", True)),
                 "Added for this deck; not from the textbook. On the test, 'No solution' is a real answer choice: simplify both sides before guessing."))
    s.append(sec("Talk the Talk · One Step at a Time · SE p. 352", "Equal areas (like test question 11)",
                 row(p("Rectangle A: width " + mt("(5 + 2x)") + " in., length 6 in. Rectangle B: width 8 in., length " + mt("(x + 5)") + " in. Same area. Find " + mt("x") + ".", "")
                     + eq("6(5 + 2x) = 8(x + 5)", "sm", True),
                     st(mt("30 + 12x = 8x + 40") + " &nbsp;distributive") + st(mt("12x = 8x + 10") + " &nbsp;subtraction")
                     + st(mt("4x = 10") + " &nbsp;subtraction") + ans("x = 2.5 &nbsp; (division)", True)),
                 "Not starred; included because End of Topic question 11 is the same kind of problem (triangle area = rectangle area). Skip if short on time."))
    s.append(sec("Essential Question · Answered", "How can you use equations to solve for unknown inputs?",
                 '<div class="col" style="gap:20px;margin-top:6px">'
                 + st("Use properties of equality to isolate the variable, and name the property for each step.", "")
                 + st("Simplify each side first. Same coefficient and constant: infinite. Same coefficient, different constant: none. Otherwise: one solution.", "")
                 + "</div>", "Have students answer the Essential Question on the lesson opener page."))
    short = ["Solve: [[7 − 3(p + 2) = 10 − (2p + 5)]]", "Solve: [[0.5(4x − 6) = −1.5x + 4]]",
             "One, none, or infinite? [[½(8x + 6) = 2(2x + 1) + 2]]", "Triangle: base 6, height [[(x + 5)]]. Rectangle: 4 by [[(x − 1)]]. Equal areas. Find [[x]]."]
    s.append(D.exit_ticket([(mq(sh), mq(ch[a]) if ch else mq(a)) for sh, (_, _, ch, a, _) in zip(short, EXIT)],
                           " ".join(f"{k}. {re.sub(r'\[\[|\]\]', '', w)}." for k, (*_, w) in enumerate(EXIT, 1)) + " " + EXIT_LIKE))
    s.append(sec("Homework", "Lesson 1 Assignment · SE pp. 355–356",
                 row(card("Practice", p("1a–e: solve and write the property for each step.") + p("2a–f: one solution, no solution, or infinite?")),
                     card(f'<a class="go" href="{BELL_PAGE}" {D.GO}>Bell work →</a>', p("Today's 4 warm-up questions online, scored on submit."))),
                 "Practice 2 answers: a none, b x = 7, c x = 2, d infinite, e none, f infinite."))
    return s


def write_deck():
    D.STARS["m3l1"] = {"Getting Started", "1.1", "1.2"}
    secs = [D.star_eyebrows("m3l1", x) for x in deck()]
    head = re.sub(r"<title>.*?</title>", "<title>Solving Linear Equations · Bluebonnet Algebra I</title>", D.HEAD, count=1)
    (OUT / f"{STEM}.html").write_text(head + '<div id="stage">\n\n' + "\n".join(secs) + D.TAIL, encoding="utf-8")
    print(f"{STEM}.html", len(secs), "slides")


# ---------------------------------------------------------------- printable bell work + exit ticket (student copy and key)
CSS = """@page{size:letter;margin:.5in}body{font-family:Lato,Segoe UI,Arial,sans-serif;font-size:12pt;color:#111;margin:0}
.top{background:#e6f1ea;padding:6px 10px;font-size:15pt}.top b{color:#0b6b3a;font-size:10pt;letter-spacing:.5px}
.hdr{display:flex;justify-content:space-between;font-size:9pt;color:#444;margin-bottom:4px}
.nm{margin:10px 0 14px}.grid{display:grid;grid-template-columns:1fr 1fr;gap:0 26px}
.it{min-height:3.1in;break-inside:avoid;padding-top:6px}.it.mc{min-height:2.4in}.ch{margin:8px 0 0 18px}.ch div{margin:7px 0}
.ans{color:#b00000;font-weight:600}.why{color:#b00000;font-size:10pt;margin-top:6px}i{font-family:'STIX Two Text',serif}"""


def plain(s):
    return re.sub(r"\[\[(.+?)\]\]", lambda m: M(m.group(1)), s)


def sheet(fname, what, items, key):
    """items: (num, stem, choices_in_print_order | None, letters, answer_html, why)"""
    blocks = []
    for n, stem, ch, letters, a, why in items:
        b = f'<div class="it{" mc" if ch else ""}"><b>{n}.</b> {plain(stem)}'
        if ch:
            b += '<div class="ch">' + "".join(f'<div><b>{letters[k]}.</b> <span class="{"ans" if key and c == a else ""}">{plain(c)}</span></div>' for k, c in enumerate(ch)) + "</div>"
        elif key:
            b += f'<div class="ans" style="margin-top:8px">{plain(a)}</div>'
        if key and why:
            b += f'<div class="why">{plain(why)}</div>'
        blocks.append(b + "</div>")
    html = (f'<!doctype html><html><head><meta charset="utf-8"><title>{fname}</title><style>{CSS}</style></head><body>'
            f'<div class="hdr"><span>MODULE 3 • TOPIC 1 • LESSON 1 • {what.upper()}</span><span>{"ANSWER KEY" if key else ""}</span></div>'
            f'<div class="top"><b>TOPIC 1</b> Linear Equations and Inequalities</div>'
            f'<div class="nm">Name ____________________________ &nbsp; Date __________</div><div class="grid">{"".join(blocks)}</div></body></html>')
    src = OUT / what / f"{fname}.html"
    src.parent.mkdir(exist_ok=True)
    src.write_text(html, encoding="utf-8")
    subprocess.run([EDGE, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={src.with_suffix('.pdf')}", src.as_uri()],
                   check=True, capture_output=True)
    src.unlink()  # the PDF is the deliverable; this script is the source
    print(src.with_suffix(".pdf").name)


def printed(q, pos):
    ch = q["choices"][1:]
    ch.insert(pos, q["choices"][0])
    return ch


def write_sheets():
    bell = [(k, q["q"], printed(q, pos), q.get("letters", "ABCD"), q["choices"][0], q["why"]) for k, (q, pos) in enumerate(zip(BELL, BELL_POS), 1)]
    ex = [(k, stem, ch, "FGHJ", ch[a] if ch else a, w) for k, (_, stem, ch, a, w) in enumerate(EXIT, 1)]
    for key in (False, True):
        sfx = "-ANSWER-KEY" if key else ""
        sheet(f"T1-Bell-Work-Thu-11-05{sfx}", "BELL WORK", bell, key)
        sheet(f"T1-Lesson1-Exit-Ticket{sfx}", "EXIT TICKET", ex, key)


# ---------------------------------------------------------------- video
SCENES = [  # (title, [(caption, new line or None, reason or None)])
    ("Solving Linear Equations", [
        ("A solution to an equation is a value for the variable that makes the equation true.", None, None),
        ("Today: solve equations, name the property for each step, and tell whether an equation has one, no, or infinite solutions.", None, None)]),
    ("Build equations from x = 2", [
        ("Start with the simplest equation: x equals 2.", "x = 2", None),
        ("Add 3 to each side.", "x + 3 = 5", "addition"),
        ("Multiply each side by 4. Every term gets multiplied.", "4x + 12 = 20", "multiplication"),
        ("Subtract 2x from each side.", "2x + 12 = −2x + 20", "subtraction"),
        ("Each equation still has the solution 2, because we did the same thing to both sides. PAUSE 1", None, None)]),
    ("Solve and justify", [
        ("Solve 0.6 times the quantity 2x plus 1 equals 4x plus 6.2.", "0.6(2x + 1) = 4x + 6.2", None),
        ("Distribute the 0.6.", "1.2x + 0.6 = 4x + 6.2", "distributive"),
        ("Subtract 4x from both sides.", "−2.8x + 0.6 = 6.2", "subtraction"),
        ("Subtract 0.6 from both sides.", "−2.8x = 5.6", "subtraction"),
        ("Divide both sides by negative 2.8.", "x = −2", "division"),
        ("Check: 0.6 times negative 3 is negative 1.8, and 4 times negative 2 plus 6.2 is also negative 1.8. PAUSE 1", None, None)]),
    ("Decimals on both sides", [
        ("Here is one like the test: 0.2 times the quantity 5x plus 5 equals negative 3x plus 9.", "0.2(5x + 5) = −3x + 9", None),
        ("Distribute.", "x + 1 = −3x + 9", "distributive"),
        ("Add 3x to both sides.", "4x + 1 = 9", "addition"),
        ("Subtract 1.", "4x = 8", "subtraction"),
        ("Divide by 4. x equals 2. PAUSE 1", "x = 2", "division")]),
    ("One, none, or infinite?", [
        ("Simplify each side first, then compare.", None, None),
        ("One half times the quantity 4x plus 10 equals 2 times the quantity x plus 1, plus 3.", "½(4x + 10) = 2(x + 1) + 3", None),
        ("Both sides become 2x plus 5. They are the same expression, so every value works: infinite solutions.", "2x + 5 = 2x + 5", "infinite"),
        ("3 times the quantity x minus 2, plus 1, equals 3x plus 4.", "3(x − 2) + 1 = 3x + 4", None),
        ("3x minus 5 equals 3x plus 4. Same x term, different constants: that is never true. No solution.", "3x − 5 = 3x + 4", "no solution"),
        ("2x plus 7 equals 5x plus 7. Different x terms, so there is one solution: x equals 0. PAUSE 1", "2x + 7 = 5x + 7 → x = 0", "one solution")]),
    ("Equal areas", [
        ("A triangle has base 10 and height x plus 2. A rectangle is 4 by x plus 8. The areas are equal.", None, None),
        ("Triangle area is one half base times height. Set it equal to the rectangle's area.", "½(10)(x + 2) = 4(x + 8)", None),
        ("Simplify both sides.", "5x + 10 = 4x + 32", "distributive"),
        ("Subtract 4x and subtract 10.", "x = 22", "subtraction"),
        ("Remember: properties of equality keep both sides balanced, and simplifying first tells you how many solutions to expect. PAUSE 2", None, None)]),
]


def write_video():
    import make_t2_video as V
    from PIL import Image, ImageDraw
    import os, tempfile
    out_dir = OUT / "videos"
    out_dir.mkdir(exist_ok=True)
    out = out_dir / "M3T1-Lesson1-Solving-Linear-Equations.mp4"
    tmp = tempfile.mkdtemp()
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{V.W}x{V.H}", "-r", str(V.FPS),
                           "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "26", os.path.join(tmp, "v.mp4")], stdin=subprocess.PIPE)
    wavs, n = [], 0
    for title, steps in SCENES:
        lines = []
        for cap, line, why in steps:
            if line: lines.append((line, why))
            img = Image.new("RGB", (V.W, V.H), "white")
            d = ImageDraw.Draw(img)
            d.rectangle([0, 0, V.W, 84], fill="#e6f1ea")
            d.text((40, 20), title, font=V.FB[44], fill="#0b6b3a")
            y = 120
            for k, (ln, rs) in enumerate(lines[-8:]):
                new = k == len(lines[-8:]) - 1 and line is not None
                d.text((80, y), ln, font=V.FB[44] if new else V.F[34], fill=V.BLUE if new else V.INK)
                if rs: d.text((760, y + 6), rs, font=V.F[34], fill=V.GREEN)
                y += 58
            d.rectangle([0, V.H - 130, V.W, V.H], fill="#f4f6fa")
            for j, w in enumerate(V.wrap(d, re.sub(r"\s*PAUSE \d+", "", cap), V.F[34], V.W - 120)[:3]):
                d.text((60, V.H - 118 + j * 38), w, font=V.F[34], fill=V.INK)
            wav = os.path.join(tmp, f"s{n:03d}.mp3"); n += 1
            dur = V.speak(V.spoken(cap), wav) + 0.6
            m = re.search(r"PAUSE (\d+)", cap)
            nf = round((dur + (float(m.group(1)) if m else 0)) * V.FPS)
            wavs.append((wav, nf / V.FPS))
            ff.stdin.write(img.tobytes() * nf)
    ff.stdin.close(); ff.wait()
    lst = os.path.join(tmp, "a.txt")
    with open(lst, "w") as fh:
        for i, (wav, slot) in enumerate(wavs):
            pad = os.path.join(tmp, f"p{i:03d}.wav")
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-af", f"apad=whole_dur={slot:.3f}", "-ar", "22050", "-ac", "1", pad], check=True)
            fh.write(f"file '{pad}'\n")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(tmp, "v.mp4"), "-f", "concat", "-safe", "0", "-i", lst,
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "96k", "-shortest", "-movflags", "+faststart", str(out)], check=True)
    print(out.name, f"{sum(s for _, s in wavs):.0f} s")


if __name__ == "__main__":
    for q in BELL:
        assert len(set(q["choices"])) == 4, q["q"]
    MP.OUT = OUT
    MP.page(BELL_PAGE, "Topic 1 Lesson 1 Bell Work · Solving Linear Equations", "Module 3 · Topic 1 · Lesson 1 · Bell Work", "Bell Work: Review",
            "Warm up while attendance is taken. Answer all 4 questions, then submit to see which ones you got right.", "quiz", BELL)
    write_deck()
    write_sheets()
    if "video" in sys.argv:
        write_video()

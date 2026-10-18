"""Writes the Topic 2 web lesson decks (same engine as lesson6's deck) into 'Module 2 topic 2/'.
Run:  python make_t2_decks.py   then make_pptx.py on each deck, and make_accom_lessons.py t2 for the IEP / 504 versions."""
import json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from make_t2_practice import BELL  # the bell work questions, shown on the deck's bell work slides too

ROOT = Path(__file__).parent
SRC = (ROOT / "lesson6/making-sense-of-representations-lesson6.html").read_text(encoding="utf-8")
HEAD = SRC.split('<div id="stage">', 1)[0]
TAIL = SRC[SRC.index('\n</div>\n\n<nav id="bar"'):]


def M(s):  # math text: every letter is an italic variable
    return re.sub(r"&\w+;|<[^>]+>|[A-Za-z]", lambda m: m.group(0) if len(m.group(0)) > 1 else f"<i>{m.group(0)}</i>", s)


def mt(s, cls=""):
    return f'<span class="mt{" " + cls if cls else ""}">{M(s)}</span>'


def eq(s, cls="", step=False):
    return f'<div class="eq{" " + cls if cls else ""}{" step" if step else ""}">{M(s)}</div>'


def ans(s, raw=False):
    return f'<div class="step pop eq sm ans">{s if raw else M(s)}</div>'


def st(s, cls="small"):
    return f'<p class="step {cls}">{s}</p>'


def p(s, cls="small"):
    return f'<p class="{cls}">{s}</p>'


def sec(eyebrow, title, body, notes="", divider=False):
    return (f'<section class="slide{" divider" if divider else ""}">\n  <p class="eyebrow">{eyebrow}</p>\n  '
            + (f"<h1>{title}</h1>" if divider else f"<h2>{title}</h2>") + f"\n  {body}\n"
            + (f'  <aside class="notes">{notes}</aside>\n' if notes else "") + "</section>\n")


def row(*cols, gap=40):
    return f'<div class="row" style="gap:{gap}px">' + "".join(f'<div class="col" style="gap:10px">{c}</div>' for c in cols) + "</div>"


def card(h, body, step=False):
    return f'<div class="card{" step" if step else ""}"><h3>{h}</h3>{body}</div>'


def graph(w, h, x, y, gx, gy, lines=(), pts=(), alt="", pts_step=False):
    g = dict(w=w, h=h, x=x, y=y, gx=gx, gy=gy, lines=list(lines), pts=list(pts), alt=alt)
    if pts_step:
        g["ptsStep"] = True
    return "<div class=\"graph\" data-g='" + json.dumps(g, ensure_ascii=False).replace("'", "&#39;") + "'></div>"


def L(p1, p2, label=None, c=None, step=False, dash=False, seg=False):
    d = {"p": [list(p1), list(p2)]}
    if label: d["label"] = label
    if c: d["c"] = c
    if step: d["step"] = True
    if dash: d["dash"] = True
    if seg: d["seg"] = True
    return d


def table(head, rows, size=26, steps=()):  # steps: column indexes revealed cell by cell
    h = "".join(f"<th>{c}</th>" for c in head)
    body = "".join("<tr>" + "".join(f'<td{" class=\"step\"" if j in steps else ""}>{c}</td>' for j, c in enumerate(r)) + "</tr>" for r in rows)
    return f'<table class="tbl" style="font-size:{size}px"><tr>{h}</tr>{body}</table>'


GO = 'target="_blank" onclick="event.stopPropagation()"'


def links(n, days):
    bw = " · ".join(f'<b><a class="go" href="t2-lesson{n}-bellwork-day{d}.html" {GO}>Day {d} →</a></b>' for d in range(1, days + 1))
    return (f'<p style="font-size:24px;margin-top:6px">Bell work: {bw} &nbsp;|&nbsp; Practice: '
            f'<b><a class="go" href="t2-lesson{n}-homework.html" {GO}>Homework →</a></b> · '
            f'<b><a class="go" href="t2-lesson{n}-quiz.html" {GO}>Quiz →</a></b></p>')


FOOT = ('<p class="foot"><strong>Bluebonnet Algebra I</strong> · a companion to Bluebonnet Learning Secondary Mathematics, Algebra I, Edition 1<br>'
        'This work is based on original works of the Texas Education Agency and Carnegie Learning, Inc. This work is made available under a Creative Commons '
        'Attribution-Non-Commercial-4.0 International License. This does not in any way imply endorsement by those authors of this work.<br>'
        '©2024–2025 Texas Education Agency, portions ©2021 Carnegie Learning, Inc.<br>Licensed <a href="https://creativecommons.org/licenses/by-nc/4.0/" '
        f'rel="license" {GO}>CC BY-NC 4.0</a>.<br><strong>This is a private site for Algebra I teachers and is not publicly available.</strong></p>')


def title(n, pages, name, formula, days, notes):
    return (f'<section class="slide">\n  <p class="eyebrow">Bluebonnet Algebra I · Module 2 · Topic 2 · Lesson {n} · Student Edition pp. {pages}</p>\n'
            f'  <h1 style="margin-top:6px;font-size:56px">{name}</h1>\n  <div class="eq" style="margin-top:8px;font-size:40px">{formula}</div>\n'
            f'  {links(n, days)}\n  <p class="muted small">Click, or press → / Space, to reveal each step. ← goes back. F = full screen.</p>\n'
            f'  {FOOT}\n  <aside class="notes">{notes}</aside>\n</section>\n')


def mq(s):  # bell work text uses [[math]] like the practice pages
    return re.sub(r"\[\[(.+?)\]\]", lambda m: mt(m.group(1)), s)


def bell(n, d, what):
    qs = BELL[(n, d)]
    item = lambda k, q: (f'<p{" style=\"margin-top:14px\"" if k % 2 else ""}>{k + 1}. {mq(q["q"])}'
                         + (f' <span class="muted" style="font-size:21px">(SE p. {q["se"]})</span>' if q.get("se") else "")
                         + f'</p>\n      <div class="step pop eq sm ans">{mq(q["choices"][0])}</div>')
    cols = "".join(f'\n    <div class="col">\n      {item(k, qs[k])}\n      {item(k + 1, qs[k + 1])}\n    </div>' for k in (0, 2))
    key = " ".join(f"{k}. " + q["why"].replace("[[", "").replace("]]", "") for k, q in enumerate(qs, 1))
    return (f'<section class="slide">\n  <p class="eyebrow">Day {d} · Bell Work · {what}</p>\n  <h2>Warm up: work these on your own</h2>\n'
            f'  <div class="row" style="gap:56px;margin-top:6px">{cols}\n  </div>\n'
            f'  <aside class="notes">Added for this deck; not from the textbook. Have this up as students walk in; they work silently while you take '
            f'attendance (about 5 minutes). The same 4 questions are on the online Day {d} bell work. Reveal the answers one at a time. Answer key: {key}</aside>\n</section>\n')


def today(n, page, goals, terms=""):
    body = '<div class="col" style="gap:10px;margin-top:4px;font-size:26px">' + "".join(
        f'<p class="step">{k}. {g}</p>' for k, g in enumerate(goals, 1)) + "</div>"
    if terms:
        body += f'\n  <p class="step small muted">{terms}</p>'
    return sec(f"Lesson {n} · SE p. {page}", "Today you will…", body, "Read each objective aloud as it appears.")


def eq_slide(n, page, lead, q):
    return sec(f"Essential Question · SE p. {page}", lead, f'<div class="col" style="gap:30px;margin-top:40px;font-size:36px"><p class="step">{q}</p></div>',
               "Have students write the Essential Question at the top of their notes. Don't answer it yet; we come back to it at the end of the lesson.")


def divider(n, d, q, recap):
    return sec(f"Lesson {n}", f"Day {d}", f'<p class="step" style="font-size:32px;max-width:900px">Essential Question: {q}</p>',
               f"Show this, then go to the bell work while you take attendance. Afterward, have a student read the Essential Question aloud and ask two or three students to summarize Day {d - 1}: {recap}", True)


def practice(n, days, se):
    bw = " · ".join(f'<b><a class="go" href="t2-lesson{n}-bellwork-day{d}.html" {GO}>Day {d} →</a></b>' for d in range(1, days + 1))
    body = (f'<div class="row" style="margin-top:20px">'
            f'<div class="col"><div class="card"><h3>Bell work</h3><p class="small">{bw}</p><p class="small">4 questions each, the same as the bell work slides. Scored when students submit.</p></div></div>'
            f'<div class="col"><div class="card"><h3><a class="go" href="t2-lesson{n}-homework.html" {GO}>Homework →</a></h3><p class="small">10 practice questions. Each answer is checked right away, with an explanation.</p></div></div>'
            f'<div class="col"><div class="card"><h3><a class="go" href="t2-lesson{n}-quiz.html" {GO}>Quiz →</a></h3><p class="small">10 questions, scored when students submit. Correct answers are shown after submitting.</p></div></div>'
            f'</div>\n  <p class="small muted" style="margin-top:6px">All are multiple choice. The homework follows the Lesson {n} Assignment ({se}).</p>')
    return sec("Practice Online", "Bell Work, Homework and Quiz", body,
               "Added for this deck; not from the textbook. Click a title to open it in a new tab. Put the day's bell work link up as students walk in. "
               "The 150-day pacing calendar (topic2-pacing-150.html) gives the day for each homework and quiz.")


def exit_ticket(items, work):
    body = '<div class="col" style="gap:12px;margin-top:6px">' + "".join(
        f'<p>{k}. {q}</p>{ans(a, True)}' for k, (q, a) in enumerate(items, 1)) + "</div>"
    return sec("Exit Ticket", "Show what you know", body,
               f"Added for this deck; not from the textbook. Give 3–4 minutes, collect the answers, and use them to decide who needs Skills Practice. Work: {work}")


C = lambda s: f'<span class="cm">{s}</span>'  # slope / dilation color
P = lambda s: f'<span class="cp">{s}</span>'  # point / translation color
FX = M("f(x)")


# ================================================================ Lesson 1
def lesson1():
    s = [title(1, "269–286", "Transforming Linear Functions", f'<i>g</i>(<i>x</i>) = {C("<i>a</i>")} · <i>f</i>(<i>x</i>) + {P("<i>d</i>")}', 3,
               "Welcome to Topic 2. Students transform the parent function f(x) = x: vertical translations f(x) + d (blue) and vertical dilations a · f(x) "
               "(orange). They prove a line and its translation are parallel and write equations of parallel lines. Three days on the 150-day calendar: Day 1 "
               "Getting Started and Activity 1.1; Day 2 Activities 1.2 and 1.3; Day 3 Activity 1.4, Activity 1.5 and Talk the Talk. Materials: masking tape and "
               "markers for the floor coordinate plane, the Problem-Solving Model Graphic Organizer.")]
    s.append(bell(1, 1, "Review"))
    s.append(today(1, 269, [f"Determine the effects on the graph of a linear function when {FX} is replaced by {M('f(x) + d')} or {M('a · f(x)')}.",
                            "Graph transformations of the parent function and describe them.",
                            "Prove that a line and its vertical translation are parallel.",
                            "Write the equation of a line parallel to a given line through a given point."],
                   "Key term: <b>parent function</b>, the simplest function of its type. " + mt("f(x) = x") + " is the parent of the linear function family."))
    s.append(eq_slide(1, 269, "You know linear functions and their slope and <i>y</i>-intercept.",
                      "How can you transform a function? What effects do different transformations have on the characteristics of linear functions?"))
    AB = L((-8, -8), (8, 8), "AB", seg=True)
    s.append(sec("Day 1 · Getting Started · Returning to Transformation Station · SE p. 270",
                 f"Translate {mt('AB')} with {mt('A(−8, −8)')} and {mt('B(8, 8)')}",
                 row(p("1. How do translations affect the coordinates?", "")
                     + table(["Original point", "4 units up", "4 units down"], [[M("(x, y)"), M("(x, y + 4)"), M("(x, y − 4)")]], 26, (1, 2))
                     + p("2. Draw " + mt("CD") + ", a translation of " + mt("AB") + " up 4 units.", "small")
                     + st(f"{mt('C(−8, −4)')} and {mt('D(8, 12)')}. Every point moves straight up 4, so {mt('CD')} is <b>parallel</b> to {mt('AB')}."),
                     graph(400, 400, [-10, 14], [-10, 14], [2, 4], [2, 4],
                           [AB, L((-8, -4), (8, 12), "CD", "b", True, seg=True)], [], "AB from (−8, −8) to (8, 8) and CD from (−8, −4) to (8, 12)")),
                 "Getting Started, 15–20 minutes. Tape a large coordinate plane on the floor; students stand on the points of AB and move as directed. "
                 "Ask: Did anyone move left or right? (No: only the y-coordinates changed.)"))
    s.append(sec("Day 1 · Getting Started · Dilations · SE p. 271", "Multiply every <i>y</i>-coordinate by 2, then by −2",
                 row(st("The points move straight up or down, away from the <i>x</i>-axis (twice as far).")
                     + st(f"× 2: {mt('E(−8, −16)')} and {mt('F(8, 16)')}. {mt('EF')} is <b>steeper</b>: a vertical stretch.")
                     + st(f"× (−2): {mt('G(−8, 16)')} and {mt('H(8, −16)')}. Steeper <b>and reflected</b> across the <i>x</i>-axis.")
                     + st("All three segments pass through the origin, which doesn't move."),
                     graph(400, 400, [-10, 10], [-18, 18], [2, 4], [2, 6],
                           [AB, L((-8, -16), (8, 16), "EF", "a", True, seg=True), L((-8, 16), (8, -16), "GH", "b", True, seg=True)], [],
                           "AB, EF stretched by 2, and GH stretched by 2 and reflected")),
                 "Ask: Which point did not move? (The origin: 0 times 2 is still 0.) What does multiplying by a negative do? (It reflects across the x-axis.)"))
    tf = lambda name, vals: table(["x", "f(x)", name], [[x, x, v] for x, v in zip(["−2", "−1", "0", "1", "2"], vals)], 22, (2,))
    s.append(sec("Day 1 · Activity 1.1 · Vertical Translations of Functions · SE p. 272", f"Translate {mt('f(x) = x')} down 5, then up 5",
                 row(tf("m(x)", ["−7", "−6", "−5", "−4", "−3"]) + ans("m(x) = x − 5"),
                     tf("p(x)", ["3", "4", "5", "6", "7"]) + ans("p(x) = x + 5"),
                     graph(330, 330, [-8, 8], [-8, 8], [1, 2], [1, 2],
                           [L((0, 0), (1, 1), "f(x)"), L((0, -5), (1, -4), "m(x)", "a", True), L((0, 5), (1, 6), "p(x)", "b", True)], [],
                           "f(x) = x with m(x) = x − 5 and p(x) = x + 5")) + st(
                     f"The slope stays <b>1</b>; only the <i>y</i>-intercept moves: {mt('(0, −5)')} and {mt('(0, 5)')}. Also {mt('f(2) = 2')} and {mt('p(2) = 7')}: the output went up 5."),
                 "Activity 1.1, 20–25 minutes. The slide reveals each table column, then the equation, then the graph line. Ask: Which values changed, the "
                 "inputs or the outputs? (Only the outputs.)"))
    s.append(sec("Day 1 · Activity 1.1 · Definition · SE p. 273", f"Vertical translation: {mt('y = f(x) + d')}",
                 '<div class="col" style="gap:20px;margin-top:10px">'
                 + st(f"{P(mt('d'))} {mt('> 0')}: the graph moves <b>up</b> {mt('d')} units. {P(mt('d'))} {mt('< 0')}: it moves <b>down</b>.", "")
                 + st("Only the output values change. The slope stays the same, so the new line is <b>parallel</b> to the original.", "")
                 + st(f"For {mt('f(x) = x')}: {mt('f(x) + d = x + d')}, a line with slope 1 and <i>y</i>-intercept {mt('(0, d)')}.", "") + "</div>",
                 "Have students copy the definition. Stamp the learning: a vertical translation changes the y-intercept, not the slope."))
    s.append(sec("Day 1 · Activity 1.1 · Questions 5–6 · SE p. 274", f"Translate {mt('j(x) = 2x − 1')} up 4 and down 4",
                 row(p("Up 4:") + ans("q(x) = j(x) + 4 = 2x + 3") + p("Down 4:") + ans("r(x) = j(x) − 4 = 2x − 5")
                     + st("All three have slope 2 and different <i>y</i>-intercepts: (0, −1), (0, 3), (0, −5). They are parallel, so they <b>never intersect</b>."),
                     graph(360, 380, [-6, 6], [-8, 8], [1, 2], [1, 2],
                           [L((0, -1), (1, 1), "j(x)"), L((0, 3), (1, 5), "q(x)", "b", True), L((0, -5), (1, -3), "r(x)", "a", True)], [],
                           "j(x) = 2x − 1, q(x) = 2x + 3 and r(x) = 2x − 5")),
                 "Ask Yourself: Will the graphs of j(x), q(x) and r(x) ever intersect? Ask: How can you tell from the equations? (Same slope, different y-intercepts.)"))
    s.append(sec("Day 1 · Activity 1.1 · Summary", "What does a vertical translation do?",
                 '<div class="col" style="gap:22px;margin-top:10px">'
                 + st(f"{mt('f(x) + d')} moves every point up or down {mt('d')} units.", "")
                 + st("The <b>slope</b> stays the same. The <b><i>y</i>-intercept</b> changes.", "")
                 + st("A line and its vertical translation are <b>parallel</b>.", "") + "</div>",
                 "To close Day 1, have students reread the Essential Question and summarize Activity 1.1 in their own words. End of Day 1."))
    q = "How can you transform a function? What effects do different transformations have on the characteristics of linear functions?"
    s.append(divider(1, 2, q, "What does f(x) + d do to the graph?"))
    s.append(bell(1, 2, "Review of Day 1"))
    s.append(sec("Day 2 · Activity 1.2 · Slopes of Parallel Lines · SE p. 275", f"Will the graphs of {mt('j(x)')} and {mt('q(x)')} ever intersect?",
                 eq("j(x) = 2x − 1 &nbsp;&nbsp; q(x) = 2x + 3") + st("No. Both lines have slope 2 and stay 4 units apart, so they are <b>parallel</b>.")
                 + p("Prove it for any line. Translate line <i>AB</i> up <i>a</i> units to make line <i>A′B′</i>.", "") +
                 row(p("Pre-image: " + mt("A(x₁, y₁)") + ", " + mt("B(x₂, y₂)")) + st("Image: " + mt("A′(x₁, y₁ + a)") + ", " + mt("B′(x₂, y₂ + a)")),
                     st("Slope of the image:") + eq("((y₂ + a) − (y₁ + a)) ÷ (x₂ − x₁)", "sm", True) + eq("= (y₂ − y₁) ÷ (x₂ − x₁)", "sm", True)),
                 "Activity 1.2, 15–20 minutes. The a's cancel, so the slopes are the same: the image is parallel to the pre-image. Ask: Why did the "
                 "x-coordinates stay the same? (A vertical translation moves only up or down.)"))
    s.append(sec("Day 2 · Activity 1.2 · Questions 3–4 · SE p. 276", "Write the equation of a parallel line",
                 row(card("Catalina", p(f"Parallel to {mt('y = ½x + 3')} through (2, 9): the point on the line at <i>x</i> = 2 is (2, 4), so translate up 5.")),
                     card("James", p("Use the slope ½ and the point (2, 9): " + mt("9 = ½(2) + b") + ", so " + mt("b = 8") + "."))) +
                 ans("y = ½x + 8") + p(f"Now you: parallel to {mt('y = −3x − 1')} through {mt('(−1, 5)')}.", "")
                 + st(f"Parallel, so the slope is −3: {mt('5 = −3(−1) + b')}, so {mt('b = 2')}.") + ans("y = −3x + 2"),
                 "Question 3 has no single answer: let students defend the method they prefer. Catalina thinks in translations; James uses the slope and a point."))
    da = lambda name, vals: table(["x", "f(x)", name], [[x, x, v] for x, v in zip(["−2", "−1", "0", "1", "2"], vals)], 22, (2,))
    s.append(sec("Day 2 · Activity 1.3 · Vertical Dilations of Functions · SE pp. 277–278", f"Multiply the outputs of {mt('f(x) = x')}",
                 row(p("× 4: " + mt("a(x)")) + da("a(x)", ["−8", "−4", "0", "4", "8"]) + ans("a(x) = 4x"),
                     p("× ⅔: " + mt("b(x)")) + da("b(x)", ["−4/3", "−2/3", "0", "2/3", "4/3"]) + ans("b(x) = ⅔x"),
                     p("× (−4): " + mt("c(x)")) + da("c(x)", ["8", "4", "0", "−4", "−8"]) + ans("c(x) = −4x"), gap=28),
                 "Activity 1.3, 20–25 minutes. All three pass through (0, 0): a dilation keeps the origin fixed. The slope becomes the factor: 4, 2/3, −4. "
                 "Ask: f(−1) = −1 and c(−1) = 4. What did the dilation do to the value at x = −1? (Multiplied it by −4.)"))
    s.append(sec("Day 2 · Activity 1.3 · Definition · SE p. 279", f"Vertical dilation: {mt('y = a · f(x)')}",
                 row('<div class="col" style="gap:18px">'
                     + st(f"{mt('|a| > 1')}: the graph <b>stretches</b> vertically (steeper).", "")
                     + st(f"{mt('0 < |a| < 1')}: it <b>compresses</b> vertically (less steep).", "")
                     + st(f"{mt('a < 0')}: it also <b>reflects</b> across the <i>x</i>-axis.", "")
                     + st(f"For {mt('f(x) = x')}, the new slope is {C(mt('a'))}; the <i>y</i>-intercept stays (0, 0).", "") + "</div>",
                     graph(330, 330, [-6, 6], [-6, 6], [1, 2], [1, 2],
                           [L((0, 0), (1, 1), "f(x)"), L((0, 0), (1, 4), "4f(x)", "a", True), L((0, 0), (3, 2), "⅔f(x)", "b", True)], [],
                           "f(x) = x, 4f(x) and two-thirds f(x)")),
                 "Have students copy the definition. Watch for students who say the slope 'increases' when a = −3: it gets steeper, but the slope is −3."))
    s.append(sec("Day 2 · Summary", "Translations vs. dilations",
                 row(card("Translation " + mt("f(x) + d"), p("Moves the line up or down. Same slope; new <i>y</i>-intercept. Parallel lines.")),
                     card("Dilation " + mt("a · f(x)"), p("Stretches, compresses or reflects. New slope; for " + mt("f(x) = x") + " the <i>y</i>-intercept stays (0, 0).")))
                 + st("Parallel line through a point: keep the slope, then find <i>b</i> with the point."),
                 "To close Day 2, have students reread the Essential Question. End of Day 2."))
    s.append(divider(1, 3, q, "How is a · f(x) different from f(x) + d?"))
    s.append(bell(1, 3, "Review of Day 2"))
    gs = [("a", "2f(x) + 7", "2x + 7", "Stretch by 2, then up 7"), ("b", "3f(x) − 1", "3x − 1", "Stretch by 3, then down 1"),
          ("c", "⅓f(x) + 2", "⅓x + 2", "Compress by ⅓, then up 2"), ("d", "½f(x) − 3", "½x − 3", "Compress by ½, then down 3"),
          ("e", "−f(x) − 4", "−x − 4", "Reflect across the <i>x</i>-axis, then down 4"), ("f", "−⅔f(x) + 5", "−⅔x + 5", "Reflect and compress by ⅔, then up 5")]
    s.append(sec("Day 3 · Activity 1.4 · Graphing Linear Transformations · SE pp. 280–281", f"Describe each transformation of {mt('f(x) = x')}, then graph <i>g</i>(<i>x</i>)",
                 '<div class="grid3" style="gap:14px 18px">' + "".join(
                     card(f"{k}. {mt('g(x) = ' + e)}", f'<p class="step small">{d}</p>{ans(r)}') for k, e, r, d in gs) + "</div>",
                 "Activity 1.4, 20 minutes. To graph g(x), start at the y-intercept (0, d) and use the slope a. Teacher-guide note: the slide numbers two items "
                 "'a.' in the student slides; they are b and e. Ask: Which number tells you the slope? Which tells you the y-intercept?"))
    s.append(sec("Day 3 · Activity 1.4 · Question 2 · SE p. 281", f"What do {C(mt('a'))} and {P(mt('d'))} do in {mt('g(x) = a · f(x) + d')}?",
                 row(card(C(mt("a")), st("Changes the slope. For " + mt("f(x) = x") + " the slope becomes " + mt("a") + ": steeper when " + mt("|a| > 1") + ", less steep when " + mt("0 < |a| < 1") + ", reflected when " + mt("a < 0") + ".")
                          + st("Does not change the <i>y</i>-intercept.")),
                     card(P(mt("d")), st("Does not change the slope.") + st("Moves the <i>y</i>-intercept to " + mt("(0, d)") + ": up when " + mt("d > 0") + ", down when " + mt("d < 0") + "."))),
                 "TE correction: the teacher guide says the slope 'increases' or 'decreases'; it means steepness. For a = −3 the slope is −3."))
    tgt = [[-4, 6, "(−4, 6)"], [5, 4, "(5, 4)"], [1, -3, "(1, −3)"], [-5, 1, "(−5, 1)"]]
    s.append(sec("Day 3 · Activity 1.5 · Hit the Targets · SE pp. 282–283", f"Aim with {mt('g(x) = a · f(x) + d')}",
                 row(p("Each shot is the graph of a transformation of " + mt("f(x) = x") + ". Hit each target.")
                     + card("Version B: " + mt("a = 1") + " or " + mt("−1") + "; choose " + mt("d"),
                            st(f"{mt('(−4, 6)')}: {mt('a = −1, d = 2')} &nbsp; {mt('(5, 4)')}: {mt('a = 1, d = −1')}<br>{mt('(1, −3)')}: {mt('a = −1, d = −2')} &nbsp; {mt('(−5, 1)')}: {mt('a = −1, d = −4')}"))
                     + card("Version C: " + mt("d = 0") + "; choose " + mt("a"),
                            st(f"{mt('(−4, 6)')}: {mt('a = −3/2')} &nbsp; {mt('(5, 4)')}: {mt('a = 4/5')}<br>{mt('(1, −3)')}: {mt('a = −3')} &nbsp; {mt('(−5, 1)')}: {mt('a = −1/5')}")),
                     graph(330, 330, [-8, 8], [-8, 8], [1, 2], [1, 2], [], tgt, "Four targets at (−4, 6), (5, 4), (1, −3) and (−5, 1)")),
                 "Activity 1.5, 20 minutes. Check any answer by substituting the target's x: for (−5, 1) with a = −1, d = −4: −(−5) − 4 = 1. Other Version B "
                 "answers exist (for example a = 1, d = 6 for (−5, 1)). TE correction: for (−5, 1) the teacher guide's a = 1, d = 4 misses; it is d = 6. "
                 "Version C's −6/4 simplifies to −3/2."))
    s.append(sec("Day 3 · Talk the Talk · SE p. 284", f"Match each graph to an equation in terms of {mt('f(x)')}",
                 '<div class="grid3" style="gap:14px 18px">' + "".join(
                     card(mt(nm), ans(e) + p(d, "step small")) for nm, e, d in
                     [("k(x)", "f(x) + 8", "Translated up 8."), ("h(x)", "2 · f(x)", "Stretched by 2: steeper, through (0, 0)."),
                      ("g(x)", "⅓ · f(x)", "Compressed by ⅓: less steep, through (0, 0)."), ("j(x)", "f(x) − 7", "Translated down 7.")]) + "</div>",
                 "Talk the Talk, 10 minutes. Students match the four transformed graphs in their book (SE p. 284) to the equations."))
    s.append(sec("Essential Question · Answered", "How can you transform a function?",
                 '<div class="col" style="gap:20px;margin-top:6px">'
                 + st(f"<b>Translation</b> {mt('y = f(x) + d')}: moves the graph up ({mt('d > 0')}) or down ({mt('d < 0')}). The slope stays the same, so the new line is parallel; the <i>y</i>-intercept changes.", "")
                 + st(f"<b>Dilation</b> {mt('y = a · f(x)')}: stretches ({mt('|a| > 1')}) or compresses ({mt('0 < |a| < 1')}) the graph; {mt('a < 0')} also reflects it across the <i>x</i>-axis. The slope changes; for {mt('f(x) = x')} it becomes {mt('a')}.", "") + "</div>",
                 "Have students answer the Essential Question on the lesson opener page."))
    s.append(exit_ticket([(f"{mt('f(x) = x')} and {mt('g(x) = 3f(x) − 2')}. Describe the transformation and write {mt('g(x)')}.", "Stretch by 3, down 2: " + M("g(x) = 3x − 2")),
                          (f"Write the line parallel to {mt('y = 4x − 1')} through {mt('(1, 7)')}.", M("y = 4x + 3")),
                          (f"{mt('(2, 5)')} is on {mt('f(x)')}. Which point is on {mt('−2 · f(x)')}?", M("(2, −10)"))],
                         "1. 3x is the stretch, − 2 moves the line down 2. 2. 7 = 4(1) + b, so b = 3. 3. Multiply the output by −2: 5 · (−2) = −10."))
    s.append(sec("Prepare · SE p. 286", "Write the equation of each line",
                 row(graph(360, 360, [-10, 6], [-12, 4], [1, 2], [1, 2], [L((-8, -10), (4, -2))], [[-8, -10, "(−8, −10)"], [-2, -6, "(−2, −6)"], [4, -2, "(4, −2)"]], "Line through (−8, −10), (−2, −6) and (4, −2)")
                     + ans("f(x) = ⅔x − 14/3"),
                     graph(360, 360, [-8, 8], [-4, 6], [1, 2], [1, 2], [L((0, 2), (4, 1))], [[0, 2, "(0, 2)"], [4, 1, "(4, 1)"]], "Line through (0, 2) and (4, 1)")
                     + ans("g(x) = −¼x + 2")),
                 "From the Lesson 1 Assignment. TE correction: the teacher guide gives f(x) = (2/3)x − 5, but the plotted points give slope 2/3 and "
                 "y-intercept (0, −14/3). Check: (2/3)(4) − 14/3 = 8/3 − 14/3 = −2. ✓"))
    s.append(practice(1, 3, "SE pp. 285–286"))
    return s


# ================================================================ Lesson 2
def lesson2():
    s = [title(2, "287–304", "Vertical and Horizontal Transformations of Linear Functions",
               f'<i>y</i> = {C("<i>a</i>")} · <i>f</i>({C("<i>b</i>")}(<i>x</i> − {P("<i>c</i>")})) + {P("<i>d</i>")}', 2,
               "Students compare horizontal transformations f(x − c) and f(bx) with the vertical ones from Lesson 1. For f(x) = x, a horizontal translation "
               "right n matches a vertical translation down n, and a vertical dilation by n matches a horizontal dilation by 1/n, but these pairs do not "
               "match for other linear functions. Two days on the 150-day calendar: Day 1 Getting Started and Activity 2.1; Day 2 Activities 2.2, 2.3 and "
               "Talk the Talk.")]
    s.append(bell(2, 1, "Review"))
    s.append(today(2, 287, ["Identify key characteristics of linear functions.",
                            f"Determine the effects on the graph of a linear function when {FX} is replaced by {M('f(x) + d')}, {M('f(x − c)')}, {M('a · f(x)')} and {M('f(bx)')}."]))
    s.append(eq_slide(2, 287, "You have learned the effects of vertical transformations on linear functions.",
                      "What effect do horizontal transformations have on linear functions? How do they compare to vertical transformations?"))
    kc = lambda rows: '<table class="cmp" style="font-size:22px">' + "".join(f'<tr><td>{a}</td><td class="step">{b}</td></tr>' for a, b in rows) + "</table>"
    s.append(sec("Day 1 · Getting Started · Hey, I Remember This! · SE p. 288", "Graph each function and describe its key characteristics",
                 row(eq("g(x) = 3x − 8", "sm") + kc([("Domain, range", "All real numbers"), ("<i>x</i>-intercept", "(8/3, 0)"), ("<i>y</i>-intercept", "(0, −8)"), ("Slope", "3, increasing")]),
                     eq("h(x) = −⅔x + 5", "sm") + kc([("Domain, range", "All real numbers"), ("<i>x</i>-intercept", "(7.5, 0)"), ("<i>y</i>-intercept", "(0, 5)"), ("Slope", "−⅔, decreasing")]),
                     graph(320, 320, [-8, 10], [-10, 8], [1, 2], [1, 2], [L((0, -8), (3, 1), "g(x)", "a", True), L((0, 5), (3, 3), "h(x)", "b", True)], [], "g(x) = 3x − 8 and h(x) = −2/3 x + 5")),
                 "Getting Started, 5–10 minutes. To find the x-intercept, set the function equal to 0: 3x − 8 = 0 gives x = 8/3; −(2/3)x + 5 = 0 gives x = 7.5."))
    tt = lambda name, xs, ys: table(["x", name], [[a, b] for a, b in zip(xs, ys)], 22, (0, 1))
    s.append(sec("Day 1 · Activity 2.1 · Comparing Vertical and Horizontal Translations · SE pp. 289–290", f"Translate {mt('f(x) = x')} left 3, then up 3",
                 row(p("Left 3: " + mt("t(x) = f(x + 3)")) + tt("t(x)", ["−5", "−4", "−3", "−2", "−1"], ["−2", "−1", "0", "1", "2"]) + st("The <b>inputs</b> change."),
                     p("Up 3: " + mt("w(x) = f(x) + 3")) + tt("w(x)", ["−2", "−1", "0", "1", "2"], ["1", "2", "3", "4", "5"]) + st("The <b>outputs</b> change."),
                     graph(320, 320, [-6, 6], [-6, 6], [1, 2], [1, 2], [L((0, 0), (1, 1), "f(x)"), L((-3, 0), (0, 3), "t(x) = w(x)", "b", True)], [], "f(x) = x and the line y = x + 3")
                     + st(f"Same line, {mt('y = x + 3')}, but different tables.")),
                 "Activity 2.1, 30–35 minutes. A horizontal translation left 3 subtracts 3 from each input value; the outputs stay the same."
                 "Ask: Which values were affected? (Left 3 changed the inputs; up 3 changed the outputs.)"))
    s.append(sec("Day 1 · Activity 2.1 · Definitions · SE p. 291", "Horizontal vs. vertical translations",
                 row(card(mt("y = f(x − c)"), p("Changes the <b>inputs</b>. " + mt("c > 0") + ": shift <b>right</b> " + mt("c") + ". " + mt("c < 0") + ": shift <b>left</b>.")),
                     card(mt("y = f(x) + d"), p("Changes the <b>outputs</b>. " + mt("d > 0") + ": shift <b>up</b> " + mt("d") + ". " + mt("d < 0") + ": shift <b>down</b>.")))
                 + st(f"For {mt('f(x) = x')}: right {mt('n')} = down {mt('n')}, and left {mt('n')} = up {mt('n')}.") + st("Does that work for <b>every</b> linear function?", "warn"),
                 "Watch the sign: f(x − 3) moves right 3, f(x + 3) moves left 3."))
    s.append(sec("Day 1 · Activity 2.1 · Questions 6–9 · SE pp. 292–294", f"Try it with {mt('j(x) = 2x − 1')}",
                 row(p("Up 4 and left 4:") + ans("q(x) = j(x) + 4 = 2x + 3") + ans("r(x) = j(x + 4) = 2(x + 4) − 1 = 2x + 7")
                     + p("Right 2 and down 2:") + ans("b(x) = j(x − 2) = 2x − 5") + ans("v(x) = j(x) − 2 = 2x − 3")
                     + st("<b>Not the same.</b> The lines are parallel with different <i>y</i>-intercepts."),
                     graph(330, 360, [-6, 6], [-8, 8], [1, 2], [1, 2],
                           [L((0, -1), (1, 1), "j(x)"), L((0, 3), (1, 5), "q(x)", "a", True), L((0, 7), (1, 9), "r(x)", "b", True)], [], "j(x), q(x) = 2x + 3 and r(x) = 2x + 7")),
                 "Teacher-guide misconception: students expect left 4 to equal up 4 for every line. It works only for slope 1. Slide typos in the student slides: "
                 "some items labeled 'a.' are b, c and d."))
    s.append(sec("Day 1 · Activity 2.1 · Summary", "Translations of linear functions",
                 '<div class="col" style="gap:22px;margin-top:10px">'
                 + st("Inside the parentheses changes the <b>input</b> (horizontal); outside changes the <b>output</b> (vertical).", "")
                 + st(f"{mt('f(x − c)')} moves right {mt('c')}; the sign flips.", "")
                 + st(f"Only for {mt('f(x) = x')} does right {mt('n')} match down {mt('n')}.", "") + "</div>",
                 "End of Day 1."))
    q = "What effect do horizontal transformations have on linear functions? How do they compare to vertical transformations?"
    s.append(divider(2, 2, q, "Does a translation right n always match a translation down n?"))
    s.append(bell(2, 2, "Review of Day 1"))
    s.append(sec("Day 2 · Activity 2.2 · Comparing Vertical and Horizontal Dilations · SE pp. 295–296", f"Change the outputs or the inputs of {mt('f(x) = x')}",
                 row(p("Outputs × 2: " + mt("a(x) = 2f(x)")) + tt("a(x)", ["−2", "−1", "0", "1", "2"], ["−4", "−2", "0", "2", "4"]),
                     p("Inputs × ½: " + mt("b(x) = f(2x)")) + tt("b(x)", ["−1", "−½", "0", "½", "1"], ["−2", "−1", "0", "1", "2"]),
                     graph(300, 300, [-4, 4], [-5, 5], [1, 1], [1, 1], [L((0, 0), (1, 1), "f(x)"), L((0, 0), (1, 2), "y = 2x", "a", True)], [], "f(x) = x and y = 2x")
                     + st(f"Both are the line {mt('y = 2x')}, with different tables.")),
                 "Activity 2.2, 15–20 minutes. Changing the inputs by a factor of 1/2 is a horizontal compression: each point moves halfway to the y-axis."))
    s.append(sec("Day 2 · Activity 2.2 · Questions 2–3 · SE p. 296", "Factors of ⅘ and 5/4",
                 row(p("Outputs × ⅘: " + mt("c(x) = ⅘f(x)")) + tt("c(x)", ["−2", "−1", "0", "1", "2"], ["−8/5", "−4/5", "0", "4/5", "8/5"]),
                     p("Inputs × 5/4: " + mt("d(x) = f(⅘x)")) + tt("d(x)", ["−5/2", "−5/4", "0", "5/4", "5/2"], ["−2", "−1", "0", "1", "2"]),
                     st(f"Same line, {mt('y = ⅘x')}.") + st(f"For {mt('f(x) = x')}: a vertical dilation by {mt('n')} = a horizontal dilation by {mt('1/n')}.")
                     + card("Definitions", p(f"{mt('y = a · f(x)')}: vertical, changes outputs.<br>{mt('y = f(bx)')}: horizontal, changes inputs; {mt('|b| > 1')} compresses, {mt('0 < |b| < 1')} stretches, {mt('b < 0')} reflects across the <i>y</i>-axis.")), gap=28),
                 "Ask: Why are the tables different if the graphs are the same? (They list different points of the same line.)"))
    s.append(sec("Day 2 · Activity 2.2 · Question 4 · SE p. 297", "Does this hold for any linear function?",
                 row(p(f"Counterexample: {mt('m(x) = 2x − 1')}", "") + ans('<span class="ga">' + M("3 · m(x) = 6x − 3") + "</span>", True) + ans('<span class="gb">' + M("m(3x) = 6x − 1") + "</span>", True)
                     + st("<b>No.</b> The graphs are parallel, not the same. It works only for the parent function."),
                     graph(330, 340, [-4, 4], [-6, 6], [1, 1], [1, 2], [L((-2.5, -6), (3.5, 6), "m(x)"), L((-0.5, -6), (1.5, 6), None, "a", True), L((-5/6, -6), (7/6, 6), None, "b", True)], [], "m(x) = 2x − 1, 3m(x) and m(3x)")),
                 "Counterexamples will vary; any linear function other than f(x) = x works."))
    gr = [("1", "f(x − 7)", "x − 7", "Right 7"), ("2", "3f(x)", "3x", "Vertical stretch by 3"), ("3", "f(x) + 2", "x + 2", "Up 2"),
          ("4", "f(½x)", "½x", "Horizontal stretch by 2"), ("5", "f(x) − 4", "x − 4", "Down 4"), ("6", "f(x + 5)", "x + 5", "Left 5")]
    s.append(sec("Day 2 · Activity 2.3 · Graphing Linear Transformations · SE pp. 298–300", f"Describe each transformation of {mt('f(x) = x')}",
                 '<div class="grid3" style="gap:14px 18px">' + "".join(card(f"{k}. {mt('g(x) = ' + e)}", f'<p class="step small">{d}</p>{ans("g(x) = " + r)}') for k, e, r, d in gr) + "</div>",
                 "Activity 2.3, 15–20 minutes. Graph each g(x) on the grids in the book: plot the y-intercept and use the slope. Slide typo in the student "
                 "slides: items 2, 3, 5 and 6 are numbered '1.'"))
    s.append(sec("Day 2 · Talk the Talk · Show Me What You've Got · SE p. 301", f"Match each graph to an equation in terms of {mt('f(x)')}",
                 '<div class="grid3" style="gap:14px 18px">' + "".join(card(mt(nm), ans(e)) for nm, e in
                     [("k(x)", "f(x) + 8"), ("h(x)", "2f(x)"), ("g(x)", "f(⅓x)"), ("j(x)", "f(x − 7)")]) + "</div>",
                 "Talk the Talk, 5 minutes. For f(x) = x, f(x) + 8 is also f(x + 8), and f(⅓x) is also ⅓f(x)."))
    s.append(sec("Essential Question · Answered", "What do horizontal transformations do?",
                 '<div class="col" style="gap:20px;margin-top:6px">'
                 + st(f"In {mt('a · f(b(x − c)) + d')}, {C(mt('b'))} and {P(mt('c'))} change the <b>inputs</b> (horizontal); {C(mt('a'))} and {P(mt('d'))} change the <b>outputs</b> (vertical).", "")
                 + st(f"For {mt('f(x) = x')}: right {mt('n')} = down {mt('n')}, and a vertical dilation by {mt('n')} = a horizontal dilation by {mt('1/n')}.", "")
                 + st("For other linear functions these pairs are <b>not</b> the same.", "") + "</div>",
                 "Have students answer the Essential Question on the lesson opener page."))
    s.append(exit_ticket([(f"{mt('f(x) = x')} and {mt('g(x) = f(x + 6)')}. Describe the transformation.", "Left 6"),
                          (f"{mt('j(x) = 3x + 1')}. Simplify {mt('j(x − 2)')}.", M("3x − 5")),
                          (f"For {mt('f(x) = x')}, which vertical dilation gives the same graph as {mt('f(5x)')}?", M("5f(x)"))],
                         "1. Adding to the input moves left. 2. 3(x − 2) + 1 = 3x − 5. 3. f(5x) = 5x = 5f(x)."))
    s.append(sec("Prepare · SE p. 304", "Determine the reciprocal of each value",
                 row(eq("1. &nbsp;3", "sm") + ans("1/3") + eq("3. &nbsp;1/5", "sm") + ans("5") + eq("5. &nbsp;−c", "sm") + ans("−1/c"),
                     eq("2. &nbsp;−10", "sm") + ans("−1/10") + eq("4. &nbsp;−5/4", "sm") + ans("−4/5") + eq("6. &nbsp;a/b", "sm") + ans("b/a")),
                 "From the Lesson 2 Assignment. TE correction: the teacher guide gives the reciprocal of −10 as 1/10; it is −1/10, since (−10)(−1/10) = 1."))
    s.append(practice(2, 2, "SE pp. 303–304"))
    return s


# ================================================================ Lesson 3
def lesson3():
    s = [title(3, "305–318", "Determining Slopes of Perpendicular Lines", f'{C("<i>m</i><sub>1</sub>")} · {C("<i>m</i><sub>2</sub>")} = −1', 2,
               "Students rotate a segment 90° at a time, prove that perpendicular lines have negative reciprocal slopes, work with horizontal and vertical "
               "lines, and write equations of perpendicular lines. Two days on the 150-day calendar: Day 1 Getting Started and Activity 3.1; Day 2 "
               "Activities 3.2, 3.3 and Talk the Talk. Materials: patty paper, straightedges.")]
    s.append(bell(3, 1, "Review"))
    s.append(today(3, 305, ["Identify and write the equations of lines perpendicular to given lines.", "Identify and write the equations of horizontal and vertical lines."]))
    s.append(eq_slide(3, 305, "You have translated graphs of linear equations to find the slopes of parallel lines.",
                      "How can you rotate the graphs of linear equations to determine the slopes of perpendicular lines?"))
    seg = lambda b, lab, c=None: L((0, 0), b, lab, c, True, seg=True)
    s.append(sec("Day 1 · Getting Started · Coordinate Rotation · SE p. 306", f"Rotate {mt('AB')}, {mt('A(0, 0)')} and {mt('B(8, 5)')}, about the origin",
                 row(table(["", "Original", "90°", "180°", "270°"], [["A", "(0, 0)", "(0, 0)", "(0, 0)", "(0, 0)"], ["B", "(8, 5)", "(−5, 8)", "(−8, −5)", "(5, −8)"]], 22, (2, 3, 4))
                     + st(f"Each 90° counterclockwise turn maps {mt('(x, y)')} to {mt('(−y, x)')}. A is the center, so it stays.")
                     + st(f"Slopes: {mt('AB')} and {mt('A″B″')}: {C(mt('5/8'))}. {mt('A′B′')} and {mt('A‴B‴')}: {C(mt('−8/5'))}.")
                     + st("The two slopes are reciprocals with opposite signs: " + mt("(5/8)(−8/5) = −1") + "."),
                     graph(330, 330, [-9, 9], [-9, 9], [1, 3], [1, 3], [L((0, 0), (8, 5), seg=True), seg((-5, 8), None, "a"), seg((-8, -5), None, "b"), seg((5, -8), None, "a")], [[8, 5, "B"], [-5, 8, "B′"], [-8, -5, "B″"], [5, -8, "B‴"]], "AB and its rotations by 90, 180 and 270 degrees")),
                 "Getting Started, 15–20 minutes. Patty paper helps: trace the segment and the axes, then turn the paper a quarter turn."))
    s.append(sec("Day 1 · Activity 3.1 · Slopes of Perpendicular Lines · SE p. 307", "A line and its 90° rotation",
                 row(card("Pair A", ans("y = x") + ans("y = −x")), card("Pair B", ans("y = ⅓x + 5") + ans("y = −3x + 5")), card("Pair C", ans("y = −⅔x + 9") + ans("y = 3/2x − 4")), gap=20)
                 + st("Each line is rotated 90°, so the lines meet at a right angle: they are <b>perpendicular</b>.")
                 + st("The slopes of each pair are reciprocals with opposite signs."),
                 "Activity 3.1, 20–25 minutes. Students read the three graphs in their book (SE p. 307) and write the equations."))
    s.append(sec("Day 1 · Activity 3.1 · Worked Example · SE p. 308", "Proof: perpendicular slopes are negative reciprocals",
                 row('<div class="col" style="gap:12px">' + p(f"Given {mt('p ⊥ q')}. Point {mt('R(a, b)')} is on {mt('p')}.", "")
                     + st(f"Rotate {mt('R')} 90° counterclockwise about {mt('O')}: it lands on {mt('q')} at {mt('D(−b, a)')}.")
                     + st(f"Slope of {mt('p')}: {C(mt('m₁ = b/a'))}. Slope of {mt('q')}: {C(mt('m₂ = a/(−b)'))}.")
                     + eq("−1/m₂ = −1 · (−b/a) = b/a = m₁", "sm", True) + st("So " + mt("m₁ = −1/m₂") + ", and " + mt("m₁ · m₂ = −1") + ".") + "</div>",
                     graph(340, 300, [-4, 6], [-4, 4], [1, 1], [1, 1], [L((0, 0), (3, 1.5), "p"), L((0, 0), (-1.5, 3), "q", "b")], [[2, 1, "R(a, b)"], [-1, 2, "D(−b, a)"]], "Line p through R(a, b) and line q through D(−b, a)")),
                 "Have students restate each step. Question 3 asks for the same proof with a clockwise rotation: R(a, b) maps to D(b, −a), so m₂ = −a/b and again m₁ = −1/m₂."))
    s.append(sec("Day 1 · Activity 3.1 · Question 4 · SE p. 309", f"Line {mt('j')} ⊥ line {mt('k')}. Find the slope of line {mt('k')}.",
                 row(eq("a. &nbsp;m = ⅔", "sm") + ans("m = −3/2"), eq("b. &nbsp;m = −⅘", "sm") + ans("m = 5/4"), eq("c. &nbsp;m = −3", "sm") + ans("m = ⅓"))
                 + st("Flip the fraction and change the sign. Check: the product is −1."),
                 "Stamp the learning: perpendicular lines have slopes that are negative reciprocals. End of Day 1."))
    q = "How can you rotate the graphs of linear equations to determine the slopes of perpendicular lines?"
    s.append(divider(3, 2, q, "How do you find the slope of a perpendicular line?"))
    s.append(bell(3, 2, "Review of Day 1"))
    s.append(sec("Day 2 · Activity 3.2 · Horizontal and Vertical Lines · SE pp. 310–311", "Extend the segments into lines",
                 row(st(f"Line {mt('p')} is vertical: {mt('x = 4')}. Lines {mt('q')}, {mt('r')} and {mt('s')} are horizontal: {mt('y = 4')}, {mt('y = 8')}, {mt('y = 12')}.")
                     + card("Horizontal", st("When <i>x</i> goes up 1, <i>y</i> doesn't change. Slope " + mt("= 0/(x₂ − x₁) = 0") + "."))
                     + card("Vertical", st("When <i>y</i> goes up 1, <i>x</i> doesn't change. Slope " + mt("= (y₂ − y₁)/0") + ": <b>undefined</b>.")),
                     graph(320, 320, [-1, 17], [-1, 17], [1, 4], [1, 4], [L((4, 0), (4, 1), "p"), L((0, 4), (1, 4), "q", "b", True), L((0, 8), (1, 8), "r", "b", True), L((0, 12), (1, 12), "s", "b", True)],
                           [[4, 12, "K"], [4, 8, "F"], [4, 4, "G"], [14, 12, "L"], [14, 8, "J"], [14, 4, "H"]], "Vertical line x = 4 and horizontal lines y = 4, 8 and 12")),
                 "Activity 3.2, 15–20 minutes. Memory trick from Topic 1: HOY VUX."))
    s.append(sec("Day 2 · Activity 3.2 · Questions 6–10 · SE p. 311", "Always, sometimes, or never?",
                 row(p("All vertical lines are parallel.") + st("<b>Always.</b> Their slopes are all undefined.") + p("All horizontal lines are parallel.") + st("<b>Always.</b> Their slopes are all 0.")
                     + p("A vertical line and a horizontal line?") + st("<b>Always perpendicular.</b>"),
                     p("Through " + mt("(2, −1)") + ":") + ans("y = −1 &nbsp;and&nbsp; x = 2") + p("⊥ to " + mt("x = 5") + " through " + mt("(1, 0)") + ":") + ans("y = 0")
                     + p("⊥ to " + mt("y = −2") + " through " + mt("(5, 6)") + ":") + ans("x = 5")),
                 "Questions 8–10 assess the lesson. For more practice, assign Skills Practice Set A."))
    s.append(sec("Day 2 · Activity 3.3 · Writing Equations of Perpendicular Lines · SE p. 312", "Use the negative reciprocal slope and point-slope form",
                 row(p(f"1. ⊥ to {mt('y = 2x + 1')} through {mt('(6, 2)')}") + st("Slope " + C(mt("−½")) + ": " + mt("y − 2 = −½(x − 6)")) + ans("y = −½x + 5"),
                     p(f"2. ⊥ to {mt('y = −¾x')} through {mt('(3, −8)')}") + st("Slope " + C(mt("4/3")) + ": " + mt("y + 8 = 4/3(x − 3)")) + ans("y = 4/3x − 12")),
                 "Activity 3.3, 15–20 minutes. TE wording slip: for Question 2 the teacher guide says the given slope is 3/4; it is −3/4."))
    s.append(sec("Day 2 · Activity 3.3 · Questions 3–5 · SE pp. 312–313", "First find the slope of the given line",
                 row(p("3. Through " + mt("(6, 2)") + ", ⊥ to the line through " + mt("(−5, 3)") + " and " + mt("(−1, −9)")) + st(mt("m = −12/4 = −3") + ", so use " + C(mt("⅓"))) + ans("y = ⅓x"),
                     p("4. Through " + mt("(−2, 7)") + ", ⊥ to the line through " + mt("(−6, 1)") + " and " + mt("(0, 4)")) + st(mt("m = 3/6 = ½") + ", so use " + C(mt("−2"))) + ans("y = −2x + 3"),
                     p("5. Lines meet at " + mt("(5, 9)") + "; one passes through " + mt("(−4, 4)")) + st(mt("m = 5/9") + ", so use " + C(mt("−9/5"))) + ans("y = −9/5x + 18"), gap=28),
                 "The teacher guide prints the slope formula with y₂ − y₁ in the denominator; it is x₂ − x₁. Its numbers are correct. For more practice, assign Skills Practice Set B."))
    s.append(sec("Day 2 · Talk the Talk · Things Aren't Always What They Seem · SE p. 314", "Linh or Jackson?",
                 p("Linh says lines <i>a</i>, <i>b</i> and <i>c</i> are parallel to each other and perpendicular to lines <i>d</i>, <i>e</i> and <i>f</i>. Jackson says they are parallel but <b>not</b> perpendicular to <i>d</i>, <i>e</i>, <i>f</i>.", "")
                 + st("<b>Jackson is correct.</b> The axes use different scales.") + st("Lines <i>a</i>, <i>b</i>, <i>c</i> have slope 1, so they are parallel. Lines <i>d</i>, <i>e</i>, <i>f</i> have slope −¼.")
                 + st(mt("1 · (−¼) ≠ −1") + ": the slopes are not negative reciprocals, so the lines are not perpendicular."),
                 "Show the graph in the book (SE p. 314). The x-axis counts 1 per square and the y-axis 1 per 2 squares, so the lines look perpendicular but aren't."))
    s.append(sec("Essential Question · Answered", "How does rotation give perpendicular slopes?",
                 '<div class="col" style="gap:20px;margin-top:6px">'
                 + st(f"A 90° rotation maps {mt('(x, y)')} to {mt('(−y, x)')}, so a slope {mt('b/a')} becomes {mt('−a/b')}.", "")
                 + st("Perpendicular lines have <b>negative reciprocal</b> slopes: their product is −1.", "")
                 + st("Any vertical line is perpendicular to any horizontal line.", "") + "</div>",
                 "Have students answer the Essential Question on the lesson opener page."))
    s.append(exit_ticket([("What slope is perpendicular to " + mt("−5/2") + "?", M("2/5")),
                          (f"Write the line ⊥ to {mt('y = 3x + 2')} through {mt('(3, 1)')}.", M("y = −⅓x + 2")),
                          (f"Write the vertical line through {mt('(−4, 7)')}.", M("x = −4"))],
                         "1. Flip and change the sign. 2. Slope −1/3: 1 = −1/3(3) + b, so b = 2. 3. A vertical line keeps x the same."))
    s.append(sec("Prepare · SE p. 317", "Does each set of ordered pairs represent a function?",
                 '<div class="col" style="gap:10px">' + "".join(f'<div class="row" style="gap:30px;align-items:center">{eq(f"{k}. &nbsp;{st_}", "sm")}{ans(a, True)}</div>' for k, st_, a in [
                     (1, "{(−1, −1), (0, 0), (1, 1), (2, 2)}", "Function"), (2, "{(−1, −2), (0, 0), (1, 2), (2, 4)}", "Function"),
                     (3, "{(−1, −1), (0, −1), (1, −1), (2, −1)}", "Function"), (4, "{(−1, −1), (−1, 0), (−1, 1), (−1, 2)}", "Not a function")]) + "</div>",
                 "From the Lesson 3 Assignment. In a function each input has exactly one output; in set 4 the input −1 has four outputs."))
    s.append(practice(3, 2, "SE pp. 315–317"))
    return s


# ================================================================ Lesson 4
def lesson4():
    s = [title(4, "319–330", "Comparing Linear Functions in Different Forms", "table · graph · equation · description", 2,
               "Students compare linear functions given as tables, graphs, equations and verbal descriptions: slope (parallel or perpendicular), "
               "y-intercept, and the units and scales in context. Two days on the 150-day calendar: Day 1 Getting Started, Activities 4.1 and 4.2; Day 2 "
               "Activities 4.3, 4.4 and Talk the Talk.")]
    s.append(bell(4, 1, "Review"))
    s.append(today(4, 319, ["Compare linear functions represented algebraically, graphically, in tables, or with verbal descriptions.",
                            "Choose and interpret appropriate units to represent independent and dependent quantities in situations modeled by linear functions.",
                            "Choose and interpret appropriate scales and origins for graphs of linear functions."]))
    s.append(eq_slide(4, 319, "You have represented linear functions in a variety of different ways.", "How does each linear function representation compare with the others?"))
    s.append(sec("Day 1 · Getting Started · Odd One Out · SE p. 320", "Which function does not belong? Justify your choice.",
                 '<div class="row" style="gap:14px">'
                 + card("A", table(["x", "y"], [["−5", "10"], ["−1.5", "3"], ["0", "0"], ["2.5", "−5"]], 20) + p("Only one <b>decreasing</b> (slope −2).", "step small"))
                 + card("B", p("The ratio of 9th- to 10th-graders is 1 : 1.") + p("Only one with a domain of <b>whole numbers</b>.", "step small"))
                 + card("C", eq("c(x) = ⅕x", "sm") + p("Only one with a slope <b>between 0 and 1</b>.", "step small"))
                 + card("D", graph(200, 200, [-4, 4], [-4, 8], [1, 2], [1, 2], [L((-1, 0), (0, 5))], [[0, 5, "(0, 5)"]], "A steep line through (0, 5)") + p("Only one whose <b><i>y</i>-intercept isn't 0</b>.", "step small")) + "</div>",
                 "Getting Started, 5–10 minutes. Any choice is correct if the justification is."))
    q41 = f"Parallel, perpendicular, or neither to {mt('y = 4x − 3')}?"
    note41 = "Activity 4.1, 15–20 minutes. Find each slope first, then compare it to 4: equal is parallel, a product of −1 is perpendicular."
    s.append(sec("Day 1 · Activity 4.1 · Slopes of Linear Relationships · SE p. 321", q41,
                 row(card("a.", table(["x", "y"], [["−2.5", "−6"], ["0", "4"], ["0.5", "6"], ["3", "16"]], 22) + st("Slope 4: <b>parallel</b>.")),
                     card("b.", p("An elevator descends 4 feet every second.") + st("Slope −4: <b>neither</b>.")),
                     card("c.", eq("y = ¼x + 5", "sm") + st("Slope ¼: <b>neither</b>. " + mt("4 · ¼ = 1") + ", not −1.")), gap=20), note41))
    s.append(sec("Day 1 · Activity 4.1 · Slopes of Linear Relationships · SE p. 321", q41,
                 row(card("d.", graph(300, 300, [-8, 8], [-8, 8], [1, 4], [1, 4], [L((-8, -2.5), (8, 1.5))], [], "A line rising gently with slope 1/4") + st("Slope ¼: <b>neither</b>.")),
                     card("e.", table(["x", "y"], [["−4", "3"], ["0", "2"], ["2", "1.5"], ["8", "0"]], 22) + st("Slope −¼: <b>perpendicular</b>.")),
                     card("f.", p("For every hour Chiletso bakes, she makes 4 dozen cookies.") + st("Slope 4: <b>parallel</b>.")), gap=20),
                 "Ask: How did you find the slope from the graph? (From (0, −0.5), right 4 and up 1.)"))
    s.append(sec("Day 1 · Activity 4.2 · Comparing Tables and Graphs · SE p. 322", "Recycling cardboard",
                 row(p("Travis County") + table(["Weight (tons)", "Payout ($)"], [["0.5", "7.50"], ["1", "15"], ["1.5", "22.50"], ["2", "30"]], 22)
                     + st(f"{mt('w(0.5) < j(0.5)')}, &nbsp;{mt('w(1) < j(1)')}, &nbsp;{mt('w(3) < j(3)')}"),
                     p("Hays County") + graph(320, 300, [0, 4], [0, 22], [0.5, 1], [1, 5], [L((0, 0), (1, 20))], [[1, 20, "(1, 20)"]], "Hays County: a line through (0, 0) and (1, 20)")
                     + st("Both <i>y</i>-intercepts are 0: $0 for 0 tons.") + st("<b>Hays County</b> pays more: $20 per ton vs. $15 per ton.")),
                 "Activity 4.2, 10–15 minutes. Question 1: label x = weight of cardboard (tons) and y = payout amount (dollars) on both. Travis: w(3) = 45; Hays: j(3) = 60. End of Day 1."))
    q = "How does each linear function representation compare with the others?"
    s.append(divider(4, 2, q, "How did you compare the recycling centers?"))
    s.append(bell(4, 2, "Review of Day 1"))
    s.append(sec("Day 2 · Activity 4.3 · Comparing Equations and Tables · SE p. 323", "Celsius and Fahrenheit",
                 row(p("Joey's table") + table(["°F", "°C"], [["10", "−12.2"], ["30", "−1.1"], ["50", "10"], ["75", "23.9"]], 22),
                     p("Xavier's equation") + eq("J(x) = 9/5x + 32", "sm")
                     + st("Xavier converts <b>°C to °F</b> (<i>x</i> is °C). Joey converts <b>°F to °C</b>.")
                     + st("<b>Slope:</b> Joey's is about 5/9 (each 9°F is about 5°C). Xavier's is 9/5 (each 5°C is 9°F).")
                     + st("<b><i>y</i>-intercept:</b> Joey's is about −17.8 (0°F ≈ −17.8°C). Xavier's is 32 (0°C = 32°F).")),
                 "Activity 4.3, 10–15 minutes. Think About: the units of the quantities matter. Joey's slope: (10 − (−12.2)) ÷ (50 − 10) = 22.2 ÷ 40 ≈ 0.56."))
    s.append(sec("Day 2 · Activity 4.4 · Comparing Descriptions and Graphs · SE p. 324", "Miguel and Lauren's bank accounts",
                 row(p("Miguel") + graph(300, 300, [0, 5], [0, 100], [1, 1], [20, 20], [], [[1, 20, ""], [2, 40, ""], [3, 60, ""], [4, 80, "(4, 80)"]], "Miguel's savings: 20, 40, 60 and 80 dollars after 1 to 4 months"),
                     p("Lauren starts with $25 and deposits $25 each month.")
                     + st("<b>Scales:</b> each <i>x</i> tick is 1 month and each <i>y</i> tick is $20 ($80 after 4 months). The origin is (0 months, $0).")
                     + st("<b>Slope:</b> Miguel saves $20 a month; Lauren saves $25 a month.") + st("<b><i>y</i>-intercept:</b> Miguel started with $0; Lauren with $25.")),
                 "Activity 4.4, 10–15 minutes. Slide typo in the student slides: the introduction calls Lauren 'Michelle'. For more practice, assign Skills Practice Set A."))
    s.append(sec("Day 2 · Talk the Talk · Function Maker Space · SE p. 325", "Create and compare",
                 table(["x", "−10", "10", "20", "25"], [["y", "0", "5", "7.5", "8.75"]], 22)
                 + row(p("1. A situation for the table:") + st("Sample: Alejandra has read 2.5 pages and reads 2.5 more every 10 minutes. Slope ¼, <i>y</i>-intercept 2.5.")
                       + p("2. A less steep equation:") + ans("y = 0.2x + 30"),
                       p("3. The graph shown in the book has slope ⅓ (through (0, −4)).") + st("It is steeper than the table (¼) and the equation (0.2).")
                       + p("4. Strategies:") + st("Answers vary: rate of change from two points; compare the slopes.")),
                 "Talk the Talk, 10–15 minutes. TE wording slip: the teacher guide's sample starts Alejandra 'at the middle of page 2'; 2.5 pages read is the middle of page 3."))
    s.append(sec("Essential Question · Answered", "How do the representations compare?",
                 '<div class="col" style="gap:20px;margin-top:6px">'
                 + st("Every form (equation, table, graph, description) shows the same features: the <b>slope</b> or rate and the <b><i>y</i>-intercept</b> or starting value.", "")
                 + st("Compare by finding these in each form: equal slopes are parallel; slopes with a product of −1 are perpendicular.", "")
                 + st("The quantities and units tell what the slope and <i>y</i>-intercept mean.", "") + "</div>",
                 "Have students answer the Essential Question on the lesson opener page."))
    s.append(exit_ticket([("A table has " + mt("(0, 3)") + " and " + mt("(2, 11)") + ". Is its line parallel, perpendicular, or neither to " + mt("y = 4x − 3") + "?", "Parallel (slope 4)"),
                          (mt("f(x) = 3x + 10") + " and a table with " + mt("(0, 4), (1, 9)") + ". Which grows faster?", "The table (slope 5 &gt; 3)"),
                          ("A taxi charges $2.50 per mile plus $3. What are the units of the slope?", "Dollars per mile")],
                         "1. (11 − 3) ÷ 2 = 4. 2. (9 − 4) ÷ 1 = 5. 3. The slope is the output unit over the input unit."))
    s.append(sec("Prepare · SE p. 330", "Solve each equation for <i>x</i>",
                 row(eq("1. &nbsp;⅓x = 8", "sm") + ans("x = 24") + eq("3. &nbsp;2x − 9 = 6", "sm") + ans("x = 7.5"),
                     eq("2. &nbsp;5 + x = 12.7", "sm") + ans("x = 7.7") + eq("4. &nbsp;12 + 2x = 3x − 1", "sm") + ans("x = 13")),
                 "From the Lesson 4 Assignment; it previews Module 3."))
    s.append(practice(4, 2, "SE pp. 327–330"))
    return s


DECKS = {1: ("t2-lesson1-transforming-linear-functions", "Transforming Linear Functions", lesson1),
         2: ("t2-lesson2-vertical-horizontal-transformations", "Vertical and Horizontal Transformations of Linear Functions", lesson2),
         3: ("t2-lesson3-perpendicular-slopes", "Determining Slopes of Perpendicular Lines", lesson3),
         4: ("t2-lesson4-comparing-linear-functions", "Comparing Linear Functions in Different Forms", lesson4)}

if __name__ == "__main__":
    for n, (stem, name, build) in DECKS.items():
        secs = build()
        head = re.sub(r"<title>.*?</title>", f"<title>{name} · Bluebonnet Algebra I</title>", HEAD, count=1)
        out = ROOT / "Module 2 topic 2" / f"{stem}.html"
        out.write_text(head + '<div id="stage">\n\n' + "\n".join(secs) + TAIL, encoding="utf-8")
        print(out.name, len(secs), "slides")

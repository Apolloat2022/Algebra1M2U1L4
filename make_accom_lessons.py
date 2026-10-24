"""Build the IEP and Section 504 versions of the Lesson 4–6 decks, then their .pptx copies.

504 = the original deck (same content and rigor) plus access supports: a key-vocabulary slide,
a "today's plan" checklist after each bell work, and a "notes to keep" copy at the end of each day.
IEP = a shorter, modified deck: vocabulary, a steps anchor chart, I do / we do / you do with
sentence frames, fewer practice items, and a short exit ticket.
Both reuse the original deck's head and script, so they work as web decks too.
Also writes IEP and 504 copies of the bell work, homework and quiz pages (see practice_pages),
and a teacher answer key .pptx for each IEP / 504 bell work, homework, quiz and exit ticket (answer_key, exit_key; needs node to read the page data).
Standard library only.  Run:  python make_accom_lessons.py   (Topic 2 instead: add t2)
"""
import html as html_mod
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
LESSONS = {4: "lesson4/point-slope-form-lesson4.html", 5: "lesson5/using-linear-equations-lesson5.html",
           6: "lesson6/making-sense-of-representations-lesson6.html"}
OUT = {4: "lesson4-point-slope-form", 5: "lesson5-using-linear-equations", 6: "lesson6-representations"}
T2 = {"2.1": "t2-lesson1-transforming-linear-functions", "2.2": "t2-lesson2-vertical-horizontal-transformations",
      "2.3": "t2-lesson3-perpendicular-slopes", "2.4": "t2-lesson4-comparing-linear-functions"}
LESSONS.update({n: f"Module 2 topic 2/{stem}.html" for n, stem in T2.items()})
OUT.update(T2)
DAYS = {4: 2, 5: 3, 6: 3, "2.1": 3, "2.2": 2, "2.3": 2, "2.4": 2}


# ---------------------------------------------------------------- helpers
def sec(eyebrow, title, body, notes=""):
    return (f'<section class="slide">\n  <p class="eyebrow">{eyebrow}</p>\n  <h2>{title}</h2>\n  {body}\n'
            + (f'  <aside class="notes">{notes}</aside>\n' if notes else "") + "</section>\n")


def ans(x, sm=True):
    return f'<div class="step pop eq{" sm" if sm else ""} ans">{x}</div>'


def card(h, body, step=False):
    return f'<div class="card{" step" if step else ""}"><h3>{h}</h3>{body}</div>'


def graph(w, h, x, y, gx, gy, lines=(), pts=(), alt="", pts_step=False):
    g = dict(w=w, h=h, x=x, y=y, gx=gx, gy=gy, lines=list(lines), pts=[list(p) + [""] * (3 - len(p)) for p in pts], alt=alt)
    if pts_step:
        g["ptsStep"] = True
    return "<div class=\"graph\" data-g='" + json.dumps(g, ensure_ascii=False) + "'></div>"


# IEP decks add one graph option: a line with dot: true also plots a point at its end, on the same click (see move)
GRAPH_JS = "    if (ln.step) s += '</g>';\n"
DOT_JS = '    if (ln.dot) s += `<circle class="g-pt" cx="${X(c[1][0])}" cy="${Y(c[1][1])}" r="5.5"/>`;\n'


def row(*cols, gap=40):
    return f'<div class="row" style="gap:{gap}px">' + "".join(f'<div class="col">{c}</div>' for c in cols) + "</div>"


def vocab(*terms):  # (term, plain definition, example)
    return '<div class="grid3">' + "".join(
        card(t, f'<p class="small">{d}</p>' + (f'<div class="eq sm">{e}</div>' if e else "")) for t, d, e in terms) + "</div>"


def checklist(*items):
    return "".join(f'<p>☐ &nbsp;{it}</p>' for it in items) + \
        '<p class="warn">One part at a time. Ask for help or a break whenever you need it.</p>'


def notes_cards(*cards):
    return '<div class="grid3">' + "".join(card(h, b) for h, b in cards) + "</div>" + \
        '<p class="small muted">Copy these into your notes, or ask your teacher for a printed copy.</p>'


def links(n, days):
    pre = src(n)[1]
    bw = " · ".join(f'<b><a class="go" href="{pre}-bellwork-day{d}.html" target="_blank" onclick="event.stopPropagation()">Day {d} →</a></b>'
                    for d in range(1, days + 1))
    return (f'<p style="font-size:24px;margin-top:6px">Bell work: {bw} &nbsp;|&nbsp; Practice: '
            f'<b><a class="go" href="{pre}-homework.html" target="_blank" onclick="event.stopPropagation()">Homework →</a></b> · '
            f'<b><a class="go" href="{pre}-quiz.html" target="_blank" onclick="event.stopPropagation()">Quiz →</a></b></p>')


Y1 = '<i>y</i><sub>1</sub>'
X1 = '<i>x</i><sub>1</sub>'
PSF = f'<i>y</i> − <span class="cp">{Y1}</span> = <span class="cm"><i>m</i></span>(<i>x</i> − <span class="cp">{X1}</span>)'


# ---------------------------------------------------------------- Section 504 additions
S504 = {
 4: dict(
  vocab=vocab(
   ("Slope (<i>m</i>)", "How steep a line is: the change in <i>y</i> divided by the change in <i>x</i>.", "<i>m</i> = {{rise|run}}"),
   ("<i>y</i>-intercept", "Where the line crosses the <i>y</i>-axis. The point is (0, <i>b</i>).", "<i>y</i> = 2<i>x</i> <b class=\"cp\">+ 5</b> → (0, 5)"),
   ("Point-slope form", "An equation that uses the slope and <b>any</b> point on the line.", PSF),
   ("Horizontal line", "A flat line. Slope is 0. The equation is <i>y</i> = a number.", "<i>y</i> = 11"),
   ("Vertical line", "A straight up-and-down line. Slope is undefined. The equation is <i>x</i> = a number.", "<i>x</i> = −2"),
   ("Constant function", "The output (<i>y</i>) is always the same number.", "<i>y</i> = −6")),
  plans={1: ["Bell work (5 min)", "Getting Started: Draining the Pool", "Activity 4.1: point-slope form", "Activity 4.2: horizontal and vertical lines"],
         2: ["Bell work (5 min)", "Activity 4.3: match equations, graphs, tables and contexts", "Talk the Talk: what each equation tells you", "Exit ticket"]},
  notes={1: [("Point-slope form", f'<div class="eq sm">{PSF}</div><p class="small">Use it when you know the slope and a point.</p>'),
             ("Change to <i>y</i> = <i>mx</i> + <i>b</i>", '<p class="small">1. Distribute the slope.<br>2. Add <i>y</i><sub>1</sub> to both sides (or subtract).</p><div class="eq sm"><i>y</i> − 6 = −{{1|2}}(<i>x</i> − 2) → <i>y</i> = −{{1|2}}<i>x</i> + 7</div>'),
             ("Horizontal vs. vertical", '<p class="small"><b>Horizontal:</b> <i>y</i> = a number, slope 0.<br><b>Vertical:</b> <i>x</i> = a number, slope undefined.<br>Memory trick: HOY VUX.</p>')],
         2: [("Read slope-intercept form", '<div class="eq sm"><i>y</i> = <span class="cm">{{3|5}}</span><i>x</i> <span class="cp">− 4</span></div><p class="small">slope {{3|5}}, <i>y</i>-intercept (0, −4)</p>'),
             ("Read point-slope form", '<div class="eq sm"><i>y</i> − 6 = <span class="cm">2</span>(<i>x</i> + 1)</div><p class="small">slope 2, point (−1, 6). The signs <b>flip</b>.</p>'),
             ("In a story", '<p class="small"><b>Slope</b> = the rate (per hour, per pound, per game).<br><b><i>y</i>-intercept</b> = the starting amount.</p>')]}),
 5: dict(
  vocab=vocab(
   ("Slope as rise over run", "Rise = up (+) or down (−). Run = right (+) or left (−).", "−2 = {{−2|1}} = {{2|−1}}"),
   ("<i>y</i>-intercept", "Where the line crosses the <i>y</i>-axis: (0, <i>b</i>). Plot it first.", "<i>y</i> = −2<i>x</i> + 10 → (0, 10)"),
   ("<i>x</i>-intercept", "Where the line crosses the <i>x</i>-axis: (<i>x</i>, 0). Find it by putting 0 in for <i>y</i>.", "5<i>x</i> = 1600 → (320, 0)"),
   ("Standard form", "<i>Ax</i> + <i>By</i> = <i>C</i>, where <i>A</i>, <i>B</i> and <i>C</i> are integers.", "5<i>x</i> + 8<i>y</i> = 1600"),
   ("Point-slope form", "Uses the slope and a point on the line.", PSF),
   ("Slope-intercept form", "Uses the slope and the <i>y</i>-intercept.", "<i>y</i> = <span class=\"cm\"><i>m</i></span><i>x</i> + <span class=\"cp\"><i>b</i></span>")),
  plans={1: ["Bell work (5 min)", "Getting Started: Jump In the Line", "Activity 5.1: graph from slope-intercept form"],
         2: ["Bell work (5 min)", "Activity 5.2: graph from point-slope form", "Activity 5.3: standard form and intercepts"],
         3: ["Bell work (5 min)", "Activity 5.4: find the slope and <i>y</i>-intercept", "Talk the Talk: choose the best form", "Exit ticket"]},
  notes={1: [("Graph <i>y</i> = <i>mx</i> + <i>b</i>", '<p class="small">1. Plot (0, <i>b</i>).<br>2. Write <i>m</i> as {{rise|run}}.<br>3. Count to the next point.<br>4. Plot 3 points and connect.</p>'),
             ("Watch the scale", '<p class="small">Count <b>units</b>, not grid squares. If the axis counts by 10, up 10 is one square.</p>'),
             ("Check the direction", '<p class="small">Positive slope: rises left to right.<br>Negative slope: falls left to right.</p>')],
         2: [("Graph point-slope form", f'<p class="small">1. Plot the point ({X1}, {Y1}).<br>2. Count the slope from there.</p><div class="eq sm"><i>y</i> + 8 = {{{{1|2}}}}(<i>x</i> + 6) → (−6, −8)</div>'),
             ("Graph standard form", '<p class="small">Put <i>y</i> = 0 to find the <i>x</i>-intercept.<br>Put <i>x</i> = 0 to find the <i>y</i>-intercept.<br>Plot both and connect.</p>'),
             ("Shortcuts", '<p class="small"><i>x</i>-intercept ({{<i>C</i>|<i>A</i>}}, 0)<br><i>y</i>-intercept (0, {{<i>C</i>|<i>B</i>}})<br>slope −{{<i>A</i>|<i>B</i>}}</p>')],
         3: [("Slope-intercept", '<p class="small">Best when you know a starting amount and a rate.</p>'),
             ("Point-slope", '<p class="small">Best when you know a rate and one point that is not the start.</p>'),
             ("Standard", '<p class="small">Best when two kinds of things add up to one total.</p>')]}),
 6: dict(
  vocab=vocab(
   ("Linear function", "Its rate of change is always the same, so its graph is a straight line.", "<i>f</i>(<i>x</i>) = 2<i>x</i> + 5"),
   ("Rate of change", "Change in <i>y</i> ÷ change in <i>x</i>. For a line, this is the slope.", "{{8|2}} = 4"),
   ("Direct variation", "A line through (0, 0): <i>y</i> = <i>kx</i>.", "<i>y</i> = 2.5<i>x</i>"),
   ("General form", "<i>f</i>(<i>x</i>) = <i>ax</i> + <i>b</i>. <i>a</i> is the slope, <i>b</i> is the <i>y</i>-intercept.", "<i>G</i>(<i>t</i>) = 15<i>t</i> − 45"),
   ("Factored form", "<i>f</i>(<i>x</i>) = <i>a</i>(<i>x</i> − <i>c</i>). <i>a</i> is the slope, <i>c</i> is the zero.", "<i>G</i>(<i>t</i>) = 15(<i>t</i> − 3)"),
   ("Zero", "The <i>x</i>-value that makes <i>f</i>(<i>x</i>) = 0. The graph crosses the <i>x</i>-axis there.", "15(3 − 3) = 0 → zero is 3")),
  plans={1: ["Bell work (5 min)", "Getting Started: linear or nonlinear?", "Activity 6.1: tables whose inputs skip"],
         2: ["Bell work (5 min)", "Activity 6.2: read a graph (Gracie's T-shirts)", "Activity 6.3: general form and factored form"],
         3: ["Bell work (5 min)", "Activity 6.4: a booth fee changes the graph", "Talk the Talk", "Exit ticket"]},
  notes={1: [("Is the table linear?", '<p class="small">1. Find {{change in <i>y</i>|change in <i>x</i>}} between every pair.<br>2. Always the same → linear.</p>'),
             ("Write the function", '<p class="small">Use the slope and a point to find <i>b</i>, the value when <i>x</i> = 0.</p>'),
             ("Direct variation", '<p class="small">Only if the line passes through (0, 0): <i>y</i> = <i>kx</i>.</p>')],
         2: [("Solve with the equation", '<div class="eq sm">100 = 15<i>t</i> → <i>t</i> ≈ 6.67</div><p class="small">Then decide what makes sense: 7 shirts.</p>'),
             ("General form", '<div class="eq sm"><i>f</i>(<i>x</i>) = <span class="cm"><i>a</i></span><i>x</i> + <span class="cp"><i>b</i></span></div><p class="small"><i>a</i> = slope, <i>b</i> = <i>y</i>-intercept</p>'),
             ("Factored form", '<div class="eq sm"><i>f</i>(<i>x</i>) = <span class="cm"><i>a</i></span>(<i>x</i> − <span class="cp"><i>c</i></span>)</div><p class="small"><i>a</i> = slope, <i>c</i> = zero, (<i>c</i>, 0) = <i>x</i>-intercept</p>')],
         3: [("Same slope", '<p class="small">Parallel lines have the same slope: the price per shirt did not change.</p>'),
             ("Subtracting a fee", '<p class="small">Subtracting $35 moves the whole line <b>down</b> 35.</p>'),
             ("Three ways to write it", '<div class="eq sm"><i>F</i>(<i>t</i>) = 15<i>t</i> − 80 = 15(<i>t</i> − {{16|3}})</div>')]}),
}


def build_504(n, sections):
    a = S504[n]
    out, day = [], 0
    for s in sections:
        if 'class="slide divider"' in s or "Essential Question · Answered" in s:  # end of a day
            day += 1
            out.append(sec(f"Day {day} · Notes to Keep", f"Notes to keep: Day {day}", notes_cards(*a["notes"][day]),
                           "Section 504 support: a copy of the day's notes. Hand out a printed copy if the student's plan lists copies of notes."))
        out.append(s)
        if "Today you will" in s:
            out.append(sec(f"{src(n)[2]} · Key Vocabulary", "Key vocabulary", a["vocab"],
                           "Section 504 support: preview the key terms before the lesson. Leave this slide up or print it as a reference card."))
        m = re.search(r"Day (\d) · Bell Work", s)
        if m:
            d = int(m.group(1))
            out.append(sec(f"Day {d} · Today's Plan", "Today's plan", checklist(*a["plans"][d]),
                           "Section 504 support: chunked directions. Check off each part as the class finishes it."))
    return out


# ---------------------------------------------------------------- IEP decks
def iep_title(n, title, eq, cans, days):
    return (f'<section class="slide">\n  <p class="eyebrow">Bluebonnet Algebra I · Module 2 · {"Topic 2" if isinstance(n, str) else "Topic 1"} · Lesson {str(n)[-1]} · IEP Version</p>\n'
            f'  <h1 style="margin-top:10px;font-size:60px">{title}</h1>\n  <div class="eq" style="margin-top:4px">{eq}</div>\n'
            '  <h3 style="margin-top:8px">I can…</h3>' + "".join(f'<p>✓ &nbsp;{c}</p>' for c in cans) + "\n" + links(n, days) +
            '\n  <p class="foot">Based on Bluebonnet Learning Secondary Mathematics, Algebra I (©2024–2025 Texas Education Agency, portions ©2021 Carnegie Learning, Inc.), licensed CC BY-NC 4.0. A private site for Algebra I teachers.</p>\n'
            f'  <aside class="notes">IEP version of {src(n)[2]}: a modified lesson that keeps the core skills and cuts the number of items. Each skill follows I do (teacher models), We do (together, with sentence frames), You do (student tries, then reveal). Click to reveal each answer. The bell work for every day follows this slide (the same questions as the online bell work); skip to the current day. Apply each student\'s IEP accommodations too: extended time, read-aloud, breaks, calculator, small group.</aside>\n</section>\n')


def steps(*items):
    return "".join(f'<p><b>{k}.</b> {t}</p>' for k, t in enumerate(items, 1))


def walk(title, *probs):  # probs: (problem, [step, ...], answer). One click per step, so students see every move.
    cards = [card(p, "".join(f'<p class="step small"><b>Step {k}.</b> {t}</p>' for k, t in enumerate(st, 1)) + ans(a))
             for p, st, a in probs]
    return sec("Check it · Step by step", title, row(*cards, gap=24),
               "For the teacher or assistant: click once for each step. Read the step aloud, and before each click ask "
               "the student what to do next. Students check their own paper and fix any mistake in a different color.")


def mt(s):  # page-data math [[...]] -> deck markup, the same rule as mc.js
    return re.sub(r"\[\[(.+?)\]\]", lambda m: '<span class="mt">' + re.sub(r"[A-Za-z]", r"<i>\g<0></i>", m.group(1)) + "</span>", s)


def move(pts, dy=0, dx=0, label=""):  # dashed arrows from each point to its moved copy, one click each, a dot at the end
    return [dict(p=[[x, y], [x + dx, y + dy]], seg=True, dash=True, step=True, dot=True, c="b", label=label) for x, y in pts]


def bell_steps(n, day, data):  # the general bell work questions with the IEP formula and worked steps (BELL)
    return [{**q, "formula": f, "steps": st} for q, (f, st) in zip(data, BELL[n, day])]


def bell_slides(n):  # IEP bell work: same questions as the general deck, plus a formula and the worked steps
    d, pre, _ = src(n)
    out = []
    for f in sorted(d.glob(f"{pre}-bellwork-day*.html")):
        day = int(f.stem[-1])
        cards = [f'<div class="card" style="padding:10px 18px;gap:4px"><p class="small"><b>{k}.</b> {mt(q["q"])}</p>'
                 f'<p class="small" style="color:var(--point)"><b>Formula:</b> {mt(q["formula"])}</p>'
                 f'<div class="step pop ans" style="font-size:19px;line-height:1.35;padding:6px 14px"><b>{mt(q["choices"][0])}</b>'
                 + "".join(f"<br><b>{j}.</b> {mt(t)}" for j, t in enumerate(q["steps"], 1)) + "</div></div>"
                 for k, q in enumerate(bell_steps(n, day, page_data(f)), 1)]
        out.append(sec(f"Day {day} · Bell Work · Review", "Warm up: work these on your own", row("".join(cards[:2]), "".join(cards[2:]), gap=24),
                       f"Have this up as students walk in (about 5 minutes). The same 4 questions are on the online IEP Day {day} bell work, "
                       "which shows the same formula under each question and these steps after each answer. Click to reveal one answer at a time; "
                       "read each step aloud and point to where the formula is used."))
    return out


# formula and worked steps for every Topic 2 bell work question, in page-data math [[...]]
SLOPE = "[[m = (y₂ − y₁) ÷ (x₂ − x₁)]]"
BELL = {
 ("2.1", 1): [(SLOPE, ["Label the points: [[(x₁, y₁) = (1, 2)]] and [[(x₂, y₂) = (4, 11)]].", "Subtract the [[y]]-values: [[11 − 2 = 9]]. Subtract the [[x]]-values: [[4 − 1 = 3]].", "Divide: [[9 ÷ 3 = 3]]."]),
              ("[[y = mx + b]], [[y]]-intercept [[(0, b)]]", ["Match [[y = 3x − 7]] to [[y = mx + b]]: [[m = 3]] and [[b = −7]].", "The [[y]]-intercept is [[(0, b) = (0, −7)]]."]),
              ("put the number in for [[x]]", ["Replace [[x]] with [[(−3)]]: [[f(−3) = 2(−3) + 1]].", "Multiply: [[2(−3) = −6]].", "Add: [[−6 + 1 = −5]]."]),
              ("parallel: same slope · [[y = mx + b]]", ["Parallel to [[y = 3x + 1]] means the same slope: [[m = 3]].", "Put in the point [[(1, 5)]]: [[5 = 3(1) + b]].", "[[5 = 3 + b]], so [[b = 2]]: [[y = 3x + 2]]."])],
 ("2.1", 2): [("up [[d]]: [[g(x) = f(x) + d]]", ["Up 4 means add 4 to every output: [[g(x) = f(x) + 4]].", "Replace [[f(x)]] with [[x]]: [[g(x) = x + 4]]."]),
              ("down [[d]]: [[(x, y) → (x, y − d)]]", ["[[x]] stays the same: [[x = 2]].", "Down 3, so subtract 3 from [[y]]: [[5 − 3 = 2]].", "The new point is [[(2, 2)]]."]),
              ("moving up or down does not change the slope", ["[[g(x) = 2x − 1 + 6 = 2x + 5]].", "The number with [[x]] is still 2, so the slope is 2."]),
              ("outside: + moves up, − moves down", ["The [[− 2]] is outside [[f(x)]]: it changes every output ([[y]]-value).", "Minus means down: a translation down 2 units."])],
 ("2.1", 3): [("for [[f(x) = x]], [[a · f(x) = ax]] has slope [[a]]", ["Replace [[f(x)]] with [[x]]: [[g(x) = 3x]].", "The number with [[x]] is 3, so the slope is 3."]),
              ("[[a · f(x)]]: [[|a| > 1]] stretches, [[a < 0]] flips", ["[[a = −2]]. The size, 2, is more than 1: stretched by 2.", "The sign is negative: reflected (flipped) across the [[x]]-axis."]),
              ("[[a · f(x)]]: [[0 < a < 1]] compresses", ["Look for a number between 0 and 1 in front of [[f(x)]].", "[[½]] is between 0 and 1, so [[g(x) = ½f(x)]] compresses."]),
              ("[[a · f(x)]]: [[a < 0]] reflects, [[|a| > 1]] stretches", ["Reflect: [[a]] is negative. Factor of 2: [[|a| = 2]].", "So [[a = −2]] and [[g(x) = −2x]]."])],
 ("2.2", 1): [("outside: + moves up, − moves down", ["The [[−3]] is outside [[f(x)]], so the graph moves up or down.", "Minus means down: down 3 units."]),
              ("[[y = mx + b]], slope [[m]]", ["Match [[g(x) = 3x − 8]] to [[y = mx + b]].", "[[m = 3]], so the slope is 3."]),
              ("[[x]]-intercept: set [[g(x) = 0]] and solve", ["[[3x − 8 = 0]].", "Add 8 to both sides: [[3x = 8]].", "Divide both sides by 3: [[x = 8/3]]. The point is [[(8/3, 0)]]."]),
              ("replace [[f(x)]] with [[x]]", ["[[g(x) = 2f(x) − 3]].", "Put in [[x]] for [[f(x)]]: [[g(x) = 2x − 3]].", "Slope 2 (dilation by 2), [[y]]-intercept [[−3]] (down 3)."])],
 ("2.2", 2): [("right [[c]]: [[g(x) = f(x − c)]]", ["Right 5 means subtract 5 inside: [[f(x − 5)]].", "For [[f(x) = x]]: [[f(x − 5) = x − 5]]."]),
              ("for [[f(x) = x]] only: right [[n]] = down [[n]]", ["Right 5: [[f(x − 5) = x − 5]].", "Down 5: [[f(x) − 5 = x − 5]].", "Same equation, so the same graph: down 5."]),
              ("put [[(x + 4)]] in for [[x]], then distribute", ["[[r(x) = 2(x + 4) − 1]].", "Distribute: [[2 · x + 2 · 4 = 2x + 8]].", "Combine: [[2x + 8 − 1 = 2x + 7]]."]),
              ("right [[c]]: [[f(x − c)]], then distribute", ["Right 2: [[g(x) = f(x − 2) = 3(x − 2)]].", "Distribute: [[3 · x − 3 · 2 = 3x − 6]].", "[[g(x) = 3x − 6]]."])],
 ("2.3", 1): [("reciprocal: flip the fraction", ["[[⅔]] has 2 on top and 3 on the bottom. Flip them: [[3/2]].", "Check: [[⅔ · 3/2 = 1]]."]),
              ("90° counterclockwise: [[(x, y) → (−y, x)]]", ["[[x = 8]] and [[y = 5]].", "[[(−y, x) = (−5, 8)]]."]),
              (SLOPE, ["Subtract the [[y]]-values: [[5 − 0 = 5]].", "Subtract the [[x]]-values: [[8 − 0 = 8]].", "Divide: [[5 ÷ 8 = 5/8]]."]),
              (SLOPE, ["Label the points: [[(x₁, y₁) = (−1, 4)]] and [[(x₂, y₂) = (2, −2)]].", "Subtract the [[y]]-values: [[−2 − 4 = −6]]. Subtract the [[x]]-values: [[2 − (−1) = 3]].", "Divide: [[−6 ÷ 3 = −2]]."])],
 ("2.3", 2): [("perpendicular: flip and change the sign", ["Flip [[⅔]]: [[3/2]].", "Change the sign: [[−3/2]].", "Check: [[⅔ · (−3/2) = −1]]."]),
              ("slope = rise ÷ run", ["A horizontal line is flat: it never goes up or down, so the rise is 0.", "[[0 ÷ run = 0]]. The slope is 0."]),
              ("vertical line: [[x =]] a number", ["On a vertical line, [[x]] never changes.", "The point has [[x = 2]], so the line is [[x = 2]]."]),
              ("perpendicular: flip and change the sign · [[y = mx + b]]", ["Slope of [[y = 2x + 3]] is 2. Flip and change the sign: [[−½]].", "Put in [[(4, 1)]]: [[1 = −½(4) + b = −2 + b]].", "[[b = 3]]: [[y = −½x + 3]]."])],
 ("2.4", 1): [(SLOPE, ["Subtract the [[y]]-values: [[4 − (−6) = 4 + 6 = 10]].", "Subtract the [[x]]-values: [[0 − (−2.5) = 2.5]].", "Divide: [[10 ÷ 2.5 = 4]]."]),
              ("parallel lines have the same slope", ["The slope of [[y = 4x − 3]] is 4, the number with [[x]].", "A parallel line has the same slope: 4."]),
              ("perpendicular: flip and change the sign", ["[[4 = 4/1]]. Flip it: [[1/4]].", "Change the sign: [[−¼]].", "Check: [[4 · (−¼) = −1]]."]),
              (SLOPE, ["Slope of [[p]]: [[(4 − 1) ÷ (4 − 0) = 3/4 = 0.75]].", "Compare each slope with 0.75: [[1]], [[0.5]], [[0.75]] ([[3x − 4y = 8]] is [[y = ¾x − 2]]), [[0.7]].", "Only 1 is greater: [[y = x − 2]]."])],
 ("2.4", 2): [("total = rate × amount", ["Rate: $15 per ton. Amount: 3 tons.", "[[15 · 3 = 45]], so $45."]),
              (SLOPE, ["Change in [[y]]: [[20 − 0 = 20]]. Change in [[x]]: [[1 − 0 = 1]].", "[[20 ÷ 1 = 20]], so $20 per ton."]),
              ("put the number in for [[x]]", ["[[J(10) = 9/5 · 10 + 32]].", "Multiply: [[9/5 · 10 = 90 ÷ 5 = 18]].", "Add: [[18 + 32 = 50]]. 10°C is 50°F."]),
              ("range = the outputs", ["The output is [[w(t)]], the gallons left.", "Most: 200 gallons at the start. Least: 0 gallons, when [[200 − 10t = 0]] at [[t = 20]].", "Range: [[0 ≤ w(t) ≤ 200]]."])]}


def exit_and_practice(n, qs):
    if isinstance(n, str):  # Topic 2: side by side, the answer then one click per worked step (EXIT_WORK)
        body = row(*[f'<div class="card"><p>{q}</p>{ans(a)}' + "".join(f'<p class="step small"><b>{j}.</b> {t}</p>' for j, t in enumerate(w, 1))
                     + '</div>' for (q, a), w in zip(qs, EXIT_WORK[n])], gap=20)
        tip = " After each answer, click once per step and read it aloud so students can find where their work went wrong."
    else:
        body, tip = '<div class="col">' + "".join(f'<div class="card"><p>{q}</p>{ans(a)}</div>' for q, a in qs) + "</div>", ""
    return [sec("Exit Ticket", "Show what you know", body,
                "Give students time to try all items before revealing. Students may use the steps slide and their notes." + tip),
            sec("Practice Online", "Bell work, homework and quiz",
                links(n, DAYS[n]) + '<p class="small">The IEP pages have 3 answer choices, 6 homework and quiz questions, a reminder card and read-aloud. '
                'Allow notes and a calculator, and give extended time as the IEP lists.</p>')]


def iep4():
    s = [iep_title(4, "Point-Slope Form", PSF, [
        "write an equation when I know the slope and one point.",
        "change point-slope form into <i>y</i> = <i>mx</i> + <i>b</i>.",
        "write equations for horizontal and vertical lines."], 2)]
    s.append(sec("Lesson 4 · Vocabulary", "Words we need", vocab(
        ("Slope (<i>m</i>)", "How steep the line is.", "<i>m</i> = {{change in <i>y</i>|change in <i>x</i>}}"),
        ("A point", "A place on the line, written (<i>x</i>, <i>y</i>).", "(<span class=\"cp\">1</span>, <span class=\"cp\">4</span>)"),
        ("Point-slope form", "An equation made from the slope and one point.", PSF)),
        "Read each word aloud. Students copy them onto their vocabulary card."))
    s.append(sec("Lesson 4 · Steps", "How to write point-slope form", steps(
        "Find the slope, <b class=\"cm\"><i>m</i></b>.",
        f"Find a point, (<span class=\"cp\">{X1}</span>, <span class=\"cp\">{Y1}</span>).",
        f"Put them into {PSF}.",
        "Check the signs: <i>x</i> − (−4) becomes <i>x</i> + 4."), "Leave this slide up, or give students a printed copy, while they work."))
    s.append(sec("I do · Watch me", "Slope 3, point (1, 4)", row(
        '<p>Step 1: <span class="cm"><i>m</i> = 3</span></p><p>Step 2: <span class="cp"><i>x</i><sub>1</sub> = 1, <i>y</i><sub>1</sub> = 4</span></p><p>Step 3: put them in.</p>'
        + ans('<i>y</i> − <span class="cp">4</span> = <span class="cm">3</span>(<i>x</i> − <span class="cp">1</span>)', False),
        graph(340, 360, [-2, 4], [-4, 10], [1, 1], [1, 2], [dict(p=[[1, 4], [2, 7]], step=True)], [[1, 4, "(1, 4)"]], "Line through (1, 4) with slope 3")),
        "Think aloud: orange is the slope, blue is the point. The point goes in with a minus sign."))
    s.append(sec("We do · Together", "Slope −8, point (3, 12)",
                 '<p><i>m</i> = ____ &nbsp; <i>x</i><sub>1</sub> = ____ &nbsp; <i>y</i><sub>1</sub> = ____</p>' + ans('<i>m</i> = −8, &nbsp;<i>x</i><sub>1</sub> = 3, &nbsp;<i>y</i><sub>1</sub> = 12')
                 + '<p><i>y</i> − ____ = ____(<i>x</i> − ____)</p>' + ans('<i>y</i> − 12 = −8(<i>x</i> − 3)'),
                 "Students fill in the blanks on their paper first, then reveal."))
    s.append(sec("You do · Try it", "Write each in point-slope form", row(
        '<div class="card"><p>1. Slope 5, point (2, −1)</p><p class="small">Tip: <i>y</i> − (−1) = <i>y</i> + 1</p>' + ans('<i>y</i> + 1 = 5(<i>x</i> − 2)') + '</div>',
        '<div class="card"><p>2. Slope {{2|3}}, point (−4, 5)</p><p class="small">Tip: <i>x</i> − (−4) = <i>x</i> + 4</p>' + ans('<i>y</i> − 5 = {{2|3}}(<i>x</i> + 4)') + '</div>')))
    s.append(sec("We do · Two points", "A line through (2, 5) and (4, 11)",
                 '<p>Step 1: slope. &nbsp;<i>m</i> = {{11 − 5|4 − 2}} = ____</p>' + ans('<i>m</i> = {{6|2}} = 3')
                 + '<p>Step 2: use the point (2, 5).</p><p><i>y</i> − ____ = ____(<i>x</i> − ____)</p>' + ans('<i>y</i> − 5 = 3(<i>x</i> − 2)'),
                 "When there is no slope given, find it first with the slope formula."))
    s.append(sec("I do · Change the form", "Rewrite as <i>y</i> = <i>mx</i> + <i>b</i>",
                 '<div class="eq"><i>y</i> − 5 = 3(<i>x</i> − 2)</div><p>Step 1: distribute the 3.</p>' + ans('<i>y</i> − 5 = 3<i>x</i> − 6')
                 + '<p>Step 2: add 5 to both sides.</p>' + ans('<i>y</i> = 3<i>x</i> − 1'),
                 "Same line, two forms. Slope-intercept form shows where it crosses the y-axis: (0, −1)."))
    s.append(sec("You do · Try it", "Rewrite as <i>y</i> = <i>mx</i> + <i>b</i>",
                 '<div class="eq"><i>y</i> − 3 = 5(<i>x</i> + 2)</div><p>Step 1: distribute. &nbsp;<i>y</i> − 3 = ____</p>' + ans('<i>y</i> − 3 = 5<i>x</i> + 10')
                 + '<p>Step 2: add 3. &nbsp;<i>y</i> = ____</p>' + ans('<i>y</i> = 5<i>x</i> + 13')))
    s.append(sec("Lesson 4 · Horizontal and Vertical", "Flat lines and straight-up lines", row(
        card("Horizontal", '<p class="small"><i>y</i> stays the same. Slope = <b>0</b>.</p><div class="eq sm"><i>y</i> = 3</div>')
        + graph(300, 230, [-4, 4], [-1, 5], [1, 1], [1, 1], [dict(p=[[-4, 3], [4, 3]], label="y = 3")]),
        card("Vertical", '<p class="small"><i>x</i> stays the same. Slope is <b>undefined</b>.</p><div class="eq sm"><i>x</i> = −2</div>')
        + graph(300, 230, [-4, 4], [-3, 3], [1, 1], [1, 1], [dict(p=[[-2, -3], [-2, 3]], label="x = −2")])),
        "Memory trick from the lesson: HOY VUX. Horizontal, zerO slope, y = a number. Vertical, Undefined slope, x = a number."))
    s.append(sec("You do · Try it", "Horizontal and vertical lines", row(
        '<div class="card"><p>1. The <i>y</i>-values are all 11.</p><table class="tbl" style="font-size:24px"><tr><th>x</th><th>y</th></tr><tr><td>−7</td><td>11</td></tr><tr><td>−2</td><td>11</td></tr><tr><td>0</td><td>11</td></tr></table>' + ans('<i>y</i> = 11') + '</div>',
        '<div class="card"><p>2. Through (−3, 8)</p><p class="small">Horizontal: <i>y</i> = ____</p>' + ans('<i>y</i> = 8') + '<p class="small">Vertical: <i>x</i> = ____</p>' + ans('<i>x</i> = −3') + '</div>')))
    s += exit_and_practice(4, [("1. Slope 4, point (1, 6). Write point-slope form.", "<i>y</i> − 6 = 4(<i>x</i> − 1)"),
                               ("2. Rewrite #1 as <i>y</i> = <i>mx</i> + <i>b</i>.", "<i>y</i> = 4<i>x</i> + 2"),
                               ("3. A line through (4, 1) and (4, −7). Horizontal or vertical? Write its equation.", "<i>x</i> = 4 · vertical")])
    return s


def iep5():
    s = [iep_title(5, "Graphing Linear Equations", "<i>y</i> = <i>mx</i> + <i>b</i> · " + PSF + " · <i>Ax</i> + <i>By</i> = <i>C</i>", [
        "graph a line from <i>y</i> = <i>mx</i> + <i>b</i> using the <i>y</i>-intercept and the slope.",
        "graph a line from point-slope form.",
        "find the intercepts of <i>Ax</i> + <i>By</i> = <i>C</i> and graph the line."], 3)]
    s.append(sec("Lesson 5 · Vocabulary", "Words we need", vocab(
        ("<i>y</i>-intercept", "Where the line crosses the <i>y</i>-axis: (0, <i>b</i>).", "<i>y</i> = 2<i>x</i> <span class=\"cp\">+ 5</span> → (0, 5)"),
        ("Rise over run", "Rise: up (+) or down (−). Run: right.", "<i>m</i> = {{3|2}}: up 3, right 2"),
        ("<i>x</i>-intercept", "Where the line crosses the <i>x</i>-axis: (<i>x</i>, 0).", "Put 0 in for <i>y</i>."),
        ("Standard form", "<i>Ax</i> + <i>By</i> = <i>C</i>", "3<i>x</i> + 2<i>y</i> = 12"),
        ("Slope-intercept form", "<i>m</i> is the slope, <i>b</i> is the <i>y</i>-intercept.", "<i>y</i> = <span class=\"cm\"><i>m</i></span><i>x</i> + <span class=\"cp\"><i>b</i></span>"),
        ("Point-slope form", "Slope and one point.", PSF))))
    s.append(sec("Lesson 5 · Steps", "How to graph <i>y</i> = <i>mx</i> + <i>b</i>", steps(
        "Plot the <i>y</i>-intercept, (0, <i>b</i>).",
        "Write the slope as {{rise|run}}.",
        "From the point, count the rise (up or down), then the run (right). Plot a point.",
        "Do it again, so you have 3 points. Connect them with a ruler."), "Leave this slide up, or give students a printed copy, while they work."))
    s.append(sec("I do · Watch me", "Graph <i>y</i> = −2<i>x</i> + 10", row(
        '<p>Step 1: <i>b</i> = 10. Plot (0, 10).</p><p>Step 2: <i>m</i> = {{−2|1}}: down 2, right 1.</p>' + ans('(1, 8) and (2, 6)') + '<p>Step 3: connect with a ruler.</p>',
        graph(340, 380, [-1, 6], [0, 12], [1, 1], [1, 2], [dict(p=[[0, 10], [2, 6]], step=True)], [[0, 10, "(0, 10)"], [1, 8, "(1, 8)"], [2, 6, "(2, 6)"]], "y = −2x + 10", True)),
        "Point to each point as it appears. Negative slope: the line falls left to right."))
    s.append(sec("We do · Together", "Graph <i>y</i> = {{3|2}}<i>x</i> − 1", row(
        '<p>Plot (0, ____).</p>' + ans('(0, −1)') + '<p>Rise ____, run ____.</p>' + ans('up 3, right 2') + '<p>Next points:</p>' + ans('(2, 2) and (4, 5)'),
        graph(340, 380, [-2, 6], [-3, 7], [1, 1], [1, 1], [dict(p=[[0, -1], [4, 5]], step=True)], [[0, -1, "(0, −1)"], [2, 2, "(2, 2)"], [4, 5, "(4, 5)"]], "y = 3/2 x − 1", True))))
    s.append(sec("You do · Try it", "Graph <i>y</i> = −{{1|3}}<i>x</i> + 4", row(
        '<p>Start at (0, ____).</p>' + ans('(0, 4)') + '<p>Down ____, right ____.</p>' + ans('down 1, right 3') + '<p>Two more points:</p>' + ans('(3, 3) and (6, 2)'),
        graph(340, 340, [-1, 7], [0, 6], [1, 1], [1, 1], [dict(p=[[0, 4], [6, 2]], step=True)], [[0, 4, "(0, 4)"], [3, 3, "(3, 3)"], [6, 2, "(6, 2)"]], "y = −1/3 x + 4", True))))
    s.append(sec("I do · Point-slope form", "Graph <i>y</i> + 8 = {{1|2}}(<i>x</i> + 6)", row(
        '<p>Step 1: find the point. The signs <b>flip</b>.</p>' + ans('(−6, −8)') + '<p>Step 2: <i>m</i> = {{1|2}}: up 1, right 2.</p>' + ans('(−4, −7) and (−2, −6)'),
        graph(340, 340, [-8, 0], [-10, -4], [1, 1], [1, 1], [dict(p=[[-6, -8], [-2, -6]], step=True)], [[-6, -8, "(−6, −8)"], [-4, -7, ""], [-2, -6, ""]], "Line through (−6, −8) with slope 1/2", True)),
        "Start at the point instead of the y-intercept; everything else is the same."))
    s.append(sec("I do · Standard form", "Graph 3<i>x</i> + 2<i>y</i> = 12", row(
        '<p><i>x</i>-intercept: put <i>y</i> = 0.<br>3<i>x</i> = 12, so <i>x</i> = 4.</p>' + ans('(4, 0)')
        + '<p><i>y</i>-intercept: put <i>x</i> = 0.<br>2<i>y</i> = 12, so <i>y</i> = 6.</p>' + ans('(0, 6)') + '<p>Connect the two points.</p>',
        graph(320, 340, [-1, 6], [-1, 8], [1, 1], [1, 1], [dict(p=[[4, 0], [0, 6]], step=True)], [[4, 0, "(4, 0)"], [0, 6, "(0, 6)"]], "3x + 2y = 12", True)),
        "Cover the x-term to find the y-intercept, and cover the y-term to find the x-intercept."))
    s.append(sec("You do · Try it", "Find the intercepts of 2<i>x</i> + 5<i>y</i> = 20",
                 '<p><i>y</i> = 0: &nbsp;2<i>x</i> = 20, so <i>x</i> = ____</p>' + ans('(10, 0)')
                 + '<p><i>x</i> = 0: &nbsp;5<i>y</i> = 20, so <i>y</i> = ____</p>' + ans('(0, 4)')))
    s.append(sec("Lesson 5 · Which form?", "Where do I start?", '<div class="grid3">'
                 + card("<i>y</i> = <i>mx</i> + <i>b</i>", '<p class="small">Start at (0, <i>b</i>). Count the slope.</p>')
                 + card("Point-slope", f'<p class="small">Start at ({X1}, {Y1}). Count the slope.</p>')
                 + card("<i>Ax</i> + <i>By</i> = <i>C</i>", '<p class="small">Find both intercepts. Connect them.</p>') + "</div>"))
    s += exit_and_practice(5, [("1. <i>y</i> = −{{3|4}}<i>x</i> + 2. Name the <i>y</i>-intercept and one more point.", "(0, 2), then down 3, right 4: (4, −1)"),
                               ("2. Find the intercepts of <i>x</i> + 2<i>y</i> = 8.", "(8, 0) and (0, 4)"),
                               ("3. Name the point and slope of <i>y</i> − 1 = 2(<i>x</i> + 3).", "point (−3, 1), slope 2")])
    return s


def iep6():
    s = [iep_title(6, "Making Sense of Linear Functions", "<i>f</i>(<i>x</i>) = <i>ax</i> + <i>b</i> · <i>f</i>(<i>x</i>) = <i>a</i>(<i>x</i> − <i>c</i>)", [
        "tell whether a table is linear.",
        "write a linear function from a table.",
        "explain what the slope and the intercepts mean in a story.",
        "find the zero from factored form."], 3)]
    s.append(sec("Lesson 6 · Vocabulary", "Words we need", vocab(
        ("Linear function", "The rate of change is always the same. The graph is a straight line.", ""),
        ("Rate of change", "Change in <i>y</i> ÷ change in <i>x</i>. It is the slope.", "{{8|2}} = 4"),
        ("General form", "<i>a</i> = slope, <i>b</i> = <i>y</i>-intercept", "<i>f</i>(<i>x</i>) = <span class=\"cm\"><i>a</i></span><i>x</i> + <span class=\"cp\"><i>b</i></span>"),
        ("Factored form", "<i>a</i> = slope, <i>c</i> = zero", "<i>f</i>(<i>x</i>) = <span class=\"cm\"><i>a</i></span>(<i>x</i> − <span class=\"cp\"><i>c</i></span>)"),
        ("Zero", "The <i>x</i> that makes <i>f</i>(<i>x</i>) = 0. The line crosses the <i>x</i>-axis there.", ""),
        ("Direct variation", "A line through (0, 0).", "<i>y</i> = <i>kx</i>"))))
    s.append(sec("Lesson 6 · Steps", "Is the table linear?", steps(
        "Find the change in <i>y</i> and the change in <i>x</i> between each pair of rows.",
        "Divide: {{change in <i>y</i>|change in <i>x</i>}}.",
        "Always the same number → <b>linear</b>. Different → <b>not linear</b>.",
        "If linear, find <i>b</i> (the <i>y</i>-value when <i>x</i> = 0) and write <i>f</i>(<i>x</i>) = <i>ax</i> + <i>b</i>."),
        "Leave this slide up, or give students a printed copy, while they work."))
    tb = lambda xs, ys: '<table class="tbl" style="font-size:26px"><tr><th>x</th><th>y</th></tr>' + "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in zip(xs, ys)) + "</table>"
    s.append(sec("I do · Watch me", "Is this table linear?", row(
        tb([0, 2, 4, 6], [5, 9, 13, 17]),
        '<p>Each row: <i>x</i> goes up 2, <i>y</i> goes up 4.</p><p>{{4|2}} = 2 every time.</p>' + ans('Linear, slope 2') + '<p>At <i>x</i> = 0, <i>y</i> = 5.</p>' + ans('<i>f</i>(<i>x</i>) = 2<i>x</i> + 5')),
        "Model the division for every pair, not just the first one."))
    s.append(sec("We do · Together", "Is this table linear?", row(
        tb([1, 2, 3, 4], [3, 6, 12, 24]),
        '<p>Change in <i>y</i>: 3, ____, ____</p>' + ans('3, 6, 12') + '<p>Is it the same every time?</p>' + ans('No, so it is not linear.'))))
    s.append(sec("You do · Try it", "Nakota sells pretzels", row(
        '<table class="tbl" style="font-size:26px"><tr><th style="font-style:normal">Pretzels</th><th style="font-style:normal">Money ($)</th></tr><tr><td>0</td><td>0</td></tr><tr><td>2</td><td>5</td></tr><tr><td>4</td><td>10</td></tr><tr><td>6</td><td>15</td></tr></table>',
        '<p>1. Rate: {{5|2}} = ____ dollars per pretzel</p>' + ans('2.5') + '<p>2. Write the function: <i>y</i> = ____<i>x</i></p>' + ans('<i>y</i> = 2.5<i>x</i>')
        + '<p>3. Money for 10 pretzels: ____</p>' + ans('$25'))))
    s.append(sec("I do · Meaning in a story", "Gracie sells T-shirts for $15 each",
                 '<div class="eq"><i>E</i>(<i>t</i>) = 15<i>t</i></div>'
                 + '<p><b class="cm">15</b> means: she earns $15 for each shirt (the slope).</p>'
                 + '<p>How many shirts to earn $100? &nbsp;100 = 15<i>t</i></p>' + ans('<i>t</i> = {{100|15}} ≈ 6.67')
                 + '<p>She can\'t sell part of a shirt, so she must sell ____ shirts.</p>' + ans('7 shirts'),
                 "Round up: 6 shirts only earns $90."))
    s.append(sec("We do · Two forms", "Gracie gives away 3 shirts", row(
        card("General form", '<div class="eq sm"><i>G</i>(<i>t</i>) = <span class="cm">15</span><i>t</i> <span class="cp">− 45</span></div><p class="small">slope: ____ &nbsp; <i>y</i>-intercept: ____</p>' + ans('15 and (0, −45)'))
        + card("Factored form", '<div class="eq sm"><i>G</i>(<i>t</i>) = <span class="cm">15</span>(<i>t</i> <span class="cp">− 3</span>)</div><p class="small">slope: ____ &nbsp; zero: ____</p>' + ans('15 and 3')),
        graph(340, 380, [-1, 8], [-60, 60], [1, 1], [10, 20], [dict(p=[[0, -45], [6, 45]], step=True)], [[0, -45, "(0, −45)"], [3, 0, "(3, 0)"]], "G(t) = 15t − 45")),
        "Check that both forms are the same: distribute 15(t − 3) = 15t − 45. The zero, 3, means she must sell 3 shirts just to break even."))
    s.append(sec("You do · Try it", "Find the slope and the zero", row(
        '<div class="card"><div class="eq sm"><i>f</i>(<i>x</i>) = 2(<i>x</i> − 4)</div><p>slope ____ &nbsp; zero ____</p>' + ans('slope 2, zero 4') + '</div>',
        '<div class="card"><div class="eq sm"><i>f</i>(<i>x</i>) = 3(<i>x</i> − 7)</div><p>slope ____ &nbsp; zero ____</p>' + ans('slope 3, zero 7') + '<p class="small">General form: 3<i>x</i> − ____</p>' + ans('3<i>x</i> − 21') + '</div>')))
    s += exit_and_practice(6, [("1. Is the table linear? <i>x</i>: 1, 3, 7 &nbsp; <i>y</i>: 4, 10, 22. If yes, write the function.", "Yes, slope 3: <i>f</i>(<i>x</i>) = 3<i>x</i> + 1"),
                               ("2. What is the zero of <i>f</i>(<i>x</i>) = 4(<i>x</i> − 5)?", "5"),
                               ("3. Bracelets sell for $10 each. The booth costs $30: <i>f</i>(<i>x</i>) = 10<i>x</i> − 30. What does the 10 mean?", "$10 earned for each bracelet (the slope)")])
    return s


IEP = {4: iep4, 5: iep5, 6: iep6}


# ---------------------------------------------------------------- Topic 2 (Section 504 additions and IEP decks)
FX = "<i>f</i>(<i>x</i>)"
S504.update({
 "2.1": dict(
  vocab=vocab(
   ("Parent function", "The simplest function of its type.", f"{FX} = <i>x</i>"),
   ("Transformation", "A change to a graph: move it, stretch it, or flip it.", ""),
   ("Vertical translation", "Moves the graph up or down <i>d</i> units. Same slope.", f"{FX} <span class=\"cp\">+ 5</span>"),
   ("Vertical dilation", "Stretches or compresses the graph. Changes the slope.", f"<span class=\"cm\">3</span> · {FX}"),
   ("Reflection", "Flips the graph across the <i>x</i>-axis (a negative factor).", f"−{FX}"),
   ("Parallel lines", "Lines with the same slope that never meet.", "<i>y</i> = 2<i>x</i> + 3, <i>y</i> = 2<i>x</i> − 5")),
  plans={1: ["Bell work (5 min)", "Getting Started: move the points on the floor", "Activity 1.1: translate up and down"],
         2: ["Bell work (5 min)", "Activity 1.2: parallel lines", "Activity 1.3: stretch and compress"],
         3: ["Bell work (5 min)", "Activity 1.4: describe and graph", "Activity 1.5: hit the targets", "Talk the Talk", "Exit ticket"]},
  notes={1: [("Translation", f'<div class="eq sm">{FX} <span class="cp">+ <i>d</i></span></div><p class="small">Up when <i>d</i> &gt; 0, down when <i>d</i> &lt; 0.</p>'),
             ("What changes?", '<p class="small">The <i>y</i>-intercept moves.<br>The slope stays the same.</p>'),
             ("Parallel", '<p class="small">A line and its translation are parallel: same slope, never meet.</p>')],
         2: [("Parallel line through a point", '<p class="small">1. Keep the slope.<br>2. Put the point into <i>y</i> = <i>mx</i> + <i>b</i>.<br>3. Solve for <i>b</i>.</p>'),
             ("Dilation", f'<div class="eq sm"><span class="cm"><i>a</i></span> · {FX}</div><p class="small">|<i>a</i>| &gt; 1 stretches. 0 &lt; |<i>a</i>| &lt; 1 compresses. <i>a</i> &lt; 0 reflects.</p>'),
             ("For <i>f</i>(<i>x</i>) = <i>x</i>", '<p class="small"><i>a</i> · <i>f</i>(<i>x</i>) = <i>ax</i>: the slope becomes <i>a</i>.</p>')],
         3: [("Both together", f'<div class="eq sm"><span class="cm"><i>a</i></span> · {FX} <span class="cp">+ <i>d</i></span></div><p class="small">slope <i>a</i>, <i>y</i>-intercept (0, <i>d</i>)</p>'),
             ("To graph", '<p class="small">1. Plot (0, <i>d</i>).<br>2. Count the slope <i>a</i>.</p>'),
             ("Check a target", '<p class="small">Put the target\'s <i>x</i> into the equation. Do you get its <i>y</i>?</p>')]}),
 "2.2": dict(
  vocab=vocab(
   ("Input", "The <i>x</i>-value you put in.", ""),
   ("Output", f"The value that comes out, {FX} or <i>y</i>.", ""),
   ("Horizontal translation", "Moves the graph left or right.", f"<i>f</i>(<i>x</i> <span class=\"cp\">− 3</span>): right 3"),
   ("Horizontal dilation", "Stretches or compresses the graph toward the <i>y</i>-axis.", "<i>f</i>(<span class=\"cm\">2</span><i>x</i>)"),
   ("Inside vs. outside", "Inside the parentheses: input. Outside: output.", ""),
   ("Counterexample", "One example that shows a rule is not always true.", "")),
  plans={1: ["Bell work (5 min)", "Getting Started: key characteristics", "Activity 2.1: horizontal vs. vertical translations"],
         2: ["Bell work (5 min)", "Activity 2.2: horizontal vs. vertical dilations", "Activity 2.3: describe and graph", "Talk the Talk", "Exit ticket"]},
  notes={1: [("Horizontal", '<div class="eq sm"><i>f</i>(<i>x</i> − <span class="cp"><i>c</i></span>)</div><p class="small">Right <i>c</i>. The sign flips: <i>f</i>(<i>x</i> + 3) is left 3.</p>'),
             ("Vertical", f'<div class="eq sm">{FX} + <span class="cp"><i>d</i></span></div><p class="small">Up <i>d</i>. No sign flip.</p>'),
             ("Only for <i>f</i>(<i>x</i>) = <i>x</i>", '<p class="small">Right <i>n</i> is the same as down <i>n</i>. Not for other lines.</p>')],
         2: [("Horizontal dilation", '<div class="eq sm"><i>f</i>(<span class="cm"><i>b</i></span><i>x</i>)</div><p class="small">|<i>b</i>| &gt; 1 compresses. 0 &lt; |<i>b</i>| &lt; 1 stretches.</p>'),
             ("Matching dilations", '<p class="small">For <i>f</i>(<i>x</i>) = <i>x</i>: vertical by <i>n</i> = horizontal by 1/<i>n</i>.</p>'),
             ("Simplify first", '<div class="eq sm"><i>j</i>(<i>x</i> + 4) = 2(<i>x</i> + 4) − 1</div><p class="small">Distribute, then combine.</p>')]}),
 "2.3": dict(
  vocab=vocab(
   ("Perpendicular", "Lines that meet at a right angle (90°).", "⊥"),
   ("Reciprocal", "Flip the fraction. A number times its reciprocal is 1.", "{{2|3}} → {{3|2}}"),
   ("Negative reciprocal", "Flip the fraction and change the sign.", "{{2|3}} → −{{3|2}}"),
   ("Rotation", "Turning a figure about a point.", "90°: (<i>x</i>, <i>y</i>) → (−<i>y</i>, <i>x</i>)"),
   ("Horizontal line", "<i>y</i> = a number. Slope 0.", "<i>y</i> = −1"),
   ("Vertical line", "<i>x</i> = a number. Slope undefined.", "<i>x</i> = 2")),
  plans={1: ["Bell work (5 min)", "Getting Started: rotate a segment", "Activity 3.1: slopes of perpendicular lines"],
         2: ["Bell work (5 min)", "Activity 3.2: horizontal and vertical lines", "Activity 3.3: write perpendicular lines", "Talk the Talk", "Exit ticket"]},
  notes={1: [("90° rotation", '<div class="eq sm">(<i>x</i>, <i>y</i>) → (−<i>y</i>, <i>x</i>)</div>'),
             ("Perpendicular slopes", '<p class="small">Negative reciprocals. Their product is −1.</p><div class="eq sm">2 · (−{{1|2}}) = −1</div>'),
             ("Parallel slopes", '<p class="small">Equal.</p>')],
         2: [("Horizontal and vertical", '<p class="small"><b>Horizontal:</b> <i>y</i> = a number, slope 0.<br><b>Vertical:</b> <i>x</i> = a number, slope undefined.<br>They are always perpendicular.</p>'),
             ("Write a perpendicular line", '<p class="small">1. Find the given slope.<br>2. Take the negative reciprocal.<br>3. Use the point: <i>y</i> − <i>y</i><sub>1</sub> = <i>m</i>(<i>x</i> − <i>x</i><sub>1</sub>).</p>'),
             ("Check the scale", '<p class="small">Lines can look perpendicular on a stretched grid. Check the slopes.</p>')]}),
 "2.4": dict(
  vocab=vocab(
   ("Representation", "A way to show a function: table, graph, equation or words.", ""),
   ("Rate of change", "Change in <i>y</i> ÷ change in <i>x</i>: the slope.", "$15 per ton"),
   ("<i>y</i>-intercept", "The output when <i>x</i> = 0: the starting amount.", "$25 to start"),
   ("Independent quantity", "The input, on the <i>x</i>-axis.", "months"),
   ("Dependent quantity", "The output, on the <i>y</i>-axis.", "dollars saved"),
   ("Scale", "How much each grid line counts.", "each tick = $20")),
  plans={1: ["Bell work (5 min)", "Getting Started: odd one out", "Activity 4.1: compare slopes", "Activity 4.2: a table and a graph"],
         2: ["Bell work (5 min)", "Activity 4.3: an equation and a table", "Activity 4.4: words and a graph", "Talk the Talk", "Exit ticket"]},
  notes={1: [("Find the slope", '<p class="small"><b>Table or graph:</b> pick two points, {{change in <i>y</i>|change in <i>x</i>}}.<br><b>Equation:</b> the number with <i>x</i>.<br><b>Words:</b> the "per" amount.</p>'),
             ("Compare", '<p class="small">Same slope → parallel.<br>Product −1 → perpendicular.<br>Otherwise neither.</p>'),
             ("Greater slope", '<p class="small">Steeper line: it grows faster (pays more per ton).</p>')],
         2: [("Units", '<p class="small">Slope units = output units per input unit: degrees per degree, dollars per month.</p>'),
             ("<i>y</i>-intercept", '<p class="small">The starting value: $0 or $25 at month 0.</p>'),
             ("Scale", '<p class="small">Use a known point to find what each tick counts: $80 after 4 months → $20 per tick.</p>')]}),
})


def iep_t2_1():
    n = "2.1"
    s = [iep_title(n, "Transforming Linear Functions", f'<i>g</i>(<i>x</i>) = <span class="cm"><i>a</i></span> · {FX} + <span class="cp"><i>d</i></span>', [
        "move a line up or down and write its equation.",
        "stretch, compress or flip a line and find its new slope.",
        "write a line parallel to another line through a point."], 3)]
    s.append(sec("Topic 2 Lesson 1 · Vocabulary", "Words we need", vocab(
        ("Parent function", "The simplest line.", f"{FX} = <i>x</i>"),
        ("Translate", "Move up or down. Add <i>d</i>.", f"{FX} <span class=\"cp\">+ 4</span>"),
        ("Dilate", "Stretch or squeeze. Multiply by <i>a</i>.", f"<span class=\"cm\">2</span> · {FX}")),
        "Read each word aloud. Students copy them onto their vocabulary card."))
    s.append(sec("Topic 2 Lesson 1 · Steps", f"How to read <i>g</i>(<i>x</i>) = <i>a</i> · {FX} + <i>d</i>", steps(
        f"Start with {FX} = <i>x</i>: slope 1, through (0, 0).",
        "<b class=\"cm\"><i>a</i></b> is the new slope. A negative <i>a</i> flips the line.",
        "<b class=\"cp\"><i>d</i></b> moves the line up (+) or down (−). The <i>y</i>-intercept is (0, <i>d</i>).",
        "Plot (0, <i>d</i>), then count the slope <i>a</i>."), "Leave this slide up, or give students a printed copy, while they work."))
    s.append(sec("I do · Watch me", f"Move {FX} = <i>x</i> up 5", row(
        graph(380, 400, [-5, 5], [-5, 9], [1, 1], [1, 2], [dict(p=[[0, 0], [1, 1]], label="f(x)")] + move([[-4, -4], [-1, -1], [2, 2]], 5, label="+5 ↑")
              + [dict(p=[[0, 5], [1, 6]], label="p(x)", c="b", step=True)], [[-4, -4], [-1, -1], [2, 2]],
              "f(x) = x with points (−4, −4), (−1, −1), (2, 2), each moved up 5 to (−4, 1), (−1, 4), (2, 7) on p(x) = x + 5"),
        '<p>Up means <b>+</b>: add 5 to every output (<i>y</i>).</p><table class="tbl" style="font-size:24px"><tr><th>x</th><th>f(x)</th><th>+ 5</th><th>p(x)</th></tr>'
        + "".join(f'<tr><td>{x}</td><td>{x}</td><td>+ 5</td><td class="step">{x + 5}</td></tr>'.replace("-", "−") for x in (-4, -1, 2)) + '</table>'
        + ans(f'<i>p</i>(<i>x</i>) = {FX} + 5 = <i>x</i> + 5') + '<p class="small">Slope: still 1. <i>y</i>-intercept: (0, 0) → (0, 5).</p>'),
        "Click once for each blue arrow: point to a black point on f(x), count up 5 squares, and land on the blue point. "
        "Then the blue line p(x) appears through the moved points. Fill in the table the same way: + 5 to each output. The lines are parallel."))
    s.append(sec("We do · Together", f"Move <i>j</i>(<i>x</i>) = 2<i>x</i> − 1 down 4", row(
        '<p>Down means <b>−</b>: subtract 4 from every output.</p>'
        '<p><i>r</i>(<i>x</i>) = <i>j</i>(<i>x</i>) − ____</p>' + ans('<i>r</i>(<i>x</i>) = <i>j</i>(<i>x</i>) − 4')
        + '<p>Simplify: 2<i>x</i> − 1 − 4 = ____</p>' + ans('<i>r</i>(<i>x</i>) = 2<i>x</i> − 5 &nbsp;(−1 − 4 = −5)')
        + '<p>Slope ____ &nbsp; <i>y</i>-intercept ____</p>' + ans('slope 2, (0, −1) → (0, −5)'),
        graph(360, 420, [-3, 3], [-8, 4], [1, 1], [1, 2], [dict(p=[[0, -1], [1, 1]], label="j(x)")] + move([[-1, -3], [0, -1], [1, 1]], -4, label="−4 ↓")
              + [dict(p=[[0, -5], [1, -3]], label="r(x)", c="b", step=True)], [[-1, -3], [0, -1], [1, 1]],
              "j(x) = 2x − 1 with points (−1, −3), (0, −1), (1, 1), each moved down 4 to (−1, −7), (0, −5), (1, −3) on r(x) = 2x − 5")),
        "Students fill in the blanks on their paper first, then reveal. On the graph, each click moves one point down 4: "
        "count 4 squares down from the black point to the blue point. Then the blue line r(x) appears."))
    s.append(sec("I do · Stretch", f"Multiply {FX} = <i>x</i> by 4", row(
        '<p>Multiply every output by 4.</p>' + ans('<i>a</i>(<i>x</i>) = 4<i>x</i>') + '<p>The slope is now <b class="cm">4</b>: steeper.</p>'
        + '<p>With −4, the line also <b>flips</b>:</p>' + ans('<i>c</i>(<i>x</i>) = −4<i>x</i>'),
        graph(340, 340, [-4, 4], [-8, 8], [1, 1], [1, 2], [dict(p=[[0, 0], [1, 1]], label="f(x)"), dict(p=[[0, 0], [1, 4]], label="4x", step=True), dict(p=[[0, 0], [1, -4]], label="−4x", c="b", step=True)], [], "f(x) = x, 4x and −4x")),
        "All three lines pass through (0, 0): multiplying 0 gives 0."))
    s.append(sec("You do · Try it", "Describe the change and write <i>g</i>(<i>x</i>)", row(
        f'<div class="card"><p>1. <i>g</i>(<i>x</i>) = 2 · {FX} + 7</p>' + ans('stretch by 2, up 7: 2<i>x</i> + 7') + '</div>',
        f'<div class="card"><p>2. <i>g</i>(<i>x</i>) = {{{{1|2}}}} · {FX} − 3</p>' + ans('compress by {{1|2}}, down 3: {{1|2}}<i>x</i> − 3') + '</div>')))
    s.append(walk("Describe the change and write <i>g</i>(<i>x</i>)",
        ("1. <i>g</i>(<i>x</i>) = 2 · <i>f</i>(<i>x</i>) + 7", [
            "<i>f</i>(<i>x</i>) = <i>x</i>, so write <i>x</i> in its place: <i>g</i>(<i>x</i>) = 2<i>x</i> + 7.",
            "The number <b class=\"cm\">multiplied</b> is <i>a</i> = 2. It is the new slope. 2 is more than 1, so the line <b>stretches</b> (gets steeper).",
            "The number <b class=\"cp\">added</b> is <i>d</i> = +7. Plus means the line moves <b>up 7</b>. It crosses the <i>y</i>-axis at (0, 7)."],
         "stretch by 2, up 7: <i>g</i>(<i>x</i>) = 2<i>x</i> + 7"),
        ("2. <i>g</i>(<i>x</i>) = {{1|2}} · <i>f</i>(<i>x</i>) − 3", [
            "Write <i>x</i> in place of <i>f</i>(<i>x</i>): <i>g</i>(<i>x</i>) = {{1|2}}<i>x</i> − 3.",
            "<i>a</i> = {{1|2}} is between 0 and 1, so the line <b>compresses</b> (gets less steep). The slope is {{1|2}}.",
            "<i>d</i> = −3. Minus means the line moves <b>down 3</b>. It crosses the <i>y</i>-axis at (0, −3)."],
         "compress by {{1|2}}, down 3: {{1|2}}<i>x</i> − 3")))
    s.append(sec("We do · Parallel line", "Parallel to <i>y</i> = −3<i>x</i> − 1, through (−1, 5)",
                 '<p>Step 1: same slope. &nbsp;<i>m</i> = ____</p>' + ans('<i>m</i> = −3')
                 + '<p>Step 2: 5 = −3(−1) + <i>b</i>, so <i>b</i> = ____</p>' + ans('<i>b</i> = 2')
                 + '<p>Step 3: write it.</p>' + ans('<i>y</i> = −3<i>x</i> + 2'),
                 "Parallel lines have the same slope; only b changes."))
    s.append(sec("You do · Try it", "Parallel to <i>y</i> = 2<i>x</i>", row(
        '<div class="card"><p>1. Through (0, 4)</p>' + ans('<i>y</i> = 2<i>x</i> + 4') + '</div>',
        '<div class="card"><p>2. Through (2, 0)</p><p class="small">0 = 2(2) + <i>b</i></p>' + ans('<i>y</i> = 2<i>x</i> − 4') + '</div>')))
    s.append(walk("Parallel to <i>y</i> = 2<i>x</i>",
        ("1. Through (0, 4)", [
            "Parallel means the <b>same slope</b>: <i>m</i> = 2.",
            "Put <i>x</i> = 0 and <i>y</i> = 4 into <i>y</i> = <i>mx</i> + <i>b</i>: 4 = 2(0) + <i>b</i>.",
            "2(0) = 0, so 4 = <i>b</i>.",
            "Write the slope and <i>b</i>: <i>y</i> = 2<i>x</i> + 4."],
         "<i>y</i> = 2<i>x</i> + 4"),
        ("2. Through (2, 0)", [
            "Same slope: <i>m</i> = 2.",
            "Put <i>x</i> = 2 and <i>y</i> = 0 into <i>y</i> = <i>mx</i> + <i>b</i>: 0 = 2(2) + <i>b</i>.",
            "Multiply: 0 = 4 + <i>b</i>.",
            "Subtract 4 from both sides: −4 = <i>b</i>."],
         "<i>y</i> = 2<i>x</i> − 4")))
    s += exit_and_practice(n, [(f"1. <i>g</i>(<i>x</i>) = {FX} + 6. Up or down? How far?", "up 6"),
                               (f"2. What is the slope of <i>g</i>(<i>x</i>) = 5 · {FX}?", "5"),
                               ("3. Write the line parallel to <i>y</i> = 4<i>x</i> + 1 through (0, −2).", "<i>y</i> = 4<i>x</i> − 2")])
    return s


def iep_t2_2():
    n = "2.2"
    s = [iep_title(n, "Horizontal and Vertical Transformations", '<i>f</i>(<i>x</i> − <span class="cp"><i>c</i></span>) · <i>f</i>(<span class="cm"><i>b</i></span><i>x</i>)', [
        "tell whether a change moves the graph left/right or up/down.",
        "write <i>f</i>(<i>x</i> − <i>c</i>) for a move right or left.",
        "simplify a transformed function like <i>j</i>(<i>x</i> + 4)."], 2)]
    s.append(sec("Topic 2 Lesson 2 · Vocabulary", "Words we need", vocab(
        ("Inside", "Changes the input: left or right.", "<i>f</i>(<i>x</i> <span class=\"cp\">− 3</span>)"),
        ("Outside", "Changes the output: up or down.", f"{FX} <span class=\"cp\">− 3</span>"),
        ("Sign flip", "Inside, minus moves <b>right</b> and plus moves <b>left</b>.", "<i>f</i>(<i>x</i> + 5): left 5"))))
    s.append(sec("Topic 2 Lesson 2 · Steps", "Which way does it move?", steps(
        "Look for the number. Is it <b>inside</b> the parentheses with <i>x</i>, or <b>outside</b>?",
        "Outside: + is up, − is down.",
        "Inside: − is right, + is left (the sign flips).",
        "To simplify, put the inside into the rule and distribute."), "Leave this slide up, or give students a printed copy, while they work."))
    s.append(sec("I do · Watch me", f"<i>f</i>(<i>x</i> − 7) and {FX} − 4", row(
        card("<i>f</i>(<i>x</i> − 7)", '<p class="small">Inside, minus → <b>right 7</b>: each point moves 7 to the right.</p>'
             + graph(330, 250, [-2, 10], [-3, 4], [1, 2], [1, 1], [dict(p=[[0, 0], [1, 1]], label="f(x)")] + move([[0, 0], [2, 2]], dx=7, label="+7 →")
                     + [dict(p=[[7, 0], [8, 1]], label="g(x)", c="b", step=True)], [[0, 0], [2, 2]], "f(x) = x with (0, 0) and (2, 2) moved right 7")
             + ans('<i>g</i>(<i>x</i>) = <i>x</i> − 7')),
        card(f"{FX} − 4", '<p class="small">Outside, minus → <b>down 4</b>: each point moves 4 down.</p>'
             + graph(330, 250, [-4, 4], [-7, 4], [1, 2], [1, 2], [dict(p=[[0, 0], [1, 1]], label="f(x)")] + move([[-2, -2], [0, 0], [2, 2]], -4, label="−4 ↓")
                     + [dict(p=[[0, -4], [1, -3]], label="g(x)", c="b", step=True)], [[-2, -2], [0, 0], [2, 2]], "f(x) = x with three points moved down 4")
             + ans('<i>g</i>(<i>x</i>) = <i>x</i> − 4'))),
        "Think aloud about inside versus outside before naming the direction. Each click moves one point: right 7 on the left graph, down 4 on the right. "
        "For f(x) = x both give a line parallel to f(x)."))
    s.append(sec("You do · Try it", "Which way, and how far?", row(
        '<div class="card"><p>1. <i>f</i>(<i>x</i> + 5)</p>' + ans('left 5') + '</div>',
        f'<div class="card"><p>2. {FX} + 2</p>' + ans('up 2') + '</div>',
        '<div class="card"><p>3. <i>f</i>(<i>x</i> − 3)</p>' + ans('right 3') + '</div>')))
    s.append(walk("Which way, and how far?",
        ("1. <i>f</i>(<i>x</i> + 5)", ["The 5 is <b>inside</b> the parentheses with <i>x</i>, so the graph moves left or right.",
                                         "Inside, the sign flips: <b>plus</b> means <b>left</b>."], "left 5"),
        ("2. <i>f</i>(<i>x</i>) + 2", ["The 2 is <b>outside</b> the parentheses, so the graph moves up or down.",
                                        "Outside, no flip: <b>plus</b> means <b>up</b>."], "up 2"),
        ("3. <i>f</i>(<i>x</i> − 3)", ["The 3 is <b>inside</b>, so left or right.",
                                         "Inside, the sign flips: <b>minus</b> means <b>right</b>."], "right 3")))
    s.append(sec("We do · Simplify", "<i>j</i>(<i>x</i>) = 2<i>x</i> − 1. Simplify <i>j</i>(<i>x</i> + 4).",
                 '<p>Put (<i>x</i> + 4) in for <i>x</i>: 2(____) − 1</p>' + ans('2(<i>x</i> + 4) − 1')
                 + '<p>Distribute: ____ − 1</p>' + ans('2<i>x</i> + 8 − 1') + '<p>Combine:</p>' + ans('2<i>x</i> + 7'),
                 "Compare with j(x) + 4 = 2x + 3: left 4 and up 4 are not the same for this line."))
    s.append(sec("You do · Try it", "<i>j</i>(<i>x</i>) = 2<i>x</i> − 1", row(
        '<div class="card"><p>1. Simplify <i>j</i>(<i>x</i> − 2).</p>' + ans('2<i>x</i> − 5') + '</div>',
        '<div class="card"><p>2. Simplify <i>j</i>(<i>x</i>) − 2.</p>' + ans('2<i>x</i> − 3') + '<p class="small">Same graph as #1? ____</p>' + ans('No') + '</div>')))
    s.append(walk("<i>j</i>(<i>x</i>) = 2<i>x</i> − 1",
        ("1. Simplify <i>j</i>(<i>x</i> − 2)", [
            "The change is inside, so put (<i>x</i> − 2) where <i>x</i> was: 2(<i>x</i> − 2) − 1.",
            "Distribute the 2: 2 · <i>x</i> = 2<i>x</i> and 2 · (−2) = −4. Now it is 2<i>x</i> − 4 − 1.",
            "Combine the numbers: −4 − 1 = −5."],
         "2<i>x</i> − 5"),
        ("2. Simplify <i>j</i>(<i>x</i>) − 2", [
            "The change is outside, so write the whole rule, then subtract 2: 2<i>x</i> − 1 − 2.",
            "Combine the numbers: −1 − 2 = −3. That gives 2<i>x</i> − 3.",
            "Compare with #1: 2<i>x</i> − 5 and 2<i>x</i> − 3 cross the <i>y</i>-axis at different places."],
         "2<i>x</i> − 3 · not the same graph as #1")))
    s.append(sec("I do · Stretch inside", f"For {FX} = <i>x</i>: <i>f</i>(2<i>x</i>) and 2{FX}", row(
        '<p><i>f</i>(2<i>x</i>) = 2<i>x</i></p><p>2 · <i>f</i>(<i>x</i>) = 2<i>x</i></p>' + ans('The same line: <i>y</i> = 2<i>x</i>') + '<p class="small">This only works for <i>f</i>(<i>x</i>) = <i>x</i>.</p>',
        graph(320, 320, [-4, 4], [-5, 5], [1, 1], [1, 1], [dict(p=[[0, 0], [1, 1]], label="f(x)"), dict(p=[[0, 0], [1, 2]], label="y = 2x", step=True)], [], "f(x) = x and y = 2x"))))
    s += exit_and_practice(n, [("1. <i>g</i>(<i>x</i>) = <i>f</i>(<i>x</i> − 6). Which way, and how far?", "right 6"),
                               ("2. <i>g</i>(<i>x</i>) = <i>f</i>(<i>x</i>) + 1. Which way, and how far?", "up 1"),
                               ("3. <i>j</i>(<i>x</i>) = 3<i>x</i>. Simplify <i>j</i>(<i>x</i> + 1).", "3<i>x</i> + 3")])
    return s


def iep_t2_3():
    n = "2.3"
    s = [iep_title(n, "Slopes of Perpendicular Lines", '<span class="cm"><i>m</i><sub>1</sub></span> · <span class="cm"><i>m</i><sub>2</sub></span> = −1', [
        "find the slope of a perpendicular line.",
        "write equations of horizontal and vertical lines.",
        "write the equation of a perpendicular line through a point."], 2)]
    s.append(sec("Topic 2 Lesson 3 · Vocabulary", "Words we need", vocab(
        ("Perpendicular", "Lines that make a square corner (90°).", "⊥"),
        ("Negative reciprocal", "Flip the fraction and change the sign.", "{{2|3}} → −{{3|2}}"),
        ("Horizontal / vertical", "<i>y</i> = number (slope 0) / <i>x</i> = number (undefined).", "<i>y</i> = 4, <i>x</i> = 2"))))
    s.append(sec("Topic 2 Lesson 3 · Steps", "How to write a perpendicular line", steps(
        "Find the slope of the given line.",
        "Flip it and change the sign. That is the new slope.",
        "Use the point: <i>y</i> − <i>y</i><sub>1</sub> = <i>m</i>(<i>x</i> − <i>x</i><sub>1</sub>).",
        "Get <i>y</i> alone."), "Leave this slide up, or give students a printed copy, while they work."))
    s.append(sec("I do · Watch me", "Perpendicular slopes", row(
        card("{{2|3}}", '<p class="small">Flip: {{3|2}}. Change sign:</p>' + ans('−{{3|2}}')),
        card("−3", '<p class="small">−3 = −{{3|1}}. Flip: {{1|3}}. Change sign:</p>' + ans('{{1|3}}'))),
        "Check each: the product should be −1."))
    s.append(sec("You do · Try it", "Find the perpendicular slope", row(
        '<div class="card"><p>1. 4</p>' + ans('−{{1|4}}') + '</div>',
        '<div class="card"><p>2. −{{4|5}}</p>' + ans('{{5|4}}') + '</div>',
        '<div class="card"><p>3. {{1|2}}</p>' + ans('−2') + '</div>')))
    s.append(walk("Find the perpendicular slope",
        ("1. 4", ["Write it as a fraction: {{4|1}}.", "Flip it: {{1|4}}.", "Change the sign: −{{1|4}}.",
                  "Check: 4 · (−{{1|4}}) = −1 ✓"], "−{{1|4}}"),
        ("2. −{{4|5}}", ["Flip it: −{{5|4}}.", "Change the sign: − becomes +, so {{5|4}}.",
                         "Check: −{{4|5}} · {{5|4}} = −1 ✓"], "{{5|4}}"),
        ("3. {{1|2}}", ["Flip it: {{2|1}} = 2.", "Change the sign: −2.", "Check: {{1|2}} · (−2) = −1 ✓"], "−2")))
    s.append(sec("We do · Flat and straight-up lines", "Through (2, −1)", row(
        '<p>Horizontal: <i>y</i> = ____</p>' + ans('<i>y</i> = −1') + '<p>Vertical: <i>x</i> = ____</p>' + ans('<i>x</i> = 2')
        + '<p class="small">A horizontal line and a vertical line are always perpendicular.</p>',
        graph(300, 300, [-4, 5], [-5, 4], [1, 1], [1, 1], [dict(p=[[-4, -1], [5, -1]], label="y = −1", step=True), dict(p=[[2, -5], [2, 4]], label="x = 2", c="b", step=True)], [[2, -1, "(2, −1)"]], "Horizontal and vertical lines through (2, −1)"))))
    s.append(sec("I do · Write it", "⊥ to <i>y</i> = 2<i>x</i> + 1, through (6, 2)",
                 '<p>Step 1: given slope 2. Step 2: new slope:</p>' + ans('−{{1|2}}')
                 + '<p>Step 3: <i>y</i> − 2 = −{{1|2}}(<i>x</i> − 6)</p><p>Step 4: <i>y</i> − 2 = −{{1|2}}<i>x</i> + 3</p>' + ans('<i>y</i> = −{{1|2}}<i>x</i> + 5'),
                 "Model each step; point to the steps slide."))
    s.append(sec("You do · Try it", "⊥ to <i>y</i> = 3<i>x</i>, through (3, 1)",
                 '<p>New slope: ____</p>' + ans('−{{1|3}}') + '<p><i>y</i> − 1 = ____(<i>x</i> − 3)</p>' + ans('<i>y</i> − 1 = −{{1|3}}(<i>x</i> − 3)')
                 + '<p><i>y</i> = ____</p>' + ans('<i>y</i> = −{{1|3}}<i>x</i> + 2')))
    s.append(walk("⊥ to <i>y</i> = 3<i>x</i>, through (3, 1)",
        ("Write the perpendicular line", [
            "The given slope is the number with <i>x</i>: 3.",
            "3 = {{3|1}}. Flip it to {{1|3}}, then change the sign: the new slope is −{{1|3}}.",
            "Put <i>m</i> = −{{1|3}}, <i>x</i><sub>1</sub> = 3, <i>y</i><sub>1</sub> = 1 into <i>y</i> − <i>y</i><sub>1</sub> = <i>m</i>(<i>x</i> − <i>x</i><sub>1</sub>): "
            "<i>y</i> − 1 = −{{1|3}}(<i>x</i> − 3).",
            "Distribute: −{{1|3}} · <i>x</i> = −{{1|3}}<i>x</i> and −{{1|3}} · (−3) = +1. Now <i>y</i> − 1 = −{{1|3}}<i>x</i> + 1.",
            "Add 1 to both sides to get <i>y</i> alone: 1 + 1 = 2."],
         "<i>y</i> = −{{1|3}}<i>x</i> + 2")))
    s += exit_and_practice(n, [("1. What slope is perpendicular to {{3|4}}?", "−{{4|3}}"),
                               ("2. Write the vertical line through (5, 6).", "<i>x</i> = 5"),
                               ("3. Write the line ⊥ to <i>y</i> = −<i>x</i> through (0, 3).", "<i>y</i> = <i>x</i> + 3")])
    return s


def iep_t2_4():
    n = "2.4"
    tb = lambda xs, ys, hx="x", hy="y": (f'<table class="tbl" style="font-size:24px"><tr><th style="font-style:normal">{hx}</th><th style="font-style:normal">{hy}</th></tr>'
                                         + "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in zip(xs, ys)) + "</table>")
    s = [iep_title(n, "Comparing Linear Functions", "table · graph · equation · words", [
        "find the slope in a table, graph, equation or story.",
        "tell whether two lines are parallel, perpendicular or neither.",
        "explain what the slope and the <i>y</i>-intercept mean."], 2)]
    s.append(sec("Topic 2 Lesson 4 · Vocabulary", "Words we need", vocab(
        ("Slope", "The rate: how much <i>y</i> changes for each 1 of <i>x</i>.", "$15 per ton"),
        ("<i>y</i>-intercept", "The starting amount, when <i>x</i> = 0.", "$25 to start"),
        ("Units", "What the numbers count.", "dollars, months"))))
    s.append(sec("Topic 2 Lesson 4 · Steps", "How to find the slope", steps(
        "<b>Equation</b> <i>y</i> = <i>mx</i> + <i>b</i>: the slope is <i>m</i>.",
        "<b>Table or graph:</b> pick two points. {{change in <i>y</i>|change in <i>x</i>}}.",
        "<b>Story:</b> look for \"each\" or \"per\".",
        "Compare: same slope → parallel. Product −1 → perpendicular."), "Leave this slide up, or give students a printed copy, while they work."))
    s.append(sec("I do · Watch me", "Compare to <i>y</i> = 4<i>x</i> − 3", row(
        tb([0, 0.5, 3], [4, 6, 16]),
        '<p>From (0, 4) to (0.5, 6): {{2|0.5}} = 4.</p>' + ans('slope 4: parallel') + '<p>Same slope as 4<i>x</i> − 3, different start.</p>'),
        "Model the slope from two rows of the table."))
    s.append(sec("You do · Try it", "Compare to <i>y</i> = 4<i>x</i> − 3", row(
        '<div class="card"><p>1. Chiletso makes 4 dozen cookies per hour.</p>' + ans('slope 4: parallel') + '</div>',
        '<div class="card"><p>2. <i>y</i> = −{{1|4}}<i>x</i> + 2</p>' + ans('perpendicular') + '</div>')))
    s.append(walk("Compare to <i>y</i> = 4<i>x</i> − 3",
        ("1. Chiletso makes 4 dozen cookies per hour.", [
            "Look for \"per\": 4 dozen <b>per</b> hour. The slope is 4.",
            "The slope of <i>y</i> = 4<i>x</i> − 3 is the number with <i>x</i>: 4.",
            "4 and 4 are the same slope, so the lines are parallel."], "slope 4: parallel"),
        ("2. <i>y</i> = −{{1|4}}<i>x</i> + 2", [
            "The slope is the number with <i>x</i>: −{{1|4}}.",
            "Is it the same as 4? No, so not parallel.",
            "Multiply the slopes: 4 · (−{{1|4}}) = −1. A product of −1 means perpendicular."], "perpendicular")))
    s.append(sec("We do · Table and graph", "Which recycling center pays more?", row(
        '<p>Travis County</p>' + tb([1, 2], [15, 30], "tons", "$") + '<p>Rate: ____ per ton</p>' + ans('$15'),
        '<p>Hays County graph: through (1, 20)</p><p>Rate: ____ per ton</p>' + ans('$20') + '<p>Which pays more?</p>' + ans('Hays County'))))
    s.append(sec("I do · Meaning in a story", "Lauren starts with $25 and saves $25 each month",
                 '<div class="eq"><i>y</i> = <span class="cm">25</span><i>x</i> + <span class="cp">25</span></div>'
                 + '<p><b class="cm">25</b> (slope): she saves $25 each month.</p><p><b class="cp">25</b> (<i>y</i>-intercept): she started with $25.</p>'
                 + '<p>Miguel saves $20 a month from $0. Who saves faster?</p>' + ans('Lauren ($25 &gt; $20)'),
                 "Units: dollars per month."))
    s.append(sec("You do · Try it", "A taxi charges $3 plus $2 per mile",
                 '<p>1. Slope (with units): ____</p>' + ans('$2 per mile') + '<p>2. <i>y</i>-intercept meaning: ____</p>' + ans('$3 before driving')))
    s.append(walk("A taxi charges $3 plus $2 per mile",
        ("1. Slope (with units)", [
            "Look for \"per\": $2 <b>per</b> mile.",
            "The slope is how much the cost goes up for each 1 mile: $2.",
            "Units: output (dollars) per input (miles)."], "$2 per mile"),
        ("2. What the <i>y</i>-intercept means", [
            "The <i>y</i>-intercept is the cost when <i>x</i> = 0 miles.",
            "At 0 miles you still pay the $3.",
            "So the equation is <i>y</i> = 2<i>x</i> + 3, and 3 is the start."], "$3 before driving")))
    s += exit_and_practice(n, [("1. A table has (0, 1) and (2, 9). What is its slope?", "4"),
                               ("2. Is <i>y</i> = 4<i>x</i> + 7 parallel or perpendicular to <i>y</i> = 4<i>x</i> − 3?", "parallel"),
                               ("3. Savings: <i>y</i> = 10<i>x</i> + 50. What does 50 mean?", "$50 to start")])
    return s


IEP.update({"2.1": iep_t2_1, "2.2": iep_t2_2, "2.3": iep_t2_3, "2.4": iep_t2_4})


# ---------------------------------------------------------------- bell work and homework pages
# Same questions as lessonN/; mc.js applies `accom`. IEP: 3 choices, 6 of the 10 homework and quiz items.
REF = {
 4: ["<b>Point-slope form:</b> <i>y</i> − <i>y</i><sub>1</sub> = <i>m</i>(<i>x</i> − <i>x</i><sub>1</sub>). The signs flip: <i>x</i> − (−2) = <i>x</i> + 2.",
     "<b>Slope:</b> <i>m</i> = (change in <i>y</i>) ÷ (change in <i>x</i>).",
     "<b>To get <i>y</i> = <i>mx</i> + <i>b</i>:</b> distribute, then add or subtract to get <i>y</i> alone.",
     "<b>Horizontal:</b> <i>y</i> = a number, slope 0. <b>Vertical:</b> <i>x</i> = a number, slope undefined."],
 5: ["<b>Graph <i>y</i> = <i>mx</i> + <i>b</i>:</b> plot (0, <i>b</i>), then count rise over run.",
     "<b>Point-slope form:</b> start at (<i>x</i><sub>1</sub>, <i>y</i><sub>1</sub>). The signs flip.",
     "<b>Intercepts of <i>Ax</i> + <i>By</i> = <i>C</i>:</b> put <i>y</i> = 0 to find the <i>x</i>-intercept; put <i>x</i> = 0 to find the <i>y</i>-intercept.",
     "<b>Slope of <i>Ax</i> + <i>By</i> = <i>C</i>:</b> −<i>A</i> ÷ <i>B</i>."],
 6: ["<b>Is it linear?</b> Find (change in <i>y</i>) ÷ (change in <i>x</i>) for every pair. Always the same → linear.",
     "<b>General form:</b> <i>f</i>(<i>x</i>) = <i>ax</i> + <i>b</i>. <b>Factored form:</b> <i>f</i>(<i>x</i>) = <i>a</i>(<i>x</i> − <i>c</i>). Distribute to switch.",
     "<b>How much?</b> Put the number in for <i>x</i>. <b>How many?</b> Set <i>f</i>(<i>x</i>) equal to the amount and solve.",
     "<b>Round up</b> when you need at least that much (you can't sell part of a shirt)."],
 "2.1": ["<b>Translate:</b> <i>f</i>(<i>x</i>) + <i>d</i> moves the graph up (<i>d</i> &gt; 0) or down (<i>d</i> &lt; 0). The slope stays the same.",
         "<b>Dilate:</b> <i>a</i> · <i>f</i>(<i>x</i>) stretches when |<i>a</i>| &gt; 1, compresses when 0 &lt; |<i>a</i>| &lt; 1, and reflects across the <i>x</i>-axis when <i>a</i> &lt; 0.",
         "<b>For <i>f</i>(<i>x</i>) = <i>x</i>:</b> <i>a</i> · <i>f</i>(<i>x</i>) + <i>d</i> = <i>ax</i> + <i>d</i>, with slope <i>a</i> and <i>y</i>-intercept (0, <i>d</i>).",
         "<b>Parallel lines</b> have the same slope. Put the point into <i>y</i> = <i>mx</i> + <i>b</i> to find <i>b</i>."],
 "2.2": ["<b>Inside the parentheses</b> changes the input (horizontal). <b>Outside</b> changes the output (vertical).",
         "<b><i>f</i>(<i>x</i> − <i>c</i>)</b> moves right <i>c</i>. <b><i>f</i>(<i>x</i> + <i>c</i>)</b> moves left <i>c</i>. The sign flips.",
         "<b><i>f</i>(<i>bx</i>)</b> compresses horizontally when |<i>b</i>| &gt; 1 and stretches when 0 &lt; |<i>b</i>| &lt; 1.",
         "<b>Only for <i>f</i>(<i>x</i>) = <i>x</i>:</b> right <i>n</i> = down <i>n</i>, and a vertical dilation by <i>n</i> = a horizontal dilation by 1/<i>n</i>."],
 "2.3": ["<b>Perpendicular slopes</b> are negative reciprocals: flip the fraction and change the sign. Their product is −1.",
         "<b>Parallel slopes</b> are equal.",
         "<b>Horizontal:</b> <i>y</i> = a number, slope 0. <b>Vertical:</b> <i>x</i> = a number, slope undefined. They are always perpendicular.",
         "<b>Point-slope form:</b> <i>y</i> − <i>y</i><sub>1</sub> = <i>m</i>(<i>x</i> − <i>x</i><sub>1</sub>), then get <i>y</i> alone."],
 "2.4": ["<b>Slope from a table or two points:</b> (change in <i>y</i>) ÷ (change in <i>x</i>).",
         "<b>Same slope</b> → parallel. <b>Slopes multiply to −1</b> → perpendicular. Otherwise neither.",
         "<b><i>y</i>-intercept:</b> the output when <i>x</i> = 0, the starting amount.",
         "<b>Units:</b> the slope is output units per input unit, for example dollars per ton."]}
KEEP = {"homework": {4: [0, 2, 5, 6, 7, 8], 5: [0, 1, 2, 3, 4, 5], 6: [0, 1, 5, 7, 8, 9],
                     "2.1": [0, 1, 3, 6, 7, 8, 10, 13], "2.2": [0, 2, 3, 6, 8, 9, 11, 12], "2.3": [0, 1, 2, 4, 5, 9, 11, 12],
                     "2.4": [0, 1, 3, 5, 6, 8, 10, 13]},  # Topic 2: the last two are test-style items (questions 11-14 on the general page)
        "quiz": {4: [0, 1, 3, 6, 7, 8], 5: [0, 1, 4, 5, 6, 9], 6: [0, 1, 4, 5, 6, 8],
                 "2.1": [0, 2, 3, 4, 6, 8, 10, 13], "2.2": [0, 1, 2, 5, 7, 9, 11, 12], "2.3": [0, 2, 6, 7, 8, 9, 10, 12],
                 "2.4": [1, 2, 3, 5, 6, 8, 10, 13]}}


def src(n):  # folder, file prefix and name of lesson n's general pages ("2.1" = Topic 2 Lesson 1)
    if isinstance(n, str):
        return HERE / "Module 2 topic 2", f"t2-lesson{n[2:]}", f"Topic 2 Lesson {n[2:]}"
    return HERE / f"lesson{n}", f"lesson{n}", f"Lesson {n}"
HELP = {"IEP": "Each question has 3 choices. Use the reminders below, and press <b>Read aloud</b> to hear a question.",
        "504": "Use the reminders below, and press <b>Read aloud</b> to hear a question. Take the time you need."}


def practice_pages(n, kind, folder):
    label = "Section 504" if kind == "504" else "IEP"
    card = (f'<div class="card ref"><p>{HELP[kind]}</p>' + "".join(f"<p>{r}</p>" for r in REF[n]) + "</div>")
    d, pre, _ = src(n)
    pages = sorted(d.glob(f"{pre}-bellwork-day*.html")) + [d / f"{pre}-{p}.html" for p in ("homework", "quiz")]
    for f in pages:
        accom = {"readAloud": True}
        s = f.read_text(encoding="utf-8")
        if kind == "IEP":
            accom["choices"] = 3
            page = f.stem.split("-")[-1]
            if page in KEEP:
                accom["keep"] = KEEP[page][n]
                s = re.sub(r"Answer all \d+ questions", f"Answer all {len(accom['keep'])} questions", s)
                s = s.replace("Questions 11–14 are written", "The last two questions are written")
            elif (n, int(page[-1])) in BELL:  # bell work: a formula under each question, worked steps after it
                accom["add"] = [{"extra": f'<p class="formula" style="margin:8px 0 2px;padding:6px 12px;border-left:4px solid #2f6fdd;'
                                          f'background:rgba(47,111,221,.08);border-radius:4px"><b>Formula:</b> {mt(q["formula"])}</p>',
                                 "why": "Here is how:" + "".join(f"<br><b>{j}.</b> {t}" for j, t in enumerate(q["steps"], 1))}
                                for q in bell_steps(n, int(page[-1]), page_data(f))]
        s = s.replace("</title>", f" · {label}</title>", 1).replace('<div class="wrap">', '<div class="wrap big">', 1)
        s = re.sub(r'(<p class="eyebrow">.*?)</p>', lambda m: f"{m.group(1)} · {label} Version</p>", s, count=1)
        s = re.sub(r'(<p class="muted">.*?</p>)', lambda m: m.group(1) + "\n  " + card, s, count=1)
        s = s.replace('</script>\n<script src="../mc.js">', f'window.MC.accom = {json.dumps(accom)};\n</script>\n<script src="../mc.js">')
        assert "window.MC.accom" in s, f
        (HERE / folder / f"{f.stem}-{kind}.html").write_text(s, encoding="utf-8")


def page_data(path):  # the page data is a JS literal (unquoted keys in Lesson 4), so let node read it
    js = re.search(r"window\.MC = (\{.*?\});\n</script>", path.read_text(encoding="utf-8"), re.S).group(1)
    return json.loads(subprocess.run(
        ["node", "-e", "let s='';process.stdin.on('data',d=>s+=d).on('end',()=>console.log(JSON.stringify(eval('('+s+')'))))"],
        input=js, capture_output=True, text=True, encoding="utf-8", check=True).stdout)["questions"]


def answer_key(n, kind, folder, name):
    """Teacher answer-key .pptx for the IEP / 504 bell work (all days), homework or quiz.
    Choices are shuffled on screen, so it gives answer text, not letters."""
    title = {"bellwork": "Bell Work", "homework": "Homework", "quiz": "Quiz"}[name]
    d, pre, lesson = src(n)
    if name == "bellwork":  # one key for every day, a heading per day
        groups = [(f"Day {f.stem[-1]} · ", page_data(f)) for f in sorted(d.glob(f"{pre}-bellwork-day*.html"))]
        if kind == "IEP" and (n, 1) in BELL:  # the IEP key gives the same worked steps as the deck and page
            groups = [(day, [{**q, "why": " ".join(f"{j}. {re.sub(r'<.*?>', '', t)}" for j, t in enumerate(q["steps"], 1))}
                             for q in bell_steps(n, int(day[4]), data)]) for day, data in groups]
    else:
        groups = [("", page_data(d / f"{pre}-{name}.html"))]
    plain = lambda t: html_mod.escape(re.sub(r"\[\[(.+?)\]\]", r"\1", t))
    label = "Section 504" if kind == "504" else "IEP"
    foot = f'<p class="foot">{lesson} {title} · {label} Version · Answer Key (teacher copy)</p>'
    per = {"bellwork": 2, "homework": 2, "quiz": 3}[name]  # rows per slide that fit the 7.5 in height
    body, total = [], 0
    for day, data in groups:
        keep = KEEP[name][n] if kind == "IEP" and name in KEEP else range(len(data))
        rows = [f'<tr><td><b>{k}</b>' + (f' (was {i + 1})' if kind == "IEP" and name in KEEP else "")
                + (f' · SE p. {data[i]["se"]}' if data[i].get("se") else "") + '</td>'
                f'<td>{plain(data[i]["q"])}{" (uses the table on the page)" if data[i].get("extra") else ""}</td>'
                f'<td><b>{plain(data[i]["choices"][0])}</b><br>{plain(data[i]["why"])}</td></tr>' for k, i in enumerate(keep, 1)]
        total += len(rows)
        for k in range(0, len(rows), per):
            head = f"Questions {k + 1}–{min(k + per, len(rows))}" if k + 1 < len(rows) else f"Question {k + 1}"
            body.append(f'<section class="slide"><h2>{day}{head}</h2><table style="font-size:19px">'
                        f'<tr><th>#</th><th>Question</th><th>Answer and why</th></tr>{"".join(rows[k:k + per])}</table>{foot}</section>')
    if kind == "IEP":
        note = (f'Each IEP question has 3 choices; "was" gives the question number on the general {title.lower()}.' if name in KEEP
                else "Each IEP question has 3 choices; the questions are the same as the general bell work.")
    else:
        note = f"Same {total} questions and choices as the general {title.lower()}."
    slides = [f'<section class="slide"><h1>Answer Key</h1><h3>{lesson} {title} · {label} Version</h3>'
              f'<p>{total} questions{f" over {len(groups)} days" if len(groups) > 1 else ""}, 1 point each. '
              f'The answer choices are shuffled for each student, so match the answer text, not the letter.</p>'
              f'<p>{note}</p><p class="warn">Teacher copy. Do not share with students.</p>{foot}</section>'] + body
    out = HERE / folder / f"{pre}-{name}-{kind}-ANSWER-KEY.html"
    out.write_text(f'<!doctype html><meta charset="utf-8"><title>{lesson} {title} Answer Key · {label}</title><body>{"".join(slides)}</body>', encoding="utf-8")
    subprocess.run([sys.executable, str(HERE / "make_pptx.py"), out.relative_to(HERE).as_posix()], check=False)
    out.unlink()


EXIT_WORK = {  # IEP exit tickets (the 504 decks keep the original exit ticket, whose notes hold the work)
 4: ["Put m = 4, x₁ = 1, y₁ = 6 into y − y₁ = m(x − x₁).", "Distribute: y − 6 = 4x − 4. Add 6: y = 4x + 2.",
     "Both points have x = 4, so the line is vertical: x = 4, slope undefined."],
 5: ["b = 2, so start at (0, 2). Slope −3/4: down 3, right 4.", "y = 0: x = 8. x = 0: 2y = 8, so y = 4.",
     "The signs flip: x + 3 gives x₁ = −3 and y − 1 gives y₁ = 1. The slope is 2."],
 6: ["(10 − 4) ÷ (3 − 1) = 3 and (22 − 10) ÷ (7 − 3) = 3, so linear. 4 = 3(1) + b gives b = 1.",
     "x − 5 = 0 when x = 5.", "10 is the rate: $10 for each bracelet. −30 is the booth cost."],
 # Topic 2: numbered steps, shown on the exit ticket slide too
 "2.1": [["The + 6 is outside f(x), so the graph moves up or down.", "Plus means up: up 6."],
         ["Replace f(x) with x: g(x) = 5x.", "The number with x is 5, so the slope is 5."],
         ["Parallel means the same slope: m = 4.", "Put x = 0, y = −2 into y = mx + b: −2 = 4(0) + b, so b = −2.", "Write it: y = 4x − 2."]],
 "2.2": [["The 6 is inside the parentheses, so the graph moves left or right.", "Inside, the sign flips: minus means right. Right 6."],
         ["The 1 is outside, so the graph moves up or down.", "Outside, no flip: plus means up. Up 1."],
         ["Put (x + 1) in for x: j(x + 1) = 3(x + 1).", "Distribute: 3 · x + 3 · 1 = 3x + 3."]],
 "2.3": [["Flip 3/4: 4/3.", "Change the sign: −4/3.", "Check: 3/4 · (−4/3) = −1."],
         ["On a vertical line, x never changes.", "The point has x = 5, so the line is x = 5."],
         ["The slope of y = −x is −1.", "Flip and change the sign: −1 becomes 1.", "(0, 3) is on the y-axis, so b = 3: y = x + 3."]],
 "2.4": [["Change in y: 9 − 1 = 8.", "Change in x: 2 − 0 = 2.", "Divide: 8 ÷ 2 = 4."],
         ["The slope is the number with x: both are 4.", "Same slope means parallel."],
         ["In y = mx + b, 50 is b: the value when x = 0.", "x = 0 months is the start, so 50 is the $50 saved at the start."]]}


def exit_key(n, kind, folder, sec):
    """Teacher answer-key .pptx for the exit ticket slide of the IEP / 504 deck."""
    qs = re.findall(r"<p>(.*?)</p>", sec, re.S)
    ans = re.findall(r'class="step pop eq sm ans">(.*?)</div>', sec, re.S)
    assert len(qs) == len(ans) == 3, (n, kind)
    notes = re.search(r'<aside class="notes">(.*?)</aside>', sec, re.S)
    work = (" ".join(f"{k}. {w if isinstance(w, str) else ' '.join(w)}" for k, w in enumerate(EXIT_WORK[n], 1)) if kind == "IEP"
            else re.sub(r"^.*?Work: |^Added for this deck; not from the textbook\. |Give 3–4 minutes.*?Sets A–[A-Z]\. ", "",
                        notes.group(1)) if notes else "")  # keep only the math, not the classroom directions
    label = "Section 504" if kind == "504" else "IEP"
    _, pre, lesson = src(n)
    foot = f'<p class="foot">{lesson} Exit Ticket · {label} Version · Answer Key (teacher copy)</p>'
    rows = "".join(f'<tr><td>{q}</td><td><b>{a}</b></td></tr>' for q, a in zip(qs, ans))
    slides = (f'<section class="slide"><h1>Answer Key</h1><h3>{lesson} Exit Ticket · {label} Version</h3>'
              f'<p>3 questions, the same ones on the exit ticket slide of the {label} deck.</p>'
              f'<p class="warn">Teacher copy. Do not share with students.</p>{foot}</section>'
              f'<section class="slide"><h2>Exit ticket answers</h2><table style="font-size:20px"><tr><th>Question</th><th>Answer</th></tr>{rows}</table>'
              f'<p class="small"><b>Work:</b> {work}</p>{foot}</section>')
    out = HERE / folder / f"{pre}-exit-ticket-{kind}-ANSWER-KEY.html"
    out.write_text(f'<!doctype html><meta charset="utf-8"><title>{lesson} Exit Ticket Answer Key · {label}</title><body>{slides}</body>', encoding="utf-8")
    subprocess.run([sys.executable, str(HERE / "make_pptx.py"), out.relative_to(HERE).as_posix()], check=False)
    out.unlink()


def deck_link(kind, m):  # the accommodated bell work, homework and quiz sit next to the deck
    return f'href="{m.group(1)[:-5]}-{kind}.html"'


def main(lessons=(4, 5, 6)):
    for n in lessons:
        path = LESSONS[n]
        src = (HERE / path).read_text(encoding="utf-8")
        head, rest = src.split('<div id="stage">', 1)
        body, tail = rest.split("\n</div>\n", 1)
        sections = re.findall(r"<section class=\"slide[^\"]*\">.*?</section>\n", body, re.S)
        for kind, folder, label in (("504", "Section 504", "Section 504"), ("IEP", "IEP", "IEP")):
            if kind == "504":
                secs = build_504(n, sections)
            else:  # the general deck's bell work slides go right after the title, one per day
                secs = IEP[n]()
                secs[1:1] = bell_slides(n) if (n, 1) in BELL else [s for s in sections if re.search(r"Day \d · Bell Work", s)]
                tail = tail.replace(GRAPH_JS, DOT_JS + GRAPH_JS, 1)
                assert DOT_JS in tail or not isinstance(n, str), n
            html = head.replace("</title>", f" · {label}</title>", 1) + '<div id="stage">\n' + "".join(secs) + "\n</div>\n" + tail
            if kind == "504":
                html = html.replace('<p style="font-size:24px;margin-top:6px">Bell work:', '<p style="font-size:24px;margin-top:6px"><b>Section 504 Version</b></p>\n  <p style="font-size:24px;margin-top:6px">Bell work:', 1)
            html = re.sub(r'href="((?:t2-)?lesson\d-[^"]+\.html)"', lambda m: deck_link(kind, m), html)
            practice_pages(n, kind, folder)
            for name in ("bellwork", "homework", "quiz"):
                answer_key(n, kind, folder, name)
            exit_key(n, kind, folder, next(s for s in secs if ">Exit Ticket<" in s))
            out = HERE / folder / f"{OUT[n]}-{kind}.html"
            out.write_text(html, encoding="utf-8")
            subprocess.run([sys.executable, str(HERE / "make_pptx.py"), out.relative_to(HERE).as_posix()], check=False)


if __name__ == "__main__":
    main(("2.1", "2.2", "2.3", "2.4")) if sys.argv[1:] == ["t2"] else main()

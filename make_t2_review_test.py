# Topic 2 Review Test (Mon Nov 2): mirrors the 10-item End of Topic 2 Assessment in assessment/M2 TOPIC 2/AlgI_Assessments_SE.pdf
# item for item (same skill, type and layout, new numbers and answer letters), plus 4 extra-practice items to fill ~60 min.
# Writes General + key, Section 504 (same items, access supports; general key) and IEP (modified) + key, through headless Edge.  Run: python make_t2_review_test.py
import subprocess
from pathlib import Path

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
OUT = Path(__file__).parent / "assessment" / "M2 TOPIC 2"
KEY = False  # flipped per build


def fr(a, b):
    return f'<span class="fr"><span>{a}</span><span>{b}</span></span>'


def ans(s, why=""):  # red answer + short reason in the key; nothing in the student copy
    return f'<div class="ans">{s}' + (f'<div class="why">{why}</div>' if why else "") + "</div>" if KEY else ""


def blank(label, a, why=""):
    return (f'<p class="blank">{label} <span class="ln">{a if KEY else ""}</span></p>'
            + (f'<div class="ans"><div class="why">{why}</div></div>' if KEY and why else ""))


def mc(opts, right, letters="ABCD"):
    right = set(right)
    return '<div class="mc">' + "".join(
        f'<p class="{"ok" if KEY and l in right else ""}"><b>{l}.</b> {o}</p>' for l, o in zip(letters, opts)) + "</div>"


def grid(lo, hi, step, lab, lines=(), pts=(), size=300):
    s = size / (hi - lo)
    X, Y = (lambda v: (v - lo) * s), (lambda v: (hi - v) * s)
    o = [f'<svg class="g" viewBox="-22 -22 {size + 44} {size + 44}" width="{size + 44}"><defs><clipPath id="c{id(lines)}">'
         f'<rect width="{size}" height="{size}"/></clipPath></defs>']
    for v in range(lo, hi + 1, step):
        w = 1.6 if v == 0 else 0.6
        o.append(f'<line x1="{X(v)}" y1="0" x2="{X(v)}" y2="{size}" stroke="#000" stroke-width="{w}"/>'
                 f'<line x1="0" y1="{Y(v)}" x2="{size}" y2="{Y(v)}" stroke="#000" stroke-width="{w}"/>')
        if v and v % lab == 0:
            o.append(f'<text x="{X(v)}" y="{Y(0) + 13}" font-size="10" text-anchor="middle">{v}</text>'
                     f'<text x="{X(0) - 4}" y="{Y(v) + 3}" font-size="10" text-anchor="end">{v}</text>')
    o.append(f'<text x="{size + 6}" y="{Y(0) + 4}" font-size="13" font-style="italic">x</text>'
             f'<text x="{X(0) + 4}" y="-8" font-size="13" font-style="italic">y</text><g clip-path="url(#c{id(lines)})">')
    for (x1, y1), (x2, y2), color, dash, label in lines:
        if x1 == x2:
            a, b = (x1, lo - 1), (x1, hi + 1)
        else:
            m = (y2 - y1) / (x2 - x1)
            a, b = (lo - 1, y1 + m * (lo - 1 - x1)), (hi + 1, y1 + m * (hi + 1 - x1))
        o.append(f'<line x1="{X(a[0])}" y1="{Y(a[1])}" x2="{X(b[0])}" y2="{Y(b[1])}" stroke="{color}" stroke-width="2.4"'
                 + (' stroke-dasharray="7 5"' if dash else "") + "/>")
        if label:
            o.append(f'<text x="{X(x2) + 6}" y="{Y(y2) - 6}" font-size="13" fill="{color}" font-style="italic">{label}</text>')
    o.append("</g>")
    for x, y, label in pts:
        o.append(f'<circle cx="{X(x)}" cy="{Y(y)}" r="4" fill="#000"/>'
                 f'<text x="{X(x) + 6}" y="{Y(y) - 7}" font-size="12" font-weight="bold">{label}</text>')
    return "".join(o) + "</svg>"


RED = "#c8102e"


def items():
    i = lambda s: f"<i>{s}</i>"
    f, g, m, x, y = (i(c) for c in "fgmxy")
    return [
        # 1. a from a graph of m(x) = a·f(x)
        f"""<p>The graph of linear function {m} is shown on the grid.</p>
        {grid(-8, 8, 1, 2, [((-6, 4), (3, -2), "#000", False, "")], [(-6, 4, "(−6, 4)"), (3, -2, "(3, −2)")])}
        <p>Given {f}({x}) = {x} and {m}({x}) = {i("a")}{f}({x}), what is the value of {i("a")}?</p>
        {blank(i("a") + " =", "−" + fr(2, 3), "slope = (−2 − 4) ÷ (3 − (−6)) = −6/9 = −2/3, and a is the slope of m(x) = a·x")}""",
        # 2. range of a bounded real-world function
        f"""<p>The cost of renting a bounce house, {y}, for {x} hours at a birthday party can be modeled using a linear
        function. The rental company charges a fixed fee of $75, plus an additional $20 per hour. The bounce house can be
        rented for a maximum of 5 hours per day. For one day of rental, what is the range of the function for this situation?</p>
        {mc(["0 ≤ " + x + " ≤ 5", "20 ≤ " + y + " ≤ 175", "75 ≤ " + y + " ≤ 175", "0 ≤ " + x + " ≤ 7"], "C")}
        {ans("", "Range = the costs (y). 0 hours: $75. 5 hours: 75 + 20(5) = $175. Choices about x are the domain.")}""",
        # 3. horizontal line: equation and slope
        f"""<p>What are the equation and slope of the line shown on the grid?</p>
        {grid(-40, 40, 10, 10, [((-40, -20), (40, -20), "#000", False, "")], size=280)}
        {mc([x + " = −20; slope is zero", y + " = −20; slope is undefined", y + " = −20; slope is zero",
             x + " = −20; slope is undefined"], "H", "FGHJ")}
        {ans("", "Horizontal line: every y-value is −20, so y = −20. It never rises, so the slope is zero.")}""",
        # 4. horizontal translation f(x - h)
        f"""<p>Marcus graphed {f}({x}) and {g}({x}) = {f}({x} − 3) on the same coordinate grid. Which statement describes
        how the graphs of {f} and {g} are related?</p>
        {mc([f"The graph of the function {f}({x}) is translated up 3 units to produce {g}({x}).",
             f"The graph of the function {f}({x}) is translated down 3 units to produce {g}({x}).",
             f"The graph of the function {f}({x}) is translated right 3 units to produce {g}({x}).",
             f"The graph of the function {f}({x}) is translated left 3 units to produce {g}({x})."], "C")}
        {ans("", "A change inside the parentheses moves the graph sideways, opposite the sign: x − 3 → right 3.")}""",
        # 5. y-intercept after translating a table
        f"""<p>What is the {y}-intercept of the linear function created by translating {f}({x}), represented in the table,
        2 units right?</p>
        <table class="t"><tr><th>{x}</th><th>{f}({x})</th></tr>"""
        + "".join(f"<tr><td>{a}</td><td>{3 * a - 1}</td></tr>".replace("-", "−") for a in range(-2, 4)) + f"""</table>
        {blank(y + "-intercept =", "−7", "Slide every x 2 right: the point (−2, −7) moves to (0, −7). Or g(x) = 3(x − 2) − 1 = 3x − 7.")}""",
        # 6. graph g(x) = f(kx)
        f"""<p>Graph {g}({x}) based on the given transformation of {f}({x}).</p>
        <p>{f}({x}) = {x} &nbsp;&nbsp;&nbsp; {g}({x}) = {f}(2{x})</p>
        {grid(-8, 8, 1, 2, [((0, 0), (5, 5), "#000", True, "f(x)")]
              + ([((0, 0), (3, 6), RED, False, "g(x)")] if KEY else []))}
        {ans("g(x) = 2x: a line through (0, 0), (1, 2) and (3, 6)", "f(2x) multiplies each input by 2, so the outputs double: slope 2.")}""",
        # 7. perpendicular through an x-intercept
        f"""<p>What is the equation in slope-intercept form of the line that crosses the {x}-axis at −6 and is perpendicular
        to the line represented by {y} = {fr(3, 2)}{x} − 1?</p><div class="work"></div>
        {blank("Equation:", y + " = −" + fr(2, 3) + x + " − 4",
               "Perpendicular slope = negative reciprocal of 3/2 = −2/3. Point (−6, 0): 0 = −2/3(−6) + b → b = −4.")}""",
        # 8. parallel through a point
        f"""<p>What is the equation in slope-intercept form of the line that passes through the point (5, 0) and is parallel
        to the line represented by {y} = −2.4{x} + 1.6?</p><div class="work"></div>
        {blank("Equation:", y + " = −2.4" + x + " + 12", "Parallel → same slope −2.4. 0 = −2.4(5) + b → b = 12.")}""",
        # 9. point-slope form from a graph
        f"""<p>Write an equation in point-slope form that represents the graph.</p>
        {grid(-8, 8, 1, 2, [((-2, -3), (2, 5), "#000", False, "")], [(-2, -3, "(−2, −3)"), (2, 5, "(2, 5)")])}
        {blank("Equation:", y + " − 5 = 2(" + x + " − 2)",
               "slope = (5 − (−3)) ÷ (2 − (−2)) = 8/4 = 2. Also correct: y + 3 = 2(x + 2).")}""",
        # 10. select two: increasing/slope/intercepts
        f"""<p>The graph of a linear function is shown on the coordinate plane.</p>
        {grid(-8, 8, 1, 2, [((-4, 0), (0, 2), "#000", False, "")])}
        <p>Which statements describe the graph of the linear function? <b>Select TWO correct answers.</b></p>
        {mc(["The graph is increasing.", "The slope of the line is 2.", f"The {y}-intercept is (0, −4).",
             "The zero of the function is −4.", "The zero of the function is 2."], "FJ", "FGHJK")}
        {ans("", "It rises left to right (increasing). It crosses the x-axis at −4, so the zero is −4. Slope = 2/4 = 1/2; y-intercept (0, 2).")}""",
        # extra practice
        f"""<p>Let {f}({x}) = {x} − 1, {g}({x}) = {f}(2{x}), and {i("h")}({x}) = 2{f}({x}). Which statement is true?</p>
        {mc([f"{g}({x}) and {i('h')}({x}) are the same function.",
             f"{g}({x}) and {i('h')}({x}) have the same slope but different {y}-intercepts.",
             f"{g}({x}) and {i('h')}({x}) have different slopes but the same {y}-intercept.",
             f"{g}({x}) and {i('h')}({x}) have different slopes and different {y}-intercepts."], "B")}
        {ans("", "g(x) = 2x − 1 and h(x) = 2(x − 1) = 2x − 2: both slope 2, y-intercepts −1 and −2.")}""",
        f"""<p>Which pair of equations represents perpendicular lines?</p>
        {mc([f"{y} = 5{x} + 1 and {y} = −5{x} + 2", f"{y} = −{fr(1, 3)}{x} + 4 and {y} = 3{x} − 2",
             f"{y} = {fr(4, 5)}{x} and {y} = {fr(5, 4)}{x} − 1", f"{y} = 2{x} + 3 and {y} = 2{x} − 3"], "B", "FGHJ")}
        {ans("", "Perpendicular slopes are negative reciprocals: −1/3 × 3 = −1. (J is parallel.)")}""",
        f"""<p>{f}({x}) = 2{x} + 1 and {g}({x}) = {f}({x}) − 4. Write the equation of {g}({x}) and describe how the graph of
        {f} moves to make the graph of {g}.</p><div class="work"></div>
        {blank(g + "(" + x + ") =", "2" + x + " − 3", "Subtract 4 from every output: 2x + 1 − 4 = 2x − 3. The graph moves down 4 units.")}
        {blank("Description:", "translated down 4 units" if KEY else "")}""",
        f"""<p>A tank holds 300 gallons of water. It drains at 15 gallons per minute until it is empty. Let {x} be the number
        of minutes. What is the domain of the function for this situation?</p>
        {mc(["0 ≤ " + x + " ≤ 300", "0 ≤ " + x + " ≤ 20", "0 ≤ " + y + " ≤ 300", "15 ≤ " + x + " ≤ 300"], "B")}
        {ans("", "Domain = the minutes (x). Empty when 300 ÷ 15 = 20 minutes.")}""",
    ]


# ---------------------------------------------------------------- IEP (modified): same 14 skills
def B(v):  # fill-in blank; filled in red on the key
    return f'<span class="bl">{v if KEY else ""}</span>'


def c1(a, b, right):  # circle-one choice
    w = lambda s: f'<span class="cir">{s}</span>' if KEY and s == right else s
    return f"<b>{w(a)} / {w(b)}</b> (circle one)"


def tip(s):
    return f'<div class="tip"><b>Tip:</b> {s}</div>'


def iep_items():
    i = lambda s: f"<i>{s}</i>"
    f, g, m, x, y = (i(c) for c in "fgmxy")
    return [
        f"""<p>The graph of linear function {m} is shown. Given {f}({x}) = {x} and {m}({x}) = {i("a")}{f}({x}), find {i("a")}.</p>
        {tip(f"In {m}({x}) = {i('a')}·{x}, the number {i('a')} is the <b>slope</b> of the line.")}
        {grid(-8, 8, 1, 2, [((-6, 4), (3, -2), "#000", False, "")], [(-6, 4, "(−6, 4)"), (3, -2, "(3, −2)")])}
        <p>Step 1: slope = {fr("−2 − 4", "3 − (−6)")} = {fr(B("−6"), B("9"))}</p>
        <p>Step 2: Simplify. {i("a")} = {B("−2/3")}</p>""",
        f"""<p>A bounce house costs $75, plus $20 per hour. It can be rented for at most 5 hours. What is the <b>range</b>?</p>
        {tip("<b>Range</b> = the costs (the y-values).")}
        <p>Step 1: Cost for 0 hours: 75 + 20(0) = {B("75")}</p><p>Step 2: Cost for 5 hours: 75 + 20(5) = {B("175")}</p>
        {mc(["0 ≤ " + x + " ≤ 5", "75 ≤ " + y + " ≤ 175", "20 ≤ " + y + " ≤ 175"], "B", "ABC")}""",
        f"""<p>What are the <b>equation and slope</b> of the line shown on the grid?</p>
        {tip(f"A flat (horizontal) line is {y} = a number. Its slope is <b>zero</b>.")}
        {grid(-40, 40, 10, 10, [((-40, -20), (40, -20), "#000", False, "")], [(0, -20, "(0, −20)")], size=280)}
        {mc([y + " = −20; slope is zero", x + " = −20; slope is undefined", y + " = −20; slope is undefined"], "A", "ABC")}""",
        f"""<p>Marcus graphed {f}({x}) and {g}({x}) = {f}({x} − 3). How does the graph of {f} move to make {g}?</p>
        {tip("A number <b>inside</b> the parentheses moves the graph left or right, the <b>opposite</b> way of the sign: − 3 → right.")}
        {mc(["up 3 units", "right 3 units", "left 3 units"], "B", "ABC")}""",
        f"""<p>Move {f}({x}) in the table <b>2 units right</b>. What is the new <b>{y}-intercept</b>?</p>
        {tip(f"Right 2 means add 2 to each {x}. The {y}-intercept is the point where {x} = 0.")}
        <table class="t"><tr><th>{x}</th><th>{f}({x})</th></tr>"""
        + "".join(f"<tr><td>{a}</td><td>{3 * a - 1}</td></tr>".replace("-", "−") for a in range(-2, 4)) + f"""</table>
        <p>Step 1: The first row is the point (−2, {B("−7")}).</p>
        <p>Step 2: Move it right 2: (−2 + 2, {B("−7")}) = (0, {B("−7")})</p><p>Step 3: New {y}-intercept = {B("−7")}</p>""",
        f"""<p>{f}({x}) = {x} (dashed) and {g}({x}) = {f}(2{x}). Graph {g}({x}).</p>
        {tip(f"{f}(2{x}) means put 2{x} in for {x}: {g}({x}) = 2{x}.")}
        <p>Step 1: Fill in the table for {g}({x}) = 2{x}.</p>
        <table class="t"><tr><th>{x}</th><td>0</td><td>1</td><td>2</td><td>3</td></tr>
        <tr><th>{g}({x})</th><td>{B("0")}</td><td>{B("2")}</td><td>{B("4")}</td><td>{B("6")}</td></tr></table>
        <p>Step 2: Plot the points and connect them with a line.</p>
        {grid(-8, 8, 1, 2, [((0, 0), (5, 5), "#000", True, "f(x)")] + ([((0, 0), (3, 6), RED, False, "g(x)")] if KEY else []))}""",
        f"""<p>Write the equation in <b>slope-intercept form</b> of the line that crosses the {x}-axis at −6 and is
        <b>perpendicular</b> to {y} = {fr(3, 2)}{x} − 1.</p>
        {tip("<b>Perpendicular</b> slope: flip the fraction and change the sign.")}
        <p>Step 1: The slope of {y} = {fr(3, 2)}{x} − 1 is {B("3/2")}.</p>
        <p>Step 2: The perpendicular slope is {B("−2/3")}.</p>
        <p>Step 3: Crossing the {x}-axis at −6 is the point ({B("−6")}, {B("0")}).</p>
        <p>Step 4: 0 = −{fr(2, 3)}(−6) + {i("b")}, so {i("b")} = {B("−4")}</p>
        <p>Step 5: {y} = {B("−2/3")}{x} + {B("(−4)")}</p>""",
        f"""<p>Write the equation in <b>slope-intercept form</b> of the line through (5, 0) that is <b>parallel</b> to
        {y} = −2.4{x} + 1.6.</p>
        {tip("<b>Parallel</b> lines have the <b>same</b> slope.")}
        <p>Step 1: Slope = {B("−2.4")}</p><p>Step 2: 0 = −2.4(5) + {i("b")} → 0 = {B("−12")} + {i("b")} → {i("b")} = {B("12")}</p>
        <p>Step 3: {y} = {B("−2.4")}{x} + {B("12")}</p>""",
        f"""<p>Write an equation in <b>point-slope form</b> for the graph.</p>
        {tip(f"Point-slope form: {y} − {y}₁ = {m}({x} − {x}₁). Use the point (2, 5).")}
        {grid(-8, 8, 1, 2, [((-2, -3), (2, 5), "#000", False, "")], [(-2, -3, "(−2, −3)"), (2, 5, "(2, 5)")])}
        <p>Step 1: slope = {fr("5 − (−3)", "2 − (−2)")} = {fr(B("8"), B("4"))} = {B("2")}</p>
        <p>Step 2: {y} − {B("5")} = {B("2")}({x} − {B("2")})</p>""",
        f"""<p>The graph of a linear function is shown. Which statements are true? <b>Select TWO correct answers.</b></p>
        {tip("The <b>zero</b> is where the line crosses the x-axis. <b>Increasing</b> means it goes up from left to right.")}
        {grid(-8, 8, 1, 2, [((-4, 0), (0, 2), "#000", False, "")], [(-4, 0, "(−4, 0)"), (0, 2, "(0, 2)")])}
        {mc(["The graph is increasing.", "The slope of the line is 2.", "The zero of the function is −4.",
             "The zero of the function is 2."], "AC", "ABCD")}""",
        f"""<p>{f}({x}) = {x} − 1, {g}({x}) = {f}(2{x}), and {i("h")}({x}) = 2{f}({x}). Compare {g} and {i("h")}.</p>
        {tip(f"{f}(2{x}): put 2{x} in for {x}. 2{f}({x}): multiply the whole function by 2.")}
        <p>Step 1: {g}({x}) = 2{x} − {B("1")}</p><p>Step 2: {i("h")}({x}) = 2({x} − 1) = 2{x} − {B("2")}</p>
        <p>Step 3: Same slope? {c1("yes", "no", "yes")} &nbsp; Same {y}-intercept? {c1("yes", "no", "no")}</p>""",
        f"""<p>Which pair of equations represents <b>perpendicular</b> lines?</p>
        {tip("Multiply the two slopes. If you get <b>−1</b>, the lines are perpendicular.")}
        {mc([f"{y} = 5{x} + 1 and {y} = −5{x} + 2", f"{y} = −{fr(1, 3)}{x} + 4 and {y} = 3{x} − 2",
             f"{y} = 2{x} + 3 and {y} = 2{x} − 3"], "B", "ABC")}""",
        f"""<p>{f}({x}) = 2{x} + 1 and {g}({x}) = {f}({x}) − 4. Write {g}({x}) and describe the move.</p>
        {tip("A number <b>outside</b> the function moves the graph up or down.")}
        <p>Step 1: {g}({x}) = 2{x} + 1 − 4 = 2{x} − {B("3")}</p>
        <p>Step 2: The graph moves {c1("up", "down", "down")} {B("4")} units.</p>""",
        f"""<p>A 300-gallon tank drains 15 gallons per minute until it is empty. What is the <b>domain</b>?</p>
        {tip("<b>Domain</b> = the minutes (the x-values).")}
        <p>Step 1: Minutes to empty: 300 ÷ 15 = {B("20")}</p>
        {mc(["0 ≤ " + x + " ≤ 300", "0 ≤ " + x + " ≤ 20", "0 ≤ " + y + " ≤ 300"], "B", "ABC")}""",
    ]


CSS = """
@page { size: letter; margin: 0.5in 0.6in 0.55in; }
body { font-family: Arial, Helvetica, sans-serif; font-size: 12pt; line-height: 1.35; color: #111; background: #fff; margin: 0; }
header { border-bottom: 2px solid #111; margin-bottom: 8px; } h1 { font-size: 19pt; margin: 0; } .sub { margin: 2px 0 6px; }
.dir { font-size: 11pt; margin: 4px 0 8px; } .part { font-size: 13pt; font-weight: bold; background: #eee; padding: 3px 8px; margin: 10px 0 6px; }
.q { break-inside: avoid; display: flex; gap: 8px; padding: 6px 0 10px; border-bottom: 1px solid #bbb; min-height: 3.3in; }
.n { font-weight: bold; min-width: 28px; } .q p { margin: 3px 0 6px; } .g { display: block; margin: 4px 0 6px; }
.mc p { margin: 4px 0 4px 10px; } .mc .ok { color: #c8102e; font-weight: bold; } .mc .ok b { border: 2px solid #c8102e; border-radius: 50%; padding: 0 4px; }
.blank { margin-top: 10px; } .ln { display: inline-block; min-width: 2.4in; border-bottom: 1px solid #111; color: #c8102e; font-weight: bold; padding: 0 6px; }
.ans { color: #c8102e; font-weight: bold; margin-top: 4px; } .why { font-weight: normal; font-size: 10.5pt; }
.work { height: 1.3in; } .t { border-collapse: collapse; margin: 4px 0; } .t td, .t th { border: 1px solid #111; padding: 2px 14px; text-align: center; }
.fr { display: inline-flex; flex-direction: column; vertical-align: middle; text-align: center; font-size: 0.85em; line-height: 1.1; }
.fr span:first-child { border-bottom: 1px solid currentColor; padding: 0 2px; }
"""


# Section 504: same items, wording and choices (graded with the same key); access supports only.
CSS504 = """
body { font-size: 15pt; line-height: 1.45; } .dir { font-size: 13.5pt; } .why { font-size: 12pt; }
.q { break-before: page; border-bottom: none; min-height: 0; } .q .g { width: 4.6in; } .work { height: 2.4in; }
.tip { border-left: 5px solid #2f6fdd; background: #eef3fc; padding: 4px 10px; margin: 6px 0; }
.bl { display: inline-block; min-width: 0.9in; border-bottom: 1.5px solid #111; text-align: center; color: #c8102e; font-weight: bold; }
.cir { color: #c8102e; border: 2px solid #c8102e; border-radius: 50%; padding: 0 5px; } .t td { min-width: 0.4in; }
.ref { border: 2px solid #111; border-radius: 6px; padding: 6px 12px; font-size: 13pt; } .ref p { margin: 3px 0; }
"""
REF504 = """<div class="ref"><p><b>Reference box</b></p>
<p>Slope: <b>m = (y₂ − y₁) ÷ (x₂ − x₁)</b> &nbsp;·&nbsp; Slope-intercept form: <b>y = mx + b</b> &nbsp;·&nbsp; Point-slope form: <b>y − y₁ = m(x − x₁)</b></p>
<p><b>Parallel</b> lines: same slope. &nbsp; <b>Perpendicular</b> lines: negative reciprocal slopes (2 and −½).</p>
<p><b>f(x) + k</b>: up k &nbsp;·&nbsp; <b>f(x) − k</b>: down k &nbsp;·&nbsp; <b>f(x − h)</b>: right h &nbsp;·&nbsp; <b>f(x + h)</b>: left h &nbsp;·&nbsp; <b>a·f(x)</b> or <b>f(ax)</b>: steeper or flatter</p>
<p><b>Domain</b> = inputs (x). &nbsp; <b>Range</b> = outputs (y). &nbsp; <b>Zero</b> = where the line crosses the x-axis.</p></div>"""
KEYWORDS = ["value of", "range", "domain", "equation and slope", "translated", "y</i>-intercept", "slope-intercept form",
            "perpendicular", "parallel", "point-slope form", "Select TWO correct answers", "same function", "true",
            "describe how the graph", "2 units right"]


def bold_keys(q):  # bold key words in the question stem only, never inside the answer choices or graphs
    stem, sep, rest = q.partition('<div class="mc">')
    parts = stem.split("<svg")
    for kw in KEYWORDS:
        parts[0] = parts[0].replace(kw, f"<b>{kw}</b>", 1)
    return "<svg".join(parts) + sep + rest


def build(key, v504=False, iep=False):
    global KEY
    KEY = key
    v504 = v504 or iep  # IEP keeps the 504 layout and reference box
    qs = iep_items() if iep else [bold_keys(q) for q in items()] if v504 else items()
    label = " · IEP" if iep else " · Section 504" if v504 else ""
    dirs = ('<b>Directions:</b> This review has the same kinds of questions as the Topic 2 test. Read each question carefully. '
            + ('Use the steps and tips. Fill in each blank. For multiple choice, choose <b>one</b> answer unless it says '
               '<b>Select TWO</b>.' if iep else
               'Show your work. <b>Select TWO</b> means choose exactly two answers.')
            + ' Finish Part 1 first; Part 2 is extra practice.'
            + (' <br>One question is on each page. Take your time. You may use a calculator and the reference box. Ask your '
               'teacher if you need a break or a question read aloud.' if v504 else ""))
    body = (f'<header><h1>Topic 2 Review Test{label}{" · ANSWER KEY" if key else ""}</h1>'
            '<p class="sub">Algebra I · Module 2, Topic 2: Transforming and Comparing Linear Functions · Monday, Nov 2</p>'
            + ("" if key else '<p class="sub">Name ______________________________ &nbsp; Period _____ &nbsp; Date __________</p>')
            + f'</header><p class="dir">{dirs}</p>' + (REF504 if v504 else "")
            + f'<div class="part"{" style=break-before:page" if v504 else ""}>Part 1 · Just like the test (Questions 1–10)</div>')
    for n, q in enumerate(qs, 1):
        if n == 11:
            body += '<div class="part" style="break-before:page">Part 2 · Extra practice (Questions 11–14)</div>'
        body += (f'<div class="q"{" style=break-before:auto" if v504 and n in (1, 11) else ""}>'
                 f'<div class="n">{n}.</div><div>{q}</div></div>')
    name = "Topic2-Review-Test" + ("-IEP" if iep else "-504" if v504 else "") + ("-ANSWER-KEY" if key else "")
    src = OUT / f"{name}.html"
    src.write_text(f"<!doctype html><meta charset='utf-8'><title>{name}</title><style>{CSS}{CSS504 if v504 else ''}</style>{body}",
                   encoding="utf-8")
    pdf = OUT / f"{name}.pdf"
    subprocess.run([EDGE, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={pdf}", src.as_uri()],
                   check=True, capture_output=True)
    src.unlink()
    print(pdf)


if __name__ == "__main__":
    build(False)
    build(True)
    build(False, v504=True)  # graded with the general key: same items and letters
    build(False, iep=True)
    build(True, iep=True)

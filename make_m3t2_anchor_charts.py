"""Anchor charts for Module 3 Topic 2: Systems of Linear Equations and Inequalities (two per lesson, letter size).
Same style as make_m3t1_anchor_charts.py.  Run: python make_m3t2_anchor_charts.py
 -> Module 3 topic 2/ANCHOR CHARTS/M3T2-Anchor-Charts.pdf  (print all ten)
 -> Module 3 topic 2/ANCHOR CHARTS/M3T2-L{n}-Anchor-{k}.jpg  (one picture per chart, shown on the web pages)"""
import subprocess
from pathlib import Path

import fitz
from PIL import Image

from make_t2_posters import CSS, EDGE, M, box, c, fr, graph, table, INK, BLUE, ORANGE, GREEN, PURPLE
from make_m3t1_anchor_charts import EXTRA, RED, steps

ROOT = Path(__file__).parent
OUT = ROOT / "Module 3 topic 2" / "ANCHOR CHARTS"
TOTAL = 10


def chart(n, lesson, title, formula, body, col=BLUE):
    return (f'<section class="page"><div class="top"><header style="background:{col}"><span>Module 3 · Topic 2 · {lesson}</span>'
            f'<span>Anchor chart {n} / {TOTAL}</span></header><h1>{title}</h1><div class="formula">{formula}</div></div>{body}'
            f'<footer>Bluebonnet Algebra I · Systems of Linear Equations and Inequalities · Mr. Pandey</footer></section>')


def above(m, b): return (-m, 1, -b)   # y >= mx + b  as  a*x + b*y + c >= 0
def below(m, b): return (m, -1, b)    # y <= mx + b
RIGHT_OF_Y_AXIS, ABOVE_X_AXIS = (1, 0, 0), (0, 1, 0)


def shade(cons, col, lo=-6, hi=6, size=430, op=0.22):
    """Shade the region where every constraint a*x + b*y + c >= 0 holds (polygon clipping of the view box)."""
    poly = [(lo - 1, lo - 1), (hi + 1, lo - 1), (hi + 1, hi + 1), (lo - 1, hi + 1)]
    for a, b, k in cons:
        f = lambda p: a * p[0] + b * p[1] + k
        out = []
        for i, p in enumerate(poly):
            q = poly[(i + 1) % len(poly)]
            if f(p) >= 0:
                out.append(p)
            if (f(p) >= 0) != (f(q) >= 0):
                t = f(p) / (f(p) - f(q))
                out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
        poly = out
    s = size / (hi - lo)
    pts = " ".join(f"{(x - lo) * s:.1f},{(hi - y) * s:.1f}" for x, y in poly)
    return f'<polygon points="{pts}" fill="{col}" fill-opacity="{op}" stroke="none"/>'


def charts():
    P = []
    # 1 · Lesson 1: solve by graphing
    P.append(chart(1, "Lesson 1", "Solve a System by Graphing", "The solution is where the lines cross",
        '<div class="row">' + graph([(1, 1, BLUE, "y = x + 1", 2.4), (-2, 4, ORANGE, "y = −2x + 4", 2.6)],
                                    [(1, 2, "(1, 2)", GREEN, 12, -10)])
        + '<div class="col"><ol class="steps">'
          "<li><b>Graph</b> both equations on the same plane.</li>"
          "<li><b>Find</b> the point where the lines intersect.</li>"
          "<li><b>Check</b> the point in <b>both</b> equations.</li></ol>"
        + box("Check (1, 2)", f"<p>{M('2 = 1 + 1')} <span class='ok'>✓</span></p><p>{M('2 = −2(1) + 4')} <span class='ok'>✓</span></p>", GREEN)
        + "</div></div>"
        + f'<p class="key">A <b>system of linear equations</b> is two or more equations with the same variables. '
          f'Its <b>solution</b> is an ordered pair that makes <b>every</b> equation true.</p>'
        + '<p class="lead">Tip: write each equation in slope-intercept form first, or graph using the intercepts. '
          "Use graphing technology to check.</p>"))

    # 2 · Lesson 1: number of solutions
    mini = lambda lines: graph(lines, (), lo=-5, hi=5, size=200)
    P.append(chart(2, "Lesson 1", "How Many Solutions?", "Compare slopes and y-intercepts",
        '<div class="grid2" style="grid-template-columns:1fr 1fr 1fr">'
        + box("One solution", mini([(1, 0, BLUE, "", 0), (-1, 2, ORANGE, "", 0)])
              + "<p>Lines <b>intersect</b>.</p><p>Different slopes.</p><p class='ok'>Consistent</p>", GREEN)
        + box("No solution", mini([(1, 2, BLUE, "", 0), (1, -2, ORANGE, "", 0)])
              + "<p>Lines are <b>parallel</b>.</p><p>Same slope, different <i>y</i>-intercepts.</p><p class='no'>Inconsistent</p>", RED)
        + box("Infinite solutions", mini([(2, -1, BLUE, "", 0), (2, -1, ORANGE, "", 0, "dash")])
              + "<p><b>Same line</b>.</p><p>Same slope, same <i>y</i>-intercept.</p><p class='ok'>Consistent</p>", BLUE) + "</div>"
        + table(["System", "Slopes", "y-intercepts", "Solutions"],
                [[M("y = x") + ", " + M("y = −x + 2"), "different", "any", "one: (1, 1)"],
                 [M("y = x + 2") + ", " + M("y = x − 2"), "same", "different", "none"],
                 [M("y = 2x − 1") + ", " + M("4x − 2y = 2"), "same", "same", "infinitely many"]], "full tight")
        + '<p class="key">A <b>consistent</b> system has at least one solution. An <b>inconsistent</b> system has none.</p>', PURPLE))

    # 3 · Lesson 2: substitution method
    P.append(chart(3, "Lesson 2", "Substitution Method", "Replace a variable with an equal expression",
        '<ol class="steps big4">'
        "<li><b>Solve</b> one equation for one variable (look for one already alone).</li>"
        "<li><b>Substitute</b> that expression into the <b>other</b> equation.</li>"
        "<li><b>Solve</b> for the remaining variable.</li>"
        "<li><b>Substitute back</b> to find the other variable.</li>"
        "<li><b>Check</b> the ordered pair in both equations.</li></ol>"
        + box("Example: " + M("y = 2x − 1") + " and " + M("3x + y = 9"), steps([
            ("3x + (2x − 1) = 9", "Substitute 2x − 1 for y"),
            ("5x − 1 = 9", "Combine like terms"),
            ("x = 2", "Add 1, divide by 5"),
            ("y = 2(2) − 1 = 3", "Substitute back"),
            (c("(2, 3)", GREEN), "Solution")]), BLUE)
        + f'<p class="key">Check: {M("3 = 2(2) − 1")} <span class="ok">✓</span> and {M("3(2) + 3 = 9")} <span class="ok">✓</span></p>', ORANGE))

    # 4 · Lesson 2: special cases and context
    P.append(chart(4, "Lesson 2", "Substitution: Read the Result", "Variable gone? Check the statement",
        '<div class="grid2">'
        + box("No solution", f"<p>{M('y = 3x + 2')} and {M('−6x + 2y = 10')}</p><p class='big'>{M('−6x + 2(3x + 2) = 10')}</p>"
              f"<p class='ans' style='color:{RED}'>{M('4 = 10')} False</p>", RED)
        + box("Infinite solutions", f"<p>{M('y = 2x + 1')} and {M('4x − 2y = −2')}</p><p class='big'>{M('4x − 2(2x + 1) = −2')}</p>"
              f"<p class='ans' style='color:{BLUE}'>{M('−2 = −2')} Always true</p>", BLUE) + "</div>"
        + box("In context: movie tickets", "<p>12 tickets cost $80. Adult tickets are $9 and student tickets are $5. How many of each?</p>"
              + steps([("a + s = 12", "<b>a</b> = adult tickets, <b>s</b> = student tickets"),
                       ("9a + 5s = 80", "Cost equation"),
                       ("9a + 5(12 − a) = 80", "Substitute s = 12 − a"),
                       (c("a = 5,  s = 7", GREEN), "5 adult, 7 student tickets")]), ORANGE)
        + '<p class="key">Define the variables, write the system, solve, answer in words.</p>', ORANGE))

    # 5 · Lesson 3: linear combinations
    P.append(chart(5, "Lesson 3", "Linear Combinations", "Add the equations to eliminate a variable",
        '<p class="key"><b>Additive inverses</b> add to zero: 3<i>y</i> and −3<i>y</i>. '
        "Line up the equations in standard form, then add them so one variable drops out.</p>"
        + box("Example", steps([
            ("2x + 3y = 12", "Equation 1"),
            ("4x − 3y = 6", "Equation 2: 3y and −3y are inverses"),
            ("6x = 18", "Add the equations"),
            ("x = 3", "Divide by 6"),
            ("2(3) + 3y = 12  →  y = 2", "Substitute back"),
            (c("(3, 2)", GREEN), "Solution")]), BLUE)
        + f'<p class="key">Check: {M("2(3) + 3(2) = 12")} <span class="ok">✓</span> and {M("4(3) − 3(2) = 6")} <span class="ok">✓</span></p>', GREEN))

    # 6 · Lesson 3: multiply first; choosing a method
    P.append(chart(6, "Lesson 3", "Multiply First, Then Add", "Make the coefficients opposites",
        box("Example: " + M("x + 2y = 7") + " and " + M("3x − y = 7"), steps([
            ("6x − 2y = 14", "Multiply equation 2 by <b>2</b>: now 2y and −2y"),
            ("7x = 21", "Add to equation 1"),
            ("x = 3", "Divide by 7"),
            ("3 + 2y = 7  →  y = 2", "Substitute back"),
            (c("(3, 2)", GREEN), "Solution")]), BLUE)
        + table(["Method", "Best when…"],
                [["<b>Graphing</b>", "you want a picture or an estimate; use technology to check"],
                 ["<b>Substitution</b>", "a variable is already alone, like " + M("y = 2x − 1")],
                 ["<b>Linear combinations</b>", "both equations are in standard form " + M("Ax + By = C")]], "full tight")
        + f'<p class="key">Multiply <b>every</b> term, including the constant. {M("3x − y = 7")} × 2 is {M("6x − 2y = 14")}.</p>', GREEN))

    # 7 · Lesson 4: graph an inequality
    P.append(chart(7, "Lesson 4", "Graph a Linear Inequality", "Boundary line, test point, shade",
        '<div class="row">' + graph([(2, -3, BLUE, "y = 2x − 3", 2.1, "dash")], [(0, 0, "(0, 0)", GREEN, 10, 22)],
                                    marks=shade([above(2, -3)], BLUE))
        + '<div class="col"><ol class="steps">'
          f"<li><b>Graph the boundary</b> {M('y = 2x − 3')}.</li>"
          "<li><b>Dashed</b> for &lt; or &gt;. <b>Solid</b> for ≤ or ≥.</li>"
          f"<li><b>Test</b> {M('(0, 0)')}: {M('0 > 2(0) − 3')} → {M('0 > −3')} <span class='ok'>true</span></li>"
          "<li><b>Shade</b> the side with the test point. False? Shade the other side.</li></ol></div></div>"
        + box("Example: " + M("y > 2x − 3"), "<p>The line is <b>dashed</b> because points on it are <b>not</b> solutions. "
              "Every point in the shaded <b>half-plane</b> is a solution.</p>", BLUE)
        + '<p class="key">If the boundary passes through (0, 0), test a different point, like (1, 0).</p>', PURPLE))

    # 8 · Lesson 4: line type and shading
    P.append(chart(8, "Lesson 4", "Solid or Dashed? Which Side?", "Read the symbol",
        table(["Symbol", "Line", "Points on the line", "Shade"],
              [[M("y >"), "dashed", "not solutions", "above"],
               [M("y ≥"), "solid", "solutions", "above"],
               [M("y <"), "dashed", "not solutions", "below"],
               [M("y ≤"), "solid", "solutions", "below"]], "full tight")
        + '<p class="lead">Shade above or below when <i>y</i> is alone on the left. Otherwise, use a test point.</p>'
        + '<div class="row">' + graph([(-2 / 3, 2, ORANGE, "2x + 3y = 6", -5.2)], [(0, 0, "(0, 0)", GREEN, 10, 22)],
                                      size=330, marks=shade([below(-2 / 3, 2)], ORANGE))
        + '<div class="col">' + box("Example: " + M("2x + 3y ≤ 6"),
              f"<p>Solid line through {M('(3, 0)')} and {M('(0, 2)')}.</p><p>Test {M('(0, 0)')}: {M('0 ≤ 6')} <span class='ok'>true</span>, "
              "so shade the side with the origin.</p>", ORANGE)
        + box("Equation vs inequality", "<p>Equation: solutions are <b>on the line</b>.</p>"
              "<p>Inequality: solutions fill a <b>half-plane</b>.</p>", BLUE) + "</div></div>", PURPLE))

    # 9 · Lesson 5: systems of inequalities
    P.append(chart(9, "Lesson 5", "Systems of Linear Inequalities", "The solution is the overlap",
        '<div class="row">' + graph([(1, -2, BLUE, "y ≥ x − 2", 3.6), (-1, 4, ORANGE, "y < −x + 4", -1.3, "dash")],
                                    [(0, 0, "(0, 0)", GREEN, 10, 22)],
                                    marks=shade([above(1, -2)], BLUE, op=0.14) + shade([below(-1, 4)], ORANGE, op=0.14)
                                    + shade([above(1, -2), below(-1, 4)], PURPLE, op=0.3))
        + '<div class="col"><ol class="steps">'
          "<li><b>Graph</b> each inequality: boundary line, then shade.</li>"
          "<li>The <b>overlap</b> (darkest region) is the solution set.</li>"
          "<li><b>Check</b> a point from the overlap in <b>both</b> inequalities.</li></ol>"
        + box("Check (0, 0)", f"<p>{M('0 ≥ 0 − 2')} <span class='ok'>✓</span></p><p>{M('0 < 0 + 4')} <span class='ok'>✓</span></p>", GREEN)
        + "</div></div>"
        + '<p class="key">A <b>system of linear inequalities</b> is two or more inequalities. '
          "Its solutions are every point that makes <b>all</b> of them true.</p>"))

    # 10 · Lesson 5: is it a solution? context
    q = graph([(-1, 10, BLUE, "x + y = 10", 6.2), (-1.5, 12, ORANGE, "15x + 10y = 120", 0.4)], [(8, 1, "(8, 1)", GREEN, -64, 8)],
              lo=0, hi=12, size=330, marks=shade([below(-1, 10), above(-1.5, 12), RIGHT_OF_Y_AXIS, ABOVE_X_AXIS], PURPLE, 0, 12, 330, 0.35))
    P.append(chart(10, "Lesson 5", "Is It a Solution?", "True in every inequality = solution",
        table(["Point", M("y ≥ x − 2"), M("y < −x + 4"), "Solution?"],
              [[M("(0, 0)"), "0 ≥ −2 ✓", "0 < 4 ✓", "<span class='ok'>Yes</span>"],
               [M("(1, 3)"), "3 ≥ −1 ✓", "3 < 3 ✗", "<span class='no'>No</span>: on the dashed line"],
               [M("(5, 0)"), "0 ≥ 3 ✗", "0 < −1 ✗", "<span class='no'>No</span>"]], "full tight")
        + '<div class="row">' + q + '<div class="col">'
        + box("In context: summer jobs", "<p>Tutor for $15 an hour (<i>x</i>) and mow for $10 an hour (<i>y</i>). "
              "Work <b>at most</b> 10 hours and earn <b>at least</b> $120.</p>"
              f"<p>{M('x + y ≤ 10')}<br>{M('15x + 10y ≥ 120')}<br>{M('x ≥ 0, y ≥ 0')}</p>", ORANGE)
        + box("Check (8, 1)", f"<p>{M('9 ≤ 10')} <span class='ok'>✓</span> and {M('130 ≥ 120')} <span class='ok'>✓</span></p>", GREEN)
        + "</div></div>"
        + '<p class="key">Hours can’t be negative, so only the first quadrant makes sense.</p>', PURPLE))
    assert len(P) == TOTAL
    return P


def check():
    """Every worked example on the charts is right."""
    ok = lambda eqs, x, y: all(a * x + b * y == k for a, b, k in eqs)
    assert ok([(-1, 1, 1), (2, 1, 4)], 1, 2)                     # y = x + 1, y = -2x + 4
    assert ok([(-1, 1, 0), (1, 1, 2)], 1, 1)                     # y = x, y = -x + 2
    assert all(4 * x - 2 * (2 * x - 1) == 2 for x in range(-5, 6))  # 4x - 2y = 2 is y = 2x - 1
    assert ok([(-2, 1, -1), (3, 1, 9)], 2, 3)                    # substitution example
    assert all(-6 * x + 2 * (3 * x + 2) == 4 for x in range(-5, 6)) and 4 != 10
    assert all(4 * x - 2 * (2 * x + 1) == -2 for x in range(-5, 6))
    assert 5 + 7 == 12 and 9 * 5 + 5 * 7 == 80                   # tickets
    assert ok([(2, 3, 12), (4, -3, 6)], 3, 2)                    # elimination
    assert ok([(1, 2, 7), (3, -1, 7)], 3, 2) and (3 * 2, -1 * 2, 7 * 2) == (6, -2, 14)
    assert 0 > 2 * 0 - 3                                          # y > 2x - 3 at (0, 0)
    assert 2 * 3 + 3 * 0 == 6 and 2 * 0 + 3 * 2 == 6 and 0 <= 6   # 2x + 3y <= 6
    sol = lambda x, y: y >= x - 2 and y < -x + 4
    assert sol(0, 0) and not sol(1, 3) and not sol(5, 0) and 3 == -1 + 4  # (1, 3) is on y = -x + 4
    assert 8 + 1 <= 10 and 15 * 8 + 10 * 1 == 130 >= 120


if __name__ == "__main__":
    check()
    OUT.mkdir(parents=True, exist_ok=True)
    name = "M3T2-Anchor-Charts"
    html = OUT / f"{name}.html"
    html.write_text(f'<!doctype html><meta charset="utf-8"><title>M3T2 Anchor Charts</title><style>{CSS}{EXTRA}</style><body>{"".join(charts())}</body>',
                    encoding="utf-8")
    pdf = OUT / f"{name}.pdf"
    subprocess.run([EDGE, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={pdf}", html.as_uri()],
                   check=True, capture_output=True)
    html.unlink()
    d = fitz.open(pdf)
    assert len(d) == TOTAL, f"{len(d)} pages: a chart overflowed"
    for i, page in enumerate(d):  # lesson = i // 2 + 1, chart = i % 2 + 1
        png = OUT / "tmp.png"
        page.get_pixmap(dpi=110).save(png)
        Image.open(png).convert("RGB").save(OUT / f"M3T2-L{i // 2 + 1}-Anchor-{i % 2 + 1}.jpg", quality=85, optimize=True)
        png.unlink()
    print("wrote", pdf, "and", TOTAL, "pictures")

"""Anchor charts for Module 3 Topic 1 (two per lesson, letter size), reusing the Topic 2 poster style.
Run: python make_m3t1_anchor_charts.py
 -> Module 3 topic 1/ANCHOR CHARTS/M3T1-Anchor-Charts.pdf  (print all six)
 -> Module 3 topic 1/ANCHOR CHARTS/M3T1-L{n}-Anchor-{k}.jpg  (one picture per chart, shown on the web pages)"""
import subprocess
from fractions import Fraction as F
from pathlib import Path

import fitz
from PIL import Image

from make_t2_posters import CSS, EDGE, M, box, c, fr, table, INK, BLUE, ORANGE, GREEN, PURPLE

ROOT = Path(__file__).parent
OUT = ROOT / "Module 3 topic 1" / "ANCHOR CHARTS"
RED = "#b4372b"
TOTAL = 6


def chart(n, lesson, title, formula, body, col=BLUE):
    return (f'<section class="page"><div class="top"><header style="background:{col}"><span>Module 3 · Topic 1 · {lesson}</span>'
            f'<span>Anchor chart {n} / {TOTAL}</span></header><h1>{title}</h1><div class="formula">{formula}</div></div>{body}'
            f'<footer>Bluebonnet Algebra I · Linear Equations and Inequalities · Mr. Pandey</footer></section>')


def steps(rows):  # worked example: (math, why) pairs
    return ('<table class="full work">' + "".join(f'<tr><td class="m">{M(m)}</td><td>{why}</td></tr>' for m, why in rows) + "</table>")


def numline(x, closed, right, col, lo=-6, hi=6, w=560):
    """Number line with the boundary at x, open/closed circle, and the shaded ray to the right or left."""
    s = w / (hi - lo + 1)
    X = lambda v: (v - lo + 0.5) * s
    g = [f'<svg viewBox="0 0 {w} 70" width="{w}" height="70"><defs><marker id="na{col[1:]}" viewBox="0 0 10 10" refX="5" refY="5" '
         f'markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{INK}"/></marker></defs>',
         f'<line x1="4" y1="28" x2="{w - 4}" y2="28" stroke="{INK}" stroke-width="2.5" marker-start="url(#na{col[1:]})" marker-end="url(#na{col[1:]})"/>']
    for k in range(lo, hi + 1):
        g.append(f'<line x1="{X(k)}" y1="21" x2="{X(k)}" y2="35" stroke="{INK}" stroke-width="2"/>'
                 f'<text x="{X(k)}" y="58" text-anchor="middle" font-size="17" font-family="Segoe UI">{str(k).replace("-", "−")}</text>')
    end = w - 10 if right else 10
    g.append(f'<line x1="{X(x)}" y1="28" x2="{end}" y2="28" stroke="{col}" stroke-width="8" stroke-linecap="round"/>')
    g.append(f'<circle cx="{X(x)}" cy="28" r="10" fill="{col if closed else "#fff"}" stroke="{col}" stroke-width="4"/>')
    return "".join(g) + "</svg>"


def charts():
    P = []
    # 1 · Lesson 1: steps to solve
    P.append(chart(1, "Lesson 1", "Solving Linear Equations", "Keep the equation balanced",
        '<ol class="steps big4">'
        "<li><b>Distribute</b> to clear parentheses. Watch the negative!</li>"
        "<li><b>Combine like terms</b> on each side.</li>"
        "<li><b>Variables to one side</b>: add or subtract a variable term.</li>"
        "<li><b>Undo + and −</b> to get the variable term alone.</li>"
        "<li><b>Undo × and ÷</b>. Whatever you do to one side, do to the other.</li>"
        "<li><b>Check</b>: substitute your answer into the original equation.</li></ol>"
        + box("Example", steps([
            ("3(x − 2) + 4 = 2x + 7", "Start"),
            ("3x − 6 + 4 = 2x + 7", "Distribute the 3"),
            ("3x − 2 = 2x + 7", "Combine like terms"),
            ("x − 2 = 7", "Subtract 2x from both sides"),
            (c("x = 9", GREEN), "Add 2 to both sides")]), BLUE)
        + f'<p class="key">Check: {M("3(9 − 2) + 4 = 25")} and {M("2(9) + 7 = 25")} <span class="ok">✓ same value</span></p>'))

    # 2 · Lesson 1: number of solutions
    P.append(chart(2, "Lesson 1", "One, None, or Infinite?", "How many solutions?",
        '<p class="lead">Solve until the variable is gone or alone. What is left tells you the answer.</p>'
        '<div class="grid2" style="grid-template-columns:1fr 1fr 1fr">'
        + box("One solution", f"<p>{M('4x + 1 = 2x + 9')}</p><p>{M('2x = 8')}</p><p class='ans'>{M('x = 4')}</p>"
              "<p>Different <i>x</i>-coefficients.</p>", GREEN)
        + box("No solution", f"<p>{M('2x + 3 = 2x + 5')}</p><p>{M('3 = 5')}</p><p class='ans' style='color:{RED}'>False ✗</p>"
              "<p>Same <i>x</i>-coefficients, different constants.</p>", RED)
        + box("Infinite solutions", f"<p>{M('2(x + 3) = 2x + 6')}</p><p>{M('6 = 6')}</p><p class='ans' style='color:{BLUE}'>Always true ✓</p>"
              "<p>Both sides are the same expression.</p>", BLUE) + "</div>"
        + table(["What you get", "Number of solutions", "Graph of each side"],
                [[M("x = a number"), "One", "Lines cross once"],
                 ["A false statement, like " + M("3 = 5"), "None", "Parallel lines"],
                 ["A true statement, like " + M("6 = 6"), "Infinitely many", "Same line"]], "full tight")
        + '<p class="key">Same <i>x</i>-coefficient on both sides? Compare the constants.</p>', PURPLE))

    # 3 · Lesson 2: solve for a letter
    P.append(chart(3, "Lesson 2", "Literal Equations", "Solve for one letter",
        '<p class="key">A <b>literal equation</b> has two or more variables, like a formula. To solve for one letter, '
        "treat every other letter as if it were a number and use the same steps.</p>"
        '<div class="grid2">'
        + box("Perimeter: solve for " + M("w"), steps([
            ("2l + 2w = P", "Start"),
            ("2w = P − 2l", "Subtract 2l"),
            (c("w = " + fr(M("P − 2l"), "2"), GREEN), "Divide by 2")]), BLUE)
        + box("Distance: solve for " + M("t"), steps([
            ("d = rt", "Start"),
            (fr(M("d"), M("r")) + " = " + M("t"), "Divide by r"),
            (c("t = " + fr(M("d"), M("r")), GREEN), "Rewrite")]), ORANGE) + "</div>"
        + box("Check with numbers", f"<p>{M('l = 5')}, {M('w = 3')} gives {M('P = 16')}. "
              f"Then {M('w = (16 − 10) ÷ 2 = 3')} <span class='ok'>✓</span></p>", GREEN), ORANGE))

    # 4 · Lesson 2: rewriting forms
    P.append(chart(4, "Lesson 2", "Rewrite Equations", "Divide EVERY term",
        '<div class="grid2">'
        + box("Standard form → slope-intercept form", steps([
            ("3x + 2y = 8", "Start"),
            ("2y = −3x + 8", "Subtract 3x"),
            ("y = " + fr("−3x", "2") + " + " + fr("8", "2"), "Divide <b>every</b> term by 2"),
            (c("y = −" + fr("3", "2") + "x + 4", GREEN), "Simplify")]), BLUE)
        + box("Temperature: solve for " + M("F"), steps([
            ("C = " + fr("5", "9") + "(F − 32)", "Start"),
            (fr("9", "5") + "C = F − 32", "Multiply by the reciprocal " + fr("9", "5")),
            (c("F = " + fr("9", "5") + "C + 32", GREEN), "Add 32")]), ORANGE) + "</div>"
        + '<div class="grid2">'
        + box("Undo in reverse order", "<p>Undo + and − first, then × and ÷. It is the order of operations, backward.</p>", PURPLE)
        + box("Watch out", f"<p><span class='no'>✗</span> {M('2y = −3x + 8')} → {M('y = −3x + 4')}</p>"
              "<p>Only one term was divided. Divide <b>every</b> term.</p>", RED) + "</div>", ORANGE))

    # 5 · Lesson 3: symbols and graphs
    P.append(chart(5, "Lesson 3", "Inequality Symbols", "Words → symbol → graph",
        table(["Symbol", "Say it", "Key words", "Circle"],
              [[M("<"), "less than", "fewer than, below", "open ○"],
               [M(">"), "greater than", "more than, above", "open ○"],
               [M("≤"), "less than or equal to", "<b>at most</b>, no more than, maximum", "closed ●"],
               [M("≥"), "greater than or equal to", "<b>at least</b>, no less than, minimum", "closed ●"]], "full")
        + '<div class="grid2">'
        + box(M("x < 2"), numline(2, False, False, BLUE, w=400) + "<p>Open circle: 2 is <b>not</b> a solution.</p>", BLUE)
        + box(M("x ≥ −3"), numline(-3, True, True, GREEN, w=400) + "<p>Closed circle: −3 <b>is</b> a solution.</p>", GREEN) + "</div>"
        + '<p class="key">Variable on the left? The symbol points the way the arrow goes: '
          + M("x < 2") + " shades left, " + M("x ≥ −3") + " shades right.</p>", GREEN))

    # 6 · Lesson 3: solving, flip the sign
    P.append(chart(6, "Lesson 3", "Solving Inequalities", "× or ÷ by a negative → FLIP",
        '<div class="grid2">'
        + box("Example", steps([
            ("−3x + 5 ≤ 17", "Start"),
            ("−3x ≤ 12", "Subtract 5"),
            (c("x ≥ −4", GREEN), "Divide by −3: <b>flip</b> ≤ to ≥")]) + numline(-4, True, True, GREEN, w=480), BLUE)
        + box("Why flip?", f"<p>{M('2 < 5')} is true.</p><p>Multiply both by −1:</p><p>{M('−2 ? −5')}</p>"
              f"<p>{M('−2 > −5')}, so the sign <b>flips</b>.</p>", RED) + "</div>"
        + box("Modeling: “at least” means ≥", f"<p>You earn $50 plus $8 for each shirt you sell. You need <b>at least</b> $250.</p>"
              f"<p class='big'>{M('50 + 8s ≥ 250')} → {M('8s ≥ 200')} → <span class='ok'>{M('s ≥ 25')}</span> shirts</p>", ORANGE)
        + f'<p class="key">Check a point from the shaded side: {M("x = 0")} gives {M("5 ≤ 17")} <span class="ok">✓ true</span></p>', GREEN))
    assert len(P) == TOTAL
    return P


def check():
    """The worked examples on the charts are right."""
    x = 9; assert 3 * (x - 2) + 4 == 2 * x + 7 == 25
    x = 4; assert 4 * x + 1 == 2 * x + 9
    assert all(2 * (x + 3) == 2 * x + 6 for x in range(-5, 6)) and all(2 * x + 3 != 2 * x + 5 for x in range(-5, 6))
    l, w = 5, 3; P = 2 * l + 2 * w; assert P == 16 and (P - 2 * l) / 2 == w
    for x in range(-4, 5):  # 3x + 2y = 8  <=>  y = -3/2 x + 4
        assert 3 * x + 2 * (F(-3, 2) * x + 4) == 8
    for Fh in (32, 212, 50):
        C = F(5, 9) * (Fh - 32); assert F(9, 5) * C + 32 == Fh
    for x in range(-10, 11):  # -3x + 5 <= 17  <=>  x >= -4
        assert (-3 * x + 5 <= 17) == (x >= -4)
    for s in range(0, 50):
        assert (50 + 8 * s >= 250) == (s >= 25)


EXTRA = """.work td{text-align:left;font-size:24px;padding:6px 14px} .work td.m{white-space:nowrap;font-size:27px}
.box .work{margin:4px 0} .box svg{display:block;margin:8px auto 2px;max-width:100%;height:auto}
.fr{display:inline-flex;flex-direction:column;vertical-align:middle;text-align:center;font-size:.78em;line-height:1.15;margin:0 2px}
.fr>span:first-child{border-bottom:2px solid currentColor;padding:0 3px}
table.tight td{padding:7px 12px;font-size:23px}"""

if __name__ == "__main__":
    check()
    OUT.mkdir(parents=True, exist_ok=True)
    name = "M3T1-Anchor-Charts"
    html = OUT / f"{name}.html"
    html.write_text(f'<!doctype html><meta charset="utf-8"><title>M3T1 Anchor Charts</title><style>{CSS}{EXTRA}</style><body>{"".join(charts())}</body>',
                    encoding="utf-8")
    pdf = OUT / f"{name}.pdf"
    subprocess.run([EDGE, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={pdf}", html.as_uri()],
                   check=True, capture_output=True)
    html.unlink()
    d = fitz.open(pdf)
    assert len(d) == TOTAL, f"{len(d)} pages: a chart overflowed"
    for i, page in enumerate(d):  # web pictures: lesson = i // 2 + 1, chart = i % 2 + 1
        png = OUT / "tmp.png"
        page.get_pixmap(dpi=110).save(png)
        Image.open(png).convert("RGB").save(OUT / f"M3T1-L{i // 2 + 1}-Anchor-{i % 2 + 1}.jpg", quality=85, optimize=True)
        png.unlink()
    print("wrote", pdf, "and", TOTAL, "pictures")

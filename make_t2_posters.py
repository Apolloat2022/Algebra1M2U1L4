"""Ten one-page classroom posters for Module 2 Topic 2, Lessons 1-3 (letter size, printed to PDF with Edge).
Run: python make_t2_posters.py  ->  Module 2 topic 2/Topic2-Lessons1-3-Posters.{html,pdf}"""
import math
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "Module 2 topic 2" / "Topic2-Lessons1-3-Posters"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
INK, BLUE, ORANGE, GREEN, PURPLE, GRID = "#16171d", "#3050b8", "#c9561f", "#4f8a3c", "#7a4fc4", "#d5d8e4"


def M(s):  # math text: every letter is an italic variable
    out, tag = [], False
    for ch in s:
        tag = tag or ch == "<"
        out.append(f"<i>{ch}</i>" if ch.isalpha() and ch.isascii() and not tag else ch)
        tag = tag and ch != ">"
    return f'<span class="m">{"".join(out)}</span>'


def c(s, color):
    return f'<span style="color:{color}">{s}</span>'


def fr(n, d):  # stacked fraction
    return f'<span class="fr"><span>{n}</span><span>{d}</span></span>'


def graph(lines=(), pts=(), lo=-6, hi=6, size=430, marks=""):
    """lines: (m, b, color, label, label_x[, dash]) for y = mx + b, or ("x", k, color, label, label_y) for x = k.
    pts: (x, y, label, color, dx, dy). Equal scales, so right angles look right."""
    s = size / (hi - lo)
    X, Y = (lambda x: (x - lo) * s), (lambda y: (hi - y) * s)
    g = [f'<svg class="g" viewBox="-14 -14 {size + 28} {size + 28}" width="{size + 28}" height="{size + 28}">',
         f'<defs><clipPath id="c{id(lines)}"><rect width="{size}" height="{size}"/></clipPath></defs>']
    for k in range(lo, hi + 1):
        g.append(f'<line x1="{X(k)}" y1="0" x2="{X(k)}" y2="{size}" stroke="{GRID}"/><line x1="0" y1="{Y(k)}" x2="{size}" y2="{Y(k)}" stroke="{GRID}"/>')
    g.append(f'<line x1="{X(0)}" y1="0" x2="{X(0)}" y2="{size}" stroke="{INK}" stroke-width="2"/>'
             f'<line x1="0" y1="{Y(0)}" x2="{size}" y2="{Y(0)}" stroke="{INK}" stroke-width="2"/>')
    for k in range(lo, hi + 1):
        if k and k % 2 == 0:
            g.append(f'<text x="{X(k)}" y="{Y(0) + 18}" class="t" text-anchor="middle">{k}</text>'
                     f'<text x="{X(0) - 6}" y="{Y(k) + 5}" class="t" text-anchor="end">{k}</text>')
    g.append(f'<text x="{size - 4}" y="{Y(0) - 8}" class="v" text-anchor="end">x</text><text x="{X(0) + 8}" y="16" class="v">y</text>')
    g.append(f'<g clip-path="url(#c{id(lines)})">')
    labels = []
    for ln in lines:
        if ln[0] == "x":
            _, k, col, lab, ly = ln
            g.append(f'<line x1="{X(k)}" y1="0" x2="{X(k)}" y2="{size}" stroke="{col}" stroke-width="4"/>')
            labels.append((X(k) + 8, Y(ly), lab, col, "start"))
            continue
        m, b, col, lab, lx, *dash = ln
        g.append(f'<line x1="{X(lo - 1)}" y1="{Y(m * (lo - 1) + b)}" x2="{X(hi + 1)}" y2="{Y(m * (hi + 1) + b)}" stroke="{col}" stroke-width="4"'
                 + (' stroke-dasharray="10 8"' if dash else "") + "/>")
        if lab:
            labels.append((X(lx) + 10, Y(m * lx + b) + (16 if m < 0 else -10 if m == 0 else 6), lab, col, "start"))
    g.append(marks.format(X=X, Y=Y) if marks else "")
    g.append("</g>")
    for x, y, lab, col, dx, dy in pts:
        g.append(f'<circle cx="{X(x)}" cy="{Y(y)}" r="7" fill="{col}" stroke="#fff" stroke-width="2"/>')
        if lab:
            labels.append((X(x) + dx, Y(y) + dy, lab, col, "start"))
    for x, y, lab, col, anchor in labels:
        g.append(f'<text x="{x}" y="{y}" class="l" fill="{col}" text-anchor="{anchor}">{lab}</text>')
    return "".join(g) + "</svg>"


def right_angle(x, y, m, lo=-6, hi=6, size=430, r=0.6):
    """Square corner where y = mx + ... meets its perpendicular at (x, y)."""
    s = size / (hi - lo)
    n = math.hypot(1, m)
    u, v = (1 / n, m / n), (-m / n, 1 / n)
    P = lambda a, b: f"{(x + a - lo) * s:.1f},{(hi - y - b) * s:.1f}"
    return (f'<polyline points="{P(r * u[0], r * u[1])} {P(r * (u[0] + v[0]), r * (u[1] + v[1]))} {P(r * v[0], r * v[1])}" '
            f'fill="none" stroke="{INK}" stroke-width="2.5"/>')


def arrow(x1, y1, x2, y2, col, lo=-6, hi=6, size=430):
    s = size / (hi - lo)
    return (f'<line x1="{(x1 - lo) * s}" y1="{(hi - y1) * s}" x2="{(x2 - lo) * s}" y2="{(hi - y2) * s}" stroke="{col}" '
            f'stroke-width="4" marker-end="url(#ah)"/>')


def table(head, rows):
    return ('<table><tr>' + "".join(f"<th>{h}</th>" for h in head) + "</tr>"
            + "".join("<tr>" + "".join(f"<td>{v}</td>" for v in r) + "</tr>" for r in rows) + "</table>")


def box(title, body, col=BLUE, cls=""):
    return f'<div class="box {cls}" style="border-color:{col}"><h3 style="color:{col}">{title}</h3>{body}</div>'


def poster(n, lesson, title, formula, body, col=BLUE):
    return (f'<section class="page"><div class="top"><header style="background:{col}"><span>Module 2 · Topic 2 · {lesson}</span><span>{n} / 10</span></header>'
            f'<h1>{title}</h1><div class="formula">{formula}</div></div>{body}'
            f'<footer>Bluebonnet Algebra I · Transforming Linear Functions</footer></section>')


ARROW = f'<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0 0L10 5L0 10z" fill="{INK}"/></marker></defs>'


def posters():
    P = []
    # 1 · Parent function
    P.append(poster(1, "Lesson 1", "The Parent Function", M("f(x) = x"),
        '<div class="row">' + graph([(1, 0, INK, "f(x) = x", 3.2)], [(k, k, "", BLUE, 0, 0) for k in range(-2, 3)])
        + '<div class="col">' + table([M("x"), M("f(x)")], [[M(str(k).replace("-", "−"))] * 2 for k in range(-2, 3)])
        + "<p>Every output equals its input.</p></div></div>"
        + '<div class="grid2" style="grid-template-columns:1fr 1fr 1fr">' + box("Slope", f"<p class='big'>{M('m = 1')}</p><p>Up 1, right 1</p>")
        + box("y-intercept", f"<p class='big'>{M('(0, 0)')}</p><p>Passes through the origin</p>")
        + box("Domain, range", "<p class='big'>All reals</p>", GREEN) + "</div>"
        + f'<p class="key">A <b>parent function</b> is the simplest function in its family. Every line is a transformation of it.</p>'))

    # 2 · Vertical translation
    P.append(poster(2, "Lesson 1", "Vertical Translation", M(f"y = f(x) + {c('d', BLUE)}"),
        '<div class="row">' + graph([(1, 4, BLUE, "x + 4", -5.6), (1, 0, INK, "f(x) = x", 2.4), (1, -4, PURPLE, "x − 4", 1.6)],
                                    [(0, 4, "(0, 4)", BLUE, 10, -8), (0, -4, "(0, −4)", PURPLE, 10, 22)],
                                    marks=ARROW + arrow(-2, -2, -2, 1.6, INK) + arrow(3, 3, 3, -0.6, INK))
        + '<div class="col">' + box(M('d > 0'), f"<p>Moves <b>up</b>.<br>{M('f(x) + 4')}: every point up 4.</p>", BLUE)
        + box(M('d < 0'), f"<p>Moves <b>down</b>.<br>{M('f(x) − 4')}: every point down 4.</p>", PURPLE) + "</div></div>"
        + '<div class="grid2">' + box("What changes", "<p>The <b>outputs</b> (<i>y</i>-values) and the <b><i>y</i>-intercept</b>, which moves to " + M("(0, d)") + ".</p>", ORANGE)
        + box("What stays", "<p>The <b>slope</b>. A line and its vertical translation are <b>parallel</b>: they never meet.</p>", GREEN) + "</div>"
        + f'<p class="key">Example: {M("j(x) = 2x − 1")} up 4 → {M("j(x) + 4 = 2x + 3")}</p>'))

    # 3 · Vertical dilation
    P.append(poster(3, "Lesson 1", "Vertical Dilation", M(f"y = {c('a', ORANGE)} · f(x)"),
        '<div class="row">' + graph([(3, 0, ORANGE, "3x", 1.75), (1, 0, INK, "f(x) = x", 3.2), (1 / 3, 0, GREEN, "⅓x", 3.5), (-2, 0, PURPLE, "−2x", -2.9)])
        + '<div class="col">' + box(M('|a| > 1'), f"<p><b>Stretch</b>: steeper.<br>{M('3 · f(x) = 3x')}</p>", ORANGE)
        + box(M('0 < |a| < 1'), f"<p><b>Compress</b>: flatter.<br>{M('⅓ · f(x) = ⅓x')}</p>", GREEN)
        + box(M('a < 0'), f"<p><b>Reflect</b> across the <i>x</i>-axis.<br>{M('−2 · f(x) = −2x')}</p>", PURPLE) + "</div></div>"
        + '<div class="grid2">' + box("What changes", f"<p>Every <b>output</b> is multiplied by {M('a')}. For {M('f(x) = x')}, the slope becomes {M('a')}.</p>", ORANGE)
        + box("What stays", f"<p>The origin {M('(0, 0)')} doesn't move: {M('a · 0 = 0')}.</p>", GREEN) + "</div>"
        + f'<p class="key">Example: {M("(2, 5)")} is on {M("f(x)")}, so {M("(2, −10)")} is on {M("−2 · f(x)")}.</p>', ORANGE))

    # 4 · Graphing a · f(x) + d
    P.append(poster(4, "Lesson 1", "Graph Any Transformation", M(f"g(x) = {c('a', ORANGE)} · f(x) + {c('d', BLUE)}"),
        '<div class="grid2 tight">' + box(c(M("a"), ORANGE) + " = slope", "<p>Stretch, compress or reflect</p>", ORANGE)
        + box(c(M("d"), BLUE) + " = <i>y</i>-intercept", f"<p>Up or down; line crosses at {M('(0, d)')}</p>", BLUE) + "</div>"
        + '<div class="row">' + graph([(1, 0, "#8a8fa3", "f(x)", -4.6, 1), (2, -3, ORANGE, "g(x) = 2x − 3", 3.6)],
                                      [(0, -3, "start (0, −3)", BLUE, 12, 6), (1, -1, "", ORANGE, 0, 0), (2, 1, "", ORANGE, 0, 0)])
        + f'<div class="col"><p class="lead">Example: {M("g(x) = 2 · f(x) − 3")}</p><ol class="steps">'
          f'<li><b>Describe it:</b> stretch by 2, then down 3.</li><li><b>Start</b> at the <i>y</i>-intercept {M("(0, −3)")}.</li>'
          f'<li><b>Use the slope</b> 2: up 2, right 1. Repeat.</li><li><b>Draw</b> the line through the points.</li></ol></div></div>'
        + table(["Function", "Describe it"], [[M("3f(x) − 1"), "Stretch by 3, down 1"],                                             [M("−f(x) − 4"), "Reflect across the <i>x</i>-axis, down 4"]])))

    # 5 · Horizontal translation
    P.append(poster(5, "Lesson 2", "Horizontal Translation", M(f"y = f(x − {c('c', BLUE)})"),
        '<p class="warn">Inside the parentheses, the sign flips!</p><div class="row">'
        + graph([(2, -1, INK, "j(x) = 2x − 1", 2.4), (2, -5, BLUE, "j(x − 2)", 3.4)],
                [(0, -1, "", INK, 0, 0), (2, -1, "", BLUE, 0, 0)], marks=ARROW + arrow(0.2, -1, 1.7, -1, INK))
        + '<div class="col">' + box(M('f(x − 3)'), "<p>Moves <b>right</b> 3.<br>Minus inside → right.</p>", BLUE)
        + box(M('f(x + 3)'), "<p>Moves <b>left</b> 3.<br>Plus inside → left.</p>", PURPLE) + "</div></div>"
        + '<div class="grid2">' + box("What changes", "<p>The <b>inputs</b> (<i>x</i>-values). Every point slides left or right.</p>", ORANGE)
        + box("What stays", "<p>The slope. The new line is <b>parallel</b> to the original.</p>", GREEN) + "</div>"
        + f'<p class="key">Example: {M("j(x) = 2x − 1")} right 2 → {M("j(x − 2) = 2(x − 2) − 1 = 2x − 5")}</p>'))

    # 6 · Horizontal dilation
    P.append(poster(6, "Lesson 2", "Horizontal Dilation", M(f"y = f({c('b', ORANGE)}x)"),
        '<p class="warn">Inside works backwards: a big <i>b</i> squeezes the graph.</p><div class="row">'
        + graph([(1, -2, INK, "f(x) = x − 2", 3.1), (2, -2, ORANGE, "f(2x)", 2.6), (0.5, -2, GREEN, "f(½x)", -5.4)],
                [(2, 0, "", INK, 0, 0), (1, 0, "", ORANGE, 0, 0), (4, 0, "", GREEN, 0, 0), (0, -2, "(0, −2) stays", BLUE, 10, 24)])
        + '<div class="col">' + box(M('|b| > 1'), "<p><b>Compress</b>: points move toward the <i>y</i>-axis.</p>", ORANGE)
        + box(M('0 < |b| < 1'), "<p><b>Stretch</b>: points move away from the <i>y</i>-axis.</p>", GREEN)
        + box(M('b < 0'), "<p><b>Reflect</b> across the <i>y</i>-axis.</p>", PURPLE) + "</div></div>"
        + '<div class="grid2">' + box("What changes", f"<p>The <b>inputs</b> are multiplied by {M('b')}. The <i>x</i>-intercept moves: 2 → 1 → 4.</p>", ORANGE)
        + box("What stays", "<p>The <i>y</i>-intercept: points on the <i>y</i>-axis have " + M("x = 0") + ".</p>", GREEN) + "</div>"
        + f'<p class="key">Example: {M("f(x) = x − 2")} → {M("f(2x) = 2x − 2")}</p>', ORANGE))

    # 7 · Inside vs. outside
    P.append(poster(7, "Lesson 2", "Inside vs. Outside",
        M(f"y = {c('a', ORANGE)} · f({c('b', ORANGE)}(x − {c('c', BLUE)})) + {c('d', BLUE)}"),
        '<div class="grid2 tall">'
        + box("Outside: <i>a</i> and <i>d</i>", "<p class='lead'>Change the <b>outputs</b> → <b>vertical</b></p><ul>"
              f"<li>{M('+ d')}: up {M('d')}</li><li>{M('− d')}: down {M('d')}</li><li>{M('a')}: vertical stretch or compress</li>"
              f"<li>{M('a < 0')}: reflect across the <i>x</i>-axis</li></ul><p class='ok'>Does what it says.</p>", BLUE)
        + box("Inside: <i>b</i> and <i>c</i>", "<p class='lead'>Change the <b>inputs</b> → <b>horizontal</b></p><ul>"
              f"<li>{M('x − c')}: right {M('c')}</li><li>{M('x + c')}: left {M('c')}</li><li>{M('b')}: horizontal compress or stretch</li>"
              f"<li>{M('b < 0')}: reflect across the <i>y</i>-axis</li></ul><p class='no'>Does the opposite.</p>", ORANGE) + "</div>"
        + box(f"Only for {M('f(x) = x')}!", f"<p>Right {M('n')} gives the same line as down {M('n')}, and {M('n · f(x)')} matches {M('f(nx)')}.</p>"
              f"<p>For other lines they are <b>not</b> the same. {M('j(x) = 2x − 1')}:</p>"
              f"<p class='big'>up 4: {M('2x + 3')} &nbsp; but &nbsp; left 4: {M('2x + 7')}</p>", PURPLE, "wide")
        + f'<p class="key">Example: {M("g(x) = −2 · f(x − 3) + 1")}<br>right 3 · stretch by 2 · reflect across the <i>x</i>-axis · up 1</p>', PURPLE))

    # 8 · Perpendicular slopes
    PM = right_angle(0, 0, 2 / 3)
    P.append(poster(8, "Lesson 3", "Perpendicular Lines", M(f"{c('m₁', ORANGE)} · {c('m₂', ORANGE)} = −1"),
        '<p class="warn">Flip the fraction. Change the sign.</p><div class="row">'
        + graph([(2 / 3, 0, ORANGE, "y = ⅔x", 3.5), (-1.5, 0, BLUE, "y = −3/2 x", -3.6)], [], marks=PM)
        + '<div class="col">' + table(["Slope", "⊥ slope"], [[M("⅔"), M("−3/2")], [M("2"), M("−½")], [M("−¾"), M("4/3")], [M("−5"), M("⅕")], [M("1"), M("−1")]])
        + "</div></div>"
        + '<div class="grid2">' + box("Perpendicular ⊥", "<p>Meet at a <b>right angle</b>. Slopes are <b>negative reciprocals</b>: " + M("⅔ · (−3/2) = −1") + ".</p>", ORANGE)
        + box("Parallel ∥", "<p>Never meet. Slopes are the <b>same</b>: " + M("y = 2x + 1") + " ∥ " + M("y = 2x − 5") + ".</p>", BLUE) + "</div>"
        + f'<p class="key">Why? A 90° turn maps {M("(x, y)")} to {M("(−y, x)")}, so slope {M("b/a")} becomes {M("−a/b")}.</p>', ORANGE))

    # 9 · Horizontal and vertical lines
    P.append(poster(9, "Lesson 3", "Horizontal and Vertical Lines", "HOY &nbsp;·&nbsp; VUX",
        '<div class="row">' + graph([(0, 3, BLUE, "y = 3", 3.2), ("x", -2, ORANGE, "x = −2", -5)], [(-2, 3, "(−2, 3)", INK, -86, 30)],
                                    marks=right_angle(-2, 3, 0))
        + '<div class="col">' + box("H · O · Y", "<p class='big'><b>H</b>orizontal</p><p>slope <b>0</b> (zero)</p>"
                                    f"<p class='big'>{M('y = k')}</p>", BLUE)
        + box("V · U · X", "<p class='big'><b>V</b>ertical</p><p>slope <b>U</b>ndefined</p>"
              f"<p class='big'>{M('x = h')}</p>", ORANGE) + "</div></div>"
        + '<div class="grid2">' + box("Why?", f"<p>Horizontal: <i>y</i> never changes, so slope {M('= 0 ÷ run = 0')}.<br>"
                                      f"Vertical: <i>x</i> never changes, so slope {M('= rise ÷ 0')}: undefined.</p>", GREEN)
        + box("Always", "<p>All horizontal lines are parallel. All vertical lines are parallel. A horizontal and a vertical line are <b>always perpendicular</b>.</p>", PURPLE) + "</div>"
        + f'<p class="key">Through {M("(2, −1)")}: horizontal {M("y = −1")}, vertical {M("x = 2")}</p>'))

    # 10 · Writing parallel and perpendicular lines
    P.append(poster(10, "Lessons 1 & 3", "Write a Parallel or Perpendicular Line", M("y − y₁ = m(x − x₁)"),
        '<ol class="steps big4"><li>Find the <b>slope</b> of the given line.</li>'
        '<li><b>Parallel:</b> use the same slope. <b>Perpendicular:</b> flip it and change the sign.</li>'
        f'<li><b>Plug in</b> the point: {M("y − y₁ = m(x − x₁)")} or {M("y = mx + b")}.</li><li><b>Solve</b> for <i>y</i>.</li></ol>'
        '<div class="grid2 tall">'
        + box(f"∥ to {M('y = −3x − 1')} through {M('(−1, 5)')}",
              f"<p>Same slope: {M('m = −3')}</p><p>{M('5 = −3(−1) + b')}</p><p>{M('5 = 3 + b')}, so {M('b = 2')}</p><p class='ans'>{M('y = −3x + 2')}</p>", BLUE)
        + box(f"⊥ to {M('y = 2x + 1')} through {M('(6, 2)')}",
              f"<p>Flip and change: {M('m = −½')}</p><p>{M('y − 2 = −½(x − 6)')}</p><p>{M('y − 2 = −½x + 3')}</p><p class='ans'>{M('y = −½x + 5')}</p>", ORANGE)
        + "</div>" + '<p class="key">Check: put the point into your answer. It must make the equation true.</p>', GREEN))
    return P


CSS = f"""@page{{size:letter;margin:0}}
*{{box-sizing:border-box}} body{{margin:0;font-family:"Segoe UI",system-ui,sans-serif;color:{INK};-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.top{{display:flex;flex-direction:column;gap:12px}}
.page{{width:8.5in;height:11in;padding:0 .55in .75in;display:flex;flex-direction:column;justify-content:space-between;gap:14px;overflow:hidden;page-break-after:always;position:relative}}
header{{margin:0 -.55in;padding:12px .55in;color:#fff;font-size:17px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;display:flex;justify-content:space-between}}
h1{{font-size:52px;line-height:1.05;margin:6px 0 0;letter-spacing:-.02em}}
.formula{{font-size:42px;font-weight:600;padding:8px 18px;border:3px solid {INK};border-radius:14px;align-self:flex-start;background:#f4f5fa}}
.m{{font-family:"Cambria Math","Cambria","Times New Roman",serif;white-space:nowrap}}
.row{{display:flex;gap:22px;align-items:center}} .col{{display:flex;flex-direction:column;gap:12px;flex:1}}
.grid2{{display:grid;grid-template-columns:1fr 1fr;gap:14px}} .grid2.tall .box{{padding:16px 20px}}
.box{{border:3px solid;border-radius:12px;padding:10px 16px;font-size:21px;line-height:1.35}} .box.wide{{font-size:22px}}
.box h3{{margin:0 0 4px;font-size:27px}} .box p{{margin:2px 0}} .box ul{{margin:6px 0;padding-left:24px;font-size:23px;line-height:1.5}}
.big{{font-size:25px}} .lead{{font-size:22px;margin:0}} .ans{{font-size:28px;font-weight:700;color:{GREEN};margin-top:6px!important}}
.ok{{color:{GREEN};font-weight:700}} .no{{color:#b4372b;font-weight:700}}
.key{{font-size:24px;margin:0;padding:12px 18px;background:#eef0f8;border-left:8px solid {INK};border-radius:6px}}
.warn{{font-size:26px;font-weight:700;margin:0;color:#b4372b}}
table{{border-collapse:collapse;font-size:26px;align-self:center}} th,td{{border:2px solid {INK};padding:6px 20px;text-align:center}} th{{background:#eef0f8;white-space:nowrap}}
.steps{{margin:0;padding-left:30px;font-size:23px;line-height:1.45}} .steps li{{margin:4px 0}} .big4{{font-size:26px}}
.g{{flex:none}} .g .t{{font:15px "Segoe UI",sans-serif;fill:#5f6272}} .g .v{{font:italic 22px Cambria,serif}}
.g .l{{font:italic 700 22px Cambria,serif;paint-order:stroke;stroke:#fff;stroke-width:5px}}
footer{{position:absolute;bottom:.25in;left:.55in;right:.55in;font-size:13px;color:#5f6272;border-top:1px solid #ccc;padding-top:6px}}"""

if __name__ == "__main__":
    pages = posters()
    assert len(pages) == 10
    html = OUT.with_suffix(".html")
    html.write_text(f'<!doctype html><meta charset="utf-8"><title>Topic 2 Lessons 1–3 Posters</title><style>{CSS}</style><body>{"".join(pages)}</body>',
                    encoding="utf-8")
    subprocess.run([EDGE, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={OUT.with_suffix('.pdf')}", html.as_uri()],
                   check=True, capture_output=True)
    print("wrote", OUT.with_suffix(".pdf"))

# Algebra I Game Plan: Topic Tests and STAAR — a workbook (General + IEP, each with an answer key).
# One chapter per topic. Each chapter: vocabulary, key ideas + worked examples per lesson (starred activities in
# materials/Pacing Guides/...150-day...pdf), practice, a Skill Check (skill-based: every tested skill, shuffled, in several
# representations, more items than the test — never test twins), and a STAAR Corner
# (STAAR formats; TEKS weighted by materials/STAAR answer keys 2018-2026).
# Add a module: write chapters in the same shape and append to BOOK.   Run: python make_game_plan.py
import random
import subprocess
from fractions import Fraction as Fr
from math import exp, log
from statistics import correlation, linear_regression
from pathlib import Path

from make_t2_review_test import EDGE, fr

ROOT = Path(__file__).parent
OUT = ROOT / "Game Plan"
TITLE = "Algebra I Game Plan: Topic Tests and STAAR"
KEY = IEP = False  # flipped per build

i = lambda s: f"<i>{s}</i>"
x, y, n = i("x"), i("y"), i("n")
sub = lambda a, k: f"<i>{a}</i><sub>{k}</sub>"
LE, GE = "≤", "≥"


# ---------- figures ----------
def plot(xr, yr, curves=(), pts=(), xlab="", ylab="", size=230):
    """xr/yr = (lo, hi, grid step, label step). curves: dict(f=fn or xy=[...], a, b, ends=(start, end))
    where an end is 'arrow' | 'open' | 'closed' | None. pts: (x, y) dots."""
    (x0, x1, xs, xl), (y0, y1, ys, yl) = xr, yr
    sx, sy = size / (x1 - x0), size / (y1 - y0)
    X, Y = (lambda v: (v - x0) * sx), (lambda v: (y1 - v) * sy)
    ax, ay = (0 if x0 <= 0 <= x1 else x0), (0 if y0 <= 0 <= y1 else y0)
    padl = 40 if ylab else 26
    o = [f'<svg class="g" viewBox="{-padl} -16 {size + padl + 24} {size + (46 if xlab else 34)}" width="{size + padl + 24}">'
         '<defs><marker id="ar" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="7" markerHeight="7" '
         'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z"/></marker></defs>']
    k = x0
    while k <= x1 + 1e-9:
        o.append(f'<line x1="{X(k)}" y1="0" x2="{X(k)}" y2="{size}" stroke="#bbb" stroke-width="0.6"/>')
        if abs(round(k / xl) * xl - k) < 1e-9 and abs(k - ax) > 1e-9:
            o.append(f'<text x="{X(k)}" y="{Y(ay) + 13}" font-size="10" text-anchor="middle">{k:g}</text>')
        k += xs
    k = y0
    while k <= y1 + 1e-9:
        o.append(f'<line x1="0" y1="{Y(k)}" x2="{size}" y2="{Y(k)}" stroke="#bbb" stroke-width="0.6"/>')
        if abs(round(k / yl) * yl - k) < 1e-9 and abs(k - ay) > 1e-9:
            o.append(f'<text x="{X(ax) - 4}" y="{Y(k) + 3.5}" font-size="10" text-anchor="end">{k:g}</text>')
        k += ys
    o.append(f'<line x1="0" y1="{Y(ay)}" x2="{size}" y2="{Y(ay)}" stroke="#000" stroke-width="1.4"/>'
             f'<line x1="{X(ax)}" y1="0" x2="{X(ax)}" y2="{size}" stroke="#000" stroke-width="1.4"/>'
             f'<text x="{X(ax) - 4}" y="{Y(ay) + 13}" font-size="10" text-anchor="end">0</text>'
             f'<text x="{size + 6}" y="{Y(ay) + 4}" font-size="12" font-style="italic">x</text>'
             f'<text x="{X(ax) + 4}" y="-5" font-size="12" font-style="italic">y</text>')
    if xlab:
        o.append(f'<text x="{size / 2}" y="{size + 28}" font-size="11" font-weight="bold" text-anchor="middle">{xlab}</text>')
    if ylab:
        o.append(f'<text transform="translate({-30},{size / 2}) rotate(-90)" font-size="11" font-weight="bold" '
                 f'text-anchor="middle">{ylab}</text>')
    global CLIP
    CLIP += 1
    o.append(f'<clipPath id="w{CLIP}"><rect x="0" y="0" width="{size}" height="{size}"/></clipPath>')
    for c in [c for c in curves if "shade" in c]:  # inequality: dashed/solid boundary + shaded half-plane
        f, far = c["f"], (y1 + 1000 if c["shade"] == "above" else y0 - 1000)
        col = c.get("color", "#2f6fdd")
        o.append(f'<g clip-path="url(#w{CLIP})"><polygon fill="{col}" fill-opacity="0.18" points="'
                 f'{X(x0)},{Y(f(x0))} {X(x1)},{Y(f(x1))} {X(x1)},{Y(far)} {X(x0)},{Y(far)}"/>'
                 f'<line x1="{X(x0)}" y1="{Y(f(x0))}" x2="{X(x1)}" y2="{Y(f(x1))}" stroke="{c.get("line", "#000")}" '
                 f'stroke-width="2.2"{" stroke-dasharray=\"7 5\"" if c.get("dash") else ""}/></g>')
    curves = [c for c in curves if "shade" not in c]
    for c in curves:
        if "xy" in c:
            p = c["xy"]
        else:
            a, b = c["a"], c["b"]
            p = [(a + (b - a) * t / 160, c["f"](a + (b - a) * t / 160)) for t in range(161)]
            p = [(u, v) for u, v in p if y0 - 1e-9 <= v <= y1 + 1e-9]
        s, e = c.get("ends", ("arrow", "arrow"))
        ms = ' marker-start="url(#ar)"' if s == "arrow" else ""
        me = ' marker-end="url(#ar)"' if e == "arrow" else ""
        col = c.get("color", "#000")
        dash = ' stroke-dasharray="7 5"' if c.get("dash") else ""
        o.append(f'<polyline fill="none" stroke="{col}" stroke-width="2.2"{dash}{ms}{me} points="'
                 + " ".join(f"{X(u):.1f},{Y(v):.1f}" for u, v in p) + '"/>')
        if c.get("label"):
            u, v = p[-1]
            o.append(f'<text x="{X(u) - 6}" y="{Y(v) + 16}" font-size="12" font-style="italic" fill="{col}" '
                     f'text-anchor="end">{c["label"]}</text>')
        for kind, (u, v) in ((s, p[0]), (e, p[-1])):
            if kind in ("open", "closed"):
                o.append(f'<circle cx="{X(u)}" cy="{Y(v)}" r="4" fill="{"#fff" if kind == "open" else "#000"}" '
                         'stroke="#000" stroke-width="1.6"/>')
    for u, v, *lab in pts:  # (x, y) or (x, y, "label")
        o.append(f'<circle cx="{X(u)}" cy="{Y(v)}" r="4.2" fill="#000"/>')
        if lab:
            o.append(f'<text x="{X(u) + 6}" y="{Y(v) - 7}" font-size="11" font-weight="bold">{lab[0]}</text>')
    return "".join(o) + "</svg>"


CLIP = 0


def numline(lo, hi, pt=None, closed=True, left=True, color="#000"):
    """Number line from lo to hi; optional solution ray: dot at pt (closed/open), arrow left or right."""
    W, u = 420, 420 / (hi - lo + 2)
    X = lambda v: (v - lo + 1) * u
    o = [f'<svg class="g" viewBox="0 0 {W} 52" width="{W}"><defs><marker id="nl" viewBox="0 0 10 10" refX="5" refY="5" '
         'markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z"/></marker></defs>'
         f'<line x1="2" y1="22" x2="{W - 2}" y2="22" stroke="#000" stroke-width="1.4" marker-start="url(#nl)" marker-end="url(#nl)"/>']
    for v in range(lo, hi + 1):
        o.append(f'<line x1="{X(v)}" y1="16" x2="{X(v)}" y2="28" stroke="#000" stroke-width="1"/>'
                 f'<text x="{X(v)}" y="44" font-size="11" text-anchor="middle">{str(v).replace("-", "−")}</text>')
    if pt is not None:
        end = 6 if left else W - 6
        o.append(f'<line x1="{X(pt)}" y1="22" x2="{end}" y2="22" stroke="{color}" stroke-width="4.5"/>'
                 f'<circle cx="{X(pt)}" cy="22" r="6" fill="{color if closed else "#fff"}" stroke="{color}" stroke-width="2.4"/>')
    return "".join(o) + "</svg>"


def mapping(dom, rng, pairs):
    h = 40 + 34 * max(len(dom), len(rng))
    o = [f'<svg class="g" viewBox="0 0 250 {h + 22}" width="250">'
         '<defs><marker id="mp" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
         '<path d="M0,0 L10,5 L0,10 z"/></marker></defs>'
         f'<ellipse cx="50" cy="{h / 2}" rx="36" ry="{h / 2 - 4}" fill="none" stroke="#000" stroke-width="1.5"/>'
         f'<ellipse cx="200" cy="{h / 2}" rx="36" ry="{h / 2 - 4}" fill="none" stroke="#000" stroke-width="1.5"/>'
         f'<text x="50" y="{h + 16}" font-size="12" text-anchor="middle">Domain</text>'
         f'<text x="200" y="{h + 16}" font-size="12" text-anchor="middle">Range</text>']
    yd = {d: h / 2 + (k - (len(dom) - 1) / 2) * 34 for k, d in enumerate(dom)}
    yr = {r: h / 2 + (k - (len(rng) - 1) / 2) * 34 for k, r in enumerate(rng)}
    for d in dom:
        o.append(f'<text x="50" y="{yd[d] + 5}" font-size="14" text-anchor="middle">{d}</text>')
    for r in rng:
        o.append(f'<text x="200" y="{yr[r] + 5}" font-size="14" text-anchor="middle">{r}</text>')
    for d, r in pairs:
        o.append(f'<line x1="64" y1="{yd[d]}" x2="182" y2="{yr[r]}" stroke="#000" stroke-width="1.3" marker-end="url(#mp)"/>')
    return "".join(o) + "</svg>"


def htable(*rows):  # rows: (header, [values])
    return '<table class="t">' + "".join(
        f"<tr><th>{h}</th>" + "".join(f"<td>{v}</td>" for v in vals) + "</tr>" for h, vals in rows) + "</table>"


def vtable(heads, rows):
    return ('<table class="t"><tr>' + "".join(f"<th>{h}</th>" for h in heads) + "</tr>"
            + "".join("<tr>" + "".join(f"<td>{v}</td>" for v in r) + "</tr>" for r in rows) + "</table>")


# ---------- items ----------
def MC(stem, choices, right, fig="", why="", tip="", frames=(), keep=None, teks="", fmt="Multiple choice"):
    """choices: list; right: index or tuple of indices (Select TWO). keep: IEP choice indices (default: right + 2 wrong)."""
    right = (right,) if isinstance(right, int) else tuple(right)
    return dict(kind="mc", stem=stem, choices=choices, right=right, fig=fig, why=why, tip=tip, frames=frames,
                keep=keep, teks=teks, fmt=fmt if len(right) == 1 else "Multiselect")


def OPEN(stem, ans, fig="", why="", tip="", frames=(), lines=3, teks="", fmt="Constructed response"):
    return dict(kind="open", stem=stem, ans=ans, fig=fig, why=why, tip=tip, frames=frames, lines=lines, teks=teks, fmt=fmt)


def ROWS(stem, cols, rows, why="", tip="", teks="", fmt="Select one in each row"):
    """rows: (label_html, index of the right column)."""
    return dict(kind="rows", stem=stem, cols=cols, rows=rows, why=why, tip=tip, frames=(), teks=teks, fmt=fmt)


def blanks(s):  # [[answer]] -> blank line (answer in red on a key)
    out, rest = "", s
    while "[[" in rest:
        a, _, rest = rest.partition("[[")
        b, _, rest = rest.partition("]]")
        out += a + f'<span class="bl">{b if KEY else "&nbsp;"}</span>'
    return out + rest


def letters_for(k, count):
    return ("ABCDE" if k % 2 else "FGHJK")[:count]


def shown(it, num):  # (letters, choice indices) as printed; IEP keeps the right answer(s) + 2 wrong
    idx = list(range(len(it["choices"])))
    if IEP:
        idx = it["keep"] or sorted(list(it["right"]) + [k for k in idx if k not in it["right"]][:2])
    return letters_for(num, len(idx)), idx


PT = False  # inside a practice test: student copies show only the question type, like the real test


def render(it, num):
    h = f'<div class="q"><div class="n">{num}.</div><div class="body">'
    if it["teks"]:
        h += f'<div class="tag">{it["fmt"]}{"" if PT and not KEY else f" · TEKS {it["teks"]}"}</div>'
    h += f'<p>{blanks(it["stem"])}</p>'  # drag-and-drop boxes: [[answer]] in the stem
    figs = it.get("fig", "")
    if callable(figs):  # graph-it items: the answer line is drawn only on a key
        figs = figs()
    if it["kind"] == "mc":
        L, idx = shown(it, num)
        ch = "".join(f'<p class="{"ok" if KEY and k in it["right"] else ""}"><b>{l}.</b> {it["choices"][k]}</p>'
                     for l, k in zip(L, idx))
        h += f'<div class="row">{figs}<div class="mc">{ch}</div></div>' if figs else f'<div class="mc">{ch}</div>'
        if KEY:
            h += f'<div class="ans">Answer: {", ".join(l for l, k in zip(L, idx) if k in it["right"])}</div>'
    elif it["kind"] == "rows":
        h += ('<table class="t rows"><tr><th></th>' + "".join(f"<th>{c}</th>" for c in it["cols"]) + "</tr>"
              + "".join(f"<tr><td class='lab'>{lab}</td>" + "".join(
                  f'<td>{"●" if KEY and c == r else "○"}</td>' for c in range(len(it["cols"]))) + "</tr>"
                        for lab, r in it["rows"]) + "</table>")
    else:
        h += figs
        if not (IEP and it["frames"]):
            h += f'<div class="work" style="height:{it["lines"] * (0.5 if IEP else 0.42)}in"></div>'
        if KEY:
            h += f'<div class="ans">{it["ans"]}</div>'
    if IEP and it["tip"]:
        h += f'<div class="tip"><b>Tip:</b> {it["tip"]}</div>'
    if IEP and it["frames"]:
        h += '<div class="frames">' + "".join(f"<p>{blanks(f)}</p>" for f in it["frames"]) + "</div>"
    if KEY and it["why"]:
        h += f'<div class="why">{it["why"]}</div>'
    return h + "</div></div>"


# =====================================================================================================
# MODULE 1 · TOPIC 1 · Quantities and Relationships
# =====================================================================================================
def ch1():
    exp_lines = plot((-8, 8, 1, 2), (-8, 8, 1, 2), [dict(f=lambda t: 2 ** t - 2, a=-8, b=3.3)])
    c2 = plot((0, 16, 1, 4), (0, 64, 4, 16), [dict(f=lambda t: 4 * t, a=0, b=14.5, ends=("closed", "arrow"))],
              xlab="Bags of Mulch", ylab="Cost (dollars)")
    c3 = plot((-5, 3, 1, 1), (-5, 4, 1, 1), [dict(f=lambda t: (t + 1) ** 2 - 4, a=-5, b=3)])
    c4 = plot((0, 10, 1, 2), (0, 22, 2, 4), pts=[(k, 8 + 1.5 * k) for k in range(9)],
              xlab="Movies Rented", ylab="Monthly Cost (dollars)")
    c6 = plot((0, 24, 2, 4), (0, 140, 10, 20), [dict(f=lambda t: 120 - 6 * t, a=0, b=20, ends=("closed", "closed"))],
              xlab="Weeks", ylab="Gift Card Balance ($)")
    gA = plot((-4, 4, 1, 2), (-4, 6, 1, 2), [dict(f=lambda t: t * t - 2, a=-4, b=4)], size=150)
    gB = plot((-4, 4, 1, 2), (-4, 6, 1, 2), [dict(f=lambda t: -1.5 * t + 1, a=-4, b=4)], size=150)
    gC = plot((-4, 4, 1, 2), (-4, 6, 1, 2), [dict(f=lambda t: 4 * 0.5 ** t, a=-1.2, b=4)], size=150)
    c9 = plot((-2, 4, 1, 1), (0, 10, 1, 2), [dict(f=lambda t: 2 ** t, a=0, b=3, ends=("open", "closed"))], pts=[(3, 8, "(3, 8)")])
    c10 = plot((-8, 4, 1, 2), (-8, 10, 1, 2), [dict(f=lambda t: -(t + 3) ** 2 + 5, a=-7, b=1)])

    sections = [
        dict(title="1.1 Independent and Dependent Quantities", lesson="Lesson 1 · Activities 1–2 ✪",
             idea=f"""<p>The <b>independent quantity</b> is the one that changes on its own (the input). The
             <b>dependent quantity</b> depends on it (the output). Ask: <i>“Does A depend on B?”</i></p>
             <p>The independent quantity goes on the <b>{x}-axis</b>. The dependent quantity goes on the <b>{y}-axis</b>.</p>""",
             example=f"""<p><b>A plumber charges $60 to come to your house plus $45 for each hour of work.</b></p>
             <p>Does the time depend on the charge? No. Does the charge depend on the time? <b>Yes.</b></p>
             <p>Independent: <b>hours worked</b> ({x}-axis) &nbsp;·&nbsp; Dependent: <b>total charge</b> ({y}-axis)</p>""",
             items=[
                 MC("Maya fills a pool with a hose. The amount of water in the pool changes as the hose runs. "
                    "Which quantity is the <b>independent</b> quantity?",
                    ["The gallons of water in the pool", "The number of minutes the hose runs",
                     "The total cost of the water", "The depth of the pool"], 1,
                    why="The water in the pool depends on how long the hose runs, so time is the independent quantity.",
                    tip="The independent quantity is the one you control: what goes in first?"),
                 OPEN("Name the independent and dependent quantity in each situation.<br>"
                      "a. The cost of gas and the number of gallons pumped<br>"
                      "b. The height of a candle and the number of hours it burns",
                      "a. Independent: gallons pumped · Dependent: cost<br>b. Independent: hours burning · Dependent: height",
                      frames=["a. Independent: [[gallons pumped]] · Dependent: [[cost]]",
                              "b. Independent: [[hours burning]] · Dependent: [[height]]"],
                      tip="Fill in: “The ____ depends on the ____.” The first blank is the dependent quantity."),
                 MC("The student council sells raffle tickets. The money raised depends on the number of tickets sold. "
                    "How should the axes of the graph be labeled?",
                    [f"{x}-axis: money raised; {y}-axis: tickets sold", f"{x}-axis: tickets sold; {y}-axis: money raised",
                     f"{x}-axis: tickets sold; {y}-axis: tickets sold", f"{x}-axis: time; {y}-axis: money raised"], 1,
                    why="Independent (tickets sold) on the x-axis, dependent (money raised) on the y-axis."),
             ]),
        dict(title="1.2 Reading a Graph’s Key Features", lesson="Lesson 2 · Getting Started, Activity 1, Talk the Talk ✪",
             idea=f"""<p><b>{y}-intercept</b>: where the graph crosses the {y}-axis, (0, <i>b</i>). It is often the
             <b>starting amount</b>. &nbsp; <b>{x}-intercept</b>: where it crosses the {x}-axis, (<i>a</i>, 0).</p>
             <p><b>Increasing</b>: goes up from left to right. <b>Decreasing</b>: goes down. <b>Maximum</b>/<b>minimum</b>:
             highest/lowest point.</p><p><b>Continuous</b>: one connected line or curve (any value makes sense, like
             time). <b>Discrete</b>: separate dots (only whole counts make sense, like tickets).</p>""",
             example=f"""<p><b>A 12-inch candle burns down steadily and is gone after 6 hours.</b> Its graph goes from
             (0, 12) to (6, 0).</p><p>{y}-intercept (0, 12): the candle starts at 12 inches. &nbsp; {x}-intercept (6, 0):
             it burns out at 6 hours. &nbsp; The graph is <b>decreasing</b> and <b>continuous</b> (time can be any value).</p>""",
             items=[
                 MC(f"The graph of {y} = 2{x} − 4 is shown. Which statements are true? Select <b>TWO</b> correct answers.",
                    [f"The {y}-intercept is (0, −4).", "The graph is decreasing.", f"The {x}-intercept is (−4, 0).",
                     "The graph is increasing.", "The graph is discrete."], (0, 3),
                    fig=plot((-6, 6, 1, 2), (-6, 6, 1, 2), [dict(f=lambda t: 2 * t - 4, a=-6, b=6)]),
                    why="It crosses the y-axis at (0, −4) and goes up from left to right. The x-intercept is (2, 0).",
                    tip="Put your finger on the y-axis. Where does the line cross it? Then trace left to right: up or down?"),
                 MC("Which situation is best shown by a <b>discrete</b> graph (separate dots)?",
                    ["The distance a car travels over time", "The temperature of soup as it cools",
                     "The total cost of buying concert tickets", "The amount of water in a draining tub"], 2,
                    why="You can only buy whole tickets (1, 2, 3, …), so the graph is separate dots.",
                    tip="Discrete = things you count (people, tickets, cars). Continuous = things you measure (time, distance)."),
                 OPEN("A phone battery is at 90% when Ty unplugs it. It loses 15% each hour until it dies.<br>"
                      "a. What is the y-intercept? What does it mean?<br>b. What is the x-intercept? What does it mean?",
                      "a. (0, 90): the battery starts at 90% when it is unplugged (0 hours).<br>"
                      "b. (6, 0): after 6 hours the battery is at 0% (dead). 90 ÷ 15 = 6.",
                      frames=["a. The y-intercept is (0, [[90]]). It means the battery starts at [[90]]% at [[0]] hours.",
                              "b. 90 ÷ 15 = [[6]], so the x-intercept is ([[6]], 0). The battery dies after [[6]] hours."]),
             ]),
        dict(title="1.3 Functions and Function Families", lesson="Lesson 3 · Activities 1–5, Talk the Talk ✪",
             idea=f"""<p>A <b>function</b> gives each input <b>exactly one</b> output. Check a table or list: an
             {x}-value may not repeat with a different {y}. Check a graph with the <b>vertical line test</b>: no vertical
             line may hit the graph twice.</p><p><b>Function notation</b>: <i>f</i>(3) means “the output when the
             input is 3.”</p><p><b>Families</b>: <b>linear</b> = straight line (<i>y</i> = <i>mx</i> + <i>b</i>);
             <b>quadratic</b> = U-shape, a parabola (<i>y</i> = <i>ax</i>² + <i>bx</i> + <i>c</i>); <b>exponential</b> =
             a curve that flattens out on one side and shoots up or down on the other (<i>y</i> = <i>a</i> · <i>b<sup>x</sup></i>).</p>""",
             example=f"""<p><b>Is {{(1, 4), (2, 5), (1, 6)}} a function?</b> No: the input 1 has two outputs, 4 and 6.</p>
             <p><b>If <i>f</i>({x}) = 3{x} − 2, find <i>f</i>(4).</b> Replace {x} with 4: 3(4) − 2 = 12 − 2 = <b>10</b>.</p>""",
             items=[
                 OPEN(f"If <i>f</i>({x}) = 2{x}² − 1, what is <i>f</i>(−3)?", "<i>f</i>(−3) = 2(9) − 1 = 17",
                      frames=["<i>f</i>(−3) = 2(−3)² − 1 = 2([[9]]) − 1 = [[17]]"],
                      tip="Square first: (−3)² = (−3)(−3) = 9. Then multiply, then subtract.", lines=2),
                 OPEN("Does the mapping diagram represent a function? Explain.",
                      "Yes. Each input (−1, 2, 5) has exactly one output. Two inputs may share the output 4.",
                      fig=mapping([-1, 2, 5], [0, 4, 7], [(-1, 4), (2, 0), (5, 4)]),
                      frames=["Count the arrows leaving each input: −1 has [[1]], 2 has [[1]], 5 has [[1]].",
                              "So it [[is]] a function, because each input has exactly one output."],
                      tip="Look at the LEFT oval. If any number has 2 arrows leaving it, it is NOT a function."),
                 ROWS("Which function family does each equation belong to? Select one in each row.",
                      ["Linear", "Quadratic", "Exponential"],
                      [(f"{y} = 3{x} + 1", 0), (f"{y} = 4 · 2<sup>{x}</sup>", 2), (f"{y} = {x}² − 5", 1)],
                      why="x alone → linear; x² → quadratic; x in the exponent → exponential.",
                      tip="Where is the x? Alone → linear. Squared (x²) → quadratic. Up in the exponent → exponential."),
                 MC("Which graph does <b>not</b> represent a function?",
                    ["A line that goes up from left to right", "A U-shaped parabola that opens up",
                     "A parabola that opens to the right", "A curve that flattens out on the left and rises on the right"], 2,
                    why="A parabola opening to the right fails the vertical line test: one x-value has two y-values."),
             ]),
        dict(title="1.4 Domain and Range", lesson="Lesson 4 · Getting Started, Activities 1–2 ✪",
             idea=f"""<p><b>Domain</b> = all the {x}-values the graph uses (read left to right).
             <b>Range</b> = all the {y}-values (read bottom to top).</p>
             <p>● closed dot: <b>{LE}</b> or <b>{GE}</b> (included) &nbsp; ○ open dot: <b>&lt;</b> or <b>&gt;</b> (not
             included) &nbsp; ➜ arrow: keeps going forever.</p><p>In a story, think about what makes sense: time and
             counts can’t be negative. A <b>discrete</b> graph’s domain is a <b>list</b> of values.</p>""",
             example=f"""<p><b>A parabola opens down with its vertex at (1, 5) and arrows on both ends.</b></p>
             <p>Domain: all real numbers (arrows go left and right forever). &nbsp; Range: <b>{y} {LE} 5</b> (5 is the highest point).</p>
             <p><b>A garage charges $3 an hour, up to 8 hours.</b> Domain 0 {LE} {x} {LE} 8 &nbsp;·&nbsp; Range 0 {LE} {y} {LE} 24.</p>""",
             items=[
                 MC("Which describes the range of the function graphed?",
                    [f"{y} {GE} −3", f"{y} {LE} −3", f"{x} {GE} −2", "All real numbers"], 0,
                    fig=plot((-6, 3, 1, 1), (-4, 6, 1, 2), [dict(f=lambda t: (t + 2) ** 2 - 3, a=-6, b=3)]),
                    why="The lowest point is the vertex (−2, −3) and the arrows go up forever, so y ≥ −3.",
                    tip="Range = y-values. Find the lowest point. Does the graph go up or down from there?"),
                 OPEN("The graph shows a piece of an exponential function. Use inequalities to write its domain and range.",
                      f"Domain: −2 &lt; {x} {LE} 3 &nbsp;·&nbsp; Range: 0.25 &lt; {y} {LE} 8",
                      fig=plot((-3, 4, 1, 1), (0, 9, 1, 1), [dict(f=lambda t: 2 ** t, a=-2, b=3, ends=("open", "closed"))]),
                      why="Open dot at (−2, 0.25) → &lt;. Closed dot at (3, 8) → ≤.",
                      frames=[f"Domain: [[−2]] [[&lt;]] {x} [[≤]] [[3]]", f"Range: [[0.25]] [[&lt;]] {y} [[≤]] [[8]]"],
                      tip="Open dot → use &lt;. Closed dot → use ≤."),
                 MC("A bakery sells muffins for $2 each. A box holds at most 6 muffins. Which statements are true? "
                    "Select <b>TWO</b> correct answers.",
                    ["Domain: 0, 1, 2, 3, 4, 5, 6", f"Domain: 0 {LE} {x} {LE} 6", "Range: 0, 2, 4, 6, 8, 10, 12",
                     "The graph is continuous.", "The range is all real numbers."], (0, 2),
                    fig=plot((0, 8, 1, 2), (0, 14, 1, 2), pts=[(k, 2 * k) for k in range(7)], xlab="Muffins",
                             ylab="Cost ($)", size=190),
                    why="You can only buy whole muffins, so the graph is dots and the domain and range are lists."),
                 OPEN(f"The graph of quadratic function <i>g</i> has its vertex at (−3, 7) and opens down. "
                      "What is the maximum value of <i>g</i>?", "7 (the y-value of the vertex)",
                      frames=["The highest point is the vertex (−3, 7). The maximum value is the [[y]]-value: [[7]]."],
                      tip="The maximum VALUE is a y-value, not a point.", lines=1),
             ]),
    ]

    check = [
        ROWS("Look at the graph. Is each statement true or false?<br>" + exp_lines, ["True", "False"],
             [("It is an exponential function.", 0), ("It falls from left to right.", 1), (f"It crosses the {x}-axis at (1, 0).", 0),
              (f"It crosses the {y}-axis at (0, −2).", 1)],
             why="It flattens out on the left and rises on the right (exponential). It crosses the x-axis at (1, 0) and the y-axis at (0, −1).",
             tip="Read where it crosses EACH axis carefully."),
        OPEN("Mulch costs $4 a bag. The graph shows the cost of the mulch. Use inequalities to write the domain and range "
             "shown by the graph.", f"Domain: {x} {GE} 0 · Range: {y} {GE} 0 (closed dot at (0, 0); the arrow never stops)", fig=c2,
             frames=[f"Domain: {x} [[≥]] [[0]] · Range: {y} [[≥]] [[0]]"],
             tip="An arrow means it does NOT stop. Closed dot at 0 means “greater than or equal to 0.”", lines=2),
        MC("What is the range of the parabola shown?", [f"{y} &gt; −4", f"{y} {LE} −4", f"{y} {GE} −4", f"{x} {GE} −1"], 2, fig=c3,
           why="The vertex (−1, −4) is the lowest point, it is on the graph, and the graph goes up forever: y ≥ −4."),
        OPEN("A streaming service charges $8 a month plus $1.50 for each movie rented, up to 8 movies. The graph shows "
             "the monthly cost.<br>a. Is the graph discrete or continuous? Why?<br>b. List the domain and the range.",
             "a. Discrete: you can only rent whole movies. b. Domain {0, 1, 2, …, 8}; range {8, 9.5, 11, 12.5, 14, 15.5, 17, 18.5, 20}",
             fig=c4, frames=["a. [[Discrete]]: only [[whole]] movies can be rented.",
                             "b. Domain: 0, 1, 2, …, [[8]] · Range: 8, [[9.5]], [[11]], …, [[20]]"], lines=4),
        MC(f"Which table does <b>NOT</b> represent a function?",
           [htable((x, [5, 6, 7, 8]), (y, [1, 1, 1, 1])), htable((x, ["−2", 0, 2, 4]), (y, [3, 3, 7, 9])),
            htable((x, [1, 2, 2, 3]), (y, [5, 6, 9, 10])), htable((x, [0, 1, 2, 3]), (y, [4, 4, 8, 8]))], 2,
           why="In C the input 2 has two outputs (6 and 9). Repeating a y-value, like 1, 1, 1, 1, is allowed.",
           tip="Look ONLY at the x row. If an x-value repeats with a different y, it is NOT a function."),
        OPEN("Marcus has $120 on a gift card. He spends $6 each week on snacks. The graph shows this situation. "
             "Where does the graph start on the <i>y</i>-axis, and what does that point tell you about Marcus’s card?",
             "(0, 120): before any weeks pass (0 weeks), the gift card balance is $120.", fig=c6,
             frames=["The y-intercept is (0, [[120]]).", "It means that at [[0]] weeks, the card has $[[120]] on it."]),
        OPEN("Is the relation {(1, 2), (4, −3), (9, 2), (4, 5)} a function? Explain.",
             "Not a function. The input 4 is paired with two outputs, −3 and 5.",
             frames=["The input [[4]] appears [[2]] times, with outputs [[−3]] and [[5]].",
                     "So it is [[not]] a function."], lines=2),
        MC("Which graph shows an exponential function?", [gA, gB, gC], 2, keep=(0, 1, 2),
           why="A is a U-shape (quadratic), B is a straight line (linear), C flattens out on the right (exponential).",
           tip="Exponential graphs curve and flatten out on one side."),
        OPEN("The graph shows <i>y</i> = 2<sup><i>x</i></sup> from an open dot to a closed dot. Use inequalities to describe "
             "the <i>x</i>-values and the <i>y</i>-values shown.", f"Domain: 0 &lt; {x} {LE} 3 &nbsp;·&nbsp; Range: 1 &lt; {y} {LE} 8", fig=c9,
             frames=[f"Domain: [[0]] [[&lt;]] {x} [[≤]] [[3]]", f"Range: [[1]] [[&lt;]] {y} [[≤]] [[8]]"],
             why="Open dot at (0, 1); closed dot at (3, 8)."),
        OPEN("What is the greatest output value of the parabola graphed? Give the point where it happens too.",
             "5, at the vertex (−3, 5)", fig=c10, frames=["Highest point: ([[−3]], [[5]]). Greatest output: [[5]]."],
             why="The greatest output is the y-value of the highest point (the vertex).", lines=1),
        # more ways to show the same skills (story, table, equation)
        OPEN("A parking garage charges $2 per hour. You can pay for part of an hour, and you can park for at most "
             "10 hours. Write the domain and range of the cost function.",
             f"Domain: 0 {LE} {x} {LE} 10 hours · Range: 0 {LE} {y} {LE} 20 dollars",
             frames=[f"Domain: [[0]] ≤ {x} ≤ [[10]]", f"Range: [[0]] ≤ {y} ≤ [[20]] &nbsp; (2 × 10 = 20)"],
             tip="Domain = hours (from the story). Range = cost: multiply the most hours by $2."),
        OPEN("The table shows the water in a pool as it drains. What is the <i>y</i>-intercept? What does it mean?"
             + htable(("Hours", [0, 1, 2, 3]), ("Gallons", [900, 750, 600, 450])),
             "(0, 900): before draining starts (0 hours), the pool holds 900 gallons.",
             frames=["At 0 hours there are [[900]] gallons, so the y-intercept is (0, [[900]]).",
                     "It means the pool starts with [[900]] gallons."]),
        ROWS("Which function family does each table show?", ["Linear", "Quadratic", "Exponential"],
             [(htable((x, [0, 1, 2, 3]), (y, [2, 5, 8, 11])), 0), (htable((x, [0, 1, 2, 3]), (y, [3, 6, 12, 24])), 2),
              (htable((x, [-2, -1, 0, 1]), (y, [4, 1, 0, 1])), 1)],
             why="+3 each time → linear; ×2 each time → exponential; goes down then up (x²) → quadratic.",
             tip="Add the same? Linear. Multiply by the same? Exponential. Down then back up? Quadratic."),
        MC("A parabola opens down. Its vertex is (4, −2). Which is the range?",
           [f"{y} {GE} −2", f"{y} {LE} −2", f"{y} {LE} 4", f"{x} {LE} 4"], 1,
           why="Opens down → the vertex is the highest point, so every y-value is −2 or less.",
           tip="Sketch it! Draw the vertex, then draw the parabola going down."),
        OPEN(f"What is the minimum value of {y} = ({x} + 1)² − 6?", "−6 (the vertex is (−1, −6))", lines=1,
             frames=["The vertex is ([[−1]], [[−6]]). It opens up, so the minimum value is [[−6]]."]),
    ]

    staar = [
        MC("Which set of ordered pairs represents a function?",
           ["{(2, 3), (4, 5), (2, 7), (6, 9)}", "{(−1, 0), (0, 0), (1, 0), (2, 0)}",
            "{(5, 1), (5, 2), (5, 3), (5, 4)}", "{(0, 2), (3, 4), (0, −2), (8, 1)}"], 1, teks="A.12(A)",
           why="Only B has no repeated x-value. All outputs being 0 is fine."),
        MC(f"The function <i>f</i>({x}) = 4{x} − 1 is defined for −2 {LE} {x} {LE} 3. What is the range of <i>f</i>?",
           [f"−2 {LE} <i>f</i>({x}) {LE} 3", f"−9 {LE} <i>f</i>({x}) {LE} 11", f"−1 {LE} <i>f</i>({x}) {LE} 11",
            f"−9 {LE} <i>f</i>({x}) {LE} 3"], 1, teks="A.2(A)",
           why="f(−2) = −9 and f(3) = 11; the line increases, so −9 ≤ f(x) ≤ 11."),
        MC(f"What is the range of {y} = ({x} − 3)² + 2?", [f"{y} {GE} 3", f"{y} {GE} 2", f"{y} {LE} 2", "All real numbers"],
           1, teks="A.6(A)", why="The vertex is (3, 2) and the parabola opens up (a = 1 > 0), so y ≥ 2."),
        MC(f"Which statement is true about the graph of <i>f</i>({x}) = 5(2)<sup>{x}</sup>?",
           [f"The {y}-intercept is (0, 5).", f"The {y}-intercept is (0, 2).", "The graph is decreasing.",
            f"The {x}-intercept is (0, 5)."], 0, teks="A.9(D)",
           why="f(0) = 5 · 2⁰ = 5 · 1 = 5. Base 2 > 1, so it increases. It never touches the x-axis."),
        OPEN(f"Choose the words that complete the sentence.<br>The graph of {y} = −{x}² + 6{x} has a "
             "( maximum / minimum ) at the point ( (3, 9) / (−3, 9) / (3, −9) ).",
             "maximum · (3, 9)", teks="A.7(A)", fmt="Inline choice", lines=1,
             why="a = −1 < 0 opens down → maximum. Vertex x = −b/(2a) = −6/(−2) = 3; y = −9 + 18 = 9.",
             frames=["a = −1 is negative, so it opens [[down]] and has a [[maximum]].",
                     "x = −b ÷ (2a) = −6 ÷ (−2) = [[3]] ; y = −(3)² + 6(3) = [[9]] → ([[3]], [[9]])"]),
        ROWS("Match each situation with the function family that models it.", ["Linear", "Quadratic", "Exponential"],
             [("A savings account grows by 5% each year.", 2), ("A taxi charges $3 plus $2 per mile.", 0),
              ("The height of a ball thrown up in the air over time.", 1)], teks="A.3(C), A.9(D)", fmt="Drag and drop",
             why="Same amount added → linear; same percent → exponential; up-then-down path → quadratic."),
    ]
    vocab = [("independent quantity", "the input; the quantity that changes on its own"),
             ("dependent quantity", "the output; depends on the independent quantity"),
             ("function", "a relation where each input has exactly one output"),
             ("domain / range", "all input (x) values / all output (y) values"),
             ("x-intercept / y-intercept", "where a graph crosses the x-axis / the y-axis"),
             ("discrete / continuous", "separate dots / connected line or curve"),
             ("maximum / minimum", "highest / lowest y-value of a graph")]
    return dict(code="M1 T1", title="Quantities and Relationships", module="Module 1: Searching for Patterns",
                teks="A.2A, A.3C, A.6A, A.7A, A.9A, A.9D, A.12A", vocab=vocab, sections=sections, check=check, staar=staar)


# =====================================================================================================
# MODULE 1 · TOPIC 2 · Sequences
# =====================================================================================================
def arith(a1, d, k):
    return [a1 + d * j for j in range(k)]


def geo(g1, r, k):
    return [g1 * r ** j for j in range(k)]


def nums(v):
    return ", ".join(f"{t:g}".replace("-", "−") if not isinstance(t, Fr) or t.denominator == 1 else
                     fr(str(t.numerator).replace("-", "−"), t.denominator) for t in v)


def ch2():
    an, gn, fn, mn, qn, rn, pn = (sub(c, "n") for c in "agfmqrp")
    an1, fn1, mn1, rn1, gn1 = sub("a", "n−1"), sub("f", "n−1"), sub("m", "n−1"), sub("r", "n−1"), sub("g", "n−1")
    tv = dict(xlab="Term Number", ylab="Term Value")
    c1 = plot((0, 10, 1, 1), (-4, 12, 1, 2), pts=[(k, 11 - 2 * k) for k in range(1, 7)], **tv)
    c2 = plot((0, 6, 1, 1), (0, 30, 2, 4), pts=[(k, 3 ** (k - 1)) for k in range(1, 5)], **tv)
    seqA = arith(30, -4, 5)
    assert seqA == [30, 26, 22, 18, 14]
    c3d = plot((0, 6, 1, 1), (0, 32, 2, 4), pts=[(k, 30 - 4 * (k - 1) - 4) for k in range(1, 6)], size=170)
    six = arith(-2, 0.75, 5)  # decimals, like the stem
    seven = geo(Fr(1, 4), 3, 5)
    q = geo(2, 3, 7)
    assert q[3:] == [54, 162, 486, 1458]

    sections = [
        dict(title="2.1 Patterns and Sequences", lesson="Lesson 1 · Activities 1–2, Talk the Talk ✪",
             idea=f"""<p>A <b>sequence</b> is an ordered list of numbers called <b>terms</b>. The <b>term number</b>
             {n} (1st, 2nd, 3rd, …) is the input; the <b>term value</b> is the output.</p><p>A sequence is a
             <b>function</b>: each term number has exactly one value. Its domain is 1, 2, 3, …, so its graph is
             <b>discrete</b> (dots).</p>""",
             example="""<p><b>3, 7, 11, 15, …</b> Each term is 4 more than the one before, so the next term is
             15 + 4 = <b>19</b>. The 1st term is 3: the point (1, 3) is on its graph.</p>""",
             items=[
                 OPEN("Write the next two terms: 50, 45, 40, 35, …", "30, 25 (subtract 5 each time)",
                      frames=["Each term is [[5]] [[less]] than the one before. Next two: [[30]], [[25]]"], lines=1),
                 MC("Which list matches the points (1, 2), (2, 6), (3, 18), (4, 54) on a graph?",
                    ["1, 2, 3, 4", "2, 6, 18, 54", "2, 4, 6, 8", "1, 2, 6, 18"], 1,
                    why="The term values are the y-coordinates, in order of the term numbers.",
                    tip="Term number = x. Term value = y. The sequence is the list of y-values."),
                 OPEN("In the sequence 1, 1, 2, 3, 5, 8, …, the value 1 appears twice. Is it still a function? Explain.",
                      "Yes. Each term number (1st, 2nd, 3rd, …) has exactly one term value. A value may repeat.",
                      frames=["Each term [[number]] has exactly [[one]] term value, so it [[is]] a function."], lines=2),
             ]),
        dict(title="2.2 Arithmetic and Geometric Sequences", lesson="Lesson 2 · Getting Started, Activities 1–2, Talk the Talk ✪",
             idea="""<p><b>Arithmetic</b>: <b>add</b> the same number each time, the <b>common difference</b>
             <i>d</i> = (a term) − (the term before it).</p><p><b>Geometric</b>: <b>multiply</b> by the same number
             each time, the <b>common ratio</b> <i>r</i> = (a term) ÷ (the term before it).</p>""",
             example="""<p><b>20, 14, 8, 2, …</b> 14 − 20 = −6, 8 − 14 = −6 → arithmetic, <i>d</i> = −6.</p>
             <p><b>4, 12, 36, 108, …</b> 12 ÷ 4 = 3, 36 ÷ 12 = 3 → geometric, <i>r</i> = 3.</p>""",
             items=[
                 ROWS("Is each sequence arithmetic, geometric, or neither?", ["Arithmetic", "Geometric", "Neither"],
                      [("7, 11, 15, 19, …", 0), ("2, −6, 18, −54, …", 1), ("1, 4, 9, 16, …", 2), ("80, 40, 20, 10, …", 1)],
                      why="+4 each time; ×(−3); differences 3, 5, 7 change and ratios change; ×½.",
                      tip="Subtract neighbors. Same answer every time? Arithmetic. If not, divide neighbors. Same? Geometric."),
                 OPEN("Find the common difference or common ratio.<br>a. 9, 5.5, 2, −1.5, …<br>b. 6, −3, 1.5, −0.75, …",
                      "a. d = −3.5 (arithmetic) &nbsp; b. r = −0.5 (geometric)",
                      frames=["a. 5.5 − 9 = [[−3.5]] → common [[difference]]", "b. −3 ÷ 6 = [[−0.5]] → common [[ratio]]"]),
             ]),
        dict(title="2.3 Recursive and Explicit Formulas", lesson="Lesson 3 · Activities 1–5, Talk the Talk ✪",
             idea=f"""<table class="t"><tr><th></th><th>Recursive (uses the term before)</th><th>Explicit (uses {n})</th></tr>
             <tr><th>Arithmetic</th><td>{an} = {an1} + <i>d</i>, &nbsp;{sub('a', 1)} = first term</td>
             <td>{an} = {sub('a', 1)} + <i>d</i>({n} − 1)</td></tr>
             <tr><th>Geometric</th><td>{gn} = <i>r</i> · {gn1}, &nbsp;{sub('g', 1)} = first term</td>
             <td>{gn} = {sub('g', 1)} · <i>r</i><sup>{n} − 1</sup></td></tr></table>
             <p>Recursive is good for the next few terms. Explicit jumps straight to any term, like the 50th.</p>""",
             example=f"""<p><b>6, 10, 14, 18, …</b> &nbsp; {sub('a', 1)} = 6, <i>d</i> = 4.</p>
             <p>Recursive: {an} = {an1} + 4, {sub('a', 1)} = 6. &nbsp; Explicit: {an} = 6 + 4({n} − 1) = <b>4{n} + 2</b>.
             &nbsp; 20th term: 4(20) + 2 = <b>82</b>.</p>
             <p><b>5, 15, 45, …</b> &nbsp; {gn} = 5 · 3<sup>{n} − 1</sup>. &nbsp; 6th term: 5 · 3⁵ = 5 · 243 = <b>1215</b>.</p>""",
             items=[
                 OPEN(f"Write the first five terms: {an} = {an1} − 3, where {sub('a', 1)} = 10.", nums(arith(10, -3, 5)),
                      frames=["10, [[7]], [[4]], [[1]], [[−2]]"], tip="Start at 10. Subtract 3 to get each next term.", lines=1),
                 OPEN(f"Write the first four terms: {sub('b', 'n')} = 2 · {sub('b', 'n−1')}, where {sub('b', 1)} = −3.",
                      nums(geo(-3, 2, 4)), frames=["−3, [[−6]], [[−12]], [[−24]]"], lines=1),
                 OPEN("Write a simplified explicit formula for 9, 13, 17, 21, …",
                      f"{an} = 9 + 4({n} − 1) = 4{n} + 5",
                      frames=[f"{sub('a', 1)} = [[9]], <i>d</i> = [[4]]",
                              f"{an} = [[9]] + [[4]]({n} − 1) = [[4]]{n} + [[5]]"], lines=2),
                 OPEN("A theater has 18 seats in row 1. Each row has 3 more seats than the row before it. "
                      "Write an explicit formula for the seats in row <i>n</i>. How many seats are in row 15?",
                      f"{an} = 18 + 3({n} − 1) = 3{n} + 15; row 15 has 3(15) + 15 = 60 seats.",
                      frames=[f"{an} = [[18]] + [[3]]({n} − 1) = [[3]]{n} + [[15]]", "Row 15: 3(15) + 15 = [[60]] seats"]),
                 OPEN("A ball is dropped. Its first bounce reaches 64 inches. Each bounce reaches half the height of the "
                      "bounce before. How high is the 5th bounce?", f"{gn} = 64(½)<sup>{n}−1</sup>; 64 → 32 → 16 → 8 → 4 inches",
                      frames=["64, [[32]], [[16]], [[8]], [[4]] → the 5th bounce is [[4]] inches."]),
             ]),
    ]

    check = [
        MC("The graph shows the first six terms of an arithmetic sequence. Which formula gives the <i>n</i>th term?",
           [f"{an} = 2{n} + 9", f"{an} = −2{n} + 9", f"{an} = −2{n} + 11", f"{an} = 11{n} − 2"], 2, fig=c1,
           why="Points (1, 9), (2, 7), (3, 5): d = −2 and a₁ = 9, so aₙ = 9 − 2(n − 1) = −2n + 11. Check n = 1: −2 + 11 = 9 ✓.",
           tip="Test each choice with n = 1. Which one gives the first dot’s value?"),
        MC("The graph shows the first four terms of a geometric sequence. Which formula gives the <i>n</i>th term?",
           [f"{gn} = 3<sup>{n}</sup>", f"{gn} = 3<sup>{n} − 1</sup>", f"{gn} = 3{n} − 2", f"{gn} = {n}<sup>3</sup>"], 1, fig=c2,
           why="Values 1, 3, 9, 27: g₁ = 1, r = 3 → gₙ = 1 · 3ⁿ⁻¹. (3ⁿ would give 3 for n = 1.)"),
        ROWS(f"A sequence starts with {sub('f', 1)} = 30 and follows {fn} = {fn1} − 4. Does each one show the same sequence?",
             ["Yes", "No"], [(nums(seqA), 0), ("26, 22, 18, 14, 10", 1), ("The dots on this graph:<br>" + c3d, 1),
                            (nums(arith(30, 4, 5)), 1), (f"<i>f</i>({n}) = 34 − 4{n}", 0)],
             why="30, 26, 22, 18, 14. The list and graph that start at 26 skip the first term; 30, 34, … adds 4. 34 − 4(1) = 30 ✓.",
             tip="Check the FIRST term (30) and the change (−4) for each one."),
        MC("A geometric sequence has a first term of 5 and a common ratio of 3. Which list shows its first four terms?",
           [nums(arith(5, 3, 4)), "5, 15, 75, 375", nums(geo(5, 3, 4)), "5, 15, 50, 160"], 2,
           why="Multiply by 3 each time: 5, 15, 45, 135."),
        MC(f"The 4th and 5th terms of a geometric sequence are 54 and 162. Which formula gives {qn}?",
           [f"{qn} = 54 · 3<sup>{n} − 1</sup>", f"{qn} = 2 · 3<sup>{n} + 1</sup>", f"{qn} = 2 · 3<sup>{n} − 1</sup>",
            f"{qn} = 54 · 3<sup>{n} + 1</sup>"], 2,
           why="r = 162 ÷ 54 = 3. Work back: q₃ = 18, q₂ = 6, q₁ = 2. Check: q₄ = 2 · 3³ = 54 ✓.",
           tip="54 is the 4th term, not the 1st. Divide by 3 to go back to q₁."),
        OPEN(f"List the first five terms if {sub('a', 1)} = −2 and {sub('a', 'n+1')} = {an} + 0.75.", nums(six),
             frames=["−2, [[−1.25]], [[−0.5]], [[0.25]], [[1]]"], tip="Add 0.75 each time. −2 + 0.75 = −1.25.", lines=1),
        OPEN(f"List the first five terms if {sub('r', 1)} = {fr(1, 4)} and {rn} = 3({rn1}).", nums(seven),
             frames=[f"{fr(1, 4)}, [[{fr(3, 4)}]], [[{fr(9, 4)}]], [[{fr(27, 4)}]], [[{fr(81, 4)}]]"],
             tip="Multiply only the top number (numerator) by 3.", lines=1),
        OPEN("Write the sequence −7.5, −3, 1.5, 6, 10.5, … two ways: as a recursive formula and as a simplified explicit formula.",
             f"Recursive: {an} = {an1} + 4.5, {sub('a', 1)} = −7.5 &nbsp;·&nbsp; Explicit: {an} = −7.5 + 4.5({n} − 1) = 4.5{n} − 12",
             frames=[f"<i>d</i> = −3 − (−7.5) = [[4.5]]", f"Recursive: {an} = {an1} + [[4.5]], {sub('a', 1)} = [[−7.5]]",
                     f"Explicit: {an} = −7.5 + 4.5({n} − 1) = [[4.5]]{n} − [[12]]"]),
        OPEN("A pond has 80 lily pads today, and the number doubles every week. How many lily pads will there be 6 weeks from "
             "today? Show how you got it.",
             "80 · 2⁶ = 80 · 64 = 5,120 lily pads. Doubling means multiply by 2 once for each of the 6 weeks.",
             frames=["80 → [[160]] → [[320]] → [[640]] → [[1,280]] → [[2,560]] → [[5,120]]",
                     "After 6 weeks there are [[5,120]] lily pads."]),
        OPEN(f"An arithmetic sequence follows {an} = {an1} − 3.4, and its 31st term is 18.6. Find its 33rd term.",
             "18.6 − 3.4 − 3.4 = 11.8", frames=["32nd: 18.6 − 3.4 = [[15.2]] ; 33rd: [[15.2]] − 3.4 = [[11.8]]"], lines=1),
        OPEN(f"A sequence follows {gn} = −3 · {gn1}, and {sub('g', 4)} = −5. Find {sub('g', 7)}.",
             f"−5 · (−3)³ = −5 · (−27) = {-5 * (-3) ** 3}",
             frames=["5th: −5 · (−3) = [[15]] ; 6th: 15 · (−3) = [[−45]] ; 7th: −45 · (−3) = [[135]]"], lines=1),
        MC("Why is the sequence −1, 1, −1, 1, … a function?", ["Each term number has exactly one term value.",
                                                             "The values never repeat.", "The values keep increasing.",
                                                             "It is not a function, because −1 repeats."], 0,
           why="Inputs are term numbers 1, 2, 3, …; each has one value. Outputs (values) may repeat."),
        # more ways to show the same skills (table, story, equation)
        OPEN("Write a simplified explicit formula for the sequence in the table."
             + htable((n, [1, 2, 3, 4]), (an, nums(arith(40, -7, 4)).split(", "))),
             f"{an} = 40 − 7({n} − 1) = −7{n} + 47",
             frames=[f"{sub('a', 1)} = [[40]], <i>d</i> = [[−7]]", f"{an} = 40 − 7({n} − 1) = [[−7]]{n} + [[47]]"]),
        OPEN("A video has 300 views on day 1. The views double each day. Write an explicit formula for the views on "
             f"day {n}. How many views are there on day 6?",
             f"{sub('v', 'n')} = 300 · 2<sup>{n} − 1</sup>; day 6: 300 · 2⁵ = {300 * 2 ** 5:,} views",
             frames=[f"{sub('v', 'n')} = [[300]] · [[2]]<sup>{n} − 1</sup>", "Day 6: 300 · 2⁵ = 300 · [[32]] = [[9,600]]"]),
        OPEN(f"Write a recursive formula for the sequence {an} = 7{n} − 3.",
             f"{sub('a', 1)} = 7(1) − 3 = 4; {an} = {an1} + 7",
             frames=[f"{sub('a', 1)} = 7(1) − 3 = [[4]] ; <i>d</i> = [[7]]", f"{an} = {an1} + [[7]], {sub('a', 1)} = [[4]]"],
             tip="The number in front of n is the common difference.", lines=2),
        OPEN("In the sequence 5, 9, 13, 17, …, which term number has the value 81?",
             f"{an} = 4{n} + 1; 4{n} + 1 = 81 → {n} = 20. The 20th term.",
             frames=[f"{an} = [[4]]{n} + [[1]]", f"4{n} + 1 = 81 → 4{n} = [[80]] → {n} = [[20]]"]),
        MC("Which explicit formula is represented by the graph?",
           [f"{gn} = 64 · 2<sup>{n} − 1</sup>", f"{gn} = 64 · (½)<sup>{n} − 1</sup>", f"{gn} = −32{n} + 96",
            f"{gn} = (½)<sup>{n} − 1</sup>"], 1,
           fig=plot((0, 6, 1, 1), (0, 70, 5, 10), pts=[(k, 64 / 2 ** (k - 1)) for k in range(1, 5)], **tv),
           why="64, 32, 16, 8: g₁ = 64 and each term is half the one before, so r = ½."),
    ]
    assert arith(40, -7, 4)[-1] == -7 * 4 + 47 and 4 * 20 + 1 == 81

    staar = [
        MC("Which explicit formula describes the arithmetic sequence 12, 7, 2, −3, …?",
           [f"{an} = 5{n} + 7", f"{an} = −5{n} + 12", f"{an} = −5{n} + 17", f"{an} = 12{n} − 5"], 2, teks="A.12(D)",
           why="a₁ = 12, d = −5: aₙ = 12 − 5(n − 1) = −5n + 17."),
        OPEN("Choose the words that complete the sentence.<br>The sequence 3, 6, 12, 24, … is ( arithmetic / geometric ) "
             "with a common ( difference / ratio ) of ( 2 / 3 ).", "geometric · ratio · 2", teks="A.12(C)",
             fmt="Inline choice", lines=1, frames=["6 ÷ 3 = [[2]], 12 ÷ 6 = [[2]] → [[geometric]], common [[ratio]] [[2]]"]),
        OPEN(f"What is the 10th term of the sequence {an} = 8 + 6({n} − 1)? Enter your answer.", "8 + 6(9) = 62",
             teks="A.12(D)", fmt="Text entry", lines=1, frames=["8 + 6(10 − 1) = 8 + 6([[9]]) = [[62]]"]),
        MC("A geometric sequence has a first term of 2 and a common ratio of 5. What is the 4th term?",
           ["17", "40", "250", "1,250"], 2, teks="A.12(D)", why="2 · 5³ = 2 · 125 = 250. (17 adds 5 three times.)"),
        MC(f"Which equations can be used to find the {n}th term of 4, 1, −2, −5, …? Select <b>TWO</b> correct answers.",
           [f"{an} = 4 − 3({n} − 1)", f"{an} = −3{n} + 7", f"{an} = 4 · (−3)<sup>{n} − 1</sup>", f"{an} = 3{n} + 1",
            f"{an} = 4{n} − 3"], (0, 1), teks="A.12(D)", fmt="Multiselect",
           why="d = −3: aₙ = 4 − 3(n − 1) = −3n + 7. Both are the same formula."),
        MC("A stack of 1 cup is 11 cm tall. Each cup added makes the stack 1.5 cm taller. Which formula gives the "
           f"height of a stack of {n} cups?", [f"<i>h</i><sub>{n}</sub> = 11{n} + 1.5", f"<i>h</i><sub>{n}</sub> = 1.5{n} + 11",
                                              f"<i>h</i><sub>{n}</sub> = 1.5{n} + 9.5", f"<i>h</i><sub>{n}</sub> = 11 · 1.5<sup>{n} − 1</sup>"],
           2, teks="A.12(C)", why="hₙ = 11 + 1.5(n − 1) = 1.5n + 9.5. Check n = 1: 1.5 + 9.5 = 11 ✓."),
    ]
    vocab = [("sequence / term", "an ordered list of numbers / each number in it"),
             ("term number (n)", "the position: 1st, 2nd, 3rd, …"),
             ("arithmetic sequence", "add the same common difference d each time"),
             ("geometric sequence", "multiply by the same common ratio r each time"),
             ("recursive formula", "finds a term from the term before it"),
             ("explicit formula", "finds any term directly from n")]
    return dict(code="M1 T2", title="Sequences", module="Module 1: Searching for Patterns", teks="A.12A, A.12C, A.12D",
                vocab=vocab, sections=sections, check=check, staar=staar)


# =====================================================================================================
# MODULE 2 · TOPIC 1 · Linear Functions
# =====================================================================================================
RED = "#c8102e"


def nm(v, money=False):  # 2.50 -> "2.5", -3 -> "−3"; money keeps cents
    s = f"{v:,.2f}" if money else f"{v:,.2f}".rstrip("0").rstrip(".")
    return s.replace("-", "−")


def eq(m, b, lhs="<i>y</i>"):  # y = mx + b with clean signs
    mx = "" if m == 0 else (f"{x}" if m == 1 else f"−{x}" if m == -1 else f"{nm(m)}{x}")
    if not mx:
        return f"{lhs} = {nm(b)}"
    return f"{lhs} = {mx}" + ("" if b == 0 else f" + {nm(b)}" if b > 0 else f" − {nm(-b)}")


def reg(xs, ys):
    s, b = linear_regression(xs, ys)
    return round(s, 2), round(b, 2)


def ch3():
    ex_x, ex_y = [1, 2, 3, 4, 5], [62, 68, 71, 79, 85]
    em, eb = reg(ex_x, ex_y)
    mem_x, mem_y = [0, 1, 2, 3, 4], [120, 135, 158, 166, 190]
    mm, mb = reg(mem_x, mem_y)
    sc_x, sc_y = [1, 2, 3, 4, 5, 6], [9.1, 8.8, 8.1, 7.9, 7.2, 6.8]
    assert correlation(sc_x, sc_y) < -0.9
    wk_x, wk_y = [1, 2, 3, 4, 5, 6, 7, 8], [3.2, 2.1, 4.5, 3.0, 2.8, 4.9, 3.6, 4.1]
    assert 0 < correlation(wk_x, wk_y) < 0.6
    lib_x, lib_y = [0, 1, 2, 3, 4], [2150, 2310, 2290, 2530, 2640]
    lm, lb = reg(lib_x, lib_y)
    tu_x, tu_y = [0, 1, 2, 3, 4, 5, 6], [0, 22, 41, 66, 80, 104, 121]
    ts, tb = linear_regression(tu_x, tu_y)
    pred = ts * 9 + tb
    sp_x, sp_y = [1, 2, 3, 4, 5, 6, 7, 8], [18, 16.5, 15, 12, 11.5, 9, 7.5, 6]
    assert correlation(sp_x, sp_y) < -0.95
    calc = ("<p class='note'><b>Calculator:</b> STAT → EDIT: type x-values in L1, y-values in L2. "
            "STAT → CALC → 4: LinReg(ax+b). Turn DiagnosticOn (MODE or CATALOG) to see <i>r</i>.</p>")

    sections = [
        dict(title="3.1 Lines of Best Fit (Linear Regression)", lesson="Lesson 1 · Getting Started, Activities 1–3, Talk the Talk ✪",
             idea=f"""<p>Real data is rarely a perfect line. The <b>line of best fit</b> (least squares regression line)
             comes as close as possible to all the points. Your calculator finds it: {y} = <i>a</i>{x} + <i>b</i>.</p>
             <p>Use it to <b>predict</b>: substitute the {x}-value and evaluate. The slope <i>a</i> is the average rate of
             change; <i>b</i> is the predicted value when {x} = 0.</p>{calc}""",
             example=f"""<p><b>Hours studied vs quiz score:</b></p>{htable(('Hours (x)', ex_x), ('Score (y)', ex_y))}
             <p>LinReg gives {eq(em, eb)}. &nbsp; Predict 6 hours: {nm(em)}(6) + {nm(eb)} = <b>{nm(em * 6 + eb)}</b>.</p>
             <p>Meaning of the slope: each extra hour of study adds about {nm(em)} points.</p>""",
             items=[
                 MC("A club tracks its members. Which linear function best models the data if <i>x</i> is the number of "
                    "years since 2018?" + htable(("Year", [2018, 2019, 2020, 2021, 2022]), ("Members", mem_y)),
                    [eq(mm, mb), eq(mb, mm), eq(round((190 - 120) / 4, 2), 120), eq(mm, 2018)], 0,
                    why=f"LinReg with x = 0, 1, 2, 3, 4 gives y ≈ {nm(mm)}x + {nm(mb)}. Choice C only uses the first and last points.",
                    tip="Type x = 0, 1, 2, 3, 4 (years SINCE 2018), not 2018, 2019, …"),
                 MC("A bake sale’s line of best fit is <i>y</i> = 3.75<i>x</i> + 22.4, where <i>x</i> is hours and <i>y</i> is "
                    "dollars raised. What is the best prediction for 10 hours?",
                    ["$37.50", "$59.90", "$227.75", "$26.15"], 1,
                    why="3.75(10) + 22.4 = 37.5 + 22.4 = 59.90.", tip="Replace x with 10. Multiply first, then add."),
                 OPEN("A plant’s height is modeled by <i>y</i> = 1.8<i>x</i> + 12, where <i>x</i> is days and <i>y</i> is "
                      "centimeters. What do 1.8 and 12 mean?",
                      "1.8: the plant grows about 1.8 cm per day. 12: it was about 12 cm tall at day 0.",
                      frames=["1.8 means the plant grows about [[1.8]] cm each [[day]].",
                              "12 means the plant was [[12]] cm tall at day [[0]]."]),
             ]),
        dict(title="3.2 Correlation and Causation", lesson="Lesson 2 · Getting Started, Activities 1–4, Talk the Talk ✪",
             idea="""<p>The <b>correlation coefficient</b> <i>r</i> is between −1 and 1. The <b>sign</b> gives the direction
             (positive: up together; negative: one up, one down). The <b>size</b> gives the strength: close to 1 or −1 is
             <b>strong</b>; close to 0 is <b>weak</b>.</p><p><b>Correlation is not causation.</b> Two things can rise
             together without one causing the other. <b>Causation</b> means one thing actually makes the other happen.</p>""",
             example="""<p><i>r</i> = −0.94 → <b>strong negative</b>. &nbsp; <i>r</i> = 0.21 → <b>weak positive</b>.</p>
             <p>Ice cream sales and sunburns rise together (correlation), but ice cream doesn’t cause sunburns: hot,
             sunny weather causes both.</p>""",
             items=[
                 ROWS("Describe each correlation coefficient.", ["Strong positive", "Weak positive", "Weak negative", "Strong negative"],
                      [("<i>r</i> = 0.96", 0), ("<i>r</i> = −0.89", 3), ("<i>r</i> = 0.15", 1), ("<i>r</i> = −0.25", 2)],
                      tip="Sign → direction. Close to 1 or −1 → strong. Close to 0 → weak."),
                 MC("Which is an example of <b>causation</b>, not just correlation?",
                    ["Cities with more libraries have more traffic jams.", "Turning up the oven makes cookies bake faster.",
                     "Students with bigger shoes score higher on reading tests.", "Towns with more firefighters have more fires."], 1,
                    why="Heat really makes cookies bake faster. The others are linked by a third thing (city size, age, town size)."),
                 MC("The table shows daily screen time and sleep. What does the correlation coefficient indicate?"
                    + htable(("Screen time (h)", sc_x), ("Sleep (h)", sc_y)),
                    ["Weak negative correlation", "Strong negative correlation", "Weak positive correlation",
                     "Strong positive correlation"], 1,
                    why=f"r ≈ {nm(round(correlation(sc_x, sc_y), 2))}: sleep goes down steadily as screen time goes up."),
             ]),
        dict(title="3.3 Rate of Change, and Sequences as Linear Functions", lesson="Lesson 3 · Activities 1–4 ✪",
             idea=f"""<p><b>Rate of change</b> = (change in {y}) ÷ (change in {x}). Always say the <b>units</b>:
             “dollars per ticket,” “gallons per minute.” If it is the same between every pair of points, the
             relationship is <b>linear</b>.</p><p>An arithmetic sequence is a linear function: the common difference
             <i>d</i> is the slope. {sub('a', 'n')} = {sub('a', 1)} + <i>d</i>({n} − 1) is the same as
             <i>f</i>({n}) = <i>d</i>{n} + ({sub('a', 1)} − <i>d</i>).</p>""",
             example=f"""<p>{htable(('Minutes', [2, 5, 9]), ('Gallons', [46, 37, 25]))}</p>
             <p>(37 − 46) ÷ (5 − 2) = −9 ÷ 3 = <b>−3 gallons per minute</b>. Check: (25 − 37) ÷ (9 − 5) = −3 ✓.</p>""",
             items=[
                 OPEN("Determine the rate of change. Include units." + htable(("Tickets sold", [10, 14, 20]),
                                                                                ("Profit ($)", ["−12", 6, 33])),
                      "(6 − (−12)) ÷ (14 − 10) = 18 ÷ 4 = 4.5 dollars per ticket",
                      frames=["(6 − (−12)) ÷ (14 − 10) = [[18]] ÷ [[4]] = [[4.5]]", "Units: [[dollars]] per [[ticket]]"],
                      tip="Subtracting a negative is adding: 6 − (−12) = 6 + 12."),
                 OPEN(f"Write the sequence 7, 11, 15, 19, … as a linear function <i>f</i>({n}).",
                      f"<i>d</i> = 4: <i>f</i>({n}) = 4{n} + 3", frames=[f"<i>d</i> = [[4]] ; 7 − 4 = [[3]] → <i>f</i>({n}) = [[4]]{n} + [[3]]"],
                      lines=2),
                 MC("Which table shows a constant rate of change?",
                    [htable((x, [1, 2, 3, 4]), (y, [3, 6, 12, 24])), htable((x, [0, 2, 4, 6]), (y, [5, 8, 11, 14])),
                     htable((x, [1, 2, 4, 5]), (y, [2, 4, 6, 8])), htable((x, [0, 1, 2, 3]), (y, [1, 2, 4, 7]))], 1,
                    why="B: y goes up 3 every time x goes up 2 (rate 1.5). In C, x jumps by 2 once, so the rate changes."),
             ]),
        dict(title="3.4 Point-Slope Form", lesson="Lesson 4 · Getting Started, Activities 1–3, Talk the Talk ✪",
             idea=f"""<p><b>Point-slope form:</b> {y} − {sub('y', 1)} = <i>m</i>({x} − {sub('x', 1)}), for slope <i>m</i>
             and point ({sub('x', 1)}, {sub('y', 1)}). Watch the signs: the point (−4, 3) gives {y} − 3 = <i>m</i>({x} + 4).</p>
             <p>From two points: find <i>m</i> = (<i>y</i>₂ − <i>y</i>₁) ÷ (<i>x</i>₂ − <i>x</i>₁), then use either point.
             Distribute and solve for {y} to get <b>slope-intercept form</b> {y} = <i>mx</i> + <i>b</i>.</p>""",
             example=f"""<p><b>Slope {fr(2, 5)} through (5, −1):</b> {y} + 1 = {fr(2, 5)}({x} − 5) → {y} + 1 = {fr(2, 5)}{x} − 2
             → <b>{y} = {fr(2, 5)}{x} − 3</b>.</p>""",
             items=[
                 OPEN("Write the equation in slope-intercept form of the line through (2, 7) and (6, −1).",
                      f"m = (−1 − 7) ÷ (6 − 2) = −2; {y} − 7 = −2({x} − 2) → {y} = −2{x} + 11",
                      frames=["<i>m</i> = (−1 − 7) ÷ (6 − 2) = [[−8]] ÷ [[4]] = [[−2]]",
                              f"{y} − 7 = −2({x} − 2) → {y} − 7 = −2{x} + [[4]] → {y} = −2{x} + [[11]]"]),
                 MC(f"Which is an equation of the line with slope −½ through (−4, 3)?",
                    [f"{y} − 3 = −½({x} + 4)", f"{y} + 3 = −½({x} − 4)", f"{y} − 4 = −½({x} + 3)", f"{y} − 3 = ½({x} + 4)"], 0,
                    why="y − y₁ = m(x − x₁): y − 3 = −½(x − (−4)) = −½(x + 4).",
                    tip="The signs inside are the OPPOSITE of the point’s signs."),
                 OPEN(f"Write the equation in slope-intercept form of the line with slope {fr(3, 2)} through (−2, 5).",
                      f"{y} − 5 = {fr(3, 2)}({x} + 2) → {y} = {fr(3, 2)}{x} + 8",
                      frames=[f"{y} − 5 = {fr(3, 2)}({x} + 2) → {y} − 5 = {fr(3, 2)}{x} + [[3]] → {y} = {fr(3, 2)}{x} + [[8]]"]),
             ]),
        dict(title="3.5 Standard Form and Intercepts", lesson="Lesson 5 · Getting Started, Activities 1–4, Talk the Talk ✪",
             idea=f"""<p><b>Standard form:</b> <i>A</i>{x} + <i>B</i>{y} = <i>C</i>. To find the slope, solve for {y}
             (or use slope = −<i>A</i> ÷ <i>B</i>).</p><p><b>Intercepts:</b> put {y} = 0 to find the {x}-intercept; put
             {x} = 0 to find the {y}-intercept. In a story, they show “all of one thing, none of the other.”</p>""",
             example=f"""<p><b>6{x} + 2{y} = 18</b> → 2{y} = −6{x} + 18 → <b>{y} = −3{x} + 9</b>. Slope −3.</p>
             <p>{x}-intercept: 6{x} = 18 → (3, 0). &nbsp; {y}-intercept: 2{y} = 18 → (0, 9).</p>""",
             items=[
                 OPEN(f"What is the slope of the line 8{x} − 2{y} = 10?", "−2y = −8x + 10 → y = 4x − 5; slope 4",
                      frames=[f"−2{y} = [[−8]]{x} + 10 → {y} = [[4]]{x} − [[5]] → slope [[4]]"],
                      tip="Move the x-term to the other side, then divide EVERY term by the number in front of y.", lines=2),
                 OPEN(f"Find the {x}- and {y}-intercepts of 3{x} + 4{y} = 24.", "x-intercept (8, 0); y-intercept (0, 6)",
                      frames=["y = 0: 3x = 24 → x = [[8]] → ([[8]], 0)", "x = 0: 4y = 24 → y = [[6]] → (0, [[6]])"], lines=2),
                 OPEN(f"Ana has $60 to spend on notebooks ($4 each, {x}) and pens ($6 each, {y}): 4{x} + 6{y} = 60. "
                      f"What is the {x}-intercept, and what does it mean?",
                      "(15, 0): she can buy 15 notebooks if she buys 0 pens.",
                      frames=["4x = 60 → x = [[15]]. She can buy [[15]] notebooks and [[0]] pens."]),
             ]),
        dict(title="3.6 Meaning in Context: Slope, Intercepts, Domain", lesson="Lesson 6 · Getting Started, Activities 1–4, Talk the Talk ✪",
             idea=f"""<p>In a story: <b>slope</b> = rate (units of {y} per unit of {x}); <b>{y}-intercept</b> = the starting
             amount; <b>{x}-intercept</b> = when the amount reaches 0. <b>Domain</b> = the {x}-values that make sense:
             a list of whole numbers if you can only count (batches, people), an interval if you measure (time).</p>""",
             example=f"""<p>A car starts with 12 gallons of gas and uses 0.4 gallon per mile. Its graph goes from (0, 12)
             to (30, 0).</p><p>Slope −0.4: it uses 0.4 gallon each mile. &nbsp; (0, 12): it starts with 12 gallons.
             &nbsp; (30, 0): the tank is empty after 30 miles.</p>""",
             items=[
                 MC(f"For <i>f</i>({x}) = −4.5{x} + 1.8, find <i>f</i>(−2.4).", ["−12.6", "−9", "9", "12.6"], 3,
                    why="−4.5(−2.4) = 10.8 (negative × negative = positive); 10.8 + 1.8 = 12.6.",
                    tip="Negative times negative is positive."),
                 MC("Tara has 24 stickers. She gives 3 stickers to each friend until they are gone. What is the domain of "
                    "the function (number of friends → stickers left)?",
                    [f"0 {LE} {x} {LE} 8", "{0, 1, 2, 3, 4, 5, 6, 7, 8}", f"0 {LE} {y} {LE} 24", "{0, 3, 6, 9, 12, 15, 18, 21, 24}"], 1,
                    why="Friends are counted in whole numbers, 0 to 24 ÷ 3 = 8, so the domain is a list."),
                 OPEN(f"Leo’s savings are modeled by {y} = 25{x} + 150, where {x} is weeks. What do 25 and 150 mean?",
                      "25: he saves $25 each week. 150: he started with $150.",
                      frames=["25 means he saves $[[25]] each [[week]]. 150 means he started with $[[150]]."]),
             ]),
    ]

    diego = plot((0, 35, 2.5, 5), (0, 7, 0.5, 1), [dict(f=lambda t: 6 - 0.2 * t, a=0, b=30, ends=("closed", "closed"))],
                 xlab="Time (minutes)", ylab="Distance from Home (miles)")
    elev = plot((0, 50, 5, 10), (0, 140, 10, 20), [dict(f=lambda t: 120 - 3 * t, a=0, b=40, ends=("closed", "closed"))],
                xlab="Time (seconds)", ylab="Height (feet)")
    check = [
        MC("The table shows visits to a town library. Which linear function best models the data if <i>x</i> is the "
           "number of years since 2020?" + htable(("Year", [2020, 2021, 2022, 2023, 2024]), ("Visits", [f"{v:,}" for v in lib_y])),
           [eq(lb, lm), eq(round((2640 - 2150) / 4, 2), 2150), eq(lm, lb), eq(lm, 2020)], 2,
           why=f"LinReg (x = 0 to 4): y = {nm(lm)}x + {nm(lb)}."),
        MC("The table shows what a tutor earns. Based on a line of best fit, what is the best prediction for 9 hours?"
           + htable(("Hours", tu_x), ("Earnings ($)", tu_y)),
           [f"${nm(ts * 9, True)}", f"${nm(pred, True)}", "$121.00", f"${nm(ts * 2, True)}"], 1,
           why=f"LinReg: y ≈ {nm(round(ts, 4))}x + {nm(round(tb, 4))}; at x = 9 → ≈ ${nm(pred, True)}."),
        ROWS("Is each pair causation, or only correlation?", ["Causation", "Correlation only"],
             [("Pressing the brake pedal and the car slowing down", 0), ("Umbrella sales and the number of colds", 1),
              ("Hours a heater runs and the room temperature", 0), ("Shoe size and reading level of students", 1)],
           why="Pressing the brake makes the car slow down. The others happen together, but one doesn’t cause the other."),
        MC("What does the correlation coefficient for this data indicate?" + htable(("Week", wk_x), ("Rainfall (in.)", wk_y)),
           ["Strong positive correlation", "Weak negative correlation", "Strong negative correlation",
            "Weak positive correlation"], 3,
           why=f"r ≈ {nm(round(correlation(wk_x, wk_y), 2))}: positive but far from 1, so weak."),
        MC("Which value of <i>r</i> best fits the scatter plot?", ["−0.98", "−0.30", "0.30", "0.98"], 0,
           fig=plot((0, 9, 1, 1), (0, 20, 1, 2), pts=list(zip(sp_x, sp_y))),
           why="The points fall steadily and lie close to a line: strong negative, close to −1."),
        OPEN("A food truck tracks its profit. Determine the rate of change. Include units."
             + htable(("Burgers sold", [20, 25, 30, 40]), ("Profit ($)", ["−35", "−10", 15, 65])),
             "(−10 − (−35)) ÷ (25 − 20) = 25 ÷ 5 = 5 dollars per burger",
             frames=["(−10 − (−35)) ÷ (25 − 20) = [[25]] ÷ [[5]] = [[5]] [[dollars]] per [[burger]]"]),
        OPEN("The graph shows an elevator going down. Determine the rate of change and explain what it means.",
             "(0 − 120) ÷ (40 − 0) = −3: the elevator goes down 3 feet each second.", fig=elev,
             frames=["Points (0, [[120]]) and ([[40]], 0): (0 − 120) ÷ 40 = [[−3]]",
                     "The elevator goes [[down]] [[3]] feet each second."]),
        OPEN("The table shows the water in a rain barrel. Write a linear function for <i>y</i>, the gallons, in terms of "
             "<i>x</i>, the weeks since June 1." + htable(("Week", [0, 1, 2, 3, 4]), ("Gallons", [f"{1200 - 85 * k:,}" for k in range(5)])),
             f"{y} = −85{x} + 1,200", frames=[f"Rate: 1,115 − 1,200 = [[−85]] per week ; start: [[1,200]] → {y} = [[−85]]{x} + [[1,200]]"]),
        OPEN("A candle is 18 cm tall and burns 1.5 cm each hour. Write a linear function for its height <i>y</i> after "
             "<i>x</i> hours. When does it burn out?", f"{y} = −1.5{x} + 18; 18 ÷ 1.5 = 12 hours",
             frames=[f"{y} = [[−1.5]]{x} + [[18]]", "0 = −1.5x + 18 → x = [[12]] hours"]),
        OPEN(f"What is the slope of the line −6{x} + 2{y} = 14? Enter your answer.", "2y = 6x + 14 → y = 3x + 7; slope 3",
             frames=[f"2{y} = [[6]]{x} + 14 → {y} = [[3]]{x} + [[7]] → slope [[3]]"], lines=1, fmt="Text entry"),
        OPEN(f"A line has slope −{fr(3, 4)} and goes through (8, −2). Write it as {y} = <i>mx</i> + <i>b</i>.",
             f"{y} + 2 = −¾({x} − 8) → {y} = −¾{x} + 4",
             frames=[f"{y} + 2 = −{fr(3, 4)}({x} − 8) → {y} + 2 = −{fr(3, 4)}{x} + [[6]] → {y} = −{fr(3, 4)}{x} + [[4]]"]),
        OPEN("Write the line through (−3, 4) and (3, 8) in the form <i>y</i> = <i>mx</i> + <i>b</i>.",
             f"m = 4/6 = ⅔; {y} − 8 = ⅔({x} − 3) → {y} = ⅔{x} + 6",
             frames=["<i>m</i> = (8 − 4) ÷ (3 − (−3)) = [[4]] ÷ [[6]] = [[⅔]]", f"{y} − 8 = ⅔({x} − 3) → {y} = ⅔{x} + [[6]]"]),
        OPEN("A phone battery drains at a constant rate. Determine the rate of change and interpret it."
             + htable(("Hours", [0, 1.5, 3, 4]), ("Battery (%)", [96, 78, 60, 48])),
             "(78 − 96) ÷ 1.5 = −12: the battery loses 12% each hour.",
             frames=["(78 − 96) ÷ (1.5 − 0) = [[−18]] ÷ 1.5 = [[−12]]", "The battery loses [[12]]% each [[hour]]."]),
        OPEN("The graph shows Diego’s bike ride home.<br>a. Identify the <i>y</i>-intercept and its meaning.<br>"
             "b. Identify the <i>x</i>-intercept and its meaning.<br>c. Calculate the slope and explain its meaning.",
             "a. (0, 6): he starts 6 miles from home. b. (30, 0): he gets home after 30 minutes. "
             "c. −6 ÷ 30 = −0.2: he gets 0.2 mile closer to home each minute.", fig=diego, lines=4,
             frames=["a. (0, [[6]]): he starts [[6]] miles from home.", "b. ([[30]], 0): he is home after [[30]] minutes.",
                     "c. (0 − 6) ÷ (30 − 0) = [[−0.2]]: he gets [[0.2]] mile closer each minute."]),
        OPEN(f"A plumber’s charge is {y} = 55{x} + 80, where {x} is hours. What do 55 and 80 mean?",
             "55: $55 for each hour of work. 80: an $80 charge to come out (at 0 hours).",
             frames=["55 means $[[55]] per [[hour]]. 80 means $[[80]] at [[0]] hours (the visit fee)."]),
        MC(f"Evaluate <i>f</i>(−1.5) when <i>f</i>({x}) = −3.6{x} + 4.2.", ["−9.6", "−1.2", "1.2", "9.6"], 3,
           why="−3.6(−1.5) = 5.4; 5.4 + 4.2 = 9.6."),
        MC("Jamal has 30 trading cards. He sells 5 cards each week until they are gone. What is the domain of the "
           "function (weeks → cards left)?",
           ["{0, 5, 10, 15, 20, 25, 30}", f"0 {LE} {x} {LE} 6", "{0, 1, 2, 3, 4, 5, 6}", f"0 {LE} {y} {LE} 30"], 2,
           why="Weeks are whole numbers from 0 to 30 ÷ 5 = 6. A is the range."),
    ]
    assert 6 - 0.2 * 30 == 0 and (6 - (-12)) / 4 == 4.5 and (78 - 96) / 1.5 == -12
    staar = [
        MC("The table shows a linear relationship. What is the rate of change of <i>y</i> with respect to <i>x</i>?"
           + htable((x, [-4, 0, 6, 10]), (y, [13, 11, 8, 6])), ["−2", "−½", "½", "2"], 1, teks="A.3(B)",
           why="(11 − 13) ÷ (0 − (−4)) = −2 ÷ 4 = −½."),
        MC("Which equation represents the line through (0, −5) and (4, 3)?",
           [f"{y} = 2{x} − 5", f"{y} = −5{x} + 2", f"{y} = ½{x} − 5", f"{y} = 2{x} + 3"], 0, teks="A.2(C)",
           why="m = (3 − (−5)) ÷ 4 = 2; y-intercept −5."),
        OPEN("What is the slope of the line through (−7, 2) and (1, −10)? Enter your answer.", "(−10 − 2) ÷ (1 + 7) = −1.5",
             teks="A.3(A)", fmt="Text entry", lines=1, frames=["(−10 − 2) ÷ (1 − (−7)) = [[−12]] ÷ [[8]] = [[−1.5]]"]),
        MC("A line of best fit for gas used <i>y</i> (gallons) and miles driven <i>x</i> is <i>y</i> = 0.035<i>x</i> + 0.2. "
           "Predict the gas used for 300 miles.", ["10.5 gallons", "10.7 gallons", "11.5 gallons", "60.2 gallons"], 1,
           teks="A.4(C)", why="0.035(300) + 0.2 = 10.5 + 0.2 = 10.7."),
        MC(f"Which equations represent the same line as {y} − 5 = 2({x} − 1)? Select <b>TWO</b> correct answers.",
           [f"{y} = 2{x} + 3", f"{y} = 2{x} + 4", f"2{x} − {y} = −3", f"{y} = 2{x} − 1", f"2{x} + {y} = 3"], (0, 2),
           teks="A.2(B)", why="y − 5 = 2x − 2 → y = 2x + 3 → 2x − y = −3."),
        OPEN(f"Choose the words that complete the sentence.<br>The graph of {y} = −2{x} + 3 ( rises / falls ) from left "
             "to right and crosses the <i>y</i>-axis at ( 3 / −2 ).", "falls · 3", teks="A.3(C)", fmt="Inline choice",
             lines=1, frames=["The slope is [[−2]] (negative), so it [[falls]]. The y-intercept is [[3]]."]),
    ]
    vocab = [("line of best fit", "the line that comes closest to all the data points (linear regression)"),
             ("correlation coefficient r", "a number from −1 to 1 that tells the direction and strength of a linear pattern"),
             ("causation", "one thing actually makes another thing happen"),
             ("rate of change", "change in y ÷ change in x, with units (the slope)"),
             ("point-slope form", "y − y₁ = m(x − x₁)"),
             ("standard form", "Ax + By = C"),
             ("x-intercept / zero", "where y = 0: the point where the line crosses the x-axis")]
    return dict(code="M2 T1", title="Linear Functions", module="Module 2: Exploring Constant Change",
                teks="A.2A–D, A.3A–C, A.3E, A.4A–C, A.12A, A.12D", vocab=vocab, sections=sections, check=check, staar=staar)


# =====================================================================================================
# MODULE 2 · TOPIC 2 · Transforming and Comparing Linear Functions
# =====================================================================================================
def ch4():
    G = (-8, 8, 1, 2)
    fx = dict(f=lambda t: t, a=-8, b=8, label="f(x)")

    def graph_it(f, a=-8, b=8):  # f(x) = x printed; g drawn in red on a key only
        return lambda: plot(G, G, [fx] + ([dict(f=f, a=a, b=b, color=RED, label="g(x)")] if KEY else []))

    sections = [
        dict(title="4.1 Vertical Translations and Dilations", lesson="Lesson 1 · Getting Started, Activities 1–4 ✪",
             idea=f"""<p>Start with <i>f</i>({x}) = {x}. &nbsp; <b><i>f</i>({x}) + <i>d</i></b>: shift up <i>d</i>
             (down if <i>d</i> is negative). &nbsp; <b><i>a</i> · <i>f</i>({x})</b>: multiplies every {y}-value by <i>a</i>:
             steeper if |<i>a</i>| &gt; 1, flatter if 0 &lt; |<i>a</i>| &lt; 1, flipped over the {x}-axis if <i>a</i> &lt; 0.</p>
             <p>For a line through the origin, <i>a</i> is the slope: pick any point and divide {y} by {x}.</p>""",
             example=f"""<p><i>g</i>({x}) = 3<i>f</i>({x}) = 3{x}: slope 3, steeper. &nbsp; <i>h</i>({x}) = <i>f</i>({x}) − 4 = {x} − 4:
             down 4. &nbsp; <i>k</i>({x}) = −½<i>f</i>({x}): flipped and flatter (slope −½).</p>""",
             items=[
                 OPEN(f"The line shown is a vertical stretch or flip of <i>f</i>({x}) = {x}, so its equation is {y} = <i>a</i>{x}. "
                      "Use a point on the line to find <i>a</i>.", "a = −6 ÷ 4 = −1.5 (from the point (4, −6))",
                      fig=plot(G, G, [dict(f=lambda t: -1.5 * t, a=-8, b=8)], pts=[(-4, 6, "(−4, 6)"), (4, -6, "(4, −6)")]),
                      frames=["a = y ÷ x = −6 ÷ 4 = [[−1.5]]"], tip="Pick a labeled point. Divide its y by its x.", lines=1),
                 MC(f"<i>f</i>({x}) = 2{x} + 1 and <i>g</i>({x}) = <i>f</i>({x}) − 5. How is the graph of <i>g</i> related to <i>f</i>?",
                    ["Translated up 5 units", "Translated down 5 units", "Translated right 5 units", "Translated left 5 units"], 1,
                    why="Subtracting 5 OUTSIDE f lowers every y-value by 5."),
                 OPEN(f"<i>f</i>({x}) = {x} and <i>g</i>({x}) = 4<i>f</i>({x}) − 2. What are the slope and <i>y</i>-intercept of <i>g</i>?",
                      "g(x) = 4x − 2: slope 4, y-intercept (0, −2)",
                      frames=[f"<i>g</i>({x}) = 4({x}) − 2 → slope [[4]], y-intercept (0, [[−2]])"], lines=1),
             ]),
        dict(title="4.2 Horizontal Translations and Dilations", lesson="Lesson 2 · Getting Started, Activities 1–3 ✪",
             idea=f"""<p><b><i>f</i>({x} − <i>h</i>)</b>: shift <b>right</b> <i>h</i>. &nbsp; <b><i>f</i>({x} + <i>h</i>)</b>:
             shift <b>left</b> <i>h</i>. Inside the parentheses, the direction is the opposite of the sign.</p>
             <p><b><i>f</i>(<i>b</i>{x})</b> multiplies the inputs; for <i>f</i>({x}) = {x} it gives slope <i>b</i>.
             To translate a <b>table</b> right 2, add 2 to every {x}-value (the {y}-values stay).</p>""",
             example=f"""<p><i>f</i>({x}) = 2{x} − 1, <i>g</i>({x}) = <i>f</i>({x} − 3) = 2({x} − 3) − 1 = <b>2{x} − 7</b>: right 3.</p>""",
             items=[
                 MC(f"How is the graph of <i>h</i>({x}) = <i>f</i>({x} − 4) related to the graph of <i>f</i>?",
                    ["Right 4 units", "Left 4 units", "Up 4 units", "Down 4 units"], 0,
                    why="x − 4 inside → right 4.", tip="Inside the ( ): minus → right, plus → left."),
                 OPEN("Shift the function in the table 2 units to the left. Where does the new graph cross the <i>y</i>-axis?" + htable((x, [-1, 0, 1, 2, 3]), ("<i>f</i>(<i>x</i>)", [8, 5, 2, "−1", "−4"])),
                      "Every x-value goes down 2: (2, −1) moves to (0, −1). The y-intercept is (0, −1).",
                      frames=["Left 2: subtract [[2]] from each x. The point (2, −1) moves to ([[0]], [[−1]]).",
                              "The new y-intercept is (0, [[−1]])."]),
                 OPEN(f"<i>f</i>({x}) = {x}. Graph <i>g</i>({x}) = <i>f</i>(½{x}).", "g(x) = ½x: a line through (0, 0) and (4, 2).",
                      fig=graph_it(lambda t: t / 2), frames=["<i>g</i>(x) = ½x. Plot (0, 0), (2, [[1]]), (4, [[2]]) and connect."],
                      fmt="Graphing", lines=0),
             ]),
        dict(title="4.3 Parallel, Perpendicular, Horizontal and Vertical Lines", lesson="Lesson 3 · Activities 1–3 ✪",
             idea=f"""<p><b>Parallel</b> lines have the <b>same slope</b>. <b>Perpendicular</b> lines have
             <b>opposite reciprocal</b> slopes (flip the fraction, change the sign): ⅔ and −{fr(3, 2)}.</p>
             <p><b>Horizontal</b> line: {y} = <i>k</i>, slope <b>0</b>. &nbsp; <b>Vertical</b> line: {x} = <i>h</i>, slope
             <b>undefined</b>. Write the new line with point-slope form, then simplify.</p>""",
             example=f"""<p><b>Perpendicular to {y} = ¾{x} − 2 through (6, 1):</b> slope −{fr(4, 3)}. {y} − 1 = −{fr(4, 3)}({x} − 6)
             → {y} − 1 = −{fr(4, 3)}{x} + 8 → <b>{y} = −{fr(4, 3)}{x} + 9</b>.</p>""",
             items=[
                 OPEN(f"Write the equation of the line parallel to {y} = −2.5{x} + 4 through (2, 3).",
                      f"{y} − 3 = −2.5({x} − 2) → {y} = −2.5{x} + 8",
                      frames=[f"Same slope: [[−2.5]]. {y} − 3 = −2.5({x} − 2) → {y} = −2.5{x} + [[8]]"]),
                 OPEN(f"Write the equation of the line perpendicular to {y} = 5{x} + 1 through (10, −4).",
                      f"slope −⅕: {y} + 4 = −⅕({x} − 10) → {y} = −⅕{x} − 2",
                      frames=["Opposite reciprocal of 5: [[−⅕]]", f"{y} + 4 = −⅕({x} − 10) → {y} + 4 = −⅕{x} + [[2]] → {y} = −⅕{x} − [[2]]"]),
                 ROWS("Are the lines parallel, perpendicular, or neither?", ["Parallel", "Perpendicular", "Neither"],
                      [(f"{y} = 3{x} + 1 and {y} = 3{x} − 4", 0), (f"{y} = ⅔{x} and {y} = −{fr(3, 2)}{x} + 5", 1),
                       (f"{y} = 2{x} and {y} = −2{x}", 2), (f"{y} = 4 and {x} = −1", 1)],
                      why="Same slope → parallel. 2 and −2 are opposites but not reciprocals → neither. Horizontal ⟂ vertical.",
                      tip="Multiply the two slopes. If you get −1, they are perpendicular."),
             ]),
        dict(title="4.4 Comparing Functions and Domain in Context", lesson="Lessons 1–2 · Talk the Talk ✪ (applying)",
             idea=f"""<p>To <b>compare</b> two linear functions in different forms (table, graph, equation, story), find
             each one’s slope and {y}-intercept, then compare.</p><p>When a story has a <b>limit</b> (“at most 8 hours”),
             the domain is an interval. Plug the smallest and largest {x} into the function to get the range.</p>""",
             example=f"""<p>A plumber charges $75 plus $50 an hour, up to 8 hours. Domain 0 {LE} {x} {LE} 8.
             Range: 75 + 50(0) = 75 to 75 + 50(8) = 475, so <b>75 {LE} {y} {LE} 475</b>.</p>""",
             items=[
                 MC("A bounce-house rental costs $60 plus $35 per hour, for up to 5 hours. What is the range for one rental?",
                    [f"60 {LE} {y} {LE} 235", f"35 {LE} {y} {LE} 175", f"0 {LE} {x} {LE} 5", f"60 {LE} {y} {LE} 300"], 0,
                    why="60 + 35(0) = 60 and 60 + 35(5) = 235."),
                 OPEN("Function A is shown in the table. Function B is <i>y</i> = 2.5<i>x</i> + 7. Which has the greater rate "
                      "of change? Which has the greater <i>y</i>-intercept?" + htable((x, [0, 2, 4]), (y, [5, 11, 17])),
                      "A: rate 3, y-int 5. B: rate 2.5, y-int 7. A has the greater rate; B has the greater y-intercept.",
                      frames=["A: rate (11 − 5) ÷ 2 = [[3]], y-intercept [[5]]", "B: rate [[2.5]], y-intercept [[7]]",
                              "Greater rate: [[A]] · Greater y-intercept: [[B]]"]),
             ]),
    ]

    check = [
        OPEN(f"The parent function <i>f</i>({x}) = {x} was transformed into the line shown, which still goes through the origin. "
             "What number <i>a</i> was {x} multiplied by?", "a = 4 ÷ (−6) = −⅔",
             fig=plot(G, G, [dict(f=lambda t: -2 * t / 3, a=-8, b=8)], pts=[(-6, 4, "(−6, 4)"), (3, -2, "(3, −2)")]),
             frames=["a = y ÷ x = −2 ÷ 3 = [[−⅔]]"], lines=1),
        MC("A photographer charges $150 plus $40 per hour and works at most 5 hours at an event. What is the range of the "
           "function for one event?", [f"0 {LE} {x} {LE} 5", f"40 {LE} {y} {LE} 200", f"150 {LE} {y} {LE} 350",
                                       f"0 {LE} {x} {LE} 150"], 2, why="150 + 40(0) = 150 and 150 + 40(5) = 350. A is the domain."),
        MC("Name the line on the grid and give its slope.",
           [f"{y} = −15; slope is 0", f"{x} = −15; slope is undefined", f"{x} = −15; slope is 0", f"{y} = −15; slope is undefined"], 1,
           fig=plot((-40, 40, 5, 10), (-40, 40, 5, 10), [dict(xy=[(-15, -40), (-15, 40)])]),
           why="A vertical line: every point has x = −15. Vertical lines have undefined slope.",
           tip="Vertical line → x = number, undefined slope. Horizontal → y = number, slope 0."),
        MC(f"Jordan graphed <i>f</i>({x}) and <i>g</i>({x}) = <i>f</i>({x} − 6). Which statement is true?",
           ["g is f translated up 6 units.", "g is f translated left 6 units.", "g is f translated right 6 units.",
            "g is f translated down 6 units."], 2, why="x − 6 inside the function → right 6."),
        MC(f"<i>g</i>({x}) = <i>f</i>({x}) + 2.5. Which statement describes the graph of <i>g</i>?",
           ["f moved up 2.5 units", "f moved right 2.5 units", "f made 2.5 times steeper", "f moved left 2.5 units"], 0,
           why="Adding outside the function moves the graph up."),
        OPEN("The table shows <i>f</i>. Slide its graph 3 units to the left. What is the new <i>y</i>-intercept?"
             + htable((x, [1, 2, 3, 4, 5]), ("<i>f</i>(<i>x</i>)", ["−6", "−2", 2, 6, 10])),
             "(3, 2) moves to (0, 2): the y-intercept is (0, 2).",
             frames=["Left 3: the point (3, 2) moves to ([[0]], [[2]]). The y-intercept is (0, [[2]])."]),
        OPEN(f"<i>f</i>({x}) = {x}. Graph <i>g</i>({x}) = −2<i>f</i>({x}).", "g(x) = −2x: through (0, 0), (1, −2), (−2, 4).",
             fig=graph_it(lambda t: -2 * t, -4, 4), frames=["<i>g</i>(x) = [[−2]]x. Plot (0, 0), (1, [[−2]]), (−2, [[4]])."],
             fmt="Graphing", lines=0),
        OPEN(f"A line is perpendicular to {y} = {fr(4, 5)}{x} − 1 and has an <i>x</i>-intercept of −8. Write it in slope-intercept form.",
             f"slope −{fr(5, 4)} through (−8, 0): {y} = −{fr(5, 4)}{x} − 10",
             frames=[f"Slope: [[−{fr(5, 4)}]] · Point: ([[−8]], 0)", f"0 = −{fr(5, 4)}(−8) + <i>b</i> → 0 = [[10]] + <i>b</i> → <i>b</i> = [[−10]]"]),
        OPEN(f"Write the line parallel to {y} = −1.6{x} + 2 that goes through (5, 1), in slope-intercept form.",
             f"{y} = −1.6{x} + 9", frames=["1 = −1.6(5) + <i>b</i> → 1 = [[−8]] + <i>b</i> → <i>b</i> = [[9]]"]),
        OPEN("Use two labeled points to write the line in point-slope form.", f"m = 6/9 = ⅔; {y} − 5 = ⅔({x} − 3) (or {y} + 1 = ⅔({x} + 6))",
             fig=plot(G, G, [dict(f=lambda t: 2 * t / 3 + 3, a=-8, b=8)], pts=[(-6, -1, "(−6, −1)"), (3, 5, "(3, 5)")]),
             frames=["<i>m</i> = (5 − (−1)) ÷ (3 − (−6)) = [[6]] ÷ [[9]] = [[⅔]]", f"{y} − [[5]] = ⅔({x} − [[3]])"]),
        MC("Which statements about this line are true? Select <b>TWO</b> correct answers.",
           ["The graph is decreasing.", "The slope of the line is ½.", "The y-intercept is (0, 3).", "The zero of the function is 6.",
            "The zero of the function is −3."], (1, 3),
           fig=plot(G, G, [dict(f=lambda t: t / 2 - 3, a=-8, b=8)]),
           why="It rises 1 for every 2 right (slope ½), crosses the y-axis at (0, −3) and the x-axis at 6."),
        MC(f"How does the graph of <i>g</i>({x}) = 5<i>f</i>({x}) compare to <i>f</i>({x}) = {x}?",
           ["It is 5 units higher.", "It is steeper.", "It is flatter.", "It is flipped over the x-axis."], 1,
           why="Multiplying by 5 makes the slope 5: steeper. (+5 would move it up.)"),
        ROWS("Are the lines parallel, perpendicular, or neither?", ["Parallel", "Perpendicular", "Neither"],
             [(f"2{x} + {y} = 3 and {y} = ½{x} + 1", 1), (f"{x} − 3{y} = 6 and {y} = ⅓{x} − 5", 0), (f"{y} = −4{x} and {y} = 4{x} + 1", 2)],
             why="2x + y = 3 → y = −2x + 3 (−2 · ½ = −1). x − 3y = 6 → y = ⅓x − 2 (same slope).",
             tip="Solve each standard-form equation for y first."),
        OPEN("A pool starts with 1,000 gallons and fills at 400 gallons per hour until it holds 9,000 gallons. Write the "
             "domain and range.", f"Domain 0 {LE} {x} {LE} 20 hours · Range 1,000 {LE} {y} {LE} 9,000 gallons",
             frames=["(9,000 − 1,000) ÷ 400 = [[20]] hours", f"Domain: 0 ≤ {x} ≤ [[20]] · Range: [[1,000]] ≤ {y} ≤ [[9,000]]"]),
        OPEN(f"Function A: {y} = −3{x} + 2. Function B goes through (0, 6) and (2, 0). Which has the greater <i>y</i>-intercept? "
             "Which is steeper?", "A: slope −3, y-int 2. B: slope −3, y-int 6. B has the greater y-intercept; they are equally steep.",
             frames=["B: slope (0 − 6) ÷ 2 = [[−3]], y-intercept [[6]]", "Greater y-intercept: [[B]] · Steeper: [[same]]"]),
    ]
    assert 0 == -5 / 4 * -8 - 10 and 1 == -1.6 * 5 + 9 and (9000 - 1000) / 400 == 20
    staar = [
        MC(f"<i>f</i>({x}) = {x} and <i>g</i>({x}) = <i>f</i>({x}) − 6. Which describes the graph of <i>g</i>?",
           ["The graph of f shifted down 6 units", "The graph of f shifted up 6 units", "The graph of f shifted left 6 units",
            "The graph of f is 6 times steeper"], 0, teks="A.3(E)"),
        MC(f"How does the graph of {y} = −3{x} compare to the graph of {y} = {x}?",
           ["Steeper and flipped over the x-axis", "Flatter and flipped over the x-axis", "Steeper, not flipped",
            "Shifted down 3 units"], 0, teks="A.3(E)", why="|−3| > 1 → steeper; negative → flipped."),
        MC(f"Which line is parallel to {y} = −⅓{x} + 7 and passes through (6, 0)?",
           [f"{y} = 3{x} − 18", f"{y} = −⅓{x} + 2", f"{y} = −⅓{x} − 2", f"{y} = −⅓{x} + 6"], 1, teks="A.2(E), A.2(F)",
           why="Same slope −⅓: 0 = −⅓(6) + b → b = 2."),
        OPEN(f"What is the slope of a line perpendicular to 3{x} − 6{y} = 12? Enter your answer.",
             "3x − 6y = 12 → y = ½x − 2 → perpendicular slope −2", teks="A.2(G)", fmt="Text entry", lines=1,
             frames=[f"{y} = [[½]]{x} − 2 → perpendicular slope [[−2]]"]),
        MC("Which is the equation of the vertical line through (4, −9)?", [f"{y} = −9", f"{x} = 4", f"{y} = 4", f"{x} = −9"], 1,
           teks="A.2(G)", why="Vertical lines are x = number; every point has x = 4."),
        MC(f"<i>f</i>({x}) = 2{x} + 1. Which functions have a <i>y</i>-intercept of 4? Select <b>TWO</b> correct answers.",
           [f"<i>f</i>({x}) + 3", f"<i>f</i>({x} + 1.5)", f"<i>f</i>({x}) − 3", f"3<i>f</i>({x})", f"<i>f</i>({x} − 1.5)"], (0, 1),
           teks="A.3(E)", why="f(x) + 3 = 2x + 4; f(x + 1.5) = 2x + 3 + 1 = 2x + 4. 3f(x) = 6x + 3."),
    ]
    vocab = [("translation", "a slide: up/down (f(x) + d) or left/right (f(x − h))"),
             ("vertical dilation", "a · f(x): stretches or shrinks the graph; a < 0 also flips it"),
             ("parallel lines", "same slope, never meet"),
             ("perpendicular lines", "opposite reciprocal slopes, meet at a right angle"),
             ("horizontal / vertical line", "y = k (slope 0) / x = h (slope undefined)"),
             ("zero of a function", "the x-value where f(x) = 0 (the x-intercept)")]
    return dict(code="M2 T2", title="Transforming and Comparing Linear Functions", module="Module 2: Exploring Constant Change",
                teks="A.2A, A.2C, A.2E–G, A.3C, A.3E", vocab=vocab, sections=sections, check=check, staar=staar)


# =====================================================================================================
# MODULE 3 · TOPIC 1 · Linear Equations and Inequalities
# =====================================================================================================
def ch5():
    def nl_it(lo, hi, pt, closed, left):  # graph-it number line: the solution ray is drawn on a key only
        return lambda: numline(lo, hi, *((pt, closed, left, RED) if KEY else ()))

    # self-checks for every solved equation / inequality below
    assert 5 - 3 * (2 - 2) == 2 * (2 + 4) - 7 and abs(0.6 * (4 * -7.5 + 5) - (1.2 * -7.5 - 6)) < 1e-9
    assert 10 - 4 * (8 + 2) == 6 - 3 * (2 * 8 - 4) and abs(0.5 * (6 * 2 + 8) - (-1.5 * 2 + 13)) < 1e-9
    assert 5 * (18 + 2) == 4 * (18 + 7)  # triangle area = rectangle area at x = 18
    sections = [
        dict(title="5.1 Solving Linear Equations", lesson="Lesson 1 · Getting Started, Activities 1–2 ✪",
             idea=f"""<p><b>Steps:</b> (1) distribute, (2) combine like terms on each side, (3) move the variable terms to one
             side, (4) undo + and −, then × and ÷. Check by substituting.</p>
             <p><b>How many solutions?</b> If the variables cancel and you get a <b>true</b> statement (5 = 5), there are
             <b>infinitely many</b> solutions. A <b>false</b> statement (1 = 5) means <b>no solution</b>. Otherwise,
             <b>one solution</b>.</p><p>Decimals: work them like whole numbers, or multiply every term by 10 first.</p>""",
             example=f"""<p><b>3(2{x} − 5) = 4{x} + 7</b> → 6{x} − 15 = 4{x} + 7 → 2{x} = 22 → <b>{x} = 11</b>.
             Check: 3(22 − 5) = 51 and 44 + 7 = 51 ✓.</p>
             <p>2({x} + 3) = 2{x} + 6 → 6 = 6: infinitely many. &nbsp; 2{x} + 1 = 2{x} + 5 → 1 = 5: no solution.</p>""",
             items=[
                 MC("What value of <i>k</i> makes 5 − 3(<i>k</i> − 2) = 2(<i>k</i> + 4) − 7 true?", ["−2", "2", "4", "No solution"], 1,
                    why="5 − 3k + 6 = 2k + 8 − 7 → 11 − 3k = 2k + 1 → 10 = 5k → k = 2.",
                    tip="Distribute the −3 to BOTH terms: −3 · k and −3 · (−2) = +6."),
                 OPEN(f"Solve 0.6(4{x} + 5) = 1.2{x} − 6.", "2.4x + 3 = 1.2x − 6 → 1.2x = −9 → x = −7.5",
                      frames=[f"[[2.4]]{x} + [[3]] = 1.2{x} − 6", f"[[1.2]]{x} = [[−9]] → {x} = [[−7.5]]"]),
                 ROWS("How many solutions does each equation have?", ["One", "None", "Infinitely many"],
                      [(f"4({x} − 1) = 4{x} − 4", 2), (f"3{x} + 2 = 3({x} + 1)", 1), (f"½(8{x} − 6) = 2{x} + 5", 0)],
                      why="4x − 4 = 4x − 4 (true always); 3x + 2 = 3x + 3 → 2 = 3 (false); 4x − 3 = 2x + 5 → x = 4.",
                      tip="Simplify both sides. Same on both sides → infinitely many. Only the numbers differ → none."),
                 MC("Marco has $35. He earns $15 for each lawn he mows. Which equation gives the money he has, <i>y</i>, "
                    "after mowing <i>x</i> lawns?", [eq(35, 15), eq(15, 35), eq(-15, 35), eq(15, -35)], 1,
                    why="The $15 per lawn is the rate (with x); the $35 he starts with is the constant."),
             ]),
        dict(title="5.2 Literal Equations and Rewriting Forms", lesson="Lesson 2 · Getting Started, Activities 1–3, Talk the Talk ✪",
             idea=f"""<p>A <b>literal equation</b> has several letters, like a formula. To solve for one letter, treat the
             other letters as numbers and undo the operations around it.</p>
             <p>To get <b>slope-intercept form</b>, solve for {y}: from standard form, move the {x}-term and divide; from
             point-slope form, distribute and add or subtract.</p>""",
             example=f"""<p><b>A = ½<i>bh</i>, solve for <i>h</i>:</b> 2A = <i>bh</i> → <b><i>h</i> = {fr('2A', '<i>b</i>')}</b>.</p>
             <p><b>4{x} − 2{y} = 10</b> → −2{y} = −4{x} + 10 → <b>{y} = 2{x} − 5</b>.</p>""",
             items=[
                 OPEN("The perimeter of a rectangle is <i>P</i> = 2<i>l</i> + 2<i>w</i>. Solve for <i>w</i>.",
                      f"<i>w</i> = {fr('<i>P</i> − 2<i>l</i>', 2)}",
                      frames=["<i>P</i> − [[2<i>l</i>]] = 2<i>w</i> → <i>w</i> = (<i>P</i> − 2<i>l</i>) ÷ [[2]]"],
                      tip="Subtract 2l from both sides first. Then divide both sides by 2.", lines=2),
                 OPEN(f"Rewrite 7{x} + 2{y} = 12 in slope-intercept form.", f"2y = −7x + 12 → y = −3.5x + 6",
                      frames=[f"2{y} = [[−7]]{x} + 12 → {y} = [[−3.5]]{x} + [[6]]"], lines=2),
                 OPEN(f"Rewrite {y} + 4 = −3({x} − 2) in slope-intercept form.", "y + 4 = −3x + 6 → y = −3x + 2",
                      frames=[f"{y} + 4 = −3{x} + [[6]] → {y} = −3{x} + [[2]]"], lines=2),
                 MC("The volume of a box is <i>V</i> = <i>lwh</i>. Which equation is solved for <i>h</i>?",
                    [f"<i>h</i> = <i>V</i> − <i>lw</i>", f"<i>h</i> = {fr('<i>V</i>', '<i>lw</i>')}", f"<i>h</i> = <i>Vlw</i>",
                     f"<i>h</i> = {fr('<i>lw</i>', '<i>V</i>')}"], 1, why="h is multiplied by lw, so divide both sides by lw."),
             ]),
        dict(title="5.3 Linear Inequalities", lesson="Lesson 3 · Getting Started, Activities 1–4, Talk the Talk ✪",
             idea=f"""<p>Solve an inequality like an equation, with one rule: when you <b>multiply or divide by a negative</b>,
             <b>flip</b> the inequality sign.</p><p>Number line: <b>closed dot</b> for {LE} or {GE} (included), <b>open
             dot</b> for &lt; or &gt;. Shade toward the solutions. Story words: “at most” {LE}, “at least” {GE},
             “more than” &gt;, “less than” &lt;.</p>""",
             example=f"""<p><b>−2({x} + 3) {GE} 10</b> → −2{x} − 6 {GE} 10 → −2{x} {GE} 16 → <b>{x} {LE} −8</b> (divided by −2: flip!).</p>
             {numline(-12, 0, -8, True, True)}""",
             items=[
                 MC("What is the solution set for 3(4 − <i>t</i>) &lt; −2<i>t</i> + 5?",
                    ["<i>t</i> &gt; 7", "<i>t</i> &lt; 7", "<i>t</i> &gt; −7", f"<i>t</i> {LE} 7"], 0,
                    why="12 − 3t < −2t + 5 → 7 < t, so t > 7.", tip="Move the t-terms to the side where t stays positive."),
                 OPEN("Solve 2.5<i>m</i> + 4 ≥ 0.5(<i>m</i> − 4). Graph the solution on the number line.",
                      "2.5m + 4 ≥ 0.5m − 2 → 2m ≥ −6 → m ≥ −3 (closed dot at −3, shade right)",
                      fig=nl_it(-6, 6, -3, True, False), fmt="Graphing",
                      frames=["2.5<i>m</i> + 4 ≥ 0.5<i>m</i> − [[2]] → [[2]]<i>m</i> ≥ [[−6]] → <i>m</i> ≥ [[−3]]",
                              "Dot at −3: [[closed]] (≥). Shade to the [[right]]."]),
                 OPEN("A phone plan costs $35 a month plus $0.10 per text. Kim can spend at most $50. Write and solve an "
                      "inequality for the number of texts <i>x</i>.", "35 + 0.10x ≤ 50 → 0.10x ≤ 15 → x ≤ 150 texts",
                      frames=["35 + 0.10<i>x</i> [[≤]] 50 → 0.10<i>x</i> ≤ [[15]] → <i>x</i> ≤ [[150]]"],
                      tip="“At most” means ≤."),
             ]),
    ]

    check = [
        MC("A gym charges a $40 sign-up fee plus $25 per month. Which equation gives the total cost <i>y</i> after <i>x</i> months?",
           [eq(40, 25), eq(-25, 40), eq(25, 40), eq(65, 0)], 2, why="$25 each month (rate) + $40 once (constant)."),
        MC("What value of <i>q</i> makes 10 − 4(<i>q</i> + 2) = 6 − 3(2<i>q</i> − 4) true?", ["2", "8", "10", "No solution"], 1,
           why="2 − 4q = 18 − 6q → 2q = 16 → q = 8."),
        MC(f"What is the solution set for 5(1 − <i>w</i>) {LE} −2<i>w</i> + 17?",
           [f"<i>w</i> {LE} −4", f"<i>w</i> {GE} 4", f"<i>w</i> {GE} −4", "<i>w</i> &lt; −4"], 2,
           why="5 − 5w ≤ −2w + 17 → −3w ≤ 12 → w ≥ −4 (divide by −3: flip).",
           tip="When you divide by −3, flip the sign."),
        OPEN(f"Solve 0.5(6{x} + 8) = −1.5{x} + 13.", "3x + 4 = −1.5x + 13 → 4.5x = 9 → x = 2",
             frames=[f"[[3]]{x} + [[4]] = −1.5{x} + 13 → [[4.5]]{x} = [[9]] → {x} = [[2]]"]),
        OPEN(f"Does ⅓(6{x} − 12) = 2({x} − 2) have one solution, no solution, or infinitely many solutions? Explain.",
             "2x − 4 = 2x − 4: both sides are the same, so infinitely many solutions.",
             frames=[f"Left: [[2]]{x} − [[4]] · Right: [[2]]{x} − [[4]]", "Both sides match, so there are [[infinitely many]] solutions."]),
        OPEN(f"How many solutions does 4({x} + 2) − {x} = 3{x} + 5 have? Explain.",
             "3x + 8 = 3x + 5 → 8 = 5 is false, so no solution.",
             frames=[f"Left: [[3]]{x} + [[8]] · Right: 3{x} + 5", "8 = 5 is [[false]], so there is [[no]] solution."]),
        OPEN("Malik buys 4 bottles of water for $1.50 each and some pretzels for $3.25 each. Write an equation for the "
             "total cost <i>y</i> when he buys <i>x</i> pretzels.", f"{y} = 3.25{x} + 6",
             frames=[f"Water: 4 × $1.50 = $[[6]] → {y} = [[3.25]]{x} + [[6]]"]),
        OPEN(f"Solve 6{x} − 4{y} = 20 for {y}.", "−4y = −6x + 20 → y = 1.5x − 5",
             frames=[f"−4{y} = [[−6]]{x} + 20 → {y} = [[1.5]]{x} − [[5]]"], lines=2),
        OPEN("The distance formula is <i>d</i> = <i>rt</i>. Solve the equation for <i>t</i>.", f"<i>t</i> = {fr('<i>d</i>', '<i>r</i>')}",
             frames=["<i>t</i> = <i>d</i> ÷ [[<i>r</i>]]"], lines=1),
        OPEN(f"Solve {y} = <i>m</i>{x} + <i>b</i> for <i>m</i>.", f"<i>m</i> = {fr('<i>y</i> − <i>b</i>', '<i>x</i>')}",
             frames=["<i>y</i> − [[<i>b</i>]] = <i>mx</i> → <i>m</i> = (<i>y</i> − <i>b</i>) ÷ [[<i>x</i>]]"], lines=2),
        OPEN("Solve the inequality and graph the solution on the number line: −3<i>n</i> + 7 &gt; 2(<i>n</i> − 4).",
             "−3n + 7 > 2n − 8 → 15 > 5n → n < 3 (open dot at 3, shade left)", fig=nl_it(-2, 8, 3, False, True), fmt="Graphing",
             frames=["−3<i>n</i> + 7 &gt; 2<i>n</i> − [[8]] → [[15]] &gt; [[5]]<i>n</i> → <i>n</i> &lt; [[3]]",
                     "Dot at 3: [[open]] (&lt;). Shade to the [[left]]."]),
        OPEN(f"Rewrite {y} + 6 = −½({x} − 4) in slope-intercept form.", "y + 6 = −½x + 2 → y = −½x − 4",
             frames=[f"{y} + 6 = −½{x} + [[2]] → {y} = −½{x} − [[4]]"], lines=2),
        OPEN("A triangle has a base of 10 inches and a height of (<i>x</i> + 2) inches. A rectangle is 4 inches wide and "
             "(<i>x</i> + 7) inches long. The two areas are equal. What is the value of <i>x</i>?",
             "½(10)(x + 2) = 4(x + 7) → 5x + 10 = 4x + 28 → x = 18", lines=4,
             frames=["Triangle: ½ · 10 · (<i>x</i> + 2) = [[5]]<i>x</i> + [[10]]", "Rectangle: 4(<i>x</i> + 7) = [[4]]<i>x</i> + [[28]]",
                     "5<i>x</i> + 10 = 4<i>x</i> + 28 → <i>x</i> = [[18]]"], tip="Triangle area = ½ · base · height."),
        OPEN("A dance studio charges a $45 registration fee plus $12.50 per class. Ella can spend at most $200. Write and "
             "solve an inequality. What is the greatest number of classes she can take?",
             "45 + 12.5x ≤ 200 → x ≤ 12.4 → at most 12 classes",
             frames=["45 + 12.5<i>x</i> ≤ [[200]] → 12.5<i>x</i> ≤ [[155]] → <i>x</i> ≤ [[12.4]]", "Whole classes only: [[12]] classes"]),
        MC("Which inequality is shown on the number line?" + numline(-6, 4, -2, True, False),
           [f"{x} &gt; −2", f"{x} {LE} −2", f"{x} {GE} −2", f"{x} &lt; −2"], 2, why="Closed dot (included) at −2, shaded right: x ≥ −2."),
        MC(f"Which value is a solution to 2{x} − 5 &gt; 9?", ["−8", "5", "7", "8"], 3,
           why="2x > 14 → x > 7. Only 8 is greater than 7 (7 itself makes 9 > 9, false)."),
    ]
    assert 45 + 12.5 * 12 <= 200 < 45 + 12.5 * 13 and 0.5 * (6 * 2 + 8) == -1.5 * 2 + 13
    staar = [
        MC(f"What is the solution to 2(3{x} − 4) = 4{x} + 10?", ["1", "3", "7", "9"], 3, teks="A.5(A)",
           why="6x − 8 = 4x + 10 → 2x = 18 → x = 9."),
        MC(f"Which is the solution set of −4({x} − 1) &lt; 2{x} − 8?", [f"{x} &gt; 2", f"{x} &lt; 2", f"{x} &gt; −2", f"{x} &lt; −2"], 0,
           teks="A.5(B)", why="−4x + 4 < 2x − 8 → 12 < 6x → x > 2."),
        MC("Which equation is equivalent to 3<i>a</i> + 2<i>b</i> = <i>c</i>, solved for <i>b</i>?",
           [f"<i>b</i> = {fr('<i>c</i> − 3<i>a</i>', 2)}", "<i>b</i> = <i>c</i> − 3<i>a</i> − 2", f"<i>b</i> = {fr('<i>c</i> + 3<i>a</i>', 2)}",
            f"<i>b</i> = {fr('<i>c</i>', '6<i>a</i>')}"], 0, teks="A.12(E)", why="2b = c − 3a → b = (c − 3a)/2."),
        OPEN(f"Solve 1.2({x} − 5) = 0.4{x} + 2. Enter your answer.", "1.2x − 6 = 0.4x + 2 → 0.8x = 8 → x = 10", teks="A.5(A)",
             fmt="Text entry", lines=1, frames=[f"[[0.8]]{x} = [[8]] → {x} = [[10]]"]),
        MC("A taxi charges $3.50 plus $2.25 per mile. Lucas paid $21.50. Which equation can find the miles <i>m</i>?",
           ["3.50<i>m</i> + 2.25 = 21.50", "2.25<i>m</i> + 3.50 = 21.50", "2.25<i>m</i> − 3.50 = 21.50", "5.75<i>m</i> = 21.50"], 1,
           teks="A.5(A)", why="$2.25 per mile times m, plus the $3.50 start."),
        MC(f"Which values are solutions to −4{x} + 3 {LE} 15? Select <b>TWO</b> correct answers.", ["−5", "−3", "0", "−4", "−3.5"],
           (1, 2), teks="A.5(B)", why="−4x ≤ 12 → x ≥ −3. Only −3 and 0 are −3 or greater."),
    ]
    vocab = [("solution", "a value that makes an equation or inequality true"),
             ("no solution / infinitely many", "simplifies to a false statement (1 = 5) / a true statement (5 = 5)"),
             ("literal equation", "an equation with two or more letters, like a formula"),
             ("inequality", "a statement using <, >, ≤, ≥"),
             ("closed dot / open dot", "the endpoint is included (≤, ≥) / not included (<, >)")]
    return dict(code="M3 T1", title="Linear Equations and Inequalities", module="Module 3: Modeling Linear Equations and Inequalities",
                teks="A.2B, A.2C, A.3A, A.5A, A.5B, A.12E", vocab=vocab, sections=sections, check=check, staar=staar)


# =====================================================================================================
# MODULE 3 · TOPIC 2 · Systems of Equations and Inequalities
# =====================================================================================================
def ch6():
    G = (-8, 8, 1, 2)
    BLUE, ORANGE = "#2f6fdd", "#e07b00"

    def sys_it(lines):  # graph-it: grid on the student page; the lines/shading are drawn on a key only
        return lambda: plot(G, G, lines if KEY else [])

    def ln(f, **k):
        return dict(f=f, a=-8, b=8, **k)

    assert 3 * 3 - 2 == 7 and 2 * 3 + 7 == 13 and 4 * 2 - 5 == 3 and 5 == 2 * 2 + 1 and 3 * 5 - 4 * 2 == 7
    assert 2 * 3 + 3 * 2 == 12 and 4 * 3 - 3 * 2 == 6 and 9 * 15 + 5 * 25 == 260 and 3 + 2 * 2 == 7 and 3 * 3 - 2 == 7
    sections = [
        dict(title="6.1 Solving Systems by Graphing", lesson="Lesson 1 · Getting Started, Activities 1–3, Talk the Talk ✪",
             idea=f"""<p>A <b>system</b> is two (or more) equations together. Its <b>solution</b> is the point that makes
             <b>both</b> true: where the lines <b>intersect</b>.</p><p><b>One solution</b>: the lines cross.
             <b>No solution</b>: parallel lines (same slope, different {y}-intercepts). <b>Infinitely many</b>: the same
             line.</p><p>In a story, the solution is where the two options are equal, like the month when two plans
             cost the same.</p>""",
             example=f"""<p>{y} = 2{x} − 1 and {y} = −{x} + 5 cross at <b>(2, 3)</b>. Check: 2(2) − 1 = 3 ✓, −2 + 5 = 3 ✓.</p>
             <p>Gym A: $20 + $30 a month → {y} = 30{x} + 20. Gym B: $50 + $25 a month → {y} = 25{x} + 50.
             30{x} + 20 = 25{x} + 50 → {x} = 6: after <b>6 months</b> both cost <b>$200</b>.</p>""",
             items=[
                 OPEN(f"Graph the system and determine the solution: {y} = {x} + 2 and {y} = −2{x} + 5.",
                      "The lines cross at (1, 3).", fig=sys_it([ln(lambda t: t + 2, color=RED), ln(lambda t: -2 * t + 5, color=RED)]),
                      frames=[f"Line 1: start at (0, [[2]]), slope [[1]]. Line 2: start at (0, [[5]]), slope [[−2]].",
                              "They cross at ([[1]], [[3]])."], fmt="Graphing", lines=0),
                 MC("Party Place A charges $80 plus $12 per guest. Party Place B charges $50 plus $15 per guest. Which system "
                    "represents the cost <i>y</i> for <i>x</i> guests?",
                    [f"{eq(80, 12)}<br>{eq(50, 15)}", f"{eq(12, 80)}<br>{eq(15, 50)}", f"{eq(12, 50)}<br>{eq(15, 80)}",
                     f"{eq(92, 0)}<br>{eq(65, 0)}"], 1, why="Per-guest prices are the slopes; the flat fees are the y-intercepts."),
             ]),
        dict(title="6.2 Solving Systems by Substitution", lesson="Lesson 2 · Activities 1–3 ✪",
             idea=f"""<p>When one equation is already solved for a variable ({y} = … or {x} = …), <b>substitute</b> that
             expression into the other equation. Solve, then plug back in to find the other variable.</p>""",
             example=f"""<p>{y} = 3{x} − 2 and 2{x} + {y} = 13 → 2{x} + (3{x} − 2) = 13 → 5{x} = 15 → {x} = 3; {y} = 3(3) − 2 = 7.
             <b>(3, 7)</b>.</p>""",
             items=[
                 OPEN(f"Solve by substitution: {y} = −2{x} + 9 and 4{x} − {y} = 3.", "4x − (−2x + 9) = 3 → 6x = 12 → x = 2; y = 5 → (2, 5)",
                      frames=[f"4{x} − (−2{x} + 9) = 3 → [[6]]{x} − 9 = 3 → {x} = [[2]]", f"{y} = −2(2) + 9 = [[5]] → ([[2]], [[5]])"],
                      tip="Put the whole expression in parentheses when you substitute."),
                 OPEN(f"Solve by substitution: {x} = 2{y} + 1 and 3{x} − 4{y} = 7.", "3(2y + 1) − 4y = 7 → 2y = 4 → y = 2; x = 5 → (5, 2)",
                      frames=[f"3(2{y} + 1) − 4{y} = 7 → [[2]]{y} + 3 = 7 → {y} = [[2]]", f"{x} = 2(2) + 1 = [[5]] → ([[5]], [[2]])"]),
             ]),
        dict(title="6.3 Solving Systems by Linear Combinations", lesson="Lesson 3 · Getting Started, Activities 1–4, Talk the Talk ✪",
             idea=f"""<p><b>Linear combinations</b> (elimination): add or subtract the equations so one variable cancels.
             If no variable cancels yet, multiply one (or both) equations by a number first.</p>
             <p>Story problems: write one equation for the <b>count</b> (how many) and one for the <b>value</b> (how much money).</p>""",
             example=f"""<p>3{x} + 2{y} = 16 and 5{x} − 2{y} = 0. Add: 8{x} = 16 → {x} = 2; 3(2) + 2{y} = 16 → {y} = 5. <b>(2, 5)</b>.</p>""",
             items=[
                 OPEN(f"Solve: 2{x} + 3{y} = 12 and 4{x} − 3{y} = 6.", "Add: 6x = 18 → x = 3; 2(3) + 3y = 12 → y = 2 → (3, 2)",
                      frames=[f"Add: [[6]]{x} = [[18]] → {x} = [[3]]", f"2(3) + 3{y} = 12 → {y} = [[2]]"]),
                 OPEN(f"Solve: {x} + 2{y} = 7 and 3{x} − {y} = 7.", "Multiply the 2nd by 2: 6x − 2y = 14; add: 7x = 21 → x = 3; y = 2",
                      frames=[f"2 × (3{x} − {y} = 7) → 6{x} − [[2]]{y} = [[14]]", f"Add: [[7]]{x} = [[21]] → {x} = [[3]] ; 3 + 2{y} = 7 → {y} = [[2]]"]),
                 OPEN("Movie tickets cost $9 for adults and $5 for children. A group of 40 people paid $260. How many adults "
                      "and how many children went?", "x + y = 40 and 9x + 5y = 260 → 9x + 5(40 − x) = 260 → 4x = 60 → 15 adults, 25 children",
                      frames=["Count: <i>a</i> + <i>c</i> = [[40]] · Money: [[9]]<i>a</i> + [[5]]<i>c</i> = 260",
                              "9<i>a</i> + 5(40 − <i>a</i>) = 260 → 4<i>a</i> = [[60]] → <i>a</i> = [[15]], <i>c</i> = [[25]]"], lines=4),
             ]),
        dict(title="6.4 Linear Inequalities in Two Variables", lesson="Lesson 4 · Activities 1–3, Talk the Talk ✪",
             idea=f"""<p>Graph the boundary line. <b>Dashed</b> for &lt; or &gt; (not included); <b>solid</b> for {LE} or {GE}.</p>
             <p>Shade the side that works: for {y} &gt; or {y} {GE}, shade <b>above</b>; for {y} &lt; or {y} {LE}, shade
             <b>below</b>. Not sure? <b>Test a point</b> like (0, 0).</p><p>In a story, <b>define your variables</b> first:
             “Let <i>x</i> = … and <i>y</i> = ….”</p>""",
             example=f"""<p><b>{y} &lt; 2{x} − 3:</b> dashed line, shade below. Test (0, 0): 0 &lt; −3 is false, so (0, 0) is not shaded. ✓</p>
             {plot(G, G, [dict(f=lambda t: 2 * t - 3, shade="below", dash=True)], size=170)}""",
             items=[
                 MC(f"Which ordered pair is in the solution set of 3{x} + {y} {GE} 6?", ["(0, 0)", "(1, 2)", "(2, 1)", "(−1, 8)"], 2,
                    why="3(2) + 1 = 7 ≥ 6 ✓. The others give 0, 5 and 5.", tip="Plug in each point. Is the answer 6 or more?"),
                 OPEN(f"Graph {y} {GE} −½{x} + 1.", "Solid line through (0, 1) with slope −½; shade above.",
                      fig=sys_it([dict(f=lambda t: -t / 2 + 1, shade="above", color=RED, line=RED)]),
                      frames=["≥ → [[solid]] line. Start at (0, [[1]]), slope [[−½]]. Shade [[above]]."], fmt="Graphing", lines=0),
                 OPEN("A bakery makes muffins (2 minutes each) and cookie batches (3 minutes each). It has at most 120 minutes. "
                      "Write a linear inequality. Define your variables.", "x = muffins, y = cookie batches: 2x + 3y ≤ 120",
                      frames=["Let <i>x</i> = [[muffins]] and <i>y</i> = [[cookie batches]].", "[[2]]<i>x</i> + [[3]]<i>y</i> [[≤]] 120"]),
             ]),
        dict(title="6.5 Systems of Linear Inequalities", lesson="Lesson 5 · Getting Started, Activities 1–2, Talk the Talk ✪",
             idea="""<p>Graph each inequality. The solutions to the <b>system</b> are in the region where the shadings
             <b>overlap</b>. A point on a dashed line is not a solution. Check a point from the overlap in <b>both</b>
             inequalities.</p>""",
             example=f"""<p><b>{y} &gt; {x}</b> (dashed, above) and <b>{y} {LE} −{x} + 4</b> (solid, below). Test (0, 2):
             2 &gt; 0 ✓ and 2 {LE} 4 ✓, so (0, 2) is in the overlap.</p>
             {plot(G, G, [dict(f=lambda t: t, shade='above', dash=True, color=BLUE), dict(f=lambda t: -t + 4, shade='below', color=ORANGE)], size=170)}""",
             items=[
                 OPEN(f"Graph the system: {y} {LE} 2{x} + 1 and {y} &gt; −{x} − 2.",
                      "Solid y = 2x + 1 shaded below; dashed y = −x − 2 shaded above; the solution is the overlap.",
                      fig=sys_it([dict(f=lambda t: 2 * t + 1, shade="below", color=BLUE, line=RED),
                                  dict(f=lambda t: -t - 2, shade="above", dash=True, color=ORANGE, line=RED)]),
                      frames=["Line 1: [[solid]], shade [[below]]. Line 2: [[dashed]], shade [[above]].", "The answer is where they [[overlap]]."],
                      fmt="Graphing", lines=0),
                 MC(f"Which point is a solution to the system {x} + {y} &lt; 6 and {y} {GE} 2{x}?", ["(1, 3)", "(3, 2)", "(0, 6)", "(2, 0)"], 0,
                    why="(1, 3): 4 < 6 ✓ and 3 ≥ 2 ✓. (0, 6) gives 6 < 6, false."),
             ]),
    ]

    sav = plot((0, 12, 1, 2), (0, 450, 25, 50), [dict(f=lambda t: 200 + 15 * t, a=0, b=12, ends=("closed", "arrow"), label="Ava"),
                                                  dict(f=lambda t: 80 + 35 * t, a=0, b=10.5, ends=("closed", "arrow"), label="Ben")],
               xlab="Weeks", ylab="Savings ($)")
    assert 200 + 15 * 6 == 80 + 35 * 6 == 290 and 45 * 50 + 30 * 70 == 4350 and 400 + 6 * 50 == 14 * 50
    assert 2 * 3 + 5 * -1 == 1 and 3 * 3 - 2 * -1 == 11 and 40 * 7 + 25 == 35 * 7 + 60 == 305
    check = [
        MC("Phone Plan A costs $25 to start plus $40 a month. Plan B costs $60 to start plus $35 a month. Which system "
           "represents the total cost <i>y</i> after <i>x</i> months?",
           [f"{eq(25, 40)}<br>{eq(60, 35)}", f"{eq(40, 60)}<br>{eq(35, 25)}", f"{eq(40, 25)}<br>{eq(35, 60)}", f"{eq(65, 0)}<br>{eq(95, 0)}"], 2),
        MC(f"The graph of 2{x} − 3{y} = 6 is shown (dashed). Which ordered pair is in the solution set of 2{x} − 3{y} &lt; 6?",
           ["(4, 0)", "(1, −1)", "(6, 2)", "(0, −3)"], 1,
           fig=plot(G, G, [dict(f=lambda t: (2 * t - 6) / 3, a=-8, b=8, dash=True)]),
           why="2(1) − 3(−1) = 5 < 6 ✓. (6, 2) gives 6 < 6 (false: on the line)."),
        OPEN(f"Graph the system and determine the solution: {y} = ½{x} + 1 and 3{x} + 2{y} = −6.",
             "3x + 2y = −6 → y = −1.5x − 3. The lines cross at (−2, 0).",
             fig=sys_it([ln(lambda t: t / 2 + 1, color=RED), ln(lambda t: -1.5 * t - 3, color=RED)]),
             frames=[f"3{x} + 2{y} = −6 → {y} = [[−1.5]]{x} − [[3]]", "The lines cross at ([[−2]], [[0]])."], fmt="Graphing", lines=0),
        OPEN("The graph shows Ava’s and Ben’s savings. Estimate the solution to the system and explain what it means.",
             "About (6, 290): after 6 weeks, Ava and Ben have saved the same amount, about $290.", fig=sav,
             frames=["The lines cross near ([[6]], [[290]]).", "After [[6]] weeks they both have about $[[290]]."]),
        OPEN("A concert sold 120 tickets. Floor tickets cost $45 and balcony tickets cost $30. The total was $4,350. "
             "How many of each ticket were sold?", "f + b = 120 and 45f + 30b = 4,350 → 15f = 750 → 50 floor, 70 balcony", lines=4,
             frames=["<i>f</i> + <i>b</i> = [[120]] · [[45]]<i>f</i> + [[30]]<i>b</i> = 4,350",
                     "45<i>f</i> + 30(120 − <i>f</i>) = 4,350 → [[15]]<i>f</i> = [[750]] → <i>f</i> = [[50]], <i>b</i> = [[70]]"]),
        OPEN("A ferry can carry at most 60 tons. Each car weighs 2 tons and each truck weighs 5 tons. Write a linear "
             "inequality to model this. Define your variables.", "c = cars, t = trucks: 2c + 5t ≤ 60",
             frames=["Let <i>c</i> = [[cars]], <i>t</i> = [[trucks]].", "[[2]]<i>c</i> + [[5]]<i>t</i> [[≤]] 60"]),
        OPEN(f"Graph the inequality 2{x} + 5{y} {LE} 60 for the ferry (cars on the {x}-axis, trucks on the {y}-axis).",
             "Solid line through (30, 0) and (0, 12); shade below, in the first quadrant.",
             fig=lambda: plot((0, 35, 2.5, 5), (0, 15, 1, 3), [dict(f=lambda t: (60 - 2 * t) / 5, shade="below", color=RED, line=RED)] if KEY else [],
                              xlab="Cars", ylab="Trucks"),
             frames=["Intercepts: ([[30]], 0) and (0, [[12]]). [[Solid]] line, shade [[below]]."], fmt="Graphing", lines=0),
        OPEN(f"Graph the solution set of the system: {y} {GE} −{x} + 3 and {x} − {y} &gt; 1.",
             "Solid y = −x + 3 shaded above; x − y > 1 → y < x − 1, dashed, shaded below; the answer is the overlap.",
             fig=sys_it([dict(f=lambda t: -t + 3, shade="above", color=BLUE, line=RED),
                         dict(f=lambda t: t - 1, shade="below", dash=True, color=ORANGE, line=RED)]),
             frames=[f"{x} − {y} &gt; 1 → {y} [[&lt;]] {x} − 1", "Line 1 [[solid]], above. Line 2 [[dashed]], below. Solutions: the [[overlap]]."],
             fmt="Graphing", lines=0),
        OPEN("Each table shows points on a line. Write the equation of each line as <i>y</i> = <i>mx</i> + <i>b</i>."
             + '<div class="row">' + htable(("<i>x</i> (line <i>f</i>)", ["−2", 0, 2, 4]), ("<i>y</i>", ["−5", "−1", 3, 7]))
             + htable(("<i>x</i> (line <i>g</i>)", ["−4", 0, 4, 8]), ("<i>y</i>", [6, 3, 0, "−3"])) + "</div>",
             f"f: {y} = 2{x} − 1 · g: {y} = −0.75{x} + 3",
             frames=["f: slope 4 ÷ 2 = [[2]], y-intercept [[−1]]", "g: slope −3 ÷ 4 = [[−0.75]], y-intercept [[3]]"]),
        OPEN("The art club pays $400 to print a yearbook design plus $6 per book. They sell each book for $14. How many "
             "books must they sell to break even?", "400 + 6x = 14x → 400 = 8x → x = 50 books",
             frames=["Cost: 400 + [[6]]<i>x</i> · Income: [[14]]<i>x</i>", "400 + 6<i>x</i> = 14<i>x</i> → <i>x</i> = [[50]]"],
             tip="Break even means cost = income."),
        MC(f"What is the value of {x} in the solution to {y} = 4{x} + 2 and {y} = −2{x} − 10?", ["−6", "−2", "2", "−12"], 1,
           why="4x + 2 = −2x − 10 → 6x = −12 → x = −2 (y = −6)."),
        OPEN(f"Solve by substitution: 3{x} + {y} = 10 and {y} = {x} − 2.", "3x + (x − 2) = 10 → 4x = 12 → x = 3, y = 1",
             frames=[f"3{x} + ({x} − 2) = 10 → [[4]]{x} = [[12]] → {x} = [[3]], {y} = [[1]]"]),
        OPEN(f"Solve: 2{x} + 5{y} = 1 and 3{x} − 2{y} = 11.", "×2 and ×5: 4x + 10y = 2, 15x − 10y = 55 → 19x = 57 → x = 3, y = −1",
             frames=[f"×2: 4{x} + 10{y} = [[2]] · ×5: 15{x} − 10{y} = [[55]]", f"Add: [[19]]{x} = [[57]] → {x} = [[3]], {y} = [[−1]]"]),
        ROWS("How many solutions does each system have?", ["One", "None", "Infinitely many"],
             [(f"{y} = 3{x} + 1 and {y} = 3{x} − 2", 1), (f"{y} = 2{x} + 4 and 2{y} = 4{x} + 8", 2), (f"{y} = {x} and {y} = −{x} + 6", 0)],
             why="Same slope, different intercepts → parallel. 2y = 4x + 8 → y = 2x + 4 (same line). Different slopes → one.",
             tip="Write both in y = mx + b. Compare the slopes, then the y-intercepts."),
        MC(f"Which point is a solution to the system {y} &gt; 2{x} − 1 and {y} {LE} −{x} + 5?", ["(3, 2)", "(0, 6)", "(2, 3)", "(1, 3)"], 3,
           why="(1, 3): 3 > 1 ✓, 3 ≤ 4 ✓. (2, 3): 3 > 3 is false."),
        OPEN("Two phone plans cost <i>y</i> = 40<i>x</i> + 25 and <i>y</i> = 35<i>x</i> + 60 dollars after <i>x</i> months. "
             "Solve the system and explain what the solution means.", "40x + 25 = 35x + 60 → x = 7, y = 305: after 7 months both plans cost $305.",
             frames=["5<i>x</i> = [[35]] → <i>x</i> = [[7]] ; <i>y</i> = 40(7) + 25 = [[305]]", "After [[7]] months both plans cost $[[305]]."]),
    ]
    staar = [
        MC(f"What is the solution to the system {x} + {y} = 10 and {x} − {y} = 4?", ["(3, 7)", "(7, 3)", "(6, 4)", "(4, 6)"], 1,
           teks="A.5(C)", why="Add: 2x = 14 → x = 7, y = 3."),
        MC("Lena has 18 coins, all dimes and quarters, worth $3.15. Which system can find the number of dimes <i>d</i> and quarters <i>q</i>?",
           ["<i>d</i> + <i>q</i> = 3.15<br>10<i>d</i> + 25<i>q</i> = 18", "<i>d</i> + <i>q</i> = 18<br>0.10<i>d</i> + 0.25<i>q</i> = 3.15",
            "<i>d</i> + <i>q</i> = 18<br>0.25<i>d</i> + 0.10<i>q</i> = 3.15", "<i>d</i> − <i>q</i> = 18<br>0.10<i>d</i> + 0.25<i>q</i> = 3.15"], 1,
           teks="A.2(I)"),
        MC("Which inequality is graphed?", [f"{y} &gt; −{x} + 2", f"{y} {GE} −{x} + 2", f"{y} &lt; −{x} + 2", f"{y} {LE} −{x} + 2"], 0,
           fig=plot(G, G, [dict(f=lambda t: -t + 2, shade="above", dash=True)], size=190), teks="A.3(D)",
           why="Dashed (not included) and shaded above: y > −x + 2."),
        MC(f"Which points are solutions to the system {y} &lt; {x} + 3 and {y} {GE} −2? Select <b>TWO</b> correct answers.",
           ["(0, 0)", "(−4, 1)", "(2, −2)", "(0, 3)", "(1, −5)"], (0, 2), teks="A.3(H)",
           why="(0, 0): 0 < 3 ✓, 0 ≥ −2 ✓. (2, −2): −2 < 5 ✓, −2 ≥ −2 ✓. (0, 3) is on the dashed line."),
        OPEN(f"What is the <i>y</i>-value of the solution to {y} = 5{x} − 3 and {y} = 2{x} + 9? Enter your answer.",
             "5x − 3 = 2x + 9 → x = 4, y = 17", teks="A.5(C)", fmt="Text entry", lines=1,
             frames=["3<i>x</i> = [[12]] → <i>x</i> = [[4]] → <i>y</i> = [[17]]"]),
        OPEN(f"Choose the words that complete the sentence.<br>The system {y} = 4{x} − 1 and {y} = 4{x} + 3 has ( no / one / "
             "infinitely many ) solution(s) because the lines are ( parallel / the same line / intersecting ).", "no · parallel",
             teks="A.3(F), A.3(G)", fmt="Inline choice", lines=1,
             frames=["Same slope [[4]], different y-intercepts → [[parallel]] → [[no]] solution."]),
    ]
    vocab = [("system of equations", "two or more equations with the same variables"),
             ("solution of a system", "the point that makes every equation true (the intersection)"),
             ("substitution", "replace a variable with an equal expression"),
             ("linear combinations", "add or subtract equations to cancel a variable (elimination)"),
             ("boundary line", "dashed for < or >, solid for ≤ or ≥"),
             ("break even", "the point where cost equals income")]
    return dict(code="M3 T2", title="Systems of Equations and Inequalities", module="Module 3: Modeling Linear Equations and Inequalities",
                teks="A.2A, A.2C, A.2H, A.2I, A.3D, A.3F–H, A.5C", vocab=vocab, sections=sections, check=check, staar=staar)


# =====================================================================================================
# MODULE 4 · TOPIC 1 · Introduction to Exponential Functions
# =====================================================================================================
def rt(inner, idx=""):  # radical: optional index, overline on the radicand
    return f'{f"<sup>{idx}</sup>" if idx else ""}√<span class="ov">{inner}</span>'


def expreg(xs, ys):  # calculator ExpReg: least squares on ln y -> y = a·b^x (rounded to hundredths)
    m, c = linear_regression(xs, [log(v) for v in ys])
    return round(exp(c), 2), round(exp(m), 2)


def ch7():
    G = (-8, 8, 1, 2)
    small = lambda f, a=-8, b=8: plot(G, G, [dict(f=f, a=a, b=b)], size=120)
    assert 6 ** 2 * 2 == 72 and 4 ** 2 * 3 == 48 and 3 ** 2 * 7 == 63 and 5 ** 2 * 3 == 75 and 7 ** 2 * 2 == 98 and 6 ** 2 * 5 == 180
    sections = [
        dict(title="7.1 Properties of Powers", lesson="Lessons 1–2 · Activities 2–6, Talk the Talk ✪",
             idea=f"""<table class="t"><tr><th>Rule</th><th>Example</th></tr>
             <tr><td>Product: add exponents</td><td>{x}³ · {x}⁴ = {x}⁷</td></tr>
             <tr><td>Quotient: subtract exponents</td><td>{x}⁹ ÷ {x}² = {x}⁷</td></tr>
             <tr><td>Power of a power: multiply</td><td>({x}³)⁴ = {x}¹²</td></tr>
             <tr><td>Power of a product</td><td>(2{x})³ = 8{x}³</td></tr>
             <tr><td>Zero exponent</td><td>{x}⁰ = 1</td></tr>
             <tr><td>Negative exponent: move it across the fraction bar</td><td>{x}<sup>−3</sup> = {fr(1, f'{x}³')}</td></tr></table>
             <p>Simplest form: no negative exponents, and each variable appears once.</p>""",
             example=f"""<p>(2{x}³{y}<sup>−2</sup>)(5{x}<sup>−1</sup>{y}⁶) = 10{x}<sup>3−1</sup>{y}<sup>−2+6</sup> = <b>10{x}²{y}⁴</b></p>
             <p>{fr('24<i>a</i>⁵<i>b</i><sup>−3</sup>', '6<i>a</i><sup>−2</sup><i>b</i>²')} = 4<i>a</i><sup>5−(−2)</sup><i>b</i><sup>−3−2</sup>
             = 4<i>a</i>⁷<i>b</i><sup>−5</sup> = <b>{fr('4<i>a</i>⁷', '<i>b</i>⁵')}</b></p>""",
             items=[
                 MC("Which is equivalent to (3<i>m</i>⁴<i>n</i><sup>−1</sup>)²?",
                    [f"{fr('6<i>m</i>⁸', '<i>n</i>²')}", f"{fr('9<i>m</i>⁸', '<i>n</i>²')}", "9<i>m</i>⁶<i>n</i>", f"{fr('9<i>m</i>⁶', '<i>n</i>')}"], 1,
                    why="3² = 9; (m⁴)² = m⁸; (n⁻¹)² = n⁻² = 1/n².", tip="Square EVERYTHING inside: the 3, the m⁴ and the n⁻¹."),
                 OPEN(f"Write in simplest form: {fr('48<i>p</i><sup>−3</sup><i>q</i>⁵<i>r</i>²', '12<i>p</i>²<i>q</i><sup>−1</sup><i>r</i>²')}",
                      f"4p⁻⁵q⁶r⁰ = {fr('4<i>q</i>⁶', '<i>p</i>⁵')}",
                      frames=["48 ÷ 12 = [[4]] · <i>p</i>: −3 − 2 = [[−5]] · <i>q</i>: 5 − (−1) = [[6]] · <i>r</i>: 2 − 2 = [[0]]",
                              "Simplest form (move p⁻⁵ to the bottom; r⁰ = 1): [[4<i>q</i>⁶ / <i>p</i>⁵]]"],
                      tip="Subtract exponents: top minus bottom. Then move negative exponents to the other side."),
                 MC(f"Which is equivalent to {fr(f'{x}⁵ · {x}<sup>−2</sup>', f'{x}⁴')}?", [f"{x}", f"{fr(1, x)}", f"{x}<sup>11</sup>", f"{x}³"], 1,
                    why="5 + (−2) − 4 = −1, and x⁻¹ = 1/x."),
             ]),
        dict(title="7.2 Geometric Sequences and Exponential Functions", lesson="Lesson 3 · Getting Started, Activities 1–4 ✪",
             idea=f"""<p>A geometric sequence {sub('g', 'n')} = {sub('g', 1)} · <i>r</i><sup>{n}−1</sup> is an <b>exponential
             function</b> <i>f</i>({x}) = <i>a</i> · <i>b</i><sup>{x}</sup> with <i>b</i> = <i>r</i> and <i>a</i> = {sub('g', 1)} ÷ <i>r</i>
             (the term before the first one, at {x} = 0).</p><p>From a table: <i>a</i> = the value at {x} = 0 and
             <i>b</i> = the number you multiply by each time.</p>""",
             example=f"""<p>{sub('g', 'n')} = 6 · 2<sup>{n}−1</sup> → <i>a</i> = 6 ÷ 2 = 3 → <b><i>f</i>({x}) = 3 · 2<sup>{x}</sup></b>.
             Check {x} = 1: 3 · 2 = 6 ✓.</p>""",
             items=[
                 OPEN(f"Rewrite {sub('g', 'n')} = 80(½)<sup>{n}−1</sup> in the form <i>f</i>({x}) = <i>a</i> · <i>b</i><sup>{x}</sup>.",
                      f"a = 80 ÷ ½ = 160 → f(x) = 160(½)<sup>x</sup>",
                      frames=["<i>b</i> = [[½]] · <i>a</i> = 80 ÷ ½ = [[160]]", f"<i>f</i>({x}) = [[160]]([[½]])<sup>{x}</sup>"],
                      tip="Dividing by ½ is the same as multiplying by 2.", lines=2),
                 OPEN(f"A sequence is defined by <i>f</i>({n}) = ⅓ · <i>f</i>({n} − 1), with <i>f</i>(1) = 54. What are the first four terms?",
                      "54, 18, 6, 2", frames=["54, [[18]], [[6]], [[2]]"], lines=1),
                 OPEN("Write an exponential function for the table." + htable((x, [0, 1, 2, 3]), (y, [5, 15, 45, 135])),
                      f"f(x) = 5 · 3<sup>x</sup>", frames=[f"<i>a</i> = value at x = 0 = [[5]] · <i>b</i> = 15 ÷ 5 = [[3]]"], lines=1),
             ]),
        dict(title="7.3 Simplifying Square Roots", lesson="Lesson 4 · Getting Started, Activities 1–2, Talk the Talk ✪",
             idea=f"""<p><b>Simplest radical form:</b> find the largest perfect square factor (4, 9, 16, 25, 36, 49, …),
             take its square root out front, and leave the rest inside: {rt('ab')} = {rt('a')} · {rt('b')}.</p>""",
             example=f"""<p>{rt(72)} = {rt('36 · 2')} = <b>6{rt(2)}</b>. &nbsp; 3{rt(50)} = 3 · {rt('25 · 2')} = 3 · 5{rt(2)} = <b>15{rt(2)}</b>.</p>""",
             items=[
                 OPEN(f"Write {rt(48)} in simplest radical form.", f"√(16 · 3) = 4{rt(3)}", frames=[f"{rt('[[16]] · 3')} = [[4]]{rt(3)}"],
                      tip="Perfect squares: 4, 9, 16, 25, 36, 49, 64. Which one divides 48?", lines=1),
                 OPEN(f"Write 2{rt(63)} in simplest radical form.", f"2 · √(9 · 7) = 2 · 3{rt(7)} = 6{rt(7)}",
                      frames=[f"2 · {rt('[[9]] · 7')} = 2 · [[3]]{rt(7)} = [[6]]{rt(7)}"], lines=1),
                 MC(f"Which is equal to {rt(200)}?", [f"2{rt(10)}", f"10{rt(2)}", f"20{rt(10)}", f"100{rt(2)}"], 1,
                    why="200 = 100 · 2 and √100 = 10."),
             ]),
        dict(title="7.4 Rational Exponents and Graphs of Exponential Functions", lesson="Lesson 5 · Getting Started, Activities 1–5, Talk the Talk ✪",
             idea=f"""<p><b>Rational exponents:</b> {x}<sup><i>m</i>/<i>n</i></sup> = {rt(f'{x}<sup><i>m</i></sup>', '<i>n</i>')}.
             The bottom of the fraction is the root. {x}<sup>½</sup> = {rt(x)}.</p>
             <p><b>Graph of <i>f</i>({x}) = <i>a</i> · <i>b</i><sup>{x}</sup>:</b> <i>y</i>-intercept (0, <i>a</i>); horizontal
             asymptote {y} = 0; domain all real numbers. If <i>a</i> &gt; 0: range {y} &gt; 0, <b>increasing</b> when <i>b</i> &gt; 1,
             <b>decreasing</b> when 0 &lt; <i>b</i> &lt; 1. If <i>a</i> &lt; 0 the graph is flipped below the {x}-axis (range {y} &lt; 0).</p>""",
             example=f"""<p>{rt('7⁴', 3)} = <b>7<sup>4/3</sup></b>. &nbsp; (5{x}<sup>⅓</sup>)(2{x}<sup>⅔</sup>) = 10{x}<sup>⅓+⅔</sup> = <b>10{x}</b>.</p>
             <p><i>f</i>({x}) = 4(½)<sup>{x}</sup>: <i>y</i>-intercept (0, 4), asymptote {y} = 0, decreasing, range {y} &gt; 0.</p>""",
             items=[
                 MC(f"Which is equivalent to {rt('2³', 5)}?", ["2<sup>5/3</sup>", "2<sup>3/5</sup>", "2<sup>15</sup>", "2<sup>8</sup>"], 1,
                    why="The root (5) is the bottom of the fraction; the power (3) is the top.", tip="Root on the bottom: “the root is the root of the tree,” down low."),
                 OPEN(f"Simplify (5{x}<sup>⅓</sup>)(2{x}<sup>⅔</sup>{y}).", f"10x<sup>1</sup>y = 10{x}{y}",
                      frames=[f"5 · 2 = [[10]] · {x}: ⅓ + ⅔ = [[1]] → [[10]]{x}{y}"], lines=1),
                 OPEN(f"For <i>f</i>({x}) = −2(3)<sup>{x}</sup>, give the <i>y</i>-intercept, the asymptote, the range, and whether it "
                      "increases or decreases.", "y-intercept (0, −2); asymptote y = 0; range y < 0; decreasing",
                      frames=["y-intercept (0, [[−2]]) · asymptote y = [[0]]", "a is negative → range y [[&lt;]] 0 · it [[decreases]]"]),
             ]),
    ]

    g5 = plot(G, G, [dict(f=lambda t: -3 * 2 ** t, a=-8, b=1.5)], pts=[(0, -3, "(0, −3)"), (1, -6, "(1, −6)")])
    check = [
        MC(f"Which graph shows <i>f</i>({x}) = −(½)<sup>{x}</sup>?",
           [small(lambda t: 0.5 ** t, -3, 8), small(lambda t: -(0.5 ** t), -3, 8), small(lambda t: -(2 ** t), -8, 3), small(lambda t: 2 ** t, -8, 3)], 1,
           why="(½)ˣ decreases toward 0; the negative sign flips it below the x-axis, so it rises toward 0 from below.",
           tip="First picture (½)ˣ. Then the minus sign flips it upside down."),
        MC(f"Write {rt('3³', 4)} as a power of 3.", ["3<sup>4/3</sup>", "3<sup>3/4</sup>", "3<sup>12</sup>", "3<sup>1/12</sup>"], 1),
        MC("A phone bought for $800 loses 20% of its value each year. Which function gives its value after <i>x</i> years?",
           ["<i>f</i>(<i>x</i>) = 800(0.2)<sup><i>x</i></sup>", "<i>f</i>(<i>x</i>) = 800(1.2)<sup><i>x</i></sup>",
            "<i>f</i>(<i>x</i>) = 800(0.8)<sup><i>x</i></sup>", "<i>f</i>(<i>x</i>) = 800(1.8)<sup><i>x</i></sup>"], 2,
           why="Losing 20% leaves 80% each year: b = 1 − 0.20 = 0.8."),
        OPEN(f"Write in simplest form: {fr('36<i>a</i><sup>−2</sup><i>b</i>⁵<i>c</i>⁴', '9<i>a</i>³<i>b</i><sup>−1</sup><i>c</i>⁴')}",
             f"4a⁻⁵b⁶ = {fr('4<i>b</i>⁶', '<i>a</i>⁵')}",
             frames=["36 ÷ 9 = [[4]] · <i>a</i>: −2 − 3 = [[−5]] · <i>b</i>: 5 − (−1) = [[6]] · <i>c</i>: [[0]]"]),
        OPEN(f"Rewrite <i>g</i>({n}) = 3(2)<sup>{n}−1</sup> in the form <i>f</i>({x}) = <i>a</i> · <i>b</i><sup>{x}</sup>.",
             f"a = 3 ÷ 2 = 1.5 → f(x) = 1.5(2)<sup>x</sup>", frames=["<i>a</i> = 3 ÷ 2 = [[1.5]] · <i>b</i> = [[2]]"], lines=2),
        OPEN(f"For <i>f</i>({x}) = 1.5(2)<sup>{x}</sup>, identify the <i>y</i>-intercept, the equation of the asymptote, and "
             "whether the function increases or decreases.", "(0, 1.5); y = 0; increases (b = 2 > 1, a > 0)",
             frames=["(0, [[1.5]]) · asymptote y = [[0]] · b = 2 &gt; 1, so it [[increases]]"]),
        OPEN(f"Write {rt(75)} in simplest radical form.", f"√(25 · 3) = 5{rt(3)}", frames=[f"{rt('[[25]] · 3')} = [[5]]{rt(3)}"], lines=1),
        OPEN(f"Write 4{rt(98)} in simplest radical form.", f"4 · √(49 · 2) = 4 · 7{rt(2)} = 28{rt(2)}",
             frames=[f"4 · {rt('[[49]] · 2')} = 4 · [[7]]{rt(2)} = [[28]]{rt(2)}"], lines=1),
        OPEN("State the domain and range of this exponential function.", "Domain: all real numbers · Range: y < 0", fig=g5,
             frames=["Domain: [[all real numbers]] · Range: y [[&lt;]] [[0]]"], tip="The curve never touches the x-axis."),
        OPEN(f"Use the two labeled points to find <i>a</i> and <i>b</i>, then write <i>f</i>({x}) = <i>a</i> · <i>b</i><sup>{x}</sup>.",
             f"a = −3, b = −6 ÷ −3 = 2 → f(x) = −3(2)<sup>x</sup>", fig=g5,
             frames=["<i>a</i> = y-intercept = [[−3]] · <i>b</i> = −6 ÷ (−3) = [[2]]"]),
        OPEN("The table shows the number of algae cells in a tank."
             + htable(("Day", [0, 1, 2, 3]), ("Cells", [250, 500, "1,000", "2,000"]))
             + "a. Write an exponential function for the cells after <i>t</i> days.<br>"
               "b. Interpret the <i>y</i>-intercept and the constant ratio.",
             f"a. f(t) = 250(2)<sup>t</sup> &nbsp; b. 250: there were 250 cells at day 0. 2: the number of cells doubles every day.",
             frames=["a. <i>a</i> = [[250]] · <i>b</i> = 500 ÷ 250 = [[2]]",
                     "b. [[250]] cells at day 0; the cells [[double]] each day."], lines=4),
        OPEN("Simplify (4<i>m</i><sup>½</sup><i>n</i><sup>⅔</sup>)(2<i>m</i><sup>½</sup><i>n</i><sup>⅓</sup>).", "8m¹n¹ = 8mn",
             frames=["4 · 2 = [[8]] · <i>m</i>: ½ + ½ = [[1]] · <i>n</i>: ⅔ + ⅓ = [[1]]"], lines=1),
        OPEN(f"A sequence is defined by <i>f</i>({n}) = ⅔ · <i>f</i>({n} − 1), with <i>f</i>(1) = 81. What are the first four terms?",
             "81, 54, 36, 24", frames=["81, [[54]], [[36]], [[24]]"], tip="⅔ of a number: divide by 3, then multiply by 2.", lines=1),
        MC(f"Which is equivalent to (2{x}³)⁴?", [f"8{x}⁷", f"16{x}¹²", f"8{x}¹²", f"16{x}⁷"], 1, why="2⁴ = 16 and (x³)⁴ = x¹²."),
        MC(f"Which is equivalent to {x}<sup>2/5</sup>?", [rt(f"{x}⁵", 2), rt(f"{x}²", 5), f"{fr(f'{x}²', 5)}", f"5{x}²"], 1),
    ]
    assert 81 * 2 / 3 == 54 and 54 * 2 / 3 == 36 and 36 * 2 / 3 == 24 and 54 / 3 == 18
    staar = [
        MC("Which is equivalent to (−3<i>a</i>²<i>b</i><sup>−4</sup>)(2<i>a</i><sup>−5</sup><i>b</i>⁶)?",
           [f"{fr('−6<i>b</i>²', '<i>a</i>³')}", "−6<i>a</i>³<i>b</i>²", f"{fr('−6', '<i>a</i>³<i>b</i>²')}", "−<i>a</i><sup>−3</sup><i>b</i>²"], 0,
           teks="A.11(B)", why="−3 · 2 = −6; a²⁺⁽⁻⁵⁾ = a⁻³; b⁻⁴⁺⁶ = b²."),
        MC(f"Which is equivalent to {fr(f'{x}<sup>−2</sup>{y}⁵', f'{x}⁴{y}<sup>−3</sup>')}?",
           [f"{fr(f'{y}²', f'{x}²')}", f"{fr(f'{y}⁸', f'{x}⁶')}", f"{x}²{y}²", f"{fr(f'{x}⁶', f'{y}⁸')}"], 1, teks="A.11(B)"),
        MC(f"Which is the simplest radical form of {rt(180)}?", [f"3{rt(20)}", f"6{rt(5)}", f"5{rt(6)}", f"9{rt(20)}"], 1, teks="A.11(A)",
           why="180 = 36 · 5."),
        MC("Which statement is true about <i>f</i>(<i>x</i>) = 200(0.75)<sup><i>x</i></sup>?",
           ["It is increasing; the y-intercept is 200.", "It is decreasing; the y-intercept is 200.",
            "It is decreasing; the y-intercept is 0.75.", "It is increasing; the y-intercept is 0.75."], 1, teks="A.9(D)"),
        OPEN("If <i>f</i>(<i>x</i>) = 3 · 4<sup><i>x</i></sup>, what is <i>f</i>(3)? Enter your answer.", "3 · 64 = 192", teks="A.9(C)",
             fmt="Text entry", lines=1, frames=["4³ = [[64]] → 3 · 64 = [[192]]"]),
        MC(f"Which expressions are equivalent to {x}⁶? Select <b>TWO</b> correct answers.",
           [f"({x}²)³", f"{x}² · {x}³", f"{fr(f'{x}⁸', f'{x}²')}", f"({x}³)³", f"{x}<sup>12</sup> ÷ {x}<sup>2</sup>"], (0, 2), teks="A.11(B)",
           why="(x²)³ = x⁶; x⁸/x² = x⁶. x² · x³ = x⁵; x¹²/x² = x¹⁰."),
    ]
    vocab = [("exponent / base", "in b<sup>x</sup>, b is the base and x is the exponent"),
             ("negative exponent", "x⁻ⁿ = 1 ÷ xⁿ"),
             ("rational exponent", "an exponent that is a fraction: x<sup>m/n</sup> = ⁿ√(x<sup>m</sup>)"),
             ("simplest radical form", "no perfect-square factor left under the √"),
             ("exponential function", "f(x) = a · b<sup>x</sup>, with a ≠ 0, b > 0, b ≠ 1"),
             ("asymptote", "a line the graph gets closer and closer to but never touches")]
    return dict(code="M4 T1", title="Introduction to Exponential Functions", module="Module 4: Investigating Growth and Decay",
                teks="A.9A–D, A.11A, A.11B, A.12B–D", vocab=vocab, sections=sections, check=check, staar=staar)


# =====================================================================================================
# MODULE 4 · TOPIC 2 · Using Exponential Equations
# =====================================================================================================
def ch8():
    sub_x, sub_y = [0, 1, 2, 3, 4], [150, 240, 370, 600, 950]
    sa, sb = expreg(sub_x, sub_y)
    st_x, st_y = [0, 1, 2, 3, 4], [52, 110, 236, 498, 1050]
    ta, tb = expreg(st_x, st_y)
    tpred = ta * tb ** 6
    q_x, q_y = [0, 1, 2, 3, 4], [20, 31, 45, 70, 104]
    qa, qb = expreg(q_x, q_y)
    ln_m, ln_b = reg(q_x, q_y)
    assert round(1000 * 1.05 ** 10, 2) == 1628.89 and 48000 * 0.97 == 46560 and (2480 - 2240) / 2 == (2840 - 2480) / 3 == 120
    calc = "<p class='note'><b>Calculator:</b> STAT → EDIT (L1 = x, L2 = y) → STAT → CALC → 0: ExpReg gives y = a · b^x.</p>"
    interest = plot((0, 50, 5, 10), (0, 900, 50, 100), [dict(f=lambda t: 300 * 1.04 ** t, a=0, b=28, ends=("closed", "arrow"))],
                    xlab="Years", ylab="Balance ($)")
    sections = [
        dict(title="8.1 Exponential Growth and Decay", lesson="Lesson 1 · Getting Started, Activities 1–3, Talk the Talk ✪",
             idea=f"""<p><b>Growth:</b> <i>f</i>(<i>t</i>) = <i>a</i>(1 + <i>r</i>)<sup><i>t</i></sup>. &nbsp; <b>Decay:</b>
             <i>f</i>(<i>t</i>) = <i>a</i>(1 − <i>r</i>)<sup><i>t</i></sup>. <i>a</i> = starting amount, <i>r</i> = rate as a decimal
             (5% → 0.05).</p><p><b>Compound interest</b> is exponential: <i>P</i>(<i>t</i>) = <i>P</i>₀(1 + <i>r</i>)<sup><i>t</i></sup>.
             <b>Simple interest</b> is linear: you earn the same amount each year, <i>I</i> = <i>Prt</i>.</p>""",
             example=f"""<p>$500 at 3% compounded annually: <i>P</i>(<i>t</i>) = 500(1.03)<sup><i>t</i></sup>. After 5 years:
             500(1.03)⁵ ≈ <b>$579.64</b>. &nbsp; Simple interest: 500 + 500(0.03)(5) = <b>$575</b>.</p>""",
             items=[
                 MC("A town’s population is modeled by <i>f</i>(<i>x</i>) = 3,200(1.045)<sup><i>x</i></sup>. What is the yearly rate of change?",
                    ["4.5% growth", "45% growth", "1.045% growth", "4.5% decay"], 0, why="b = 1.045 = 1 + 0.045 → 4.5% growth.",
                    tip="Subtract 1 from b, then change the decimal to a percent."),
                 OPEN("A car worth $24,000 loses 15% of its value each year. Write a function for its value <i>V</i> after <i>t</i> years.",
                      "V(t) = 24,000(0.85)<sup>t</sup>", frames=["<i>b</i> = 1 − [[0.15]] = [[0.85]] → <i>V</i>(<i>t</i>) = [[24,000]]([[0.85]])<sup><i>t</i></sup>"],
                      lines=1),
                 MC("Which description matches the graph?",
                    ["$300 at 4% simple interest: <i>I</i> = 300(0.04)<i>t</i>", "$300 at 4% compounded annually: <i>P</i> = 300(1.04)<sup><i>t</i></sup>",
                     "$400 at 3% compounded annually: <i>P</i> = 400(1.03)<sup><i>t</i></sup>", "$400 at 3% simple interest: <i>I</i> = 400(0.03)<i>t</i>"], 1,
                    fig=interest, why="It starts at 300 and curves upward (exponential), so it is compound interest on $300."),
             ]),
        dict(title="8.2 Interpreting Parameters in Context", lesson="Lesson 2 · Getting Started, Activities 1–2, Talk the Talk ✪",
             idea=f"""<p>In <i>f</i>({x}) = <i>a</i> · <i>b</i><sup>{x}</sup>: <i>a</i> is the <b>starting value</b> (at {x} = 0)
             and <i>b</i> is the <b>growth or decay factor</b> per unit of {x}. The point (1, <i>f</i>(1)) is the value after one
             period. The asymptote is {y} = 0, not {y} = <i>a</i>.</p><p>In context, the domain is usually {x} {GE} 0 (time).</p>""",
             example=f"""<p><i>f</i>({x}) = 18,000(0.92)<sup>{x}</sup>, fish in a lake {x} years after 2020: 18,000 fish in 2020;
             the population shrinks 8% each year; after 1 year 18,000(0.92) = 16,560 fish.</p>""",
             items=[
                 OPEN(f"Bacteria in a dish are modeled by <i>b</i>(<i>t</i>) = 650(1.3)<sup><i>t</i></sup>, <i>t</i> in hours. What do 650 and 1.3 mean?",
                      "650 bacteria at the start (t = 0). 1.3: the number grows by 30% each hour.",
                      frames=["650 means [[650]] bacteria at [[0]] hours.", "1.3 means they grow [[30]]% each [[hour]]."]),
                 OPEN("A piece of <i>f</i>(<i>x</i>) = 2<sup><i>x</i></sup> is graphed. Use inequalities to give its domain and range.",
                      f"Domain −2 {LE} x &lt; 3 · Range 0.25 {LE} y &lt; 8",
                      fig=plot((-3, 4, 1, 1), (0, 9, 1, 1), [dict(f=lambda t: 2 ** t, a=-2, b=3, ends=("closed", "open"))]),
                      frames=[f"Domain: [[−2]] [[≤]] {x} [[&lt;]] [[3]]", f"Range: [[0.25]] [[≤]] {y} [[&lt;]] [[8]]"]),
             ]),
        dict(title="8.3 Modeling with Exponential Functions", lesson="Lesson 3 · Activities 1–2, Talk the Talk ✪",
             idea=f"""<p>When data grows by about the <b>same percent</b> each step (ratios close to equal), model it with
             <b>exponential regression</b>. Round <i>a</i> and <i>b</i> to the hundredths, then use the model to predict.</p>{calc}""",
             example=f"""<p>{htable(('Years since 2018', sub_x), ('Subscribers', sub_y))}</p>
             <p>ExpReg: <b><i>f</i>({x}) = {nm(sa)}({nm(sb)})<sup>{x}</sup></b>. Each year the subscribers grow by about
             {round((sb - 1) * 100)}%. Predict 2024 ({x} = 6): {nm(sa)}({nm(sb)})⁶ ≈ {nm(round(sa * sb ** 6))}.</p>""",
             items=[
                 MC("Which function best models the data?" + htable((x, q_x), (y, q_y)),
                    [f"<i>f</i>({x}) = {nm(qa)}({nm(qb)})<sup>{x}</sup>", f"<i>f</i>({x}) = {nm(qb)}({nm(qa)})<sup>{x}</sup>",
                     f"<i>f</i>({x}) = {nm(ln_m)}{x} + {nm(ln_b)}", f"<i>f</i>({x}) = 20(1.05)<sup>{x}</sup>"], 0,
                    why=f"Ratios 31/20, 45/31, 70/45 … are all about 1.5, so it is exponential. ExpReg gives a ≈ {nm(qa)}, b ≈ {nm(qb)}."),
                 OPEN(f"Use <i>f</i>({x}) = {nm(qa)}({nm(qb)})<sup>{x}</sup> to predict <i>y</i> when {x} = 6.",
                      f"{nm(qa)}({nm(qb)})⁶ ≈ {nm(round(qa * qb ** 6, 1))}", frames=[f"{nm(qa)} × {nm(qb)}⁶ ≈ [[{nm(round(qa * qb ** 6, 1))}]]"], lines=1),
             ]),
    ]

    g4 = plot((-2, 8, 1, 2), (0, 9, 1, 1), [dict(f=lambda t: 6 * (1 / 3) ** t, a=-0.4, b=8)], pts=[(0, 6, "(0, 6)"), (1, 2, "(1, 2)")])
    check = [
        OPEN("The graph shows an account balance over time. The balance after 1 year is $312.<br>a. Is the interest simple or "
             "compound? How can you tell?<br>b. What was the deposit and the yearly rate? Write the equation.",
             "a. Compound: the graph curves upward (exponential). b. $300 at 4% (312 ÷ 300 = 1.04): P = 300(1.04)<sup>t</sup>",
             fig=interest, frames=["a. The graph [[curves]], so it is [[compound]] interest.",
                                   "b. Deposit $[[300]] · 312 ÷ 300 = [[1.04]] → rate [[4]]% · <i>P</i> = [[300]]([[1.04]])<sup><i>t</i></sup>"],
             lines=4),
        MC("A city’s population is modeled by <i>f</i>(<i>x</i>) = 48,000(0.97)<sup><i>x</i></sup>, where <i>x</i> is years since 2015. "
           "Which statement is <b>NOT</b> true?",
           ["The point (1, 46,560) is the population in 2016.", "The population in 2015 was 48,000.",
            "The population decreases by 3% each year.", "The function has an asymptote at y = 48,000."], 3,
           why="The asymptote of a · bˣ is y = 0. 48,000 is the y-intercept."),
        OPEN("Find <i>a</i> and <i>b</i> so that <i>f</i>(<i>x</i>) = <i>a</i> · <i>b</i><sup><i>x</i></sup> fits the table." + htable((x, [0, 1, 2, 3]), (y, ["−2", "−8", "−32", "−128"])),
             f"f(x) = −2(4)<sup>x</sup>", frames=["<i>a</i> = [[−2]] · <i>b</i> = −8 ÷ (−2) = [[4]]"], lines=1),
        OPEN("Use the labeled points to write <i>f</i>(<i>x</i>) = <i>a</i> · <i>b</i><sup><i>x</i></sup> for this graph.", f"a = 6, b = 2 ÷ 6 = ⅓ → f(x) = 6(⅓)<sup>x</sup>", fig=g4,
             frames=["<i>a</i> = [[6]] · <i>b</i> = 2 ÷ 6 = [[⅓]]"]),
        OPEN("A patient takes 500 mg of a medicine. The amount in the body decreases by 12% each hour. Write a function for the "
             "amount <i>m</i> after <i>t</i> hours.", f"m(t) = 500(0.88)<sup>t</sup>", frames=["<i>b</i> = 1 − 0.12 = [[0.88]]"], lines=1),
        OPEN("The table shows a song’s streams (in thousands). Let <i>x</i> be years since 2019."
             + htable(("Year", [2019, 2020, 2021, 2022, 2023]), ("Streams (thousands)", st_y))
             + "a. Write an exponential function that best models the data. Round to the hundredths.<br>"
               "b. What do <i>a</i> and <i>b</i> mean in this situation?<br>c. Predict the streams in 2025.",
             f"a. ExpReg: f(x) = {nm(ta)}({nm(tb)})<sup>x</sup> &nbsp; b. about {nm(ta)} thousand streams in 2019; streams grow about "
             f"{round((tb - 1) * 100)}% each year &nbsp; c. x = 6: {nm(ta)}({nm(tb)})⁶ ≈ {nm(round(tpred))} thousand",
             frames=[f"a. ExpReg: <i>a</i> ≈ [[{nm(ta)}]], <i>b</i> ≈ [[{nm(tb)}]]",
                     f"b. <i>a</i>: about [[{nm(ta)}]] thousand streams in [[2019]]. <i>b</i>: they grow about [[{round((tb - 1) * 100)}]]% each year.",
                     f"c. 2025 → x = [[6]] → {nm(ta)}({nm(tb)})⁶ ≈ [[{nm(round(tpred))}]] thousand"], lines=5,
             tip="Type x = 0, 1, 2, 3, 4 (years since 2019)."),
        OPEN("Give the domain and range of the exponential curve shown, as inequalities.",
             f"Domain 0 {LE} x &lt; 4 · Range 1 {LE} y &lt; 81",
             fig=plot((-1, 5, 1, 1), (0, 90, 5, 10), [dict(f=lambda t: 3 ** t, a=0, b=4, ends=("closed", "open"))]),
             frames=[f"Domain: [[0]] ≤ {x} [[&lt;]] [[4]] · Range: [[1]] ≤ {y} &lt; [[81]]"]),
        OPEN("Maya uses <i>f</i>(<i>x</i>) = 3,500(1.065)<sup><i>x</i></sup> for her savings account. What is the yearly interest rate as a percent?",
             "1.065 − 1 = 0.065 → 6.5%", frames=["1.065 − 1 = [[0.065]] = [[6.5]]%"], lines=1),
        OPEN("The expression (<i>x</i>⁹)(<i>x</i><sup>⅓</sup>)⁶ is equivalent to <i>x</i><sup><i>p</i></sup>. What is the value of <i>p</i>?",
             "(x^⅓)⁶ = x² → x⁹ · x² = x¹¹ → p = 11", frames=["(<i>x</i><sup>⅓</sup>)⁶ = <i>x</i><sup>[[2]]</sup> → 9 + 2 = [[11]]"], lines=1),
        OPEN("Leo deposited money in an account that earns simple interest. What is the rate of change of the balance with respect to time?"
             + htable(("Time (years)", [2, 4, 7]), ("Balance ($)", ["2,240", "2,480", "2,840"])), "(2,480 − 2,240) ÷ 2 = $120 per year",
             frames=["(2,480 − 2,240) ÷ (4 − 2) = [[240]] ÷ 2 = $[[120]] per year"]),
        ROWS("Is each situation linear or exponential?", ["Linear", "Exponential"],
             [("A salary increases by $50 each month.", 0), ("A salary increases by 5% each month.", 1),
              ("A town’s population doubles every 3 years.", 1), ("A snowbank shrinks 2 inches each day.", 0)],
             why="Same amount → linear. Same percent or factor → exponential.", tip="“By ___%” or “doubles” → exponential."),
        MC("Which describes <i>f</i>(<i>t</i>) = 900(0.82)<sup><i>t</i></sup>?", ["18% decay", "82% growth", "82% decay", "18% growth"], 0,
           why="b = 0.82 < 1 → decay; 1 − 0.82 = 0.18 = 18%."),
        OPEN("You put $1,000 in an account for 10 years at 5%. How much do you have with simple interest? With interest compounded annually?",
             "Simple: 1,000 + 1,000(0.05)(10) = $1,500 · Compound: 1,000(1.05)¹⁰ ≈ $1,628.89",
             frames=["Simple: 1,000 + 1,000(0.05)(10) = $[[1,500]]", "Compound: 1,000(1.05)¹⁰ ≈ $[[1,628.89]]"]),
    ]
    staar = [
        MC("Which describes <i>f</i>(<i>x</i>) = 2,500(1.08)<sup><i>x</i></sup>?",
           ["Starts at 2,500 and grows 8% per year", "Starts at 2,500 and grows 108% per year", "Starts at 1.08 and grows 2,500 per year",
            "Starts at 2,500 and decays 8% per year"], 0, teks="A.9(D)"),
        MC("A town of 1,200 people loses 6% of its population each year. Which function models the population after <i>x</i> years?",
           ["<i>f</i>(<i>x</i>) = 1,200(0.06)<sup><i>x</i></sup>", "<i>f</i>(<i>x</i>) = 1,200(1.06)<sup><i>x</i></sup>",
            "<i>f</i>(<i>x</i>) = 1,200(0.94)<sup><i>x</i></sup>", "<i>f</i>(<i>x</i>) = 1,200 − 0.06<i>x</i>"], 2, teks="A.9(C)"),
        MC(f"<i>f</i>(<i>t</i>) = 40(0.5)<sup><i>t</i></sup> gives the grams left after <i>t</i> hours, for 0 {LE} <i>t</i> {LE} 6. What is the range?",
           [f"0 {LE} <i>f</i>(<i>t</i>) {LE} 40", f"0.625 {LE} <i>f</i>(<i>t</i>) {LE} 40", f"0 {LE} <i>f</i>(<i>t</i>) {LE} 6",
            f"20 {LE} <i>f</i>(<i>t</i>) {LE} 40"], 1, teks="A.9(A)", why="f(6) = 40(0.5)⁶ = 0.625 and f(0) = 40."),
        OPEN("Choose the words that complete the sentence.<br><i>f</i>(<i>x</i>) = 7(0.6)<sup><i>x</i></sup> is ( increasing / decreasing ) "
             "and its <i>y</i>-intercept is ( 7 / 0.6 ).", "decreasing · 7", teks="A.9(D)", fmt="Inline choice", lines=1,
             frames=["b = 0.6 is less than 1, so it is [[decreasing]]. The y-intercept is a = [[7]]."]),
        MC(f"Which expressions are equivalent to 2{x}²? Select <b>TWO</b> correct answers.",
           [f"(8{x}⁶)<sup>⅓</sup>", rt(f"4{x}⁴"), f"2{x}⁸ ÷ {x}⁴", f"(2{x})²", f"2{x}<sup>½</sup> · {x}<sup>½</sup>"], (0, 1), teks="A.11(B)",
           why="(8x⁶)^⅓ = 2x²; √(4x⁴) = 2x². 2x⁸ ÷ x⁴ = 2x⁴; (2x)² = 4x²; 2x^½ · x^½ = 2x."),
        OPEN("Ty invests $2,000 at 4% interest compounded annually. To the nearest dollar, what is the balance after 6 years? Enter your answer.",
             f"2,000(1.04)⁶ ≈ ${round(2000 * 1.04 ** 6):,}", teks="A.9(C)", fmt="Text entry", lines=1,
             frames=[f"2,000 × 1.04⁶ ≈ $[[{round(2000 * 1.04 ** 6):,}]]"]),
    ]
    vocab = [("growth factor / decay factor", "b in a · bˣ: more than 1 grows, between 0 and 1 decays"),
             ("rate of growth or decay", "b − 1 (growth) or 1 − b (decay), written as a percent"),
             ("compound interest", "interest on the balance each period: P(1 + r)ᵗ (exponential)"),
             ("simple interest", "the same interest every year: I = Prt (linear)"),
             ("exponential regression", "the exponential function that best fits data (ExpReg)")]
    return dict(code="M4 T2", title="Using Exponential Equations", module="Module 4: Investigating Growth and Decay",
                teks="A.3B, A.3C, A.9A–E, A.11B, A.12B", vocab=vocab, sections=sections, check=check, staar=staar)


# =====================================================================================================
# MODULE 5 · TOPIC 1 · Introduction to Quadratic Functions
# =====================================================================================================
same = lambda f, g: all(abs(f(t) - g(t)) < 1e-9 for t in range(-5, 6))  # two polynomials agree -> identical


def ch9():
    P, BLUE = (-6, 6, 1, 2), "#2f6fdd"
    f1 = lambda t: -t * t + 2 * t + 8  # −(x − 4)(x + 2), vertex (1, 9)
    assert f1(4) == f1(-2) == 0 and f1(1) == 9 and f1(0) == 8
    g_f1 = plot(P, (-4, 10, 1, 2), [dict(f=f1, a=-6, b=6)])
    hb = lambda t: -16 * t * t + 48 * t
    assert hb(1.5) == 36 and hb(3) == 0
    ball = lambda: plot((0, 3.5, 0.25, 0.5), (0, 40, 5, 10), [dict(f=hb, a=0, b=3, ends=("closed", "closed"), color=RED)] if KEY else [],
                        xlab="Time (seconds)", ylab="Height (feet)")
    r1 = lambda t: -16 * t * t + 64 * t + 4
    land = (64 + (64 ** 2 + 4 * 16 * 4) ** 0.5) / 32
    assert r1(2) == 68 and round(land, 1) == 4.1
    t2 = lambda t: -16 * t * t + 32 * t + 6
    assert t2(1) == 22 and round((32 + (32 ** 2 + 4 * 16 * 6) ** 0.5) / 32, 1) == 2.2
    half = lambda t: 0.5 * (t + 5) * (t - 1)
    assert half(-2) == -4.5
    g_half = plot((-8, 4, 1, 2), (-6, 6, 1, 2), [dict(f=half, a=-8, b=4)], pts=[(-5, 0, "(−5, 0)"), (1, 0, "(1, 0)"), (-2, -4.5, "(−2, −4.5)")])
    fh = plot((-5, 5, 1, 1), (-10, 10, 1, 2), [dict(f=lambda t: t * t, a=-4, b=4, label="f(x)"),
                                               dict(f=lambda t: -2 * t * t + 8, a=-3.2, b=3.2, color=BLUE, label="h(x)")])
    pn = plot(P, (-4, 10, 1, 2), [dict(f=lambda t: t * t + 3, a=-6, b=6)], pts=[(-2, 7, "(−2, 7)"), (2, 7, "(2, 7)")])
    down = plot(P, (-6, 6, 1, 2), [dict(f=lambda t: -(t - 2) ** 2 + 3, a=-1.5, b=5.5)], pts=[(2, 3, "(2, 3)")])
    up = plot(P, (-6, 6, 1, 2), [dict(f=lambda t: (t + 2) ** 2 - 1, a=-5, b=1)], pts=[(-2, -1, "(−2, −1)")])
    assert same(lambda t: (t - 3) ** 2 - 4, lambda t: t * t - 6 * t + 5) and same(lambda t: (t + 1) ** 2 - 9, lambda t: (t + 4) * (t - 2))
    assert 2 * (0 - 2) ** 2 - 3 == 5 and -2 * (1 + 2) ** 2 + 5 == -13 and 2 * (2 - 4) ** 2 - 2 == 6 and 2 * (0 - 1) * (0 - 5) == 10
    assert same(lambda t: -2 * (t - 1) ** 2 + 4, lambda t: -2 * t * t + 4 * t + 2) and same(lambda t: t * (40 - 2 * t), lambda t: -2 * (t - 10) ** 2 + 200)
    tab = lambda ys: htable((x, [0, 1, 2, 3, 4]), (y, ys))
    sections = [
        dict(title="9.1 Exploring Quadratic Functions", lesson="Lesson 1 · Getting Started, Activities 1–4, Talk the Talk ✪",
             idea=f"""<p>A <b>quadratic function</b> has the form <i>f</i>({x}) = <i>a</i>{x}² + <i>b</i>{x} + <i>c</i> with <i>a</i> ≠ 0.
             Its graph is a <b>parabola</b>. The <b>vertex</b> is the highest point (maximum) or lowest point (minimum).</p>
             <p><b>Vertical motion:</b> <i>h</i>(<i>t</i>) = −16<i>t</i>² + <i>v</i>₀<i>t</i> + <i>h</i>₀ (feet, seconds), where <i>v</i>₀ is
             the starting speed and <i>h</i>₀ the starting height. In a story the domain and range stop where the story stops
             (time ≥ 0, height ≥ 0). The <b>function</b> itself has domain all real numbers.</p>""",
             example=f"""<p><i>g</i>(<i>t</i>) = −16<i>t</i>² + 48<i>t</i>: zeros at <i>t</i> = 0 and <i>t</i> = 3, so the vertex is halfway, at
             <i>t</i> = 1.5. <i>g</i>(1.5) = 36: <b>maximum height 36 ft at 1.5 s</b>.</p>
             <p>Situation: domain 0 {LE} <i>t</i> {LE} 3, range 0 {LE} <i>h</i> {LE} 36. &nbsp; Function: domain all real numbers, range {y} {LE} 36.</p>""",
             items=[
                 OPEN("Graph <i>g</i>(<i>t</i>) = −16<i>t</i>² + 48<i>t</i>, the height of a kicked ball after <i>t</i> seconds. Label the axes.",
                      "Parabola from (0, 0) up to the vertex (1.5, 36) and back down to (3, 0); x-axis: time (s), y-axis: height (ft).",
                      fig=ball, frames=["Points to plot: (0, [[0]]), (1.5, [[36]]), (3, [[0]])"],
                      tip="Plot the start, the top (vertex) and where it lands. Connect them with a smooth curve."),
                 OPEN("A ball is thrown from 6 feet with <i>h</i>(<i>t</i>) = −16<i>t</i>² + 32<i>t</i> + 6. It lands after about 2.2 seconds.<br>"
                      "a. What is the maximum height, and when? &nbsp; b. Write the domain and range of the situation.",
                      f"a. Vertex (1, 22): 22 ft at 1 second. b. Domain 0 {LE} t {LE} 2.2; range 0 {LE} h {LE} 22",
                      frames=["a. Calculator maximum: <i>t</i> = [[1]] s, height = [[22]] ft",
                              f"b. Domain: [[0]] {LE} <i>t</i> {LE} [[2.2]] · Range: [[0]] {LE} <i>h</i> {LE} [[22]]"], lines=4,
                      tip="On the calculator: 2nd TRACE → 4: maximum."),
                 MC("Revenue for a T-shirt sale is <i>R</i>(<i>x</i>) = <i>x</i>(40 − 2<i>x</i>), where <i>x</i> is the price in dollars. "
                    "Which price gives the most revenue?", ["$20", "$10", "$40", "$200"], 1,
                    why="Zeros at x = 0 and x = 20; the vertex is halfway, x = 10 (R = $200)."),
             ]),
        dict(title="9.2 Key Characteristics of Quadratic Functions", lesson="Lesson 2 · Getting Started, Activities 1–4, Talk the Talk ✪",
             idea=f"""<table class="t"><tr><th>Form</th><th>Equation</th><th>Shows you</th></tr>
             <tr><td>Standard</td><td><i>a</i>{x}² + <i>b</i>{x} + <i>c</i></td><td><i>y</i>-intercept (0, <i>c</i>); axis {x} = −<i>b</i> ÷ 2<i>a</i></td></tr>
             <tr><td>Factored</td><td><i>a</i>({x} − <i>r</i>₁)({x} − <i>r</i>₂)</td><td>zeros <i>r</i>₁ and <i>r</i>₂; axis halfway between</td></tr>
             <tr><td>Vertex</td><td><i>a</i>({x} − <i>h</i>)² + <i>k</i></td><td>vertex (<i>h</i>, <i>k</i>); axis {x} = <i>h</i></td></tr></table>
             <p><i>a</i> &gt; 0 opens up (minimum); <i>a</i> &lt; 0 opens down (maximum). A table is quadratic when the
             <b>second differences</b> are constant.</p>""",
             example=f"""<p><i>f</i>({x}) = ({x} − 1)({x} − 5): zeros 1 and 5; axis {x} = 3; vertex <i>f</i>(3) = (2)(−2) = −4 → (3, −4);
             <i>y</i>-intercept <i>f</i>(0) = 5 → (0, 5). Opens up: decreasing for {x} &lt; 3, increasing for {x} &gt; 3; range {y} {GE} −4.</p>""",
             items=[
                 OPEN("Identify the key characteristics of the quadratic function graphed.",
                      f"y-int (0, 8); zeros −2 and 4; axis x = 1; vertex (1, 9); increasing x &lt; 1; decreasing x &gt; 1; "
                      f"domain all real numbers; range y {LE} 9", fig=g_f1, lines=5,
                      frames=["<i>y</i>-intercept: (0, [[8]]) · zeros: [[−2]] and [[4]]", "Axis of symmetry: <i>x</i> = [[1]] · vertex: ([[1]], [[9]])",
                              "Increasing: <i>x</i> [[&lt;]] 1 · Decreasing: <i>x</i> [[&gt;]] 1", f"Range: <i>y</i> [[{LE}]] [[9]]"],
                      tip="The axis of symmetry is halfway between the zeros."),
                 MC("Which table represents a quadratic function?",
                    [tab([1, 4, 7, 10, 13]), tab([2, 4, 8, 16, 32]), tab([3, 4, 7, 12, 19]), tab([1, 2, 4, 5, 7])], 2,
                    why="First differences 1, 3, 5, 7; second differences all 2.", tip="Subtract twice. Same second differences → quadratic."),
                 OPEN(f"A quadratic function has zeros at {x} = 1 and {x} = 5 and passes through (0, 10). Write it in factored form.",
                      "10 = a(0 − 1)(0 − 5) = 5a → a = 2: f(x) = 2(x − 1)(x − 5)",
                      frames=["10 = <i>a</i>(0 − 1)(0 − 5) = [[5]]<i>a</i> → <i>a</i> = [[2]]", "<i>f</i>(<i>x</i>) = [[2]](<i>x</i> − 1)(<i>x</i> − 5)"]),
             ]),
        dict(title="9.3 Quadratic Function Transformations", lesson="Lesson 3 · Getting Started, Activities 1–3, Talk the Talk ✪",
             idea=f"""<p><i>g</i>({x}) = <i>a</i>({x} − <i>c</i>)² + <i>d</i> compared with <i>f</i>({x}) = {x}²:</p>
             <table class="t"><tr><td>({x} − <i>c</i>)</td><td>right <i>c</i> &nbsp; (({x} + <i>c</i>) → left <i>c</i>)</td></tr>
             <tr><td>+ <i>d</i></td><td>up <i>d</i> (− <i>d</i> → down)</td></tr>
             <tr><td>|<i>a</i>| &gt; 1</td><td>vertical stretch (narrower)</td></tr>
             <tr><td>0 &lt; |<i>a</i>| &lt; 1</td><td>vertical compression (wider)</td></tr>
             <tr><td><i>a</i> &lt; 0</td><td>reflection across the {x}-axis (opens down)</td></tr></table>
             <p>The vertex moves from (0, 0) to (<i>c</i>, <i>d</i>).</p>""",
             example=f"""<p><i>m</i>({x}) = −2({x} + 4)² − 1: <b>reflected across the {x}-axis, vertical stretch by 2, left 4, down 1</b>.
             Vertex (−4, −1).</p>""",
             items=[
                 OPEN(f"Describe how the graph of <i>n</i>({x}) = ½({x} − 3)² + 5 compares to the graph of <i>f</i>({x}) = {x}².",
                      "Vertical compression by ½, right 3, up 5. Vertex (3, 5).",
                      frames=["½ → vertical [[compression]] · (x − 3) → [[right]] 3 · + 5 → [[up]] 5"],
                      tip="Inside the parentheses the sign is backwards: (x − 3) moves RIGHT."),
                 OPEN(f"The graph shows <i>p</i>({x}) = {x}² + <i>n</i>. Use a labeled point to find <i>n</i>.",
                      "p(2) = 2² + n = 7 → n = 3", fig=pn, frames=["2² + <i>n</i> = 7 → [[4]] + <i>n</i> = 7 → <i>n</i> = [[3]]"], lines=2),
                 MC(f"What is the vertex of <i>g</i>({x}) = 4({x} + 1)² − 6?", ["(1, −6)", "(−1, −6)", "(−1, 6)", "(4, −6)"], 1),
             ]),
        dict(title="9.4 Horizontal Transformations and Vertex Form", lesson="Lesson 4 · Getting Started, Activities 1–4, Talk the Talk ✪",
             idea=f"""<p><b>Horizontal dilation</b> <i>f</i>(<i>b</i>{x}): |<i>b</i>| &gt; 1 squeezes the graph toward the <i>y</i>-axis
             (horizontal compression by 1/<i>b</i>); 0 &lt; |<i>b</i>| &lt; 1 stretches it out.</p>
             <p><b>Write vertex form from the vertex and one point:</b> put (<i>h</i>, <i>k</i>) into <i>a</i>({x} − <i>h</i>)² + <i>k</i>,
             plug in the point, and solve for <i>a</i>. Expand to get standard form.</p>""",
             example=f"""<p>Vertex (2, −3), through (0, 5): 5 = <i>a</i>(0 − 2)² − 3 → 4<i>a</i> = 8 → <i>a</i> = 2.
             <b><i>f</i>({x}) = 2({x} − 2)² − 3</b> = 2({x}² − 4{x} + 4) − 3 = <b>2{x}² − 8{x} + 5</b>.</p>""",
             items=[
                 OPEN("A parabola has its vertex at (−2, 5) and goes through (1, −13). Find its equation in vertex form.",
                      "−13 = a(1 + 2)² + 5 → 9a = −18 → a = −2: f(x) = −2(x + 2)² + 5",
                      frames=["−13 = <i>a</i>(1 + 2)² + 5 → [[9]]<i>a</i> = [[−18]] → <i>a</i> = [[−2]]", "<i>f</i>(<i>x</i>) = [[−2]](<i>x</i> + 2)² + 5"]),
                 MC(f"Which is <i>f</i>({x}) = ({x} − 3)² − 4 in standard form?", [f"{x}² − 6{x} + 5", f"{x}² − 6{x} + 13", f"{x}² + 5", f"{x}² − 9{x} − 4"], 0,
                    why="(x − 3)² = x² − 6x + 9; 9 − 4 = 5.", tip="(x − 3)² means (x − 3)(x − 3). Do not just square each part."),
                 MC(f"How does the graph of <i>g</i>({x}) = (3{x})² compare to the graph of <i>f</i>({x}) = {x}²?",
                    ["Horizontal compression by a factor of ⅓", "Horizontal stretch by a factor of 3", "Shifted right 3", "Shifted up 3"], 0),
             ]),
    ]

    check = [
        MC("Which best describes the domain and range of the function graphed?", [
            "Domain: all real numbers · Range: <i>y</i> ≤ 3", "Domain: <i>x</i> ≤ 2 · Range: all real numbers",
            "Domain: all real numbers · Range: <i>y</i> ≥ 3", "Domain: <i>x</i> ≥ 0 · Range: <i>y</i> ≤ 3"], 0, fig=down,
           why="A parabola always has domain all real numbers. It opens down with its top at y = 3."),
        OPEN("A model rocket’s height is <i>h</i>(<i>t</i>) = −16<i>t</i>² + 64<i>t</i> + 4 (feet, seconds).<br>"
             "a. What is the maximum height, and when? Round to the nearest tenth.<br>"
             "b. Write the domain and range of the situation. c. Write the domain and range of the function <i>h</i>(<i>t</i>).",
             f"a. 68 ft at 2 s &nbsp; b. 0 {LE} t {LE} {land:.1f}; 0 {LE} h {LE} 68 &nbsp; c. all real numbers; y {LE} 68",
             frames=["a. Maximum: <i>t</i> = [[2]] s, height [[68]] ft",
                     f"b. Lands at <i>t</i> ≈ [[{land:.1f}]] → domain 0 {LE} <i>t</i> {LE} {land:.1f}, range [[0]] {LE} <i>h</i> {LE} [[68]]",
                     f"c. Domain: [[all real numbers]] · Range: <i>y</i> {LE} [[68]]"], lines=5,
             tip="The situation stops when the rocket hits the ground (h = 0). The function keeps going."),
        OPEN(f"For <i>f</i>({x}) = {x}² + 2{x} − 3 = ({x} + 3)({x} − 1), identify the zeros, <i>y</i>-intercept, axis of symmetry, vertex, "
             "and intervals of increase and decrease.",
             "zeros −3, 1; y-int (0, −3); axis x = −1; vertex (−1, −4); decreasing x &lt; −1; increasing x &gt; −1", lines=5,
             frames=["Zeros: [[−3]] and [[1]] · <i>y</i>-intercept (0, [[−3]])", "Axis <i>x</i> = [[−1]] · vertex <i>f</i>(−1) = ([[−1]], [[−4]])",
                     "Opens up: decreasing <i>x</i> &lt; [[−1]], increasing <i>x</i> &gt; [[−1]]"]),
        OPEN("Use the labeled zeros and vertex to write the parabola in factored form, <i>a</i>(<i>x</i> − <i>r</i>₁)(<i>x</i> − <i>r</i>₂).",
             "f(x) = a(x + 5)(x − 1); −4.5 = a(3)(−3) → a = 0.5: f(x) = ½(x + 5)(x − 1)", fig=g_half,
             frames=["<i>f</i>(<i>x</i>) = <i>a</i>(<i>x</i> + [[5]])(<i>x</i> − [[1]])", "−4.5 = <i>a</i>(3)(−3) = [[−9]]<i>a</i> → <i>a</i> = [[½]]"],
             tip="Use the vertex as the point to find a."),
        OPEN(f"Describe how the graph of <i>m</i>({x}) = −({x} − 5)² − 2 compares to the graph of <i>f</i>({x}) = {x}².",
             "Reflected across the x-axis, right 5, down 2. Vertex (5, −2).",
             frames=["− in front → [[reflection]] across the x-axis · (x − 5) → [[right]] 5 · − 2 → [[down]] 2"]),
        OPEN("The graph shows <i>f</i>(<i>x</i>) = <i>x</i>² and a transformed function <i>h</i>(<i>x</i>). Describe the transformations.",
             "h(x) = −2x² + 8: reflection across the x-axis, vertical stretch by 2, up 8", fig=fh,
             frames=["<i>h</i> opens [[down]] → reflection · it is [[narrower]] → vertical stretch · vertex (0, [[8]]) → up 8"]),
        OPEN("Find the vertex form of the parabola through (2, 6) whose vertex is (4, −2).",
             "6 = a(2 − 4)² − 2 → 4a = 8 → a = 2: f(x) = 2(x − 4)² − 2",
             frames=["6 = <i>a</i>(2 − 4)² − 2 → [[4]]<i>a</i> = [[8]] → <i>a</i> = [[2]]"]),
        MC("Which function’s graph is <i>f</i>(<i>x</i>) = <i>x</i>² shifted 3 units left and 4 units down?",
           [f"({x} − 3)² − 4", f"({x} + 3)² − 4", f"({x} + 4)² − 3", f"({x} − 3)² + 4"], 1),
        MC(f"What is the vertex of <i>f</i>({x}) = −3({x} − 1)² + 8, and is it a maximum or a minimum?",
           ["(1, 8), maximum", "(1, 8), minimum", "(−1, 8), maximum", "(8, 1), minimum"], 0, why="a = −3 &lt; 0 → opens down → maximum."),
        MC("Which table shows a quadratic relationship?",
           [tab([0, 1, 4, 9, 16]), tab([5, 8, 11, 14, 17]), tab([1, 3, 9, 27, 81]), tab([0, 2, 3, 5, 8])], 0,
           why="Second differences: 2, 2, 2."),
        ROWS("Which form is each function written in?", ["Standard", "Factored", "Vertex"],
             [(f"−3({x} + 1)({x} − 6)", 1), (f"2{x}² − 5{x} + 1", 0), (f"½({x} − 4)² + 3", 2), (f"−({x} + 2)² − 9", 2)]),
        OPEN("Write the intervals where the function graphed is increasing and decreasing.", "decreasing x &lt; −2; increasing x &gt; −2",
             fig=up, frames=["Decreasing: <i>x</i> [[&lt;]] [[−2]] · Increasing: <i>x</i> [[&gt;]] [[−2]]"], lines=2,
             tip="Read the graph left to right: going down, then going up."),
        OPEN(f"Write <i>f</i>({x}) = ({x} + 1)² − 9 in standard form and in factored form. What are the zeros?",
             "x² + 2x − 8 = (x + 4)(x − 2); zeros −4 and 2",
             frames=["Standard: <i>x</i>² + [[2]]<i>x</i> − [[8]]", "Factored: (<i>x</i> + [[4]])(<i>x</i> − [[2]]) · zeros [[−4]] and [[2]]"]),
        MC(f"How does <i>g</i>({x}) = (½{x})² compare to <i>f</i>({x}) = {x}²?",
           ["Horizontal stretch by a factor of 2", "Horizontal compression by a factor of ½", "Shifted left ½", "Reflected across the y-axis"], 0),
        OPEN(f"The graph of <i>p</i>({x}) = {x}² + <i>n</i> passes through (−3, 4). What is <i>n</i>?", "9 + n = 4 → n = −5",
             frames=["(−3)² + <i>n</i> = 4 → [[9]] + <i>n</i> = 4 → <i>n</i> = [[−5]]"], lines=1),
    ]
    staar = [
        MC("What is the range of <i>f</i>(<i>x</i>) = 2(<i>x</i> + 1)² − 3?", ["All real numbers", "<i>y</i> ≥ −3", "<i>y</i> ≤ −3", "<i>y</i> ≥ −1"], 1,
           teks="A.6(A)", why="a = 2 &gt; 0: opens up from the vertex (−1, −3)."),
        MC(f"What is the axis of symmetry of <i>y</i> = 2{x}² − 12{x} + 7?", [f"{x} = −3", f"{x} = 3", f"{x} = 6", f"{x} = 12"], 1, teks="A.7(A)",
           why="x = −b ÷ 2a = 12 ÷ 4 = 3."),
        MC("The graph of <i>g</i>(<i>x</i>) = <i>f</i>(<i>x</i> − 2) + 5 is the graph of <i>f</i> moved —", ["left 2 and up 5", "right 2 and up 5",
                                                                                                       "right 5 and up 2", "left 2 and down 5"], 1, teks="A.7(C)"),
        OPEN("A parabola has vertex (1, 4) and passes through (3, −4). Written as <i>ax</i>² + <i>bx</i> + <i>c</i>, what is the value of <i>c</i>? Enter your answer.",
             "a(2)² + 4 = −4 → a = −2; −2(x − 1)² + 4 = −2x² + 4x + 2 → c = 2", teks="A.6(B)", fmt="Text entry", lines=2,
             frames=["<i>a</i>(3 − 1)² + 4 = −4 → <i>a</i> = [[−2]]", "−2(<i>x</i> − 1)² + 4 = −2<i>x</i>² + 4<i>x</i> + [[2]]"]),
        MC(f"Which statements are true about <i>f</i>({x}) = −({x} + 1)({x} − 5)? Select <b>TWO</b> correct answers.",
           ["The zeros are −1 and 5.", "The vertex is (2, 9).", "The graph opens up.", "The <i>y</i>-intercept is (0, −5).", "The axis of symmetry is <i>x</i> = 3."],
           (0, 1), teks="A.7(A)", why="f(2) = −(3)(−3) = 9; f(0) = −(1)(−5) = 5; axis x = (−1 + 5) ÷ 2 = 2."),
        MC("A quadratic function has zeros at 2 and 6, and its graph passes through (4, −8). Which is the function?",
           [f"<i>f</i>({x}) = 2({x} − 2)({x} − 6)", f"<i>f</i>({x}) = −2({x} − 2)({x} − 6)", f"<i>f</i>({x}) = 2({x} + 2)({x} + 6)",
            f"<i>f</i>({x}) = ({x} − 2)({x} − 6)"], 0, teks="A.6(C)", why="a(2)(−2) = −8 → a = 2."),
    ]
    assert -(-1 + 1) * (-1 - 5) == 0 and 2 * (4 - 2) * (4 - 6) == -8
    vocab = [("quadratic function", "f(x) = ax² + bx + c, a ≠ 0; its graph is a parabola"),
             ("vertex", "the turning point: the maximum or minimum of a parabola"),
             ("axis of symmetry", "the vertical line through the vertex that splits the parabola in half"),
             ("zeros / x-intercepts", "where the graph crosses the x-axis (f(x) = 0)"),
             ("standard / factored / vertex form", "ax² + bx + c / a(x − r₁)(x − r₂) / a(x − h)² + k"),
             ("second differences", "differences of the differences; constant → quadratic")]
    return dict(code="M5 T1", title="Introduction to Quadratic Functions", module="Module 5: Maximizing and Minimizing",
                teks="A.6A–C, A.7A, A.7C", vocab=vocab, sections=sections, check=check, staar=staar)


# =====================================================================================================
# MODULE 5 · TOPIC 2 · Polynomial Operations
# =====================================================================================================
def ch10():
    a_, b_, k_, m_, p_, r_, w_, u_ = (i(c) for c in "abkmprwu")
    area = lambda r, c, cells: ('<table class="t"><tr><th>·</th>' + "".join(f"<th>{v}</th>" for v in c) + "</tr>"
                                + "".join(f"<tr><th>{rv}</th>" + "".join(f"<td>{blanks(cells[ri][ci]) if '[[' in cells[ri][ci] else cells[ri][ci]}</td>"
                                                                          for ci in range(len(c))) + "</tr>" for ri, rv in enumerate(r)) + "</table>")
    for f, g in [  # every product / quotient / sum in this chapter
        (lambda t: (4 * t * t - 3 * t + 7) - (t * t - 5 * t - 2), lambda t: 3 * t * t + 2 * t + 9),
        (lambda t: (2 * t + 3) * (4 * t - 5), lambda t: 8 * t * t + 2 * t - 15),
        (lambda t: -3 * t * (2 * t * t - 5 * t + 6), lambda t: -6 * t ** 3 + 15 * t * t - 18 * t),
        (lambda t: (5 * t - 2) * (2 * t + 7), lambda t: 10 * t * t + 31 * t - 14),
        (lambda t: (3 * t - 5) ** 2, lambda t: 9 * t * t - 30 * t + 25),
        (lambda t: (t + 3) * (2 * t + 1), lambda t: 2 * t * t + 7 * t + 3),
        (lambda t: (t - 2) * (t + 6) + 11, lambda t: t * t + 4 * t - 1),
        (lambda t: (t - 4) * (t + 3), lambda t: t * t - t - 12),
        (lambda t: (t + 2) * (3 * t - 2) - 1, lambda t: 3 * t * t + 4 * t - 5),
        (lambda t: (2 * t - 3) * (t + 4), lambda t: 2 * t * t + 5 * t - 12),
        (lambda t: (t + 2) * (4 * t - 3) + 3, lambda t: 4 * t * t + 5 * t - 3),
        (lambda t: (2 * t * t + 3) + (-t * t + 4 * t) + (5 * t - 1), lambda t: t * t + 9 * t + 2),
        (lambda t: -2 * t * (5 * t * t + 3 * t - 7), lambda t: -10 * t ** 3 - 6 * t * t + 14 * t),
        (lambda t: (t + 5) * (t - 5), lambda t: t * t - 25),
        (lambda t: (4 * t - 3) * (2 * t + 5), lambda t: 8 * t * t + 14 * t - 15),
        (lambda t: (3 * t * t + t) + (t * t - 4 * t + 2) - (5 * t - 6), lambda t: 4 * t * t - 8 * t + 8),
        (lambda t: (2 * t + 7) ** 2, lambda t: 4 * t * t + 28 * t + 49),
        (lambda t: (2 * t - 1) * (2 * t + 3), lambda t: 4 * t * t + 4 * t - 3),
        (lambda t: (t - 4) * (t * t + 2 * t - 3), lambda t: t ** 3 - 2 * t * t - 11 * t + 12),
        (lambda t: (-2 * t * t + 80 * t) - (10 * t + 300), lambda t: -2 * t * t + 70 * t - 300),
        (lambda t: 2 * (t - 3) ** 2 + 1, lambda t: 2 * t * t - 12 * t + 19),
        (lambda t: (3 * t * t - 7 * t + 2) + (-5 * t * t + t - 9), lambda t: -2 * t * t - 6 * t - 7),
        (lambda t: (2 * t - 5) * (3 * t + 4), lambda t: 6 * t * t - 7 * t - 20),
        (lambda t: (3 * t - 1) * (2 * t + 3), lambda t: 6 * t * t + 7 * t - 3),
        (lambda t: 3 * t * (2 * t - 5) - 4 * (2 * t - 5), lambda t: 6 * t * t - 23 * t + 20),
        (lambda t: (t + 4) * (t * t - t + 2), lambda t: t ** 3 + 3 * t * t - 2 * t + 8),
        (lambda t: (t + 9) * (t - 9), lambda t: t * t - 81),
    ]:
        assert same(f, g)
    rem = lambda q, d, r: f"{q} {'+' if r > 0 else '−'} {fr(abs(r), d)}"
    sections = [
        dict(title="10.1 Adding and Subtracting Polynomials", lesson="Lesson 1 · Getting Started, Activities 1 and 4 ✪",
             idea=f"""<p>A <b>polynomial</b> is a sum of terms like 5{x}³ or −2{x} or 7. <b>Monomial</b> = 1 term, <b>binomial</b> = 2 terms,
             <b>trinomial</b> = 3 terms. The <b>degree</b> is the largest exponent. <b>Standard form</b>: exponents from largest to smallest.</p>
             <p><b>Add:</b> combine like terms (same variable, same exponent). <b>Subtract:</b> change the sign of <u>every</u> term
             in the second polynomial, then add.</p>""",
             example=f"""<p>(4{x}² − 3{x} + 7) − ({x}² − 5{x} − 2) = 4{x}² − 3{x} + 7 <b>− {x}² + 5{x} + 2</b> = <b>3{x}² + 2{x} + 9</b></p>""",
             items=[
                 MC(f"Which expression is the difference (2{x}² + 5{x} − 1) − (2{x}² − 4{x} − 1)?", [f"9{x}", f"{x}", f"4{x}² + 9{x} − 2", f"9{x} − 2"], 0,
                    why="2x² − 2x² = 0; 5x − (−4x) = 9x; −1 − (−1) = 0.", tip="Change every sign in the second ( ), then combine."),
                 OPEN(f"A rectangle has length 3{w_}² − 2 and width 5{w_} + 4. Write its perimeter in simplest form.",
                      f"2(3w² − 2) + 2(5w + 4) = 6w² + 10w + 4",
                      frames=[f"2(3{w_}² − 2) + 2(5{w_} + 4) = [[6]]{w_}² + [[10]]{w_} + [[4]]"], lines=2),
                 ROWS("Name each polynomial by its number of terms.", ["Monomial", "Binomial", "Trinomial"],
                      [(f"7{x}³", 0), (f"{x}² − 9", 1), (f"4{y}² + {y} − 2", 2), ("−5", 0)]),
             ]),
        dict(title="10.2 Multiplying Polynomials", lesson="Lesson 2 · Activities 2–4, Talk the Talk ✪",
             idea=f"""<p>Multiply <b>every</b> term by <b>every</b> term (distributive property or an area model), then combine like terms.</p>
             <p><b>Special products:</b> (<i>a</i> + <i>b</i>)² = <i>a</i>² + 2<i>ab</i> + <i>b</i>² &nbsp;·&nbsp;
             (<i>a</i> − <i>b</i>)² = <i>a</i>² − 2<i>ab</i> + <i>b</i>² &nbsp;·&nbsp; (<i>a</i> + <i>b</i>)(<i>a</i> − <i>b</i>) = <i>a</i>² − <i>b</i>²</p>""",
             example=f"""<p>(2{x} + 3)(4{x} − 5):</p>{area([f"2{x}", "3"], [f"4{x}", "−5"], [[f"8{x}²", f"−10{x}"], [f"12{x}", "−15"]])}
             <p>8{x}² − 10{x} + 12{x} − 15 = <b>8{x}² + 2{x} − 15</b></p>""",
             items=[
                 OPEN(f"Multiply −3{b_}(2{b_}² − 5{b_} + 6).", "−6b³ + 15b² − 18b",
                      frames=[f"−3{b_} · 2{b_}² = [[−6{b_}³]] · −3{b_} · (−5{b_}) = [[15{b_}²]] · −3{b_} · 6 = [[−18{b_}]]"], lines=1,
                      tip="Negative times negative is positive."),
                 OPEN(f"Use the area model to multiply (5{k_} − 2)(2{k_} + 7). Combine like terms.",
                      "10k² + 35k − 4k − 14 = 10k² + 31k − 14",
                      fig=lambda: area([f"5{k_}", "−2"], [f"2{k_}", "7"], [["[[10<i>k</i>²]]", "[[35<i>k</i>]]"], ["[[−4<i>k</i>]]", "[[−14]]"]]),
                      frames=[f"Combine: 10{k_}² + [[31]]{k_} − [[14]]"]),
                 MC("Which is equivalent to (3<i>n</i> − 5)²?", ["9<i>n</i>² + 25", "9<i>n</i>² − 30<i>n</i> + 25", "9<i>n</i>² − 15<i>n</i> + 25",
                                                                 "9<i>n</i>² − 30<i>n</i> − 25"], 1,
                    why="(a − b)² = a² − 2ab + b²: 2 · 3n · 5 = 30n.", tip="Write it twice: (3n − 5)(3n − 5)."),
             ]),
        dict(title="10.3 Polynomial Division", lesson="Lesson 3 · Activities 1–2, Talk the Talk ✪",
             idea=f"""<p><b>Factor Theorem:</b> ({x} − <i>r</i>) is a factor of <i>f</i>({x}) exactly when <i>f</i>(<i>r</i>) = 0. So
             ({x} + 2) is a factor when <i>f</i>(−2) = 0.</p><p><b>Long division:</b> divide the first terms, multiply, subtract,
             bring down, repeat. <b>Remainder Theorem:</b> the remainder from dividing by ({x} − <i>r</i>) is <i>f</i>(<i>r</i>).
             Write the answer as quotient + {fr('remainder', 'divisor')}.</p>""",
             example=f"""<p>(2{x}² + 7{x} + 3) ÷ ({x} + 3): <i>f</i>(−3) = 18 − 21 + 3 = 0, so ({x} + 3) is a factor. 2{x}² ÷ {x} = 2{x};
             2{x}({x} + 3) = 2{x}² + 6{x}; subtract → {x} + 3; {x} ÷ {x} = 1 → <b>2{x} + 1</b>.</p>
             <p>({x}² + 4{x} − 1) ÷ ({x} − 2) = <b>{rem(f'{x} + 6', f'{x} − 2', 11)}</b> &nbsp; (check: <i>f</i>(2) = 11 = the remainder).</p>""",
             items=[
                 OPEN(f"Use the Factor Theorem to test whether ({x} − 4) is a factor of <i>f</i>({x}) = {x}² − {x} − 12. If it is, find the other factor.",
                      "f(4) = 16 − 4 − 12 = 0, so yes. Quotient: x + 3.",
                      frames=["<i>f</i>(4) = 16 − 4 − 12 = [[0]] → it [[is]] a factor", "Quotient: <i>x</i> + [[3]]"],
                      tip="Plug in the number that makes the factor zero."),
                 MC(f"Which is the quotient (3{x}² + 4{x} − 5) ÷ ({x} + 2)?",
                    [f"3{x} − 2", rem(f"3{x} − 2", f"{x} + 2", -1), rem(f"3{x} + 10", f"{x} + 2", 15), rem(f"3{x} − 2", f"{x} + 2", 1)], 1,
                    why="(x + 2)(3x − 2) = 3x² + 4x − 4; −5 − (−4) = −1."),
                 OPEN(f"Divide (2{y}² + 5{y} − 12) ÷ (2{y} − 3).", "y + 4", frames=[f"2{y}² ÷ 2{y} = [[{y}]] · then 8{y} ÷ 2{y} = [[4]]"], lines=2),
             ]),
    ]
    check = [
        MC(f"Which expression is the difference (5{x}² − 2{x} + 8) − (5{x}² + 4{x} + 8)?", [f"−6{x}", f"2{x}", f"10{x}² + 2{x} + 16", f"−6{x} + 16"], 0),
        MC(f"Which is the quotient (4{x}² + 5{x} − 3) ÷ ({x} + 2)?",
           [rem(f"4{x} − 3", f"{x} + 2", 3), f"4{x} − 3", rem(f"4{x} − 3", f"{x} + 2", -3), rem(f"4{x} + 13", f"{x} + 2", 23)], 0,
           why="(x + 2)(4x − 3) = 4x² + 5x − 6; −3 − (−6) = 3."),
        OPEN(f"A triangle has sides 2{m_}² + 3, −{m_}² + 4{m_}, and 5{m_} − 1. Write its perimeter in simplest form.", "m² + 9m + 2",
             frames=[f"{m_}² terms: 2 − 1 = [[1]] · {m_} terms: 4 + 5 = [[9]] · numbers: 3 − 1 = [[2]]"], lines=2),
        OPEN(f"Multiply −2{p_}(5{p_}² + 3{p_} − 7).", "−10p³ − 6p² + 14p",
             frames=[f"[[−10]]{p_}³ [[−]] 6{p_}² + [[14]]{p_}"], lines=1),
        OPEN(f"Plug in one number to decide whether ({x} + 3) divides <i>f</i>({x}) = {x}² − 2{x} − 15 evenly. Then find the quotient.",
             "f(−3) = 9 + 6 − 15 = 0 → yes (Factor Theorem). Quotient x − 5.",
             frames=["<i>f</i>(−3) = 9 + 6 − 15 = [[0]] → yes", "Quotient: <i>x</i> − [[5]]"]),
        OPEN(f"Fill in the area model for (4{r_} − 3)(2{r_} + 5), then write the product with like terms combined.", "8r² + 20r − 6r − 15 = 8r² + 14r − 15",
             fig=lambda: area([f"4{r_}", "−3"], [f"2{r_}", "5"], [["[[8<i>r</i>²]]", "[[20<i>r</i>]]"], ["[[−6<i>r</i>]]", "[[−15]]"]]),
             frames=[f"8{r_}² + [[14]]{r_} − [[15]]"]),
        OPEN(f"Given <i>P</i>({x}) = 3{x}² + {x}, <i>Q</i>({x}) = {x}² − 4{x} + 2, and <i>R</i>({x}) = 5{x} − 6, find <i>P</i>({x}) + <i>Q</i>({x}) − <i>R</i>({x}) in standard form.",
             "4x² − 8x + 8", frames=[f"[[4]]{x}² − [[8]]{x} + [[8]]"], tip="Subtracting R: −5x and +6.", lines=3),
        OPEN(f"A square has side length (2{y} + 7) inches. Write its area in standard form.", "(2y + 7)² = 4y² + 28y + 49",
             frames=[f"(2{y} + 7)(2{y} + 7) = [[4]]{y}² + [[28]]{y} + [[49]]"], lines=2),
        OPEN(f"Simplify the quotient {fr(f'{x}² − 64', f'{x} − 8')}.", "(x − 8)(x + 8) ÷ (x − 8) = x + 8",
             frames=[f"{x}² − 64 = ({x} − 8)({x} + [[8]]) → [[{x} + 8]]"], lines=1, tip="x² − 64 is a difference of squares."),
        OPEN(f"Divide (4{m_}² + 4{m_} − 3) ÷ (2{m_} − 1).", "2m + 3", frames=[f"(2{m_} − 1)(2{m_} + [[3]])"], lines=2),
        MC(f"Which is equivalent to ({x} + 9)({x} − 9)?", [f"{x}² − 81", f"{x}² + 81", f"{x}² − 18{x} − 81", f"{x}² − 18"], 0),
        ROWS("Classify each polynomial by its degree.", ["Linear (1)", "Quadratic (2)", "Cubic (3)"],
             [(f"4{x} − 7", 0), (f"{x}³ + 2", 2), (f"6 − {x}²", 1), (f"2{x}({x} + 1)", 1)], tip="Multiply out first, then find the biggest exponent."),
        MC(f"Which is equivalent to ({x} − 4)({x}² + 2{x} − 3)?",
           [f"{x}³ − 2{x}² − 11{x} + 12", f"{x}³ + 2{x}² − 3{x} − 4", f"{x}³ − 2{x}² − 5{x} + 12", f"{x}³ + 6{x}² + 5{x} + 12"], 0),
        OPEN(f"A club’s revenue is <i>R</i>({x}) = −2{x}² + 80{x} and its cost is <i>C</i>({x}) = 10{x} + 300. Profit is revenue minus cost. "
             f"Write the profit function <i>P</i>({x}).", "−2x² + 70x − 300", frames=[f"−2{x}² + [[70]]{x} − [[300]]"], lines=2),
        MC(f"What is the remainder when {x}² + 3{x} + 7 is divided by ({x} − 1)?", ["7", "11", "5", "0"], 1, why="Remainder Theorem: f(1) = 1 + 3 + 7 = 11."),
        OPEN(f"Write <i>f</i>({x}) = 2({x} − 3)² + 1 in standard form.", "2(x² − 6x + 9) + 1 = 2x² − 12x + 19",
             frames=[f"2({x}² − [[6]]{x} + [[9]]) + 1 = 2{x}² − [[12]]{x} + [[19]]"], lines=2),
    ]
    staar = [
        MC(f"Which is equivalent to (3{x}² − 7{x} + 2) + (−5{x}² + {x} − 9)?", [f"−2{x}² − 6{x} − 7", f"8{x}² − 8{x} + 11", f"−2{x}² − 8{x} − 7",
                                                                               f"−15{x}² − 7{x} − 18"], 0, teks="A.10(A)"),
        MC(f"Which is equivalent to (2{x} − 5)(3{x} + 4)?", [f"6{x}² − 20", f"6{x}² − 7{x} − 20", f"6{x}² + 7{x} − 20", f"6{x}² − 23{x} − 20"], 1, teks="A.10(B)"),
        MC(f"What is the quotient (6{x}² + 7{x} − 3) ÷ (3{x} − 1)?", [f"2{x} − 3", f"2{x} + 3", f"3{x} + 2", f"2{x} + 7"], 1, teks="A.10(C)"),
        MC(f"Which expressions are equivalent to 3{x}(2{x} − 5) − 4(2{x} − 5)? Select <b>TWO</b> correct answers.",
           [f"6{x}² − 23{x} + 20", f"(3{x} − 4)(2{x} − 5)", f"6{x}² − 7{x} + 20", f"6{x}² − 23{x} − 20", f"(3{x} + 4)(2{x} − 5)"], (0, 1), teks="A.10(D)"),
        OPEN(f"When ({x} + 4)({x}² − {x} + 2) is written in standard form, what is the coefficient of the {x}² term? Enter your answer.",
             "x³ + 3x² − 2x + 8 → 3", teks="A.10(B)", fmt="Text entry", lines=2,
             frames=[f"{x} · (−{x}) = −{x}² and 4 · {x}² = 4{x}² → −1 + 4 = [[3]]"]),
        MC(f"A rectangle has length {x}² + 3 and width 2{x} − 1. What is its perimeter?",
           [f"2{x}² + 4{x} + 4", f"{x}² + 2{x} + 2", f"2{x}³ − {x}² + 6{x} − 3", f"2{x}² + 4{x} + 2"], 0, teks="A.10(A)",
           why="2(x² + 3) + 2(2x − 1) = 2x² + 6 + 4x − 2."),
    ]
    vocab = [("polynomial", "a sum of terms with whole-number exponents"),
             ("monomial / binomial / trinomial", "1 term / 2 terms / 3 terms"),
             ("degree", "the largest exponent in the polynomial"),
             ("like terms", "same variable with the same exponent (3x² and −5x²)"),
             ("Factor Theorem", "(x − r) is a factor of f(x) when f(r) = 0"),
             ("difference of squares", "a² − b² = (a + b)(a − b)")]
    return dict(code="M5 T2", title="Polynomial Operations", module="Module 5: Maximizing and Minimizing",
                teks="A.10A–D", vocab=vocab, sections=sections, check=check, staar=staar)


# =====================================================================================================
# MODULE 5 · TOPIC 3 · Solving Quadratic Equations
# =====================================================================================================
def qreg(xs, ys):  # calculator QuadReg: least squares y = ax² + bx + c, exact (Fractions), rounded to hundredths
    S = lambda k: sum(Fr(v) ** k for v in xs)
    T = lambda k: sum(Fr(v) ** k * Fr(w) for v, w in zip(xs, ys))
    M = [[S(4), S(3), S(2), T(2)], [S(3), S(2), S(1), T(1)], [S(2), S(1), S(0), T(0)]]
    for c in range(3):  # Gauss-Jordan
        M[c] = [v / M[c][c] for v in M[c]]
        for r in range(3):
            if r != c:
                M[r] = [p - M[r][c] * q for p, q in zip(M[r], M[c])]
    return tuple(round(float(M[r][3]), 2) for r in range(3))


assert qreg([0, 1, 2, 3], [1, 2, 5, 10]) == (1, 0, 1)


def ch11():
    G = (-8, 8, 1, 2)
    sq = lambda f, a, b: lambda: plot(G, G, [dict(f=f, a=a, b=b, color=RED)] if KEY else [])
    vx = list(range(0, 21, 2))
    vy = [186, 265, 352, 413, 429, 453, 439, 426, 362, 308, 225]
    va, vb, vc = qreg(vx, vy)
    vm, vb0 = reg(vx, vy)
    ea, eb = expreg(vx, vy)
    vpred = va * 22 ** 2 + vb * 22 + vc
    bx, by = [0, 0.5, 1, 1.5, 2, 2.5], [5, 24, 35, 38, 33, 20]
    ba, bb, bc = qreg(bx, by)
    bt = -bb / (2 * ba)
    bh = ba * bt ** 2 + bb * bt + bc
    lm, lb = reg(bx, by)
    for f, g in [(lambda t: (2 * t - 3) * (t + 5), lambda t: 2 * t * t + 7 * t - 15), (lambda t: 3 * (t - 4) * (t + 4), lambda t: 3 * t * t - 48),
                 (lambda t: (2 * t + 5) * (2 * t - 3), lambda t: 4 * t * t + 4 * t - 15), (lambda t: (3 * t + 4) * (t + 2), lambda t: 3 * t * t + 10 * t + 8),
                 (lambda t: 5 * (t - 3) * (t + 3), lambda t: 5 * t * t - 45), (lambda t: (3 * t - 4) * (2 * t + 3), lambda t: 6 * t * t + t - 12),
                 (lambda t: (2 * t + 3) * (t - 5), lambda t: 2 * t * t - 7 * t - 15), (lambda t: (2 * t - 5) * (3 * t + 2), lambda t: 6 * t * t - 11 * t - 10),
                 (lambda t: 4 * (t - 3) * (t + 3), lambda t: 4 * t * t - 36), (lambda t: (t + 6) * (t - 4), lambda t: t * t + 2 * t - 24),
                 (lambda t: (t - 8) * (t + 2), lambda t: t * t - 6 * t - 16), (lambda t: (t - 4) * (t + 2), lambda t: t * t - 2 * t - 8),
                 (lambda t: -16 * (t - 3) * (t + 1), lambda t: -16 * t * t + 32 * t + 48)]:
        assert same(f, g)
    for v, s in [(1, lambda t: t * t + 10 * t - 11), (-11, lambda t: t * t + 10 * t - 11), (1, lambda t: t * t + 14 * t - 15), (-15, lambda t: t * t + 14 * t - 15)]:
        assert s(v) == 0
    r = lambda v: abs(v) < 1e-9
    assert r(-0.5 * (-1 + 2 * 3 ** 0.5 + 1) ** 2 + 6) and r(2 * (3 + 5 ** 0.5 - 3) ** 2 - 10) and r((3 + 7 ** 0.5) ** 2 - 6 * (3 + 7 ** 0.5) + 2)
    assert r(-0.5 * (3 + 2 * 2 ** 0.5 - 3) ** 2 + 4) and r((2 + 7 ** 0.5) ** 2 - 4 * (2 + 7 ** 0.5) - 3) and r((3 + 5 ** 0.5) ** 2 - 6 * (3 + 5 ** 0.5) + 4)
    assert 2 * 6 ** 2 - 11 == 61 and 7 * 4 ** 2 + 4 == 116 and 16 * 9 == 144 and 64 * 3 == 192 and 100 * 3 == 300
    q1 = [round((5 + s * 37 ** 0.5) / 6, 2) for s in (1, -1)]
    q0 = [round((-3 + s * 41 ** 0.5) / 4, 2) for s in (1, -1)]
    calc = "<p class='note'><b>Calculator:</b> STAT → EDIT (L1 = x, L2 = y) → STAT → CALC → 5: QuadReg gives y = ax² + bx + c.</p>"
    g14 = plot(G, G, [dict(f=lambda t: (t + 1) * (t - 4), a=-2.5, b=5.5)], pts=[(-1, 0), (4, 0)])
    sections = [
        dict(title="11.1 Representing Solutions to Quadratic Equations", lesson="Lesson 1 · Getting Started, Activities 1–2, Talk the Talk ✪",
             idea=f"""<p><b>Square root method:</b> get {x}² alone, then take the square root of both sides. Remember <b>±</b>:
             {x}² = 25 → {x} = 5 or {x} = −5.</p><p><b>Zero Product Property:</b> if <i>A</i> · <i>B</i> = 0, then <i>A</i> = 0 or <i>B</i> = 0.
             So the zeros of a quadratic function are the zeros of its <b>linear factors</b>.</p>""",
             example=f"""<p>3{x}² − 5 = 70 → 3{x}² = 75 → {x}² = 25 → <b>{x} = ±5</b>.</p>
             <p>({x} − 2)({x} + 7) = 0 → {x} − 2 = 0 or {x} + 7 = 0 → <b>{x} = 2 or {x} = −7</b>.</p>""",
             items=[
                 MC(f"What are the solutions of (2{x} − 3)({x} + 4) = 0?", [f"{x} = 3 and {x} = −4", f"{x} = {fr(3, 2)} and {x} = −4",
                                                                            f"{x} = −{fr(3, 2)} and {x} = 4", f"{x} = −3 and {x} = 4"], 1,
                    why="2x − 3 = 0 → x = 3/2; x + 4 = 0 → x = −4.", tip="Set EACH factor equal to 0."),
                 OPEN(f"Solve 2{x}² − 11 = 61.", "2x² = 72 → x² = 36 → x = ±6",
                      frames=[f"2{x}² = [[72]] → {x}² = [[36]] → {x} = [[±6]]"], lines=1),
                 OPEN(f"Write {rt(192)} in simplest radical form.", f"√(64 · 3) = 8{rt(3)}", frames=[f"{rt('[[64]] · 3')} = [[8]]{rt(3)}"], lines=1),
             ]),
        dict(title="11.2 Solutions to Quadratic Equations in Vertex Form", lesson="Lesson 2 · Getting Started, Activities 1–3, Talk the Talk ✪",
             idea=f"""<p>Solve <i>a</i>({x} − <i>h</i>)² + <i>k</i> = 0: subtract <i>k</i>, divide by <i>a</i>, take ±√, then add <i>h</i>.
             The zeros sit the same distance left and right of the axis {x} = <i>h</i>.</p>
             <p><b>Number of real zeros:</b> vertex below the {x}-axis and opening up (or above and opening down) → <b>2</b>;
             vertex on the {x}-axis → <b>1</b> (double root); otherwise → <b>0</b>.</p>""",
             example=f"""<p>2({x} − 3)² − 10 = 0 → ({x} − 3)² = 5 → {x} − 3 = ±{rt(5)} → <b>{x} = 3 ± {rt(5)}</b> (≈ 5.24 and 0.76).</p>""",
             items=[
                 OPEN(f"Find the exact zeros of <i>f</i>({x}) = −½({x} + 1)² + 6.",
                      f"(x + 1)² = 12 → x = −1 ± 2{rt(3)}",
                      frames=[f"−½({x} + 1)² = −6 → ({x} + 1)² = [[12]]", f"{x} + 1 = ±{rt(12)} = ±[[2]]{rt(3)} → {x} = [[−1]] ± 2{rt(3)}"],
                      tip="Multiply both sides by −2 to undo −½."),
                 ROWS("How many real zeros does each function have?", ["0", "1", "2"],
                      [(f"<i>y</i> = ({x} − 2)² + 3", 0), (f"<i>y</i> = −({x} + 1)² + 4", 2), (f"<i>y</i> = 5({x} − 6)²", 1), (f"<i>y</i> = −2{x}² − 1", 0)],
                      tip="Find the vertex and which way it opens. Does it reach the x-axis?"),
                 OPEN(f"Graph <i>f</i>({x}) = −({x} − 1)² + 4. How many real zeros does it have? What are they?",
                      "Vertex (1, 4), opens down → 2 zeros: x = −1 and x = 3", fig=sq(lambda t: -(t - 1) ** 2 + 4, -2.5, 4.5),
                      frames=["Vertex ([[1]], [[4]]), opens [[down]]", "Zeros: <i>x</i> = [[−1]] and <i>x</i> = [[3]]"]),
             ]),
        dict(title="11.3 Factoring and Completing the Square", lesson="Lesson 3 · Getting Started, Activities 1–5, Talk the Talk ✪",
             idea=f"""<p><b>Factor completely:</b> 1) take out the GCF; 2) {x}² + <i>b</i>{x} + <i>c</i>: two numbers that multiply to <i>c</i>
             and add to <i>b</i>; 3) <i>a</i>{x}² + <i>b</i>{x} + <i>c</i>: find two numbers that multiply to <i>a</i> · <i>c</i> and add to <i>b</i>,
             split the middle term, and group; 4) look for a difference of squares.</p>
             <p><b>Completing the square</b> ({x}² + <i>b</i>{x} + <i>c</i> = 0): move <i>c</i>; add (<i>b</i>/2)² to both sides;
             write ({x} + <i>b</i>/2)²; take ±√.</p>""",
             example=f"""<p>2{x}² + 7{x} − 15: <i>a</i> · <i>c</i> = −30 → 10 and −3 → 2{x}² + 10{x} − 3{x} − 15 = 2{x}({x} + 5) − 3({x} + 5) =
             <b>(2{x} − 3)({x} + 5)</b>.</p>
             <p>{x}² + 10{x} − 11 = 0 → {x}² + 10{x} = 11 → {x}² + 10{x} + 25 = 36 → ({x} + 5)² = 36 → {x} + 5 = ±6 → <b>{x} = 1 or {x} = −11</b>.</p>""",
             items=[
                 OPEN(f"Factor completely: 3{x}² − 48", "3(x² − 16) = 3(x − 4)(x + 4)",
                      frames=[f"GCF: [[3]]({x}² − 16) = 3({x} − [[4]])({x} + [[4]])"], lines=1, tip="Take out the GCF first."),
                 OPEN(f"Factor completely: 4{x}² + 4{x} − 15", "a · c = −60 → 10 and −6 → (2x + 5)(2x − 3)",
                      frames=["4 · (−15) = [[−60]] → two numbers: [[10]] and [[−6]]", f"(2{x} + [[5]])(2{x} − [[3]])"]),
                 OPEN(f"Solve 3{x}² + 10{x} + 8 = 0.", f"(3x + 4)(x + 2) = 0 → x = −{fr(4, 3)} or x = −2",
                      frames=[f"(3{x} + [[4]])({x} + [[2]]) = 0", f"{x} = [[−4/3]] or {x} = [[−2]]"]),
                 OPEN(f"Solve {x}² − 6{x} + 2 = 0 by completing the square. Write the answer in simplest radical form.",
                      f"x² − 6x + 9 = −2 + 9 → (x − 3)² = 7 → x = 3 ± {rt(7)}",
                      frames=[f"{x}² − 6{x} + [[9]] = −2 + [[9]]", f"({x} − [[3]])² = [[7]] → {x} = 3 ± {rt('[[7]]')}"],
                      tip="Half of −6 is −3, and (−3)² = 9."),
             ]),
        dict(title="11.4 The Quadratic Formula", lesson="Lesson 4 · Getting Started, Activities 1–4, Talk the Talk ✪",
             idea=f"""<p>For <i>a</i>{x}² + <i>b</i>{x} + <i>c</i> = 0: &nbsp; <b>{x} = {fr('−<i>b</i> ± √<span class="ov"><i>b</i>² − 4<i>ac</i></span>', '2<i>a</i>')}</b>
             &nbsp; (it is on the STAAR reference sheet).</p><p>The <b>discriminant</b> <i>b</i>² − 4<i>ac</i>: positive → 2 real
             solutions; zero → 1; negative → no real solutions.</p>""",
             example=f"""<p>2{x}² + 3{x} − 4 = 0: <i>a</i> = 2, <i>b</i> = 3, <i>c</i> = −4. Discriminant 9 + 32 = 41.
             {x} = {fr(f'−3 ± {rt(41)}', 4)} ≈ <b>{nm(q0[0])} and {nm(q0[1])}</b>.</p>""",
             items=[
                 OPEN(f"Solve {x}² − 4{x} − 3 = 0 with the quadratic formula. Write the answer in simplest radical form.",
                      f"discriminant 16 + 12 = 28; x = (4 ± 2{rt(7)}) ÷ 2 = 2 ± {rt(7)}",
                      frames=["<i>a</i> = [[1]], <i>b</i> = [[−4]], <i>c</i> = [[−3]] · <i>b</i>² − 4<i>ac</i> = [[28]]",
                              f"{x} = (4 ± {rt(28)}) ÷ 2 = [[2]] ± {rt(7)}"], tip="√28 = √(4 · 7) = 2√7."),
                 MC(f"How many real solutions does 3{x}² − 2{x} + 5 = 0 have?", ["0", "1", "2", "3"], 0, why="(−2)² − 4(3)(5) = 4 − 60 = −56 &lt; 0."),
                 OPEN("A ball is thrown with <i>h</i>(<i>t</i>) = −16<i>t</i>² + 32<i>t</i> + 48. After how many seconds does it hit the ground?",
                      "−16(t² − 2t − 3) = −16(t − 3)(t + 1) = 0 → t = 3 seconds (t = −1 makes no sense)",
                      frames=["−16(<i>t</i> − [[3]])(<i>t</i> + [[1]]) = 0 → <i>t</i> = [[3]] seconds"], tip="Hits the ground → h = 0."),
             ]),
        dict(title="11.5 Using Quadratic Functions to Model Data", lesson="Lesson 5 · Getting Started, Activities 1–2, Talk the Talk ✪",
             idea=f"""<p>Data that rises then falls (or falls then rises) is best modeled by a <b>quadratic regression</b>. Linear data
             has a constant difference; exponential data has a constant ratio.</p>{calc}""",
             example=f"""<p>A pop-up shop’s daily visitors:</p>{htable(('Day', vx), ('Visitors', vy))}
             <p>QuadReg: <b><i>f</i>({x}) = {nm(va)}{x}² + {nm(vb)}{x} + {nm(vc)}</b>. Predict day 22:
             {nm(va)}(22)² + {nm(vb)}(22) + {nm(vc)} ≈ <b>{round(vpred)}</b> visitors.</p>""",
             items=[
                 MC("Which function best models the visitor data in the worked example?",
                    [f"<i>f</i>({x}) = {nm(vm)}{x} + {nm(vb0)}", f"<i>f</i>({x}) = {nm(va)}{x}² + {nm(vb)}{x} + {nm(vc)}",
                     f"<i>f</i>({x}) = {nm(ea)}({nm(eb)})<sup>{x}</sup>", "No function can model this data."], 1,
                    why="The visitors rise, peak near day 10, then fall: quadratic."),
                 OPEN(f"Use <i>f</i>({x}) = {nm(va)}{x}² + {nm(vb)}{x} + {nm(vc)} to estimate the visitors on day 5.",
                      f"≈ {round(va * 25 + vb * 5 + vc)}", frames=[f"{nm(va)}(25) + {nm(vb)}(5) + {nm(vc)} ≈ [[{round(va * 25 + vb * 5 + vc)}]]"], lines=1),
             ]),
    ]
    check = [
        MC(f"Which statement about <i>f</i>({x}) = ({x} + 3)(2{x} − 1) is true?",
           [f"The zeros are −3 and {fr(1, 2)}.", f"The zeros are 3 and −{fr(1, 2)}.", "The zeros are 3 and −1.", "The <i>y</i>-intercept is 3."], 0,
           why="The zeros of f are the zeros of its linear factors: x + 3 = 0 and 2x − 1 = 0."),
        MC("A ball’s height was measured every half second. Use regression to choose the model for the data."
           + htable(("Time (s)", bx), ("Height (ft)", by)),
           [f"<i>h</i>(<i>t</i>) = {nm(lm)}<i>t</i> + {nm(lb)}", f"<i>h</i>(<i>t</i>) = {nm(ba)}<i>t</i>² + {nm(bb)}<i>t</i> + {nm(bc)}",
            f"<i>h</i>(<i>t</i>) = {nm(bb)}<i>t</i>² − {nm(-ba)}<i>t</i> + {nm(bc)}", f"<i>h</i>(<i>t</i>) = 5(1.5)<sup><i>t</i></sup>"], 1,
           why=f"Up then down → QuadReg. Its maximum is about {nm(round(bh, 1))} ft at {nm(round(bt, 2))} s."),
        OPEN(f"For <i>f</i>({x}) = −½({x} − 3)² + 4:<br>a. Sketch the graph. Use the vertex and the direction it opens to say how many "
             "real zeros there are.<br>b. Find the exact zeros. c. Give the range.",
             f"a. Vertex (3, 4), opens down → 2 real zeros. b. (x − 3)² = 8 → x = 3 ± 2{rt(2)} c. all real numbers; y {LE} 4",
             fig=sq(lambda t: -0.5 * (t - 3) ** 2 + 4, -1.5, 7.5), lines=5,
             frames=["a. Vertex ([[3]], [[4]]) above the x-axis, opens [[down]] → [[2]] real zeros",
                     f"b. ({x} − 3)² = [[8]] → {x} = 3 ± [[2]]{rt(2)}", f"c. Domain: [[all real numbers]] · Range: {y} {LE} [[4]]"]),
        OPEN(f"Factor completely: 5{x}² − 45", "5(x − 3)(x + 3)", frames=[f"[[5]]({x}² − 9) = 5({x} − [[3]])({x} + [[3]])"], lines=1),
        OPEN(f"Factor completely: 6{x}² + {x} − 12", "a · c = −72 → 9 and −8 → (3x − 4)(2x + 3)",
             frames=["6 · (−12) = [[−72]] → [[9]] and [[−8]]", f"(3{x} − [[4]])(2{x} + [[3]])"]),
        OPEN(f"Determine the solutions of 2{x}² − 7{x} − 15 = 0.", f"(2x + 3)(x − 5) = 0 → x = −{fr(3, 2)} or x = 5",
             frames=[f"(2{x} + [[3]])({x} − [[5]]) = 0 → {x} = [[−3/2]] or {x} = [[5]]"]),
        OPEN(f"Complete the square to solve {x}² + 14{x} − 15 = 0.",
             "x² + 14x + 49 = 64 → (x + 7)² = 64 → x + 7 = ±8 → x = 1 or x = −15",
             frames=[f"{x}² + 14{x} + [[49]] = 15 + [[49]]", f"({x} + 7)² = [[64]] → {x} = [[1]] or {x} = [[−15]]"]),
        OPEN(f"Rewrite {rt(300)} in simplest radical form.", f"√(100 · 3) = 10{rt(3)}", frames=[f"{rt('[[100]] · 3')} = [[10]]{rt(3)}"], lines=1),
        OPEN(f"What is the positive solution of 7{x}² + 4 = 116?", "7x² = 112 → x² = 16 → x = 4", frames=[f"7{x}² = [[112]] → {x}² = [[16]] → {x} = [[4]]"], lines=1),
        MC("Which equation has exactly one real solution?", [f"{x}² − 10{x} + 25 = 0", f"{x}² + 4 = 0", f"{x}² − 5{x} + 4 = 0", f"2{x}² + {x} + 3 = 0"], 0,
           why="Discriminant (−10)² − 4(1)(25) = 0.", tip="Find b² − 4ac for each. Zero → one solution."),
        OPEN(f"Solve 3{x}² − 5{x} − 1 = 0. Round to the nearest hundredth.", f"x = (5 ± {rt(37)}) ÷ 6 ≈ {nm(q1[0])} and {nm(q1[1])}",
             frames=[f"<i>b</i>² − 4<i>ac</i> = 25 + 12 = [[37]]", f"{x} = (5 ± {rt(37)}) ÷ 6 ≈ [[{nm(q1[0])}]] and [[{nm(q1[1])}]]"]),
        OPEN("A rock falls from a 144-foot cliff: <i>h</i>(<i>t</i>) = −16<i>t</i>² + 144. When does it hit the ground?",
             "16t² = 144 → t² = 9 → t = 3 seconds", frames=["16<i>t</i>² = [[144]] → <i>t</i>² = [[9]] → <i>t</i> = [[3]] s"], lines=2),
        MC("The graph shows the solutions of which equation?", [f"({x} − 1)({x} + 4) = 0", f"({x} + 1)({x} − 4) = 0", f"({x} + 1)({x} + 4) = 0", f"{x}² − 4 = 0"], 1,
           fig=g14, why="The graph crosses at x = −1 and x = 4, so the factors are (x + 1) and (x − 4)."),
        OPEN(f"Determine the zeros of <i>f</i>({x}) = 3({x} − 5)². How many are there?", "one zero (a double root): x = 5",
             frames=[f"({x} − 5)² = 0 → {x} = [[5]] → [[1]] zero (double root)"], lines=1),
        ROWS("Use the discriminant. How many real solutions does each equation have?", ["0", "1", "2"],
             [(f"{x}² + 6{x} + 9 = 0", 1), (f"{x}² − 3{x} − 10 = 0", 2), (f"4{x}² + {x} + 1 = 0", 0), (f"2{x}² − 8 = 0", 2)]),
        OPEN(f"Solve {x}² + 8{x} + 3 = 0 by completing the square. Write the answer in simplest radical form.",
             f"(x + 4)² = 13 → x = −4 ± {rt(13)}", frames=[f"{x}² + 8{x} + [[16]] = −3 + [[16]]", f"({x} + 4)² = [[13]] → {x} = −4 ± {rt('[[13]]')}"]),
    ]
    assert r((-4 + 13 ** 0.5) ** 2 + 8 * (-4 + 13 ** 0.5) + 3)
    staar = [
        MC(f"Which is a factor of 6{x}² − 11{x} − 10?", [f"2{x} − 5", f"3{x} − 2", f"2{x} + 5", f"6{x} + 1"], 0, teks="A.10(E)",
           why="6x² − 11x − 10 = (2x − 5)(3x + 2)."),
        MC(f"Which shows 4{x}² − 36 factored completely?", [f"(2{x} − 6)(2{x} + 6)", f"4({x} − 3)({x} + 3)", f"4({x} − 3)²", f"(4{x} − 6)({x} + 6)"], 1,
           teks="A.10(E)", why="(2x − 6)(2x + 6) is equal, but each factor still has a common factor of 2."),
        MC(f"What are the solutions of {x}² + 2{x} − 24 = 0?", ["−6 and 4", "6 and −4", "−8 and 3", "−12 and 2"], 0, teks="A.8(A)"),
        OPEN(f"What is the positive solution of {x}² − 6{x} − 16 = 0? Enter your answer.", "(x − 8)(x + 2) = 0 → 8", teks="A.8(A)", fmt="Text entry", lines=1,
             frames=[f"({x} − [[8]])({x} + [[2]]) = 0 → positive solution [[8]]"]),
        MC(f"What are the solutions of {x}² − 6{x} + 4 = 0?", [f"3 ± {rt(5)}", f"−3 ± {rt(5)}", f"3 ± 2{rt(5)}", f"6 ± {rt(20)}"], 0, teks="A.8(A)",
           why="x = (6 ± √20) ÷ 2 = (6 ± 2√5) ÷ 2 = 3 ± √5."),
        MC(f"Which statements are true about <i>g</i>({x}) = {x}² − 2{x} − 8? Select <b>TWO</b> correct answers.",
           [f"<i>g</i> has a zero at {x} = 4.", f"<i>g</i> has a zero at {x} = −2.", "The vertex is (1, −8).", "The <i>y</i>-intercept is −2.",
            f"The axis of symmetry is {x} = −1."], (0, 1), teks="A.7(A)", why="g(x) = (x − 4)(x + 2); vertex (1, −9); y-intercept −8."),
        MC("A quadratic regression for a data set gives <i>y</i> = −0.5<i>x</i>² + 6<i>x</i> + 10. What is the greatest <i>y</i>-value the model predicts?",
           ["6", "10", "28", "46"], 2, teks="A.8(B)", why="x = −6 ÷ (2 · −0.5) = 6; y = −18 + 36 + 10 = 28."),
    ]
    vocab = [("Zero Product Property", "if A · B = 0, then A = 0 or B = 0"),
             ("double root", "a zero that appears twice: the vertex touches the x-axis"),
             ("completing the square", "adding (b/2)² to make a perfect square trinomial"),
             ("quadratic formula", "x = (−b ± √(b² − 4ac)) ÷ 2a"),
             ("discriminant", "b² − 4ac: tells how many real solutions"),
             ("quadratic regression", "the quadratic function that best fits data (QuadReg)")]
    return dict(code="M5 T3", title="Solving Quadratic Equations", module="Module 5: Maximizing and Minimizing",
                teks="A.6A, A.7A, A.8A, A.8B, A.10E, A.10F, A.11A", vocab=vocab, sections=sections, check=check, staar=staar)


BOOK = [ch1, ch2, ch3, ch4, ch5, ch6, ch7, ch8, ch9, ch10, ch11]


# =====================================================================================================
# STAAR UNIT · reference sheet guide, question types, blueprint, 2 full practice tests
# Blueprint from the 2024–2026 STAAR Algebra I answer keys (materials/STAAR): 50 questions; reporting categories
# 1–5 ≈ 10/11/13/10/6; each of the 16 readiness TEKS appears exactly twice (32 questions) + 18 supporting.
# =====================================================================================================
CAT = {"10": 1, "11": 1, "12": 1, "3": 2, "4": 2, "2": 3, "5": 3, "6": 4, "7": 4, "8": 4, "9": 5}
CATNAME = {1: "Number and Algebraic Methods", 2: "Describing and Graphing Linear Functions, Equations, and Inequalities",
           3: "Writing and Solving Linear Functions, Equations, and Inequalities", 4: "Quadratic Functions and Equations",
           5: "Exponential Functions and Equations"}
READY = "A.2A A.2C A.2I A.3B A.3C A.3D A.5A A.5C A.6A A.7A A.7C A.8A A.9C A.9D A.10E A.11B".split()
FIXIT = {"A.2A": "1, 3", "A.2B": "3, 5", "A.2C": "3, 4", "A.2D": "3", "A.2E": "4", "A.2F": "4", "A.2G": "4", "A.2H": "6", "A.2I": "6",
         "A.3A": "3, 5", "A.3B": "3, 8", "A.3C": "3, 4", "A.3D": "6", "A.3E": "4", "A.3F": "6", "A.3G": "6", "A.3H": "6",
         "A.4A": "3", "A.4B": "3", "A.4C": "3", "A.5A": "5", "A.5B": "5", "A.5C": "6", "A.6A": "1, 9", "A.6B": "9", "A.6C": "9",
         "A.7A": "9, 11", "A.7B": "11", "A.7C": "9", "A.8A": "11", "A.8B": "11", "A.9A": "7, 8", "A.9B": "8", "A.9C": "8",
         "A.9D": "7", "A.9E": "8", "A.10A": "10", "A.10B": "10", "A.10C": "10", "A.10D": "10", "A.10E": "11", "A.10F": "11",
         "A.11A": "7, 11", "A.11B": "7", "A.12A": "1, 2", "A.12B": "7", "A.12C": "2", "A.12D": "2", "A.12E": "5"}
tk = lambda t: t.replace("(", "").replace(")", "")  # "A.10(E)" -> "A.10E"
cat_of = lambda t: CAT[tk(t).split(".")[1][:-1]]
tiles = lambda *ts: ('<span class="tiles">' + "".join(f'<span class="tile">{v}</span>' for v in ts) + "</span>")
DD, GR, IC, EE, HS, MG = "Drag and drop", "Graphing", "Inline choice", "Equation editor", "Hot spot", "Match table grid"


def test1():
    G = (-8, 8, 1, 2)
    BLUE = "#2f6fdd"
    ya, yb = expreg([0, 1, 2, 3, 4], [12, 19, 29, 45, 70])
    lm, lb = reg([0, 1, 2, 3, 4], [12, 19, 29, 45, 70])
    q = [round((-4 + s * 72 ** 0.5) / 4, 2) for s in (-1, 1)]
    assert q == [-3.12, 1.12] and 7 + 8 == 15 and 12 * 7 + 8 * 8 == 148 and 8 * 5 - 17 == 3 * 5 + 8 and Fr(2, 3) * 30 == 21 - 1
    assert 3 * 4 + 2 * -4 == 4 and 4 - 2 * -4 == 12 and abs(2 * 2.1 + 3 * 3.1 - 13.5) < 1e-9 and abs(4 * 2.1 + 3.1 - 11.5) < 1e-9
    assert same(lambda t: (3 * t + 2) * (t - 4), lambda t: 3 * t * t - 10 * t - 8) and same(lambda t: (2 * t - 3) * (t + 4), lambda t: 2 * t * t + 5 * t - 12)
    assert same(lambda t: (t - 7) * (2 * t + 3), lambda t: 2 * t * t - 11 * t - 21) and same(lambda t: -4 * (3 * t - 5) + 2 * t, lambda t: -10 * t + 20)
    assert -2 * 9 + 5 * -3 == -33 and 4 * (-3) ** 3 == -108 and 0 ** 2 - 4 * 0 - 5 == -5 and 2 * (-1 + 3) ** 2 + 2 == 10
    assert same(lambda t: (t - 7) * (t + 2), lambda t: t * t - 5 * t - 14) and 4.5 * 6 + 58 == 85
    sections = [
        # ---- category 3 (13) ----
        MC("A food truck sells tacos for $3 each. It can make at most 120 tacos a day. Which is the most reasonable range for "
           "the truck’s daily taco revenue, <i>R</i>, in dollars?",
           ["{0, 3, 6, 9, …, 360}", f"0 {LE} <i>R</i> {LE} 120", f"All real numbers 0 {LE} <i>R</i> {LE} 360", f"<i>R</i> {GE} 0"], 0, teks="A.2(A)",
           why="Tacos come in whole numbers, so revenue goes up $3 at a time, from $0 to 120 × $3 = $360."),
        MC("What is the domain of the function graphed?", [f"−3 {LE} <i>x</i> &lt; 4", f"−3 &lt; <i>x</i> {LE} 4", f"−2 &lt; <i>x</i> {LE} 5", f"−3 {LE} <i>x</i> {LE} 4"], 0,
           fig=plot(G, G, [dict(xy=[(-3, 5), (4, -2)], ends=("closed", "open"))]), teks="A.2(A)",
           why="Closed dot at x = −3 (included), open dot at x = 4 (not included)."),
        MC("Which equation represents the table?" + htable((x, ["−2", 1, 4, 7]), (y, [11, 5, "−1", "−7"])),
           [f"{y} = −2{x} + 7", f"{y} = 2{x} + 7", f"{y} = −2{x} + 11", f"{y} = −½{x} + 7"], 0, teks="A.2(C)",
           why="Slope (5 − 11) ÷ (1 − (−2)) = −2; 5 = −2(1) + b → b = 7."),
        OPEN("A gym charges a $45 sign-up fee plus $28 per month. Drag numbers into the boxes to complete the equation for the total "
             f"cost <i>C</i> after <i>m</i> months.<br>{tiles(17, 28, 45, 73)}<br><i>C</i> = [[28]]<i>m</i> + [[45]]",
             "C = 28m + 45", teks="A.2(C)", fmt=DD, lines=1),
        MC("Adult movie tickets cost $12 and child tickets cost $8. A family bought 15 tickets for $148. Which system can find the number "
           "of adult tickets <i>a</i> and child tickets <i>c</i>?",
           ["<i>a</i> + <i>c</i> = 148<br>12<i>a</i> + 8<i>c</i> = 15", "<i>a</i> + <i>c</i> = 15<br>12<i>a</i> + 8<i>c</i> = 148",
            "<i>a</i> + <i>c</i> = 15<br>8<i>a</i> + 12<i>c</i> = 148", "12<i>a</i> = 8<i>c</i><br><i>a</i> + <i>c</i> = 148"], 1, teks="A.2(I)"),
        MC("Plan A costs $20 plus $5 per class. Plan B costs $10 per class. Which system gives the cost <i>y</i> of <i>x</i> classes for each plan?",
           [f"{y} = 20{x} + 5<br>{y} = 10{x}", f"{y} = 5{x} + 20<br>{y} = 10{x}", f"{y} = 5{x} + 20<br>{y} = {x} + 10", f"{y} = 25{x}<br>{y} = 10{x}"], 1,
           teks="A.2(I)"),
        MC(f"What is the solution of 4(2{x} − 3) − 5 = 3{x} + 8?", [f"{x} = 1", f"{x} = 5", f"{x} = 3", f"{x} = −5"], 1, teks="A.5(A)",
           why="8x − 17 = 3x + 8 → 5x = 25 → x = 5."),
        OPEN(f"What value of {x} makes ⅔({x} + 9) = {x} − 1 true? Enter your answer.", "2x + 18 = 3x − 3 → x = 21", teks="A.5(A)", fmt=EE, lines=2,
             tip="Multiply both sides by 3 first."),
        MC(f"What is the solution of the system?<br>3{x} + 2{y} = 4<br>{x} − 2{y} = 12", ["(4, −4)", "(−4, 4)", "(4, 4)", "(2, −1)"], 0, teks="A.5(C)",
           why="Add: 4x = 16 → x = 4; 4 − 2y = 12 → y = −4."),
        MC("Two bagels and three coffees cost $13.50. Four bagels and one coffee cost $11.50. What is the price of one coffee?",
           ["$2.10", "$3.10", "$3.50", "$4.50"], 1, teks="A.5(C)", why="2b + 3c = 13.50, 4b + c = 11.50 → b = 2.10, c = 3.10."),
        MC(f"Which line passes through (2, 5) and is parallel to {y} = −3{x} + 1?", [f"{y} = −3{x} + 11", f"{y} = −3{x} − 1", f"{y} = ⅓{x} + 4⅓", f"{y} = 3{x} − 1"], 0,
           teks="A.2(E)", why="Same slope −3: 5 = −3(2) + b → b = 11."),
        MC("Which inequality is graphed?", [f"{y} &gt; 2{x} − 1", f"{y} {GE} 2{x} − 1", f"{y} &lt; 2{x} − 1", f"{y} &gt; −2{x} − 1"], 0,
           fig=plot(G, G, [dict(f=lambda t: 2 * t - 1, shade="above", dash=True)]), teks="A.2(H)", why="Dashed → strict (&gt; or &lt;); shaded above → &gt;."),
        OPEN("Choose the symbol and number that complete the solution of −3<i>x</i> + 7 ≥ 22.<br><i>x</i> ( ≤ / ≥ ) ( −5 / 5 )",
             "x ≤ −5", teks="A.5(B)", fmt=IC, lines=1, frames=["−3<i>x</i> ≥ 15 → divide by −3 and [[flip]] the sign → <i>x</i> [[≤]] [[−5]]"]),
        # ---- category 2 (11) ----
        MC("A bus travels at a constant speed. What is the rate of change of distance with respect to time?"
           + htable(("Time (h)", [2, 5, 9]), ("Distance (mi)", [130, 325, 585])), ["50 mi per hour", "65 mi per hour", "130 mi per hour", "0.015 hour per mi"], 1,
           teks="A.3(B)", why="(325 − 130) ÷ (5 − 2) = 65."),
        MC("The graph shows the water in a tank as it drains. What is the rate of change?", ["−5 gallons per minute", "−0.2 gallon per minute",
                                                                                       "5 gallons per minute", "50 gallons per minute"], 0,
           fig=plot((0, 12, 1, 2), (0, 60, 5, 10), [dict(xy=[(0, 50), (10, 0)], ends=("closed", "closed"))], pts=[(4, 30, "(4, 30)")],
                    xlab="Time (min)", ylab="Water (gal)"), teks="A.3(B)", why="(30 − 50) ÷ (4 − 0) = −5."),
        OPEN(f"Graph 2{x} + 3{y} = 12 on the grid.", "Line through (0, 4) and (6, 0)", teks="A.3(C)", fmt=GR,
             fig=lambda: plot(G, G, [dict(f=lambda t: (12 - 2 * t) / 3, a=-6, b=8, color=RED)] if KEY else []),
             frames=["<i>x</i> = 0 → <i>y</i> = [[4]] · <i>y</i> = 0 → <i>x</i> = [[6]]"], tip="Find both intercepts, plot them, and connect."),
        MC(f"What is the {x}-intercept of {y} = 4{x} − 10?", ["(−10, 0)", "(2.5, 0)", "(0, −10)", "(−2.5, 0)"], 1, teks="A.3(C)", why="0 = 4x − 10 → x = 2.5."),
        MC("Which system of equations is represented by the graph?", [f"{y} = {x} + 5<br>{y} = −2{x} − 1", f"{y} = {x} − 5<br>{y} = −2{x} + 1",
                                                                     f"{y} = −{x} + 5<br>{y} = 2{x} − 1", f"{y} = {x} + 5<br>{y} = 2{x} − 1"], 0,
           fig=plot(G, G, [dict(f=lambda t: t + 5, a=-8, b=3), dict(f=lambda t: -2 * t - 1, a=-4.5, b=3.5)]), teks="A.3(D)"),
        MC(f"The graphs of {y} = ½{x} + 1 and {y} = −{x} + 4 are drawn on the same grid. What is the solution of the system?",
           ["(2, 2)", "(1, 3)", "(0, 4)", "(−2, 0)"], 0, teks="A.3(D)", why="½(2) + 1 = 2 and −2 + 4 = 2."),
        MC("What is the slope of the line through (−4, 7) and (2, −5)?", ["2", "−2", "−½", "−6"], 1, teks="A.3(A)", why="(−5 − 7) ÷ (2 − (−4)) = −12 ÷ 6."),
        MC(f"How does the graph of <i>g</i>({x}) = {x} − 4 compare to the graph of <i>f</i>({x}) = {x}?",
           ["It is 4 units lower.", "It is 4 units higher.", "It is 4 times as steep.", "It is 4 units to the left."], 0, teks="A.3(E)"),
        OPEN(f"Graph the solution set of the system.<br>{y} &lt; −{x} + 3<br>{y} {GE} 2{x} − 3", "Dashed y = −x + 3 shaded below; solid y = 2x − 3 "
             "shaded above; the solution is the overlap (it contains (0, 0)).", teks="A.3(H)", fmt=GR,
             fig=lambda: plot(G, G, [dict(f=lambda t: -t + 3, shade="below", dash=True, color=RED, line=RED),
                                     dict(f=lambda t: 2 * t - 3, shade="above", color=BLUE, line=RED)] if KEY else []),
             frames=["<i>y</i> &lt; −<i>x</i> + 3: [[dashed]] line, shade [[below]]", "<i>y</i> ≥ 2<i>x</i> − 3: [[solid]] line, shade [[above]]"]),
        MC("The correlation coefficient for a data set is <i>r</i> = −0.92. Which describes the relationship?",
           ["Strong negative", "Weak negative", "Strong positive", "No correlation"], 0, teks="A.4(A)"),
        MC("The line of best fit for hours studied <i>x</i> and test score <i>y</i> is <i>y</i> = 4.5<i>x</i> + 58. What score does it predict for 6 hours?",
           ["62.5", "85", "79", "348"], 1, teks="A.4(C)"),
        # ---- category 1 (10) ----
        MC(f"Which is the factored form of 3{x}² − 10{x} − 8?", [f"(3{x} − 2)({x} + 4)", f"(3{x} + 2)({x} − 4)", f"(3{x} + 4)({x} − 2)", f"(3{x} − 4)({x} + 2)"], 1,
           teks="A.10(E)"),
        MC(f"Which expressions are factors of 2{x}² + 5{x} − 12? Select <b>TWO</b> correct answers.",
           [f"2{x} − 3", f"{x} + 4", f"2{x} + 3", f"{x} − 4", f"2{x} + 4"], (0, 1), teks="A.10(E)", why="2x² + 5x − 12 = (2x − 3)(x + 4)."),
        MC(f"Which is equivalent to (2{x}³{y}<sup>−2</sup>)³?", [f"6{x}⁶{y}<sup>−6</sup>", fr(f"8{x}⁹", f"{y}⁶"), fr(f"8{x}⁶", f"{y}⁵"), f"8{x}⁹{y}⁶"], 1, teks="A.11(B)"),
        OPEN(f"Drag numbers into the boxes to simplify (16<i>a</i>⁸)<sup>½</sup>.<br>{tiles(2, 4, 8, 16)}<br>[[4]]<i>a</i><sup>[[4]]</sup>",
             "4a⁴", teks="A.11(B)", fmt=DD, lines=1, tip="A ½ exponent is a square root. A tile can be used more than once."),
        MC(f"Which is equivalent to ({x} − 7)(2{x} + 3)?", [f"2{x}² − 21", f"2{x}² − 11{x} − 21", f"2{x}² + 11{x} − 21", f"2{x}² − 17{x} − 21"], 1, teks="A.10(B)"),
        MC(f"Which is equivalent to −4(3{x} − 5) + 2{x}?", [f"−10{x} − 20", f"−10{x} + 20", f"14{x} − 20", f"−12{x} + 22"], 1, teks="A.10(D)"),
        MC(f"Which is equivalent to 3{rt(50)}?", [f"15{rt(2)}", f"5{rt(6)}", f"75{rt(2)}", f"3{rt(10)}"], 0, teks="A.11(A)"),
        OPEN(f"If <i>f</i>({x}) = −2{x}² + 5{x}, what is <i>f</i>(−3)? Enter your answer.", "−2(9) + 5(−3) = −18 − 15 = −33", teks="A.12(B)", fmt=EE, lines=1,
             tip="(−3)² = 9. Square first, then multiply by −2."),
        MC("A sequence is defined by <i>f</i>(1) = 4 and <i>f</i>(<i>n</i>) = −3 · <i>f</i>(<i>n</i> − 1). What is the 4th term?", ["−108", "108", "−36", "−5"], 0,
           teks="A.12(C)", why="4, −12, 36, −108."),
        MC("Which equation is <i>A</i> = ½<i>h</i>(<i>b</i>₁ + <i>b</i>₂) solved for <i>h</i>?",
           [f"<i>h</i> = {fr('<i>A</i>', '2(<i>b</i>₁ + <i>b</i>₂)')}", f"<i>h</i> = {fr('2<i>A</i>', '<i>b</i>₁ + <i>b</i>₂')}",
            "<i>h</i> = 2<i>A</i> − <i>b</i>₁ − <i>b</i>₂", f"<i>h</i> = {fr('<i>A</i>(<i>b</i>₁ + <i>b</i>₂)', 2)}"], 1, teks="A.12(E)"),
        # ---- category 4 (10) ----
        MC(f"What is the range of <i>f</i>({x}) = −3({x} − 2)² + 7?", [f"{y} {GE} 7", f"{y} {LE} 7", f"{y} {LE} 2", "All real numbers"], 1, teks="A.6(A)"),
        OPEN("Choose the words that complete the sentences about the graph.<br>The domain is ( all real numbers / <i>x</i> ≥ −1 ). "
             "The range is ( <i>y</i> ≥ −4 / <i>y</i> ≤ −4 ).", "all real numbers; y ≥ −4", teks="A.6(A)", fmt=IC, lines=1,
             fig=plot(G, G, [dict(f=lambda t: (t + 1) ** 2 - 4, a=-4.4, b=2.4)], pts=[(-1, -4, "(−1, −4)")])),
        MC(f"What is the vertex of the graph of <i>f</i>({x}) = {x}² − 6{x} + 5?", ["(3, −4)", "(−3, 32)", "(3, 5)", "(6, 5)"], 0, teks="A.7(A)",
           why="x = 6 ÷ 2 = 3; f(3) = 9 − 18 + 5 = −4."),
        OPEN(f"The graph of <i>y</i> = {x}² − 4{x} − 5 is shown. Mark the point on the graph that is the <i>y</i>-intercept.", "(0, −5)", teks="A.7(A)", fmt=HS,
             fig=lambda: plot((-6, 8, 1, 2), (-10, 6, 1, 2), [dict(f=lambda t: t * t - 4 * t - 5, a=-2.3, b=6.3)], pts=[(0, -5, "(0, −5)")] if KEY else []),
             lines=0, tip="The y-intercept is where the graph crosses the y-axis (x = 0)."),
        MC(f"How does the graph of <i>g</i>({x}) = ({x} + 3)² − 1 compare to the graph of <i>f</i>({x}) = {x}²?",
           ["Right 3, down 1", "Left 3, down 1", "Left 3, up 1", "Right 1, down 3"], 1, teks="A.7(C)"),
        MC(f"How does the graph of <i>g</i>({x}) = ¼{x}² compare to the graph of <i>f</i>({x}) = {x}²?",
           ["It is wider (vertical compression).", "It is narrower (vertical stretch).", "It is shifted up ¼.", "It opens down."], 0, teks="A.7(C)"),
        MC(f"What are the solutions of {x}² − 5{x} − 14 = 0?", ["−7 and 2", "−2 and 7", "−14 and 1", "2 and 7"], 1, teks="A.8(A)"),
        OPEN(f"What are the solutions of 2{x}² + 4{x} − 7 = 0, to the nearest hundredth? Drag the answers into the boxes.<br>"
             f"{tiles('−3.12', '−1.12', '−0.56', '1.12', '3.12')}<br>{x} = [[−3.12]] and {x} = [[1.12]]",
             f"x = (−4 ± {rt(72)}) ÷ 4 ≈ −3.12 and 1.12", teks="A.8(A)", fmt=DD, lines=2, tip="Use the quadratic formula: a = 2, b = 4, c = −7."),
        MC("A parabola has vertex (−3, 2) and passes through (−1, 10). Which is its equation?",
           [f"{y} = 2({x} + 3)² + 2", f"{y} = 2({x} − 3)² + 2", f"{y} = 4({x} + 3)² + 2", f"{y} = ½({x} + 3)² + 2"], 0, teks="A.6(B)",
           why="10 = a(−1 + 3)² + 2 → 4a = 8 → a = 2."),
        MC(f"Which function has zeros at {x} = −5 and {x} = ¾?", [f"<i>f</i>({x}) = ({x} − 5)(4{x} + 3)", f"<i>f</i>({x}) = ({x} + 5)(4{x} − 3)",
                                                                 f"<i>f</i>({x}) = ({x} + 5)(3{x} − 4)", f"<i>f</i>({x}) = ({x} − 5)(3{x} + 4)"], 1, teks="A.7(B)",
           why="x + 5 = 0 → −5; 4x − 3 = 0 → ¾."),
        # ---- category 5 (6) ----
        MC("A $1,500 investment grows 3.5% per year. Which function gives its value after <i>t</i> years?",
           ["<i>f</i>(<i>t</i>) = 1,500(0.035)<sup><i>t</i></sup>", "<i>f</i>(<i>t</i>) = 1,500(1.35)<sup><i>t</i></sup>",
            "<i>f</i>(<i>t</i>) = 1,500(1.035)<sup><i>t</i></sup>", "<i>f</i>(<i>t</i>) = 1,500 + 1.035<i>t</i>"], 2, teks="A.9(C)"),
        MC("A $28,000 car loses 12% of its value each year. Which function gives its value after <i>t</i> years?",
           ["<i>V</i>(<i>t</i>) = 28,000(0.12)<sup><i>t</i></sup>", "<i>V</i>(<i>t</i>) = 28,000(0.88)<sup><i>t</i></sup>",
            "<i>V</i>(<i>t</i>) = 28,000(1.12)<sup><i>t</i></sup>", "<i>V</i>(<i>t</i>) = 28,000 − 0.12<i>t</i>"], 1, teks="A.9(C)"),
        OPEN(f"Graph <i>y</i> = 2(3)<sup>{x}</sup> on the grid.", "Curve through (0, 2) and (1, 6), approaching the asymptote y = 0 on the left",
             teks="A.9(D)", fmt=GR, fig=lambda: plot(G, G, [dict(f=lambda t: 2 * 3 ** t, a=-8, b=1.25, color=RED)] if KEY else []),
             frames=["Points: (0, [[2]]), (1, [[6]]) · asymptote <i>y</i> = [[0]]"]),
        MC("What are the <i>y</i>-intercept and the asymptote of <i>f</i>(<i>x</i>) = −5(2)<sup><i>x</i></sup>?",
           ["(0, −5); <i>y</i> = 0", "(0, 2); <i>y</i> = 0", "(0, −5); <i>y</i> = −5", "(−5, 0); <i>x</i> = 0"], 0, teks="A.9(D)"),
        MC("A town’s population is modeled by <i>P</i>(<i>t</i>) = 2,400(1.06)<sup><i>t</i></sup>. What does 1.06 mean?",
           ["The population grows 6% each year.", "The population grows 106% each year.", "The town starts with 1.06 thousand people.",
            "The population grows by 6 people each year."], 0, teks="A.9(B)"),
        MC("Which exponential function best models the data?" + htable((x, [0, 1, 2, 3, 4]), (y, [12, 19, 29, 45, 70])),
           [f"<i>y</i> = {nm(ya)}({nm(yb)})<sup>{x}</sup>", f"<i>y</i> = {nm(yb)}({nm(ya)})<sup>{x}</sup>", f"<i>y</i> = {nm(lm)}{x} + {nm(lb)}",
            f"<i>y</i> = 12(1.05)<sup>{x}</sup>"], 0, teks="A.9(E)", why="ExpReg."),
    ]
    return sections


def test2():
    G = (-8, 8, 1, 2)
    BLUE = "#2f6fdd"
    small = lambda f, a=-8, b=8, *p: plot(G, G, [dict(f=f, a=a, b=b)], pts=p, size=150)
    lx, ly = [1, 2, 3, 4, 5, 6], [3.1, 4.9, 7.2, 8.8, 11.1, 12.9]
    lm, lb = reg(lx, ly)
    qx, qy = [0, 1, 2, 3, 4, 5, 6], [2, 9, 13, 14, 12, 8, 1]
    qa, qb, qc = qreg(qx, qy)
    em, eb = reg(qx, qy)
    assert 40 * 140 + 25 * 160 == 9600 and 5 - 2 * 6 == 3 * -4 + 5 and abs(0.4 * 30 - 0.25 * 40 - 2) < 1e-9 and 3 * 4 - 5 == 7 and 2 * 4 + 7 == 15
    assert 24 + 16 == 40 and 2 * 24 + 4 * 16 == 112 and -2 * -2 + 5 == 9 and -2 * 4 + 5 == -3 and 18 / 4 * 10 == 45
    assert same(lambda t: (2 * t + 5) * (3 * t - 4), lambda t: 6 * t * t + 7 * t - 20) and same(lambda t: (t - 6) ** 2, lambda t: t * t - 12 * t + 36)
    assert same(lambda t: (4 * t * t - 3 * t) - (-t * t + 2 * t - 6), lambda t: 5 * t * t - 5 * t + 6) and same(lambda t: (t + 7) * (t - 5), lambda t: t * t + 2 * t - 35)
    assert -16 + 32 == 16 and abs((-3 + 13 ** 0.5) ** 2 + 6 * (-3 + 13 ** 0.5) - 4) < 1e-9 and 4 * 25 - 9 == 91 and 2 * 2 * -4 == -16
    sections = [
        # ---- category 3 (13) ----
        MC("A pool holds 9,000 gallons. It drains at 300 gallons per hour until it is empty. What is the reasonable domain for the time <i>t</i>, in hours?",
           [f"0 {LE} <i>t</i> {LE} 9,000", f"0 {LE} <i>t</i> {LE} 30", f"<i>t</i> {GE} 0", f"0 {LE} <i>t</i> {LE} 300"], 1, teks="A.2(A)", why="9,000 ÷ 300 = 30 hours."),
        MC(f"<i>f</i>({x}) = −2{x} + 5 has the domain −1 {LE} {x} {LE} 4. What is the range?", [f"−3 {LE} {y} {LE} 7", f"−1 {LE} {y} {LE} 4", f"3 {LE} {y} {LE} 7",
                                                                                          f"−7 {LE} {y} {LE} 3"], 0, teks="A.2(A)", why="f(−1) = 7 and f(4) = −3."),
        MC("Which equation represents the line?", [f"{y} = 2{x} − 2", f"{y} = ½{x} − 2", f"{y} = −2{x} + 4", f"{y} = 2{x} + 3"], 0,
           fig=plot(G, G, [dict(f=lambda t: 2 * t - 2, a=-3, b=5)], pts=[(0, -2, "(0, −2)"), (3, 4, "(3, 4)")]), teks="A.2(C)"),
        MC("A plant is 8 cm tall and grows 1.5 cm per week. Which equation gives its height <i>h</i> after <i>w</i> weeks?",
           ["<i>h</i> = 8<i>w</i> + 1.5", "<i>h</i> = 1.5<i>w</i> + 8", "<i>h</i> = 9.5<i>w</i>", "<i>h</i> = 1.5(<i>w</i> + 8)"], 1, teks="A.2(C)"),
        OPEN("Floor tickets cost $40 and balcony tickets cost $25. A concert sold 300 tickets for $9,600. Drag numbers into the boxes to "
             f"complete the system for <i>f</i> floor and <i>b</i> balcony tickets.<br>{tiles(25, 40, 65, 300, '9,600')}<br>"
             "<i>f</i> + <i>b</i> = [[300]]<br>[[40]]<i>f</i> + [[25]]<i>b</i> = [[9,600]]", "f + b = 300; 40f + 25b = 9,600", teks="A.2(I)", fmt=DD, lines=1),
        MC("The tables show the total cost of two phone plans. Which system represents them?"
           + htable(("Months", [0, 1, 2]), ("Plan X ($)", [30, 45, 60]), ("Plan Y ($)", [50, 60, 70])),
           [f"{y} = 15{x} + 30<br>{y} = 10{x} + 50", f"{y} = 30{x} + 15<br>{y} = 50{x} + 10", f"{y} = 15{x} + 30<br>{y} = 50{x} + 10",
            f"{y} = 45{x}<br>{y} = 60{x}"], 0, teks="A.2(I)"),
        MC(f"What is the solution of 5 − 2({x} + 4) = 3({x} − 6) + 5?", [f"{x} = −2", f"{x} = 2", f"{x} = 4", f"{x} = 10"], 1, teks="A.5(A)",
           why="−2x − 3 = 3x − 13 → 10 = 5x → x = 2."),
        OPEN(f"What value of {x} makes 0.4({x} − 10) = 0.25{x} + 2 true? Enter your answer.", "0.4x − 4 = 0.25x + 2 → 0.15x = 6 → x = 40", teks="A.5(A)",
             fmt=EE, lines=2),
        MC(f"What is the solution of the system?<br>{y} = 3{x} − 5<br>2{x} + {y} = 15", ["(4, 7)", "(2, 1)", "(7, 4)", "(5, 10)"], 0, teks="A.5(C)",
           why="2x + 3x − 5 = 15 → x = 4, y = 7."),
        MC("A farm has 40 chickens and goats. Together they have 112 legs. How many goats are there?", ["16", "24", "12", "28"], 0, teks="A.5(C)",
           why="c + g = 40, 2c + 4g = 112 → 2g = 32."),
        MC("Which equation describes the line through (−2, 9) and (4, −3)?", [f"{y} = −2{x} + 5", f"{y} = −½{x} + 8", f"{y} = 2{x} + 13", f"{y} = −2{x} + 13"], 0,
           teks="A.2(B)", why="Slope −12 ÷ 6 = −2; 9 = −2(−2) + b → b = 5."),
        MC(f"{y} varies directly with {x}, and {y} = 18 when {x} = 4. What is {y} when {x} = 10?", ["24", "45", "40", "72"], 1, teks="A.2(D)",
           why="k = 18 ÷ 4 = 4.5; 4.5 × 10 = 45."),
        MC("Which is the equation of the vertical line through (−3, 7)?", [f"{y} = 7", f"{x} = 7", f"{x} = −3", f"{y} = −3"], 2, teks="A.2(G)"),
        # ---- category 2 (11) ----
        MC("A taxi ride costs <i>C</i>(<i>m</i>) = 2.4<i>m</i> + 3.5 dollars for <i>m</i> miles. What does the rate of change mean?",
           ["$3.50 per mile", "$2.40 per mile", "$5.90 for the first mile", "$2.40 to start the ride"], 1, teks="A.3(B)"),
        MC("A lake’s water level drops at a constant rate. What is the rate of change?" + htable(("Hours", [1, 3, 6, 10]), ("Level (ft)", [48, 42, 33, 21])),
           ["−3 ft per hour", "−6 ft per hour", "3 ft per hour", "−⅓ ft per hour"], 0, teks="A.3(B)"),
        MC(f"Which graph represents {y} = −⅔{x} + 2?", [small(lambda t: 2 * t / 3 + 2), small(lambda t: -2 * t / 3 + 2), small(lambda t: -2 * t / 3 - 2),
                                                       small(lambda t: -1.5 * t + 2, -4, 6.6)], 1, teks="A.3(C)",
           why="y-intercept 2, falling 2 for every 3 to the right."),
        OPEN("Choose the numbers that complete the sentence.<br>For <i>f</i>(<i>x</i>) = 3<i>x</i> − 6, the zero is ( 2 / −6 ) and the "
             "<i>y</i>-intercept is ( 2 / −6 ).", "zero 2; y-intercept −6", teks="A.3(C)", fmt=IC, lines=1,
             frames=["3<i>x</i> − 6 = 0 → zero [[2]] · <i>f</i>(0) = [[−6]]"]),
        OPEN(f"Graph the system and give its solution.<br>{y} = 2{x} − 3<br>{y} = −{x} + 3", "The lines cross at (2, 1).", teks="A.3(D)", fmt=GR,
             fig=lambda: plot(G, G, [dict(f=lambda t: 2 * t - 3, a=-2.5, b=5.5, color=RED), dict(f=lambda t: -t + 3, a=-5, b=8, color=RED)] if KEY else []),
             frames=["The lines cross at ([[2]], [[1]])."]),
        MC(f"How many solutions does the system have?<br>{y} = {x} + 1<br>{y} = {x} − 2", ["None", "One", "Two", "Infinitely many"], 0, teks="A.3(D)",
           why="Same slope, different y-intercepts: parallel lines never cross."),
        MC(f"What is the slope of 4{x} − 2{y} = 10?", ["4", "−2", "2", "−5"], 2, teks="A.3(A)", why="−2y = −4x + 10 → y = 2x − 5."),
        MC("Which system of inequalities is graphed?", [f"{y} {LE} 2{x} + 1<br>{y} &gt; −{x} − 2", f"{y} {GE} 2{x} + 1<br>{y} &lt; −{x} − 2",
                                                       f"{y} &lt; 2{x} + 1<br>{y} {GE} −{x} − 2", f"{y} {LE} 2{x} + 1<br>{y} {GE} −{x} − 2"], 0,
           fig=plot(G, G, [dict(f=lambda t: 2 * t + 1, shade="below"), dict(f=lambda t: -t - 2, shade="above", dash=True, color="#e07b00")]), teks="A.3(F)"),
        ROWS(f"Is each point in the solution set of the system {y} &lt; {x} + 2 and {y} {GE} −2{x} − 1?", ["In the solution set", "Not in the solution set"],
             [("(0, 0)", 0), ("(2, 1)", 0), ("(−1, 4)", 1), ("(3, −3)", 0)], teks="A.3(G)", fmt=MG, tip="Plug each point into BOTH inequalities."),
        MC("Ice cream sales and sunburns have a strong positive correlation. Which statement is true?",
           ["Eating ice cream causes sunburns.", "Sunburns cause people to buy ice cream.",
            "They are correlated, but hot, sunny weather likely causes both.", "There is no relationship between them."], 2, teks="A.4(B)"),
        MC("Use the linear regression for the data to predict <i>y</i> when <i>x</i> = 10." + htable((x, lx), (y, ly)),
           [nm(round(lm * 10 + lb, 1)), nm(round(lm * 10, 1)), nm(round(lb * 10 + lm, 1)), "12.9"], 0, teks="A.4(C)",
           why=f"LinReg: y = {nm(lm)}x + {nm(lb)}."),
        # ---- category 1 (10) ----
        MC(f"Which is the factored form of {x}² − 12{x} + 36?", [f"({x} − 6)²", f"({x} + 6)²", f"({x} − 6)({x} + 6)", f"({x} − 4)({x} − 9)"], 0, teks="A.10(E)"),
        OPEN(f"Drag numbers into the boxes to factor 6{x}² + 7{x} − 20.<br>{tiles(2, 3, 4, 5, 10)}<br>([[2]]{x} + [[5]])([[3]]{x} − [[4]])",
             "(2x + 5)(3x − 4)", teks="A.10(E)", fmt=DD, lines=2),
        MC(f"Which is equivalent to {fr(f'{x}<sup>−3</sup>{y}⁵', f'{x}²{y}<sup>−1</sup>')}?", [fr(f"{y}⁴", f"{x}"), fr(f"{y}⁶", f"{x}⁵"), f"{x}⁵{y}⁶", fr(f"{y}⁶", f"{x}")], 1,
           teks="A.11(B)"),
        MC(f"Which is equivalent to (27{x}⁶)<sup>⅓</sup>?", [f"9{x}²", f"3{x}³", f"3{x}²", f"9{x}<sup>18</sup>"], 2, teks="A.11(B)"),
        MC(f"Which is equivalent to (4{x}² − 3{x}) − (−{x}² + 2{x} − 6)?", [f"3{x}² − {x} − 6", f"5{x}² − 5{x} + 6", f"5{x}² − {x} + 6", f"3{x}² − 5{x} − 6"], 1,
           teks="A.10(A)"),
        MC(f"What is the quotient ({x}² + 2{x} − 35) ÷ ({x} + 7)?", [f"{x} + 5", f"{x} − 5", f"{x} − 7", f"{x} + 9"], 1, teks="A.10(C)"),
        MC(f"Which binomials can be written as a difference of two squares? Select <b>TWO</b> correct answers.",
           [f"{x}² − 49", f"{x}² + 16", f"4{x}² − 25", f"{x}² − 12", f"9{x}² + 1"], (0, 2), teks="A.10(F)", why="49 = 7² and 4x² − 25 = (2x)² − 5²."),
        MC("Which relation is <b>not</b> a function?", ["{(1, 3), (2, 3), (3, 3)}", "{(2, 3), (4, 5), (2, −1), (6, 3)}", "{(0, 1), (1, 2), (2, 4)}",
                                                       "{(−1, 5), (0, 5), (1, −5)}"], 1, teks="A.12(A)", why="x = 2 goes to two different y-values."),
        MC("Which formula gives the <i>n</i>th term of 3, 12, 48, 192, …?", ["<i>a</i><sub><i>n</i></sub> = 3 + 9(<i>n</i> − 1)",
                                                                             "<i>a</i><sub><i>n</i></sub> = 3 · 4<sup><i>n</i>−1</sup>",
                                                                             "<i>a</i><sub><i>n</i></sub> = 4 · 3<sup><i>n</i>−1</sup>", "<i>a</i><sub><i>n</i></sub> = 3 · 4<sup><i>n</i></sup>"], 1,
           teks="A.12(D)"),
        MC(f"Which equation is 3{x} − 4{y} = 12 solved for {y}?", [f"{y} = −¾{x} + 3", f"{y} = ¾{x} − 3", f"{y} = {fr(4, 3)}{x} − 4", f"{y} = 3{x} − 12"], 1, teks="A.12(E)"),
        # ---- category 4 (10) ----
        MC("What are the domain and range of the function graphed?", ["Domain: all real numbers · Range: <i>y</i> ≤ 5",
                                                                      "Domain: <i>x</i> ≤ 2 · Range: <i>y</i> ≤ 5", "Domain: all real numbers · Range: <i>y</i> ≥ 5",
                                                                      "Domain: <i>x</i> ≥ 0 · Range: all real numbers"], 0,
           fig=plot(G, G, [dict(f=lambda t: -(t - 2) ** 2 + 5, a=-1.6, b=5.6)], pts=[(2, 5, "(2, 5)")]), teks="A.6(A)"),
        OPEN("A ball’s height is <i>h</i>(<i>t</i>) = −16<i>t</i>² + 32<i>t</i> feet, for 0 ≤ <i>t</i> ≤ 2 seconds. Drag numbers to complete the range."
             f"<br>{tiles(0, 1, 2, 16, 32)}<br>[[0]] ≤ <i>h</i> ≤ [[16]]", "0 ≤ h ≤ 16", teks="A.6(A)", fmt=DD, lines=1, tip="The highest point is at t = 1."),
        MC(f"What is the axis of symmetry of {y} = −{x}² + 8{x} − 3?", [f"{x} = −4", f"{x} = 4", f"{x} = 8", f"{x} = 13"], 1, teks="A.7(A)", why="x = −8 ÷ (2 · −1) = 4."),
        MC("Which statement about the graphed function is true?", ["The zeros are −3 and 1, and the vertex is (−1, −4).", "The zeros are 3 and −1.",
                                                                   "The vertex is (−4, −1).", "The y-intercept is (0, −4)."], 0,
           fig=plot(G, G, [dict(f=lambda t: (t + 3) * (t - 1), a=-4.6, b=2.6)], pts=[(-3, 0), (1, 0), (-1, -4)]), teks="A.7(A)",
           why="y-intercept: (3)(−1) = −3."),
        MC(f"How does the graph of <i>g</i>({x}) = −{x}² + 5 compare to the graph of <i>f</i>({x}) = {x}²?",
           ["Reflected across the x-axis and shifted up 5", "Shifted right 5", "Reflected across the y-axis and shifted up 5", "Shifted down 5"], 0, teks="A.7(C)"),
        OPEN("Choose the words that complete the sentence.<br>Compared with <i>f</i>(<i>x</i>) = <i>x</i>², the graph of <i>g</i>(<i>x</i>) = 2<i>f</i>(<i>x</i>) + 6 "
             "is a vertical ( stretch / compression ) shifted ( up / down ) 6.", "stretch; up", teks="A.7(C)", fmt=IC, lines=1),
        MC(f"What are the solutions of {x}² + 6{x} − 4 = 0?", [f"−3 ± {rt(13)}", f"3 ± {rt(13)}", f"−3 ± {rt(5)}", f"−6 ± {rt(13)}"], 0, teks="A.8(A)",
           why="x² + 6x + 9 = 13 → (x + 3)² = 13."),
        OPEN(f"What is the positive solution of 4{x}² − 9 = 91? Enter your answer.", "4x² = 100 → x² = 25 → x = 5", teks="A.8(A)", fmt=EE, lines=1),
        MC("A parabola crosses the x-axis at −2 and 4 and passes through (0, −16). Which is its equation?",
           [f"<i>f</i>({x}) = ({x} + 2)({x} − 4)", f"<i>f</i>({x}) = 2({x} + 2)({x} − 4)", f"<i>f</i>({x}) = 2({x} − 2)({x} + 4)",
            f"<i>f</i>({x}) = −2({x} + 2)({x} − 4)"], 1, teks="A.6(C)", why="a(2)(−4) = −16 → a = 2."),
        MC("Which function best models the data?" + htable((x, qx), (y, qy)),
           [f"<i>y</i> = {nm(qa)}{x}² + {nm(qb)}{x} + {nm(qc)}", f"<i>y</i> = {nm(em)}{x} + {nm(eb)}", f"<i>y</i> = {nm(-qa)}{x}² − {nm(qb)}{x} + {nm(qc)}",
            f"<i>y</i> = {nm(qb)}{x}² − {nm(-qa)}{x} + {nm(qc)}"], 0, teks="A.8(B)", why="Up, then down → QuadReg."),
        # ---- category 5 (6) ----
        MC("A colony of 200 bacteria triples every hour. Which function gives the number after <i>h</i> hours?",
           ["<i>f</i>(<i>h</i>) = 3(200)<sup><i>h</i></sup>", "<i>f</i>(<i>h</i>) = 200(3)<sup><i>h</i></sup>", "<i>f</i>(<i>h</i>) = 200 + 3<i>h</i>",
            "<i>f</i>(<i>h</i>) = 200(1.3)<sup><i>h</i></sup>"], 1, teks="A.9(C)"),
        OPEN("A $900 laptop loses 20% of its value each year. Drag numbers into the boxes to complete its value function."
             f"<br>{tiles(0.2, 0.8, 1.2, 20, 900)}<br><i>V</i>(<i>t</i>) = [[900]]([[0.8]])<sup><i>t</i></sup>", "V(t) = 900(0.8)ᵗ", teks="A.9(C)", fmt=DD, lines=1),
        MC(f"Which graph represents <i>f</i>({x}) = 3(2)<sup>{x}</sup>?", [small(lambda t: 2 * 3 ** t, -8, 1.3, (0, 2, "(0, 2)")), small(lambda t: 3 * 0.5 ** t, -1.4, 8, (0, 3, "(0, 3)")),
                                                                          small(lambda t: 3 * 2 ** t, -8, 1.4, (0, 3, "(0, 3)")),
                                                                          small(lambda t: -3 * 2 ** t, -8, 1.4, (0, -3, "(0, −3)"))], 2,
           teks="A.9(D)", why="y-intercept 3, doubling to the right."),
        MC("Which statement about <i>y</i> = 45(0.6)<sup><i>x</i></sup> is true?", ["It is increasing, and its y-intercept is 45.",
                                                                                   "It is decreasing, and its y-intercept is 45.",
                                                                                   "It is decreasing, and its y-intercept is 0.6.", "It has an x-intercept at (45, 0)."], 1,
           teks="A.9(D)"),
        MC("What are the domain and range of <i>f</i>(<i>x</i>) = 5(1.2)<sup><i>x</i></sup>?", ["Domain: all real numbers · Range: <i>y</i> &gt; 0",
                                                                                               "Domain: <i>x</i> &gt; 0 · Range: <i>y</i> &gt; 5",
                                                                                               "Domain: all real numbers · Range: <i>y</i> ≥ 5",
                                                                                               "Domain: <i>x</i> ≥ 0 · Range: all real numbers"], 0, teks="A.9(A)"),
        MC("A car’s value is <i>V</i>(<i>t</i>) = 12,000(0.92)<sup><i>t</i></sup>. What does 12,000 represent?",
           ["The value lost each year", "The value when it was bought", "The value after one year", "The rate of decay"], 1, teks="A.9(B)"),
    ]
    return sections


def check_blueprint(items):
    from collections import Counter
    t = [tk(it["teks"]) for it in items]
    cats = Counter(cat_of(it["teks"]) for it in items)
    ready = Counter(v for v in t if v in READY)
    assert len(items) == 50 and all(ready[r] == 2 for r in READY) and sum(ready.values()) == 32, (len(items), ready)
    assert [cats[c] for c in range(1, 6)] == [10, 11, 13, 10, 6], cats


def practice_test(n, items):
    global PT
    check_blueprint(items)
    items = list(items)
    random.Random(100 + n).shuffle(items)  # mixed order, like the real test
    h = (f'<h2 class="ch">STAAR Practice Test {n}<small>50 questions · all five reporting categories · original questions</small></h2>'
         '<p class="note">Use only the STAAR reference sheet and a graphing calculator. Give yourself one class period or more; '
         'there is no time limit on the real test. Answer every question: there is no penalty for guessing.</p>')
    PT = True
    for k, it in enumerate(items, 1):
        h += render(it, k)
    PT = False
    rows = ""
    for k, it in enumerate(items, 1):
        if it["kind"] == "mc":
            L, idx = shown(it, k)
            a = ", ".join(l for l, j in zip(L, idx) if j in it["right"])
        elif it["kind"] == "rows":
            a = " · ".join(it["cols"][r].split()[0] for _, r in it["rows"])
        else:
            a = it["ans"]
        t = tk(it["teks"])
        rows += (f"<tr><td>{k}</td>" + (f"<td style='text-align:left'>{a}</td>" if KEY else "")
                 + f"<td style='white-space:nowrap'>{t}{' ★' if t in READY else ''}</td><td>{cat_of(it['teks'])}</td><td>{FIXIT[t]}</td></tr>")
    h += (f'<div class="part" style="break-before:page">Practice Test {n} · {"Answer Key and " if KEY else ""}Fix-It Map</div>'
          '<p class="note">Circle the numbers you missed. Each one tells you the TEKS (★ = readiness standard, tested the most) and the '
          'chapter to review. Count your misses by category to find your weakest area.</p>'
          '<table class="t fix"><tr><th>#</th>' + ("<th>Answer</th>" if KEY else "") + "<th>TEKS</th><th>Category</th><th>Review chapter</th></tr>"
          + rows + "</table>")
    return h


REF = [("Perfect square trinomials", "<i>a</i>² ± 2<i>ab</i> + <i>b</i>² = (<i>a</i> ± <i>b</i>)²", "Factoring like 9x² − 12x + 4", "11"),
       ("Difference of squares", "<i>a</i>² − <i>b</i>² = (<i>a</i> − <i>b</i>)(<i>a</i> + <i>b</i>)", "Factoring x² − 49; A.10(F)", "10, 11"),
       ("Product / quotient of powers", "<i>a</i><sup><i>m</i></sup><i>a</i><sup><i>n</i></sup> = <i>a</i><sup><i>m</i>+<i>n</i></sup> · "
                                        "<i>a</i><sup><i>m</i></sup> ÷ <i>a</i><sup><i>n</i></sup> = <i>a</i><sup><i>m</i>−<i>n</i></sup>", "Simplifying exponents, A.11(B)", "7"),
       ("Power of a power", "(<i>a</i><sup><i>m</i></sup>)<sup><i>n</i></sup> = <i>a</i><sup><i>mn</i></sup>", "(2x³)⁴ — raise the 2 as well!", "7"),
       ("Rational and negative exponents", f"<i>a</i><sup><i>m</i>/<i>n</i></sup> = {rt('<i>a</i><sup><i>m</i></sup>', '<i>n</i>')} · "
                                           "<i>a</i><sup>−<i>n</i></sup> = 1 ÷ <i>a</i><sup><i>n</i></sup>", "Roots as exponents; no negative exponents in answers", "7"),
       ("Standard form", "<i>Ax</i> + <i>By</i> = <i>C</i>", "Finding both intercepts fast (cover x, then cover y)", "3, 4"),
       ("Slope-intercept form", "<i>y</i> = <i>mx</i> + <i>b</i>", "Graphing; reading the rate (m) and start (b)", "3, 4"),
       ("Point-slope form", "<i>y</i> − <i>y</i>₁ = <i>m</i>(<i>x</i> − <i>x</i>₁)", "Line through a point; parallel lines, A.2(B), A.2(E)", "3, 4"),
       ("Slope of a line", f"<i>m</i> = {fr('<i>y</i>₂ − <i>y</i>₁', '<i>x</i>₂ − <i>x</i>₁')}", "Rate of change from two points or a table", "3"),
       ("Quadratic standard and vertex form", "<i>ax</i>² + <i>bx</i> + <i>c</i> · <i>a</i>(<i>x</i> − <i>h</i>)² + <i>k</i>", "Vertex (h, k); y-intercept c", "9"),
       ("Quadratic formula", f"<i>x</i> = {fr('−<i>b</i> ± √<span class=ov><i>b</i>² − 4<i>ac</i></span>', '2<i>a</i>')}", "Any quadratic equation, A.8(A)", "11"),
       ("Axis of symmetry", f"<i>x</i> = {fr('−<i>b</i>', '2<i>a</i>')}", "Vertex x-value; then plug in for y", "9")]
NOT_ON_SHEET = ["Exponential growth and decay: <i>f</i>(<i>x</i>) = <i>a</i>(1 ± <i>r</i>)<sup><i>x</i></sup>, and <i>a</i> = start, <i>b</i> = factor (Ch 8)",
                "Domain and range written with inequalities; open dot = &lt; or &gt;, closed dot = ≤ or ≥ (Ch 1, 3, 9)",
                "Dashed line = &lt; or &gt;; solid line = ≤ or ≥; shade above for <i>y</i> &gt;, below for <i>y</i> &lt; (Ch 6)",
                "Flip the inequality sign when you multiply or divide by a negative (Ch 5)",
                "Arithmetic: <i>a</i><sub><i>n</i></sub> = <i>a</i>₁ + <i>d</i>(<i>n</i> − 1) · Geometric: <i>a</i><sub><i>n</i></sub> = <i>a</i>₁ · <i>r</i><sup><i>n</i>−1</sup> (Ch 2)",
                "Transformations: (<i>x</i> − <i>h</i>) moves right, + <i>k</i> moves up, negative <i>a</i> reflects (Ch 4, 9)",
                "Discriminant <i>b</i>² − 4<i>ac</i>: positive → 2, zero → 1, negative → 0 real solutions (Ch 11)",
                "Correlation <i>r</i>: near ±1 strong, near 0 weak; correlation is not causation (Ch 3)",
                "Calculator: Y= and 2nd TRACE (zero, maximum, intersect); STAT → CALC (LinReg 4, QuadReg 5, ExpReg 0) (Ch 3, 8, 11)"]
TYPES = [("Multiple choice", "≈ 77%", "Pick one answer.", "Work it first, then find your answer. Eliminate choices you know are wrong."),
         ("Drag and drop", "≈ 9%", "Drag tiles into boxes. A tile may be used more than once, and some tiles are not used.",
          "Solve on paper first, then drag. Check every box before moving on."),
         ("Graphing", "≈ 4%", "Click points to draw a line or curve; choose solid or dashed and the shaded side.",
          "Plot two exact points (intercepts are easiest). For inequalities: line type first, then shading."),
         ("Inline choice", "≈ 4%", "Pick a word or number from a drop-down menu in a sentence.", "Read the whole sentence after you choose. Each menu is scored."),
         ("Multiselect", "≈ 2%", "Select ALL the correct answers (the question says how many).", "Treat each choice as true/false. Choose exactly the number asked."),
         ("Equation editor", "≈ 1%", "Type your answer (a number or expression) with the on-screen keypad.", "Check signs and decimals. Fractions are fine unless it says to round."),
         ("Hot spot", "≈ 1%", "Click a point or region on a graph or picture.", "Find the exact coordinates before you click."),
         ("Match table grid", "≈ 1%", "Mark one box in each row of a table.", "Answer every row; test each row on its own.")]


def staar_unit():
    t1, t2 = test1(), test2()
    h = ('<h2 class="ch">STAAR Unit · Getting Ready for the Algebra I EOC<small>Reference sheet · question types · blueprint · '
         'two full practice tests</small></h2>')
    h += ('<h3>The reference sheet <small>· what it gives you, and when to use it</small></h3>'
          '<p class="note">On the test you get the STAAR Algebra I reference materials (online or on paper). Know what is on it so you '
          'reach for it, and know what is <b>not</b> on it so you memorize that.</p><table class="t ref"><tr><th>On the sheet</th>'
          '<th>Formula</th><th>Use it for</th><th>Chapter</th></tr>'
          + "".join(f"<tr><td style='text-align:left'><b>{a}</b></td><td>{b}</td><td style='text-align:left'>{c}</td><td>{d}</td></tr>"
                    for a, b, c, d in REF) + "</table>"
          '<div class="box"><p class="h">Not on the sheet: memorize these</p><ul>' + "".join(f"<li>{v}</li>" for v in NOT_ON_SHEET) + "</ul></div>")
    h += ('<h3>Question types <small>· how often each appeared on the 2024–2026 tests</small></h3><table class="t ref"><tr><th>Type</th>'
          '<th>Share</th><th>What you do</th><th>Game plan</th></tr>'
          + "".join(f"<tr><td style='text-align:left'><b>{a}</b></td><td>{b}</td><td style='text-align:left'>{c}</td><td style='text-align:left'>{d}</td></tr>"
                    for a, b, c, d in TYPES) + "</table>"
          '<p class="note">Some questions are worth 2 points (most drag and drop, inline choice, multiselect, and graphing). Partial '
          'credit is possible, so never leave one blank.</p>')
    ready_rows = "".join(f"<tr><td>{r}</td><td>{CATNAME[CAT[r.split('.')[1][:-1]]]}</td><td>{FIXIT[r]}</td></tr>" for r in READY)
    h += ('<h3>The blueprint <small>· what a 50-question test looks like</small></h3><table class="t ref"><tr><th>Category</th>'
          '<th>Questions</th></tr>'
          + "".join(f"<tr><td style='text-align:left'>{c}. {CATNAME[c]}</td><td>{n}</td></tr>" for c, n in zip(range(1, 6), [10, 11, 13, 10, 6]))
          + '</table><p class="note">The 16 <b>readiness standards</b> below are tested twice on every recent test: that is 32 of the '
            '50 questions. Master these first.</p><table class="t ref"><tr><th>TEKS</th><th>Category</th><th>Review chapter</th></tr>'
          + ready_rows + "</table>")
    h += ('<div class="box ex"><p class="h">Test-day game plan</p><ol>'
          '<li>Read the last sentence first: what is the question asking for?</li>'
          '<li>Write on scratch paper for every question, even the easy ones.</li>'
          '<li>Use the calculator to check: graph both sides, use intersect, zero, maximum, or a regression.</li>'
          '<li>Plug your answer back in when you can (equations, systems, zeros).</li>'
          '<li>Watch the words NOT, BEST, and Select TWO.</li>'
          '<li>Flag hard questions, finish the test, then come back. Never leave a question blank.</li></ol></div>')
    h += practice_test(1, t1) + practice_test(2, t2)
    return h

# ---------- book ----------
CSS = """
@page { size: letter; margin: 0.55in 0.6in 0.6in; }
body { font-family: Arial, Helvetica, sans-serif; font-size: 11.5pt; line-height: 1.38; color: #111; background: #fff; margin: 0; }
.cover { height: 9.6in; display: flex; flex-direction: column; justify-content: center; text-align: center; break-after: page; }
.cover h1 { font-size: 34pt; margin: 0 0 10px; } .cover .s { font-size: 15pt; } .cover .v { font-size: 20pt; font-weight: bold; color: #0b6b3a; margin-top: 18px; }
h2.ch { break-before: page; background: #0b6b3a; color: #fff; padding: 10px 14px; margin: 0 0 8px; font-size: 20pt; }
h2.ch small { display: block; font-size: 11pt; font-weight: normal; }
h3 { break-after: avoid; font-size: 14pt; border-bottom: 2px solid #0b6b3a; margin: 16px 0 6px; padding-bottom: 2px; } h3 small { font-weight: normal; font-size: 10pt; color: #444; }
.box { border: 1.5px solid #0b6b3a; border-radius: 6px; padding: 4px 12px; margin: 6px 0; break-inside: avoid; }
.box.ex { border-color: #2f6fdd; background: #f3f7ff; } .box .h { font-weight: bold; color: #0b6b3a; } .box.ex .h { color: #2f6fdd; }
.box p { margin: 4px 0; } .vocab td { padding: 2px 8px; border-bottom: 1px solid #ddd; } .vocab { border-collapse: collapse; }
.q { display: flex; gap: 8px; padding: 6px 0 8px; border-bottom: 1px solid #ccc; break-inside: avoid; }
.n { font-weight: bold; min-width: 26px; } .body { flex: 1; } .q p { margin: 3px 0 5px; }
.row { display: flex; gap: 14px; align-items: flex-start; } .g { display: block; margin: 2px 0 4px; }
.mc p { margin: 4px 0 4px 6px; } .mc .ok { color: #c8102e; font-weight: bold; } .mc .ok > b { border: 2px solid #c8102e; border-radius: 50%; padding: 0 4px; }
.ans { color: #c8102e; font-weight: bold; margin-top: 4px; } .why { color: #c8102e; font-size: 10pt; margin-top: 2px; }
.t { border-collapse: collapse; margin: 4px 0; } .t td, .t th { border: 1px solid #111; padding: 2px 10px; text-align: center; }
.t th { background: #eef5f0; } .rows td { font-size: 14pt; } .rows td.lab { font-size: 11.5pt; text-align: left; }
.tag { font-size: 9pt; font-weight: bold; color: #555; text-transform: uppercase; letter-spacing: .3px; }
.part { font-size: 13pt; font-weight: bold; background: #e8e8e8; padding: 4px 10px; margin: 14px 0 6px; }
.part.staar { background: #fff1d6; } .note { font-size: 10.5pt; color: #333; }
.fr { display: inline-flex; flex-direction: column; vertical-align: middle; text-align: center; font-size: 0.85em; line-height: 1.1; }
.fr span:first-child { border-bottom: 1px solid currentColor; padding: 0 2px; }
.bl { display: inline-block; min-width: 0.7in; border-bottom: 1.5px solid #111; text-align: center; color: #c8102e; font-weight: bold; padding: 0 3px; }
.tip { border-left: 5px solid #2f6fdd; background: #eef3fc; padding: 3px 10px; margin: 6px 0; }
.ov { border-top: 1.3px solid currentColor; padding: 0 2px; }
.credits { break-after: page; font-size: 11pt; } .credits p { margin: 6px 0; }
.frames p { margin: 8px 0; } .toc td { padding: 3px 10px; } .plan li { margin: 3px 0; }
.tiles { display: inline-flex; gap: 8px; flex-wrap: wrap; margin: 4px 0; } .tile { border: 1.5px solid #555; border-radius: 4px; padding: 1px 10px; background: #f4f4f4; }
.ref td, .ref th { font-size: 10.5pt; padding: 3px 8px; } .fix td, .fix th { font-size: 10pt; padding: 1px 8px; } .fix tr { break-inside: avoid; } .ref { break-inside: avoid; }
"""
CSS_IEP = """
body { font-size: 14pt; line-height: 1.5; } .q { padding: 10px 0 14px; } .tag { font-size: 10pt; }
.rows td.lab { font-size: 13pt; } .why { font-size: 12pt; } .note { font-size: 12.5pt; }
"""


CREDITS = f"""<div class="credits"><h3>About this book</h3>
<p><b>{TITLE}</b><br>Written by Robin Pandey (Mr. Pandey) with AI assistance.</p>
<p><b>© 2026 Robin Pandey.</b> Use it freely for noncommercial purposes: you may copy, print, share, and adapt it.
No one may sell it or charge money for it. Released under the same Creative Commons Attribution-NonCommercial 4.0
license as its source materials.</p>
<h3>About the author</h3>
<p><b>Robin Pandey</b>, known to students as Mr. Pandey, teaches Algebra I in Texas with the Bluebonnet Learning
curriculum. Every topic in the course ends with a test that never moves, and the year ends with STAAR, so Mr. Pandey
builds tools to keep every student ready for that date: lessons with worked answers, bell work, exit tickets,
review days, and a class website that tells students what to do each day.</p>
<p>This book grew out of that work. Mr. Pandey wanted one place where a student can learn the words, see a worked
example, practice every skill the topic test checks, and then practice the way STAAR asks. The IEP edition holds the
same questions, with fewer answer choices, fill-in steps, tips, and larger print, so that every student in the
class works from the same book.</p>
<p>Mr. Pandey gives this book away for free so it can help students in any classroom, this year and next.</p>
<h3>License and attribution</h3>
<p>This work is based on original works of the Texas Education Agency and Carnegie Learning, Inc. This work is
made available under a Creative Commons Attribution-Non-Commercial-4.0 International License. This does not in any
way imply endorsement by those authors of this work.</p>
<p>License terms: <b>https://creativecommons.org/licenses/by-nc/4.0/</b></p>
<p>Source materials: Bluebonnet Learning Secondary Mathematics, Algebra I, Edition 1 (© 2024 Texas Education Agency;
portions © 2021 Carnegie Learning, Inc.), used under the same license.</p>
<p>STAAR® is a registered trademark of the Texas Education Agency. This book is not produced, reviewed, or endorsed by
the Texas Education Agency, Carnegie Learning, Inc., or any school district. All practice questions are original;
no STAAR test questions are reproduced.</p>
<p>Questions or corrections: tell Mr. Pandey.</p></div>"""


def chapter(c, num):
    h = (f'<h2 class="ch">Chapter {num} · {c["title"]}<small>{c["module"]} · Topic {c["code"][-1]} · '
         f'TEKS {c["teks"]}</small></h2>')
    h += ('<div class="box"><p class="h">Words to know</p><table class="vocab">'
          + "".join(f"<tr><td><b>{a}</b></td><td>{b}</td></tr>" for a, b in c["vocab"]) + "</table></div>")
    q = 0
    for s in c["sections"]:
        h += f'<h3>{s["title"]} <small>· {s["lesson"]}</small></h3>'
        h += f'<div class="box"><p class="h">Key idea</p>{s["idea"]}</div>'
        h += f'<div class="box ex"><p class="h">Worked example</p>{s["example"]}</div>'
        for it in s["items"]:
            q += 1
            h += render(it, q)
    h += (f'<div class="part" style="break-before:page">Chapter {num} Skill Check</div>'
          '<p class="note">Mixed practice on every skill in this chapter, shown in different ways (graphs, tables, stories, '
          'equations). If you can do all of these, you know this topic. '
          + ("Use the tips and fill in the blanks. Choose <b>one</b> answer unless it says <b>Select TWO</b>."
             if IEP else "Show your work. <b>Select TWO</b> means choose exactly two answers.") + "</p>")
    check = list(c["check"])
    random.Random(num).shuffle(check)  # fixed mixed order (same in every edition), never the test's order
    for k, it in enumerate(check, 1):
        h += render(it, k)
    h += ('<div class="part staar" style="break-before:page">STAAR Corner</div><p class="note">STAAR-style questions on '
          'this chapter’s TEKS. The label tells you the question type you will see on the computer test.</p>')
    for k, it in enumerate(c["staar"], 1):
        h += render(it, k)
    return h


def build(key, iep):
    global KEY, IEP
    KEY, IEP = key, iep
    chs = [f() for f in BOOK]
    ver = "IEP Edition" if iep else "Student Edition"
    body = (f'<div class="cover"><h1>{TITLE}</h1><p class="s">Algebra I · Bluebonnet Learning · TEKS-aligned practice</p>'
            f'<p class="v">{ver}{" · Answer Key" if key else ""}</p>'
            f'<p class="s" style="margin-top:28px">Written by <b>Robin Pandey</b> (Mr. Pandey) with AI assistance</p>'
            '<p class="s" style="font-size:10.5pt">© 2026 Robin Pandey · Free for noncommercial use</p>'
            + ("" if key else '<p class="s" style="margin-top:40px">Name ______________________________ &nbsp; Period _____</p>')
            + "</div>" + CREDITS)
    body += ('<h2 class="ch" style="break-before:auto">How to use this book</h2><ol class="plan">'
             "<li><b>Words to know</b>: read the vocabulary before each chapter.</li>"
             "<li><b>Key idea + Worked example</b>: read the box, then try the practice right after it.</li>"
             "<li><b>Skill Check</b>: mixed practice on every skill in the chapter. Do it before your topic test. "
             "Missed one? Go back to the section with the same skill.</li>"
             "<li><b>STAAR Corner</b>: the question types from the STAAR Algebra I test (multiselect, inline choice, "
             "drag and drop, text entry). Keep the STAAR reference sheet next to you.</li>"
             + ("<li><b>Tips</b> and <b>fill-in steps</b> walk you through each problem. Fill in every blank.</li>" if iep else "")
             + '</ol><table class="toc"><tr><th>Chapter</th><th>Topic</th><th>TEKS</th></tr>'
             + "".join(f"<tr><td>{k}</td><td>{c['code']} · {c['title']}</td><td>{c['teks']}</td></tr>"
                       for k, c in enumerate(chs, 1))
             + "<tr><td>STAAR</td><td>Reference sheet guide · question types · blueprint · Practice Tests 1 and 2</td>"
               "<td>All tested TEKS</td></tr></table>")
    body += "".join(chapter(c, k) for k, c in enumerate(chs, 1)) + staar_unit()
    name = "Algebra-I-Game-Plan" + ("-IEP" if iep else "") + ("-ANSWER-KEY" if key else "")
    OUT.mkdir(exist_ok=True)
    src = OUT / f"{name}.html"
    src.write_text(f"<!doctype html><meta charset='utf-8'><title>{TITLE}</title><style>{CSS}{CSS_IEP if iep else ''}"
                   f"</style>{body}", encoding="utf-8")
    pdf = OUT / f"{name}.pdf"
    subprocess.run([EDGE, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={pdf}", src.as_uri()],
                   check=True, capture_output=True)
    src.unlink()
    finish(pdf)
    print(pdf)


COVER = ROOT / "Algebra I Game Plan Topic" / "Book Cover.png"


def finish(pdf):
    """Cover art as page 1 (the printed title page stays as page 2), then lock the ANSWER KEYS only.
    Student and IEP editions stay open. Password comes from GAME_PLAN_PW so it never lands in the repo."""
    import os, fitz
    d = fitz.open(pdf)
    if d[0].get_text().strip():  # first page not yet the image-only cover
        r = d[0].rect
        page = d.new_page(0, width=r.width, height=r.height)
        page.draw_rect(r, color=None, fill=(0.07, 0.42, 0.25))  # green bleed behind the 800x1024 art
        page.insert_image(r, filename=str(COVER), keep_proportion=True)
    pw = os.environ.get("GAME_PLAN_PW") if "ANSWER-KEY" in pdf.name else None
    tmp = pdf.with_suffix(".tmp.pdf")
    d.save(tmp, garbage=3, deflate=True,
           **({"encryption": fitz.PDF_ENCRYPT_AES_256, "user_pw": pw, "owner_pw": pw} if pw else {}))
    d.close()
    tmp.replace(pdf)


if __name__ == "__main__":
    import sys
    if sys.argv[1:] == ["--finish"]:  # cover + lock the PDFs already in Game Plan/ without rebuilding
        for f in sorted(OUT.glob("Algebra-I-Game-Plan*.pdf")):
            finish(f); print(f)
    else:
        for iep in (False, True):
            for key in (False, True):
                build(key, iep)

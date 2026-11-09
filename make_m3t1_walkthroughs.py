"""M3T1 "How to Solve" walkthroughs for students: every item as Spot it -> Fastest way -> Check -> Trap.
  Review (open to students):  Module 3 topic 1/REVIEW/T1-Review-How-To-Solve.pdf     (items from make_m3t1_review.py)
  Test (password-protected):  assessment/M3 TOPIC 1/M3T1-Test-How-To-Solve.pdf      (items from make_m3t1_test_keys.py)
Run:  python make_m3t1_walkthroughs.py <password>"""
import subprocess, sys
from pathlib import Path

import fitz
import make_m3t1_review as RV
import make_m3t1_test_keys as TK

ROOT = Path(__file__).parent
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

MOVES = [
    ("Word problem → equation", "The amount that happens <b>per</b> week/item gets the x. The amount you <b>start</b> with or pay once is the plain number. y = rate·x + start."),
    ("Distribute first", "Multiply the outside number by <b>everything</b> inside ( ), watch the signs, then combine like terms on each side."),
    ("Variables on both sides", "Move the <b>smaller</b> x-term. The x stays positive, so you never have to flip an inequality."),
    ("One, none, or infinite?", "Simplify both sides. Different x-terms → <b>one</b>. Same x-terms, different numbers → <b>none</b>. Identical sides → <b>infinite</b>."),
    ("Inequalities", "Multiply or divide by a <b>negative</b> → <b>flip</b> the sign. Open circle for &lt; &gt;, closed for ≤ ≥. With x on the left, the sign points the way to shade."),
    ("Formulas and forms", "Undo what is done to the letter you want, in reverse order. When you divide, divide <b>every</b> term."),
    ("Always check", "Put your answer back in the original problem. Both sides must match (or the inequality must be true)."),
]

# (spot it, fastest-way steps, check, trap) — one per review item, in make_m3t1_review.items() order
REVIEW = [
    ("“Each week” is a rate → it multiplies x. “Has $40” is the start → the plain number.",
     ["Rate: 15 per week → 15x", "Start: 40", "y = 15x + 40"], "After 2 weeks: 40 + 15 + 15 = 70, and 15(2) + 40 = 70 ✓",
     "y = 15 + 40x swaps the rate and the start."),
    ("Parentheses on both sides and “No solution” is a choice → distribute and compare.",
     ["Left: 5 − 4k − 12 = −4k − 7", "Right: 9 − 4k − 12 = −4k − 3", "Same −4k, different numbers (−7 ≠ −3) → <b>No solution</b>"],
     "Once the k-terms match, stop. Just compare the numbers.", "Picking a number. No number can make −7 equal −3."),
    ("Inequality with a negative x-term → move the smaller x-term so you don't have to flip.",
     ["Distribute: 12 − 3t &gt; −2t + 15", "Add 3t (the smaller x-term goes away): 12 &gt; t + 15", "Subtract 15: −3 &gt; t, which means <b>t &lt; −3</b>"],
     "Try t = −4: 3(8) = 24 and 8 + 15 = 23, 24 &gt; 23 ✓", "t &gt; −3: you divided by −1 and forgot to flip."),
    ("Decimals → you can multiply everything by 10 to work with whole numbers.",
     ["Distribute: 1.2x − 1.8 = −1.8x + 4.2", "Add 1.8x: 3x − 1.8 = 4.2", "Add 1.8: 3x = 6 → <b>x = 2</b>"],
     "0.3(8 − 6) = 0.6 and −3.6 + 4.2 = 0.6 ✓", "Only multiplying 0.3 by 4x and not by the 6."),
    ("“One, none, or infinite?” → simplify each side and compare.",
     ["Left: ⅓ · 12x + ⅓ · 30 = 4x + 10", "Right: 4x + 8 + 2 = 4x + 10", "Identical sides → <b>infinite solutions</b>"],
     "Try x = 0: ⅓(30) = 10 and 4(2) + 2 = 10 ✓. Any x works.", "Getting 0 = 0 and writing “x = 0”. 0 = 0 means <i>every</i> x works."),
    ("“Some pens” is the unknown → pens get the x. Exactly 4 notebooks is a fixed cost.",
     ["Notebooks: 4 × 1.75 = 7.00", "Pens: 1.20x", "<b>y = 1.20x + 7.00</b>"], "2 pens: 7.00 + 2.40 = 9.40, and 1.20(2) + 7 = 9.40 ✓",
     "y = 1.75x + 4.80: the x went on the notebooks instead of the pens."),
    ("Standard form → slope-intercept: get y alone.",
     ["Subtract 2x: 5y = −2x + 15", "Divide <b>every</b> term by 5", "<b>y = −⅖x + 3</b>"], "x = 5: 2(5) + 5y = 15 → y = 1, and −⅖(5) + 3 = 1 ✓",
     "Dividing only the x-term: y = −⅖x + 15."),
    ("Formula with only multiplication → divide by everything that is not h.",
     ["h is multiplied by ℓw", "Divide both sides by ℓw", "<b>h = V/(ℓw)</b>"], "ℓ = 2, w = 3, h = 4 gives V = 24, and 24 ÷ 6 = 4 ✓",
     "h = V − ℓw: you subtract to undo adding, not to undo multiplying."),
    ("Inequality with x on both sides → move the smaller x-term, then graph.",
     ["Distribute: 2.5m − 3 &lt; −1.5m − 27", "Add 1.5m: 4m − 3 &lt; −27", "Add 3: 4m &lt; −24 → <b>m &lt; −6</b>",
      "Open circle at −6 (no “equal to”), shade left"],
     "m = −7: −17.5 − 3 = −20.5 and −1.5(11) = −16.5, −20.5 &lt; −16.5 ✓", "A closed circle. &lt; does not include −6."),
    ("Point-slope → slope-intercept: distribute, then get y alone.",
     ["Distribute: y − 4 = 3x + 6", "Add 4: <b>y = 3x + 10</b>"], "x = −2: y − 4 = 0, so y = 4, and 3(−2) + 10 = 4 ✓",
     "y = 3x + 2: subtracting 4 instead of adding it."),
    ("Two shapes with equal areas → write each area, set them equal.",
     ["Triangle: ½ · 10 = 5 first, so 5(3n − 6) = 15n − 30", "Rectangle: 5(n + 4) = 5n + 20", "15n − 30 = 5n + 20 → 10n = 50 → <b>n = 5</b>"],
     "Height 3(5) − 6 = 9: ½ · 10 · 9 = 45. Width 5 + 4 = 9: 5 · 9 = 45 ✓", "Forgetting the ½ in the triangle's area."),
    ("Looking for no solution → you need the <b>same</b> x-term on both sides.",
     ["Distribute each choice", "3(x − 2) = 3x + 5 → 3x − 6 = 3x + 5: same 3x, −6 ≠ 5", "<b>3(x − 2) = 3x + 5</b>"],
     "3(x − 2) = 3x − 6 is identical → infinite, not none.", "Choices with different x-terms always have exactly one solution."),
    ("Negative in front of x → you will divide by a negative and flip.",
     ["Subtract 7: −4x ≥ 12", "Divide by −4 and flip: <b>x ≤ −3</b>"], "x = −4: 16 + 7 = 23 ≥ 19 ✓", "x ≥ −3: no flip."),
    ("Solve a formula for w → undo the adding, then the multiplying.",
     ["Subtract 2ℓ: 2w = P − 2ℓ", "Divide every term by 2: <b>w = (P − 2ℓ)/2 = P/2 − ℓ</b>"], "ℓ = 3, w = 2 → P = 10, and 10/2 − 3 = 2 ✓",
     "w = P/2 − 2ℓ: only the P was divided by 2."),
    ("“At most” → ≤. Fee paid once is the start; “per class” is the rate.",
     ["25 + 8c ≤ 90", "Subtract 25: 8c ≤ 65", "c ≤ 8.125 → whole classes → <b>at most 8</b>"], "8 classes: 25 + 64 = 89 ≤ 90 ✓. 9 classes: 97 &gt; 90 ✗",
     "Rounding up to 9. You can't go over $90."),
]

TEST = [
    ("“Saves $20 per week” is the rate → 20x. “$50 from her aunt” is the start.",
     ["Rate 20 → 20x, start 50", "y = 20x + 50 → <b>B</b>"], "2 weeks: 50 + 40 = 90, and 20(2) + 50 = 90 ✓", "A swaps the numbers. C and D subtract, but her money goes up."),
    ("Parentheses on both sides and “No solution” is a choice → distribute and compare.",
     ["Left: 8 − 6p − 24 = −6p − 16", "Right: 12 − 6p − 20 = −6p − 8", "Same −6p, −16 ≠ −8 → <b>J. No solution</b>"],
     "Once the p-terms match, stop. Just compare the numbers.", "Distributing −6 as +6 and getting the 24 with the wrong sign."),
    ("Negative x-term in an inequality → move the smaller x-term so you don't have to flip.",
     ["Distribute: 8 − 4s &gt; −3s + 9", "Add 4s: 8 &gt; s + 9", "Subtract 9: −1 &gt; s → <b>s &lt; −1 (D)</b>"],
     "s = −2: 4(4) = 16 and 6 + 9 = 15, 16 &gt; 15 ✓", "s &gt; −1: divided by −1 and forgot to flip."),
    ("Decimals with x on both sides → distribute, then collect x's.",
     ["Distribute: 2x − 0.8 = −2.4x + 3.6", "Add 2.4x and 0.8: 4.4x = 4.4", "<b>x = 1</b>"], "0.4(5 − 2) = 1.2 and −2.4 + 3.6 = 1.2 ✓",
     "Writing 0.4 · 2 = 0.08. It is 0.8."),
    ("“One, none, or infinite?” → simplify each side and compare.",
     ["Left: ⅓ · 9x + ⅓ · 45 = 3x + 15", "Right: 3x + 9 + 6 = 3x + 15", "Identical sides → <b>infinitely many solutions</b>"],
     "x = 0: ⅓(45) = 15 and 9 + 6 = 15 ✓", "0 = 0 means every x works, not x = 0."),
    ("x doughnuts is the unknown → the doughnuts get the x. Exactly 3 eclairs is a fixed cost.",
     ["Eclairs: 3 × 2.25 = 6.75", "Doughnuts: 2.80x", "<b>y = 2.80x + 6.75</b>"], "1 doughnut: 6.75 + 2.80 = 9.55 ✓", "Putting the x on the eclairs (2.25x)."),
    ("Standard form → slope-intercept: get y alone.",
     ["Subtract 5x: 3y = −5x + 9", "Divide <b>every</b> term by 3", "<b>y = −(5/3)x + 3</b>"], "x = 3: 15 + 3y = 9 → y = −2, and −5 + 3 = −2 ✓",
     "Leaving 9 instead of 9 ÷ 3 = 3."),
    ("Formula with only multiplication → divide by everything that is not r.",
     ["r is multiplied by 2π", "Divide both sides by 2π: <b>r = C/(2π)</b>"], "r = 1 gives C = 2π, and 2π ÷ 2π = 1 ✓", "r = C − 2π: subtracting undoes adding, not multiplying."),
    ("Inequality with x on both sides → move the smaller x-term, then graph.",
     ["Distribute: 1.5m − 2 &lt; −2m − 16", "Add 2m: 3.5m − 2 &lt; −16", "Add 2: 3.5m &lt; −14 → <b>m &lt; −4</b>",
      "Open circle at −4, shade left"],
     "m = −5: −9.5 and −2(3) = −6, −9.5 &lt; −6 ✓", "Flipping the sign here. You divided by +3.5, so no flip."),
    ("Point-slope → slope-intercept: distribute, then get y alone.",
     ["Distribute: y − 5 = 2x + 6", "Add 5: <b>y = 2x + 11</b>"], "x = −3: y − 5 = 0 → y = 5, and −6 + 11 = 5 ✓", "y = 2x + 1: subtracting 5 instead of adding."),
    ("Two shapes with equal areas → write each area, set them equal.",
     ["Triangle: ½ · 8 = 4 first, so 4(2n − 4) = 8n − 16", "Rectangle: 6(3 + n) = 18 + 6n", "8n − 16 = 6n + 18 → 2n = 34 → <b>n = 17</b>"],
     "Height 30: ½ · 8 · 30 = 120. Width 20: 6 · 20 = 120 ✓", "Forgetting the ½ in the triangle's area."),
]

CSS = """@page{size:letter;margin:.5in .55in}body{font:11pt/1.4 'Segoe UI',Arial,sans-serif;color:#111;margin:0}
h1{font-size:18pt;margin:0}.sub{color:#444;margin:2px 0 10px}
.moves{border:2px solid #1d3557;border-radius:8px;padding:6px 12px;margin:8px 0 12px}.moves h2{font-size:13pt;margin:2px 0 6px;color:#1d3557}
.moves li{margin:3px 0}.item{break-inside:avoid;border:1px solid #bcc8d6;border-radius:8px;padding:8px 12px;margin:10px 0}
.item h3{margin:0 0 4px;font-size:12pt;color:#1d3557}.q{margin:0 0 6px}.ans{font-family:Cambria,serif;font-size:13pt;background:#e8f4ec;
border-left:4px solid #2a9d8f;padding:3px 10px;margin:4px 0}.row{margin:3px 0}.lb{display:inline-block;min-width:92px;font-weight:700;font-size:9.5pt}
.spot .lb{color:#457b9d}.do .lb{color:#1d3557}.chk .lb{color:#2a9d8f}.trap .lb{color:#c8102e}
.do ol{margin:2px 0 2px 18px;padding:0;font-family:Cambria,serif;font-size:11.5pt}.fr{display:inline-flex;flex-direction:column;vertical-align:middle;
text-align:center;font-size:.85em;line-height:1.1}.fr>span:first-child{border-bottom:1px solid}"""


def card(n, q, ans, spot, steps, check, trap, extra=""):
    return (f'<div class="item"><h3>Question {n}</h3><p class="q">{q}</p><div class="ans">Answer: {ans}</div>'
            f'<div class="row spot"><span class="lb">🔍 Spot it</span>{spot}</div>'
            f'<div class="row do"><span class="lb">⚡ Fastest way</span><ol>{"".join(f"<li>{s}</li>" for s in steps)}</ol>{extra}</div>'
            f'<div class="row chk"><span class="lb">✔ Check</span>{check}</div>'
            f'<div class="row trap"><span class="lb">⚠ Trap</span>{trap}</div></div>')


def page(title, sub, cards):
    moves = "".join(f"<li><b>{a}.</b> {b}</li>" for a, b in MOVES)
    return (f'<!doctype html><meta charset="utf-8"><title>{title}</title><style>{CSS}</style><h1>{title}</h1><p class="sub">{sub}</p>'
            f'<div class="moves"><h2>The 7 moves for all of Topic 1</h2><ol>{moves}</ol></div>{"".join(cards)}')


def review():
    items = RV.items()
    assert len(items) == len(REVIEW)
    out = []
    for n, (it, (spot, steps, chk, trap)) in enumerate(zip(items, REVIEW), 1):
        ans = it["ans"] or it["choices"][0]
        extra = RV.numline(-10, 2, -6, True, True) if n == 9 else ""
        out.append(card(n if n <= 11 else f"{n} (extra practice)", it["q"], ans, spot, steps, chk, trap, extra))
    return page("Topic 1 Review · How to Solve It", "Algebra I · Module 3 Topic 1: Linear Equations and Inequalities · "
                "Every review question, the fastest correct way, a check, and the trap to avoid.", out)


def test():
    assert len(TK.ITEMS) == len(TEST)
    out = [card(n, q, a, *TEST[n - 1], TK.numline() if n == 9 else "") for n, _, q, a, *_ in TK.ITEMS]
    return page("End of Topic 1 Test · How to Solve It", "Algebra I · Module 3 Topic 1 · Test review after the test: "
                "every question, the fastest correct way, a check, and the trap to avoid.", out)


def pdf(html, out, password=None):
    src = out.with_suffix(".html")
    src.write_text(html, encoding="utf-8")
    subprocess.run([EDGE, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={out}", src.as_uri()],
                   check=True, capture_output=True)
    src.unlink()
    if password:  # the browser asks for it before showing anything
        tmp = out.with_suffix(".tmp.pdf"); out.replace(tmp)
        with fitz.open(tmp) as d:
            d.save(out, encryption=fitz.PDF_ENCRYPT_AES_256, user_pw=password, owner_pw=password)
        tmp.unlink()
    print(out)


if __name__ == "__main__":
    # the math behind the review answers (test answers are asserted in make_m3t1_test_keys.py)
    assert 3 * (4 - -4) > -2 * -4 + 15 and not 3 * (4 - 0) > 15  # R3 t < -3
    assert abs(0.3 * (4 * 2 - 6) - (-1.8 * 2 + 4.2)) < 1e-9  # R4
    assert 2.5 * -7 - 3 < -1.5 * (-7 + 18) and 2.5 * -6 - 3 == -1.5 * (-6 + 18)  # R9 boundary -6
    assert 0.5 * 10 * (3 * 5 - 6) == 5 * (5 + 4) == 45  # R11
    assert 25 + 8 * 8 <= 90 < 25 + 8 * 9  # R15
    pdf(review(), ROOT / "Module 3 topic 1" / "REVIEW" / "T1-Review-How-To-Solve.pdf")
    pdf(test(), ROOT / "assessment" / "M3 TOPIC 1" / "M3T1-Test-How-To-Solve.pdf", sys.argv[1])

# Two answer keys for the M3T1 End of Topic Assessment (assessment/M3 TOPIC 1/…Student Edition M3T1.pdf, SE pp. 27-30, 11 items):
#   QUICK    = the efficient way: answer + shortest correct steps.
#   DETAILED = every step explained in kid-friendly words (an elementary student can follow it).
# Run: python make_m3t1_test_keys.py
import subprocess
from fractions import Fraction as F
from pathlib import Path

import make_t2_real_key as K

fr, EDGE = K.fr, K.RT.EDGE
DIR = Path(__file__).parent / "assessment" / "M3 TOPIC 1"


def numline():  # Q9: m < -4 -> open circle at -4, shade left
    W, x0, step = 420, 30, 36  # ticks -8..2
    X = lambda v: x0 + (v + 8) * step
    t = "".join(f'<line x1="{X(v)}" y1="22" x2="{X(v)}" y2="34" stroke="#000"/>'
                f'<text x="{X(v)}" y="50" font-size="12" text-anchor="middle">{str(v).replace("-", "−")}</text>' for v in range(-8, 3))
    return (f'<svg width="{W}" height="58"><line x1="8" y1="28" x2="{W - 8}" y2="28" stroke="#000"/>{t}'
            f'<line x1="{X(-4)}" y1="28" x2="10" y2="28" stroke="#c8102e" stroke-width="5"/>'
            f'<polygon points="4,28 16,21 16,35" fill="#c8102e"/>'
            f'<circle cx="{X(-4)}" cy="28" r="7" fill="#fff" stroke="#c8102e" stroke-width="3"/></svg>')


# (n, SE page, prompt, answer, quick steps, detailed steps)
ITEMS = [
    (1, 27, "Sofia: $50 from her aunt, saves $20 per week. Equation for amount y after x weeks?",
     "B.  y = 20x + 50",
     ["Rate (per week) = slope = 20; start amount = y-intercept = 50.", "y = 20x + 50 → <b>B</b>."],
     ["Sofia <b>starts</b> with $50. That money is there on day one, so it is the number that is added by itself: <b>+ 50</b>.",
      "Every week she adds $20. \"Per week\" means it gets multiplied by the number of weeks: <b>20 × x = 20x</b>.",
      "Put them together: money = 20x + 50, so <b>y = 20x + 50</b>.",
      "Check with a real week: after 2 weeks she has 50 + 20 + 20 = $90. The formula gives 20(2) + 50 = 90 ✓.",
      "Choice <b>A</b> swaps the numbers (she does not save $50 a week). <b>C</b> and <b>D</b> have a minus sign, but her money is going <b>up</b>, not down."]),
    (2, 27, "What value of p makes 8 − 6(p + 4) = 12 − 2(3p + 10) true?",
     "J.  No solution",
     ["Distribute: 8 − 6p − 24 = 12 − 6p − 20.", "Combine: −6p − 16 = −6p − 8.", "Add 6p: −16 = −8 (false) → <b>J</b>."],
     ["<b>Distribute</b> means multiply the number outside the parentheses by each thing inside. Left side: −6 × p = −6p and −6 × 4 = −24. So 8 − 6p − 24.",
      "Right side: −2 × 3p = −6p and −2 × 10 = −20. So 12 − 6p − 20.",
      "Put the plain numbers together on each side: 8 − 24 = −16 and 12 − 20 = −8. Now it says <b>−6p − 16 = −6p − 8</b>.",
      "Both sides have −6p. Add 6p to both sides and the p's disappear: <b>−16 = −8</b>.",
      "−16 is NOT equal to −8. That is a false statement, so no number for p can ever work. Answer: <b>No solution</b>.",
      "Tip: same p-part on both sides + different numbers = no solution."]),
    (3, 28, "Solution set for 4(2 − s) > −3s + 9?",
     "D.  s < −1",
     ["8 − 4s > −3s + 9", "Add 3s: 8 − s > 9 → −s > 1.", "Divide by −1, <b>flip</b>: s < −1 → <b>D</b>."],
     ["Distribute the 4: 4 × 2 = 8 and 4 × (−s) = −4s. Now: <b>8 − 4s > −3s + 9</b>.",
      "Get the s's on one side. Add 3s to both sides: −4s + 3s = −s. Now: <b>8 − s > 9</b>.",
      "Get the numbers on the other side. Subtract 8 from both sides: <b>−s > 1</b>.",
      "We want s, not −s, so divide both sides by −1. <b>Rule: when you multiply or divide by a negative number, flip the sign.</b> > becomes <.",
      "Answer: <b>s < −1</b>.",
      "Check with a number that should work, s = −2: 4(2 − (−2)) = 4(4) = 16, and −3(−2) + 9 = 6 + 9 = 15. Is 16 > 15? Yes ✓."]),
    (4, 28, "Solve 0.4(5x − 2) = −2.4x + 3.6",
     "x = 1",
     ["2x − 0.8 = −2.4x + 3.6", "Add 2.4x, add 0.8: 4.4x = 4.4", "x = 1"],
     ["Distribute 0.4: 0.4 × 5x = 2x (because 0.4 × 5 = 2) and 0.4 × 2 = 0.8. Now: <b>2x − 0.8 = −2.4x + 3.6</b>.",
      "Get all the x's on the left. Add 2.4x to both sides: 2x + 2.4x = 4.4x. Now: <b>4.4x − 0.8 = 3.6</b>.",
      "Get the numbers on the right. Add 0.8 to both sides: 3.6 + 0.8 = 4.4. Now: <b>4.4x = 4.4</b>.",
      "4.4 times what is 4.4? Divide both sides by 4.4: <b>x = 1</b>.",
      "Check: left 0.4(5 − 2) = 0.4(3) = 1.2; right −2.4 + 3.6 = 1.2. Same ✓."]),
    (5, 28, f"One solution, no solution, or infinite? {fr(1, 3)}(9x + 45) = 3(x + 3) + 6",
     "Infinitely many solutions",
     ["Left: 3x + 15.  Right: 3x + 9 + 6 = 3x + 15.", "Both sides identical (0 = 0) → <b>infinite</b>: every x works."],
     ["Left side: one-third of each part. 9x ÷ 3 = 3x and 45 ÷ 3 = 15. So the left side is <b>3x + 15</b>.",
      "Right side: 3 × x = 3x and 3 × 3 = 9, then + 6. So 3x + 9 + 6 = <b>3x + 15</b>.",
      "Now it says <b>3x + 15 = 3x + 15</b>. Both sides are exactly the same!",
      "If you subtract 3x and 15 from both sides you get 0 = 0, which is always true. So <b>any</b> number for x works.",
      "Answer: <b>infinite number of solutions</b>, because both sides simplify to the same expression, 3x + 15.",
      "Try it: x = 0 gives 15 = 15 ✓, x = 10 gives 45 = 45 ✓."]),
    (6, 28, "Chloe buys 3 eclairs at $2.25 each and x doughnuts at $2.80 each. Equation for total cost y?",
     "y = 2.80x + 6.75",
     ["Eclairs: 3 × 2.25 = 6.75 (fixed).", "Doughnuts: 2.80x (changes).", "y = 2.80x + 6.75  (also accept y = 6.75 + 2.8x or y = 3(2.25) + 2.80x)."],
     ["The eclairs are always 3, so their cost never changes: 3 × $2.25 = <b>$6.75</b>. (2.25 + 2.25 + 2.25 = 6.75.)",
      "We don't know how many doughnuts, so call it x. Each one is $2.80, so doughnuts cost <b>2.80 × x = 2.80x</b>.",
      "Total = doughnuts + eclairs: <b>y = 2.80x + 6.75</b>.",
      "Check: 2 doughnuts → 2.80(2) + 6.75 = 5.60 + 6.75 = $12.35 ✓."]),
    (7, 29, "Rewrite 5x + 3y = 9 in slope-intercept form.",
     f"y = −{fr(5, 3)}x + 3",
     ["Subtract 5x: 3y = −5x + 9.", f"Divide by 3: y = −{fr(5, 3)}x + 3."],
     ["<b>Slope-intercept form</b> means y is all by itself: y = mx + b.",
      "Move the 5x away from the y. Subtract 5x from both sides: <b>3y = −5x + 9</b>. (Write the x-part first.)",
      f"y is being multiplied by 3. Divide <b>everything</b> on both sides by 3: −5x ÷ 3 = −{fr(5, 3)}x and 9 ÷ 3 = 3.",
      f"Answer: <b>y = −{fr(5, 3)}x + 3</b>. Slope is −5/3, y-intercept is 3.",
      "Common mistake: dividing only the 9 by 3 and forgetting the −5x."]),
    (8, 29, "C = 2πr. Solve for r.",
     f"r = {fr('C', '2π')}",
     ["r is multiplied by 2π, so divide both sides by 2π.", f"r = {fr('C', '2π')}"],
     ["We want r by itself. Right now r is being <b>multiplied</b> by 2 and by π.",
      "To undo multiplying, we <b>divide</b>. Divide both sides by 2π.",
      f"On the right, 2πr ÷ 2π leaves just r. On the left we get C ÷ 2π.",
      f"Answer: <b>r = {fr('C', '2π')}</b>  (same as r = C ÷ (2π)).",
      "Like a number problem: if 10 = 2 × 5, then 5 = 10 ÷ 2."]),
    (9, 29, "Solve 1.5m − 2 < −2(m + 8) and graph on the number line.",
     "m < −4  (open circle at −4, shade left)",
     ["1.5m − 2 < −2m − 16", "Add 2m, add 2: 3.5m < −14", "m < −4 (divided by positive → no flip)", numline()],
     ["Distribute −2: −2 × m = −2m and −2 × 8 = −16. Now: <b>1.5m − 2 < −2m − 16</b>.",
      "Get the m's on the left. Add 2m to both sides: 1.5m + 2m = 3.5m. Now: <b>3.5m − 2 < −16</b>.",
      "Get numbers on the right. Add 2 to both sides: −16 + 2 = −14. Now: <b>3.5m < −14</b>.",
      "Divide both sides by 3.5: −14 ÷ 3.5 = −4. We divided by a <b>positive</b> number, so the sign stays the same: <b>m < −4</b>.",
      "Graph: <b>open</b> (empty) circle on −4, because −4 itself does not work (it's < , not ≤). Shade to the <b>left</b>, where the smaller numbers are." + numline(),
      "Check: m = −5 → 1.5(−5) − 2 = −9.5 and −2(−5 + 8) = −6. Is −9.5 < −6? Yes ✓."]),
    (10, 30, "Rewrite y − 5 = 2(x + 3) in slope-intercept form.",
     "y = 2x + 11",
     ["y − 5 = 2x + 6", "Add 5: y = 2x + 11"],
     ["Distribute the 2: 2 × x = 2x and 2 × 3 = 6. Now: <b>y − 5 = 2x + 6</b>.",
      "y has a −5 with it. Add 5 to both sides to get y alone: 6 + 5 = 11.",
      "Answer: <b>y = 2x + 11</b>. Slope 2, y-intercept 11.",
      "Check: x = 0 → original: y − 5 = 2(3) = 6, so y = 11 ✓."]),
    (11, 30, "Triangle: height (2n − 4) in, base 8 in. Rectangle: length 6 in, width (3 + n) in. Areas equal. Find n.",
     "n = 17",
     [f"Triangle: {fr(1, 2)}(8)(2n − 4) = 8n − 16.  Rectangle: 6(3 + n) = 18 + 6n.",
      "8n − 16 = 6n + 18 → 2n = 34 → n = 17.", "Check: both areas = 120 in²."],
     ["<b>Area of a triangle</b> = ½ × base × height. Half of 8 is 4, so the area is 4 × (2n − 4) = <b>8n − 16</b>.",
      "<b>Area of a rectangle</b> = length × width = 6 × (3 + n) = <b>18 + 6n</b>.",
      "The problem says the areas are equal, so set them equal: <b>8n − 16 = 6n + 18</b>.",
      "Subtract 6n from both sides: <b>2n − 16 = 18</b>. Add 16 to both sides: <b>2n = 34</b>.",
      "Divide by 2: <b>n = 17</b>.",
      "Check: triangle height 2(17) − 4 = 30, area ½ × 8 × 30 = 120. Rectangle width 3 + 17 = 20, area 6 × 20 = 120. Equal ✓."]),
]


def page(detailed):
    kind = "DETAILED (step-by-step, easy words)" if detailed else "QUICK (efficient method)"
    h = (f"<header><h1>M3 Topic 1 End of Topic Assessment · ANSWER KEY · {kind}</h1>"
         "<p class='sub'>Algebra I · Module 3, Topic 1: Linear Equations and Inequalities · SE pp. 27–30 · 11 questions</p></header>"
         "<h3>Quick key</h3><table class='k'><tr><th>#</th><th>SE p.</th><th>Answer</th></tr>"
         + "".join(f"<tr><td>{n}</td><td>{p}</td><td class='a'>{a}</td></tr>" for n, p, _, a, *_ in ITEMS) + "</table>")
    if detailed:
        h += ("<div class='acc'><b>Big ideas used on this test</b><br>"
              "• Do the same thing to <b>both sides</b> to keep it balanced.<br>"
              "• <b>Distribute</b>: multiply the outside number by everything inside the ( ).<br>"
              "• Inequalities: multiply/divide by a <b>negative</b> → <b>flip</b> the sign.<br>"
              "• Same x-part, different numbers → <b>no solution</b>. Both sides identical → <b>infinite</b>.<br>"
              "• Slope-intercept form: <b>y = mx + b</b> (m = rate/slope, b = starting value).</div>")
    for n, p, prompt, ans, quick, det in ITEMS:
        steps = "".join(f"<li>{s}</li>" for s in (det if detailed else quick))
        h += (f"<div class='item'><h2><span>Question {n}</span><span class='tag'>SE p. {p}</span></h2>"
              f"<p class='prompt'>{prompt}</p><div class='big'>{ans}</div><ol>{steps}</ol></div>")
    return h


if __name__ == "__main__":
    # self-check the math behind every answer
    assert -16 != -8  # Q2 no solution
    s = -2; assert 4 * (2 - s) > -3 * s + 9 and not (4 * (2 - 0) > 9)  # Q3
    assert abs(0.4 * (5 * 1 - 2) - (-2.4 * 1 + 3.6)) < 1e-9  # Q4
    assert all(F(1, 3) * (9 * x + 45) == 3 * (x + 3) + 6 for x in range(-5, 6))  # Q5
    assert all(5 * x + 3 * (F(-5, 3) * x + 3) == 9 for x in range(-5, 6))  # Q7
    assert 1.5 * -4 - 2 == -2 * (-4 + 8) and 1.5 * -5 - 2 < -2 * (-5 + 8) and not (1.5 * -3 - 2 < -2 * (-3 + 8))  # Q9 boundary
    assert all(2 * (x + 3) + 5 == 2 * x + 11 for x in range(-5, 6))  # Q10
    assert F(1, 2) * 8 * (2 * 17 - 4) == 6 * (3 + 17) == 120  # Q11
    for detailed, tag in ((False, "QUICK"), (True, "DETAILED")):
        out = DIR / f"M3T1-End-of-Topic-ANSWER-KEY-{tag}"
        src = out.with_suffix(".html")
        src.write_text(f"<!doctype html><meta charset='utf-8'><title>{out.name}</title><style>{K.CSS}</style>{page(detailed)}", encoding="utf-8")
        pdf = out.with_suffix(".pdf")
        subprocess.run([EDGE, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={pdf}", src.as_uri()],
                       check=True, capture_output=True)
        src.unlink()
        print(pdf)

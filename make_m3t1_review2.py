"""M3T1 Review Set 2: weekend practice for Wayground (all multiple choice, plain-text math so it types straight in).
New numbers and contexts, skill-based, not test twins.  Run: python make_m3t1_review2.py <password>"""
import sys
from pathlib import Path
import make_m3t1_walkthroughs as W

OUT = Path(__file__).parent / "Module 3 topic 1" / "REVIEW"

# (skill, question, [correct, wrong, wrong, wrong], why) – correct is listed first, moved by POS below
Q = [
    ("Write an equation", "Carlos has $25 in savings and adds $18 each week. Which equation gives the amount, y, he has after x weeks?",
     ["y = 18x + 25", "y = 25x + 18", "y = 18x − 25", "y = 43x"], "$18 per week is the rate (times x); the $25 he starts with is the constant."),
    ("Write an equation", "A phone card starts with $50. Each call costs $2.50. Which equation gives the money left, y, after x calls?",
     ["y = −2.5x + 50", "y = 2.5x + 50", "y = 50x − 2.5", "y = −50x + 2.5"], "The money goes down $2.50 per call, so the slope is negative. It starts at $50."),
    ("Write an equation", "Ana buys 3 adult tickets at $9.50 each and some student tickets at $6.25 each. Which equation gives the total cost, y, for x student tickets?",
     ["y = 6.25x + 28.50", "y = 9.50x + 6.25", "y = 28.50x + 6.25", "y = 15.75x"], "Adult tickets are fixed: 3 × 9.50 = 28.50. Student tickets change: 6.25x."),
    ("Solve", "Solve: 4(x − 3) = 2x + 6",
     ["x = 9", "x = 3", "x = −3", "x = 1.5"], "4x − 12 = 2x + 6 → 2x = 18 → x = 9. Check: 4(6) = 24 and 18 + 6 = 24."),
    ("Solve", "Solve: 0.5(6x + 8) = 2x − 1",
     ["x = −5", "x = 5", "x = −3", "x = 3"], "3x + 4 = 2x − 1 → x = −5. Check: 0.5(−22) = −11 and −10 − 1 = −11."),
    ("Solve", "What value of x makes 7 − 3(x − 2) = 2x − 2 true?",
     ["x = 3", "x = −3", "x = 1", "x = 5"], "7 − 3x + 6 = 2x − 2 → 13 − 3x = 2x − 2 → 15 = 5x → x = 3."),
    ("How many solutions", "How many solutions does 2(3x + 4) = 6x + 8 have?",
     ["Infinitely many", "No solution", "One solution, x = 0", "One solution, x = 8"], "Left side: 6x + 8. Both sides are the same, so every x works."),
    ("How many solutions", "Which equation has NO solution?",
     ["5(x + 1) = 5x − 2", "5(x + 1) = 5x + 5", "5(x + 1) = 4x − 2", "5x + 1 = 4x + 1"], "5x + 5 = 5x − 2: same x-term, different numbers, so it is never true."),
    ("Inequality", "Solve: −3x + 5 > 17",
     ["x < −4", "x > −4", "x < 4", "x > 4"], "−3x > 12 → divide by −3 and FLIP: x < −4."),
    ("Inequality", "Solve: 2(5 − x) ≤ x − 8",
     ["x ≥ 6", "x ≤ 6", "x ≥ −6", "x ≤ −6"], "10 − 2x ≤ x − 8 → 18 ≤ 3x → 6 ≤ x, so x ≥ 6."),
    ("Graph an inequality", "Which describes the graph of n > −2?",
     ["Open circle at −2, shade right", "Closed circle at −2, shade right", "Open circle at −2, shade left", "Closed circle at −2, shade left"],
     "> does not include −2 → open circle. Greater than → shade right."),
    ("Graph an inequality", "Which describes the graph of x ≤ 4?",
     ["Closed circle at 4, shade left", "Open circle at 4, shade left", "Closed circle at 4, shade right", "Open circle at 4, shade right"],
     "≤ includes 4 → closed circle. Less than → shade left."),
    ("Write an inequality", "A club already has $60 and earns $40 per car wash, w. They need at least $500. Which inequality fits?",
     ["40w + 60 ≥ 500", "40w + 60 ≤ 500", "60w + 40 ≥ 500", "40w + 60 > 500"], "“At least” means ≥. $40 per car wash times w, plus the $60 they have."),
    ("Write an inequality", "Using 40w + 60 ≥ 500, how many car washes does the club need?",
     ["At least 11", "At most 11", "At least 12", "At least 14"], "40w ≥ 440 → w ≥ 11."),
    ("Slope-intercept form", "Rewrite in slope-intercept form: 3x + 4y = 12",
     ["y = −3/4 x + 3", "y = 3/4 x + 3", "y = −3x + 12", "y = −4/3 x + 4"], "4y = −3x + 12 → divide EVERY term by 4: y = −3/4 x + 3."),
    ("Slope-intercept form", "Rewrite in slope-intercept form: 6x − 2y = 10",
     ["y = 3x − 5", "y = −3x + 5", "y = 3x + 5", "y = 6x − 10"], "−2y = −6x + 10 → divide every term by −2: y = 3x − 5."),
    ("Slope-intercept form", "Rewrite in slope-intercept form: y + 2 = 4(x − 1)",
     ["y = 4x − 6", "y = 4x − 2", "y = 4x + 2", "y = 4x − 3"], "y + 2 = 4x − 4 → subtract 2: y = 4x − 6."),
    ("Literal equation", "Solve y = mx + b for x.",
     ["x = (y − b)/m", "x = y/m − b", "x = (y + b)/m", "x = m(y − b)"], "Subtract b first: y − b = mx. Then divide by m."),
    ("Literal equation", "Solve 3x + 2y = z for y.",
     ["y = (z − 3x)/2", "y = z/2 − 3x", "y = (z + 3x)/2", "y = 2(z − 3x)"], "Subtract 3x: 2y = z − 3x. Divide ALL of it by 2."),
    ("Geometry", "A square has sides of (x + 2) cm. A rectangle is (x + 6) cm long and 2 cm wide. Their perimeters are equal. What is x?",
     ["x = 4", "x = 2", "x = 8", "x = 6"], "4(x + 2) = 2(x + 6) + 2(2) → 4x + 8 = 2x + 16 → x = 4. Both perimeters are 24 cm."),
]
POS = [1, 3, 0, 2, 2, 0, 3, 1, 0, 2, 1, 3, 0, 1, 2, 3, 3, 0, 1, 2]  # where the correct choice lands (A=0)


def placed(choices, pos):
    c = choices[1:]
    c.insert(pos, choices[0])
    return c


def check():
    assert len(Q) == len(POS) == 20
    for (_, _, ch, _), p in zip(Q, POS):
        assert len(set(ch)) == 4 and placed(ch, p)[p] == ch[0]
    # spot-check the math
    x = 9; assert 4 * (x - 3) == 2 * x + 6
    x = -5; assert 0.5 * (6 * x + 8) == 2 * x - 1
    x = 3; assert 7 - 3 * (x - 2) == 2 * x - 2
    x = 4; assert 4 * (x + 2) == 2 * (x + 6) + 4
    assert 40 * 11 + 60 >= 500 > 40 * 10 + 60


CSS = W.CSS + """.qq{break-inside:avoid;border:1px solid #bcc8d6;border-radius:8px;padding:6px 12px;margin:8px 0}
.qq h3{margin:0 0 3px;font-size:11.5pt;color:#1d3557}.qq .sk{font-weight:400;color:#777;font-size:9.5pt}
.qq ol{list-style:upper-alpha;margin:3px 0 0 20px;padding:0;font-family:Cambria,serif;font-size:12pt}.qq li{margin:2px 0}
.qq li.ok{color:#c8102e;font-weight:700}.why{color:#c8102e;margin:3px 0 0;font-size:10pt}"""


def build(key):
    out = []
    for n, ((sk, q, ch, why), p) in enumerate(zip(Q, POS), 1):
        lis = "".join(f'<li class="{"ok" if key and i == p else ""}">{c}{" ✔" if key and i == p else ""}</li>'
                      for i, c in enumerate(placed(ch, p)))
        out.append(f'<div class="qq"><h3>{n}. {q} <span class="sk">· {sk}</span></h3><ol>{lis}</ol>'
                   + (f'<p class="why">Answer {"ABCD"[p]}: {why}</p>' if key else "") + "</div>")
    title = "Topic 1 Review Set 2" + (" · Answer Key" if key else "")
    quick = (f'<div class="moves"><b>Quick key:</b> ' + " · ".join(f"{n} {'ABCD'[p]}" for n, p in enumerate(POS, 1)) + "</div>") if key else ""
    return (f'<!doctype html><meta charset="utf-8"><title>{title}</title><style>{CSS}</style><h1>{title}</h1>'
            '<p class="sub">Module 3 Topic 1 · weekend practice on Wayground · 20 multiple choice</p>' + quick + "".join(out))


if __name__ == "__main__":
    check()
    W.pdf(build(False), OUT / "T1-Review-2-Wayground.pdf")
    W.pdf(build(True), OUT / "T1-Review-2-Wayground-ANSWER-KEY.pdf", sys.argv[1])

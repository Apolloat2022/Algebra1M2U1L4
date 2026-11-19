"""Gap practice: 20 skill items built from the EDIA skills-gap report (one item per reported skill, same order, new numbers).
1-10 one-step equations (natural, integer, decimal, fraction) · 11-15 standard form → slope-intercept · 16-20 point-slope → slope-intercept.
Online practice with instant feedback (general / 504 / IEP) + printed worksheet and keys in Module 3 topic 1/GAP PRACTICE.
Run:  python make_m3t1_gap_practice.py   then lock the keys with lock_keys.py before committing."""
from fractions import Fraction as F
import make_m3t1_lessons as L
import make_m3t1_bell_1119 as B

bq = L.bq
UNDO = "undo it with the opposite operation on both sides"
SI = "get [[y]] alone: move the [[x]]-term, then divide every term by the number with [[y]]"
PS = "distribute, then add or subtract to get [[y]] alone"
GAP = [
 # 1-10 one-step equations
 bq("Solve [[x + 14 = 31]].", ["[[17]]", "[[45]]", "[[27]]", "[[13]]"],
    "Subtract 14 from both sides: [[x = 31 − 14 = 17]]. 45 adds instead of subtracting.", UNDO, ["Subtract 14: [[x = 31 − 14]].", "[[x = 17]]."]),
 bq("Solve [[x + 9 = −4]].", ["[[−13]]", "[[5]]", "[[13]]", "[[−5]]"],
    "Subtract 9 from both sides: [[x = −4 − 9 = −13]]. 5 adds 9 instead of subtracting.", UNDO, ["Subtract 9: [[x = −4 − 9]].", "[[x = −13]]."]),
 bq("Solve [[2.5x = 10]].", ["[[4]]", "[[25]]", "[[7.5]]", "[[12.5]]"],
    "Divide both sides by 2.5: [[x = 10 ÷ 2.5 = 4]]. 25 multiplies instead of dividing.", UNDO, ["Divide by 2.5: [[x = 10 ÷ 2.5]].", "[[x = 4]]."]),
 bq("Solve [[x/6 = 7]].", ["[[42]]", "[[13]]", "[[1]]", "[[36]]"],
    "Multiply both sides by 6: [[x = 7 · 6 = 42]]. 13 adds 6 instead of multiplying.", UNDO, ["Multiply by 6: [[x = 7 · 6]].", "[[x = 42]]."]),
 bq("Solve [[x + 3.6 = 9.2]].", ["[[5.6]]", "[[12.8]]", "[[6.6]]", "[[5.4]]"],
    "Subtract 3.6: [[x = 9.2 − 3.6 = 5.6]]. Line up the decimal points.", UNDO, ["Subtract 3.6: [[x = 9.2 − 3.6]].", "[[x = 5.6]]."]),
 bq("Solve [[x − 4.75 = 2.5]].", ["[[7.25]]", "[[2.25]]", "[[−2.25]]", "[[4.8]]"],
    "Add 4.75 to both sides: [[x = 2.5 + 4.75 = 7.25]]. 2.25 subtracts instead of adding.", UNDO, ["Add 4.75: [[x = 2.5 + 4.75]].", "[[x = 7.25]]."]),
 bq("Solve [[0.4x = 6]].", ["[[15]]", "[[2.4]]", "[[1.5]]", "[[5.6]]"],
    "Divide both sides by 0.4: [[x = 6 ÷ 0.4 = 15]]. 2.4 multiplies instead of dividing.", UNDO, ["Divide by 0.4: [[x = 6 ÷ 0.4]].", "[[x = 15]]."]),
 bq("Solve [[x + 1/4 = 5/6]].", ["[[7/12]]", "[[13/12]]", "[[2]]", "[[1/12]]"],
    "Subtract [[1/4]]. Common denominator 12: [[10/12 − 3/12 = 7/12]]. 2 subtracts tops and bottoms separately.",
    "subtract; use a common denominator", ["Subtract [[1/4]]: [[x = 5/6 − 1/4]].", "Common denominator 12: [[10/12 − 3/12]].", "[[x = 7/12]]."]),
 bq("Solve [[x + 0.85 = 3.1]].", ["[[2.25]]", "[[3.95]]", "[[2.35]]", "[[2.75]]"],
    "Subtract 0.85: [[x = 3.10 − 0.85 = 2.25]]. Write 3.1 as 3.10 to line up the places.", UNDO, ["Write 3.1 as 3.10.", "Subtract 0.85: [[x = 3.10 − 0.85]].", "[[x = 2.25]]."]),
 bq("Solve [[x + 38 = 95]].", ["[[57]]", "[[133]]", "[[67]]", "[[47]]"],
    "Subtract 38: [[x = 95 − 38 = 57]].", UNDO, ["Subtract 38: [[x = 95 − 38]].", "[[x = 57]]."]),
 # 11-15 standard form → slope-intercept
 bq("Write [[6x + 3y = 12]] in slope-intercept form.", ["[[y = −2x + 4]]", "[[y = 2x + 4]]", "[[y = −6x + 12]]", "[[y = −2x + 12]]"],
    "Subtract [[6x]]: [[3y = −6x + 12]]. Divide every term by 3: [[y = −2x + 4]].", SI,
    ["Subtract [[6x]]: [[3y = −6x + 12]].", "Divide every term by 3: [[y = −2x + 4]]."]),
 bq("Write [[5x + 2y = 8]] in slope-intercept form.", ["[[y = −(5/2)x + 4]]", "[[y = (5/2)x + 4]]", "[[y = −5x + 4]]", "[[y = −(5/2)x + 8]]"],
    "Subtract [[5x]]: [[2y = −5x + 8]]. Divide every term by 2: [[y = −(5/2)x + 4]].", SI,
    ["Subtract [[5x]]: [[2y = −5x + 8]].", "Divide every term by 2: [[y = −(5/2)x + 4]]."]),
 bq("Write [[2x − 3y = 7]] in slope-intercept form.", ["[[y = (2/3)x − 7/3]]", "[[y = −(2/3)x + 7/3]]", "[[y = (2/3)x + 7/3]]", "[[y = 2x − 7]]"],
    "Subtract [[2x]]: [[−3y = −2x + 7]]. Divide every term by [[−3]]: [[y = (2/3)x − 7/3]].", SI,
    ["Subtract [[2x]]: [[−3y = −2x + 7]].", "Divide every term by [[−3]] (signs change).", "[[y = (2/3)x − 7/3]]."]),
 bq("Write [[(1/2)x + (1/3)y = 2]] in slope-intercept form.", ["[[y = −(3/2)x + 6]]", "[[y = −(1/6)x + 2/3]]", "[[y = (3/2)x + 6]]", "[[y = −(3/2)x + 2]]"],
    "Subtract [[(1/2)x]]: [[(1/3)y = −(1/2)x + 2]]. Multiply every term by 3: [[y = −(3/2)x + 6]].",
    "dividing by [[1/3]] = multiplying by 3", ["Subtract [[(1/2)x]]: [[(1/3)y = −(1/2)x + 2]].", "Multiply every term by 3: [[y = −(3/2)x + 6]]."]),
 bq("Write [[4x + 2y = −10]] in slope-intercept form.", ["[[y = −2x − 5]]", "[[y = 2x − 5]]", "[[y = −2x + 5]]", "[[y = −4x − 10]]"],
    "Subtract [[4x]]: [[2y = −4x − 10]]. Divide every term by 2: [[y = −2x − 5]].", SI,
    ["Subtract [[4x]]: [[2y = −4x − 10]].", "Divide every term by 2: [[y = −2x − 5]]."]),
 # 16-20 point-slope → slope-intercept
 bq("Write [[y − 3 = 2(x + 1)]] in slope-intercept form.", ["[[y = 2x + 5]]", "[[y = 2x + 4]]", "[[y = 2x − 1]]", "[[y = 2x + 1]]"],
    "Distribute: [[y − 3 = 2x + 2]]. Add 3: [[y = 2x + 5]]. 2x + 4 forgets to multiply the 1.", PS,
    ["Distribute: [[y − 3 = 2x + 2]].", "Add 3: [[y = 2x + 5]]."]),
 bq("Write [[y + 4 = −3(x − 2)]] in slope-intercept form.", ["[[y = −3x + 2]]", "[[y = −3x + 10]]", "[[y = −3x − 10]]", "[[y = −3x − 2]]"],
    "Distribute: [[y + 4 = −3x + 6]]. Subtract 4: [[y = −3x + 2]]. 10 adds the 4 instead of subtracting.", PS,
    ["Distribute: [[−3 · −2 = +6]], so [[y + 4 = −3x + 6]].", "Subtract 4: [[y = −3x + 2]]."]),
 bq("Write [[y − 7 = 4(x − 2)]] in slope-intercept form.", ["[[y = 4x − 1]]", "[[y = 4x − 15]]", "[[y = 4x + 5]]", "[[y = 4x + 1]]"],
    "Distribute: [[y − 7 = 4x − 8]]. Add 7: [[y = 4x − 1]]. 4x + 5 forgets to multiply the 2.", PS,
    ["Distribute: [[y − 7 = 4x − 8]].", "Add 7: [[y = 4x − 1]]."]),
 bq("Write [[y − 2 = (1/2)(x − 6)]] in slope-intercept form.", ["[[y = (1/2)x − 1]]", "[[y = (1/2)x − 4]]", "[[y = (1/2)x − 5]]", "[[y = (1/2)x + 1]]"],
    "Distribute: [[(1/2)(−6) = −3]], so [[y − 2 = (1/2)x − 3]]. Add 2: [[y = (1/2)x − 1]].", PS,
    ["Distribute: [[y − 2 = (1/2)x − 3]].", "Add 2: [[y = (1/2)x − 1]]."]),
 bq("Write [[y + 1 = −(2/3)(x + 9)]] in slope-intercept form.", ["[[y = −(2/3)x − 7]]", "[[y = −(2/3)x − 5]]", "[[y = −(2/3)x − 10]]", "[[y = (2/3)x − 7]]"],
    "Distribute: [[−(2/3)(9) = −6]], so [[y + 1 = −(2/3)x − 6]]. Subtract 1: [[y = −(2/3)x − 7]].", PS,
    ["Distribute: [[y + 1 = −(2/3)x − 6]].", "Subtract 1: [[y = −(2/3)x − 7]]."]),
]


def check():
    """The correct choice really solves each item (one-step: plug in; forms: test two x-values)."""
    x = [F(17), F(-13), F(4), F(42), F("5.6"), F("7.25"), F(15), F(7, 12), F("2.25"), F(57)]
    eq = [lambda v: v + 14 == 31, lambda v: v + 9 == -4, lambda v: F("2.5") * v == 10, lambda v: v / 6 == 7,
          lambda v: v + F("3.6") == F("9.2"), lambda v: v - F("4.75") == F("2.5"), lambda v: F("0.4") * v == 6,
          lambda v: v + F(1, 4) == F(5, 6), lambda v: v + F("0.85") == F("3.1"), lambda v: v + 38 == 95]
    assert all(f(v) for f, v in zip(eq, x))
    lines = [  # (m, b) of the answer, original relation
        (F(-2), F(4), lambda a, y: 6 * a + 3 * y == 12), (F(-5, 2), F(4), lambda a, y: 5 * a + 2 * y == 8),
        (F(2, 3), F(-7, 3), lambda a, y: 2 * a - 3 * y == 7), (F(-3, 2), F(6), lambda a, y: a / 2 + y / 3 == 2),
        (F(-2), F(-5), lambda a, y: 4 * a + 2 * y == -10), (F(2), F(5), lambda a, y: y - 3 == 2 * (a + 1)),
        (F(-3), F(2), lambda a, y: y + 4 == -3 * (a - 2)), (F(4), F(-1), lambda a, y: y - 7 == 4 * (a - 2)),
        (F(1, 2), F(-1), lambda a, y: y - 2 == F(1, 2) * (a - 6)), (F(-2, 3), F(-7), lambda a, y: y + 1 == F(-2, 3) * (a + 9))]
    assert all(rel(a, m * a + b) for m, b, rel in lines for a in (F(0), F(3)))
    assert len(GAP) == 20 and all(len(set(q["choices"])) == 4 for q in GAP)


if __name__ == "__main__":
    check()
    tag = "1–2"
    L.ACC[tag] = {"ref": [L.ACC[1]["ref"][1], L.ACC[1]["ref"][2], L.ACC[2]["ref"][0], L.ACC[2]["ref"][1]]}
    B.exit_pages(tag, GAP, "m3t1-gap-practice.html", "Skills Gap Practice", "Module 3 · Topic 1 · Skills Gap Practice",
                 "Skills Gap Practice: One-Step Equations and Slope-Intercept Form",
                 "Work each question on paper first, then pick your answer. You see right away if it is correct and how to solve it.", "homework")
    items = [dict(num=k, q=q["q"], choices=L.print_order(q["choices"], (k + 1) % 4), letters="FGHJ" if k % 2 == 0 else "ABCD",
                  answer=q["choices"][0], why=q["why"], tip=q["formula"], frames=None) for k, q in enumerate(GAP, 1)]
    for kind in (None, "504", "IEP"):
        for key in (False, True):
            name = f"T1-Gap-Practice{f'-{kind}' if kind else ''}{'-ANSWER-KEY' if key else ''}"
            L.sheet(name, "GAP PRACTICE", tag, items, key, kind)
            print(name)

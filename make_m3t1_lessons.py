"""Module 3 Topic 1, Lessons 1-3: slide decks, narrated videos, bell work and exit tickets for every class day, plus the
IEP and Section 504 versions of each (decks, online bell work, printable sheets with keys).
Bell work and exit tickets are written like the End of Topic 1 Assessment
(materials/Secondary Mathematics Algebra Module 3 Topic 1 Assements Student Edition.pdf):
  Lesson 1 -> test Q2, Q4, Q5, Q11 · Lesson 2 -> Q7, Q8, Q10 · Lesson 3 -> Q1, Q3, Q6, Q9.
Stars (essential activities) come from the 150-day pacing guide, Module 3 Topic 1 p. 3.
Run:  python make_m3t1_lessons.py [video]      (builds everything, the .pptx copies too; videos only with "video")"""
import json, os, re, subprocess, sys, tempfile
from pathlib import Path

import make_t2_decks as D
import make_t2_practice as MP
import make_accom_lessons as A

ROOT = Path(__file__).parent
OUT = ROOT / "Module 3 topic 1"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
M, mt, eq, ans, st, p, sec, row, card, table, L, graph = D.M, D.mt, D.eq, D.ans, D.st, D.p, D.sec, D.row, D.card, D.table, D.L, D.graph
mq = D.mq
FOLDER = {"504": ROOT / "Section 504", "IEP": ROOT / "IEP"}
LABEL = {"504": "Section 504", "IEP": "IEP"}


# ================================================================ item builders
def bq(q, choices, why, formula, steps):
    """Bell work question. First choice is correct. formula + steps feed the IEP version."""
    return {"q": q, "choices": choices, "why": why, "formula": formula, "steps": steps}


def mc(q, choices, work, tip, short=None):
    return {"kind": "mc", "q": q, "choices": choices, "answer": choices[0], "work": work, "tip": tip, "short": short or q}


def op(q, answer, work, tip, frames, short=None):
    """Open item. frames: IEP fill-in steps ('Distribute: ______')."""
    return {"kind": "open", "q": q, "answer": answer, "work": work, "tip": tip, "frames": frames, "short": short or q}


# ================================================================ Lesson data
DATES = {(1, 1): "Thu-11-05", (2, 1): "Mon-11-09", (2, 2): "Tue-11-10", (3, 1): "Wed-11-11", (3, 2): "Thu-11-12", (3, 3): "Mon-11-16"}

BELL = {
 (1, 1): [
  bq("Marcus has $35 and saves $15 per week. Which equation gives the amount he has saved, [[y]], after [[x]] weeks?",
     ["[[y = 15x + 35]]", "[[y = 35x + 15]]", "[[y = −15x + 35]]", "[[y = 50x]]"],
     "Start at $35 ([[b]]) and add $15 each week ([[m]]): [[y = 15x + 35]]. Like test Q1.",
     "[[y = mx + b]]: [[m]] = rate, [[b]] = start", ["The start is $35, so [[b = 35]].", "The rate is $15 per week, so [[m = 15]].", "[[y = 15x + 35]]."]),
  bq("What value of [[x]] makes [[3(x − 2) = 12]] true?", ["[[6]]", "[[4⅔]]", "[[2]]", "[[10]]"],
     "Distribute: [[3x − 6 = 12]], so [[3x = 18]] and [[x = 6]]. 4⅔ forgets to multiply the 2.",
     "distribute, then undo + and ×", ["Distribute: [[3x − 6 = 12]].", "Add 6: [[3x = 18]].", "Divide by 3: [[x = 6]]."]),
  bq("Is [[x = 2]] a solution of [[5x − 1 = 9]]?", ["Yes, because [[9 = 9]]", "No, because [[10 ≠ 9]]", "Yes, because [[x = 9]]", "No, because [[11 ≠ 9]]"],
     "Substitute: [[5(2) − 1 = 10 − 1 = 9]]. A true statement means 2 is a solution.",
     "put the number in for [[x]]", ["[[5(2) − 1]].", "[[10 − 1 = 9]].", "[[9 = 9]] is true, so yes."]),
  bq("Which expression is equivalent to [[4(x + 2) − x]]?", ["[[3x + 8]]", "[[3x + 2]]", "[[5x + 8]]", "[[4x + 6]]"],
     "Distribute: [[4x + 8 − x = 3x + 8]].", "distribute, then combine like terms", ["Distribute: [[4x + 8 − x]].", "Combine [[4x − x = 3x]]: [[3x + 8]]."])],
 (2, 1): [
  bq("What value of [[x]] makes [[2(x + 3) = x − 4]] true?", ["[[−10]]", "[[−7]]", "[[2]]", "No solution"],
     "[[2x + 6 = x − 4]], so [[x = −10]].", "distribute, then get [[x]] on one side",
     ["Distribute: [[2x + 6 = x − 4]].", "Subtract [[x]]: [[x + 6 = −4]].", "Subtract 6: [[x = −10]]."]),
  bq("How many solutions does [[3x + 1 = 3x − 5]] have?", ["No solution", "One solution, [[x = 0]]", "Infinite solutions", "One solution, [[x = −2]]"],
     "Same [[x]]-term, different constants: [[1 ≠ −5]], never true.", "same [[x]]-term + different numbers → no solution",
     ["Both sides have [[3x]].", "The numbers are different: [[1]] and [[−5]].", "[[1 = −5]] is never true: no solution."]),
  bq("What are the slope and [[y]]-intercept of [[y = −2x + 7]]?", ["slope [[−2]], [[(0, 7)]]", "slope [[7]], [[(0, −2)]]", "slope [[2]], [[(0, 7)]]", "slope [[−2]], [[(7, 0)]]"],
     "In [[y = mx + b]], [[m = −2]] and [[b = 7]].", "[[y = mx + b]]: slope [[m]], [[y]]-intercept [[(0, b)]]",
     ["Match to [[y = mx + b]].", "[[m = −2]]: slope [[−2]].", "[[b = 7]]: [[(0, 7)]]."]),
  bq("What is the [[x]]-intercept of [[y = 2x − 6]]?", ["[[(3, 0)]]", "[[(−6, 0)]]", "[[(0, −6)]]", "[[(−3, 0)]]"],
     "Set [[y = 0]]: [[0 = 2x − 6]], [[x = 3]].", "[[x]]-intercept: put 0 in for [[y]]",
     ["[[0 = 2x − 6]].", "Add 6: [[6 = 2x]].", "Divide by 2: [[x = 3]], so [[(3, 0)]]."])],
 (2, 2): [
  bq("Which equation is [[4x + 2y = 10]] written in slope-intercept form?", ["[[y = −2x + 5]]", "[[y = 2x + 5]]", "[[y = −4x + 10]]", "[[y = −2x + 10]]"],
     "Subtract [[4x]]: [[2y = −4x + 10]]. Divide by 2: [[y = −2x + 5]].", "get [[y]] alone: subtract, then divide every term",
     ["Subtract [[4x]]: [[2y = −4x + 10]].", "Divide every term by 2.", "[[y = −2x + 5]]."]),
  bq("What value of [[x]] makes [[3x − 7 = 11]] true?", ["[[6]]", "[[4/3]]", "[[18]]", "[[3]]"],
     "Add 7: [[3x = 18]]. Divide by 3: [[x = 6]].", "undo − with +, undo × with ÷", ["Add 7: [[3x = 18]].", "Divide by 3: [[x = 6]]."]),
  bq("[[P = 2ℓ + 2w]]. What is [[ℓ]] when [[P = 30]] and [[w = 5]]?", ["[[10]]", "[[20]]", "[[12.5]]", "[[15]]"],
     "[[30 = 2ℓ + 10]], so [[2ℓ = 20]] and [[ℓ = 10]].", "put in the numbers you know, then solve",
     ["[[30 = 2ℓ + 2(5)]].", "[[30 = 2ℓ + 10]], subtract 10: [[2ℓ = 20]].", "Divide by 2: [[ℓ = 10]]."]),
  bq("[[C = 5/9(F − 32)]]. What is [[C]] when [[F = 50]]?", ["[[10]]", "[[18]]", "[[50]]", "[[−10]]"],
     "[[50 − 32 = 18]], and [[5/9 · 18 = 10]].", "parentheses first, then multiply",
     ["Parentheses: [[50 − 32 = 18]].", "Multiply: [[5/9 · 18 = 10]]."])],
 (3, 1): [
  bq("Elijah starts with a $25 credit and earns $3.75 for each box he sells. Which equation gives his total sales, [[y]], after selling [[x]] boxes?",
     ["[[y = 3.75x + 25]]", "[[y = 25x + 3.75]]", "[[y = −3.75x + 25]]", "[[y = 28.75x]]"],
     "Start $25 ([[b]]), $3.75 per box ([[m]]). Like test Q1.", "[[y = mx + b]]: [[m]] = rate, [[b]] = start",
     ["Start: [[b = 25]].", "Rate: [[m = 3.75]].", "[[y = 3.75x + 25]]."]),
  bq("Which symbol means \"at least\"?", ["[[≥]]", "[[≤]]", "[[>]]", "[[<]]"], "At least 5 means 5 or more: [[≥]].",
     "at least = this much or more", ["\"At least 5\" allows 5.", "It also allows more than 5.", "Greater than or equal: [[≥]]."]),
  bq("Which symbol means \"no more than\"?", ["[[≤]]", "[[≥]]", "[[<]]", "[[>]]"], "No more than 5 means 5 or less: [[≤]].",
     "no more than = this much or less", ["\"No more than 5\" allows 5.", "It also allows less than 5.", "Less than or equal: [[≤]]."]),
  bq("What value of [[b]] makes [[3.75b + 25 = 400]] true?", ["[[100]]", "[[106.67]]", "[[113.33]]", "[[375]]"],
     "Subtract 25: [[3.75b = 375]]. Divide: [[b = 100]].", "subtract the start, then divide by the rate",
     ["Subtract 25: [[3.75b = 375]].", "Divide by 3.75: [[b = 100]]."])],
 (3, 2): [
  bq("What value of [[x]] makes [[2x + 5 = 17]] true?", ["[[6]]", "[[11]]", "[[8.5]]", "[[12]]"], "Subtract 5: [[2x = 12]]. Divide: [[x = 6]].",
     "undo + with −, undo × with ÷", ["Subtract 5: [[2x = 12]].", "Divide by 2: [[x = 6]]."]),
  bq("Which describes the graph of [[x ≥ 2]] on a number line?", ["closed circle at 2, shaded right", "open circle at 2, shaded right",
                                                                   "closed circle at 2, shaded left", "open circle at 2, shaded left"],
     "[[≥]] includes 2 (closed); greater means right.", "≥ or ≤: closed circle · > or <: open circle",
     ["[[≥]] includes 2: closed circle.", "Greater than: shade right."]),
  bq("Is [[x = −5]] a solution of [[−x > 4]]?", ["Yes, because [[5 > 4]]", "No, because [[−5 < 4]]", "Yes, because [[−5 > 4]]", "No, because [[5 < 4]]"],
     "[[−(−5) = 5]], and [[5 > 4]] is true.", "put the number in for [[x]]", ["[[−(−5) = 5]].", "[[5 > 4]] is true, so yes."]),
  bq("Chloe buys 2 muffins for $1.50 each and some juices for $2.25 each. Which equation gives the total cost, [[y]], for [[x]] juices?",
     ["[[y = 2.25x + 3]]", "[[y = 1.50x + 4.50]]", "[[y = 3x + 2.25]]", "[[y = 3.75x]]"],
     "Muffins: [[2 · 1.50 = 3]] (start). Juices: $2.25 each (rate). Like test Q6.", "[[y = mx + b]]: rate × amount + fixed cost",
     ["Fixed cost: [[2 · 1.50 = 3]].", "Rate: $2.25 per juice.", "[[y = 2.25x + 3]]."])],
 (3, 3): [
  bq("What is the solution set of [[−4x > 12]]?", ["[[x < −3]]", "[[x > −3]]", "[[x < 3]]", "[[x > 3]]"],
     "Divide by [[−4]] and flip: [[x < −3]].", "÷ by a negative → flip the sign", ["Divide by [[−4]]: [[12 ÷ −4 = −3]].", "Negative divisor: flip [[>]] to [[<]].", "[[x < −3]]."]),
  bq("What is the solution set of [[2x + 3 ≤ x − 1]]?", ["[[x ≤ −4]]", "[[x ≥ −4]]", "[[x ≤ −2]]", "[[x ≤ 4]]"],
     "Subtract [[x]]: [[x + 3 ≤ −1]]. Subtract 3: [[x ≤ −4]].", "get [[x]] on one side, like an equation",
     ["Subtract [[x]]: [[x + 3 ≤ −1]].", "Subtract 3: [[x ≤ −4]]."]),
  bq("Which inequality means the same as [[−6 ≤ x]]?", ["[[x ≥ −6]]", "[[x ≤ −6]]", "[[x > −6]]", "[[x < 6]]"],
     "Read it from [[x]]'s side: [[x]] is greater than or equal to [[−6]].", "switch sides → the sign points the other way",
     ["[[−6 ≤ x]]: [[−6]] is less than or equal to [[x]].", "So [[x]] is greater than or equal to [[−6]]: [[x ≥ −6]]."]),
  bq("What value of [[x]] makes [[3(x − 2) = 9]] true?", ["[[5]]", "[[3]]", "[[11/3]]", "[[1]]"], "[[3x − 6 = 9]], [[3x = 15]], [[x = 5]].",
     "distribute, then undo + and ×", ["Distribute: [[3x − 6 = 9]].", "Add 6: [[3x = 15]].", "Divide by 3: [[x = 5]]."])],
}

EXIT = {
 (1, 1): [
  mc("What value of [[p]] makes the equation [[7 − 3(p + 2) = 10 − (2p + 5)]] true?", ["[[−4]]", "[[4]]", "[[−6]]", "No solution"],
     "[[1 − 3p = 5 − 2p]] → [[−p = 4]] → [[p = −4]]", "Distribute on both sides first. −( ) changes every sign inside.",
     "Solve: [[7 − 3(p + 2) = 10 − (2p + 5)]]"),
  op("Solve the equation shown.<br>[[0.5(4x − 6) = −1.5x + 4]]", "[[x = 2]]", "[[2x − 3 = −1.5x + 4]] → [[3.5x = 7]] → [[x = 2]]",
     "Distribute the 0.5 to both terms.", ["Distribute: ______ = −1.5x + 4", "Add 1.5x to both sides: ______", "Add 3 to both sides: ______", "Divide: x = ______"],
     "Solve: [[0.5(4x − 6) = −1.5x + 4]]"),
  op("Does the equation shown below have one solution, no solution, or an infinite number of solutions? Explain your reasoning.<br>[[½(8x + 6) = 2(2x + 1) + 2]]",
     "No solution", "[[4x + 3 = 4x + 4]]: same [[x]]-coefficient, different constants, so [[3 = 4]] is never true",
     "Simplify each side, then compare the x-terms and numbers.",
     ["Left side simplifies to: ______", "Right side simplifies to: ______", "Circle: one solution · no solution · infinite"],
     "One, none, or infinite? [[½(8x + 6) = 2(2x + 1) + 2]]"),
  op("A triangle has a height of [[(x + 5)]] inches and a base of 6 inches. A rectangle has a length of 4 inches and a width of [[(x − 1)]] inches. "
     "The area of the triangle equals the area of the rectangle. What is the value of [[x]]?", "[[x = 19]]",
     "[[½(6)(x + 5) = 4(x − 1)]] → [[3x + 15 = 4x − 4]] → [[x = 19]]", "Triangle area = ½ · base · height. Rectangle area = length · width.",
     ["½ · 6 · (x + 5) = 4 · (x − 1)", "Simplify both sides: ______ = ______", "Solve: x = ______"],
     "Triangle: base 6, height [[(x + 5)]]. Rectangle: 4 by [[(x − 1)]]. Equal areas. Find [[x]].")],
 (2, 1): [
  op("Rewrite the equation in slope-intercept form.<br>[[6x + 3y = 12]]", "[[y = −2x + 4]]", "[[3y = −6x + 12]] → [[y = −2x + 4]]",
     "Get y alone: subtract the x-term, then divide every term.", ["Subtract 6x: 3y = ______", "Divide every term by 3: y = ______"]),
  op("Rewrite the equation [[y − 4 = 3(x + 2)]] in slope-intercept form.", "[[y = 3x + 10]]", "[[y − 4 = 3x + 6]] → [[y = 3x + 10]]",
     "Distribute first, then add 4 to both sides.", ["Distribute: y − 4 = ______", "Add 4: y = ______"]),
  mc("What are the [[x]]- and [[y]]-intercepts of [[2x − 5y = 10]]?", ["[[(5, 0)]] and [[(0, −2)]]", "[[(−5, 0)]] and [[(0, 2)]]",
                                                                       "[[(2, 0)]] and [[(0, −5)]]", "[[(5, 0)]] and [[(0, 2)]]"],
     "[[y = 0]]: [[2x = 10]], [[x = 5]]. [[x = 0]]: [[−5y = 10]], [[y = −2]]", "x-intercept: put 0 in for y. y-intercept: put 0 in for x.")],
 (2, 2): [
  op("The formula for the area of a rectangle is [[A = ℓw]]. Solve the equation for [[w]].", "[[w = A/ℓ]]", "Divide both sides by [[ℓ]]",
     "Undo the multiplication.", ["A = ℓw. Divide both sides by ______", "w = ______"]),
  op("The formula for the volume of a cylinder is [[V = πr²h]]. Solve the equation for [[h]].", "[[h = V/(πr²)]]", "Divide both sides by [[πr²]]",
     "Everything multiplied by h moves together.", ["V = πr²h. Divide both sides by ______", "h = ______"]),
  mc("Which equation is [[d = rt]] solved for [[r]]?", ["[[r = d/t]]", "[[r = dt]]", "[[r = t/d]]", "[[r = d − t]]"], "Divide both sides by [[t]]",
     "Undo × with ÷."),
  op("The lateral surface area of a can is [[S = 2πrh]]. [[S = 37.68]] square inches and [[r = 1.5]] inches. Use 3.14 for [[π]]. What is [[h]]?", "[[h = 4]] in.",
     "[[h = S/(2πr) = 37.68 ÷ 9.42 = 4]]", "Solve for h first, then put in the numbers.", ["h = S ÷ ______", "h = 37.68 ÷ ______ = ______"],
     "[[S = 2πrh]], [[S = 37.68]], [[r = 1.5]]. Find [[h]].")],
 (3, 1): [
  mc("Maya has $40 and earns $12 per hour. Which equation gives the total, [[y]], she has after working [[x]] hours?",
     ["[[y = 12x + 40]]", "[[y = 40x + 12]]", "[[y = −12x + 40]]", "[[y = 52x]]"], "Start $40, rate $12 per hour", "Rate goes with x. The start is b."),
  op("Jordan buys 4 notebooks that cost $1.75 each and some pens for $0.90 each. Write an equation for the total cost, [[y]], when Jordan buys [[x]] pens.",
     "[[y = 0.90x + 7]]", "Notebooks: [[4 · 1.75 = 7]]; pens: [[0.90x]]", "Find the fixed cost first: 4 notebooks × $1.75.",
     ["Fixed cost: 4 × 1.75 = ______", "y = ______x + ______"], "4 notebooks at $1.75, pens at $0.90. Equation for [[x]] pens?"),
  op("[[f(b) = 3.75b + 25]]. Write an inequality for sales of at most $1150, solve it, and graph the solution on a number line.",
     "[[b ≤ 300]], closed circle at 300, shaded left", "[[3.75b + 25 ≤ 1150]] → [[3.75b ≤ 1125]] → [[b ≤ 300]]",
     "At most → ≤. ≤ gets a closed circle.", ["3.75b + 25 ______ 1150", "b ______ ______", "Circle: open / closed. Shade: left / right"],
     "Sales of at most $1150: inequality for [[b]]?")],
 (3, 2): [
  mc("What is the solution set for [[−3x + 4 ≥ 19]]?", ["[[x ≤ −5]]", "[[x ≥ −5]]", "[[x ≤ 5]]", "[[x ≥ 5]]"],
     "[[−3x ≥ 15]] → divide by [[−3]], flip → [[x ≤ −5]]", "Dividing by a negative flips the sign."),
  op("Solve the inequality, and graph the solution on the number line.<br>[[5 − 2x < 11]]", "[[x > −3]], open circle at −3, shaded right",
     "[[−2x < 6]] → [[x > −3]] (flip)", "Subtract 5, then divide by −2 and flip.", ["Subtract 5: −2x < ______", "Divide by −2 and flip: x ______ ______"],
     "Solve and graph: [[5 − 2x < 11]]"),
  op("A tire has 26 psi and loses 0.1 psi per minute. It must stay at or above 22 psi. Write and solve an inequality for the time [[t]] in minutes.",
     "[[t ≤ 40]] minutes", "[[26 − 0.1t ≥ 22]] → [[−0.1t ≥ −4]] → [[t ≤ 40]]", "At or above → ≥. Divide by −0.1 and flip.",
     ["26 − 0.1t ______ 22", "−0.1t ≥ ______", "t ______ ______"], "Tire: 26 psi, −0.1 psi/min, stay ≥ 22. Solve for [[t]].")],
 (3, 3): [
  mc("What is the solution set for [[3(4 − x) > −2x + 10]]?", ["[[x < 2]]", "[[x > 2]]", "[[x ≤ −2]]", "[[x > −2]]"],
     "[[12 − 3x > −2x + 10]] → [[−x > −2]] → [[x < 2]]", "Distribute, move the x-terms, and flip if you divide by a negative."),
  op("Solve the inequality, and graph the solution on the number line.<br>[[1.5m + 4 ≥ −2(m − 9)]]", "[[m ≥ 4]], closed circle at 4, shaded right",
     "[[1.5m + 4 ≥ −2m + 18]] → [[3.5m ≥ 14]] → [[m ≥ 4]]", "Distribute the −2 to both terms.",
     ["Distribute: 1.5m + 4 ≥ ______", "Add 2m, subtract 4: ______ ≥ ______", "m ______ ______"], "Solve and graph: [[1.5m + 4 ≥ −2(m − 9)]]"),
  op("Solve the inequality.<br>[[−2(x + 1) ≥ 8]]", "[[x ≤ −5]]", "[[−2x − 2 ≥ 8]] → [[−2x ≥ 10]] → [[x ≤ −5]]", "Divide by −2 at the end: flip.",
     ["Distribute: ______ ≥ 8", "Add 2: −2x ≥ ______", "Divide by −2 and flip: x ______ ______"], "Solve: [[−2(x + 1) ≥ 8]]")],
}


# ================================================================ decks (each returns a list of days, each a list of slides)
GO = D.GO


def bell_href(n, d):
    return f"m3t1-lesson{n}-bellwork-day{d}.html"


def title_slide(n, pages, name, sub, days, notes):
    bw = " · ".join(f'<b><a class="go" href="{bell_href(n, d)}" {GO}>Day {d} →</a></b>' for d in range(1, days + 1))
    return (f'<section class="slide">\n  <p class="eyebrow">Bluebonnet Algebra I · Module 3 · Topic 1 · Lesson {n} · Student Edition pp. {pages}</p>\n'
            f'  <h1 style="margin-top:6px;font-size:56px">{name}</h1>\n  <div class="eq" style="margin-top:8px;font-size:40px">{sub}</div>\n'
            f'  <p style="font-size:24px;margin-top:6px">Bell work: {bw}</p>\n'
            f'  <p class="muted small">Click, or press → / Space, to reveal each step. ← goes back. F = full screen.</p>\n  {D.FOOT}\n'
            f'  <aside class="notes">{notes}</aside>\n</section>\n')


def bell(n, d, what="Review"):
    MP.BELL[(f"m3l{n}", d)] = [{k: q[k] for k in ("q", "choices", "why")} for q in BELL[n, d]]
    return D.bell(f"m3l{n}", d, what)


def exit_slide(n, d):
    items = EXIT[n, d]
    body = '<div class="col" style="gap:10px;margin-top:4px">' + "".join(
        f'<p>{k}. {mq(it["short"])}</p>{ans(mq(it["answer"]), True)}' for k, it in enumerate(items, 1)) + "</div>"
    work = " ".join(f"{k}. {re.sub(r'\[\[|\]\]', '', it['work'])}." for k, it in enumerate(items, 1))
    return sec(f"Day {d} · Exit Ticket", "Show what you know", body,
               f"Printed copy: EXIT TICKET/T1-Exit-Ticket-{DATES[n, d]}.pdf (written like the End of Topic 1 test). Give about 8 minutes. Work: {work}")


def divider(n, d, q, recap):
    return sec(f"Lesson {n}", f"Day {d}", f'<p class="step" style="font-size:32px;max-width:900px">Essential Question: {q}</p>',
               f"Show this, then go to the bell work while you take attendance. Afterward, ask two or three students to summarize Day {d - 1}: {recap}", True)


def homework(n, se, items, key):
    return sec("Homework", f"Lesson {n} Assignment · SE pp. {se}", row(*[card(h, p(b)) for h, b in items], gap=24), key)


def deck1():
    s = [title_slide(1, "345–356", "Solving Linear Equations", "one solution · no solution · infinite solutions", 1,
                     "One day on the 150-day calendar (Thu Nov 5): Getting Started, Activities 1.1 and 1.2 (all starred). Activity 1.3 Tic-Tac-Bingo is "
                     "not starred and is saved for the Nov 19 retake day. Talk the Talk is included as a short test-style area problem because it "
                     "matches End of Topic Assessment question 11."), bell(1, 1)]
    s.append(D.today(1, 345, ["Write equivalent equations using properties of equality.",
                              "Use properties of equality to solve linear equations and justify a solution method.",
                              "Determine whether an equation has one solution, no solution, or infinite solutions.",
                              "Solve linear equations with variables on both sides."], "New key terms: solution · no solution · infinite solutions"))
    s.append(D.eq_slide(1, 345, "You know that equations are one way to represent a linear function.",
                        "How can you use equations to solve for unknown input values of a function?"))
    s.append(sec("Getting Started · Equation Creation · SE p. 346", f"Build harder equations from {mt('x = 2')}",
                 row(p("A <b>solution</b> to an equation is a value for the variable that makes the equation a true statement.", "")
                     + st("a. Add 3 to each side: " + mt("x + 3 = 5")) + st("b. Multiply each side by 4: " + mt("4x + 12 = 20"))
                     + st("c. Subtract " + mt("2x") + ": " + mt("2x + 12 = −2x + 20")) + st("d. Divide each side by 2: " + mt("x + 6 = 10 − x")),
                     card("2. Partner check", p("Substitute 2 into your partner's last equation.") + ans("2 + 6 = 10 − 2 → 8 = 8 ✓")
                          + st("Same operation on <b>both</b> sides, to <b>every</b> term, keeps the solution.", "small muted"))),
                 "Getting Started, 15 minutes. Look for students who multiply or divide only the x-term instead of every term (TE common misconception). Algebra tiles help."))
    s.append(sec("Activity 1.1 · Using Properties to Justify Solutions · SE p. 347", "Properties of equality",
                 table(["Property", "For all numbers a, b, and c"], [["addition", M("If a = b, then a + c = b + c.")], ["subtraction", M("If a = b, then a − c = b − c.")],
                                                                     ["multiplication", M("If a = b, then ac = bc.")], ["division", M("If a = b and c ≠ 0, then a/c = b/c.")]], 26)
                 + st("These rules keep both sides balanced while you isolate the variable."),
                 "Explicit instruction. TE suggestion: make a poster of both property tables; Lessons 2 and 3 use them again."))
    s.append(sec("Activity 1.1 · Question 1 · SE p. 347", "Harper and Sofia both started from " + mt("x = 2"),
                 row(card("Harper", eq("−3x + 14 = 18 − 5x", "sm") + st("Substitute: " + mt("−6 + 14 = 18 − 10")) + ans("8 = 8 ✓")
                          + st("Properties: add " + mt("5x") + ", subtract 14 → " + mt("2x = 4") + " → " + mt("x = 2"))),
                     card("Sofia", eq("2x = 5 − ½x", "sm") + st("Substitute: " + mt("4 = 5 − 1")) + ans("4 = 4 ✓")
                          + st("Properties: add " + mt("½x") + " → " + mt("5/2 x = 5") + ", multiply by " + mt("2/5") + " → " + mt("x = 2"))), gap=24),
                 "Question 1. Assistance for All: multiply Sofia's equation by 2 first to clear the fraction (4x = 10 − x)."))
    s.append(sec("Activity 1.1 · Question 2 · SE p. 348", "Solve, check, and name each property",
                 row(eq("b. &nbsp;0.6(2x + 1) = 4x + 6.2", "sm") + st(mt("1.2x + 0.6 = 4x + 6.2") + " &nbsp;distributive")
                     + st(mt("−2.8x + 0.6 = 6.2") + " &nbsp;subtraction") + st(mt("−2.8x = 5.6") + " &nbsp;subtraction") + ans("x = −2 &nbsp; (division)", True),
                     eq("c. &nbsp;½x − 6 = 2 + (2x + 1)", "sm") + st(mt("½x − 6 = 3 + 2x") + " &nbsp;commutative, associative")
                     + st(mt("−9 = 3/2 x") + " &nbsp;subtraction") + ans("x = −6 &nbsp; (multiplication by ⅔)", True)),
                 "Number properties (commutative, associative, distributive) are on SE p. 348. Check b: 0.6(−3) = −1.8 and 4(−2) + 6.2 = −1.8. "
                 "Questions 2 and 3 are the TE's check point; for more practice assign Skills Practice Set A."))
    s.append(sec("Activity 1.1 · Question 3 · SE p. 349", "Daniel and Chloe: same equation, different first step",
                 row(card("Daniel", eq("4(3x + 2) = 8x + 4", "sm") + st(mt("12x + 8 = 8x + 4") + " distributive first") + st(mt("4x = −4")) + ans("x = −1")),
                     card("Chloe", eq("4(3x + 2) = 8x + 4", "sm") + st(mt("3x + 2 = 2x + 1") + " divide by 4 first") + st(mt("x = −1")) + ans("x = −1")), gap=24)
                 + st("More than one correct path. Both finish with subtraction and division properties."),
                 "Ask: Why do you think Chloe chose 4 as the divisor? Whose method do you prefer?"))
    s.append(sec("Activity 1.2 · Solutions to Linear Equations · SE pp. 349–350", "Can you change the truth of a sentence?",
                 row(card("1. " + mt("2 = 2"), st("Add " + mt("x") + ": " + mt("2 + x = 2 + x")) + st("Multiply by 5: " + mt("10 + 5x = 10 + 5x")) + st("Still always true.")),
                     card("2. " + mt("2 = 3"), st("Add " + mt("x") + ": " + mt("2 + x = 3 + x")) + st("Multiply by 5: " + mt("5(2 + x) = 5(3 + x)")) + st("Still always false.")), gap=24)
                 + st("<b>No solution</b>: no value makes the equation true. <b>Infinite solutions</b>: every value makes it true."),
                 "Questions 1–3. Common misconception: 8 = 8 does not mean x = 8; it means the value we substituted works."))
    s.append(sec("Activity 1.2 · Question 4 + Seeing Structure", "Simplify each side, then compare",
                 table(["Equation", "Simplified", "Solutions"], [[M("2x + 5 = 2x + 5"), "same coefficient, same constant", "<b>infinite</b>"],
                                                                [M("2x + 5 = 2x + 7"), "same coefficient, different constant", "<b>none</b>"],
                                                                [M("2x + 5 = 3x + 5"), "different coefficients", M("one: x = 0")],
                                                                [M("2x = 3x"), "different coefficients", M("one: x = 0")]], 24, (2,)),
                 "Question 4 and the TE's Seeing Structure questions. Stamp the learning: one solution, no solution, or infinite solutions. Skills Practice Set B."))
    s.append(sec("Test Practice · Like End of Topic Questions 2 and 5", "Which kind of solution?",
                 row(p("1. What value of " + mt("m") + " makes " + mt("6 − 4(m + 2) = 3 − 2(2m + 1)") + " true?", "")
                     + st(mt("−4m − 2 = −4m + 1")) + ans("No solution (−2 ≠ 1)", True),
                     p("2. One solution, no solution, or infinite? " + mt("¼(8x + 12) = 2(x + 2) − 1"), "")
                     + st(mt("2x + 3 = 2x + 3")) + ans("Infinite solutions: the two sides are equivalent", True)),
                 "Added for this deck; not from the textbook. On the test, 'No solution' is a real answer choice: simplify both sides before guessing."))
    s.append(sec("Talk the Talk · One Step at a Time · SE p. 352", "Equal areas (like test question 11)",
                 row(p("Rectangle A: width " + mt("(5 + 2x)") + " in., length 6 in. Rectangle B: width 8 in., length " + mt("(x + 5)") + " in. Same area. Find " + mt("x") + ".", "")
                     + eq("6(5 + 2x) = 8(x + 5)", "sm", True),
                     st(mt("30 + 12x = 8x + 40") + " &nbsp;distributive") + st(mt("12x = 8x + 10") + " &nbsp;subtraction")
                     + st(mt("4x = 10") + " &nbsp;subtraction") + ans("x = 2.5 &nbsp; (division)", True)),
                 "Not starred; included because End of Topic question 11 is the same kind of problem. Skip if short on time."))
    s.append(sec("Essential Question · Answered", "How can you use equations to solve for unknown inputs?",
                 '<div class="col" style="gap:20px;margin-top:6px">' + st("Use properties of equality to isolate the variable, and name the property for each step.", "")
                 + st("Simplify each side first. Same coefficient and constant: infinite. Same coefficient, different constant: none. Otherwise: one solution.", "")
                 + "</div>", "Have students answer the Essential Question on the lesson opener page."))
    s.append(exit_slide(1, 1))
    s.append(homework(1, "355–356", [("Practice", "1a–e: solve and write the property for each step. 2a–f: one solution, no solution, or infinite?")],
                      "Practice 2 answers: a none, b x = 7, c x = 2, d infinite, e none, f infinite."))
    return [s]


def deck2():
    q = "How can you use those same properties to solve for one specific variable in an equation that has multiple variables?"
    d1 = [title_slide(2, "357–370", "Literal Equations", f"{M('y = mx + b')} · {M('y − y₁ = m(x − x₁)')} · {M('Ax + By = C')}", 2,
                      "Two days on the 150-day calendar (Mon Nov 9 and Tue Nov 10). Every activity is starred: Day 1 Getting Started and Activity 2.1; "
                      "Day 2 Activities 2.2, 2.3 and Talk the Talk. End of Topic questions 7, 8 and 10 come from this lesson."), bell(2, 1)]
    d1.append(D.today(2, 357, ["Rewrite linear equations in different forms.", "Analyze the structure of different forms of linear equations.",
                               "Recognize and use literal equations.", "Rearrange literal equations to highlight quantities of interest."], "New key term: literal equation"))
    d1.append(D.eq_slide(2, 357, "You have used different properties to solve linear equations to determine which value makes the equation true.", q))
    d1.append(sec("Day 1 · Getting Started · Perimeter Perspectives · SE p. 358", "Two backyards share sides with a park",
                  row(p("The city gives Juan and Mia the perimeter " + mt("P") + " of the park. Juan needs the width " + mt("w") + "; Mia needs the length " + mt("ℓ") + ".", "")
                      + st("Juan: " + mt("w = P/2 − ℓ")) + st("Mia: " + mt("ℓ = P/2 − w")),
                      card("2. Show they are equivalent", st("Multiply each by 2: " + mt("2w = P − 2ℓ") + " and " + mt("2ℓ = P − 2w"))
                           + ans("Both become 2ℓ + 2w = P"))),
                  "Getting Started, 15 minutes. Remember: the perimeter of a rectangle is P = 2ℓ + 2w. Same formula, solved for the variable each person needs."))
    d1.append(sec("Day 1 · Activity 2.1 · Equations in Different Forms · SE pp. 359–360", "Find the slope and both intercepts",
                  row(card("1. " + mt("y = −⅔x + 4"), ans("slope −⅔") + ans("(0, 4) · (6, 0)")),
                      card("2. " + mt("y = 4(x − 2)"), ans("slope 4") + ans("(0, −8) · (2, 0)")),
                      card("3. " + mt("3x − 2y = 8"), ans("slope 3/2") + ans("(0, −4) · (8/3, 0)")), gap=20)
                  + st("y-intercept: put 0 in for <i>x</i>. x-intercept: put 0 in for <i>y</i>."),
                  "Questions 1–3, pairs. Q3: rewrite in slope-intercept form (y = 3/2x − 4) or use intercepts."))
    d1.append(sec("Day 1 · Activity 2.1 · Three Forms · SE p. 360", "Which form shows what?",
                  table(["Form", "Equation", "Shows quickly"], [["slope-intercept", M("y = mx + b"), "slope, y-intercept"],
                                                               ["point-slope", M("y − y₁ = m(x − x₁)"), "slope, a point"],
                                                               ["standard", M("Ax + By = C"), M("slope −A/B, x-int (C/A, 0), y-int (0, C/B)")]], 24, (2,))
                  + st("In standard form A, B, and C are integers, and A and B are not both 0."),
                  "Explicit instruction (Questions 4–6). For graphing technology, slope-intercept form is the most efficient (Q7). Skills Practice Sets A–C."))
    d1.append(sec("Day 1 · Activity 2.1 · Questions 8–9 · SE p. 361", "Rewrite each equation",
                  row(p("8. Slope-intercept form", "") + eq("a. y − 2 = 5(x − 7)", "sm") + ans("y = 5x − 33") + eq("b. 8x − 2y = 12", "sm") + ans("y = 4x − 6"),
                      p("9. Standard form", "") + eq("a. y + 7 = 0.5(x − 1)", "sm") + ans("x − 2y = 15") + eq("b. y = −4x + 3", "sm") + ans("4x + y = 3")),
                  "For 9a, multiply by 2 to clear the decimal: 2y + 14 = x − 1, so x − 2y = 15."))
    d1.append(sec("Test Practice · Like End of Topic Questions 7 and 10", "Rewrite in slope-intercept form",
                  row(eq("1. &nbsp;2x + 4y = 8", "sm") + st(mt("4y = −2x + 8")) + ans("y = −½x + 2"),
                      eq("2. &nbsp;y + 1 = −3(x − 2)", "sm") + st(mt("y + 1 = −3x + 6")) + ans("y = −3x + 5")),
                  "Added for this deck; not from the textbook. Standard form: subtract the x-term, then divide every term. Point-slope: distribute, then move the constant."))
    d1.append(exit_slide(2, 1))
    d2 = [divider(2, 2, q, "Which form of a line shows the slope and y-intercept fastest?"), bell(2, 2)]
    d2.append(sec("Day 2 · Activity 2.2 · Rewriting Literal Equations · SE p. 362", "Celsius and Fahrenheit",
                  row(p("A <b>literal equation</b> is an equation in which the variables represent specific measures, like a formula.", "")
                      + eq("C = 5/9(F − 32)", "sm") + st("1. Multiply by " + mt("9/5") + ": " + mt("9/5 C = F − 32")) + ans("F = 9/5 C + 32"),
                      card("2. Who is warmer?", p("Jayden: 77°F. Mateo: 30°C.") + st(mt("F = 9/5(30) + 32 = 86")) + ans("Mateo: 86°F > 77°F", True))),
                  "Activity 2.2, 15–20 minutes. Either convert 30°C to °F (86) or 77°F to °C (25)."))
    d2.append(sec("Day 2 · Activity 2.2 · Question 3 and Worked Example · SE pp. 363–364", "Find the error",
                  row(card("Ethan", eq("C = 5/9 F − 32", "sm") + st("Error: he did not distribute 5/9 to the 32.")),
                      card("Minh", eq("9C = 45F − 1440", "sm") + st("Error: he multiplied 9 · 5/9 F wrong (it is 5F, not 45F).")),
                      card("4. No fractions", eq("9C = 5(F − 32)", "sm") + ans("9C − 5F = −160")), gap=20),
                  "Isabella is correct: distribute, multiply by 9, add 160, divide by 5. The Worked Example multiplies by the denominator to clear the fraction."))
    d2.append(sec("Day 2 · Activity 2.3 · Solving Literal Equations for Specific Variables · SE pp. 365–366", "Solve for the height",
                  row(card("1. Box", eq("V = Bh", "sm") + ans("h = V/B") + st("V = 450, B = 75: " + mt("h = 6") + " in.")),
                      card("2. Cone", eq("V = ⅓πr²h", "sm") + ans("h = 3V/(πr²)") + st("cubic ÷ square units = linear units")),
                      card("3. Trapezoid", eq("A = ½h(b₁ + b₂)", "sm") + ans("h = 2A/(b₁ + b₂)") + st("A = 24, bases 9 and 7: " + mt("h = 3") + " cm")), gap=18),
                  "Questions 1–3, 15–20 minutes. Skills Practice Set D."))
    d2.append(sec("Day 2 · Activity 2.3 · Question 4 · SE p. 366", "Solve " + mt("Z = A/B + C/D") + " for each variable",
                  row(card("a. Solve for " + mt("A"), st("Multiply by " + mt("B") + ": " + mt("BZ = A + BC/D")) + ans("A = BZ − BC/D")),
                      card("b. Solve for " + mt("D") + " (challenge)", st("Multiply by " + mt("BD") + ": " + mt("BDZ = AD + BC")) + st("Factor out " + mt("D") + ": " + mt("D(BZ − A) = BC"))
                           + ans("D = BC/(BZ − A)")), gap=24),
                  "Part b is a challenge: collect the D terms on one side and factor out D."))
    d2.append(sec("Day 2 · Talk the Talk · Rearrange It · SE p. 367", "Cans of soup (use 3.14 for π)",
                  row(p("1. Lateral area " + mt("S = 2πrh") + ". Solve for " + mt("h") + ".", "") + ans("h = S/(2πr)")
                      + p("2. " + mt("S = 37.68") + ", " + mt("r = 1.5") + ".", "") + ans("h = 4 in."),
                      p("3. Surface area " + mt("S = 2πr² + 2πrh") + ". Solve for " + mt("h") + ".", "") + ans("h = (S − 2πr²)/(2πr)")
                      + p("4. " + mt("S = 51.81") + ", " + mt("r = 1.5") + ".", "") + ans("h = 4 in.")),
                  "Talk the Talk, 10 minutes. Q4: 51.81 − 14.13 = 37.68, and 37.68 ÷ 9.42 = 4."))
    d2.append(sec("Test Practice · Like End of Topic Question 8", "Solve each formula for the given variable",
                  row(eq("1. &nbsp;A = ½bh &nbsp;for b", "sm") + st("Multiply by 2: " + mt("2A = bh")) + ans("b = 2A/h"),
                      eq("2. &nbsp;I = Prt &nbsp;for t", "sm") + st("Divide by " + mt("Pr")) + ans("t = I/(Pr)")),
                  "Added for this deck; not from the textbook. Undo the operations on the variable you want, in reverse order."))
    d2.append(sec("Essential Question · Answered", "How do you solve for one variable in a formula?",
                  '<div class="col" style="gap:20px;margin-top:6px">' + st("Use the same properties of equality: undo each operation on that variable, doing the same to both sides.", "")
                  + st("Every other letter is treated like a number.", "") + st("Pick the form that shows what you need: slope-intercept for the slope and y-intercept, point-slope for a point.", "") + "</div>",
                  "Have students answer the Essential Question on the lesson opener page."))
    d2.append(exit_slide(2, 2))
    d2.append(homework(2, "369–370", [("Day 1", "Practice 1a–d: rewrite in the given form."), ("Day 2", "Practice 2–3: formulas, plus Prepare (inequalities).")],
                       "Practice 1: a 3x − 4y = 32, b y = −3x + 15, c y = 5/2x + 9, d x − 2y = 22. Prepare: x = 5, x > 7, x ≤ −3, x < −4."))
    return [d1, d2]


def deck3():
    q = "Can you use these same methods to solve problems involving linear inequalities?"
    sales = graph(380, 330, [0, 600], [0, 2400], [60, 120], [200, 400], [L((0, 25), (400, 1525), "f(b)"), L((0, 1600), (1, 1600), None, "b", True, True)],
                  [[420, 1600, "(420, 1600)"]], "f(b) = 3.75b + 25 with the horizontal line y = 1600")
    hike = graph(380, 330, [0, 260], [0, 5000], [20, 60], [500, 1000], [L((0, 4800), (240, 0), "h(m)"), L((0, 3200), (1, 3200), None, "b", True, True)],
                 [[80, 3200, "(80, 3200)"]], "h(m) = −20m + 4800 with the horizontal line y = 3200")
    d1 = [title_slide(3, "371–386", "Modeling Linear Inequalities", "< &nbsp; ≤ &nbsp; > &nbsp; ≥", 3,
                      "Three days on the 150-day calendar (Wed Nov 11, Thu Nov 12, Mon Nov 16). Every activity is starred: Day 1 Getting Started and 3.1; "
                      "Day 2 3.2 and 3.3; Day 3 3.4 and Talk the Talk. End of Topic questions 1, 3, 6 and 9 come from this lesson."), bell(3, 1)]
    d1.append(D.today(3, 371, ["Write and solve inequalities.", "Analyze a graph on a coordinate plane to solve problems involving inequalities.",
                               "Interpret how a negative rate affects how to solve an inequality."], "New key term: linear inequality"))
    d1.append(D.eq_slide(3, 371, "You have used horizontal lines on a graph and properties of equality to solve problems modeled with linear equations.", q))
    d1.append(sec("Day 1 · Getting Started · Fundraising Function · SE p. 372", "Elijah sells popcorn",
                  row(p("Each camper starts with a $25 credit. Each box sells for $3.75.", "") + st("1. " + mt("f(b) = 3.75b + 25")),
                      card("2. Analyze", st("Independent: boxes sold. Dependent: total sales ($).") + st("Slope 3.75: dollars per box.") + st("y-intercept 25: the starting credit."))),
                  "Getting Started, 10–15 minutes. Ask yourself: how will you represent the $25 credit in your function?"))
    d1.append(sec("Day 1 · Activity 3.1 · Modeling Linear Inequalities · SE pp. 373–374", "Read the graph at $1600",
                  row(sales, st("1. Draw " + mt("y = 1600") + " to the line, then straight down: " + mt("b = 420") + " boxes.")
                      + p("A <b>linear inequality</b> is a non-equal comparison of two linear expressions.", "step")
                      + st("2. Below the line (and on it): " + mt("f(b) ≤ 1600") + ", so " + mt("b ≤ 420") + ": ● closed circle, shade left.")
                      + st("3. Above the line: " + mt("b > 420") + ": ○ open circle, shade right.")),
                  "Activity 3.1, 25–30 minutes. Only whole numbers of boxes make sense in context. Skills Practice Sets A and B."))
    d1.append(sec("Day 1 · Activity 3.1 · Questions 4–5 · SE p. 375", "Open or closed? Use the graph.",
                  row(card("4. Circles", p("○ open: the point is <b>not</b> included (&lt;, &gt;).") + p("● closed: the point <b>is</b> included (≤, ≥).")),
                      card("5. How many boxes?", p("a. at least $925") + ans("b ≥ 240") + p("b. less than $2050") + ans("b < 540") + p("c. exactly $700") + ans("b = 180")), gap=24),
                  "Check: 3.75(240) + 25 = 925; 3.75(540) + 25 = 2050; 3.75(180) + 25 = 700."))
    d1.append(sec("Test Practice · Like End of Topic Questions 1 and 6", "Write the equation",
                  row(p("1. Ana has $60 and saves $15 per week. Equation for the amount " + mt("y") + " after " + mt("x") + " weeks?", "") + ans("y = 15x + 60"),
                      p("2. Ben buys 3 tickets at $8.50 each and some snacks at $3.25 each. Total cost " + mt("y") + " for " + mt("x") + " snacks?", "")
                      + st("Fixed: " + mt("3 · 8.50 = 25.50")) + ans("y = 3.25x + 25.50")),
                  "Added for this deck; not from the textbook. The rate goes with x; the starting or fixed amount is b."))
    d1.append(exit_slide(3, 1))
    d2 = [divider(3, 2, q, "What do open and closed circles mean?"), bell(3, 2)]
    d2.append(sec("Day 2 · Activity 3.2 · Solving Two-Step Linear Inequalities · SE p. 376", "First deposit: at least $1100",
                  row(p("To <b>solve an inequality</b> means to determine the values of the variable that make it true.", "")
                      + eq("3.75b + 25 ≥ 1100", "sm") + st(mt("3.75b ≥ 1075")) + st(mt("b ≥ 286.6…")),
                      card("1. How many boxes?", ans("at least 287 boxes", True) + st("He can't sell part of a box, and 286 boxes is not enough."))),
                  "Worked Example: solve an inequality the same way you solve an equation. Think about how accurate the answer needs to be."))
    d2.append(sec("Day 2 · Activity 3.2 · Questions 2–3 · SE p. 377", "Write and solve",
                  row(p("a. Most boxes and still under $600?", "") + st(mt("3.75b + 25 < 600 → b < 153.3…")) + ans("at most 153 boxes", True),
                      p("b. At least how many boxes for $1500?", "") + st(mt("3.75b + 25 ≥ 1500 → b ≥ 393.3…")) + ans("at least 394 boxes", True))
                  + st("3. The method does not change for other forms: use the properties of equality."),
                  "\"At least\" rounds up; \"at most\" rounds down."))
    d2.append(sec("Day 2 · Activity 3.3 · Reversing Inequality Signs · SE p. 378", "Hiking down from 4800 feet at 20 feet per minute",
                  row(hike, st("1. " + mt("h(m) = −20m + 4800")) + st("Slope −20: down 20 ft each minute. y-int 4800: the start.")
                      + st("x-int 240: sea level after 240 min. Domain " + mt("0 ≤ m ≤ 240") + ".")),
                  "Activity 3.3, 20–25 minutes. Ask: what are the independent and dependent quantities and their units?"))
    d2.append(sec("Day 2 · Activity 3.3 · Questions 3–6 · SE p. 379", "Below 3200 feet: why does the sign flip?",
                  row(st("3. Graph: below 3200 ft after " + mt("m > 80")) + eq("−20m + 4800 < 3200", "sm", True) + st(mt("−20m < −1600"))
                      + ans("m > 80 &nbsp;(÷ −20 flips the sign)", True),
                      table([M("h(m)"), M("m")], [[M("h(m) > 3200"), M("m < 80")], [M("h(m) ≥ 3200"), M("m ≤ 80")], [M("h(m) = 3200"), M("m = 80")],
                                                  [M("h(m) < 3200"), M("m > 80")], [M("h(m) ≤ 3200"), M("m ≥ 80")]], 22, (1,))
                      + st("Multiply or divide by a negative → <b>reverse</b> the sign.")),
                  "Stamp the learning: when you multiply or divide both sides by a negative number, the inequality sign reverses. Skills Practice Set C."))
    d2.append(exit_slide(3, 2))
    d3 = [divider(3, 3, q, "When does the inequality sign flip?"), bell(3, 3)]
    d3.append(sec("Day 3 · Activity 3.4 · Solving Other Linear Inequalities · SE p. 380", mt("5x + 2 ≥ 3x − 10"),
                  row(card("Victoria", st("x-terms left: " + mt("2x + 2 ≥ −10")) + st(mt("2x ≥ −12")) + ans("x ≥ −6")),
                      card("Kai", st("x-terms right: " + mt("2 ≥ −2x − 10")) + st(mt("12 ≥ −2x") + ", ÷ −2 flips") + ans("−6 ≤ x")), gap=24)
                  + st("Same answer: " + mt("−6 ≤ x") + " means " + mt("x ≥ −6") + ". It works like an equation, but watch the sign."),
                  "Questions 1–2. Keeping x on the side with the larger coefficient avoids dividing by a negative."))
    d3.append(sec("Day 3 · Activity 3.4 · Questions 3–4 · SE p. 381", mt("−4(x − 6) < 22"),
                  row(card("Aaliyah", st("Distribute: " + mt("−4x + 24 < 22")) + st(mt("−4x < −2") + ", ÷ −4 flips") + ans("x > ½")),
                      card("Ava", st("÷ −4 first, flip: " + mt("x − 6 > −5½")) + st("Add 6") + ans("x > ½")), gap=24)
                  + st("Distributing works the same for inequalities and equations."),
                  "Skills Practice Set D."))
    d3.append(sec("Day 3 · Talk the Talk · It's About Solutions, More or Less · SE p. 382", "Solve and graph each inequality",
                  row(eq("a. −⅔x ≥ 7", "sm") + ans("x ≤ −21/2 &nbsp;●, shade left", True) + eq("b. 32 > 23 − x", "sm") + ans("x > −9 &nbsp;○, shade right", True),
                      eq("c. 15 − 4x ≤ 3x − 6", "sm") + ans("x ≥ 3 &nbsp;●, shade right", True) + eq("d. 2(x + 6) < 14 + 4x", "sm") + ans("x > −1 &nbsp;○, shade right", True)),
                  "Talk the Talk Q1, 10 minutes."))
    d3.append(sec("Day 3 · Talk the Talk · Question 2 · SE p. 382", "If " + mt("A < B") + ", when is each statement true?",
                  row(card(mt("A + C < B + C"), ans("always")), card(mt("AC > BC"), ans("only when C < 0")), card(mt("−A < −B"), ans("never")), gap=20),
                  "Multiplying by a negative C flips the sign; multiplying by −1 always flips it."))
    d3.append(sec("Test Practice · Like End of Topic Questions 3 and 9", "Solve; graph the second one",
                  row(p("1. Solution set for " + mt("2(5 − x) > −x + 4") + "?", "") + st(mt("10 − 2x > −x + 4 → −x > −6")) + ans("x < 6"),
                      p("2. " + mt("2m − 1 ≥ −(m − 8)"), "") + st(mt("2m − 1 ≥ −m + 8 → 3m ≥ 9")) + ans("m ≥ 3 &nbsp;●, shade right", True)),
                  "Added for this deck; not from the textbook. The test gives answer choices with all four signs: check the flip."))
    d3.append(sec("Essential Question · Answered", "Do the same methods work for inequalities?",
                  '<div class="col" style="gap:20px;margin-top:6px">' + st("Yes: graphs (horizontal lines) and properties of equality both work.", "")
                  + st("Exception: multiplying or dividing both sides by a negative number <b>reverses</b> the inequality sign.", "")
                  + st("Graph: ○ for &lt; and &gt;, ● for ≤ and ≥.", "") + "</div>", "Have students answer the Essential Question on the lesson opener page."))
    d3.append(exit_slide(3, 3))
    d3.append(homework(3, "383–386", [("Day 1", "Practice 1a–d (Noah's trip)."), ("Day 2", "Practice 1e–g, 2a–b."), ("Day 3", "Practice 3a–d + Topic 1 Self-Reflection.")],
                       "Practice 3: a x > −1, b x < 7, c d ≤ 11, d k ≤ −24."))
    return [d1, d2, d3]


LESSONS = {
 1: dict(stem="m3t1-lesson1-solving-linear-equations", name="Solving Linear Equations", deck=deck1, se="345–356"),
 2: dict(stem="m3t1-lesson2-literal-equations", name="Literal Equations", deck=deck2, se="357–370"),
 3: dict(stem="m3t1-lesson3-modeling-linear-inequalities", name="Modeling Linear Inequalities", deck=deck3, se="371–386"),
}
D.STARS.update({"m3l1": {"Getting Started", "1.1", "1.2"}, "m3l2": {"Getting Started", "2.1", "2.2", "2.3"}, "m3l3": {"Getting Started", "3.1", "3.2", "3.3", "3.4"}})


def doc(head_title, slides):
    head = re.sub(r"<title>.*?</title>", f"<title>{head_title}</title>", D.HEAD, count=1)
    return head + '<div id="stage">\n\n' + "\n".join(slides) + D.TAIL


def pptx(path):
    r = subprocess.run([sys.executable, str(ROOT / "make_pptx.py"), path.relative_to(ROOT).as_posix()], capture_output=True, text=True)
    print("  ", (r.stdout.strip().splitlines() or ["?"])[-1])
    if "WARNING" in r.stdout:
        print("  ", "\n   ".join(l for l in r.stdout.splitlines() if "WARNING" in l))


# ================================================================ accommodations data
V = A.vocab
ACC = {
 1: dict(
  vocab=V(("Solution", "A value for the variable that makes the equation true.", "x = 2 in x + 3 = 5"),
          ("Properties of equality", "Do the same thing to both sides and the equation stays balanced.", "add, subtract, multiply, divide"),
          ("Distributive property", "Multiply the number outside by every term inside.", "3(x − 2) = 3x − 6"),
          ("No solution", "No value works. The sides simplify to a false statement.", "3 = 4"),
          ("Infinite solutions", "Every value works. Both sides are the same.", "2x + 5 = 2x + 5"),
          ("Coefficient", "The number in front of a variable.", "the 4 in 4x")),
  plans={1: ["Bell work (5 min)", "Getting Started: build equations from x = 2", "Activity 1.1: name the property for each step",
             "Activity 1.2: one, none, or infinite solutions", "Exit ticket"]},
  notes={1: [("Solve", "<p class='small'>1. Distribute.<br>2. Combine like terms.<br>3. Get x-terms on one side.<br>4. Undo + and −, then × and ÷.</p>"),
             ("Check", "<p class='small'>Put your answer back in. Both sides equal → correct.</p>"),
             ("How many solutions?", "<p class='small'>Same x-term, same number: infinite.<br>Same x-term, different number: none.<br>Different x-terms: one.</p>")]},
  ref=["<b>Distribute</b> first: multiply the outside number by every term inside.",
       "<b>Get x alone:</b> undo + and − first, then × and ÷. Do the same thing to both sides.",
       "<b>Check:</b> put your answer back in. Both sides equal → correct.",
       "<b>How many solutions?</b> Same x-term and same number: infinite. Same x-term, different number: none. Otherwise: one."],
  cans=["solve an equation and name the property for each step", "tell if an equation has one, no, or infinite solutions"],
  steps=["Distribute.", "Combine like terms on each side.", "Move the x-terms to one side.", "Undo + or −.", "Undo × or ÷.", "Check by substituting."],
  skills={1: [("Solve and justify", ("Solve 3(x + 2) = 18", ["Distribute: 3x + 6 = 18", "Subtract 6: 3x = 12", "Divide by 3"], "x = 4"),
               ("2(x − 1) = x + 5", ["Distribute: 2x − 2 = ___", "Subtract x: ___ − 2 = 5", "Add 2: x = ___"], "x = 7"),
               ("4(x + 1) = 2x + 10", "x = 3")),
              ("One, none, or infinite?", ("2x + 4 = 2(x + 2)", ["Simplify the right: 2x + 4", "Same x-term, same number"], "infinite"),
               ("3x + 1 = 3x + 7", ["Both sides have ___x", "The numbers 1 and 7 are ___ (same / different)"], "no solution"),
               ("5x − 2 = 5x − 2", "infinite"))]}),
 2: dict(
  vocab=V(("Slope-intercept form", "y = mx + b. Shows the slope m and y-intercept (0, b).", "y = 2x + 3"),
          ("Point-slope form", "y − y₁ = m(x − x₁). Shows the slope and a point.", "y − 4 = 3(x + 2)"),
          ("Standard form", "Ax + By = C, with integers A, B, C.", "6x + 3y = 12"),
          ("x-intercept", "Where the line crosses the x-axis. Put 0 in for y.", "(5, 0)"),
          ("y-intercept", "Where the line crosses the y-axis. Put 0 in for x.", "(0, −2)"),
          ("Literal equation", "A formula with letters for measures. You can solve it for any letter.", "V = Bh → h = V/B")),
  plans={1: ["Bell work (5 min)", "Getting Started: the park's perimeter", "Activity 2.1: slope and intercepts from three forms", "Exit ticket"],
         2: ["Bell work (5 min)", "Activity 2.2: Celsius and Fahrenheit", "Activity 2.3: solve formulas for a letter", "Talk the Talk", "Exit ticket"]},
  notes={1: [("Standard → slope-intercept", "<p class='small'>1. Subtract the x-term.<br>2. Divide every term by the number with y.</p>"),
             ("Point-slope → slope-intercept", "<p class='small'>1. Distribute.<br>2. Add or subtract to get y alone.</p>"),
             ("Intercepts", "<p class='small'>x-intercept: y = 0.<br>y-intercept: x = 0.</p>")],
         2: [("Literal equation", "<p class='small'>Circle the letter you want. Undo everything around it.</p>"),
             ("Undo in reverse", "<p class='small'>Undo + and − first, then × and ÷.</p>"),
             ("Then plug in", "<p class='small'>Put the numbers in after you solve for the letter.</p>")]},
  ref=["<b>Standard → slope-intercept:</b> subtract the x-term, then divide every term by the number with y.",
       "<b>Point-slope → slope-intercept:</b> distribute, then add or subtract to get y alone.",
       "<b>Intercepts:</b> x-intercept: put 0 in for y. y-intercept: put 0 in for x.",
       "<b>Solve a formula for a letter:</b> undo everything around that letter, doing the same to both sides."],
  cans=["rewrite a line in slope-intercept form", "solve a formula for one letter"],
  steps=["Circle the letter you want alone.", "Distribute if there are parentheses.", "Add or subtract to move other terms.", "Divide every term by the number with your letter.", "Check by substituting."],
  skills={1: [("Standard form → slope-intercept", ("6x + 2y = 8", ["Subtract 6x: 2y = −6x + 8", "Divide every term by 2"], "y = −3x + 4"),
               ("4x + 2y = 6", ["Subtract 4x: 2y = ___", "Divide every term by 2: y = ___"], "y = −2x + 3"),
               ("3x + y = 5", "y = −3x + 5")),
              ("Point-slope → slope-intercept", ("y − 2 = 4(x + 1)", ["Distribute: y − 2 = 4x + 4", "Add 2"], "y = 4x + 6"),
               ("y − 1 = 2(x + 3)", ["Distribute: y − 1 = ___", "Add 1: y = ___"], "y = 2x + 7"),
               ("y + 3 = 5(x − 1)", "y = 5x − 8"))],
          2: [("Solve a formula", ("V = Bh for h", ["h is multiplied by B", "Divide both sides by B"], "h = V/B"),
               ("A = ℓw for ℓ", ["ℓ is multiplied by ___", "Divide both sides by ___"], "ℓ = A/w"),
               ("d = rt for t", "t = d/r")),
              ("Use the formula", ("V = Bh, V = 450, B = 75", ["h = V/B", "h = 450 ÷ 75"], "h = 6"),
               ("A = ℓw, A = 36, w = 4", ["ℓ = A ÷ ___", "ℓ = 36 ÷ 4 = ___"], "ℓ = 9"),
               ("d = rt, d = 120, r = 40", "t = 3"))]}),
 3: dict(
  vocab=V(("Linear inequality", "A comparison with <, ≤, >, or ≥ instead of =.", "3.75b + 25 ≥ 1100"),
          ("At least / no less than", "This much or more: ≥.", "at least 5 → x ≥ 5"),
          ("At most / no more than", "This much or less: ≤.", "at most 5 → x ≤ 5"),
          ("Open circle ○", "The number is NOT included: < or >.", "x > 2"),
          ("Closed circle ●", "The number IS included: ≤ or ≥.", "x ≥ 2"),
          ("Flip the sign", "Multiply or divide by a negative → reverse the sign.", "−2x < 6 → x > −3")),
  plans={1: ["Bell work (5 min)", "Getting Started: Elijah's popcorn function", "Activity 3.1: read inequalities from a graph", "Exit ticket"],
         2: ["Bell work (5 min)", "Activity 3.2: solve two-step inequalities", "Activity 3.3: when the sign flips", "Exit ticket"],
         3: ["Bell work (5 min)", "Activity 3.4: variables on both sides, distributing", "Talk the Talk", "Exit ticket"]},
  notes={1: [("Words → symbols", "<p class='small'>at least ≥ · at most ≤ · more than > · fewer than <</p>"),
             ("Circles", "<p class='small'>○ for < and >.<br>● for ≤ and ≥.</p>"),
             ("Shade", "<p class='small'>x > or x ≥: shade right.<br>x < or x ≤: shade left.</p>")],
         2: [("Solve like an equation", "<p class='small'>Undo + and −, then × and ÷.</p>"),
             ("Flip!", "<p class='small'>Multiply or divide by a negative → reverse the sign.</p>"),
             ("Round in context", "<p class='small'>At least → round up. At most → round down.</p>")],
         3: [("Both sides", "<p class='small'>Move x to the side with the bigger number in front: no flip needed.</p>"),
             ("Distribute first", "<p class='small'>−2(x + 1) = −2x − 2</p>"),
             ("Read it from x", "<p class='small'>−6 ≤ x is the same as x ≥ −6.</p>")]},
  ref=["<b>Words:</b> at least ≥ · at most ≤ · more than > · fewer than <.",
       "<b>Solve like an equation:</b> undo + and −, then × and ÷.",
       "<b>Flip the sign</b> when you multiply or divide both sides by a negative number.",
       "<b>Graph:</b> ○ for < and >, ● for ≤ and ≥. Shade right for > and ≥, left for < and ≤."],
  cans=["write an inequality from words", "solve an inequality and flip the sign when I divide by a negative", "graph the answer on a number line"],
  steps=["Write the inequality (match the words to the symbol).", "Distribute if there are parentheses.", "Move x-terms to one side.", "Undo + or −.",
         "Undo × or ÷. Negative number? FLIP the sign.", "Graph: ○ or ●, then shade."],
  skills={1: [("Words to inequalities", ("Sales of at least $1100: 3.75b + 25 ___ 1100", ["At least = this much or more", "Symbol ≥"], "3.75b + 25 ≥ 1100"),
               ("Sales of at most $700: 3.75b + 25 ___ 700", ["At most = this much or ___", "Symbol ___"], "3.75b + 25 ≤ 700"),
               ("More than $500: 3.75b + 25 ___ 500", "3.75b + 25 > 500")),
              ("Graph on a number line", ("x ≥ 4", ["≥ includes 4: closed ●", "Greater: shade right"], "● at 4, shade right"),
               ("x < 2", ["< does not include 2: ___ circle", "Less: shade ___"], "○ at 2, shade left"),
               ("x ≤ −1", "● at −1, shade left"))],
          2: [("Solve two-step inequalities", ("2x + 5 > 11", ["Subtract 5: 2x > 6", "Divide by 2 (positive: no flip)"], "x > 3"),
               ("3x − 4 ≤ 8", ["Add 4: 3x ≤ ___", "Divide by 3: x ≤ ___"], "x ≤ 4"),
               ("4x + 1 ≥ 9", "x ≥ 2")),
              ("Flip when dividing by a negative", ("−2x < 6", ["Divide by −2", "Negative: FLIP < to >"], "x > −3"),
               ("−3x ≥ 12", ["Divide by ___", "Flip ≥ to ___: x ___ −4"], "x ≤ −4"),
               ("5 − x > 7", "x < −2"))],
          3: [("Variables on both sides", ("5x + 2 ≥ 3x − 10", ["Subtract 3x: 2x + 2 ≥ −10", "Subtract 2: 2x ≥ −12", "Divide by 2"], "x ≥ −6"),
               ("4x − 1 < 2x + 7", ["Subtract 2x: ___ − 1 < 7", "Add 1: 2x < ___", "Divide by 2: x < ___"], "x < 4"),
               ("6x + 3 ≤ 4x + 9", "x ≤ 3")),
              ("Distribute first", ("−2(x + 1) ≥ 8", ["Distribute: −2x − 2 ≥ 8", "Add 2: −2x ≥ 10", "Divide by −2: FLIP"], "x ≤ −5"),
               ("3(x − 2) < 9", ["Distribute: ___ < 9", "Add 6: 3x < ___", "Divide by 3: x < ___"], "x < 5"),
               ("−4(x − 6) < 22", "x > ½"))]}),
}


# ================================================================ Section 504 and IEP decks
def deck_504(n, days):
    a, out = ACC[n], []
    for d, slides in enumerate(days, 1):
        for s in slides:
            if "Day 1 · Exit Ticket" in s or f"Day {d} · Exit Ticket" in s:
                out.append(s)
                out.append(sec(f"Day {d} · Notes to Keep", f"Notes to keep: Day {d}", A.notes_cards(*a["notes"][d]),
                               "Section 504 support: a copy of the day's notes. Hand out a printed copy if the student's plan lists copies of notes."))
                continue
            out.append(s)
            if "Today you will" in s:
                out.append(sec(f"Lesson {n} · Key Vocabulary", "Key vocabulary", a["vocab"],
                               "Section 504 support: preview the key terms before the lesson. Leave this slide up or print it as a reference card."))
            if re.search(r"Day \d · Bell Work", s):
                out.append(sec(f"Day {d} · Today's Plan", "Today's plan", A.checklist(*a["plans"][d]),
                               "Section 504 support: chunked directions. Check off each part as the class finishes it."))
    out[0] = out[0].replace('<p style="font-size:24px;margin-top:6px">Bell work:', '<p style="font-size:24px;margin-top:6px"><b>Section 504 Version</b></p>\n  <p style="font-size:24px;margin-top:6px">Bell work:', 1)
    return out


def iep_bell(n, d):
    cards = [f'<div class="card" style="padding:10px 18px;gap:4px"><p class="small"><b>{k}.</b> {A.mt(q["q"])}</p>'
             f'<p class="small" style="color:var(--point)"><b>Formula:</b> {A.mt(q["formula"])}</p>'
             f'<div class="step pop ans" style="font-size:19px;line-height:1.35;padding:6px 14px"><b>{A.mt(q["choices"][0])}</b>'
             + "".join(f"<br><b>{j}.</b> {A.mt(t)}" for j, t in enumerate(q["steps"], 1)) + "</div></div>" for k, q in enumerate(BELL[n, d], 1)]
    return sec(f"Day {d} · Bell Work · Review", "Warm up: work these on your own", row("".join(cards[:2]), "".join(cards[2:]), gap=24),
               f"Same 4 questions as the online IEP Day {d} bell work (3 answer choices there). Click to reveal one answer at a time; read each step aloud.")


def iep_skill(d, title, ido, wedo, youdo):
    prob, steps, a = ido
    s1 = sec(f"Day {d} · I do · {title}", "Watch: " + prob, A.steps(*steps) + A.ans(a, False),
             "I do: model every step aloud. Students copy the steps into their notes.")
    prob, frames, a = wedo
    s2 = sec(f"Day {d} · We do · {title}", "Together: " + prob, "".join(f'<p class="step">{f}</p>' for f in frames) + A.ans(a, False),
             "We do: students fill in each blank on whiteboards before you click. Use the sentence frames.")
    prob, a = youdo
    s3 = sec(f"Day {d} · You do · {title}", "Your turn: " + prob, '<p class="muted">Use the steps chart. Then check.</p>' + A.ans(a, False),
             "You do: give 2–3 minutes, then reveal. Students fix mistakes in a different color.")
    return [s1, s2, s3]


def iep_exit(n, d):
    items = EXIT[n, d][:3]
    cards = []
    for k, it in enumerate(items, 1):
        extra = ("".join(f'<p class="step small">{f}</p>' for f in it.get("frames", [])[:3]) if it["kind"] == "open"
                 else '<p class="small">' + " · ".join(A.mt(c) for c in it["choices"][:3]) + "</p>")
        cards.append(f'<div class="card"><p>{k}. {A.mt(it["short"])}</p><p class="small muted">Tip: {it["tip"]}</p>{extra}{A.ans(A.mt(it["answer"]))}</div>')
    return sec(f"Day {d} · Exit Ticket", "Show what you know", row(*cards, gap=18),
               f"IEP exit ticket: the first 3 items of the printed exit ticket (EXIT TICKET/T1-Exit-Ticket-{DATES[n, d]}-IEP.pdf), with a tip, "
               "3 answer choices on multiple choice, and step frames. Students may use the steps chart and notes.")


def deck_iep(n):
    a, info = ACC[n], LESSONS[n]
    days = len(a["plans"])
    bw = " · ".join(f'<b><a class="go" href="{bell_href(n, d)[:-5]}-IEP.html" {GO}>Day {d} →</a></b>' for d in range(1, days + 1))
    out = [f'<section class="slide">\n  <p class="eyebrow">Bluebonnet Algebra I · Module 3 · Topic 1 · Lesson {n} · IEP Version</p>\n'
           f'  <h1 style="margin-top:10px;font-size:60px">{info["name"]}</h1>\n  <h3 style="margin-top:8px">I can…</h3>'
           + "".join(f"<p>✓ &nbsp;{c}</p>" for c in a["cans"]) + f'\n  <p style="font-size:24px;margin-top:6px">Bell work: {bw}</p>\n'
           '  <p class="foot">Based on Bluebonnet Learning Secondary Mathematics, Algebra I (©2024–2025 Texas Education Agency, portions ©2021 Carnegie Learning, Inc.), licensed CC BY-NC 4.0. A private site for Algebra I teachers.</p>\n'
           f'  <aside class="notes">IEP version of Lesson {n}: a modified lesson that keeps the core skills (the starred activities) and cuts the number of items. '
           "Each skill follows I do, We do (sentence frames), You do. Apply each student's IEP accommodations too: extended time, read-aloud, breaks, calculator, small group.</aside>\n</section>\n"]
    out.append(sec(f"Lesson {n} · Key Vocabulary", "Key vocabulary", a["vocab"], "Preview the key terms. Leave up or print as a reference card."))
    chart = sec(f"Lesson {n} · Steps Chart", "Steps to follow", A.steps(*a["steps"]), "Anchor chart: students keep this out for every problem.")
    for d in range(1, days + 1):
        out.append(iep_bell(n, d))
        out.append(chart)
        for title, ido, wedo, youdo in a["skills"][d]:
            out += [s.replace(f"Day {d} · I do", f"Day {d} · I do · {D.ESSENTIAL}", 1) for s in iep_skill(d, title, ido, wedo, youdo)]
        out.append(iep_exit(n, d))
        out.append(sec(f"Day {d} · Notes to Keep", f"Notes to keep: Day {d}", A.notes_cards(*a["notes"][d]), "Give a printed copy of the notes."))
    return out


# ================================================================ online bell work (general, 504, IEP)
def bell_pages(n, d):
    name = f"m3t1-lesson{n}-bellwork-day{d}.html"
    qs = [{k: q[k] for k in ("q", "choices", "why")} | ({"letters": "FGHJ"} if i % 2 else {}) for i, q in enumerate(BELL[n, d])]
    MP.OUT = OUT
    MP.page(name, f"Topic 1 Lesson {n} Day {d} Bell Work · {LESSONS[n]['name']}", f"Module 3 · Topic 1 · Lesson {n} · Day {d} Bell Work", "Bell Work: Review",
            "Warm up while attendance is taken. Answer all 4 questions, then submit to see which ones you got right.", "quiz", qs)
    s = (OUT / name).read_text(encoding="utf-8")
    for kind in ("504", "IEP"):
        accom = {"readAloud": True}
        if kind == "IEP":
            accom["choices"] = 3
            accom["add"] = [{"extra": f'<p class="formula" style="margin:8px 0 2px;padding:6px 12px;border-left:4px solid #2f6fdd;background:rgba(47,111,221,.08);'
                                      f'border-radius:4px"><b>Formula:</b> {A.mt(q["formula"])}</p>',
                             "why": "Here is how:" + "".join(f"<br><b>{j}.</b> {t}" for j, t in enumerate(q["steps"], 1))} for q in BELL[n, d]]
        ref = f'<div class="card ref"><p>{A.HELP[kind]}</p>' + "".join(f"<p>{r}</p>" for r in ACC[n]["ref"]) + "</div>"
        t = s.replace("</title>", f" · {LABEL[kind]}</title>", 1).replace('<div class="wrap">', '<div class="wrap big">', 1)
        t = re.sub(r'(<p class="eyebrow">.*?)</p>', lambda m: f"{m.group(1)} · {LABEL[kind]} Version</p>", t, count=1)
        t = re.sub(r'(<p class="muted">.*?</p>)', lambda m: m.group(1) + "\n  " + ref, t, count=1)
        t = t.replace('</script>\n<script src="../mc.js">', f'window.MC.accom = {json.dumps(accom, ensure_ascii=False)};\n</script>\n<script src="../mc.js">')
        assert "window.MC.accom" in t
        (FOLDER[kind] / f"{name[:-5]}-{kind}.html").write_text(t, encoding="utf-8")


# ================================================================ printable bell work + exit ticket (general / 504 / IEP, each with key)
CSS = """@page{size:letter;margin:.5in}body{font-family:Lato,Segoe UI,Arial,sans-serif;font-size:12pt;color:#111;margin:0}
.top{background:#e6f1ea;padding:6px 10px;font-size:15pt}.top b{color:#0b6b3a;font-size:10pt;letter-spacing:.5px}
.hdr{display:flex;justify-content:space-between;font-size:9pt;color:#444;margin-bottom:4px}
.nm{margin:10px 0 12px}.grid{display:grid;grid-template-columns:1fr 1fr;gap:0 26px}.one{display:block}
.it{min-height:3.1in;break-inside:avoid;padding-top:6px}.it.mc{min-height:2.4in}.ch{margin:8px 0 0 18px}.ch div{margin:7px 0}
.big{font-size:15pt}.big .it{min-height:4.3in}.big .it.mc{min-height:3.4in}
.tip{border-left:5px solid #2f6fdd;background:#eef3fc;padding:5px 10px;margin:8px 0;font-size:11.5pt}
.ref{border:1.5px solid #2f6fdd;border-radius:6px;padding:6px 12px;margin-bottom:10px;font-size:11pt}.ref p{margin:3px 0}
.fr{margin:12px 0 0 10px;line-height:2.1}.ans{color:#b00000;font-weight:600}.why{color:#b00000;font-size:10pt;margin-top:6px}i{font-family:'STIX Two Text',serif}"""


def plain(s):
    return re.sub(r"\[\[(.+?)\]\]", lambda m: M(m.group(1)), s)


def sheet(fname, what, n, items, key, kind=None):
    """items: dicts with num, q, choices (print order) or None, letters, answer, why, tip, frames"""
    blocks = []
    for it in items:
        ch = it["choices"]
        if ch and kind == "IEP":  # 3 choices: drop the last distractor, keep the correct one
            ch = [c for c in ch if c == it["answer"]] + [c for c in ch if c != it["answer"]][:2]
            ch = sorted(ch, key=lambda c: it["choices"].index(c))
        b = f'<div class="it{" mc" if ch else ""}"><b>{it["num"]}.</b> {plain(it["q"])}'
        if kind == "IEP" and it.get("tip"):
            b += f'<div class="tip"><b>Tip:</b> {it["tip"]}</div>'
        if ch:
            b += '<div class="ch">' + "".join(f'<div><b>{it["letters"][k]}.</b> <span class="{"ans" if key and c == it["answer"] else ""}">{plain(c)}</span></div>'
                                              for k, c in enumerate(ch)) + "</div>"
        else:
            if kind == "IEP" and it.get("frames"):
                b += '<div class="fr">' + "<br>".join(it["frames"]) + "</div>"
            if key:
                b += f'<div class="ans" style="margin-top:8px">{plain(it["answer"])}</div>'
        if key and it.get("why"):
            b += f'<div class="why">{plain(it["why"])}</div>'
        blocks.append(b + "</div>")
    lab = f" · {LABEL[kind].upper()} VERSION" if kind else ""
    ref = (f'<div class="ref"><b>Reminders</b>' + "".join(f"<p>{r}</p>" for r in ACC[n]["ref"]) + "</div>") if kind else ""
    html = (f'<!doctype html><html><head><meta charset="utf-8"><title>{fname}</title><style>{CSS}</style></head><body>'
            f'<div class="hdr"><span>MODULE 3 • TOPIC 1 • LESSON {n} • {what.upper()}{lab}</span><span>{"ANSWER KEY" if key else ""}</span></div>'
            f'<div class="top"><b>TOPIC 1</b> Linear Equations and Inequalities</div>'
            f'<div class="nm">Name ____________________________ &nbsp; Date __________</div>{ref}'
            f'<div class="{"one big" if kind else "grid"}">{"".join(blocks)}</div></body></html>')
    src = OUT / what / f"{fname}.html"
    src.parent.mkdir(exist_ok=True)
    src.write_text(html, encoding="utf-8")
    subprocess.run([EDGE, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={src.with_suffix('.pdf')}", src.as_uri()],
                   check=True, capture_output=True)
    src.unlink()


def print_order(choices, pos):
    rest = choices[1:]
    rest.insert(pos, choices[0])
    return rest


def write_sheets(n, d):
    date = DATES[n, d]
    bell = [dict(num=k, q=q["q"], choices=print_order(q["choices"], (k + d + n) % 4), letters="FGHJ" if k % 2 == 0 else "ABCD",
                 answer=q["choices"][0], why=q["why"], tip=q["formula"], frames=None) for k, q in enumerate(BELL[n, d], 1)]
    ex = [dict(num=k, q=it["q"], choices=print_order(it["choices"], (k + d) % 4) if it["kind"] == "mc" else None,
               letters="FGHJ" if k % 2 == 0 else "ABCD", answer=it["answer"], why=it["work"], tip=it["tip"], frames=it.get("frames"))
          for k, it in enumerate(EXIT[n, d], 1)]
    for kind in (None, "504", "IEP"):
        sfx = f"-{kind}" if kind else ""
        exk = ex[:3] if kind == "IEP" else ex
        for key in (False, True):
            k2 = "-ANSWER-KEY" if key else ""
            sheet(f"T1-Bell-Work-{date}{sfx}{k2}", "BELL WORK", n, bell, key, kind)
            sheet(f"T1-Exit-Ticket-{date}{sfx}{k2}", "EXIT TICKET", n, exk, key, kind)


# ================================================================ video
SCENES = {
 1: [("Solving Linear Equations", [
       ("A solution to an equation is a value for the variable that makes the equation true.", None, None),
       ("Today: solve equations, name the property for each step, and tell whether an equation has one, no, or infinite solutions.", None, None)]),
     ("Build equations from x = 2", [
       ("Start with the simplest equation: x equals 2.", "x = 2", None), ("Add 3 to each side.", "x + 3 = 5", "addition"),
       ("Multiply each side by 4. Every term gets multiplied.", "4x + 12 = 20", "multiplication"), ("Subtract 2x from each side.", "2x + 12 = −2x + 20", "subtraction"),
       ("Each equation still has the solution 2, because we did the same thing to both sides. PAUSE 1", None, None)]),
     ("Solve and justify", [
       ("Solve 0.6 times the quantity 2x plus 1 equals 4x plus 6.2.", "0.6(2x + 1) = 4x + 6.2", None), ("Distribute the 0.6.", "1.2x + 0.6 = 4x + 6.2", "distributive"),
       ("Subtract 4x from both sides.", "−2.8x + 0.6 = 6.2", "subtraction"), ("Subtract 0.6 from both sides.", "−2.8x = 5.6", "subtraction"),
       ("Divide both sides by negative 2.8.", "x = −2", "division"),
       ("Check: 0.6 times negative 3 is negative 1.8, and 4 times negative 2 plus 6.2 is also negative 1.8. PAUSE 1", None, None)]),
     ("Decimals on both sides", [
       ("Here is one like the test: 0.2 times the quantity 5x plus 5 equals negative 3x plus 9.", "0.2(5x + 5) = −3x + 9", None), ("Distribute.", "x + 1 = −3x + 9", "distributive"),
       ("Add 3x to both sides.", "4x + 1 = 9", "addition"), ("Subtract 1.", "4x = 8", "subtraction"), ("Divide by 4. x equals 2. PAUSE 1", "x = 2", "division")]),
     ("One, none, or infinite?", [
       ("Simplify each side first, then compare.", None, None),
       ("One half times the quantity 4x plus 10 equals 2 times the quantity x plus 1, plus 3.", "½(4x + 10) = 2(x + 1) + 3", None),
       ("Both sides become 2x plus 5. They are the same expression, so every value works: infinite solutions.", "2x + 5 = 2x + 5", "infinite"),
       ("3 times the quantity x minus 2, plus 1, equals 3x plus 4.", "3(x − 2) + 1 = 3x + 4", None),
       ("3x minus 5 equals 3x plus 4. Same x term, different constants: that is never true. No solution.", "3x − 5 = 3x + 4", "no solution"),
       ("2x plus 7 equals 5x plus 7. Different x terms, so there is one solution: x equals 0. PAUSE 1", "2x + 7 = 5x + 7 → x = 0", "one solution")]),
     ("Equal areas", [
       ("A triangle has base 10 and height x plus 2. A rectangle is 4 by x plus 8. The areas are equal.", None, None),
       ("Triangle area is one half base times height. Set it equal to the rectangle's area.", "½(10)(x + 2) = 4(x + 8)", None),
       ("Simplify both sides.", "5x + 10 = 4x + 32", "distributive"), ("Subtract 4x and subtract 10.", "x = 22", "subtraction"),
       ("Remember: properties of equality keep both sides balanced, and simplifying first tells you how many solutions to expect. PAUSE 2", None, None)])],
 2: [("Literal Equations", [
       ("A line can be written three ways: slope-intercept, point-slope, and standard form.", "y = mx + b", "slope-intercept"),
       ("Point-slope form shows the slope and a point.", "y − y₁ = m(x − x₁)", "point-slope"),
       ("Standard form has integers A, B, and C.", "Ax + By = C", "standard")]),
     ("Standard form to slope-intercept", [
       ("Rewrite 3x minus 2y equals 8 in slope-intercept form.", "3x − 2y = 8", None), ("Subtract 3x from both sides.", "−2y = −3x + 8", "subtraction"),
       ("Divide every term by negative 2.", "y = 3/2 x − 4", "division"),
       ("The slope is 3 halves and the y-intercept is 0, negative 4. For the x-intercept, put 0 in for y: x is 8 thirds. PAUSE 1", "(0, −4) and (8/3, 0)", "intercepts")]),
     ("Point-slope to slope-intercept", [
       ("Rewrite y minus 2 equals 5 times the quantity x minus 7.", "y − 2 = 5(x − 7)", None), ("Distribute the 5.", "y − 2 = 5x − 35", "distributive"),
       ("Add 2 to both sides. y equals 5x minus 33. PAUSE 1", "y = 5x − 33", "addition")]),
     ("Solve a formula for a letter", [
       ("A literal equation is a formula where the letters stand for measures. Here is Celsius from Fahrenheit.", "C = 5/9(F − 32)", None),
       ("To get F alone, multiply both sides by 9 fifths.", "9/5 C = F − 32", "multiplication"), ("Add 32 to both sides.", "F = 9/5 C + 32", "addition"),
       ("Now 30 degrees Celsius is 9 fifths times 30, plus 32, which is 86 degrees Fahrenheit. PAUSE 1", "F = 9/5(30) + 32 = 86", None)]),
     ("Height from a formula", [
       ("The lateral area of a can is S equals 2 pi r h. Solve for h.", "S = 2πrh", None), ("h is multiplied by 2 pi r, so divide both sides by 2 pi r.", "h = S/(2πr)", "division"),
       ("If S is 37.68 and r is 1.5, then h is 37.68 divided by 9.42, which is 4 inches.", "h = 37.68 ÷ 9.42 = 4", None),
       ("Remember: to solve for one letter, undo everything around it, doing the same thing to both sides. PAUSE 2", None, None)])],
 3: [("Modeling Linear Inequalities", [
       ("An inequality compares with less than, less than or equal, greater than, or greater than or equal.", None, None),
       ("At least means greater than or equal. At most means less than or equal.", "at least ≥   ·   at most ≤", None)]),
     ("Elijah's popcorn", [
       ("Elijah starts with a 25 dollar credit and earns 3.75 dollars per box.", "f(b) = 3.75b + 25", None),
       ("He needs at least 1100 dollars. Write an inequality.", "3.75b + 25 ≥ 1100", "at least"), ("Subtract 25.", "3.75b ≥ 1075", "subtraction"),
       ("Divide by 3.75. b is at least 286.67.", "b ≥ 286.67", "division"),
       ("He can't sell part of a box, so he needs at least 287 boxes. PAUSE 1", {"nl": (287, True, True)}, None)]),
     ("When the sign flips", [
       ("The troop hikes down from 4800 feet at 20 feet per minute.", "h(m) = −20m + 4800", None),
       ("When are they below 3200 feet?", "−20m + 4800 < 3200", None), ("Subtract 4800.", "−20m < −1600", "subtraction"),
       ("Divide by negative 20. Dividing by a negative reverses the sign, so less than becomes greater than.", "m > 80", "flip!"),
       ("After more than 80 minutes. Open circle, because 80 itself is not included. PAUSE 1", {"nl": (80, False, True)}, None)]),
     ("Variables on both sides", [
       ("Solve 5x plus 2 is greater than or equal to 3x minus 10.", "5x + 2 ≥ 3x − 10", None), ("Subtract 3x from both sides.", "2x + 2 ≥ −10", "subtraction"),
       ("Subtract 2.", "2x ≥ −12", "subtraction"), ("Divide by positive 2. No flip.", "x ≥ −6", "division"),
       ("Closed circle at negative 6, shaded to the right. PAUSE 1", {"nl": (-6, True, True)}, None)]),
     ("Distribute first", [
       ("Solve negative 2 times the quantity x plus 1 is greater than or equal to 8.", "−2(x + 1) ≥ 8", None), ("Distribute.", "−2x − 2 ≥ 8", "distributive"),
       ("Add 2.", "−2x ≥ 10", "addition"), ("Divide by negative 2 and flip the sign.", "x ≤ −5", "flip!"),
       ("Closed circle at negative 5, shaded left. Remember: solve like an equation, and flip when you multiply or divide by a negative. PAUSE 2", {"nl": (-5, True, False)}, None)])],
}
VIDEO_NAMES = {1: "M3T1-Lesson1-Solving-Linear-Equations.mp4", 2: "M3T1-Lesson2-Literal-Equations.mp4", 3: "M3T1-Lesson3-Linear-Inequalities.mp4"}


def write_video(n):
    import make_t2_video as Vd
    from PIL import Image, ImageDraw
    out_dir = OUT / "videos"
    out_dir.mkdir(exist_ok=True)
    out = out_dir / VIDEO_NAMES[n]
    tmp = tempfile.mkdtemp()
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{Vd.W}x{Vd.H}", "-r", str(Vd.FPS),
                           "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "26", os.path.join(tmp, "v.mp4")], stdin=subprocess.PIPE)
    wavs, k = [], 0
    for title, steps in SCENES[n]:
        lines, nl = [], None
        for cap, line, why in steps:
            if isinstance(line, dict):
                nl = line["nl"]
            elif line:
                lines.append((line, why))
            img = Image.new("RGB", (Vd.W, Vd.H), "white")
            d = ImageDraw.Draw(img)
            d.rectangle([0, 0, Vd.W, 84], fill="#e6f1ea")
            d.text((40, 20), title, font=Vd.FB[44], fill="#0b6b3a")
            y = 110
            shown = lines[-7:]
            for j, (ln, rs) in enumerate(shown):
                new = j == len(shown) - 1 and isinstance(line, str)
                d.text((80, y), ln, font=Vd.FB[44] if new else Vd.F[34], fill=Vd.BLUE if new else Vd.INK)
                if rs: d.text((760, y + 6), rs, font=Vd.F[34], fill=Vd.RED if rs == "flip!" else Vd.GREEN)
                y += 56
            if nl:  # number line: 11 ticks centered on the boundary value, ponytail: fixed span, no scale choice
                v, closed, right = nl
                x0, x1, ly = 140, 1140, 520
                d.line([x0, ly, x1, ly], fill=Vd.INK, width=3)
                step = max(1, round(abs(v) / 25) * 5) if abs(v) > 20 else 1
                for t in range(-5, 6):
                    tx = (x0 + x1) / 2 + t * (x1 - x0) / 12
                    d.line([tx, ly - 10, tx, ly + 10], fill=Vd.INK, width=2)
                    d.text((tx - 18, ly + 14), str(v + t * step), font=Vd.F[26], fill=Vd.MUTED)
                cx = (x0 + x1) / 2
                d.line([cx, ly, x1 if right else x0, ly], fill=Vd.BLUE, width=9)
                d.ellipse([cx - 13, ly - 13, cx + 13, ly + 13], fill=Vd.BLUE if closed else "white", outline=Vd.BLUE, width=4)
            d.rectangle([0, Vd.H - 130, Vd.W, Vd.H], fill="#f4f6fa")
            for j, w in enumerate(Vd.wrap(d, re.sub(r"\s*PAUSE \d+", "", cap), Vd.F[34], Vd.W - 120)[:3]):
                d.text((60, Vd.H - 118 + j * 38), w, font=Vd.F[34], fill=Vd.INK)
            wav = os.path.join(tmp, f"s{k:03d}.mp3"); k += 1
            say = Vd.spoken(cap).replace("≥", " greater than or equal to ").replace("≤", " less than or equal to ")
            dur = Vd.speak(say, wav) + 0.6
            m = re.search(r"PAUSE (\d+)", cap)
            nf = round((dur + (float(m.group(1)) if m else 0)) * Vd.FPS)
            wavs.append((wav, nf / Vd.FPS))
            ff.stdin.write(img.tobytes() * nf)
    ff.stdin.close(); ff.wait()
    lst = os.path.join(tmp, "a.txt")
    with open(lst, "w") as fh:
        for i, (wav, slot) in enumerate(wavs):
            pad = os.path.join(tmp, f"p{i:03d}.wav")
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-af", f"apad=whole_dur={slot:.3f}", "-ar", "22050", "-ac", "1", pad], check=True)
            fh.write(f"file '{pad}'\n")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(tmp, "v.mp4"), "-f", "concat", "-safe", "0", "-i", lst,
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "96k", "-shortest", "-movflags", "+faststart", str(out)], check=True)
    print(out.name, f"{sum(s for _, s in wavs):.0f} s")


# ================================================================ main
def build(n):
    info = LESSONS[n]
    days = info["deck"]()
    general = [D.star_eyebrows(f"m3l{n}", s) for day in days for s in day]
    path = OUT / f"{info['stem']}.html"
    path.write_text(doc(f"{info['name']} · Bluebonnet Algebra I", general), encoding="utf-8")
    print(path.name, len(general), "slides"); pptx(path)
    starred_days = [[D.star_eyebrows(f"m3l{n}", s) for s in day] for day in days]
    link = lambda kind, h: re.sub(r'href="(m3t1-lesson\d-bellwork-day\d)\.html"', rf'href="\1-{kind}.html"', h)
    for kind, slides in (("504", deck_504(n, starred_days)), ("IEP", deck_iep(n))):
        p_ = FOLDER[kind] / f"{info['stem']}-{kind}.html"
        p_.write_text(link(kind, doc(f"{info['name']} · Bluebonnet Algebra I · {LABEL[kind]}", slides)), encoding="utf-8")
        print(p_.name, len(slides), "slides"); pptx(p_)
    for d in range(1, len(days) + 1):
        bell_pages(n, d)
        write_sheets(n, d)


if __name__ == "__main__":
    for key, qs in BELL.items():
        for q in qs:
            assert len(set(q["choices"])) == 4, q["q"]
    for key, items in EXIT.items():
        for it in items:
            assert it["kind"] == "open" or len(set(it["choices"])) == 4, it["q"]
    assert all(len(ACC[n]["plans"]) == len(LESSONS[n]["deck"]()) for n in LESSONS)
    for n in [int(a) for a in sys.argv[1:] if a.isdigit()] or LESSONS:
        build(n)
        if "video" in sys.argv:
            write_video(n)

"""Module 3 Topic 2 bell work and exit tickets, one of each per class day (12 days), each in General, Section 504 and IEP
versions: online bell work pages (4 questions, scored), printable PDFs with answer keys, and the deck slides.
New skill-based items, not copies of the End of Topic 2 assessment. Dates follow the district pacing calendar (AHS).
Built by make_m3t2_lessons.py.  Lock the keys afterwards: python lock_keys.py (BELL WORK / EXIT TICKET use DAILY_PW)."""
import json, re, subprocess
from pathlib import Path

import make_t2_decks as D
import make_t2_practice as MP
import make_accom_lessons as A
from make_m3t1_lessons import bq, mc, op, CSS, plain, print_order, EDGE

ROOT = Path(__file__).parent
OUT = ROOT / "Module 3 topic 2"
FOLDER = {"504": ROOT / "Section 504", "IEP": ROOT / "IEP"}
LABEL = {"504": "Section 504", "IEP": "IEP"}
mt, ans, sec, row = D.mt, D.ans, D.sec, D.row

DATES = {(1, 1): "Mon-11-30", (1, 2): "Tue-12-01", (2, 1): "Wed-12-02", (2, 2): "Thu-12-03", (3, 1): "Mon-12-07", (3, 2): "Tue-12-08",
         (3, 3): "Wed-12-09", (4, 1): "Mon-01-04", (4, 2): "Tue-01-05", (5, 1): "Wed-01-06", (5, 2): "Thu-01-07", (5, 3): "Mon-01-11"}

REF = {
 1: ["<b>Intercepts:</b> set y = 0 to find the x-intercept; set x = 0 to find the y-intercept.",
     "<b>Solution of a system:</b> the point where the lines cross. It makes both equations true.",
     "<b>How many?</b> Different slopes: one. Same slope, different y-intercept: none. Same line: infinite."],
 2: ["<b>Substitution:</b> get a variable alone, put its expression into the other equation, solve, substitute back.",
     "<b>Variable drops out?</b> False statement (like 0 = 7): no solution. True statement (like 5 = 5): infinite.",
     "<b>Check:</b> put both values into both equations."],
 3: ["<b>Linear combinations:</b> make one variable's coefficients opposites, then add the equations.",
     "<b>Multiply every term</b>, including the number on the right side.",
     "<b>Fractions:</b> multiply by the LCD first. Variable alone? Substitution is faster."],
 4: ["<b>Boundary:</b> solid for ≤ or ≥, dashed for &lt; or &gt;.",
     "<b>Test (0, 0):</b> true → shade its side; false → shade the other side.",
     "<b>Words:</b> at least ≥ · at most ≤ · more than &gt; · less than &lt;."],
 5: ["<b>System of inequalities:</b> graph and shade each one; the overlap is the solution set.",
     "<b>A solution</b> makes EVERY inequality true. Points on a dashed line are not solutions.",
     "<b>In a story:</b> no negative amounts, so stay in the first quadrant."],
}

BELL = {
 (1, 1): [
  bq("What is the [[x]]-intercept of [[2x + 5y = 20]]?", ["[[(10, 0)]]", "[[(0, 4)]]", "[[(4, 0)]]", "[[(20, 0)]]"],
     "Set [[y = 0]]: [[2x = 20]], so [[x = 10]].", "x-intercept: set [[y = 0]]", ["Set [[y = 0]]: [[2x + 0 = 20]].", "Divide by 2: [[x = 10]].", "Point: [[(10, 0)]]."]),
  bq("What is the [[y]]-intercept of [[3x + 4y = 24]]?", ["[[(0, 6)]]", "[[(8, 0)]]", "[[(0, 8)]]", "[[(6, 0)]]"],
     "Set [[x = 0]]: [[4y = 24]], so [[y = 6]].", "y-intercept: set [[x = 0]]", ["Set [[x = 0]]: [[4y = 24]].", "Divide by 4: [[y = 6]].", "Point: [[(0, 6)]]."]),
  bq("Is [[(2, 3)]] a solution of [[y = 2x − 1]]?", ["Yes, because [[3 = 3]]", "No, because [[3 ≠ 5]]", "Yes, because [[2 = 2]]", "No, because [[3 ≠ 1]]"],
     "[[2(2) − 1 = 3]], and [[y = 3]]. True, so yes.", "put [[x]] and [[y]] in", ["[[x = 2]]: [[2(2) − 1 = 3]].", "[[y]] is 3.", "[[3 = 3]] is true: yes."]),
  bq("What is the slope of [[y = −½x + 4]]?", ["[[−½]]", "[[4]]", "[[½]]", "[[−2]]"],
     "In [[y = mx + b]], [[m]] is the slope: [[−½]].", "[[y = mx + b]]: [[m]] is the slope", ["Match [[y = mx + b]].", "[[m = −½]]."])],
 (1, 2): [
  bq("Which point is the solution of [[y = 2x]] and [[y = x + 3]]?", ["[[(3, 6)]]", "[[(6, 3)]]", "[[(1, 2)]]", "[[(0, 3)]]"],
     "[[(3, 6)]]: [[6 = 2(3)]] and [[6 = 3 + 3]].", "the solution makes both equations true", ["Try [[(3, 6)]] in [[y = 2x]]: [[6 = 6]].", "In [[y = x + 3]]: [[6 = 6]].", "Both true."]),
  bq("The graphs of [[y = 3x + 1]] and [[y = 3x − 4]] are…", ["parallel lines", "lines that cross once", "the same line", "perpendicular lines"],
     "Same slope 3, different [[y]]-intercepts: parallel.", "same slope, different [[b]]: parallel", ["Slopes: 3 and 3.", "[[y]]-intercepts: 1 and −4.", "Parallel."]),
  bq("Which point is on the line [[5s + 10a = 3000]]?", ["[[(200, 200)]]", "[[(300, 200)]]", "[[(100, 300)]]", "[[(600, 300)]]"],
     "[[5(200) + 10(200) = 1000 + 2000 = 3000]].", "substitute and check", ["[[5(200) = 1000]].", "[[10(200) = 2000]].", "[[1000 + 2000 = 3000]] ✓."]),
  bq("What are the slope and [[y]]-intercept of [[y = 4x + 40]]?", ["slope 4, [[y]]-intercept 40", "slope 40, [[y]]-intercept 4", "slope 4, [[y]]-intercept −40", "slope −4, [[y]]-intercept 40"],
     "[[y = mx + b]]: [[m = 4]], [[b = 40]].", "[[m]] = slope, [[b]] = [[y]]-intercept", ["[[m = 4]].", "[[b = 40]]."])],
 (2, 1): [
  bq("Which point is the solution of [[y = −x + 4]] and [[y = x − 2]]?", ["[[(3, 1)]]", "[[(1, 3)]]", "[[(4, −2)]]", "[[(2, 2)]]"],
     "[[(3, 1)]]: [[1 = −3 + 4]] and [[1 = 3 − 2]].", "check the point in both", ["[[−3 + 4 = 1]] ✓.", "[[3 − 2 = 1]] ✓."]),
  bq("Solve [[4x + y = 9]] for [[y]].", ["[[y = −4x + 9]]", "[[y = 4x + 9]]", "[[y = 9 − x]]", "[[y = −4x − 9]]"],
     "Subtract [[4x]] from both sides: [[y = −4x + 9]].", "undo [[+ 4x]] by subtracting", ["Subtract [[4x]]: [[y = 9 − 4x]].", "Write as [[y = −4x + 9]]."]),
  bq("What is [[y]] when [[x = 3]] in [[y = 2x − 1]]?", ["[[5]]", "[[7]]", "[[6]]", "[[3]]"],
     "[[2(3) − 1 = 5]].", "substitute 3 for [[x]]", ["[[2(3) = 6]].", "[[6 − 1 = 5]]."]),
  bq("Which system has no solution?", ["[[y = x + 1]] and [[y = x − 3]]", "[[y = x + 1]] and [[y = 2x + 1]]", "[[y = x + 1]] and [[y = −x + 1]]", "[[y = x + 1]] and [[2y = 2x + 2]]"],
     "Same slope 1, different [[y]]-intercepts: parallel lines never meet.", "same slope, different [[b]]: none", ["Look for equal slopes.", "Then different [[y]]-intercepts.", "[[y = x + 1]] and [[y = x − 3]]."])],
 (2, 2): [
  bq("Solve by substitution: [[y = 4x]] and [[2x + y = 18]].", ["[[(3, 12)]]", "[[(12, 3)]]", "[[(2, 8)]]", "[[(3, 4)]]"],
     "[[2x + 4x = 18]], [[x = 3]], [[y = 12]].", "replace [[y]] with [[4x]]", ["[[2x + 4x = 18]].", "[[6x = 18]], [[x = 3]].", "[[y = 4(3) = 12]]."]),
  bq("You substitute and get [[0 = 7]]. How many solutions does the system have?", ["No solution", "One solution", "Infinitely many", "[[x = 7]]"],
     "A false statement means no ordered pair works.", "false statement → no solution", ["[[0 = 7]] is false.", "No solution."]),
  bq("Write [[6x + 2y = 10]] in slope-intercept form.", ["[[y = −3x + 5]]", "[[y = 3x + 5]]", "[[y = −6x + 10]]", "[[y = −3x + 10]]"],
     "[[2y = −6x + 10]], then divide every term by 2.", "get [[y]] alone, divide every term", ["Subtract [[6x]]: [[2y = −6x + 10]].", "Divide every term by 2: [[y = −3x + 5]]."]),
  bq("Which point is a solution of both [[x + y = 10]] and [[x − y = 2]]?", ["[[(6, 4)]]", "[[(4, 6)]]", "[[(5, 5)]]", "[[(8, 2)]]"],
     "[[6 + 4 = 10]] and [[6 − 4 = 2]].", "check both equations", ["[[6 + 4 = 10]] ✓.", "[[6 − 4 = 2]] ✓."])],
 (3, 1): [
  bq("Solve: [[x = y + 2]] and [[x + y = 12]].", ["[[(7, 5)]]", "[[(5, 7)]]", "[[(6, 6)]]", "[[(10, 2)]]"],
     "[[(y + 2) + y = 12]], [[y = 5]], [[x = 7]].", "substitute [[y + 2]] for [[x]]", ["[[2y + 2 = 12]].", "[[y = 5]].", "[[x = 5 + 2 = 7]]."]),
  bq("What is the additive inverse of [[5y]]?", ["[[−5y]]", "[[5y]]", "[[⅕y]]", "[[0]]"],
     "Additive inverses add to zero: [[5y + (−5y) = 0]].", "opposite sign, same term", ["Change the sign.", "[[−5y]]."]),
  bq("Add the equations [[3x + 2y = 7]] and [[x − 2y = 5]]. What do you get?", ["[[4x = 12]]", "[[4x − 4y = 12]]", "[[2x = 2]]", "[[4x + 4y = 12]]"],
     "[[2y]] and [[−2y]] add to 0: [[4x = 12]].", "add like terms down the columns", ["[[3x + x = 4x]].", "[[2y − 2y = 0]].", "[[7 + 5 = 12]]."]),
  bq("Multiply every term of [[2x − y = 3]] by 3.", ["[[6x − 3y = 9]]", "[[6x − y = 3]]", "[[6x − 3y = 3]]", "[[2x − 3y = 9]]"],
     "Every term, including the 3 on the right: [[6x − 3y = 9]].", "multiply EVERY term", ["[[3(2x) = 6x]].", "[[3(−y) = −3y]].", "[[3(3) = 9]]."])],
 (3, 2): [
  bq("Solve: [[x + y = 12]] and [[x − y = 4]].", ["[[(8, 4)]]", "[[(4, 8)]]", "[[(16, −4)]]", "[[(6, 6)]]"],
     "Add: [[2x = 16]], [[x = 8]], [[y = 4]].", "add the equations", ["Add: [[2x = 16]].", "[[x = 8]].", "[[8 + y = 12]], [[y = 4]]."]),
  bq("To eliminate [[y]] in [[3x + y = 7]] and [[2x + 2y = 6]], multiply the first equation by…", ["[[−2]]", "[[2]]", "[[3]]", "[[−3]]"],
     "[[−2y]] and [[2y]] are opposites.", "make the [[y]]-terms opposites", ["The second has [[2y]].", "You need [[−2y]] in the first.", "Multiply by [[−2]]."]),
  bq("Multiply [[4x + y = 15]] by [[−2]].", ["[[−8x − 2y = −30]]", "[[−8x + 2y = −30]]", "[[−8x − 2y = 15]]", "[[8x + 2y = 30]]"],
     "Every term times [[−2]].", "multiply EVERY term", ["[[−2(4x) = −8x]].", "[[−2(y) = −2y]].", "[[−2(15) = −30]]."]),
  bq("Is [[(6, −9)]] a solution of [[4x + y = 15]]?", ["Yes, because [[15 = 15]]", "No, because [[33 ≠ 15]]", "No, because [[6 ≠ −9]]", "Yes, because [[−9 < 15]]"],
     "[[4(6) + (−9) = 24 − 9 = 15]].", "substitute both values", ["[[4(6) = 24]].", "[[24 + (−9) = 15]].", "True: yes."])],
 (3, 3): [
  bq("Solve: [[2x + y = 11]] and [[x − y = 1]].", ["[[(4, 3)]]", "[[(3, 4)]]", "[[(5, 1)]]", "[[(4, −3)]]"],
     "Add: [[3x = 12]], [[x = 4]], [[y = 3]].", "add the equations", ["Add: [[3x = 12]].", "[[x = 4]].", "[[4 − y = 1]], [[y = 3]]."]),
  bq("Multiply [[½x + ¾y = 10]] by 4.", ["[[2x + 3y = 40]]", "[[2x + 3y = 10]]", "[[½x + 3y = 40]]", "[[4x + 3y = 40]]"],
     "The LCD 4 clears both fractions: [[2x + 3y = 40]].", "multiply every term by the LCD", ["[[4(½x) = 2x]].", "[[4(¾y) = 3y]].", "[[4(10) = 40]]."]),
  bq("Which method is fastest for [[y = 3x − 1]] and [[5x − 2y = 4]]?", ["substitution", "linear combinations", "graphing", "none of them works"],
     "[[y]] is already alone, so substitute [[3x − 1]] for [[y]].", "variable alone → substitution", ["Look for a variable alone.", "[[y = 3x − 1]]: substitute."]),
  bq("Is [[(3, 2)]] a solution of [[x + 2y = 7]] and [[3x − y = 7]]?", ["Yes, both are true", "Only the first is true", "Only the second is true", "Neither is true"],
     "[[3 + 4 = 7]] and [[9 − 2 = 7]].", "check both equations", ["[[3 + 2(2) = 7]] ✓.", "[[3(3) − 2 = 7]] ✓."])],
 (4, 1): [
  bq("Is [[(0, 0)]] a solution of [[y > 2x − 5]]?", ["Yes, because [[0 > −5]]", "No, because [[0 < −5]]", "Yes, because [[0 = 0]]", "No, because [[0 > 5]]"],
     "[[0 > 2(0) − 5]] means [[0 > −5]]: true.", "substitute [[(0, 0)]]", ["[[2(0) − 5 = −5]].", "[[0 > −5]] is true."]),
  bq("Solve: [[x + y = 8]] and [[x − y = 2]].", ["[[(5, 3)]]", "[[(3, 5)]]", "[[(6, 2)]]", "[[(4, 4)]]"],
     "Add: [[2x = 10]], [[x = 5]], [[y = 3]].", "add the equations", ["[[2x = 10]].", "[[x = 5]], [[y = 3]]."]),
  bq("Which inequality means “at least 20”?", ["[[x ≥ 20]]", "[[x > 20]]", "[[x ≤ 20]]", "[[x < 20]]"],
     "At least 20: 20 or more, so [[≥]].", "at least → ≥", ["“At least” includes 20.", "[[x ≥ 20]]."]),
  bq("Which describes the graph of [[x < −2]] on a number line?", ["open circle at −2, shade left", "closed circle at −2, shade left", "open circle at −2, shade right", "closed circle at −2, shade right"],
     "&lt; does not include −2 (open) and means smaller (left).", "&lt; or &gt;: open circle", ["&lt;: open circle.", "Less than: shade left."])],
 (4, 2): [
  bq("Is [[(0, 0)]] a solution of [[y ≤ −x + 4]]?", ["Yes, because [[0 ≤ 4]]", "No, because [[0 > 4]]", "No, because [[0 ≤ −4]]", "Yes, because [[0 = 4]]"],
     "[[0 ≤ −0 + 4]] means [[0 ≤ 4]]: true.", "substitute [[(0, 0)]]", ["[[−0 + 4 = 4]].", "[[0 ≤ 4]] is true."]),
  bq("Which symbol gives a dashed boundary line?", ["[[<]]", "[[≤]]", "[[≥]]", "[[=]]"],
     "&lt; and &gt; do not include the line: dashed.", "&lt; or &gt; → dashed", ["≤ and ≥ include the line: solid.", "&lt;: dashed."]),
  bq("Rewrite [[2x − y < 4]] with [[y]] alone.", ["[[y > 2x − 4]]", "[[y < 2x − 4]]", "[[y > −2x + 4]]", "[[y < −2x + 4]]"],
     "[[−y < −2x + 4]]; divide by −1 and flip: [[y > 2x − 4]].", "÷ by a negative → flip", ["Subtract [[2x]]: [[−y < −2x + 4]].", "Divide by −1, flip: [[y > 2x − 4]]."]),
  bq("For [[3x + y > 6]], the points on the line [[3x + y = 6]] are…", ["not solutions", "all solutions", "solutions only at the intercepts", "solutions only above [[(0, 6)]]"],
     "&gt; does not include equal, so points on the line are not solutions.", "&gt; → line not included", ["On the line, [[3x + y = 6]].", "[[6 > 6]] is false."])],
 (5, 1): [
  bq("Is [[(1, 1)]] a solution of [[y > 2x − 3]]?", ["Yes, because [[1 > −1]]", "No, because [[1 < −1]]", "No, because [[1 > 2]]", "Yes, because [[1 = 1]]"],
     "[[2(1) − 3 = −1]], and [[1 > −1]].", "substitute the point", ["[[2(1) − 3 = −1]].", "[[1 > −1]] is true."]),
  bq("Which inequality has a solid boundary line with the half-plane above shaded?", ["[[y ≥ x + 1]]", "[[y > x + 1]]", "[[y ≤ x + 1]]", "[[y < x + 1]]"],
     "Solid: ≥ or ≤. Above: [[y ≥]].", "solid → ≥ or ≤", ["Solid: ≥ or ≤.", "Above: [[y ≥ …]]."]),
  bq("Which point is a solution of [[x + y ≤ 6]]?", ["[[(2, 3)]]", "[[(4, 3)]]", "[[(6, 1)]]", "[[(5, 2)]]"],
     "[[2 + 3 = 5]] and [[5 ≤ 6]].", "add, then compare", ["[[2 + 3 = 5]].", "[[5 ≤ 6]] ✓."]),
  bq("Which inequality means “at most 10 hours”?", ["[[h ≤ 10]]", "[[h ≥ 10]]", "[[h < 10]]", "[[h > 10]]"],
     "At most 10: 10 or less, so ≤.", "at most → ≤", ["“At most” includes 10.", "[[h ≤ 10]]."])],
 (5, 2): [
  bq("Is [[(0, 0)]] a solution of [[x + y > 1]]?", ["No, because [[0 > 1]] is false", "Yes, because [[0 < 1]]", "Yes, because [[0 = 0]]", "No, because [[1 > 0]]"],
     "[[0 + 0 = 0]], and [[0 > 1]] is false.", "substitute [[(0, 0)]]", ["[[0 + 0 = 0]].", "[[0 > 1]] is false: no."]),
  bq("Where is the solution set of [[y > x + 2]] and [[y > x + 5]]?", ["above [[y = x + 5]]", "below [[y = x + 2]]", "between the lines", "no solution"],
     "Above both lines means above the higher one, [[y = x + 5]].", "both &gt; → above both", ["Both say above.", "Above the higher line."]),
  bq("The lines of [[y > −x + 1]] and [[y ≤ x + 3]] cross at [[(−1, 2)]]. Is [[(−1, 2)]] a solution?", ["No, because [[2 > 2]] is false", "Yes, because it is where the lines meet", "Yes, because [[2 ≤ 2]]", "No, because [[2 ≤ 2]] is false"],
     "[[−(−1) + 1 = 2]], and [[2 > 2]] is false: it is on the dashed line.", "check every inequality", ["[[y > −x + 1]]: [[2 > 2]] false.", "One false → not a solution."]),
  bq("[[x + y ≤ 45]] (minutes). Which pair works?", ["[[(20, 25)]]", "[[(30, 20)]]", "[[(45, 1)]]", "[[(50, 0)]]"],
     "[[20 + 25 = 45]] and [[45 ≤ 45]].", "add, then compare", ["[[20 + 25 = 45]].", "[[45 ≤ 45]] ✓."])],
 (5, 3): [
  bq("Where is the solution set of [[y < x + 1]] and [[y < x + 4]]?", ["below [[y = x + 1]]", "below [[y = x + 4]] only", "between the lines", "no solution"],
     "Below both lines means below the lower one, [[y = x + 1]].", "both &lt; → below both", ["Both say below.", "Below the lower line."]),
  bq("Is [[(3, 0)]] a solution of [[y ≥ −x + 2]] and [[y ≤ x − 1]]?", ["Yes, both are true", "Only the first is true", "Only the second is true", "Neither is true"],
     "[[0 ≥ −1]] and [[0 ≤ 2]].", "check every inequality", ["[[0 ≥ −3 + 2 = −1]] ✓.", "[[0 ≤ 3 − 1 = 2]] ✓."]),
  bq("A dashed line [[y = ½x − 1]] has the half-plane below it shaded. Which inequality is it?", ["[[y < ½x − 1]]", "[[y ≤ ½x − 1]]", "[[y > ½x − 1]]", "[[y ≥ ½x − 1]]"],
     "Dashed: &lt; or &gt;. Below: [[y <]].", "dashed + below → &lt;", ["Dashed: &lt; or &gt;.", "Below: [[y < …]]."]),
  bq("Together, [[x ≥ 0]] and [[y ≥ 0]] keep the solutions in which quadrant?", ["Quadrant I", "Quadrant II", "Quadrant III", "Quadrant IV"],
     "[[x]] and [[y]] both 0 or positive: Quadrant I.", "both positive → Quadrant I", ["[[x ≥ 0]]: right side.", "[[y ≥ 0]]: top.", "Quadrant I."])],
}

EXIT = {
 (1, 1): [
  mc("Which point is the solution of the system [[y = x + 2]] and [[y = −x + 6]]?", ["[[(2, 4)]]", "[[(4, 2)]]", "[[(0, 2)]]", "[[(6, 0)]]"],
     "[[4 = 2 + 2]] and [[4 = −2 + 6]]", "Check each point in BOTH equations.", "Solution of [[y = x + 2]], [[y = −x + 6]]?"),
  mc("Student tickets cost $4 and adult tickets cost $8. A club sold 40 tickets for $240. Which system models this?",
     ["[[4s + 8a = 240]] and [[s + a = 40]]", "[[8s + 4a = 240]] and [[s + a = 40]]", "[[4s + 8a = 40]] and [[s + a = 240]]", "[[s + a = 240]] and [[4s = 8a]]"],
     "money: [[4s + 8a = 240]]; tickets: [[s + a = 40]]", "One equation for money, one for the number of tickets.", "System for 40 tickets, $240?"),
  op("Use the intercepts to graph [[3x + 2y = 12]]. Where does the line cross each axis?", "[[(4, 0)]] and [[(0, 6)]]",
     "[[y = 0]]: [[3x = 12]], [[x = 4]]. [[x = 0]]: [[2y = 12]], [[y = 6]]", "Set y = 0, then set x = 0.",
     ["Set y = 0: 3x = ______, x = ______", "Set x = 0: 2y = ______, y = ______", "Intercepts: (____, 0) and (0, ____)"], "Intercepts of [[3x + 2y = 12]]")],
 (1, 2): [
  mc("How many solutions does the system [[y = 2x + 5]] and [[y = 2x − 1]] have?", ["No solution", "One solution", "Infinitely many", "Two solutions"],
     "same slope, different [[y]]-intercepts: parallel", "Compare the slopes, then the y-intercepts.", "How many: [[y = 2x + 5]], [[y = 2x − 1]]?"),
  mc("Which system has infinitely many solutions?", ["[[y = 3x + 2]] and [[2y = 6x + 4]]", "[[y = 3x + 2]] and [[y = 3x − 2]]", "[[y = 3x + 2]] and [[y = −3x + 2]]", "[[y = 3x]] and [[y = 2x]]"],
     "[[2y = 6x + 4]] is [[y = 3x + 2]]: the same line", "Write both in slope-intercept form.", "Which has infinitely many solutions?"),
  op("Maya has $20 and saves $5 a week. Leo also has $20 and saves $5 a week. Write a system and tell how many solutions it has.",
     "[[y = 5x + 20]] and [[y = 5x + 20]]: infinitely many (same line)", "same slope and same [[y]]-intercept", "Start amount is b, weekly amount is m.",
     ["Maya: y = ____x + ____", "Leo: y = ____x + ____", "Same line, so ______ solutions"], "Maya and Leo: how many solutions?")],
 (2, 1): [
  mc("Solve by substitution: [[y = 3x]] and [[x + y = 20]].", ["[[(5, 15)]]", "[[(15, 5)]]", "[[(4, 12)]]", "[[(5, 20)]]"],
     "[[x + 3x = 20]] → [[x = 5]] → [[y = 15]]", "Replace y with 3x.", "Solve: [[y = 3x]], [[x + y = 20]]"),
  mc("Which equation do you get by substituting [[y = 2x − 3]] into [[4x + y = 15]]?", ["[[4x + 2x − 3 = 15]]", "[[4(2x − 3) + y = 15]]", "[[4x + 2x = 15]]", "[[6x + 3 = 15]]"],
     "replace [[y]] with [[2x − 3]]", "Put the whole expression in place of y.", "Substitute [[y = 2x − 3]] into [[4x + y = 15]]"),
  op("Solve by substitution: [[y = x + 4]] and [[3x + y = 24]].", "[[(5, 9)]]", "[[3x + x + 4 = 24]] → [[4x = 20]] → [[x = 5]], [[y = 9]]",
     "Replace y with x + 4.", ["3x + (______) = 24", "4x + 4 = 24, so x = ______", "y = ______ + 4 = ______"], "Solve: [[y = x + 4]], [[3x + y = 24]]")],
 (2, 2): [
  mc("Solve: [[y = 2x + 1]] and [[4x − 2y = −2]].", ["Infinitely many solutions", "No solution", "[[(0, 1)]] only", "[[(1, 3)]] only"],
     "[[4x − 2(2x + 1) = −2]] → [[−2 = −2]], always true", "If the variable drops out, read the statement.", "Solve: [[y = 2x + 1]], [[4x − 2y = −2]]"),
  mc("Floor seats cost $10 more than balcony seats. 300 floor seats and 200 balcony seats bring in $8000. Which system models this?",
     ["[[f = b + 10]] and [[300f + 200b = 8000]]", "[[b = f + 10]] and [[300f + 200b = 8000]]", "[[f = b + 10]] and [[200f + 300b = 8000]]", "[[f + b = 10]] and [[300f + 200b = 8000]]"],
     "floor = balcony + 10; 300 floor seats at [[f]], 200 balcony at [[b]]", "Which price is bigger? Match each count with its price.", "System for the concert seats?"),
  op("Solve the concert system from Question 2. What does each seat cost?", "floor $20, balcony $10",
     "[[300(b + 10) + 200b = 8000]] → [[500b = 5000]] → [[b = 10]], [[f = 20]]", "Substitute b + 10 for f.",
     ["300(______) + 200b = 8000", "500b + 3000 = 8000, so b = ______", "f = b + 10 = ______"], "Solve the concert system")],
 (3, 1): [
  mc("Use linear combinations to solve [[x + y = 9]] and [[x − y = 3]].", ["[[(6, 3)]]", "[[(3, 6)]]", "[[(12, −3)]]", "[[(6, −3)]]"],
     "add: [[2x = 12]], [[x = 6]], [[y = 3]]", "Add the equations: y and −y drop out.", "Solve: [[x + y = 9]], [[x − y = 3]]"),
  mc("You add [[2x + 5y = 4]] and [[−2x + 3y = 12]]. Which variable drops out?", ["[[x]]", "[[y]]", "both", "neither"],
     "[[2x + (−2x) = 0]]", "Look for opposite coefficients.", "Which variable drops out?"),
  op("Solve: [[2x + 5y = 4]] and [[−2x + 3y = 12]].", "[[(−3, 2)]]", "add: [[8y = 16]], [[y = 2]]; [[2x + 10 = 4]], [[x = −3]]",
     "Add the equations first.", ["Add: ____y = 16, so y = ______", "2x + 5(____) = 4", "x = ______"], "Solve: [[2x + 5y = 4]], [[−2x + 3y = 12]]")],
 (3, 2): [
  mc("Solve: [[3x + y = 7]] and [[2x + 2y = 6]].", ["[[(2, 1)]]", "[[(1, 2)]]", "[[(2, 3)]]", "[[(−2, 13)]]"],
     "× (−2): [[−6x − 2y = −14]]; add: [[−4x = −8]], [[x = 2]], [[y = 1]]", "Multiply the first equation by −2.", "Solve: [[3x + y = 7]], [[2x + 2y = 6]]"),
  mc("Plan A: 3 classes and 2 snacks cost $35. Plan B: 2 classes and 4 snacks cost $30. What does one class and one snack cost?",
     ["class $10, snack $2.50", "class $2.50, snack $10", "class $11, snack $1", "class $9, snack $4"],
     "[[3c + 2s = 35]], [[2c + 4s = 30]]; × (−2) the first: [[−4c = −40]], [[c = 10]], [[s = 2.5]]", "Check your answer in BOTH plans.", "Class and snack prices?"),
  op("Solve: [[4x + 3y = 10]] and [[3x + 2y = 7]].", "[[(1, 2)]]", "× 2 and × (−3): [[8x + 6y = 20]], [[−9x − 6y = −21]]; add: [[x = 1]], [[y = 2]]",
     "Multiply both equations so the y-terms are 6y and −6y.", ["× 2: 8x + 6y = ______", "× (−3): −9x − 6y = ______", "Add: −x = ______, so x = ______, y = ______"],
     "Solve: [[4x + 3y = 10]], [[3x + 2y = 7]]")],
 (3, 3): [
  mc("Solve: [[x + y = 20]] and [[½x + ¼y = 7]].", ["[[(8, 12)]]", "[[(12, 8)]]", "[[(10, 10)]]", "[[(6, 14)]]"],
     "× 4: [[2x + y = 28]]; subtract [[x + y = 20]]: [[x = 8]], [[y = 12]]", "Multiply by 4 to clear the fractions.", "Solve: [[x + y = 20]], [[½x + ¼y = 7]]"),
  mc("Which method is most efficient for [[4x − 3y = 5]] and [[2x + 3y = 7]]?", ["linear combinations", "substitution", "graphing", "guess and check"],
     "[[−3y]] and [[3y]] are already opposites", "Look for opposite coefficients or a variable alone.", "Best method?"),
  op("A snack bar sold 50 items: hot dogs for $3 and drinks for $2. It made $130. How many of each did it sell?", "30 hot dogs and 20 drinks",
     "[[h + d = 50]], [[3h + 2d = 130]]; × (−2) the first and add: [[h = 30]], [[d = 20]]", "Write one equation for items and one for money.",
     ["Items: h + d = ______", "Money: 3h + 2d = ______", "h = ______, d = ______"], "Hot dogs and drinks")],
 (4, 1): [
  mc("The boundary line for [[y ≤ 3x + 1]] is…", ["solid, because ≤ includes the line", "dashed, because ≤ includes the line", "solid, because points on the line are not solutions", "dashed, because the slope is 3"],
     "≤ includes equal, so points on the line are solutions: solid", "≤ and ≥ → solid. &lt; and &gt; → dashed.", "Line for [[y ≤ 3x + 1]]?"),
  mc("Which point is a solution of [[2x + 3y ≥ 12]]?", ["[[(3, 3)]]", "[[(1, 2)]]", "[[(0, 3)]]", "[[(2, 2)]]"],
     "[[2(3) + 3(3) = 15]] and [[15 ≥ 12]]", "Substitute, then compare to 12.", "Solution of [[2x + 3y ≥ 12]]?"),
  op("Graph [[y > x − 2]]. Describe the boundary line and which side you shade.", "dashed line; [[(0, 0)]]: [[0 > −2]] true, shade the side with [[(0, 0)]] (above)",
     "&gt; → dashed; test [[(0, 0)]]: true", "Line first, then test (0, 0).", ["Line y = x − 2 is ______ (solid / dashed)", "Test (0, 0): 0 > ______ is ______", "Shade ______ the line"],
     "Graph [[y > x − 2]]")],
 (4, 2): [
  mc("A $30 gift card buys songs for $1.50 ([[s]]) and movies for $6 ([[m]]). Which inequality shows what Kim can buy?",
     ["[[1.5s + 6m ≤ 30]]", "[[1.5s + 6m ≥ 30]]", "[[6s + 1.5m ≤ 30]]", "[[1.5s + 6m = 30]]"],
     "spend at most $30: ≤", "Match each price with its item. “At most” → ≤.", "Gift card inequality?"),
  mc("Can Kim buy 8 songs and 3 movies with the card?", ["Yes, it costs exactly $30", "No, it costs $33", "Yes, it costs $24", "No, it costs $36"],
     "[[1.5(8) + 6(3) = 12 + 18 = 30]] and [[30 ≤ 30]]", "Substitute s = 8, m = 3.", "8 songs and 3 movies?"),
  op("A solid line passes through [[(0, 2)]] and [[(4, 0)]]. The half-plane below it is shaded. Write the inequality.", "[[y ≤ −½x + 2]]",
     "slope [[−2/4 = −½]], [[y]]-intercept 2; solid and below → ≤", "Find the slope and y-intercept, then pick the symbol.",
     ["Slope = −2 ÷ 4 = ______", "y-intercept = ______", "Solid + below: y ____ ______"], "Inequality for the graph")],
 (5, 1): [
  mc("Is [[(2, 1)]] a solution of [[y ≥ x − 3]] and [[y < −x + 5]]?", ["Yes, it makes both true", "No, only the first is true", "No, only the second is true", "No, neither is true"],
     "[[1 ≥ −1]] ✓ and [[1 < 3]] ✓", "Test the point in EVERY inequality.", "Is [[(2, 1)]] a solution?"),
  mc("A raft holds at most 600 lb. Adults weigh about 150 lb and children 75 lb. Adults pay $40 and children $20, and the guide wants at least $100. Which system models this?",
     ["[[150a + 75c ≤ 600]] and [[40a + 20c ≥ 100]]", "[[150a + 75c ≥ 600]] and [[40a + 20c ≤ 100]]", "[[40a + 20c ≤ 600]] and [[150a + 75c ≥ 100]]", "[[150a + 75c ≤ 100]] and [[40a + 20c ≥ 600]]"],
     "weight at most 600: ≤; money at least 100: ≥", "One inequality for weight, one for money.", "Raft system?"),
  op("Name one point that is a solution of [[y > x]] and [[y < 4]], and show that it works.", "Sample: [[(0, 2)]]: [[2 > 0]] ✓ and [[2 < 4]] ✓",
     "any point above [[y = x]] and below [[y = 4]]", "Pick a point, then test BOTH inequalities.", ["My point: (____, ____)", "y > x: ______ ✓", "y < 4: ______ ✓"],
     "A solution of [[y > x]], [[y < 4]]")],
 (5, 2): [
  mc("Which system has no solution?", ["[[y > 2x + 3]] and [[y < 2x − 1]]", "[[y > 2x + 3]] and [[y > 2x − 1]]", "[[y < 2x + 3]] and [[y > 2x − 1]]", "[[y > x]] and [[y < −x]]"],
     "parallel lines: above the top and below the bottom never overlap", "Same slope? Check which sides are shaded.", "Which system has no solution?"),
  mc("A workout is at most 40 minutes and burns at least 300 calories. Walking ([[w]]) burns 5 calories a minute and running ([[r]]) burns 10. Which ([[w]], [[r]]) is a solution?",
     ["[[(10, 30)]]", "[[(30, 5)]]", "[[(20, 25)]]", "[[(5, 20)]]"],
     "[[10 + 30 = 40 ≤ 40]] and [[5(10) + 10(30) = 350 ≥ 300]]", "Check the minutes AND the calories.", "Workout solution?"),
  op("Write the system of inequalities for the workout in Question 2.", "[[w + r ≤ 40]] and [[5w + 10r ≥ 300]]", "time at most 40; calories at least 300",
     "One inequality for minutes, one for calories.", ["Minutes: w + r ____ 40", "Calories: 5w + 10r ____ 300"], "Workout system")],
 (5, 3): [
  mc("Where is the solution set of [[y > ⅔x + 1]] and [[y < −⅔x + 1]]?", ["between the lines, left of where they cross", "between the lines, right of where they cross", "above both lines", "below both lines"],
     "above the rising line and below the falling line: the left wedge", "Sketch both lines, then shade each.", "Region of the system?"),
  mc("Which point is a solution of [[y > ⅔x + 1]] and [[y < −⅔x + 1]]?", ["[[(−3, 0)]]", "[[(3, 0)]]", "[[(0, 1)]]", "[[(0, −2)]]"],
     "[[0 > −1]] ✓ and [[0 < 3]] ✓", "Test each point in both inequalities.", "Solution of the system?"),
  op("Explain why [[(0, 1)]] is not a solution of [[y > ⅔x + 1]] and [[y < −⅔x + 1]].", "[[(0, 1)]] is where the dashed lines cross: [[1 > 1]] is false",
     "both boundaries are dashed, so their crossing point is not included", "What does a dashed line mean?", ["Test y > ⅔x + 1: 1 > ______ is ______", "So (0, 1) is ______ a solution"],
     "Why is [[(0, 1)]] not a solution?")],
}


def check():
    from fractions import Fraction as F
    for key, qs in BELL.items():
        assert len(qs) == 4 and all(len(set(q["choices"])) == 4 for q in qs), key
    for key, items in EXIT.items():
        assert all(it["kind"] == "open" or len(set(it["choices"])) == 4 for it in items), key
    assert set(BELL) == set(EXIT) == set(DATES)
    sol = lambda eqs, x, y: all(a * x + b * y == c for a, b, c in eqs)
    assert 2 * 10 == 20 and 4 * 6 == 24 and 2 * 2 - 1 == 3
    assert sol([(-2, 1, 0), (-1, 1, 3)], 3, 6) and 5 * 200 + 10 * 200 == 3000 and 5 * 300 + 10 * 200 != 3000
    assert sol([(1, 1, 4), (-1, 1, -2)], 3, 1) and not sol([(1, 1, 4), (-1, 1, -2)], 2, 2) and 2 * 3 - 1 == 5
    assert sol([(-4, 1, 0), (2, 1, 18)], 3, 12) and sol([(1, 1, 10), (1, -1, 2)], 6, 4)
    assert sol([(1, -1, 2), (1, 1, 12)], 7, 5) and sol([(1, 1, 12), (1, -1, 4)], 8, 4) and 4 * 6 - 9 == 15
    assert sol([(2, 1, 11), (1, -1, 1)], 4, 3) and sol([(1, 2, 7), (3, -1, 7)], 3, 2) and sol([(1, 1, 8), (1, -1, 2)], 5, 3)
    assert 0 > 2 * 0 - 5 and 0 <= 4 and 1 > 2 * 1 - 3 and 2 + 3 <= 6 and not 4 + 3 <= 6 and not 6 + 1 <= 6 and not 5 + 2 <= 6
    assert not (2 > -(-1) + 1) and 20 + 25 <= 45 and not 30 + 20 <= 45
    assert 0 >= -3 + 2 and 0 <= 3 - 1
    # exit tickets
    assert sol([(-1, 1, 2), (1, 1, 6)], 2, 4) and 4 * 20 + 8 * 20 == 240
    assert 3 * 4 == 12 and 2 * 6 == 12
    assert all(2 * (3 * x + 2) == 6 * x + 4 for x in range(-3, 4))
    assert sol([(-3, 1, 0), (1, 1, 20)], 5, 15) and sol([(-1, 1, 4), (3, 1, 24)], 5, 9)
    assert all(4 * x - 2 * (2 * x + 1) == -2 for x in range(-3, 4)) and 300 * 20 + 200 * 10 == 8000
    assert sol([(1, 1, 9), (1, -1, 3)], 6, 3) and sol([(2, 5, 4), (-2, 3, 12)], -3, 2)
    assert sol([(3, 1, 7), (2, 2, 6)], 2, 1) and sol([(3, 2, 35), (2, 4, 30)], 10, F(5, 2)) and sol([(4, 3, 10), (3, 2, 7)], 1, 2)
    assert not sol([(3, 2, 35), (2, 4, 30)], 11, 1) and not sol([(3, 2, 35), (2, 4, 30)], 9, 4)
    assert sol([(1, 1, 20), (F(1, 2), F(1, 4), 7)], 8, 12) and sol([(1, 1, 50), (3, 2, 130)], 30, 20)
    assert [2 * x + 3 * y >= 12 for x, y in [(3, 3), (1, 2), (0, 3), (2, 2)]] == [True, False, False, False]
    assert F(3, 2) * 8 + 6 * 3 == 30 and F(-2, 4) == F(-1, 2)
    assert 1 >= 2 - 3 and 1 < -2 + 5 and 2 > 0 and 2 < 4
    work = lambda w, r: w + r <= 40 and 5 * w + 10 * r >= 300
    assert [work(*p) for p in [(10, 30), (30, 5), (20, 25), (5, 20)]] == [True, False, False, False]
    s53 = lambda x, y: y > F(2, 3) * x + 1 and y < -F(2, 3) * x + 1
    assert [s53(*p) for p in [(-3, 0), (3, 0), (0, 1), (0, -2)]] == [True, False, False, False]


# ================================================================ deck slides
def bell_href(n, d, kind=None):
    return f"m3t2-lesson{n}-bellwork-day{d}{'-' + kind if kind else ''}.html"


def bell_slide(n, d):
    MP.BELL[(f"m3t2l{n}", d)] = [{k: q[k] for k in ("q", "choices", "why")} for q in BELL[n, d]]
    return D.bell(f"m3t2l{n}", d, "Review").replace(f"online Day {d} bell work", f"online Day {d} bell work ({bell_href(n, d)})")


def exit_slide(n, d):
    items = EXIT[n, d]
    body = '<div class="col" style="gap:10px;margin-top:4px">' + "".join(
        f'<p>{k}. {D.mq(it["short"])}</p>{ans(D.mq(it["answer"]), True)}' for k, it in enumerate(items, 1)) + "</div>"
    work = " ".join(f"{k}. {re.sub(r'\[\[|\]\]', '', it['work'])}." for k, it in enumerate(items, 1))
    return sec(f"Day {d} · Exit Ticket", "Show what you know", body,
               f"Printed copy: EXIT TICKET/M3T2-Exit-Ticket-{DATES[n, d]}.pdf. Give about 8 minutes. Work: {work}")


def iep_bell(n, d):
    cards = [f'<div class="card" style="padding:10px 18px;gap:4px"><p class="small"><b>{k}.</b> {A.mt(q["q"])}</p>'
             f'<p class="small" style="color:var(--point)"><b>Formula:</b> {A.mt(q["formula"])}</p>'
             f'<div class="step pop ans" style="font-size:19px;line-height:1.35;padding:6px 14px"><b>{A.mt(q["choices"][0])}</b>'
             + "".join(f"<br><b>{j}.</b> {A.mt(t)}" for j, t in enumerate(q["steps"], 1)) + "</div></div>" for k, q in enumerate(BELL[n, d], 1)]
    return sec(f"Day {d} · Bell Work · Review", "Warm up: work these on your own", row("".join(cards[:2]), "".join(cards[2:]), gap=24),
               f"Same 4 questions as the online IEP Day {d} bell work ({bell_href(n, d, 'IEP')}, 3 answer choices there). Reveal one answer at a time; read each step aloud.")


def iep_exit(n, d):
    cards = []
    for k, it in enumerate(EXIT[n, d][:3], 1):
        extra = ("".join(f'<p class="step small">{f}</p>' for f in it.get("frames", [])[:3]) if it["kind"] == "open"
                 else '<p class="small">' + " · ".join(A.mt(c) for c in it["choices"][:3]) + "</p>")
        cards.append(f'<div class="card"><p>{k}. {A.mt(it["short"])}</p><p class="small muted">Tip: {it["tip"]}</p>{extra}{A.ans(A.mt(it["answer"]))}</div>')
    return sec(f"Day {d} · Exit Ticket", "Show what you know", row(*cards, gap=18),
               f"IEP exit ticket (EXIT TICKET/M3T2-Exit-Ticket-{DATES[n, d]}-IEP.pdf): a tip on each item, 3 answer choices on multiple choice, step frames.")


# ================================================================ online bell work (general, 504, IEP)
def bell_pages(n, d, lesson_name):
    name = bell_href(n, d)
    qs = [{k: q[k] for k in ("q", "choices", "why")} | ({"letters": "FGHJ"} if i % 2 else {}) for i, q in enumerate(BELL[n, d])]
    MP.OUT = OUT
    MP.page(name, f"Topic 2 Lesson {n} Day {d} Bell Work · {lesson_name}", f"Module 3 · Topic 2 · Lesson {n} · Day {d} Bell Work", "Bell Work: Review",
            "Warm up while attendance is taken. Answer all 4 questions, then submit to see which ones you got right.", "quiz", qs)
    s = (OUT / name).read_text(encoding="utf-8")
    for kind in ("504", "IEP"):
        accom = {"readAloud": True}
        if kind == "IEP":
            accom["choices"] = 3
            accom["add"] = [{"extra": f'<p class="formula" style="margin:8px 0 2px;padding:6px 12px;border-left:4px solid #2f6fdd;background:rgba(47,111,221,.08);'
                                      f'border-radius:4px"><b>Formula:</b> {A.mt(q["formula"])}</p>',
                             "why": "Here is how:" + "".join(f"<br><b>{j}.</b> {t}" for j, t in enumerate(q["steps"], 1))} for q in BELL[n, d]]
        ref = f'<div class="card ref"><p>{A.HELP[kind]}</p>' + "".join(f"<p>{r}</p>" for r in REF[n]) + "</div>"
        t = s.replace("</title>", f" · {LABEL[kind]}</title>", 1).replace('<div class="wrap">', '<div class="wrap big">', 1)
        t = re.sub(r'(<p class="eyebrow">.*?)</p>', lambda m: f"{m.group(1)} · {LABEL[kind]} Version</p>", t, count=1)
        t = re.sub(r'(<p class="muted">.*?</p>)', lambda m: m.group(1) + "\n  " + ref, t, count=1)
        t = t.replace('</script>\n<script src="../mc.js">', f'window.MC.accom = {json.dumps(accom, ensure_ascii=False)};\n</script>\n<script src="../mc.js">')
        assert "window.MC.accom" in t
        (FOLDER[kind] / bell_href(n, d, kind)).write_text(t, encoding="utf-8")


# ================================================================ printable sheets (general / 504 / IEP, each with key)
def sheet(fname, what, n, items, key, kind=None):
    blocks = []
    for it in items:
        ch = it["choices"]
        if ch and kind == "IEP":  # 3 choices: drop the last distractor, keep the correct one
            ch = [c for c in ch if c == it["answer"]] + [c for c in ch if c != it["answer"]][:2]
            ch = sorted(ch, key=lambda c: it["choices"].index(c))
        b = f'<div class="it{" mc" if ch else ""}"><b>{it["num"]}.</b> {plain(it["q"])}'
        if kind == "IEP" and it.get("tip"):
            b += f'<div class="tip"><b>Tip:</b> {plain(it["tip"])}</div>'
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
    ref = (f'<div class="ref"><b>Reminders</b>' + "".join(f"<p>{r}</p>" for r in REF[n]) + "</div>") if kind else ""
    html = (f'<!doctype html><html><head><meta charset="utf-8"><title>{fname}</title><style>{CSS}</style></head><body>'
            f'<div class="hdr"><span>MODULE 3 • TOPIC 2 • LESSON {n} • {what.upper()}{lab}</span><span>{"ANSWER KEY" if key else ""}</span></div>'
            f'<div class="top"><b>TOPIC 2</b> Systems of Linear Equations and Inequalities</div>'
            f'<div class="nm">Name ____________________________ &nbsp; Date __________</div>{ref}'
            f'<div class="{"one big" if kind else "grid"}">{"".join(blocks)}</div></body></html>')
    src = OUT / what / f"{fname}.html"
    src.parent.mkdir(exist_ok=True)
    src.write_text(html, encoding="utf-8")
    subprocess.run([EDGE, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={src.with_suffix('.pdf')}", src.as_uri()],
                   check=True, capture_output=True)
    src.unlink()


def write_sheets(n, d):
    date = DATES[n, d]
    bell = [dict(num=k, q=q["q"], choices=print_order(q["choices"], (k + d + n) % 4), letters="FGHJ" if k % 2 == 0 else "ABCD",
                 answer=q["choices"][0], why=q["why"], tip=q["formula"], frames=None) for k, q in enumerate(BELL[n, d], 1)]
    ex = [dict(num=k, q=it["q"], choices=print_order(it["choices"], (k + d) % 4) if it["kind"] == "mc" else None,
               letters="FGHJ" if k % 2 == 0 else "ABCD", answer=it["answer"], why=it["work"], tip=it["tip"], frames=it.get("frames"))
          for k, it in enumerate(EXIT[n, d], 1)]
    for kind in (None, "504", "IEP"):
        sfx = f"-{kind}" if kind else ""
        for key in (False, True):
            k2 = "-ANSWER-KEY" if key else ""
            sheet(f"M3T2-Bell-Work-{date}{sfx}{k2}", "BELL WORK", n, bell, key, kind)
            sheet(f"M3T2-Exit-Ticket-{date}{sfx}{k2}", "EXIT TICKET", n, ex, key, kind)


# ================================================================ Today's Agenda slides (district pacing calendar, AHS)
import agendas as AG

BELL_ITEM = ("Bell Work", "Four warm-ups. Start as soon as you sit down.")
EXIT_ITEM = ("Exit Ticket", "Three questions to show what you learned.")
# (date key, weekday + date, eyebrow, middle items, closing line, color, lesson day or None)
AGENDA = [
 ("Mon-11-30", "Monday, Nov 30", "🦃 Welcome back! Topic 2 starts today", [("Lesson 1: Using Graphing to Solve Systems", "Getting Started, Activities 1.1 and 1.2 (SE pp. 394–399).")], "New topic, fresh start. Let’s go! 🚀", "#0b6b3a", (1, 1)),
 ("Tue-12-01", "Tuesday, Dec 1", "Lesson 1 · Day 2", [("Lesson 1: Using Graphing to Solve Systems", "Activity 1.3 and Talk the Talk (SE pp. 400–405).")], "Let’s get busy! 💪", "#3050b8", (1, 2)),
 ("Wed-12-02", "Wednesday, Dec 2", "Lesson 2 · Day 1", [("Lesson 2: Using Substitution", "Getting Started and Activity 2.1 (SE pp. 412–416).")], "Let’s get busy! 💪", "#3050b8", (2, 1)),
 ("Thu-12-03", "Thursday, Dec 3", "Lesson 2 · Day 2", [("Lesson 2: Using Substitution", "Activities 2.2, 2.3 and Talk the Talk (SE pp. 417–425).")], "Let’s get busy! 💪", "#3050b8", (2, 2)),
 ("Mon-12-07", "Monday, Dec 7", "Lesson 3 · Day 1", [("Lesson 3: Using Linear Combinations", "Getting Started and Activity 3.1 (SE pp. 434–436).")], "Let’s get busy! 💪", "#3050b8", (3, 1)),
 ("Tue-12-08", "Tuesday, Dec 8", "Lesson 3 · Day 2", [("Lesson 3: Using Linear Combinations", "Activities 3.2 and 3.3 (SE pp. 437–441).")], "Let’s get busy! 💪", "#3050b8", (3, 2)),
 ("Wed-12-09", "Wednesday, Dec 9", "Lesson 3 · Day 3", [("Lesson 3: Using Linear Combinations", "Activity 3.4 and Talk the Talk (SE pp. 442–444).")], "Let’s get busy! 💪", "#3050b8", (3, 3)),
 ("Thu-12-10", "Thursday, Dec 10", "Skills Practice Day", [("Warm-up", "Solve one system three ways: graphing, substitution, linear combinations."),
   ("Skills Practice", "Your assigned problem set on systems of equations."), ("Check your work", "Use the anchor charts and the lessons with answers."),
   ("Finished?", "Show your teacher, then help other students.")], "Practice makes progress! 💪", "#7a4fc4", None),
 ("Mon-01-04", "Monday, Jan 4", "❄️ Welcome back! Happy New Year", [("Lesson 4: Graphing Inequalities in Two Variables", "Getting Started, Activities 4.1 and 4.2 (SE pp. 450–457).")], "New year, fresh start! 🚀", "#0b6b3a", (4, 1)),
 ("Tue-01-05", "Tuesday, Jan 5", "Lesson 4 · Day 2", [("Lesson 4: Graphing Inequalities in Two Variables", "Activity 4.3 and Talk the Talk (SE pp. 459–462).")], "Let’s get busy! 💪", "#3050b8", (4, 2)),
 ("Wed-01-06", "Wednesday, Jan 6", "Lesson 5 · Day 1", [("Lesson 5: Systems of Linear Inequalities", "Getting Started and Activity 5.1 (SE pp. 468–470).")], "Let’s get busy! 💪", "#3050b8", (5, 1)),
 ("Thu-01-07", "Thursday, Jan 7", "Lesson 5 · Day 2", [("Lesson 5: Systems of Linear Inequalities", "Activities 5.2 and 5.3 (SE pp. 471–475).")], "Let’s get busy! 💪", "#3050b8", (5, 2)),
 ("Mon-01-11", "Monday, Jan 11", "Lesson 5 · Day 3", [("Lesson 5: Systems of Linear Inequalities", "Activity 5.4 and Talk the Talk (SE pp. 476–478).")], "Test is Wednesday. You’ve got this! 💪", "#3050b8", (5, 3)),
 ("Tue-01-12", "Tuesday, Jan 12", "📝 Review Day: the test is tomorrow!", [("Warm-up", "One system and one inequality to graph."),
   ("Topic 2 Review", "Graphing, substitution, linear combinations, inequalities and systems of inequalities."),
   ("Missed one?", "Use the anchor charts and rewatch that lesson’s slides."), ("Get ready for tomorrow!", "The Topic 2 Test is Wednesday, Jan 13.")],
  "Let’s get busy! 💪", "#c9561f", None),
 ("Wed-01-13", "Wednesday, Jan 13", "📝 Test Day · Topic 2 Test", [("Clear your desk", "Only a pencil stays out."), ("Chromebook ready", "You will enter your answers on it."),
   ("Calculator + formula sheet", "Get them now."), ("Take the test", "Read each question carefully and check your work.")],
  "Good luck! You’ve got this! 🍀", "#b00020", None),
 ("Thu-01-14", "Thursday, Jan 14", "🔁 Retake Day", [("Retaking? Get set up", "Clear desk, Chromebook ready, calculator + formula sheet."),
   ("Not retaking?", "Redo the questions you missed using the anchor charts and lesson slides."),
   ("Quiet room", "Work silently so retakers can focus. Raise your hand for help.")], "Second chance, best effort! 💪", "#1f8a4c", None),
]
TEST_DAY = {"Wed-01-13": "🪑 Walk in and take your seat quickly."}


def agenda_slide(i):
    key, long, eyebrow, mid, end, color, lesson = AGENDA[i]
    items = [BELL_ITEM] + mid + [EXIT_ITEM] if lesson else mid
    return AG.slide(eyebrow, f"📅 Today’s Agenda · {long}", items, end, color,
                    "Leave this up as students walk in. Same for all periods." + (" Bell work and exit ticket are in this deck." if lesson else ""),
                    TEST_DAY.get(key, AG.FIRST))


def agenda_for(n, d):
    return agenda_slide(next(i for i, a in enumerate(AGENDA) if a[6] == (n, d)))


def agenda_deck():
    """All Topic 2 agendas in one deck: slide k + 1 is day k (link with #s{k+1})."""
    first = (f'<section class="slide">\n  <p class="eyebrow">Bluebonnet Algebra I · Module 3 · Topic 2</p>\n'
             f'  <h1 style="margin-top:6px;font-size:56px">Today’s Agenda</h1>\n  <div class="eq" style="margin-top:8px;font-size:36px">Systems of Linear Equations and Inequalities · Nov 30 – Jan 14</div>\n'
             '  <p class="muted small">Press → for the next day. Each class day has its own slide.</p>\n'
             '  <aside class="notes">One agenda slide per class day on the district pacing calendar. Thanksgiving is over; winter break is Dec 21–31; the semester exam week (Dec 14–17) is not in this deck.</aside>\n</section>\n')
    return [first] + [agenda_slide(i) for i in range(len(AGENDA))]

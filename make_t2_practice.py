"""Writes the Topic 2 bell work, homework and quiz pages into 'Module 2 topic 2/'.  Run:  python make_t2_practice.py"""
import json, sys
from pathlib import Path

OUT = Path(__file__).parent / "Module 2 topic 2"
ICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' "
        "rx='8' fill='%233050b8'/%3E%3Cg fill='%23fff'%3E%3Ccircle cx='16' cy='7.5' r='2.3'/%3E%3Ccircle cx='12.8' cy='11.8' "
        "r='2.5'/%3E%3Ccircle cx='19.2' cy='11.8' r='2.5'/%3E%3Ccircle cx='16' cy='14.6' r='2.6'/%3E%3Ccircle cx='11.8' "
        "cy='17.6' r='2.7'/%3E%3Ccircle cx='20.2' cy='17.6' r='2.7'/%3E%3C/g%3E%3Crect x='15.2' y='20.5' width='1.6' "
        "height='6.5' rx='.8' fill='%239fd18b'/%3E%3C/svg%3E")
HEAD = f"""<!doctype html>
<html lang="en">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{title}}</title>
<link rel="icon" href="{ICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=STIX+Two+Text:ital,wght@0,500;1,500&display=swap">
<link rel="stylesheet" href="../mc.css">
"""

LESSONS = {1: "Transforming Linear Functions", 2: "Vertical and Horizontal Transformations",
           3: "Slopes of Perpendicular Lines", 4: "Comparing Linear Functions"}


def table(rows, head=None):
    h = f"<tr>{''.join(f'<th>{c}</th>' for c in head)}</tr>" if head else ""
    return f'<table class="data">{h}' + "".join(
        f"<tr>{''.join(f'<td>{c}</td>' for c in r)}</tr>" for r in rows) + "</table>"


def page(path, title, eyebrow, h1, intro, mode, qs):
    named = mode == "quiz"
    body = f"""<div class="wrap">
  <p class="eyebrow">{eyebrow}</p>
  <h1>{h1}</h1>
  <p class="muted">{intro}</p>
"""
    if named:
        body += """  <label class="name">Your name <input id="name" autocomplete="name"></label>
  <ol id="questions"></ol>
  <div class="bar">
    <button id="submit" disabled>Submit</button>
    <button id="reset" class="ghost">Start over</button>
  </div>
  <p id="result" class="card" style="margin-top:16px" hidden></p>
</div>
"""
    else:
        body += """  <ol id="questions"></ol>
  <div class="bar">
    <p id="result" class="card" hidden></p>
    <button id="reset" class="ghost">Start over</button>
  </div>
</div>
"""
    items = ",\n".join("  " + json.dumps(q, ensure_ascii=False) for q in qs)
    js = f'<script>\nwindow.MC = {{ mode: "{"quiz" if named else "homework"}", questions: [\n{items},\n] }};\n</script>\n<script src="../mc.js"></script>\n'
    (OUT / path).write_text(HEAD.replace("{title}", title) + body + js, encoding="utf-8")


def Q(q, choices, why, se=None, extra=None):
    d = {"q": q, "choices": choices, "why": why}
    if se: d = {"se": se, **d}
    if extra: d["extra"] = extra
    return d


BELL = {  # (lesson, day): 4 warm-up questions
    (1, 1): [
        Q("What is the slope between [[(1, 2)]] and [[(4, 11)]]?", ["[[3]]", "[[⅓]]", "[[9]]", "[[−3]]"],
          "Slope [[= (11 − 2) ÷ (4 − 1) = 9 ÷ 3 = 3]]."),
        Q("What is the [[y]]-intercept of [[y = 3x − 7]]?", ["[[(0, −7)]]", "[[(0, 3)]]", "[[(−7, 0)]]", "[[(7, 0)]]"],
          "In [[y = mx + b]], the [[y]]-intercept is [[(0, b)]], so it is [[(0, −7)]]."),
        Q("[[f(x) = 2x + 1]]. What is [[f(−3)]]?", ["[[−5]]", "[[−7]]", "[[7]]", "[[−6]]"],
          "[[2(−3) + 1 = −6 + 1 = −5]]."),
        Q("Which line is parallel to [[y = 3x + 1]]?", ["[[y = 3x − 5]]", "[[y = −3x + 1]]", "[[y = ⅓x + 1]]", "[[y = x + 3]]"],
          "Parallel lines have the same slope. Only [[y = 3x − 5]] has slope 3."),
    ],
    (1, 2): [
        Q("[[f(x) = x]] is translated up 4 units. Which equation is the new function?",
          ["[[g(x) = x + 4]]", "[[g(x) = x − 4]]", "[[g(x) = 4x]]", "[[g(x) = x + ¼]]"],
          "A vertical translation adds to the output: [[g(x) = f(x) + 4 = x + 4]].", se=272),
        Q("The point [[(2, 5)]] is translated down 3 units. Where does it go?", ["[[(2, 2)]]", "[[(−1, 5)]]", "[[(2, 8)]]", "[[(5, 5)]]"],
          "A vertical translation changes only [[y]]: [[5 − 3 = 2]], so [[(2, 2)]].", se=273),
        Q("[[f(x) = 2x − 1]]. What is the slope of [[g(x) = f(x) + 6]]?", ["[[2]]", "[[6]]", "[[8]]", "[[5]]"],
          "A vertical translation does not change the slope. [[g(x) = 2x + 5]] still has slope 2.", se=275),
        Q("[[f(x) = 2x − 1]]. What is the [[y]]-intercept of [[g(x) = f(x) + 6]]?", ["[[(0, 5)]]", "[[(0, 6)]]", "[[(0, −1)]]", "[[(0, 7)]]"],
          "[[g(x) = 2x − 1 + 6 = 2x + 5]], so the [[y]]-intercept moves from [[(0, −1)]] up 6 to [[(0, 5)]].", se=275),
    ],
    (1, 3): [
        Q("[[f(x) = x]] and [[g(x) = 3f(x)]]. What is the slope of [[g(x)]]?", ["[[3]]", "[[1]]", "[[⅓]]", "[[−3]]"],
          "[[g(x) = 3x]]. A vertical dilation by 3 multiplies the slope of [[f(x) = x]] by 3.", se=277),
        Q("How is [[g(x) = −2f(x)]] related to [[f(x) = x]]?",
          ["Stretched vertically by 2 and reflected across the [[x]]-axis", "Translated down 2",
           "Compressed vertically by ½", "Reflected across the [[y]]-axis only"],
          "The 2 stretches the graph and the negative sign reflects it across the [[x]]-axis.", se=278),
        Q("Which function is a vertical compression of [[f(x) = x]]?", ["[[g(x) = ½f(x)]]", "[[g(x) = 2f(x)]]", "[[g(x) = f(x) − ½]]", "[[g(x) = −f(x)]]"],
          "Multiplying by a number between 0 and 1 compresses the graph toward the [[x]]-axis.", se=278),
        Q("[[f(x) = x]] and [[g(x) = 2f(x) − 5]]. What is the [[y]]-intercept of [[g(x)]]?", ["[[(0, −5)]]", "[[(0, 2)]]", "[[(0, −3)]]", "[[(5, 0)]]"],
          "[[g(x) = 2x − 5]]. The dilation keeps [[(0, 0)]] fixed, then the graph moves down 5.", se=280),
    ],
    (2, 1): [
        Q("[[f(x) = x]] and [[g(x) = f(x) − 3]]. How does the graph move?", ["Down 3 units", "Up 3 units", "Right 3 units", "Left 3 units"],
          "Subtracting from the output is a vertical translation down 3."),
        Q("What is the slope of [[g(x) = 3x − 8]]?", ["[[3]]", "[[−8]]", "[[8/3]]", "[[−3]]"],
          "In [[y = mx + b]], [[m]] is the slope.", se=288),
        Q("What is the [[x]]-intercept of [[g(x) = 3x − 8]]?", ["[[(8/3, 0)]]", "[[(0, −8)]]", "[[(−8/3, 0)]]", "[[(8, 0)]]"],
          "Set [[g(x) = 0]]: [[3x − 8 = 0]], so [[x = 8/3]].", se=288),
        Q("Is [[h(x) = −⅔x + 5]] increasing or decreasing?", ["Decreasing", "Increasing", "Neither", "Both"],
          "The slope [[−⅔]] is negative, so the line falls from left to right.", se=288),
    ],
    (2, 2): [
        Q("[[f(x) = x]] is translated right 5 units. Which equation is the new function?",
          ["[[g(x) = f(x − 5) = x − 5]]", "[[g(x) = f(x + 5) = x + 5]]", "[[g(x) = f(x) + 5]]", "[[g(x) = 5f(x)]]"],
          "A horizontal translation right 5 subtracts 5 from the input: [[f(x − 5)]].", se=289),
        Q("For [[f(x) = x]], a translation right 5 gives the same graph as which other translation?",
          ["Down 5 units", "Up 5 units", "Left 5 units", "None"],
          "[[f(x − 5) = x − 5 = f(x) − 5]], a vertical translation down 5.", se=291),
        Q("[[j(x) = 2x − 1]] and [[r(x) = j(x + 4)]]. Simplify [[r(x)]].", ["[[r(x) = 2x + 7]]", "[[r(x) = 2x + 3]]", "[[r(x) = 2x + 8]]", "[[r(x) = 2x − 5]]"],
          "[[2(x + 4) − 1 = 2x + 8 − 1 = 2x + 7]].", se=292),
        Q("For [[f(x) = x]], is the graph of [[f(2x)]] the same as the graph of [[2f(x)]]?",
          ["Yes, both are [[y = 2x]]", "No, they are parallel", "No, they are perpendicular", "No, one is [[y = ½x]]"],
          "[[f(2x) = 2x]] and [[2f(x) = 2x]]. For the parent function they match.", se=295),
    ],
    (3, 1): [
        Q("What is the reciprocal of [[⅔]]?", ["[[3/2]]", "[[−⅔]]", "[[−3/2]]", "[[1]]"],
          "Flip the fraction: [[⅔ · 3/2 = 1]]."),
        Q("Rotate the point [[(8, 5)]] 90° counterclockwise about the origin. Where does it go?",
          ["[[(−5, 8)]]", "[[(5, −8)]]", "[[(−8, −5)]]", "[[(8, −5)]]"],
          "A 90° counterclockwise rotation maps [[(x, y)]] to [[(−y, x)]].", se=306),
        Q("What is the slope of the segment from [[(0, 0)]] to [[(8, 5)]]?", ["[[5/8]]", "[[8/5]]", "[[−5/8]]", "[[13]]"],
          "Slope [[= (5 − 0) ÷ (8 − 0) = 5/8]].", se=306),
        Q("What is the slope of [[y = −3x + 5]]?", ["[[−3]]", "[[5]]", "[[3]]", "[[⅓]]"],
          "In [[y = mx + b]], [[m = −3]]."),
    ],
    (3, 2): [
        Q("Line [[j]] has slope [[⅔]]. Line [[k]] is perpendicular to it. What is the slope of [[k]]?",
          ["[[−3/2]]", "[[3/2]]", "[[−⅔]]", "[[⅔]]"],
          "Perpendicular slopes are negative reciprocals: [[⅔ · (−3/2) = −1]].", se=309),
        Q("What is the slope of any horizontal line?", ["[[0]]", "Undefined", "[[1]]", "[[−1]]"],
          "On a horizontal line [[y]] never changes, so the rise is 0.", se=310),
        Q("Which is the equation of the vertical line through [[(2, −1)]]?", ["[[x = 2]]", "[[y = −1]]", "[[y = 2]]", "[[x = −1]]"],
          "Every point on a vertical line has the same [[x]]-value, here 2.", se=311),
        Q("What is the product of the slopes of two perpendicular lines (neither vertical)?", ["[[−1]]", "[[1]]", "[[0]]", "Undefined"],
          "Negative reciprocals multiply to [[−1]].", se=308),
    ],
    (4, 1): [
        Q("What is the slope of the line through [[(−2.5, −6)]] and [[(0, 4)]]?", ["[[4]]", "[[−4]]", "[[¼]]", "[[10]]"],
          "Slope [[= (4 − (−6)) ÷ (0 − (−2.5)) = 10 ÷ 2.5 = 4]].", se=321),
        Q("What slope does a line parallel to [[y = 4x − 3]] have?", ["[[4]]", "[[−4]]", "[[−¼]]", "[[−3]]"],
          "Parallel lines have equal slopes.", se=321),
        Q("What slope does a line perpendicular to [[y = 4x − 3]] have?", ["[[−¼]]", "[[¼]]", "[[−4]]", "[[4]]"],
          "The negative reciprocal of 4 is [[−¼]].", se=321),
        Q("The ratio of 9th-graders to 10th-graders is [[1 : 1]]. What is the slope of this relationship?", ["[[1]]", "[[0]]", "[[2]]", "[[½]]"],
          "Equal numbers of each grade: [[y = x]], slope 1.", se=320),
    ],
    (4, 2): [
        Q("Travis County pays $15 per ton of cardboard. How much is paid for 3 tons?", ["$45", "$18", "$5", "$60"],
          "[[15 · 3 = 45]].", se=322),
        Q("Hays County's graph passes through [[(0, 0)]] and [[(1, 20)]]. What is the payout per ton?", ["$20", "$15", "$1", "$10"],
          "Slope [[= 20 ÷ 1 = 20]] dollars per ton.", se=322),
        Q("[[J(x) = 9/5x + 32]] converts °C to °F. What is [[J(10)]]?", ["[[50]]", "[[42]]", "[[18]]", "[[23.9]]"],
          "[[9/5 · 10 + 32 = 18 + 32 = 50]], so 10°C is 50°F.", se=323),
        Q("Miguel started with $0 and had $80 after 4 months. How much did he save each month?", ["$20", "$80", "$25", "$4"],
          "[[80 ÷ 4 = 20]] dollars per month.", se=324),
    ],
}

HOMEWORK = {
    1: [
        Q("[[w(x) = 4x]] and [[r(x) = ½ · w(x)]]. What is [[r(30)]]?", ["[[60]]", "[[120]]", "[[15]]", "[[240]]"],
          "[[w(30) = 120]], and half of that is 60.", se=285),
        Q("[[w(x) = 4x]] and [[r(x) = ½ · w(x)]]. Which is [[r(x)]] in general form?", ["[[r(x) = 2x]]", "[[r(x) = 4.5x]]", "[[r(x) = 8x]]", "[[r(x) = 4x + ½]]"],
          "[[½ · 4x = 2x]].", se=285),
        Q("What transformation turns [[w(x) = 4x]] into [[r(x) = ½ · w(x)]]?",
          ["A vertical compression by a factor of ½", "A vertical stretch by a factor of 2", "A translation down ½", "A reflection across the [[x]]-axis"],
          "Multiplying the output by a number between 0 and 1 compresses the graph.", se=285),
        Q("Which line is parallel to [[y = 2x]] and passes through [[(0, 4)]]?", ["[[y = 2x + 4]]", "[[y = 4x]]", "[[y = −½x + 4]]", "[[y = 2x − 4]]"],
          "Same slope 2, and the [[y]]-intercept is [[(0, 4)]].", se=285),
        Q("Which line is parallel to [[y = 2x]] and passes through [[(−2, −1)]]?", ["[[y = 2x + 3]]", "[[y = 2x − 3]]", "[[y = 2x + 1]]", "[[y = −2x − 5]]"],
          "[[−1 = 2(−2) + b]], so [[b = 3]].", se=285),
        Q("Which line is parallel to [[y = 2x]] and passes through [[(2, 0)]]?", ["[[y = 2x − 4]]", "[[y = 2x + 4]]", "[[y = 2x − 2]]", "[[y = 2x]]"],
          "[[0 = 2(2) + b]], so [[b = −4]].", se=285),
        Q("[[f(x) = x]] and [[g(x) = f(x) − 7]]. Describe the transformation.", ["Translated down 7 units", "Translated up 7 units", "Stretched by a factor of 7", "Translated right 7 units"],
          "Subtracting 7 from the output moves every point down 7.", se=280),
        Q("[[f(x) = x]] and [[g(x) = −3f(x)]]. What is the slope of [[g(x)]]?", ["[[−3]]", "[[3]]", "[[−⅓]]", "[[−1]]"],
          "[[g(x) = −3x]]: stretched by 3 and reflected across the [[x]]-axis.", se=278),
        Q("Which line is parallel to [[y = −3x + 4]] and passes through [[(−1, 5)]]?", ["[[y = −3x + 2]]", "[[y = −3x + 8]]", "[[y = ⅓x + 5]]", "[[y = 3x + 8]]"],
          "[[5 = −3(−1) + b = 3 + b]], so [[b = 2]].", se=276),
        Q("[[f(x) = x]] and [[g(x) = ⅓f(x) + 2]]. Which describes [[g(x)]]?",
          ["Compressed vertically by ⅓, then up 2", "Stretched vertically by 3, then up 2", "Compressed vertically by ⅓, then right 2", "Translated up ⅓, then stretched by 2"],
          "[[g(x) = ⅓x + 2]]: the ⅓ compresses, the [[+ 2]] moves the graph up.", se=280),
    ],
    2: [
        Q("[[f(x) = x]] is translated left 3 units to make [[t(x)]]. Which is [[t(x)]]?", ["[[t(x) = f(x + 3) = x + 3]]", "[[t(x) = f(x − 3) = x − 3]]", "[[t(x) = f(x) − 3]]", "[[t(x) = 3f(x)]]"],
          "Left 3 adds 3 to the input: [[f(x + 3)]].", se=289),
        Q("A horizontal translation of [[f(x) = x]] changes which values in the table?", ["The input values", "The output values", "Both", "Neither"],
          "The outputs stay the same; each input moves left or right.", se=290),
        Q("For [[f(x) = x]], translating right [[n]] units gives the same graph as which translation?", ["Down [[n]] units", "Up [[n]] units", "Left [[n]] units", "Right [[2n]] units"],
          "[[f(x − n) = x − n = f(x) − n]].", se=291),
        Q("[[j(x) = 2x − 1]] and [[b(x) = j(x − 2)]]. Simplify [[b(x)]].", ["[[b(x) = 2x − 5]]", "[[b(x) = 2x − 3]]", "[[b(x) = 2x − 4]]", "[[b(x) = 2x + 3]]"],
          "[[2(x − 2) − 1 = 2x − 4 − 1 = 2x − 5]].", se=293),
        Q("[[j(x) = 2x − 1]], [[b(x) = j(x − 2)]] and [[v(x) = j(x) − 2]]. Are [[b(x)]] and [[v(x)]] the same?",
          ["No: [[b(x) = 2x − 5]] and [[v(x) = 2x − 3]] are parallel", "Yes, both are [[2x − 5]]", "Yes, both are [[2x − 3]]", "No, they are perpendicular"],
          "Right 2 and down 2 match only for [[f(x) = x]]. Here the [[y]]-intercepts differ.", se=294),
        Q("For [[f(x) = x]], the graph of [[f(½x)]] is the same as the graph of which function?", ["[[½f(x)]]", "[[2f(x)]]", "[[f(x) + ½]]", "[[f(x − ½)]]"],
          "[[f(½x) = ½x = ½f(x)]].", se=297),
        Q("[[f(x) = x]] and [[g(x) = f(x + 5)]]. Describe the transformation.", ["Translated left 5 units", "Translated right 5 units", "Translated up 5 units", "Stretched by 5"],
          "Adding 5 to the input moves the graph left 5.", se=300),
        Q("[[f(x) = x]] and [[g(x) = f(⅓x)]]. Describe the transformation.", ["Stretched horizontally by a factor of 3", "Compressed horizontally by a factor of ⅓", "Stretched vertically by 3", "Translated right ⅓"],
          "For [[f(bx)]] with [[0 < b < 1]], the graph stretches horizontally by [[1/b = 3]].", se=297),
        Q("Ricardo burns [[w(x) = 4x]] calories in [[x]] minutes of walking. Which domain fits the situation?", ["[[x ≥ 0]]", "All real numbers", "[[x ≤ 0]]", "[[x ≥ 4]]"],
          "He can't walk a negative number of minutes.", se=303),
        Q("Ricardo burns [[w(x) = 4x]] calories in [[x]] minutes. How many calories does he burn in 45 minutes?", ["[[180]]", "[[49]]", "[[11.25]]", "[[90]]"],
          "[[4 · 45 = 180]].", se=303),
    ],
    3: [
        Q("Line [[j]] has slope [[−⅘]]. What is the slope of a line perpendicular to [[j]]?", ["[[5/4]]", "[[−5/4]]", "[[⅘]]", "[[−⅘]]"],
          "The negative reciprocal of [[−⅘]] is [[5/4]].", se=309),
        Q("Line [[j]] has slope [[−3]]. What is the slope of a line perpendicular to [[j]]?", ["[[⅓]]", "[[−⅓]]", "[[3]]", "[[−3]]"],
          "[[−3 · ⅓ = −1]].", se=309),
        Q("Which line is perpendicular to [[y = 2x + 1]] and passes through [[(6, 2)]]?", ["[[y = −½x + 5]]", "[[y = −½x + 2]]", "[[y = 2x − 10]]", "[[y = ½x − 1]]"],
          "Slope [[−½]]: [[y − 2 = −½(x − 6)]], so [[y = −½x + 3 + 2 = −½x + 5]].", se=312),
        Q("A line passes through [[(−2, 7)]] and is perpendicular to the line through [[(−6, 1)]] and [[(0, 4)]]. Which is it?",
          ["[[y = −2x + 3]]", "[[y = ½x + 8]]", "[[y = −2x + 11]]", "[[y = 2x + 11]]"],
          "The given line has slope [[3/6 = ½]], so the new slope is [[−2]]: [[7 = −2(−2) + b]], [[b = 3]].", se=313),
        Q("Which line is perpendicular to [[x = 5]] and passes through [[(1, 0)]]?", ["[[y = 0]]", "[[x = 1]]", "[[y = 1]]", "[[x = 0]]"],
          "[[x = 5]] is vertical, so the perpendicular line is horizontal: [[y = 0]].", se=311),
        Q("Which line is perpendicular to [[y = −2]] and passes through [[(5, 6)]]?", ["[[x = 5]]", "[[y = 6]]", "[[y = 5]]", "[[x = −2]]"],
          "[[y = −2]] is horizontal, so the perpendicular line is vertical: [[x = 5]].", se=311),
        Q("Moonbeam Drive has slope [[−⅘]]. Which road is parallel to it through [[(20, 7)]]?", ["[[y = −⅘x + 23]]", "[[y = −⅘x + 7]]", "[[y = 5/4x − 18]]", "[[y = −⅘x − 9]]"],
          "[[7 = −⅘(20) + b = −16 + b]], so [[b = 23]].", se=316),
        Q("Moonbeam Drive has slope [[−⅘]]. Which road is perpendicular to it through [[(2, 6)]]?", ["[[y = 5/4x + 7/2]]", "[[y = −⅘x + 7.6]]", "[[y = 5/4x + 6]]", "[[y = 5/4x − 7/2]]"],
          "Slope [[5/4]]: [[6 = 5/4(2) + b = 5/2 + b]], so [[b = 7/2]].", se=316),
        Q("Buildings are at [[(8, 4)]] and [[(12, 10)]]. Is the road between them perpendicular to Moonbeam Drive (slope [[−⅘]])?",
          ["No: its slope is [[3/2]], not [[5/4]]", "Yes: its slope is [[5/4]]", "Yes: its slope is [[3/2]]", "No: its slope is [[−⅘]]"],
          "[[(10 − 4) ÷ (12 − 8) = 3/2]], and [[3/2 · (−⅘) = −6/5 ≠ −1]].", se=316),
        Q("What is the slope of any vertical line?", ["Undefined", "[[0]]", "[[1]]", "[[−1]]"],
          "The run is 0, and you can't divide by 0.", se=310),
    ],
    4: [
        Q("A table has the points [[(−4, 3)]], [[(0, 2)]], [[(2, 1.5)]] and [[(8, 0)]]. How does its line compare to [[y = 4x − 3]]?",
          ["Perpendicular", "Parallel", "Neither", "The same line"],
          "Slope [[= (2 − 3) ÷ (0 − (−4)) = −¼]], and [[4 · (−¼) = −1]].", se=321),
        Q("An elevator descends 4 feet every second. How does its graph compare to [[y = 4x − 3]]?", ["Neither parallel nor perpendicular", "Parallel", "Perpendicular", "The same line"],
          "Its slope is [[−4]]: not equal to 4, and [[4 · (−4) ≠ −1]].", se=321),
        Q("How does [[y = ¼x + 5]] compare to [[y = 4x − 3]]?", ["Neither parallel nor perpendicular", "Perpendicular", "Parallel", "The same line"],
          "[[4 · ¼ = 1]], not [[−1]], and the slopes are not equal.", se=321),
        Q("Travis pays [[w(x) = 15x]] and Hays pays [[j(x) = 20x]] dollars for [[x]] tons. Compare [[w(3)]] and [[j(3)]].", ["[[w(3) < j(3)]]", "[[w(3) > j(3)]]", "[[w(3) = j(3)]]", "Not enough information"],
          "[[w(3) = 45]] and [[j(3) = 60]].", se=322),
        Q("Both recycling functions have a [[y]]-intercept of 0. What does it mean?", ["$0 is paid for 0 tons", "The centers pay nothing", "The rate is $0 per ton", "0 tons are allowed"],
          "The [[y]]-intercept is the payout when the weight is 0.", se=322),
        Q("Xavier uses [[J(x) = 9/5x + 32]]. Which conversion does he make?", ["°C to °F", "°F to °C", "°C to °C", "Miles to kilometers"],
          "The input [[x]] is Celsius and the output [[J(x)]] is Fahrenheit.", se=323),
        Q("What does the [[y]]-intercept of [[J(x) = 9/5x + 32]] mean?", ["0°C is 32°F", "32°C is 0°F", "Each degree C is 32°F", "0°F is 32°C"],
          "At [[x = 0]] (0°C), [[J(0) = 32]] (32°F).", se=323),
        Q("Joey's table has [[(10, −12.2)]] and [[(50, 10)]] (°F, °C). What is its slope, about?", ["About [[5/9]]", "About [[9/5]]", "About [[−12.2]]", "About [[32]]"],
          "[[(10 − (−12.2)) ÷ (50 − 10) = 22.2 ÷ 40 ≈ 0.56 ≈ 5/9]].", se=323),
        Q("Lauren starts with $25 and deposits $25 each month. How much does she have after 3 months?", ["$100", "$75", "$50", "$28"],
          "[[25 + 25 · 3 = 100]].", se=324),
        Q("Brianna has 0 movies and buys 3 a month. Antonio has 27 and buys 2 a month. After how many months will they have the same number?",
          ["27", "9", "5", "54"],
          "[[3m = 27 + 2m]], so [[m = 27]]. Then both have 81.", se=329),
    ],
}

QUIZ = {
    1: [
        Q("Which changes when [[f(x)]] becomes [[f(x) + d]]?", ["The [[y]]-intercept only", "The slope only", "Both slope and [[y]]-intercept", "Neither"],
          "A vertical translation moves the line up or down; it stays parallel, so the slope is unchanged.", se=275),
        Q("[[(3, −1)]] is on [[f(x)]]. Which point is on [[g(x) = f(x) + 5]]?", ["[[(3, 4)]]", "[[(8, −1)]]", "[[(3, −6)]]", "[[(−2, −1)]]"],
          "Add 5 to the output: [[−1 + 5 = 4]].", se=273),
        Q("[[f(x) = x]] and [[g(x) = f(x) + 5]]. Which is [[g(x)]]?", ["[[g(x) = x + 5]]", "[[g(x) = 5x]]", "[[g(x) = x − 5]]", "[[g(x) = 5]]"],
          "[[f(x) + 5 = x + 5]].", se=274),
        Q("How is [[g(x) = 4f(x)]] related to [[f(x) = x]]?", ["Stretched vertically by a factor of 4", "Translated up 4", "Compressed vertically by ¼", "Translated right 4"],
          "Multiplying the output by 4 stretches the graph.", se=278),
        Q("How is [[g(x) = −f(x)]] related to [[f(x) = x]]?", ["Reflected across the [[x]]-axis", "Translated down 1", "Reflected across the line [[y = x]]", "Unchanged"],
          "Each output changes sign, which flips the graph across the [[x]]-axis.", se=278),
        Q("[[f(x) = x]] is compressed vertically by ½, then translated down 3. Which is the new function?", ["[[g(x) = ½x − 3]]", "[[g(x) = 2x − 3]]", "[[g(x) = ½x + 3]]", "[[g(x) = ½(x − 3)]]"],
          "[[½f(x) − 3 = ½x − 3]].", se=280),
        Q("Which line is parallel to [[y = ½x + 3]] and passes through [[(2, 9)]]?", ["[[y = ½x + 8]]", "[[y = ½x + 9]]", "[[y = −2x + 13]]", "[[y = 2x + 5]]"],
          "[[9 = ½(2) + b = 1 + b]], so [[b = 8]].", se=276),
        Q("Which pair of lines is parallel?", ["[[y = 2x − 1]] and [[y = 2x + 3]]", "[[y = 2x − 1]] and [[y = −2x − 1]]", "[[y = 2x]] and [[y = ½x]]", "[[y = x + 2]] and [[y = 2x + 1]]"],
          "Parallel lines have equal slopes and different [[y]]-intercepts.", se=276),
        Q("[[j(x) = 2x − 1]] and [[q(x) = j(x) + 4]]. Which is [[q(x)]]?", ["[[q(x) = 2x + 3]]", "[[q(x) = 2x + 4]]", "[[q(x) = 6x − 1]]", "[[q(x) = 2x − 5]]"],
          "[[2x − 1 + 4 = 2x + 3]].", se=275),
        Q("[[f(x) = x]]. Which function has slope [[−1]] and [[y]]-intercept [[(0, −4)]]?", ["[[g(x) = −f(x) − 4]]", "[[g(x) = f(x) − 4]]", "[[g(x) = −4f(x)]]", "[[g(x) = −f(x) + 4]]"],
          "[[−f(x) − 4 = −x − 4]].", se=282),
    ],
    2: [
        Q("[[f(x) = x]] and [[g(x) = f(x − 7)]]. Describe the transformation.", ["Translated right 7 units", "Translated left 7 units", "Translated down 7 units", "Stretched by 7"],
          "Subtracting 7 from the input moves the graph right 7.", se=298),
        Q("[[f(x) = x]] and [[g(x) = 3f(x)]]. Describe the transformation.", ["Stretched vertically by a factor of 3", "Compressed horizontally by ⅓ only", "Translated up 3", "Translated right 3"],
          "Multiplying the output by 3 is a vertical stretch. (For [[f(x) = x]] it matches [[f(3x)]].)", se=298),
        Q("For [[f(x) = x]], which gives the same graph as a translation down 4?", ["[[f(x − 4)]]", "[[f(x + 4)]]", "[[4f(x)]]", "[[f(x) + 4]]"],
          "[[f(x − 4) = x − 4 = f(x) − 4]].", se=291),
        Q("[[m(x) = 2x − 1]]. Compare [[3m(x)]] and [[m(3x)]].", ["Parallel: [[6x − 3]] and [[6x − 1]]", "The same: both [[6x − 3]]", "The same: both [[6x − 1]]", "Perpendicular"],
          "[[3(2x − 1) = 6x − 3]], but [[2(3x) − 1 = 6x − 1]].", se=297),
        Q("For [[f(x) = x]], which transformation is the same as [[k(x) = f(x) + 8]]?", ["[[f(x + 8)]]", "[[f(x − 8)]]", "[[8f(x)]]", "[[f(8x)]]"],
          "[[x + 8]] is both up 8 and left 8 for the parent function.", se=301),
        Q("[[f(x) = x]] is compressed horizontally by a factor of ½. Which is the new function?", ["[[g(x) = f(2x) = 2x]]", "[[g(x) = f(½x) = ½x]]", "[[g(x) = f(x) + 2]]", "[[g(x) = f(x − 2)]]"],
          "For [[f(bx)]] with [[|b| > 1]], the graph compresses horizontally by [[1/b = ½]].", se=296),
        Q("In [[a · f(b(x − c)) + d]], which constants change the input values?", ["[[b]] and [[c]]", "[[a]] and [[d]]", "[[a]] and [[b]]", "[[c]] and [[d]]"],
          "[[b]] and [[c]] are inside with [[x]]: horizontal changes.", se=303),
        Q("[[j(x) = 2x − 1]]. Simplify [[j(x + 4)]].", ["[[2x + 7]]", "[[2x + 3]]", "[[2x + 4]]", "[[8x − 1]]"],
          "[[2(x + 4) − 1 = 2x + 7]].", se=292),
        Q("For [[f(x) = x]], a vertical dilation by [[⅘]] gives the same graph as a horizontal dilation by which factor?", ["[[5/4]]", "[[⅘]]", "[[−⅘]]", "[[1]]"],
          "A vertical dilation by [[n]] matches a horizontal dilation by [[1/n]].", se=297),
        Q("What is the reciprocal of [[−⅘]]?", ["[[−5/4]]", "[[5/4]]", "[[⅘]]", "[[−1]]"],
          "[[−⅘ · (−5/4) = 1]].", se=304),
    ],
    3: [
        Q("Are [[y = ¾x + 1]] and [[y = −4/3x − 2]] perpendicular?", ["Yes, the slopes multiply to [[−1]]", "No, they are parallel", "No, the slopes are not equal", "Cannot tell"],
          "[[¾ · (−4/3) = −1]].", se=308),
        Q("How are [[y = 2x]] and [[y = −2x]] related?", ["Neither parallel nor perpendicular", "Perpendicular", "Parallel", "The same line"],
          "[[2 · (−2) = −4]], not [[−1]], and the slopes are not equal.", se=309),
        Q("Which line is perpendicular to [[y = −¾x]] and passes through [[(3, −8)]]?", ["[[y = 4/3x − 12]]", "[[y = −¾x − 5.75]]", "[[y = 4/3x − 4]]", "[[y = −4/3x − 4]]"],
          "Slope [[4/3]]: [[−8 = 4/3(3) + b = 4 + b]], so [[b = −12]].", se=312),
        Q("Which line passes through [[(6, 2)]] and is perpendicular to the line through [[(−5, 3)]] and [[(−1, −9)]]?", ["[[y = ⅓x]]", "[[y = −3x + 20]]", "[[y = ⅓x + 2]]", "[[y = 3x − 16]]"],
          "Given slope [[−12/4 = −3]], so the new slope is [[⅓]]: [[2 = ⅓(6) + b]], [[b = 0]].", se=312),
        Q("Two perpendicular lines meet at [[(5, 9)]]. One passes through [[(−4, 4)]]. Which is the other line?", ["[[y = −9/5x + 18]]", "[[y = 5/9x + 56/9]]", "[[y = −9/5x + 9]]", "[[y = 9/5x]]"],
          "Slope through the points [[= 5/9]], so the other slope is [[−9/5]]: [[9 = −9/5(5) + b]], [[b = 18]].", se=313),
        Q("Rotating [[(a, b)]] 90° counterclockwise about the origin gives which point?", ["[[(−b, a)]]", "[[(b, −a)]]", "[[(−a, −b)]]", "[[(a, −b)]]"],
          "This is the rotation used in the proof that perpendicular slopes are negative reciprocals.", se=308),
        Q("“All horizontal lines are parallel.” Is this always, sometimes, or never true?", ["Always", "Sometimes", "Never", "Only through the origin"],
          "Every horizontal line has slope 0.", se=311),
        Q("Which is the horizontal line through [[(2, −1)]]?", ["[[y = −1]]", "[[x = 2]]", "[[y = 2]]", "[[x = −1]]"],
          "Every point on a horizontal line has the same [[y]]-value.", se=311),
        Q("What is the slope of a line perpendicular to a line with slope [[⅕]]?", ["[[−5]]", "[[5]]", "[[−⅕]]", "[[⅕]]"],
          "[[⅕ · (−5) = −1]].", se=309),
        Q("Lines with slope 1 and lines with slope [[−¼]] look perpendicular on a graph. Are they?", ["No: [[1 · (−¼) ≠ −1]]", "Yes, they look it", "Yes: [[1 · (−¼) = −1]]", "Only if they cross at the origin"],
          "Different axis scales can make lines look perpendicular. Check the slopes.", se=314),
    ],
    4: [
        Q("Which function is decreasing?", ["A table with [[(−5, 10)]], [[(0, 0)]] and [[(2.5, −5)]]", "[[c(x) = ⅕x]]", "A 1 : 1 ratio of 9th- to 10th-graders", "A line through [[(0, 5)]] and [[(1, 10)]]"],
          "The table's slope is [[−2]]; the others have positive slopes.", se=320),
        Q("Which line is perpendicular to [[y = 4x − 3]]?", ["[[y = −¼x + 2]]", "[[y = 4x + 2]]", "[[y = ¼x − 3]]", "[[y = −4x − 3]]"],
          "The slope must be the negative reciprocal of 4.", se=321),
        Q("For every hour Chiletso bakes, she makes 4 dozen cookies. How does this compare to [[y = 4x − 3]]?", ["Parallel", "Perpendicular", "Neither", "The same line"],
          "Both have slope 4 but different [[y]]-intercepts.", se=321),
        Q("Travis County pays $15 per ton; Hays County's graph shows $20 per ton. Which is true?", ["Hays pays $5 more per ton", "Travis pays more per ton", "They pay the same", "Hays pays $20 less per ton"],
          "Compare the slopes: 20 > 15.", se=322),
        Q("Miguel saves $20 a month from $0. Lauren starts with $25 and saves $25 a month. Compare the slopes.", ["Lauren's is greater (25 > 20)", "Miguel's is greater", "They are equal", "Neither has a slope"],
          "The slope is the monthly deposit.", se=324),
        Q("What does the [[y]]-intercept of Miguel's account (0) mean?", ["He started with $0", "He saves $0 each month", "He has $0 after 4 months", "The graph has no [[y]]-intercept"],
          "The [[y]]-intercept is the amount at 0 months.", se=324),
        Q("What is the slope of this table?", ["[[¼]]", "[[4]]", "[[½]]", "[[2.5]]"],
          "[[(5 − 0) ÷ (10 − (−10)) = 5 ÷ 20 = ¼]].", se=325,
          extra=table([["−10", "10", "20", "25"], ["0", "5", "7.5", "8.75"]], None).replace("<tr><td>−10", "<tr><th>x</th><td>−10").replace("<tr><td>0<", "<tr><th>y</th><td>0<")),
        Q("What is the [[y]]-intercept of the same table ([[x]]: −10, 10, 20, 25; [[y]]: 0, 5, 7.5, 8.75)?", ["[[(0, 2.5)]]", "[[(0, 0)]]", "[[(−10, 0)]]", "[[(0, 5)]]"],
          "From [[(−10, 0)]], move right 10 at slope [[¼]]: up 2.5.", se=325),
        Q("Which equation is less steep than a slope of [[¼]]?", ["[[y = 0.2x + 30]]", "[[y = ⅓x − 4]]", "[[y = x]]", "[[y = 0.3x]]"],
          "[[0.2 < 0.25]].", se=325),
        Q("Joey's table converts °F to °C with a [[y]]-intercept of about [[−17.8]]. What does it mean?", ["0°F is about −17.8°C", "0°C is about −17.8°F", "It drops 17.8° per degree", "It has no meaning"],
          "The input is °F, so at 0°F the output is about −17.8°C.", se=323),
    ],
}


if __name__ == "__main__":
    for (l, d), qs in BELL.items():
        page(f"t2-lesson{l}-bellwork-day{d}.html", f"Topic 2 Lesson {l} Day {d} Bell Work · {LESSONS[l]}",
             f"Module 2 · Topic 2 · Lesson {l} · Day {d} Bell Work", "Bell Work: Review",
             "Warm up while attendance is taken. Answer all 4 questions, then submit to see which ones you got right.", "quiz", qs)
    for l, qs in HOMEWORK.items():
        page(f"t2-lesson{l}-homework.html", f"Topic 2 Lesson {l} Homework · {LESSONS[l]}",
             f"Module 2 · Topic 2 · Lesson {l} · Homework", f"{LESSONS[l]} Practice",
             "Pick an answer for each question. You'll see right away whether it's correct, and why. The page numbers point "
             "to your Student Edition if you want to look back.", "homework", qs)
    for l, qs in QUIZ.items():
        page(f"t2-lesson{l}-quiz.html", f"Topic 2 Lesson {l} Quiz · {LESSONS[l]}",
             f"Module 2 · Topic 2 · Lesson {l} · Quiz", f"{LESSONS[l]} Quiz",
             "Answer all 10 questions, then submit. You'll see your score and the correct answers after you submit.", "quiz", qs)

    for qs in [*BELL.values(), *HOMEWORK.values(), *QUIZ.values()]:  # every question: 4 distinct choices
        for q in qs:
            assert len(q["choices"]) == 4 and len(set(q["choices"])) == 4, q["q"]
    print(len(BELL), "bell work,", len(HOMEWORK), "homework,", len(QUIZ), "quizzes")

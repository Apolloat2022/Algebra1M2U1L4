"""Module 3 Topic 2 (Systems of Linear Equations and Inequalities), Lessons 1-5: slide decks in the General, IEP and
Section 504 versions, each with a .pptx copy. Same engine and helpers as make_m3t1_lessons.py. Slides only: no bell work,
exit tickets or dated agendas yet. Lesson 6 is 0 days on the 150-day pacing guide, so it is not built.
Days and stars (essential activities) come from the 150-day pacing guide, Module 3 Topic 2 p. 4.
Run:  python make_m3t2_lessons.py [1 2 ...]"""
import re
from fractions import Fraction as Fr
from pathlib import Path

import make_t2_decks as D
import make_accom_lessons as A
from make_m3t1_lessons import doc, pptx

ROOT = Path(__file__).parent
OUT = ROOT / "Module 3 topic 2"
FOLDER = {"504": ROOT / "Section 504", "IEP": ROOT / "IEP"}
LABEL = {"504": "Section 504", "IEP": "IEP"}
M, mt, eq, ans, st, p, sec, row, card, table, graph, L = D.M, D.mt, D.eq, D.ans, D.st, D.p, D.sec, D.row, D.card, D.table, D.graph, D.L
STAR = D.ESSENTIAL
D.STARS.update({"m3t2l1": {"Getting Started", "1.1", "1.2", "1.3"}, "m3t2l2": {"2.1", "2.2", "2.3"},
                "m3t2l3": {"Getting Started", "3.1", "3.2", "3.3", "3.4"}, "m3t2l4": {"4.1", "4.2", "4.3"},
                "m3t2l5": {"Getting Started", "5.1", "5.2"}})

# The deck engine (copied from lesson6's deck) learns one new trick: shaded regions for inequality graphs.
SHADE_JS = ("  for (const sh of g.shade || []) s += `<polygon style=\"fill:var(--g${sh.c || 'a'});fill-opacity:.22\" points=\"${"
            "sh.p.map(([a, b]) => X(a) + ',' + Y(b)).join(' ')}\"/>`;\n")
ANCHOR_JS = "  const ptsSVG = () =>"
assert ANCHOR_JS in D.TAIL
TAIL = D.TAIL.replace(ANCHOR_JS, SHADE_JS + ANCHOR_JS, 1)


def deck_doc(title_, slides):
    return doc(title_, slides).replace(D.TAIL, TAIL)


# ================================================================ graph helpers
def hp(cons, xr, yr):
    """Region where every a*x + b*y + c >= 0 holds, clipped to the window: polygon corners in graph units."""
    poly = [(xr[0], yr[0]), (xr[1], yr[0]), (xr[1], yr[1]), (xr[0], yr[1])]
    for a, b, c in cons:
        f = lambda q: a * q[0] + b * q[1] + c
        out = []
        for i, q in enumerate(poly):
            r = poly[(i + 1) % len(poly)]
            if f(q) >= 0:
                out.append(q)
            if (f(q) >= 0) != (f(r) >= 0):
                t = f(q) / (f(q) - f(r))
                out.append((q[0] + t * (r[0] - q[0]), q[1] + t * (r[1] - q[1])))
        poly = out
    return [[round(float(x), 4), round(float(y), 4)] for x, y in poly]


above = lambda m, b: (-m, 1, -b)   # y >= mx + b
below = lambda m, b: (m, -1, b)    # y <= mx + b


def gshade(w, h, xr, yr, gx, gy, lines, pts, shades, alt):
    """graph() plus shade: [(constraints, color)]."""
    html = graph(w, h, xr, yr, gx, gy, lines, pts, alt)
    data = re.search(r"data-g='(.*)'", html).group(1)
    import json
    g = json.loads(data.replace("&#39;", "'"))
    g["shade"] = [{"p": hp(c, xr, yr), "c": col} for c, col in shades]
    return "<div class=\"graph\" data-g='" + json.dumps(g, ensure_ascii=False).replace("'", "&#39;") + "'></div>"


def line(m, b, xr, label=None, c=None, dash=False, step=False):
    return L((xr[0], m * xr[0] + b), (xr[1], m * xr[1] + b), label, c, step, dash)


# ================================================================ shared slides
def title_slide(n, pages, name, sub, notes):
    return (f'<section class="slide">\n  <p class="eyebrow">Bluebonnet Algebra I · Module 3 · Topic 2 · Lesson {n} · Student Edition pp. {pages}</p>\n'
            f'  <h1 style="margin-top:6px;font-size:56px">{name}</h1>\n  <div class="eq" style="margin-top:8px;font-size:40px">{sub}</div>\n'
            f'  <p class="muted small">Click, or press → / Space, to reveal each step. ← goes back. F = full screen.</p>\n  {D.FOOT}\n'
            f'  <aside class="notes">{notes}</aside>\n</section>\n')


def divider(n, d, q, recap):
    return sec(f"Lesson {n}", f"Day {d}", f'<p class="step" style="font-size:32px;max-width:900px">Essential Question: {q}</p>',
               f"Have a student read the Essential Question aloud. Ask two or three students to summarize Day {d - 1}: {recap}", True)


def homework(n, se, items, key):
    return sec("Homework", f"Lesson {n} Assignment · SE pp. {se}", row(*[card(h, p(b)) for h, b in items], gap=24), key)


def eq_done(q, points, notes="Have students answer the Essential Question on the lesson opener page."):
    return sec("Essential Question · Answered", q, '<div class="col" style="gap:20px;margin-top:6px">'
               + "".join(st(t, "") for t in points) + "</div>", notes)


# ================================================================ Lesson 1 · Using Graphing to Solve Systems of Equations
def deck1():
    eqq = "How can you solve problems that require two linear functions?"
    T = graph(420, 330, [0, 700], [0, 500], [50, 100], [50, 100],
              [L((0, 300), (600, 0), "5s + 10a = 3000", "a"), L((0, 450), (450, 0), "s + a = 450", "b", True)],
              [[300, 150, "(300, 150)"]], "Ticket sales: two lines crossing at (300, 150)")
    d1 = [title_slide(1, "393–410", "Using Graphing to Solve Systems of Equations", "two lines · one point that works for both",
                      "Two days on the 150-day calendar. Day 1: Getting Started, Activities 1.1 and 1.2. Day 2: Activity 1.3 and Talk the Talk. "
                      "Every part is starred (essential). Students need graph paper and graphing technology."),
          D.today(1, 393, ["Write equations in standard form and use the intercepts to graph them.",
                           "Write a system of equations to represent a problem context.",
                           "Use a graph to solve a system of linear equations and interpret the solution.",
                           "Use slopes and y-intercepts to tell whether a system has one, no, or infinite solutions."],
                  "New key terms: system of linear equations · consistent systems · inconsistent systems"),
          D.eq_slide(1, 393, "You have examined different linear functions and solved for unknown values.", eqq),
          sec("Getting Started · Ticket Tabulation · SE p. 394", "Raise $3000 with $5 student and $10 adult tickets",
              row(p("1. Write an equation for the situation. Let " + mt("s") + " = student tickets and " + mt("a") + " = adult tickets.", "")
                  + ans("5s + 10a = 3000"),
                  card("2. Some combinations that reach the goal", st(mt("600") + " student, " + mt("0") + " adult")
                       + st(mt("200") + " student, " + mt("200") + " adult") + st(mt("0") + " student, " + mt("300") + " adult"))
                  + st("3. Classmates get different answers: one equation in two unknowns has <b>many</b> solutions.")),
              "Getting Started, about 10 minutes. Collect several combinations on the board; every one is a point on the same line."),
          sec("Activity 1.1 · Graph Using Intercepts · SE p. 395", "Standard form: graph with the intercepts",
              row(st("<b>x-intercept</b>: let " + mt("a = 0") + ": " + mt("5s = 3000") + " → " + mt("(600, 0)"))
                  + st("<b>y-intercept</b>: let " + mt("s = 0") + ": " + mt("10a = 3000") + " → " + mt("(0, 300)"))
                  + st("Slope " + mt("= −300/600 = −½") + ": for every 2 more student tickets, 1 fewer adult ticket.")
                  + st("Domain, real world: whole numbers " + mt("0 ≤ s ≤ 600") + ". Range: " + mt("0 ≤ a ≤ 300") + "."),
                  graph(380, 300, [0, 700], [0, 400], [50, 100], [50, 100], [L((0, 300), (600, 0), "5s + 10a = 3000", "a")],
                        [[600, 0, "(600, 0)"], [0, 300, "(0, 300)"]], "Line through (600, 0) and (0, 300)", True)),
              "Questions 1–5. The mathematical function has all real numbers for its domain and range; the situation only allows whole numbers of tickets."),
          sec("Activity 1.1 · Ethan's Graph · SE pp. 396–397", "Same equation, axes switched",
              row(card("Ethan: adult tickets on the x-axis", st("Intercepts " + mt("(300, 0)") + " and " + mt("(0, 600)"))
                       + st("Slope " + mt("−2") + ": 1 more adult ticket replaces 2 student tickets.")),
                  card("What stays the same", st("The same combinations meet the goal; only the axes are switched.")
                       + st("Neither graph shows the money: every point on the line is exactly $3000.")), gap=24),
              "Questions 6–12. Ethan's graph is correct; the domain and range trade places."),
          sec("Activity 1.2 · Determining the Solution · SE p. 398", "450 tickets were sold. How many of each?",
              row(st("Second equation: " + mt("s + a = 450"))
                  + p("Two or more linear equations about the same quantities form a <b>system of linear equations</b>.", "small")
                  + st("The lines cross at " + mt("(300, 150)") + ": 300 student and 150 adult tickets.")
                  + ans("Check: " + mt("5(300) + 10(150) = 3000") + " ✓ · " + mt("300 + 150 = 450") + " ✓", True), T),
              "Questions 1–5. Use graphing technology to find the exact intersection: graph both lines, then use the intersect tool. "
              "There is only one solution because the lines cross once."),
          ]
    d2 = [divider(1, 2, eqq, "the point where two lines intersect makes both equations true."),
          sec("Activity 1.3 · Samuel and Diego · SE p. 400", "Both save $10 a week. Samuel starts with $25, Diego with $40.",
              row(st("Samuel: " + mt("y = 10x + 25")) + st("Diego: " + mt("y = 10x + 40"))
                  + st("Same slope (same weekly savings), different y-intercepts (different start).")
                  + ans("Parallel lines: they never have the same amount. No solution.", True),
                  graph(380, 300, [0, 9], [0, 140], [1, 1], [10, 20], [line(10, 25, (0, 9), "Samuel", "a"), line(10, 40, (0, 9), "Diego", "b", step=True)], [],
                        "Two parallel lines")),
              "Questions 1–6. Students predict first. Diego is always $15 ahead."),
          sec("Activity 1.3 · Isabella and Diego · SE pp. 402–404", "Same start, different rates, then the same rate",
              row(card("Isabella saves $4 a week", st(mt("y = 4x + 40") + " and " + mt("y = 10x + 40"))
                       + st("Different slopes, same y-intercept.") + ans("One solution: (0, 40), the day they start", True)),
                  card("Then she saves $4 + $6 = $10 a week", st(mt("y = 10x + 40") + " and " + mt("y = 10x + 40"))
                       + st("Same slope, same y-intercept: the same line.") + ans("Infinite solutions. Diego's claim is false.", True)), gap=24),
              "Questions 7–11. Don't forget to define the variables: x = weeks, y = dollars saved."),
          sec("Talk the Talk · Beating the System · SE p. 405 · " + STAR, "One solution, no solution, or infinite solutions",
              table(["Slopes", "y-intercepts", "Graph", "Solutions", "System"],
                    [["different", "same or different", "lines intersect", "one", "consistent"],
                     ["same", "different", "parallel lines", "none", "inconsistent"],
                     ["same", "same", "same line", "infinite", "consistent"]], 24, (2, 3, 4)),
              "Question 2: the coordinates of the intersection are on both lines, so they make both equations true."),
          eq_done(eqq, ["Write an equation for each relationship, graph both on the same plane, and find where they intersect.",
                        "The intersection point is the solution: it makes both equations true.",
                        "Compare slopes and y-intercepts to know how many solutions to expect."]),
          homework(1, "407–409", [("Practice", "1. Mr. Nguyen's test: write the equation, find three combinations, graph with intercepts."),
                                  ("Practice", "2. Harper's milking: write and graph the system, estimate and interpret the intersection."),
                                  ("Practice", "3. Consistent or inconsistent? Explain.")],
                   "Key 1a: 2c − 0.5i = 80; for example (40, 0), (41, 4), (42, 8). 2a: hand y = 0.2x + 0.3, machine y = 0.05x + 0.4; they are equal at "
                   "x = ⅔ cow, so for any real herd the machine is faster. Consistent: the lines intersect.")]
    return [d1, d2]


# ================================================================ Lesson 2 · Using Substitution to Solve Linear Systems
def deck2():
    eqq = "If the intersection is not clear from a graph, how can you determine the solution to a system?"
    d1 = [title_slide(2, "411–431", "Using Substitution to Solve Linear Systems", "replace a variable with an equal expression",
                      "Two days on the 150-day calendar. Day 1: Getting Started and Activity 2.1. Day 2: Activities 2.2, 2.3 and Talk the Talk. "
                      "Activities 2.1–2.3 are starred; Getting Started and Talk the Talk are not, so shorten them if time is tight."),
          D.today(2, 411, ["Write a system of equations to represent a problem context.",
                           "Solve a system of equations algebraically using substitution.",
                           "Interpret the solution in terms of the problem situation."], "New key term: substitution method"),
          D.eq_slide(2, 411, "You have graphed systems of equations.", eqq),
          sec("Getting Started · Goats, Chickens, and Pigs · SE p. 412", "Is the third trade fair?",
              row(st("Trade 1: 4 goats = 5 chickens") + st("Trade 2: 1 pig = 2 chickens + 1 goat")
                  + st("Trade 3: Lyndi's 3 chickens + 1 pig against Simpson's 4 goats."),
                  st("Replace the pig: " + mt("3C + (2C + G) = 5C + G")) + st("Replace the goats: " + mt("4G = 5C"))
                  + ans("Lyndi's side is worth 1 goat more. Simpson adds 1 goat to make it fair.", True)),
              "Not starred. This is substitution without the name: swap something for what it equals."),
          sec("Activity 2.1 · Introduction to Substitution · SE p. 413", "Sofia's $30 potato salad",
              row(st("Onions $1.25/lb, potatoes $1.05/lb: " + mt("1.25x + 1.05y = 30"))
                  + st("8 times as many pounds of potatoes: " + mt("y = 8x"))
                  + st("Does (1, 8) work? " + mt("1.25 + 8.40 = 9.65 ≠ 30") + ": no."),
                  graph(380, 300, [0, 6], [0, 40], [0.5, 1], [5, 10], [L((0, 30 / 1.05), (6, (30 - 7.5) / 1.05), "1.25x + 1.05y = 30", "a"),
                                                                       L((0, 0), (5, 40), "y = 8x", "b")], [[3.1, 24.8, ""]],
                        "The lines cross near (3.1, 24.8)")),
              "Questions 1–6. The graph only gives an estimate; the exact point is hard to read. That is why we need an algebraic method."),
          sec("Activity 2.1 · Worked Example · SE p. 415", "The substitution method",
              row(st("<b>Step 1</b> Pick an equation with a variable alone: " + mt("y = 8x"))
                  + st("<b>Step 2</b> Substitute " + mt("8x") + " for " + mt("y") + ": " + mt("1.25x + 1.05(8x) = 30"))
                  + st("<b>Step 3</b> Solve: " + mt("9.65x = 30") + ", so " + mt("x ≈ 3.1")) + st("Then " + mt("y = 8(3.1) = 24.8")),
                  st("<b>Step 4</b> Check in both equations:") + st(mt("1.25(3.1) + 1.05(24.8) ≈ 30") + " ✓")
                  + ans("About 3.1 lb of onions and 24.8 lb of potatoes", True)),
              "Questions 7–9. The substitution method replaces a variable in one equation with an equivalent expression from the other equation."),
          ]
    d2 = [divider(2, 2, eqq, "substitution turns two equations into one equation with one unknown."),
          sec("Activity 2.2 · Substitution with Special Systems · SE pp. 417–419", "Daniel and Chloe earn $7 an hour",
              row(st("Daniel starts at 7:00: " + mt("y = 7x")) + st("Chloe starts 90 minutes later: " + mt("y = 7(x − 1.5) = 7x − 10.5"))
                  + st("By noon: Daniel $35, Chloe $24.50."),
                  st("Substitute: " + mt("7x = 7x − 10.5")) + st(mt("0 = −10.5")) + ans("False: no solution. Parallel lines; Chloe never catches up.", True)),
              "Questions 1–9. When the variable disappears and the statement is false, the system has no solution."),
          sec("Activity 2.2 · Same Line · SE pp. 419–420", "$4 tickets, 5 tickets, $20",
              row(st(mt("4x + 4y = 20") + " → " + mt("y = −x + 5")) + st(mt("x + y = 5") + " → " + mt("y = −x + 5")),
                  st("Substitute: " + mt("−x + 5 = −x + 5")) + st(mt("5 = 5"))
                  + ans("Always true: infinite solutions. Any 5 tickets cost $20.", True)),
              "Questions 10–16. When the variable disappears and the statement is true, the two equations are the same line."),
          sec("Activity 2.3 · Writing and Solving Systems · SE pp. 421–422", "Band tickets: $236,000 from 4000 seats",
              row(st("2800 main-level seats at " + mt("x") + " dollars, 1200 upper-level at " + mt("y") + " dollars.")
                  + st(mt("2800x + 1200y = 236000")) + st("Main level costs $20 more: " + mt("x = y + 20")),
                  st(mt("2800(y + 20) + 1200y = 236000")) + st(mt("4000y + 56000 = 236000") + " → " + mt("y = 45"))
                  + ans("Main level $65, upper level $45", True)),
              "Questions 1–4. Question 1 asks only for the system. Check: 2800(65) + 1200(45) = 182,000 + 54,000 = 236,000."),
          sec("Talk the Talk · The Substitution Train · SE pp. 424–425", "Solve each system by substitution",
              row(card("a. " + mt("2x + 3y = 34") + ", " + mt("y = 5x"), st(mt("17x = 34")) + ans("(2, 10)")),
                  card("b. " + mt("y = 4x + 2") + ", " + mt("y = 3x − 2"), st(mt("4x + 2 = 3x − 2")) + ans("(−4, −14)")),
                  card("c. " + mt("3x + 2y = 4") + ", " + mt("2x − y = 5"), st(mt("y = 2x − 5") + " → " + mt("7x − 10 = 4")) + ans("(2, −1)")),
                  card("d. " + mt("3x + y = 8") + ", " + mt("6x + 2y = 10"), st(mt("6x + 2(8 − 3x) = 10") + " → " + mt("16 = 10")) + ans("No solution", True)), gap=14),
              "Not starred; use as practice or an exit check. Have students check each answer in both equations."),
          eq_done(eqq, ["Solve one equation for a variable, substitute that expression into the other equation, solve, then substitute back.",
                        "A false statement (like 0 = −10.5) means no solution. A true statement (like 5 = 5) means infinite solutions."]),
          homework(2, "427–431", [("Practice", "1. Victoria's furniture polish: write, solve and interpret two systems."),
                                  ("Practice", "2. Juan's snacks: define variables, solve by substitution, interpret."),
                                  ("Practice", "3–4. Write systems from descriptions, graphs, tables; solve four systems.")],
                   "Key 1c: x + y = 48, y = 2x → 16 oz lemon juice, 32 oz olive oil. 1f: x + y = 84, 0.25x + 0.39y = 29.40 → 24 oz lemon juice, "
                   "60 oz olive oil. 2c: 10s + 8w = 192, 20s + w = 99 → 4 calories per strawberry, 19 per wafer.")]
    return [d1, d2]


# ================================================================ Lesson 3 · Using Linear Combinations
def deck3():
    eqq = "What are other algebraic strategies for solving systems of equations?"
    d1 = [title_slide(3, "433–447", "Using Linear Combinations to Solve a System of Linear Equations", "add the equations so one variable drops out",
                      "Three days on the 150-day calendar. Day 1: Getting Started and Activity 3.1. Day 2: Activities 3.2 and 3.3. "
                      "Day 3: Activity 3.4 and Talk the Talk. Every part is starred."),
          D.today(3, 433, ["Write a system of equations to represent a problem context.",
                           "Solve a system of equations algebraically using linear combinations.",
                           "Interpret the solution in terms of a problem situation."], "New key term: linear combinations method"),
          D.eq_slide(3, 433, "You have solved systems by graphing and by substitution.", eqq),
          sec("Getting Started · Coding Class · SE p. 434", "324 students; 9th graders outnumber 10th graders by 34",
              row(st("Take away the extra 34: " + mt("324 − 34 = 290")) + st("Split evenly: " + mt("290 ÷ 2 = 145") + " tenth graders"),
                  ans("179 ninth graders and 145 tenth graders", True) + st("Check: " + mt("179 + 145 = 324") + " and " + mt("179 − 145 = 34"))),
              "Students reason first, without a system. Ask how they could check."),
          sec("Activity 3.1 · Combining Linear Systems · SE pp. 435–436", "Mateo substitutes; Minh adds the equations",
              row(card("Mateo", st(mt("x = y + 34")) + st(mt("(y + 34) + y = 324")) + st(mt("y = 145, x = 179"))),
                  card("Minh", st(mt("x + y = 324")) + st(mt("x − y = 34")) + st("Add: " + mt("2x = 358")) + st(mt("x = 179, y = 145"))), gap=24)
              + st("Minh's way works because " + mt("y") + " and " + mt("−y") + " add to zero. That is the <b>linear combinations method</b>."),
              "Questions 1–4. The solution is (179, 145): 179 ninth graders and 145 tenth graders."),
          sec("Activity 3.1 · Question 5 · SE p. 436", "Add the equations, then substitute back",
              row(card("a. " + mt("−4x + y = 10") + " and " + mt("−2x − y = −1"), st("Add: " + mt("−6x = 9") + " → " + mt("x = −1.5"))
                       + st(mt("−4(−1.5) + y = 10") + " → " + mt("y = 4")) + ans("(−1.5, 4)")),
                  card("b. " + mt("−½x + 5y = −6") + " and " + mt("½x + y = −6"), st("Add: " + mt("6y = −12") + " → " + mt("y = −2"))
                       + st(mt("½x − 2 = −6") + " → " + mt("x = −8")) + ans("(−8, −2)")), gap=24),
              "Have students check each solution in both equations."),
          ]
    d2 = [divider(3, 2, eqq, "add two equations when a variable has opposite coefficients, so it drops out."),
          sec("Activity 3.2 · Using Additive Inverses · SE p. 437", "Multiply first to make opposites",
              row(st(mt("7x + 2y = 24")) + st(mt("4x + y = 15") + " × (−2): " + mt("−8x − 2y = −30"))
                  + st("Add: " + mt("−x = −6") + ", so " + mt("x = 6")) + st(mt("7(6) + 2y = 24") + " → " + mt("y = −9")),
                  ans("(6, −9)") + st("Check: " + mt("4(6) + (−9) = 15") + " ✓")
                  + st("Only one equation needed to change: the 2" + mt("y") + " was already a multiple of " + mt("y") + ".")),
              "Worked Example and Question 1. Additive inverses: two numbers with a sum of zero."),
          sec("Activity 3.2 · Both Equations Change · SE pp. 438–439", "When neither coefficient is a multiple of the other",
              row(card(mt("4x + 2y = 3") + ", " + mt("5x + 3y = 4"), st("× 3 and × (−2): " + mt("12x + 6y = 9") + ", " + mt("−10x − 6y = −8"))
                       + st("Add: " + mt("2x = 1") + " → " + mt("x = ½")) + ans("(½, ½)")),
                  card(mt("4x + 3y = 12") + ", " + mt("3x + 2y = 4"), st("× 2 and × (−3): " + mt("8x + 6y = 24") + ", " + mt("−9x − 6y = −12"))
                       + st("Add: " + mt("−x = 12") + " → " + mt("x = −12")) + ans("(−12, 20)")), gap=24),
              "Worked Example 2 and Questions 2–5. Question 3: you could also make the x-terms opposites with × 5 and × (−4)."),
          sec("Activity 3.3 · Applying the Method · SE pp. 440–441", "Let It Snow: lodging and meals",
              row(st("Get-Away: " + mt("2n + 4m = 270")) + st("Extended Stay: " + mt("3n + 8m = 435"))
                  + st("× (−2) the first: " + mt("−4n − 8m = −540")),
                  st("Add: " + mt("−n = −105") + " → " + mt("n = 105")) + st(mt("2(105) + 4m = 270") + " → " + mt("m = 15"))
                  + ans("$105 a night, $15 a meal", True) + st("Both specials use the same prices, so neither is a better deal per item.")),
              "Questions 1–6. Check: 3(105) + 8(15) = 315 + 120 = 435."),
          ]
    d3 = [divider(3, 3, eqq, "multiply one or both equations so a variable has opposite coefficients."),
          sec("Activity 3.4 · Fractions and Linear Combinations · SE pp. 442–443", "84 bracelets; 49 made so far",
              row(st(mt("x + y = 84")) + st(mt("½x + ¾y = 49")) + st("Aaliyah: × 4 (the LCD): " + mt("2x + 3y = 196"))
                  + st("Liam: × (−½) the first equation also works."),
                  st("× (−2) the first: " + mt("−2x − 2y = −168")) + st("Add: " + mt("y = 28") + ", then " + mt("x = 56"))
                  + ans("56 five-inch and 28 seven-inch bracelets", True)),
              "Questions 1–5. Both students are correct: each step makes a pair of opposite coefficients. Check: ½(56) + ¾(28) = 28 + 21 = 49."),
          sec("Talk the Talk · There's a Method in My Madness · SE p. 444 · " + STAR, "Which method when?",
              table(["Method", "How", "Best when"],
                    [["Graphing", "graph both lines, read the intersection", "you want a picture or an estimate; use technology"],
                     ["Substitution", "replace a variable with its equal expression", "a variable is already alone, like " + M("y = 5x")],
                     ["Linear combinations", "add equations so a variable drops out", "both equations are in standard form " + M("Ax + By = C")]], 24, (1, 2)),
              "Students describe each method and the kind of system that suits it."),
          eq_done(eqq, ["Linear combinations: line up the equations, multiply so one variable has opposite coefficients, then add.",
                        "Solve for the remaining variable, substitute back, and check in both equations."]),
          homework(3, "445–447", [("Practice", "1. Field trips: 3 vans and 6 buses, 6 vans and 7 buses. Solve and interpret."),
                                  ("Practice", "2. Solve four systems by linear combinations.")],
                   "Key 1: 3x + 6y = 408, 6x + 7y = 516 → 16 students per van, 60 per bus. 2a: 3x + y = 9, 7x + y = 32 → x = 5.75, y = −8.25.")]
    return [d1, d2, d3]


# ================================================================ Lesson 4 · Graphing Inequalities in Two Variables
def deck4():
    eqq = "What does the graph of a linear inequality in two variables look like?"
    W = ([-8, 8], [-8, 8])
    kai = gshade(380, 300, [0, 12], [0, 10], [1, 2], [1, 2], [L((0, 20 / 3), (10, 0), "2x + 3y = 20", "a")],
                 [[6, 2, ""], [7, 2, "(7, 2)"], [7, 4, "(7, 4)"]], [([(2, 3, -20)], "a")], "Shaded above 2x + 3y = 20")
    g42 = gshade(360, 320, *W, [1, 2], [1, 2], [line(4, -6, (-8, 8), "y = 4x − 6", "a", dash=True)], [[0, 0, "(0, 0)"]],
                 [([above(4, -6)], "a")], "Dashed line y = 4x − 6, shaded on the side with (0, 0)")
    d1 = [title_slide(4, "449–465", "Graphing Inequalities in Two Variables", "boundary line · test point · shade a half-plane",
                      "Two days on the 150-day calendar. Day 1: Getting Started, Activities 4.1 and 4.2. Day 2: Activity 4.3 and Talk the Talk. "
                      "Activities 4.1–4.3 and Talk the Talk are starred; Getting Started is not."),
          D.today(4, 449, ["Write an inequality in two variables.", "Graph an inequality in two variables on a coordinate plane.",
                           "Decide whether the boundary line is solid or dashed.",
                           "Interpret the solutions mathematically and in real-world problems."], "New key terms: half-plane · boundary line"),
          D.eq_slide(4, 449, "You have graphed linear inequalities in one variable.", eqq),
          sec("Getting Started · Making a Statement · SE p. 450", "Five solution statements",
              table(["Statement", "Meaning"], [[M("x = 2"), "exactly 2"], [M("x < 2"), "less than 2"], [M("x ≤ 2"), "at most 2"],
                                               [M("x > 2"), "more than 2"], [M("x ≥ 2"), "at least 2"]], 26, (1,)),
              "Not starred. Have pairs write one scenario, then change a word to get another statement."),
          sec("Activity 4.1 · Linear Inequalities in Two Variables · SE pp. 451–453", "Kai needs at least 20 points",
              row(st("Two-point shots " + mt("x") + ", three-point shots " + mt("y") + ": " + mt("2x + 3y = 20"))
                  + st(mt("(6, 2)") + ": 18, no · " + mt("(7, 2)") + ": 20, yes · " + mt("(7, 4)") + ": 26, yes")
                  + st("At least 20: " + mt("2x + 3y ≥ 20"))
                  + st("Only whole numbers of shots make sense, so " + mt("(6.5, 5.5)") + " is not a real answer."), kai),
              "Questions 1–11. Points on or above the line meet the goal. The equation's solutions are only on the line; the inequality's fill a region."),
          sec("Activity 4.2 · Determining the Graphs · SE pp. 454–455", "Graph " + mt("y > 4x − 6"),
              row(p("A <b>boundary line</b> splits the plane into two <b>half-planes</b>.", "small")
                  + st("<b>Dashed</b> for &gt; or &lt;: points on the line are not solutions. <b>Solid</b> for ≥ or ≤.")
                  + st("Test " + mt("(0, 0)") + ": " + mt("0 > 4(0) − 6") + ", " + mt("0 > −6") + " true")
                  + st("Shade the half-plane that contains " + mt("(0, 0)") + "."), g42),
              "Questions 1–3. If the boundary line goes through (0, 0), test a different point."),
          sec("Activity 4.2 · Practice · SE pp. 455–457", "Graph each inequality",
              row(card("a. " + mt("y > x + 3"), st("dashed · test (0, 0): " + mt("0 > 3") + " false") + ans("shade above", True)),
                  card("b. " + mt("y ≤ −⅓x + 4"), st("solid · test (0, 0): " + mt("0 ≤ 4") + " true") + ans("shade below", True)),
                  card("c. " + mt("2x − y < 4"), st("rewrite: " + mt("y > 2x − 4")) + st("dashed · " + mt("0 < 4") + " true") + ans("shade above", True)), gap=16),
              "Questions 4–6. Worked Example: a solid line y = −(3/2)x − 5 with the half-plane above shaded is y ≥ −(3/2)x − 5."),
          ]
    phone = gshade(380, 300, [0, 260], [0, 110], [20, 40], [10, 20], [L((0, 100), (250, 0), "0.2x + 0.5y = 50", "a")],
                   [[100, 80, "(100, 80)"], [90, 55, "(90, 55)"]], [([(-0.2, -0.5, 50)], "a")], "Shaded below 0.2x + 0.5y = 50")
    d2 = [divider(4, 2, eqq, "solid or dashed boundary, then test a point to decide which half-plane to shade."),
          sec("Activity 4.3 · Interpreting the Graph · SE pp. 459–460", "César's $50 phone card",
              row(st("Table: " + mt("(0, 100)") + ", " + mt("(50, 80)") + ", " + mt("(250, 0)") + " → U.S. calls 20¢ a minute, Mexico 50¢ a minute")
                  + st(mt("0.2x + 0.5y ≤ 50")) + st("70 minutes to Mexico: " + mt("0.2x + 35 ≤ 50") + " → up to 75 U.S. minutes")
                  + st(mt("(100, 80)") + ": $60, no · " + mt("(90, 55)") + ": $45.50, yes"), phone),
              "Questions 1–6. On the line: uses exactly $50. Below: money left over. Above: costs more than the card holds."),
          sec("Talk the Talk · There's a Fine Line · SE pp. 461–462 · " + STAR, "Compare the solution sets",
              table(["Equation or inequality", "Solution set"],
                    [[M("x + y = 0"), "the points on the line"], [M("x + y ≥ 0"), "the line and the half-plane above it"],
                     [M("x + y ≤ 0"), "the line and the half-plane below it"], [M("x + y > 0"), "the half-plane above, line not included"],
                     [M("x + y < 0"), "the half-plane below, line not included"]], 24, (1,)),
              "Questions 1–4 use x + y = 12; test (0, 0) for each."),
          eq_done(eqq, ["Graph the boundary line: solid for ≤ or ≥, dashed for &lt; or &gt;.",
                        "Test a point. If it is a solution, shade its half-plane; if not, shade the other one."]),
          homework(4, "463–465", [("Practice", "1. Elijah's two jobs: write, graph and use the inequality."),
                                  ("Practice", "2. Graph four inequalities.")],
                   "Key 1: (8, 11) earns $174, so yes. Over $160: 8x + 10y > 160, dashed. (0, 0) is not shaded. (5, 10) earns $140, no. "
                   "With 6 hours tutoring he needs 13 hours at the pizzeria: 8(13) + 60 = 164.")]
    return [d1, d2]


# ================================================================ Lesson 5 · Systems of Linear Inequalities
def deck5():
    eqq = "What does the graph of a system of linear inequalities look like, and how can you describe the solution set?"
    raft = gshade(380, 300, [0, 6], [0, 9], [1, 1], [1, 2], [L((0, 8), (4, 0), "weight", "a"), L((0, 3), (2, 0), "money", "b")],
                  [[2, 2, "(2, 2)"], [5, 0, "(5, 0)"]], [([below(-2, 8)], "a"), ([above(-1.5, 3)], "b")], "Overlap of the two raft inequalities")
    W = ([-8, 8], [-8, 8])
    g52 = gshade(360, 320, *W, [1, 2], [1, 2], [line(-1, 1, (-8, 8), "x + y = 1", "a", dash=True), line(1, 3, (-8, 8), "−x + y = 3", "b")],
                 [[-1, 2, "(−1, 2)"]], [([above(-1, 1)], "a"), ([below(1, 3)], "b")], "Overlap of x + y > 1 and −x + y ≤ 3")
    d1 = [title_slide(5, "467–483", "Systems of Linear Inequalities", "the solution set is the overlap",
                      "Three days on the 150-day calendar. Day 1: Getting Started and Activity 5.1. Day 2: Activities 5.2 and 5.3. "
                      "Day 3: Activity 5.4 and Talk the Talk. Getting Started, 5.1, 5.2 and Talk the Talk are starred; 5.3 and 5.4 are not."),
          D.today(5, 467, ["Represent constraints in a problem with a system of inequalities.", "Write and graph systems of linear inequalities.",
                           "Graph the solution set as the intersection of half-planes.", "Verify solutions algebraically."],
                  "New key terms: constraints · solution set of a system of linear inequalities"),
          D.eq_slide(5, 467, "You have graphed a linear inequality in two variables.", eqq),
          sec("Getting Started · A River Runs Through It · SE p. 468", "Noah's raft: 800 pounds, at least $150",
              row(st("Adults " + mt("a") + " (200 lb, $75), children " + mt("c") + " (100 lb, $50)")
                  + st("Weight: " + mt("200a + 100c ≤ 800")) + st("Money: " + mt("75a + 50c ≥ 150")),
                  p("Together they form a <b>system of linear inequalities</b>.", "small") + ans(mt("200a + 100c ≤ 800") + " and " + mt("75a + 50c ≥ 150"), True)),
              "Questions 1–3. Noah's own weight is not counted in the estimate."),
          sec("Activity 5.1 · Determining Solutions · SE pp. 469–470", "Which trips work?",
              row(p("The inequalities are <b>constraints</b>: they limit where solutions can be.", "small")
                  + st("2 adults, 2 children: " + mt("600 ≤ 800") + " ✓, " + mt("250 ≥ 150") + " ✓ → works")
                  + st("5 adults: " + mt("1000 ≤ 800") + " ✗ → too heavy")
                  + st("More solutions: " + mt("(1, 2)") + ", " + mt("(0, 3)") + ", " + mt("(3, 2)") + ". Not one: " + mt("(0, 2)") + ", only $100."), raft),
              "Questions 1–3. The solution set is the overlap of the two shaded half-planes, in the first quadrant (no negative rafters). "
              "The lines meet at (10, −12), which cannot happen here."),
          ]
    d2 = [divider(5, 2, eqq, "the solution set of a system of inequalities is where the shaded regions overlap."),
          sec("Activity 5.2 · Analyzing Graphs · SE pp. 471–473", "Graph " + mt("x + y > 1") + " and " + mt("−x + y ≤ 3"),
              row(st(mt("x + y > 1") + ": dashed, shade above") + st(mt("−x + y ≤ 3") + ": solid, shade below")
                  + st("Test " + mt("(−8, 2)") + ": " + mt("−6 > 1") + " ✗ and " + mt("10 ≤ 3") + " ✗, in neither region")
                  + st("Ava is wrong: " + mt("(−1, 2)") + " is on the dashed line, so it is <b>not</b> a solution."), g52),
              "Questions 1–3. Have students pick a point in each of the four regions and test it in both inequalities."),
          sec("Activity 5.2 · Question 4 · SE p. 473", "Solve each system by graphing",
              row(card("a. " + mt("y > 5x + 3") + " and " + mt("y < 5x − 3"), st("Parallel lines; above the top one and below the bottom one.")
                       + ans("No solution", True)),
                  card("b. " + mt("x ≥ −5") + " and " + mt("x ≥ 1"), st("Two vertical lines; every point right of " + mt("x = 1") + " works.")
                       + ans(mt("x ≥ 1") + ", for example " + mt("(1, 0)") + " and " + mt("(4, −2)"), True)), gap=24),
              "Question 4."),
          sec("Activity 5.3 · Applying Systems · SE pp. 474–475", "Emma's stair stepper workout",
              row(st("Light effort " + mt("x") + " minutes (6.9 cal/min), vigorous " + mt("y") + " minutes (10.4 cal/min)")
                  + st("At most 45 minutes: " + mt("x + y ≤ 45")) + st("At least 400 calories: " + mt("6.9x + 10.4y ≥ 400")),
                  st(mt("(10, 35)") + ": " + mt("45 ≤ 45") + " ✓, " + mt("433 ≥ 400") + " ✓")
                  + st(mt("(0, 40)") + ": " + mt("40 ≤ 45") + " ✓, " + mt("416 ≥ 400") + " ✓")),
              "Not starred. Graph with technology to check."),
          ]
    d3 = [divider(5, 3, eqq, "test a point in both inequalities; it must make every one true."),
          sec("Activity 5.4 · Identifying Systems · SE pp. 476–477", "Same lines, different symbols, different regions",
              row(st("Each system uses " + mt("y = ⅗x + 3") + " and " + mt("y = −⅗x + 3") + ".")
                  + st("Isabella is wrong: changing &lt; and &gt; changes which side is shaded, so the regions differ."),
                  table(["System", "Region"], [["A: " + M("y < ⅗x + 3, y > −⅗x + 3"), "right, between"], ["B: " + M("y > ⅗x + 3, y > −⅗x + 3"), "above both"],
                                               ["C: " + M("y > ⅗x + 3, y < −⅗x + 3"), "left, between"], ["D: " + M("y < ⅗x + 3, y < −⅗x + 3"), "below both"]], 22, (1,))),
              "Not starred. Match each system to a graph and to a pair of possible solutions."),
          sec("Talk the Talk · Get to Know the Region · SE p. 478 · " + STAR, "Which region is the solution set?",
              row(card("a. " + mt("y < 2x + 8") + ", " + mt("y < 2x + 3"), ans("below both lines", True)),
                  card("b. " + mt("y > x + 5") + ", " + mt("y > x + 7"), ans("above both lines", True)),
                  card("c. " + mt("y > −3x + 12") + ", " + mt("y < −3x + 10"), ans("no solution", True)),
                  card("d. " + mt("y > −x + 6") + ", " + mt("y < −x + 9"), ans("between the lines", True)), gap=14),
              "Question 2: a system of equations has at most one point (or a whole line); a system of inequalities usually has a whole region."),
          eq_done(eqq, ["Graph each inequality and shade it. The overlap is the solution set.",
                        "A point is a solution only if it makes every inequality true. Points on a dashed line are not solutions."]),
          homework(5, "479–483", [("Practice", "Samuel's basement flooring and the other Lesson 5 practice problems."),
                                  ("Practice", "Graph each system and name two solutions.")],
                   "Use the Teacher Edition key for the assignment; check each named solution in every inequality.")]
    return [d1, d2, d3]


LESSONS = {
    1: dict(stem="m3t2-lesson1-graphing-systems", name="Using Graphing to Solve Systems of Equations", deck=deck1),
    2: dict(stem="m3t2-lesson2-substitution", name="Using Substitution to Solve Linear Systems", deck=deck2),
    3: dict(stem="m3t2-lesson3-linear-combinations", name="Using Linear Combinations", deck=deck3),
    4: dict(stem="m3t2-lesson4-graphing-inequalities", name="Graphing Inequalities in Two Variables", deck=deck4),
    5: dict(stem="m3t2-lesson5-systems-of-inequalities", name="Systems of Linear Inequalities", deck=deck5),
}

# ================================================================ accommodations
V = A.vocab
ACC = {
 1: dict(vocab=V(("System of linear equations", "Two or more linear equations about the same quantities.", "y = x + 1, y = −2x + 4"),
                 ("Solution of a system", "A point that makes every equation true: where the lines cross.", "(1, 2)"),
                 ("Intercepts", "Where a line crosses the axes. Set the other variable to 0.", "5s + 10a = 3000 → (600, 0), (0, 300)"),
                 ("Consistent", "The system has at least one solution.", "lines cross or are the same"),
                 ("Inconsistent", "The system has no solution.", "parallel lines"),
                 ("Slope", "Rate of change. Same slope means parallel or the same line.", "y = 10x + 25 has slope 10")),
         plans={1: ["Getting Started: ticket combinations", "Activity 1.1: graph using intercepts", "Activity 1.2: two lines, one solution"],
                2: ["Activity 1.3: parallel lines and the same line", "Talk the Talk: one, none or infinite", "Homework"]},
         notes={1: [("Graph with intercepts", "<p class='small'>Set x = 0, solve for y.<br>Set y = 0, solve for x.<br>Plot both points, draw the line.</p>"),
                    ("Solve by graphing", "<p class='small'>Graph both lines.<br>The crossing point is the solution.<br>Check it in both equations.</p>"),
                    ("Read the solution", "<p class='small'>(300, 150) means 300 student and 150 adult tickets.</p>")],
                2: [("One solution", "<p class='small'>Different slopes. Lines cross once.</p>"),
                    ("No solution", "<p class='small'>Same slope, different y-intercepts. Parallel. Inconsistent.</p>"),
                    ("Infinite solutions", "<p class='small'>Same slope, same y-intercept. Same line.</p>")]},
         cans=["graph a line using its intercepts", "find where two lines cross", "tell if a system has one, no or infinite solutions"],
         steps=["Write each equation.", "Graph both lines on the same plane.", "Find the point where they cross.", "Check the point in both equations."],
         skills={1: [("Solve by graphing", ("[[y = x + 1]] and [[y = −2x + 4]]", ["Graph [[y = x + 1]]: start at 1, up 1 right 1.", "Graph [[y = −2x + 4]]: start at 4, down 2 right 1.", "They cross at [[(1, 2)]].", "Check: [[2 = 1 + 1]] ✓ and [[2 = −2 + 4]] ✓"], "[[(1, 2)]]"),
                      ("[[y = x]] and [[y = −x + 2]]", ["Graph [[y = x]]: ______", "Graph [[y = −x + 2]]: ______", "They cross at ______"], "[[(1, 1)]]"),
                      ("[[y = 2x]] and [[y = x + 3]]", "[[(3, 6)]]"))],
                 2: [("How many solutions?", ("[[y = 10x + 25]] and [[y = 10x + 40]]", ["Slopes: 10 and 10, the same.", "y-intercepts: 25 and 40, different.", "Same slope, different start: parallel."], "No solution"),
                      ("[[y = 4x + 40]] and [[y = 10x + 40]]", ["Slopes: ______", "Different slopes: lines ______"], "One solution"),
                      ("[[y = 3x − 1]] and [[y = 3x − 1]]", "Infinite solutions"))]}),
 2: dict(vocab=V(("Substitution method", "Replace a variable with an expression it equals.", "y = 8x → 1.25x + 1.05(8x) = 30"),
                 ("Isolate", "Get a variable alone on one side.", "y = 8x"),
                 ("Standard form", "Ax + By = C", "1.25x + 1.05y = 30"),
                 ("No solution", "The variable drops out and the statement is false.", "0 = −10.5"),
                 ("Infinite solutions", "The variable drops out and the statement is true.", "5 = 5"),
                 ("Interpret", "Say what the answer means in the story.", "3.1 lb of onions")),
         plans={1: ["Getting Started: fair trades", "Activity 2.1: graph, then substitute", "Check in both equations"],
                2: ["Activity 2.2: special systems", "Activity 2.3: write and solve systems", "Talk the Talk", "Homework"]},
         notes={1: [("Substitution", "<p class='small'>1. Get a variable alone.<br>2. Put its expression into the other equation.<br>3. Solve.<br>4. Substitute back.</p>"),
                    ("Check", "<p class='small'>Put both values into both equations.</p>"),
                    ("Why not graph?", "<p class='small'>Graphs give estimates. Substitution gives the exact answer.</p>")],
                2: [("False statement", "<p class='small'>0 = −10.5 → no solution (parallel).</p>"),
                    ("True statement", "<p class='small'>5 = 5 → infinite solutions (same line).</p>"),
                    ("Word problems", "<p class='small'>Define variables, write two equations, solve, answer in words.</p>")]},
         cans=["solve a system by substitution", "tell when a system has no solution or infinite solutions", "write a system for a story"],
         steps=["Get one variable alone.", "Substitute its expression into the other equation.", "Solve for the other variable.", "Substitute back to find the first variable.", "Check in both equations."],
         skills={1: [("Substitution", ("[[y = 2x]] and [[x + y = 9]]", ["Substitute: [[x + 2x = 9]]", "Combine: [[3x = 9]], so [[x = 3]]", "Back: [[y = 2(3) = 6]]", "Check: [[3 + 6 = 9]] ✓"], "[[(3, 6)]]"),
                      ("[[y = 3x]] and [[2x + y = 10]]", ["Substitute: [[2x + ___ = 10]]", "Solve: [[x = ___]]", "Back: [[y = ___]]"], "[[(2, 6)]]"),
                      ("[[y = x + 1]] and [[x + y = 7]]", "[[(3, 4)]]"))],
                 2: [("Special systems", ("[[y = 7x]] and [[y = 7x − 10.5]]", ["Substitute: [[7x = 7x − 10.5]]", "Subtract [[7x]]: [[0 = −10.5]]", "False statement."], "No solution"),
                      ("[[y = −x + 5]] and [[x + y = 5]]", ["Substitute: [[x + (−x + 5) = 5]]", "Simplify: ______", "True or false? ______"], "Infinite solutions"),
                      ("[[y = 2x + 1]] and [[y = 2x + 4]]", "No solution"))]}),
 3: dict(vocab=V(("Linear combinations method", "Add the equations so one variable drops out.", "x + y = 324, x − y = 34"),
                 ("Additive inverses", "Two numbers that add to zero.", "3y and −3y"),
                 ("Coefficient", "The number in front of a variable.", "the 7 in 7x"),
                 ("Eliminate", "Make a variable drop out.", "2y + (−2y) = 0"),
                 ("LCD", "Least common denominator: clears fractions.", "½ and ¾ → multiply by 4"),
                 ("Standard form", "Ax + By = C", "2n + 4m = 270")),
         plans={1: ["Getting Started: coding class", "Activity 3.1: add the equations", "Check in both equations"],
                2: ["Activity 3.2: multiply first", "Activity 3.3: Let It Snow", "Check the answer"],
                3: ["Activity 3.4: fractions", "Talk the Talk: which method?", "Homework"]},
         notes={1: [("Add the equations", "<p class='small'>Line up x, y and the numbers.<br>Opposite coefficients drop out when you add.</p>"),
                    ("Then", "<p class='small'>Solve for the variable left.<br>Substitute back for the other.</p>"),
                    ("Check", "<p class='small'>Put both values into both equations.</p>")],
                2: [("Multiply first", "<p class='small'>Multiply an equation so a variable has opposite coefficients.</p>"),
                    ("Every term", "<p class='small'>Multiply the x-term, the y-term AND the number.</p>"),
                    ("Both equations?", "<p class='small'>If needed, multiply both: × 3 and × (−2).</p>")],
                3: [("Fractions", "<p class='small'>Multiply by the LCD to clear fractions first.</p>"),
                    ("Which method?", "<p class='small'>Variable alone → substitution.<br>Standard form → linear combinations.</p>"),
                    ("Graphing", "<p class='small'>Use for a picture or an estimate.</p>")]},
         cans=["add two equations to eliminate a variable", "multiply an equation to make opposite coefficients", "choose a method for a system"],
         steps=["Write both equations in standard form.", "Multiply if needed so one variable has opposite coefficients.", "Add the equations.", "Solve, then substitute back.", "Check in both equations."],
         skills={1: [("Add the equations", ("[[x + y = 10]] and [[x − y = 4]]", ["Add: [[2x = 14]]", "Solve: [[x = 7]]", "Back: [[7 + y = 10]], [[y = 3]]"], "[[(7, 3)]]"),
                      ("[[x + y = 8]] and [[x − y = 2]]", ["Add: [[___x = ___]]", "Solve: [[x = ___]]", "Back: [[y = ___]]"], "[[(5, 3)]]"),
                      ("[[2x + y = 9]] and [[x − y = 3]]", "[[(4, 1)]]"))],
                 2: [("Multiply first", ("[[x + 2y = 7]] and [[3x − y = 7]]", ["× 2 the second: [[6x − 2y = 14]]", "Add: [[7x = 21]], [[x = 3]]", "Back: [[3 + 2y = 7]], [[y = 2]]"], "[[(3, 2)]]"),
                      ("[[x + y = 5]] and [[2x + 3y = 12]]", ["× (−2) the first: [[−2x − 2y = ___]]", "Add: [[y = ___]]", "Back: [[x = ___]]"], "[[(3, 2)]]"),
                      ("[[2x + y = 7]] and [[x + 3y = 11]]", "[[(2, 3)]]"))],
                 3: [("Choose a method", ("[[y = 4x]] and [[x + y = 10]]", ["y is alone: use substitution.", "[[x + 4x = 10]], [[x = 2]]", "[[y = 8]]"], "[[(2, 8)]]"),
                      ("[[3x + 2y = 12]] and [[x − 2y = 4]]", ["Standard form, −2y and 2y: ______", "Add: ______"], "[[(4, 0)]]"),
                      ("[[y = x − 1]] and [[2x + y = 8]]", "[[(3, 2)]]"))]}),
 4: dict(vocab=V(("Inequality in two variables", "Uses &lt;, &gt;, ≤ or ≥ with x and y.", "2x + 3y ≥ 20"),
                 ("Boundary line", "The line that splits the plane. Graph it like an equation.", "y = 4x − 6"),
                 ("Half-plane", "One side of the boundary line.", "the shaded side"),
                 ("Solid line", "For ≤ or ≥: points on the line are solutions.", "y ≥ x"),
                 ("Dashed line", "For &lt; or &gt;: points on the line are not solutions.", "y > x"),
                 ("Test point", "Plug in a point, often (0, 0), to pick the side.", "0 > −6 true")),
         plans={1: ["Getting Started: x = 2, x < 2 …", "Activity 4.1: Kai's points", "Activity 4.2: solid or dashed, then shade"],
                2: ["Activity 4.3: César's phone card", "Talk the Talk: compare solution sets", "Homework"]},
         notes={1: [("Boundary line", "<p class='small'>Graph it like y = mx + b.<br>≤ ≥ solid. &lt; &gt; dashed.</p>"),
                    ("Test point", "<p class='small'>Try (0, 0). True → shade its side.<br>False → shade the other side.</p>"),
                    ("Solutions", "<p class='small'>Every point in the shaded half-plane works.</p>")],
                2: [("In a story", "<p class='small'>Only points that make sense count, like whole minutes or shots.</p>"),
                    ("On the line", "<p class='small'>Exactly the limit, like exactly $50.</p>"),
                    ("Above or below", "<p class='small'>Over the limit or under it.</p>")]},
         cans=["graph the boundary line, solid or dashed", "use a test point to pick the side to shade", "explain what the shaded points mean"],
         steps=["Graph the boundary line.", "Solid for ≤ or ≥. Dashed for &lt; or &gt;.", "Test (0, 0) in the inequality.", "True: shade the side with (0, 0). False: shade the other side."],
         skills={1: [("Graph an inequality", ("[[y > 4x − 6]]", ["Boundary [[y = 4x − 6]]: start at −6, up 4 right 1.", "Symbol >: dashed line.", "Test [[(0, 0)]]: [[0 > −6]] true.", "Shade the side with [[(0, 0)]]."], "dashed, shade above"),
                      ("[[y ≤ x + 2]]", ["Line: ______", "Symbol ≤: ______ line", "Test (0, 0): [[0 ≤ 2]] ______"], "solid, shade below"),
                      ("[[y > x + 3]]", "dashed, shade above"))],
                 2: [("Use the graph", ("Phone card: [[0.2x + 0.5y ≤ 50]]. Is (100, 80) OK?", ["[[0.2(100) + 0.5(80)]]", "[[20 + 40 = 60]]", "[[60 ≤ 50]] is false."], "No, it costs $60"),
                      ("Is (90, 55) OK?", ["[[0.2(90) + 0.5(55) = ___]]", "Is it ≤ 50? ______"], "Yes, $45.50"),
                      ("Is (50, 80) OK?", "Yes, exactly $50"))]}),
 5: dict(vocab=V(("System of linear inequalities", "Two or more inequalities with the same variables.", "200a + 100c ≤ 800, 75a + 50c ≥ 150"),
                 ("Constraint", "A limit in the problem.", "at most 800 pounds"),
                 ("Solution set", "Every point in the overlap of the shaded regions.", "the double-shaded region"),
                 ("Overlap", "Where both shadings are.", "darkest region"),
                 ("Dashed boundary", "Points on it are not solutions.", "x + y > 1"),
                 ("Verify", "Check a point in every inequality.", "600 ≤ 800 ✓, 250 ≥ 150 ✓")),
         plans={1: ["Getting Started: Noah's raft", "Activity 5.1: test trips, then graph"],
                2: ["Activity 5.2: graph and test regions", "Activity 5.3: Emma's workout"],
                3: ["Activity 5.4: match systems and graphs", "Talk the Talk: name the region", "Homework"]},
         notes={1: [("Graph a system", "<p class='small'>Graph and shade each inequality.<br>The overlap is the solution set.</p>"),
                    ("Check a point", "<p class='small'>It must make EVERY inequality true.</p>"),
                    ("In a story", "<p class='small'>No negative people: stay in the first quadrant.</p>")],
                2: [("Dashed line", "<p class='small'>Points on it are not solutions, even where lines cross.</p>"),
                    ("Test each region", "<p class='small'>Pick a point, test both inequalities.</p>"),
                    ("Two solutions", "<p class='small'>Name two points in the overlap and check them.</p>")],
                3: [("Regions", "<p class='small'>Above both, below both, between, or none.</p>"),
                    ("Parallel lines", "<p class='small'>Above the top and below the bottom → no solution.</p>"),
                    ("Same lines", "<p class='small'>Different symbols → different regions.</p>")]},
         cans=["graph a system of inequalities", "find the overlap (solution set)", "check if a point is a solution"],
         steps=["Graph the first inequality and shade.", "Graph the second inequality and shade.", "The overlap is the solution set.", "Check a point in both inequalities."],
         skills={1: [("Is it a solution?", ("Raft: [[200a + 100c ≤ 800]], [[75a + 50c ≥ 150]]. Try (2, 2).", ["Weight: [[400 + 200 = 600 ≤ 800]] ✓", "Money: [[150 + 100 = 250 ≥ 150]] ✓", "Both true."], "Yes"),
                      ("Try (5, 0).", ["Weight: [[200(5) = ___]]", "Is it ≤ 800? ______"], "No, too heavy"),
                      ("Try (0, 2).", "No, only $100"))],
                 2: [("Graph a system", ("[[y > −x + 1]] and [[y ≤ x + 3]]", ["First: dashed, shade above.", "Second: solid, shade below.", "Overlap: the double-shaded region.", "(−1, 2) is on the dashed line: not a solution."], "the overlap region"),
                      ("Is (0, 3) a solution?", ["[[0 + 3 > 1]]? ______", "[[3 ≤ 0 + 3]]? ______"], "Yes"),
                      ("Is (−8, 2) a solution?", "No"))],
                 3: [("Name the region", ("[[y > x + 5]] and [[y > x + 7]]", ["Both say above.", "Above the higher line: [[y > x + 7]]."], "above both lines"),
                      ("[[y < 2x + 8]] and [[y < 2x + 3]]", ["Both say ______", "Below the ______ line"], "below both lines"),
                      ("[[y > −x + 6]] and [[y < −x + 9]]", "between the lines"))]}),
}


def deck_504(n, days):
    a, out = ACC[n], []
    for d, slides in enumerate(days, 1):
        for k, s in enumerate(slides):
            out.append(s)
            if "Today you will" in s:
                out.append(sec(f"Lesson {n} · Key Vocabulary", "Key vocabulary", a["vocab"],
                               "Section 504 support: preview the key terms before the lesson. Leave this slide up or print it as a reference card."))
            if (d == 1 and "Essential Question · SE" in s) or (d > 1 and k == 0):
                out.append(sec(f"Day {d} · Today's Plan", "Today's plan", A.checklist(*a["plans"][d]),
                               "Section 504 support: chunked directions. Check off each part as the class finishes it."))
        out.append(sec(f"Day {d} · Notes to Keep", f"Notes to keep: Day {d}", A.notes_cards(*a["notes"][d]),
                       "Section 504 support: a copy of the day's notes. Hand out a printed copy if the student's plan lists copies of notes."))
    out[0] = out[0].replace('<p class="muted small">Click', '<p style="font-size:24px;margin-top:6px"><b>Section 504 Version</b></p>\n  <p class="muted small">Click', 1)
    return out


def iep_skill(d, title, ido, wedo, youdo):
    prob, steps, a = ido
    out = [sec(f"Day {d} · I do · {STAR} · {title}", "Watch: " + A.mt(prob), A.steps(*map(A.mt, steps)) + A.ans(A.mt(a), False),
               "I do: model every step aloud. Students copy the steps into their notes.")]
    prob, frames, a = wedo
    out.append(sec(f"Day {d} · We do · {title}", "Together: " + A.mt(prob), "".join(f'<p class="step">{A.mt(f)}</p>' for f in frames) + A.ans(A.mt(a), False),
                   "We do: students fill in each blank on whiteboards before you click. Use the sentence frames."))
    prob, a = youdo
    out.append(sec(f"Day {d} · You do · {title}", "Your turn: " + A.mt(prob), '<p class="muted">Use the steps chart. Then check.</p>' + A.ans(A.mt(a), False),
                   "You do: give 2–3 minutes, then reveal. Students fix mistakes in a different color."))
    return out


def deck_iep(n):
    a, info = ACC[n], LESSONS[n]
    out = [f'<section class="slide">\n  <p class="eyebrow">Bluebonnet Algebra I · Module 3 · Topic 2 · Lesson {n} · IEP Version</p>\n'
           f'  <h1 style="margin-top:10px;font-size:60px">{info["name"]}</h1>\n  <h3 style="margin-top:8px">I can…</h3>'
           + "".join(f"<p>✓ &nbsp;{c}</p>" for c in a["cans"]) + "\n"
           '  <p class="foot">Based on Bluebonnet Learning Secondary Mathematics, Algebra I (©2024–2025 Texas Education Agency, portions ©2021 Carnegie Learning, Inc.), licensed CC BY-NC 4.0. A private site for Algebra I teachers.</p>\n'
           f'  <aside class="notes">IEP version of Lesson {n}: a modified lesson that keeps the core skills (the starred activities) and cuts the number of items. '
           "Each skill follows I do, We do (sentence frames), You do. Apply each student's IEP accommodations too: extended time, read-aloud, breaks, calculator, small group.</aside>\n</section>\n"]
    out.append(sec(f"Lesson {n} · Key Vocabulary", "Key vocabulary", a["vocab"], "Preview the key terms. Leave up or print as a reference card."))
    chart = sec(f"Lesson {n} · Steps Chart", "Steps to follow", A.steps(*a["steps"]), "Anchor chart: students keep this out for every problem.")
    for d in sorted(a["skills"]):
        out.append(chart)
        for skill in a["skills"][d]:
            out += iep_skill(d, *skill)
        out.append(sec(f"Day {d} · Notes to Keep", f"Notes to keep: Day {d}", A.notes_cards(*a["notes"][d]), "Give a printed copy of the notes."))
    return out


# ================================================================ checks
def check():
    """Every system, solution and inequality claim on the slides is right (exact arithmetic)."""
    F = Fr
    sol = lambda eqs, x, y: all(a * x + b * y == c for a, b, c in eqs)
    assert sol([(5, 10, 3000), (1, 1, 450)], 300, 150)
    assert all(5 * s + 10 * a == 3000 for s, a in [(600, 0), (200, 200), (0, 300)])
    assert F(2, 1) * 42 - F(1, 2) * 8 == 80 and 2 * 41 - F(1, 2) * 4 == 80 and 2 * 40 == 80
    assert F(2, 10) * F(2, 3) + F(3, 10) == F(5, 100) * F(2, 3) + F(4, 10)       # Harper: equal at 2/3 cow
    # Lesson 2
    G, C = 5, 4                                          # 4 goats = 5 chickens (goat 5, chicken 4)
    assert 4 * G == 5 * C and 3 * C + (2 * C + G) - 4 * G == G
    assert 1.25 + 1.05 * 8 != 30 and abs(1.25 * 3.1 + 1.05 * 24.8 - 30) < 0.1
    assert 7 * 5 == 35 and 7 * (5 - 1.5) == 24.5
    assert sol([(2800, 1200, 236000), (1, -1, 20)], 65, 45)
    assert sol([(2, 3, 34), (-5, 1, 0)], 2, 10) and sol([(-4, 1, 2), (-3, 1, -2)], -4, -14) and sol([(3, 2, 4), (2, -1, 5)], 2, -1)
    assert all(6 * x + 2 * (8 - 3 * x) == 16 for x in range(-3, 4))
    assert sol([(1, 1, 48), (-2, 1, 0)], 16, 32) and sol([(1, 1, 84), (F(25, 100), F(39, 100), F(2940, 100))], 24, 60)
    assert sol([(10, 8, 192), (20, 1, 99)], 4, 19)
    # Lesson 3
    assert sol([(1, 1, 324), (1, -1, 34)], 179, 145)
    assert sol([(-4, 1, 10), (-2, -1, -1)], F(-3, 2), 4) and sol([(F(-1, 2), 5, -6), (F(1, 2), 1, -6)], -8, -2)
    assert sol([(7, 2, 24), (4, 1, 15)], 6, -9) and sol([(4, 2, 3), (5, 3, 4)], F(1, 2), F(1, 2)) and sol([(4, 3, 12), (3, 2, 4)], -12, 20)
    assert sol([(2, 4, 270), (3, 8, 435)], 105, 15)
    assert sol([(1, 1, 84), (F(1, 2), F(3, 4), 49)], 56, 28)
    assert sol([(3, 6, 408), (6, 7, 516)], 16, 60) and sol([(3, 1, 9), (7, 1, 32)], F(23, 4), F(-33, 4))
    # Lesson 4
    assert [2 * x + 3 * y for x, y in [(6, 2), (7, 2), (7, 4)]] == [18, 20, 26]
    assert 0 > 4 * 0 - 6 and not 0 > 3 and 0 <= 4 and 0 < 4
    for x, y in [(0, 100), (50, 80), (140, 44), (200, 20), (240, 4), (250, 0)]:
        assert F(2, 10) * x + F(5, 10) * y == 50
    assert F(2, 10) * 75 + F(5, 10) * 70 == 50 and F(2, 10) * 100 + F(5, 10) * 80 == 60 and F(2, 10) * 90 + F(5, 10) * 55 == F(91, 2)
    assert 8 * 8 + 10 * 11 == 174 and 8 * 5 + 10 * 10 == 140 and 8 * 13 + 60 == 164 and 8 * 12 + 60 <= 160
    # Lesson 5
    raft = lambda a, c: 200 * a + 100 * c <= 800 and 75 * a + 50 * c >= 150
    assert raft(2, 2) and not raft(5, 0) and raft(1, 2) and raft(0, 3) and raft(3, 2) and not raft(0, 2)
    assert sol([(200, 100, 800), (75, 50, 150)], 10, -12)
    s52 = lambda x, y: x + y > 1 and -x + y <= 3
    assert not s52(-8, 2) and not (-8 + 2 > 1) and not (8 + 2 <= 3) and not s52(-1, 2) and -1 + 2 == 1 and s52(0, 3)
    emma = lambda x, y: x + y <= 45 and F(69, 10) * x + F(104, 10) * y >= 400
    assert emma(10, 35) and emma(0, 40) and F(69, 10) * 10 + F(104, 10) * 35 == 433 and F(104, 10) * 40 == 416
    # IEP skill answers
    assert sol([(-1, 1, 1), (2, 1, 4)], 1, 2) and sol([(-1, 1, 0), (1, 1, 2)], 1, 1) and sol([(-2, 1, 0), (-1, 1, 3)], 3, 6)
    assert sol([(-2, 1, 0), (1, 1, 9)], 3, 6) and sol([(-3, 1, 0), (2, 1, 10)], 2, 6) and sol([(-1, 1, 1), (1, 1, 7)], 3, 4)
    assert sol([(1, 1, 10), (1, -1, 4)], 7, 3) and sol([(1, 1, 8), (1, -1, 2)], 5, 3) and sol([(2, 1, 9), (1, -1, 3)], 4, 1)
    assert sol([(1, 2, 7), (3, -1, 7)], 3, 2) and sol([(1, 1, 5), (2, 3, 12)], 3, 2) and sol([(2, 1, 7), (1, 3, 11)], 2, 3)
    assert sol([(-4, 1, 0), (1, 1, 10)], 2, 8) and sol([(3, 2, 12), (1, -2, 4)], 4, 0) and sol([(-1, 1, -1), (2, 1, 8)], 3, 2)
    assert F(2, 10) * 50 + F(5, 10) * 80 == 50 and raft(1, 2)


# ================================================================ main
def build(n):
    info = LESSONS[n]
    days = info["deck"]()
    key = f"m3t2l{n}"
    starred = [[D.star_eyebrows(key, s) for s in day] for day in days]
    general = [s for day in starred for s in day]
    OUT.mkdir(exist_ok=True)
    path = OUT / f"{info['stem']}.html"
    path.write_text(deck_doc(f"{info['name']} · Bluebonnet Algebra I", general), encoding="utf-8")
    print(path.name, len(general), "slides"); pptx(path)
    for kind, slides in (("504", deck_504(n, starred)), ("IEP", deck_iep(n))):
        p_ = FOLDER[kind] / f"{info['stem']}-{kind}.html"
        p_.write_text(deck_doc(f"{info['name']} · Bluebonnet Algebra I · {LABEL[kind]}", slides), encoding="utf-8")
        print(p_.name, len(slides), "slides"); pptx(p_)


if __name__ == "__main__":
    import sys
    check()
    assert all(set(ACC[n]["plans"]) == set(range(1, len(LESSONS[n]["deck"]()) + 1)) == set(ACC[n]["notes"]) == set(ACC[n]["skills"]) for n in LESSONS)
    for n in [int(a) for a in sys.argv[1:] if a.isdigit()] or LESSONS:
        build(n)

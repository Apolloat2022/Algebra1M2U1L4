"""Teacher script for M3T1 Lesson 3 (Modeling Linear Inequalities): Day 1 (Wed Nov 11), Day 2 (Thu Nov 12), Day 3 (Mon Nov 16).
What to say, what to ask, and every essential (✪) problem worked step by step. SE pp. 371-386. Same layout as make_m3t1_l2_script.py.
Run:  python make_m3t1_l3_script.py <password>   ->  Module 3 topic 1/LESSON PLANS/M3T1-Lesson3-Teaching-Script.pdf (password-protected)"""
import sys
from pathlib import Path

from make_m3t1_l2_script import say, ask, board, prob, part, tip, CSS
import make_m3t1_walkthroughs as W   # pdf(): print + encrypt
import make_m3t1_review as RV

RV.KEY = True
OUT = Path(__file__).parent / "Module 3 topic 1" / "LESSON PLANS" / "M3T1-Lesson3-Teaching-Script.pdf"
nl = RV.numline  # (lo, hi, mark, shade left?, open circle?)

DAY1 = [
    part("0–5", "Bell work · build the words chart",
         board("1. $25 credit + $3.75 per box → <b>y = 3.75x + 25</b>", "2. “at least” → <b>≥</b>", "3. “no more than” → <b>≤</b>",
               "4. 3.75b + 25 = 400 → 3.75b = 375 → <b>b = 100</b>"),
         say("Copy this chart into your notes. It stays on the board all lesson."),
         board("at least, no less than, minimum → <b>≥</b> &nbsp;·&nbsp; at most, no more than, maximum → <b>≤</b>",
               "more than, over → <b>&gt;</b> &nbsp;·&nbsp; less than, under, below → <b>&lt;</b>")),
    part("5–7", "Launch the lesson (SE p. 371)",
         say("You know how to read a graph with a horizontal line and how to solve equations. Today the question is: "
             "do those same tools work when the answer is <i>a whole range of numbers</i> instead of one number? Spoiler: yes, with one twist we will find tomorrow.")),
    part("7–20", "✪ Getting Started: Fundraising Function (SE p. 372)",
         say("Elijah sells popcorn. He starts with a $25 credit, and each box sells for $3.75."),
         ask("Which number gets multiplied by the boxes, and which number is just added once?", "3.75 per box is the rate; 25 is added once."),
         prob("Q1 · Write the function", board("<b>f(b) = 3.75b + 25</b>")),
         prob("Q2 · Analyze it",
              board("a. Independent: number of boxes sold (boxes). Dependent: total sales (dollars).",
                    "b. Slope <b>3.75</b>: he earns $3.75 more for each box.", "c. y-intercept <b>(0, 25)</b>: the $25 credit he has before selling anything."))),
    part("20–35", "✪ Activity 3.1: Modeling Linear Inequalities (SE pp. 373–374)",
         say("Goal: $1600. Put your finger at 1600 on the y-axis, slide right to the line, then straight down."),
         prob("Q1 · Exactly $1600",
              board("3.75b + 25 = 1600 → 3.75b = 1575 → <b>b = 420 boxes</b>", "Number line: one closed dot at 420")),
         say("A <b>linear inequality</b> is a comparison of two linear expressions that is not an equals: &lt;, &gt;, ≤, ≥ or ≠."),
         prob("Q2 · Below the line, including the point",
              board("a. Total sales of $1600 or less", "b. f(b) ≤ 1600, so <b>b ≤ 420</b>", "c. Closed circle at 420, shade left (to 0)",
                    "d. Only whole numbers 0, 1, 2, … 420 make sense. He can't sell half a box or −3 boxes.")),
         prob("Q3 · Above the line, not including the point",
              board("a. Total sales of more than $1600", "b. f(b) &gt; 1600, so <b>b &gt; 420</b>", "c. Open circle at 420, shade right",
                    "d. Only whole numbers 421, 422, … make sense.")),
         ask("Thumbs: open or closed circle for x &lt; 3?", "Open. 3 itself is not included.")),
    part("35–45", "✪ Activity 3.1: Questions 4–5 (SE p. 375)",
         prob("Q4 · Open vs closed", board("○ Open: the endpoint is <b>not</b> a solution (&lt;, &gt;).", "● Closed: the endpoint <b>is</b> a solution (≤, ≥).")),
         prob("Q5 · Use the graph, then check with the equation",
              board("a. At least $925: 3.75b + 25 ≥ 925 → 3.75b ≥ 900 → <b>b ≥ 240</b>",
                    "b. Less than $2050: 3.75b + 25 &lt; 2050 → 3.75b &lt; 2025 → <b>b &lt; 540</b>",
                    "c. Exactly $700: 3.75b + 25 = 700 → 3.75b = 675 → <b>b = 180</b>")),
         prob("Test move (like End of Topic Q1 and Q6)",
              board("$40 to start + $15 per week → <b>y = 15x + 40</b>", "4 notebooks at $1.75 + x pens at $0.90 → 4(1.75) = 7 → <b>y = 0.90x + 7</b>"),
              say("The thing that changes gets the x. The start, or anything you buy a fixed number of, is the plain number."))),
    part("45–55", "Exit ticket",
         board("1. $40 + $12 per hour → <b>y = 12x + 40</b>", "2. 4 notebooks at $1.75 + pens at $0.90 → <b>y = 0.90x + 7</b>",
               "3. At most $1150: 3.75b + 25 ≤ 1150 → 3.75b ≤ 1125 → <b>b ≤ 300</b>, closed circle at 300, shade left")),
    part("55–60", "Wrap up",
         say("Tonight: Lesson 3 Assignment, Practice 1a–d, SE p. 383. Tomorrow we solve inequalities with algebra, and you'll see when the sign flips."),
         board("Key: a f(g) = 3.25g + 40 · b rate $3.25 per gallon, y-intercept $40 for food and fun",
               "d $170: 3.25g + 40 ≤ 170 → 3.25g ≤ 130 → g ≤ 40 gallons")),
]

DAY2 = [
    part("0–5", "Bell work",
         board("1. 2x + 5 = 17 → 2x = 12 → <b>x = 6</b>", "2. x ≥ 2 → <b>closed circle at 2, shade right</b>",
               "3. Is −5 a solution of −x &gt; 4? −(−5) = 5, and 5 &gt; 4 → <b>Yes</b>", "4. 2 muffins at $1.50 = $3 → <b>y = 2.25x + 3</b>"),
         say("Look at number 3. x = −5 works, but if you “solved” −x &gt; 4 by just dropping the negative you'd get x &gt; 4, and −5 is not more than 4. Something has to flip. That's today.")),
    part("5–8", "Homework check (Practice 1a–d)", board("f(g) = 3.25g + 40 · g ≤ 40 gallons for $170")),
    part("8–25", "✪ Activity 3.2: Solving Two-Step Linear Inequalities (SE pp. 376–377)",
         say("To <b>solve an inequality</b> means to find all the values that make it true. You solve it exactly like an equation, using inverse operations."),
         prob("Worked Example and Q1 · First deposit: at least $1100",
              board("3.75b + 25 ≥ 1100", "3.75b ≥ 1075 &nbsp;(subtract 25)", "b ≥ 286.66… &nbsp;(divide by 3.75)",
                    "<b>At least 287 boxes</b>: 286 boxes only make $1097.50, so round <b>up</b>.")),
         prob("Q2a · Most boxes and still not $600",
              board("3.75b + 25 &lt; 600 → 3.75b &lt; 575 → b &lt; 153.33…", "<b>At most 153 boxes</b>: round <b>down</b>, because 154 boxes make $602.50.")),
         prob("Q2b · At least how many boxes for $1500",
              board("3.75b + 25 ≥ 1500 → 3.75b ≥ 1475 → b ≥ 393.33…", "<b>At least 394 boxes</b>: round <b>up</b>.")),
         prob("Q3 · Other forms", board("Nothing changes: undo the operations in reverse order, the same as an equation.")),
         tip("rounding the wrong way. “At least” rounds up; “at most” rounds down. Plug the rounded number back in to be sure.")),
    part("25–40", "✪ Activity 3.3: Reversing Inequality Signs (SE p. 378)",
         say("Elijah's troop hikes down from a campsite at 4800 feet, losing 20 feet every minute, until they reach sea level, 0 feet."),
         ask("Is the elevation going up or down? So is the slope positive or negative?", "Down, so the slope is negative: −20."),
         prob("Q1 · Write the function", board("<b>h(m) = −20m + 4800</b>")),
         prob("Q2 · Analyze it",
              board("a. Slope <b>−20</b>: they drop 20 feet each minute.", "b. y-intercept <b>(0, 4800)</b>: they start at the campsite, 4800 ft.",
                    "c. x-intercept: 0 = −20m + 4800 → 20m = 4800 → m = 240 → <b>(240, 0)</b>: sea level after 240 minutes.",
                    "d. Domain <b>0 ≤ m ≤ 240</b>: from the start of the hike to sea level."))),
    part("40–50", "✪ Activity 3.3: Why the sign flips (SE p. 379)",
         prob("Q3 · From the graph: below 3200 feet",
              board("The line is under 3200 ft to the <b>right</b> of m = 80", "h(m) &lt; 3200 when <b>m &gt; 80</b>")),
         prob("Q4 · Verify with algebra",
              board("−20m + 4800 &lt; 3200", "−20m &lt; −1600 &nbsp;(subtract 4800)", "m <b>&gt;</b> 80 &nbsp;(divide by −20, and <b>flip</b> the sign)")),
         prob("Q5 · Compare", board("The graph and the algebra both give m &gt; 80. The algebra only matches because we flipped the sign.")),
         prob("Q6 · The table",
              board("h(m) &gt; 3200 ↔ m &lt; 80 · h(m) ≥ 3200 ↔ m ≤ 80 · h(m) = 3200 ↔ m = 80",
                    "h(m) &lt; 3200 ↔ m &gt; 80 · h(m) ≤ 3200 ↔ m ≥ 80",
                    "b. Every sign is reversed (except =). c. To get m alone you divide by −20, a negative."),
              say("Write this rule in a box: <b>when you multiply or divide both sides by a negative number, flip the inequality sign.</b> "
                  "Example: 2 &lt; 3, but multiply both by −1 and −2 &gt; −3.")),
         prob("Test move (like End of Topic Q3)",
              board("3(4 − k) &gt; −k + 16", "12 − 3k &gt; −k + 16 &nbsp;(distribute)", "−2k &gt; 4 &nbsp;(add k, subtract 12)",
                    "<b>k &lt; −2</b> &nbsp;(divide by −2, flip)")),
         ask("Thumbs: subtracting a negative number flips the sign.", "Down. Only multiplying or dividing by a negative flips it.")),
    part("50–58", "Exit ticket",
         board("1. −3x + 4 ≥ 19 → −3x ≥ 15 → <b>x ≤ −5</b> (flip)", "2. 5 − 2x &lt; 11 → −2x &lt; 6 → <b>x &gt; −3</b>: open circle at −3, shade right",
               "3. Tire: 26 − 0.1t ≥ 22 → −0.1t ≥ −4 → <b>t ≤ 40 minutes</b> (flip)"),
         nl(-6, 4, -3, False, True)),
    part("58–60", "Wrap up",
         say("Tonight: Practice 1e–g and 2a–b, SE pp. 384–385."),
         board("e. Check: 3.25(40) + 40 = 170 ✓ · f. 3.25g + 40 ≤ 220 → g ≤ 55.38… → <b>55 gallons</b>",
               "g. 3.25g + 40 &gt; 92 → 3.25g &gt; 52 → <b>g &gt; 16 gallons</b>",
               "2a. p(t) = −0.1t + 26 · 2b. −0.1t + 26 ≥ 22 → t ≤ 40 → <b>40 minutes</b>")),
]

DAY3 = [
    part("0–5", "Bell work",
         board("1. −4x &gt; 12 → <b>x &lt; −3</b> (flip)", "2. 2x + 3 ≤ x − 1 → <b>x ≤ −4</b>", "3. −6 ≤ x is the same as <b>x ≥ −6</b>",
               "4. 3(x − 2) = 9 → x − 2 = 3 → <b>x = 5</b>"),
         say("Number 3 matters today: −6 ≤ x and x ≥ −6 say the same thing. Read it from the x: “x is at least −6.”")),
    part("5–8", "Homework check (Practice 1e–g, 2)", board("f 55 gallons · g more than 16 gallons · 2b 40 minutes")),
    part("8–20", "✪ Activity 3.4: Variables on both sides (SE p. 380)",
         say("Victoria and Kai both solved 5x + 2 ≥ 3x − 10. They did it differently. Who is right?"),
         prob("Q1a · Victoria: x-terms on the left",
              board("5x − 3x + 2 ≥ −10 → 2x + 2 ≥ −10", "2x ≥ −12", "<b>x ≥ −6</b> &nbsp;(divided by +2, no flip)")),
         prob("Q1b · Kai: x-terms on the right",
              board("2 ≥ 3x − 5x − 10 → 2 ≥ −2x − 10", "12 ≥ −2x", "<b>−6 ≤ x</b> &nbsp;(divided by −2, flipped)", "−6 ≤ x is the same as x ≥ −6")),
         prob("Q2 · Compare with equations", board("Same steps as an equation with variables on both sides, but if you divide by a negative, flip.")),
         say("Both are right. Victoria's way is faster: <b>move the smaller x-term</b>, so the x stays positive and you never have to flip."),
         ask("5x vs 3x: which one do you move?", "The 3x, the smaller one. Then the x-term is +2x.")),
    part("20–30", "✪ Activity 3.4: The distributive property (SE p. 381)",
         prob("Q3a · Aaliyah: distribute first",
              board("−4(x − 6) &lt; 22", "−4x + 24 &lt; 22", "−4x &lt; −2", "<b>x &gt; ½</b> &nbsp;(divided by −4, flipped)")),
         prob("Q3b · Ava: divide first",
              board("−4(x − 6) &lt; 22", "x − 6 &gt; −5½ &nbsp;(divided both sides by −4, flipped)", "<b>x &gt; ½</b> &nbsp;(added 6)")),
         prob("Q4 · Compare with equations", board("Distributing works the same way. The only new thing is the flip when you divide by −4.")),
         prob("Test move (like End of Topic Q9)",
              board("2.5p − 4 &gt; −1.5(p + 8)", "2.5p − 4 &gt; −1.5p − 12 &nbsp;(distribute)", "4p − 4 &gt; −12 &nbsp;(add 1.5p, the smaller x-term)",
                    "4p &gt; −8 → <b>p &gt; −2</b>: open circle at −2, shade right"),
              nl(-6, 4, -2, False, True))),
    part("30–50", "✪ Talk the Talk: It's About Solutions, More or Less (SE p. 382)",
         prob("Q1a · −⅔x ≥ 7",
              board("Multiply by −3/2 and flip: x ≤ 7 · (−3/2)", "<b>x ≤ −10½</b>: closed circle at −10½, shade left"), nl(-14, 0, -10.5, True, False)),
         prob("Q1b · 32 &gt; 23 − x",
              board("Add x (keeps x positive): 32 + x &gt; 23", "Subtract 23: <b>x &gt; −9</b>: open circle at −9, shade right"), nl(-12, 0, -9, False, True)),
         prob("Q1c · 15 − 4x ≤ 3x − 6",
              board("Add 4x (the smaller x-term): 15 ≤ 7x − 6", "21 ≤ 7x → 3 ≤ x → <b>x ≥ 3</b>: closed circle at 3, shade right"), nl(-2, 8, 3, False, False)),
         prob("Q1d · 2(x + 6) &lt; 14 + 4x",
              board("2x + 12 &lt; 14 + 4x", "Subtract 2x (the smaller x-term): 12 &lt; 14 + 2x", "−2 &lt; 2x → <b>x &gt; −1</b>: open circle at −1, shade right"),
              nl(-6, 4, -1, False, True)),
         prob("Q2 · If A &lt; B, when is each true?",
              board("a. A + C &lt; B + C → <b>always</b> (adding never flips)", "b. AC &gt; BC → <b>only when C &lt; 0</b> (multiplying by a negative flips)",
                    "c. −A &lt; −B → <b>never</b> (multiplying by −1 always flips, so −A &gt; −B)"),
              say("Try numbers: A = 2, B = 5, C = −1. Then AC = −2 and BC = −5, and −2 &gt; −5 ✓."))),
    part("50–58", "Exit ticket",
         board("1. 3(4 − x) &gt; −2x + 10 → 12 − 3x &gt; −2x + 10 → add 3x: 12 &gt; x + 10 → <b>x &lt; 2</b>",
               "2. 1.5m + 4 ≥ −2(m − 9) → 1.5m + 4 ≥ −2m + 18 → 3.5m ≥ 14 → <b>m ≥ 4</b>: closed circle at 4, shade right",
               "3. −2(x + 1) ≥ 8 → −2x − 2 ≥ 8 → −2x ≥ 10 → <b>x ≤ −5</b> (flip)")),
    part("58–60", "Essential Question and homework",
         ask("Can you use the same methods to solve inequalities?",
             "Yes: graphs with a horizontal line and inverse operations both work. The one change: multiply or divide by a negative → flip the sign."),
         say("Tonight: Practice 3a–d, SE p. 385, and the Topic 1 Self-Reflection. Review tomorrow, test Wednesday."),
         board("3a. 13 + 4x &gt; 9 → <b>x &gt; −1</b> · 3b. 12 − 15x &gt; 8x − 149 → 161 &gt; 23x → <b>x &lt; 7</b>",
               "3c. 99 − 5d ≥ 4d → 99 ≥ 9d → <b>d ≤ 11</b> · 3d. 3k − 9 ≤ −6k − 225 → 9k ≤ −216 → <b>k ≤ −24</b>")),
]


def html():
    head = ('<h1>Module 3 Topic 1 · Lesson 3: Modeling Linear Inequalities · Teaching Script</h1>'
            '<p class="sub">Algebra I · Mr. Pandey · SE pp. 371–386 · Every activity is essential (✪) on the 150-day pacing guide. '
            '<b>SAY</b> = read to class · <b>ASK</b> = question with the answer to listen for · blue boxes = what to write on the board, fully solved.</p>')
    days = [("Day 1 · Wednesday, Nov 11 · Reading inequalities from a graph", DAY1),
            ("Day 2 · Thursday, Nov 12 · Solving inequalities and the flip", DAY2),
            ("Day 3 · Monday, Nov 16 · Variables on both sides and distributing", DAY3)]
    body = "".join(f'<h2{" class=first" if i == 0 else ""}>{t}</h2>{"".join(d)}' for i, (t, d) in enumerate(days))
    return f'<!doctype html><html><head><meta charset="utf-8"><title>M3T1 Lesson 3 Script</title><style>{CSS}</style></head><body>{head}{body}</body></html>'


if __name__ == "__main__":
    # the math behind the worked answers
    assert 3.75 * 420 + 25 == 1600 and 3.75 * 240 + 25 == 925 and 3.75 * 540 + 25 == 2050 and 3.75 * 180 + 25 == 700
    assert 3.75 * 286 + 25 < 1100 <= 3.75 * 287 + 25 and 3.75 * 153 + 25 < 600 <= 3.75 * 154 + 25 and 3.75 * 393 + 25 < 1500 <= 3.75 * 394 + 25
    assert -20 * 80 + 4800 == 3200 and -20 * 81 + 4800 < 3200
    assert 5 * -6 + 2 == 3 * -6 - 10 and -4 * (0.5 - 6) == 22 and 2.5 * -2 - 4 == -1.5 * (-2 + 8)
    assert -2 / 3 * -10.5 == 7 and 32 == 23 + 9 and 15 - 12 == 9 - 6 and 2 * (-1 + 6) == 14 - 4
    assert 13 + 4 * -1 == 9 and 3 * (4 - 35) == 8 * 7 - 149 and 99 - 55 == 44 and 3 * -24 - 9 == -6 * -24 - 225
    assert 3.25 * 55 + 40 <= 220 < 3.25 * 56 + 40 and 3.25 * 16 + 40 == 92
    W.pdf(html(), OUT, sys.argv[1])

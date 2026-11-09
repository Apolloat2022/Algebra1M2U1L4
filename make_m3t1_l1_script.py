"""Teacher script for M3T1 Lesson 1 (Solving Linear Equations), one day (Thu Nov 5): what to say, what to ask, and every
essential (✪) problem worked step by step. SE pp. 345-356. Same layout as make_m3t1_l2_script.py.
Run:  python make_m3t1_l1_script.py <password>   ->  Module 3 topic 1/LESSON PLANS/M3T1-Lesson1-Teaching-Script.pdf (password-protected)"""
import sys
from fractions import Fraction as F
from pathlib import Path

from make_m3t1_l2_script import say, ask, board, prob, part, tip, CSS
import make_m3t1_walkthroughs as W   # pdf(): print + encrypt

OUT = Path(__file__).parent / "Module 3 topic 1" / "LESSON PLANS" / "M3T1-Lesson1-Teaching-Script.pdf"

DAY = [
    part("0–5", "Bell work",
         board("1. $35 to start + $15 per week → <b>y = 15x + 35</b>", "2. 3(x − 2) = 12 → 3x − 6 = 12 → 3x = 18 → <b>x = 6</b>",
               "3. 5(2) − 1 = 9 → 9 = 9 → <b>Yes</b>", "4. 4(x + 2) − x = 4x + 8 − x = <b>3x + 8</b>"),
         say("Four of the eleven questions on the test on November 18 come from today's lesson. Pay attention to number 2: distribute first.")),
    part("5–7", "Launch the lesson (SE p. 345)",
         say("You already solve equations. Today you will <i>prove</i> each step with a property, and find out that some equations have "
             "no answer at all, and some have every number as an answer.")),
    part("7–15", "✪ Getting Started: Equation Creation (SE p. 346)",
         say("A <b>solution</b> is a value of the variable that makes the equation true. Start from x = 2 and build a harder equation, "
             "doing the same thing to both sides each time."),
         prob("Build it from x = 2",
              board("x + 3 = 5 &nbsp;(add 3 to both sides)", "4x + 12 = 20 &nbsp;(multiply both sides by 4, <b>every</b> term)",
                    "2x + 12 = −2x + 20 &nbsp;(subtract 2x from both sides)", "x + 6 = 10 − x &nbsp;(divide both sides by 2, every term)")),
         prob("Swap with a partner and check", board("Put x = 2 into x + 6 = 10 − x: 2 + 6 = 10 − 2 → <b>8 = 8 ✓</b>")),
         tip("multiplying only the x-term: 4(x + 3) is 4x + <b>12</b>, not 4x + 3. That same mistake costs points on test Q2 and Q5.")),
    part("15–20", "✪ Activity 1.1: The properties (SE pp. 347–348)",
         say("These rules keep the equation balanced. Whatever you do to one side, you do to the other."),
         board("<b>Addition</b>: if a = b, then a + c = b + c · <b>Subtraction</b>: a − c = b − c",
               "<b>Multiplication</b>: ac = bc · <b>Division</b>: a/c = b/c (c ≠ 0)",
               "<b>Distributive</b>: a(b + c) = ab + ac · <b>Commutative</b>: a + b = b + a · <b>Associative</b>: (a + b) + c = a + (b + c)")),
    part("20–32", "✪ Activity 1.1: Questions 1–3",
         prob("Q1 · Harper: −3x + 14 = 18 − 5x",
              board("a. Substitution: −3(2) + 14 = 8 and 18 − 5(2) = 8 → <b>8 = 8 ✓</b>",
                    "b. Properties: add 5x → 2x + 14 = 18 · subtract 14 → 2x = 4 · divide by 2 → <b>x = 2</b>")),
         prob("Q1 · Sofia: 2x = 5 − ½x",
              board("a. Substitution: 2(2) = 4 and 5 − ½(2) = 4 → <b>4 = 4 ✓</b>",
                    "b. Multiply by 2 to clear the fraction: 4x = 10 − x · add x → 5x = 10 · divide by 5 → <b>x = 2</b>")),
         prob("Q2a · −4x + 7 = −4x",
              board("Add 4x: 7 = 0 &nbsp;(addition property)", "7 = 0 is false → <b>no solution</b>")),
         prob("Q2b · 0.6(2x + 1) = 4x + 6.2 (decimals, like test Q4)",
              board("1.2x + 0.6 = 4x + 6.2 &nbsp;(distributive)", "0.6 = 2.8x + 6.2 &nbsp;(subtract 1.2x, the smaller x-term)",
                    "−5.6 = 2.8x &nbsp;(subtract 6.2)", "<b>x = −2</b> &nbsp;(divide by 2.8)",
                    "Check: 0.6(−4 + 1) = −1.8 and 4(−2) + 6.2 = −1.8 ✓")),
         prob("Q2c · ½x − 6 = 2 + (2x + 1)",
              board("½x − 6 = 2x + 3 &nbsp;(commutative and associative: 2 + 1 = 3)", "−6 = 1½x + 3 &nbsp;(subtract ½x)",
                    "−9 = 1½x &nbsp;(subtract 3)", "<b>x = −6</b> &nbsp;(multiply by ⅔)", "Check: −3 − 6 = −9 and 2 + (−12 + 1) = −9 ✓")),
         prob("Q3 · Daniel vs. Chloe: 4(3x + 2) = 8x + 4",
              board("Daniel distributes first: 12x + 8 = 8x + 4 → 4x = −4 → <b>x = −1</b>",
                    "Chloe divides both sides by 4 first: 3x + 2 = 2x + 1 → <b>x = −1</b>"),
              say("Both are correct. Chloe saw that every term was a multiple of 4, so dividing first made the numbers smaller.")),
         ask("Whiteboards: what is −4(m + 2)?", "−4m − 8. The negative goes to both terms.")),
    part("32–42", "✪ Activity 1.2: Solutions to Linear Equations (SE pp. 349–350)",
         prob("Q1 · Start from 2 = 2 (true)",
              board("Add x: 2 + x = 2 + x · multiply by 5: 10 + 5x = 10 + 5x", "Nothing you do to both sides makes it false → <b>infinite solutions</b>")),
         prob("Q2 · Start from 2 = 3 (false)",
              board("Add x: 2 + x = 3 + x · multiply by 5: 10 + 5x = 15 + 5x", "Nothing you do to both sides makes it true → <b>no solution</b>")),
         prob("Q3 · Classify", board("a. Equations built from 2 = 2: infinite solutions. b. Equations built from 2 = 3: no solution.")),
         prob("Q4 · 2x = 3x", board("Subtract 2x: 0 = x → <b>one solution, x = 0</b>", "0 is a real answer, not “no solution.”")),
         say("The rule. Simplify each side first, then look at it."),
         board("<b>Different</b> x-terms → <b>one</b> solution", "<b>Same</b> x-term, <b>different</b> numbers → <b>no</b> solution (you get something false like 7 = 0)",
               "<b>Same</b> x-term, <b>same</b> number → <b>infinite</b> solutions (you get something true like 3 = 3)"),
         ask("Thumbs: x + 5 = x + 5 has no solution.", "Down. Both sides are identical, so it has infinite solutions.")),
    part("42–50", "Test moves (like End of Topic Q2, Q5, Q11)",
         prob("Negative outside the parentheses (like Q2) · 6 − 4(m + 2) = 3 − 2(2m + 1)",
              board("Left: 6 − 4m − 8 = −4m − 2", "Right: 3 − 4m − 2 = −4m + 1", "Same −4m, −2 ≠ 1 → <b>no solution</b>"),
              say("As soon as both sides have the same x-term, stop and compare the numbers. No more steps needed.")),
         prob("Explain your reasoning (like Q5) · ¼(8x + 12) = 2(x + 2) − 1",
              board("Left: 2x + 3 · Right: 2x + 4 − 1 = 2x + 3", "<b>Infinite solutions</b>"),
              say("Write it as a sentence: “The equation has <b>infinite</b> solutions because both sides simplify to <b>2x + 3</b>.”")),
         prob("✪ Talk the Talk: equal areas (like Q11, SE p. 352)",
              board("Rectangle A: 6(5 + 2x) · Rectangle B: 8(x + 5)", "30 + 12x = 8x + 40 &nbsp;(distributive)",
                    "4x + 30 = 40 &nbsp;(subtract 8x)", "4x = 10 &nbsp;(subtract 30)", "<b>x = 2.5</b> &nbsp;(divide by 4)",
                    "Check: 6(5 + 5) = 60 and 8(2.5 + 5) = 60 ✓"),
              say("Write the area formula first. Rectangle: length × width. Triangle: ½ × base × height."))),
    part("50–58", "Exit ticket",
         board("1. 7 − 3(p + 2) = 10 − (2p + 5) → 1 − 3p = 5 − 2p → add 3p: 1 = 5 + p → <b>p = −4</b>",
               "2. 0.5(4x − 6) = −1.5x + 4 → 2x − 3 = −1.5x + 4 → 3.5x = 7 → <b>x = 2</b>",
               "3. ½(8x + 6) = 2(2x + 1) + 2 → 4x + 3 = 4x + 4 → <b>no solution</b>",
               "4. Triangle ½ · 6 · (x + 5) = 3x + 15. Rectangle 4(x − 1) = 4x − 4. 3x + 15 = 4x − 4 → <b>x = 19</b>")),
    part("58–60", "Essential Question and homework",
         ask("How can you use equations to solve for unknown input values?",
             "Use the properties of equality to get the variable alone, naming the property for each step. Simplify both sides first to see one, none, or infinite."),
         say("Tonight: SE pp. 355–356, Practice 1a–e and 2a–f. If you are stuck, watch the Lesson 1 video."),
         board("1a. 3x − 8 = −7x + 18 → 10x = 26 → <b>x = 2.6</b> · 1b. −8 + 2x = 12x − 3 → −5 = 10x → <b>x = −½</b>",
               "1c. −5x + 2 = 12 − 8x + 8 → 3x = 18 → <b>x = 6</b> · 1d. ×5: −2x − 4 + 8 = 15x − 15 → 19 = 17x → <b>x = 19/17</b>",
               "1e. (4/3)x + 18 − (2/3)x = −(7/3)x + 9 → 3x = −9 → <b>x = −3</b>",
               "2. a none · b x = 7 · c x = 2 · d infinite · e none · f infinite",
               "Prepare (r = C ÷ 6.28): 1. 10 in · 2. 1.6 cm · 3. 2.5 ft · 4. 7.6 mm")),
]


def html():
    head = ('<h1>Module 3 Topic 1 · Lesson 1: Solving Linear Equations · Teaching Script</h1>'
            '<p class="sub">Algebra I · Mr. Pandey · SE pp. 345–356 · Every activity here is essential (✪) on the 150-day pacing guide '
            '(Activity 1.3 Tic-Tac-Bingo is not starred; save it for the retake day). '
            '<b>SAY</b> = read to class · <b>ASK</b> = question with the answer to listen for · blue boxes = what to write on the board, fully solved.</p>')
    body = f'<h2 class="first">Thursday, Nov 5 · One day · One, none, or infinite solutions</h2>{"".join(DAY)}'
    return f'<!doctype html><html><head><meta charset="utf-8"><title>M3T1 Lesson 1 Script</title><style>{CSS}</style></head><body>{head}{body}</body></html>'


if __name__ == "__main__":
    # the math behind the worked answers
    assert -3 * 2 + 14 == 18 - 5 * 2 and 2 * 2 == 5 - F(1, 2) * 2
    assert abs(0.6 * (2 * -2 + 1) - (4 * -2 + 6.2)) < 1e-9 and F(1, 2) * -6 - 6 == 2 + (2 * -6 + 1) and 4 * (3 * -1 + 2) == 8 * -1 + 4
    assert 6 * (5 + 2 * 2.5) == 8 * (2.5 + 5)
    assert 7 - 3 * (-4 + 2) == 10 - (2 * -4 + 5) and 0.5 * (4 * 2 - 6) == -1.5 * 2 + 4 and F(1, 2) * 6 * (19 + 5) == 4 * (19 - 1)
    x = F(19, 17); assert (-2 * x - 4) / 5 + F(8, 5) == 3 * (x - 1)
    assert 3 * 2.6 - 8 == -7 * 2.6 + 18 or abs(3 * 2.6 - 8 - (-7 * 2.6 + 18)) < 1e-9
    assert -2 * (4 - F(-1, 2)) == 12 * F(-1, 2) - 3 and F(1, 2) * (-60 + 4) == -4 * (-3 + 12) + 8
    assert F(4, 3) * -3 + 2 * (9 - F(1, 3) * -3) == F(-7, 3) * -3 + 9
    assert 4 * (0.2 * 7 - 1.2) == -0.5 * 7 + 4.3 or abs(4 * (0.2 * 7 - 1.2) - (-0.5 * 7 + 4.3)) < 1e-9
    assert (F(1, 2) * 2 - 5) / 2 == -3 * 2 + 4
    W.pdf(html(), OUT, sys.argv[1])

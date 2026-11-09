"""Teacher script for M3T1 Lesson 2 (Literal Equations), Day 1 (Mon Nov 9) and Day 2 (Tue Nov 10):
what to say, what to ask, and every essential (✪) problem worked step by step. SE pp. 357-370.
Run:  python make_m3t1_l2_script.py <password>   ->  Module 3 topic 1/LESSON PLANS/M3T1-Lesson2-Teaching-Script.pdf"""
import subprocess, sys
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "Module 3 topic 1" / "LESSON PLANS" / "M3T1-Lesson2-Teaching-Script.pdf"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"


def say(t): return f'<p class="say"><span class="lb">SAY</span> {t}</p>'
def ask(q, a): return f'<p class="ask"><span class="lb">ASK</span> {q} <span class="exp">Listen for: {a}</span></p>'
def board(*lines): return '<div class="board">' + "".join(f"<div>{l}</div>" for l in lines) + "</div>"
def prob(title, *body): return f'<div class="prob"><h4>{title}</h4>{"".join(body)}</div>'
def part(time, title, *body): return f'<section><h3><span class="t">{time}</span> {title}</h3>{"".join(body)}</section>'
def tip(t): return f'<p class="tip"><span class="lb">Watch for</span> {t}</p>'


DAY1 = [
    part("0–5", "Bell work", say("Bell work is on the board. Four questions: two from Lesson 1, two about lines. You have five minutes."),
         board("1. 2(x + 3) = x − 4 → 2x + 6 = x − 4 → x = −10", "2. 3x + 1 = 3x − 5 → 1 = −5 is false → no solution",
               "3. y = −2x + 7 → slope −2, y-intercept (0, 7)", "4. y = 2x − 6: set y = 0 → 0 = 2x − 6 → x = 3 → (3, 0)")),
    part("5–10", "Homework check (Lesson 1, Practice 2)", board("a none · b x = 7 · d infinite · f infinite")),
    part("10–12", "Launch the lesson (SE p. 357)",
         say("Last lesson you used the properties of equality to find the one number that makes an equation true. "
             "Today we use those same moves, but the equation has <i>several</i> letters, and we get one letter by itself."),
         say("Big idea for the whole lesson: <b>a letter you are not solving for acts just like a number.</b> "
             "You add, subtract, multiply and divide it the same way.")),
    part("12–25", "✪ Getting Started: Perimeter Perspectives (SE p. 358)",
         say("Juan and Mia share the park's sides. The city tells them the perimeter P. Juan needs the width w. Mia needs the length ℓ. "
             "Remember, the perimeter of a rectangle is P = 2ℓ + 2w."),
         ask("Which letter does Juan want alone? Which does Mia want?", "Juan → w, Mia → ℓ"),
         prob("Q1 · Juan solves for w",
              board("P = 2ℓ + 2w", "P − 2ℓ = 2w &nbsp;&nbsp;(subtract 2ℓ from both sides)", "(P − 2ℓ)/2 = w &nbsp;&nbsp;(divide both sides by 2)",
                    "<b>w = P/2 − ℓ</b>")),
         prob("Q1 · Mia solves for ℓ",
              board("P = 2ℓ + 2w", "P − 2w = 2ℓ", "<b>ℓ = P/2 − w</b>")),
         prob("Q2 · Show they are equivalent",
              board("Juan: w = P/2 − ℓ → multiply by 2 → 2w = P − 2ℓ → add 2ℓ → <b>2ℓ + 2w = P</b>",
                    "Mia: ℓ = P/2 − w → multiply by 2 → 2ℓ = P − 2w → add 2w → <b>2ℓ + 2w = P</b>"),
              say("Both go back to the same formula. Same equation, just solved for the letter each person needs.")),
         tip("students who divide only P by 2 and forget the 2ℓ: (P − 2ℓ)/2 means divide <i>every</i> term.")),
    part("25–40", "✪ Activity 2.1: Equations in Different Forms (SE pp. 359–360)",
         say("Two tools for the whole activity. <b>y-intercept: put 0 in for x.</b> <b>x-intercept: put 0 in for y.</b>"),
         prob("Q1 · y = −⅔x + 4",
              board("a. Slope: the number in front of x → <b>−⅔</b>", "b. y-intercept: x = 0 → y = 4 → <b>(0, 4)</b>",
                    "c. x-intercept: 0 = −⅔x + 4 → ⅔x = 4 → x = 4 · 3/2 = 6 → <b>(6, 0)</b>",
                    "d. Slope and y-intercept read straight off y = mx + b; x-intercept by substituting y = 0.")),
         prob("Q2 · y = 4(x − 2)",
              board("a. Slope: <b>4</b>", "b. x = 0 → y = 4(−2) = −8 → <b>(0, −8)</b>",
                    "c. y = 0 → 0 = 4(x − 2) → x − 2 = 0 → x = 2 → <b>(2, 0)</b>",
                    "d. It is point-slope form y − 0 = 4(x − 2): slope 4 through (2, 0).")),
         prob("Q3 · 3x − 2y = 8",
              board("Rewrite: −2y = −3x + 8 → y = (3/2)x − 4", "a. Slope: <b>3/2</b>",
                    "b. x = 0 → −2y = 8 → y = −4 → <b>(0, −4)</b>", "c. y = 0 → 3x = 8 → x = 8/3 → <b>(8/3, 0)</b>")),
         tip("in Q3, when dividing by −2, <i>every</i> term flips sign: −3x ÷ −2 = +3/2 x and 8 ÷ −2 = −4."),
         prob("Q4 · Name the forms",
              board("Q1 slope-intercept (y = mx + b) · Q2 point-slope (y − y₁ = m(x − x₁)) · Q3 standard (Ax + By = C)")),
         prob("Q5 · Ax + By = C, the general case",
              board("Slope: By = −Ax + C → y = (−A/B)x + C/B → <b>slope = −A/B</b>",
                    "x-intercept: y = 0 → Ax = C → <b>(C/A, 0)</b>", "y-intercept: x = 0 → By = C → <b>(0, C/B)</b>"),
              say("In standard form, A, B and C are integers, and A and B are not both 0. No fractions, no decimals.")),
         prob("Q6–Q7 · Which form is fastest?",
              board("a. Slope → slope-intercept or point-slope (it is m)", "b. A point → point-slope (x₁, y₁)",
                    "c. y-intercept → slope-intercept (it is b)",
                    "Q7. Graphing technology → slope-intercept, because the calculator needs y = ...")),
         ask("Thumbs up or down: standard form can have A = ½.", "Down. A, B, C must be integers.")),
    part("40–50", "✪ Activity 2.1: Rewriting forms (SE p. 361)",
         say("Recipe to get to <b>slope-intercept</b>: distribute, then get y alone. Recipe to get to <b>standard</b>: clear fractions or decimals, "
             "then move x and y to the left and the number to the right."),
         prob("Q8a · y − 2 = 5(x − 7) → slope-intercept",
              board("y − 2 = 5x − 35 &nbsp;(distribute)", "<b>y = 5x − 33</b> &nbsp;(add 2)")),
         prob("Q8b · 8x − 2y = 12 → slope-intercept",
              board("−2y = −8x + 12 &nbsp;(subtract 8x)", "<b>y = 4x − 6</b> &nbsp;(divide every term by −2)")),
         prob("Q9a · y + 7 = 0.5(x − 1) → standard",
              board("y + 7 = 0.5x − 0.5 &nbsp;(distribute)", "2y + 14 = x − 1 &nbsp;(multiply by 2 to clear the decimal)",
                    "15 = x − 2y &nbsp;(subtract 2y and add 1)", "<b>x − 2y = 15</b>",
                    "Check with the point (1, −7): 1 − 2(−7) = 15 ✓")),
         prob("Q9b · y = −4x + 3 → standard", board("<b>4x + y = 3</b> &nbsp;(add 4x)")),
         prob("Q10 (if time) · Standard form through a point",
              board("a. slope ½ through (−3, 5): y − 5 = ½(x + 3) → 2y − 10 = x + 3 → <b>x − 2y = −13</b>",
                    "&nbsp;&nbsp;&nbsp;Check: −3 − 2(5) = −13 ✓",
                    "b. slope −4 through (2, 1): y − 1 = −4(x − 2) → y − 1 = −4x + 8 → <b>4x + y = 9</b>",
                    "&nbsp;&nbsp;&nbsp;Check: 4(2) + 1 = 9 ✓")),
         prob("Test move (like End of Topic Q7 and Q10)",
              board("4x + 3y = 12 → 3y = −4x + 12 → <b>y = −(4/3)x + 4</b>", "y + 4 = 3(x − 2) → y + 4 = 3x − 6 → <b>y = 3x − 10</b>"),
              say("Standard form: subtract the x-term, then divide <i>every</i> term. Point-slope: distribute, then move the constant."))),
    part("50–58", "Exit ticket",
         board("1. 6x + 3y = 12 → 3y = −6x + 12 → <b>y = −2x + 4</b>", "2. y − 4 = 3(x + 2) → y − 4 = 3x + 6 → <b>y = 3x + 10</b>",
               "3. 2x − 5y = 10: y = 0 → x = 5 → <b>(5, 0)</b>; x = 0 → y = −2 → <b>(0, −2)</b>")),
    part("58–60", "Wrap up",
         say("Tonight: Lesson 2 Assignment, Practice 1a–d, SE p. 369. Tomorrow we use the same moves on real formulas, like temperature and volume."),
         board("Key: a 3x − 4y = 32 · b y = −3x + 15 · c y = (5/2)x + 9 · d x − 2y = 22")),
]

DAY2 = [
    part("0–5", "Bell work",
         board("1. 4x + 2y = 10 → 2y = −4x + 10 → y = −2x + 5", "2. 3x − 7 = 11 → 3x = 18 → x = 6",
               "3. P = 2ℓ + 2w, P = 30, w = 5 → 30 = 2ℓ + 10 → ℓ = 10", "4. C = 5/9(F − 32), F = 50 → 5/9(18) = 10"),
         say("Questions 3 and 4 are formulas. Today we solve formulas for whichever letter we need.")),
    part("5–20", "✪ Activity 2.2: Rewriting Literal Equations (SE pp. 362–363)",
         say("A <b>literal equation</b> is an equation where the letters stand for real measures, like a formula. "
             "Write it in your notes: <i>a formula you can solve for any one of its letters.</i>"),
         say("Jayden thinks in °F. Mateo thinks in °C. The formula C = 5/9(F − 32) turns °F into °C. Jayden needs one that turns °C into °F."),
         ask("What is happening to F, in order?", "subtract 32, then multiply by 5/9. So undo in reverse: multiply by 9/5, then add 32."),
         prob("Q1 · Solve C = 5/9(F − 32) for F",
              board("(9/5)C = F − 32 &nbsp;(multiply both sides by 9/5)", "<b>F = (9/5)C + 32</b> &nbsp;(add 32)")),
         prob("Q2 · Who is warmer: 77°F or 30°C?",
              board("F = (9/5)(30) + 32 = 54 + 32 = 86°F", "86°F > 77°F → <b>Mateo is correct</b>",
                    "Or the other way: C = 5/9(77 − 32) = 5/9(45) = 25°C < 30°C")),
         ask("Thumbs: to get F alone, subtract 32 first.", "Down. The 32 is inside the parentheses; multiply by 9/5 first (or distribute first).")),
    part("20–25", "✪ Activity 2.2: Find the error, Worked Example (SE pp. 363–364)",
         prob("Q3a · Isabella (correct)",
              board("Distributed 5/9: C = (5/9)F − 160/9", "Multiplied by 9: 9C = 5F − 160", "Added 160, divided by 5: <b>(9/5)C + 32 = F</b>")),
         prob("Q3b · Ethan's error", board("He wrote C = (5/9)F − 32. He did <b>not distribute 5/9 to the 32</b>. It should be −160/9.")),
         prob("Q3c · Minh's error",
              board("9 · (5/9)F is <b>5F</b>, not 45F, and 9 · (160/9) is <b>160</b>, not 1440.",
                    "He multiplied the numerators by 9 instead of cancelling the 9s.")),
         prob("Q4 · Rewrite C = 5/9(F − 32) with no fractions",
              board("9C = 5(F − 32) &nbsp;(multiply both sides by 9)", "9C = 5F − 160", "<b>160 = 5F − 9C</b> &nbsp;(same as 9C − 5F = −160)"))),
    part("25–45", "✪ Activity 2.3: Solving Literal Equations for Specific Variables (SE pp. 365–366)",
         say("Same rule as yesterday: whatever is attached to the letter you want, undo it. Do the same thing to both sides."),
         prob("Q1 · Box: volume and height",
              board("a. V = Bh → divide by B → <b>h = V/B</b>", "b. V = 450 in³, B = 75 in² → h = 450/75 = <b>6 inches</b>")),
         prob("Q2 · Ice cream cone",
              board("a. V = (1/3)πr²h", "3V = πr²h &nbsp;(multiply by 3)", "<b>h = 3V/(πr²)</b> &nbsp;(divide by πr²)",
                    "b. Units: cubic units ÷ square units = in³/in² = <b>in</b>, a length.")),
         prob("Q3 · Trapezoid",
              board("a. A = ½h(b₁ + b₂) → 2A = h(b₁ + b₂) → <b>h = 2A/(b₁ + b₂)</b>",
                    "b. A = 24, b₁ = 9, b₂ = 7 → h = 48/16 = <b>3 cm</b>")),
         prob("Q4 · Z = A/B + C/D",
              board("a. Solve for A: Z − C/D = A/B → multiply by B → <b>A = BZ − BC/D</b>",
                    "b. Solve for D (challenge): Z − A/B = C/D → D(Z − A/B) = C → D = C/(Z − A/B)",
                    "&nbsp;&nbsp;&nbsp;Multiply top and bottom by B: <b>D = BC/(BZ − A)</b>")),
         prob("Test move (like End of Topic Q8)",
              board("V = ℓwh for w → divide by ℓh → <b>w = V/(ℓh)</b>", "A = ½bh for h → 2A = bh → <b>h = 2A/b</b>")),
         tip("students who 'move' a letter without doing the same thing to both sides. Make them say the property out loud.")),
    part("45–57", "✪ Talk the Talk: Rearrange It (SE p. 367) · use 3.14 for π",
         prob("Q1 · S = 2πrh, solve for h", board("Divide by 2πr → <b>h = S/(2πr)</b>")),
         prob("Q2 · S = 37.68, r = 1.5", board("2(3.14)(1.5) = 9.42", "h = 37.68/9.42 = <b>4 inches</b>")),
         prob("Q3 · S = 2πr² + 2πrh, solve for h", board("S − 2πr² = 2πrh &nbsp;(subtract 2πr²)", "<b>h = (S − 2πr²)/(2πr)</b> &nbsp;(divide by 2πr)")),
         prob("Q4 · S = 51.81, r = 1.5",
              board("2πr² = 2(3.14)(2.25) = 14.13", "51.81 − 14.13 = 37.68", "h = 37.68/9.42 = <b>4 inches</b> (same can as Q2)")),
         say("Exit ticket for today is on the half sheet."),
         board("Exit: 1. A = ℓw → w = A/ℓ · 2. V = πr²h → h = V/(πr²) · 3. d = rt → r = d/t · 4. S = 2πrh, S = 37.68, r = 1.5 → h = 4 in.")),
    part("57–60", "Essential Question and homework",
         ask("How can you use the same properties to solve for one variable in an equation with several variables?",
             "Undo each operation on that variable, doing the same thing to both sides. Treat the other letters like numbers."),
         say("Homework: Lesson 2 Assignment, Practice 2–3 and Prepare, SE p. 370."),
         board("2a V = ℓwh (or Bh) · 2b 112 × 3.5 = 392 in³ · 2c h = V/B · 2d 1 ft = 12 in: 456 = 12 · w · 4 → w = 9.5 in",
               "3a B = 3V/h · 3b r = I/(pt) · 3c y = 18 − x · 3d C = 180 − A − B",
               "Prepare: x = 5 · x > 7 · x ≤ −3 · x < −4")),
]

CSS = """@page{size:letter;margin:.55in .6in}body{font:11pt/1.4 'Segoe UI',Arial,sans-serif;color:#111}
h1{font-size:19pt;margin:0}h2{font-size:15pt;background:#1d3557;color:#fff;padding:6px 10px;margin:18px 0 8px;break-before:page}
h2.first{break-before:auto}h3{font-size:12pt;border-bottom:2px solid #457b9d;margin:14px 0 6px;padding-bottom:2px}
.t{display:inline-block;background:#457b9d;color:#fff;border-radius:4px;padding:0 6px;font-size:10pt;margin-right:4px}
h4{font-size:11pt;margin:6px 0 3px;color:#1d3557}.prob{break-inside:avoid;margin:6px 0 8px 8px}
.say,.ask,.tip{margin:4px 0}.lb{display:inline-block;width:44px;font-size:9pt;color:#fff;text-align:center;border-radius:3px;margin-right:6px}
.say .lb{background:#2a9d8f}.ask .lb{background:#e76f51}.tip .lb{background:#888;width:auto;padding:0 5px}
.exp{color:#555;font-style:italic}.board{font-family:Cambria,'Times New Roman',serif;font-size:12pt;background:#f4f7fa;border-left:4px solid #457b9d;padding:5px 10px;margin:3px 0}
.board div{margin:2px 0}.sub{color:#444;margin:2px 0 10px}section{break-inside:auto}"""


def html():
    head = ('<h1>Module 3 Topic 1 · Lesson 2: Literal Equations · Teaching Script</h1>'
            '<p class="sub">Algebra I · Mr. Pandey · SE pp. 357–370 · Every activity is essential (✪) on the 150-day pacing guide. '
            '<b>SAY</b> = read to class · <b>ASK</b> = question with the answer to listen for · blue boxes = what to write on the board, fully solved.</p>')
    body = (f'<h2 class="first">Day 1 · Monday, Nov 9 · Equations in Different Forms</h2>{"".join(DAY1)}'
            f'<h2>Day 2 · Tuesday, Nov 10 · Solving Formulas for a Letter</h2>{"".join(DAY2)}')
    return f'<!doctype html><html><head><meta charset="utf-8"><title>M3T1 Lesson 2 Script</title><style>{CSS}</style></head><body>{head}{body}</body></html>'


if __name__ == "__main__":
    PASSWORD = sys.argv[1]  # kept out of the repo; the encrypted PDF is what protects the script
    src = OUT.with_suffix(".html")
    src.write_text(html(), encoding="utf-8")
    subprocess.run([EDGE, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={OUT}", src.as_uri()],
                   check=True, capture_output=True)
    src.unlink()
    import fitz  # password-protect: the browser asks for it before showing the PDF
    tmp = OUT.with_suffix(".tmp.pdf"); OUT.replace(tmp)
    with fitz.open(tmp) as d:
        d.save(OUT, encryption=fitz.PDF_ENCRYPT_AES_256, user_pw=PASSWORD, owner_pw=PASSWORD)
    tmp.unlink()
    print(OUT)

"""Narrated explainer videos for Module 2 Topic 2: Lesson 1 (vertical translations, dilations, reflections), Lesson 2
(horizontal translations and dilations vs. vertical), Lesson 3 (perpendicular slopes), Lesson 4 (comparing functions).
Draws frames with Pillow, speaks each caption with a Microsoft neural voice (edge-tts), joins them with ffmpeg.
Run:  python make_t2_video.py [1 2 3 4]      ->  Module 2 topic 2/videos/T2-Lesson{n}-....mp4  (no arguments: all)"""
import asyncio, math, os, re, subprocess, sys, tempfile
import edge_tts
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1280, 720, 24
VIDEOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Module 2 topic 2", "videos")
VOICE, RATE = "en-US-JennyNeural", "-5%"
FONT = "C:/Windows/Fonts/calibri.ttf"
BOLD = "C:/Windows/Fonts/calibrib.ttf"
F = {s: ImageFont.truetype(FONT, s) for s in (18, 26, 30, 34)}
FB = {s: ImageFont.truetype(BOLD, s) for s in (26, 34, 44, 60)}
INK, GRID, AX, BLUE, RED, GREEN, MUTED = "#1d2433", "#e3e7ee", "#5b6478", "#2563eb", "#dc2626", "#15803d", "#6b7280"

# graph: x and y from -10 to 10 in a square on the left
GX, GY, GS, R = 50, 30, 570, 10
def px(x, y): return GX + (x + R) / (2 * R) * GS, GY + (R - y) / (2 * R) * GS

# Each scene: title, parent line f = (slope, intercept, label) (default f(x) = x), x-values of the points to track, steps.
# The red line is g(x) = a · f(b(x − h)) + d: the parent point (x, f(x)) moves to (x/b + h, a · f(x) + d).
# A step: (caption, spoken text or None, move or None, panel line or None). A move is (a, d) or a dict of a, b, h, d;
# reset=True first leaves the red line as a gray ghost and starts again from f. "PAUSE n" in the caption = n s of quiet.
# kind="title" is a title card; kind="list" shows the panel lines full width, no graph.
SCENES_1 = [
    dict(kind="title", title="Transforming Linear Functions", sub="Module 2 · Topic 2 · Lesson 1",
         steps=[("Today: what adding, multiplying, and a negative sign do to the graph of f(x) = x.", None, None, None)]),
    dict(title="The parent function", pts=[-4, 2, 6], steps=[
        ("This is f(x) = x.", None, None, "f(x) = x"),
        ("Every output equals its input: (2, 2), (6, 6), (−4, −4).", "Every output equals its input. 2 goes to 2, 6 goes to 6, negative 4 goes to negative 4.", None, None),
        ("Its slope is 1 and its y-intercept is (0, 0).", "Its slope is 1, and its y-intercept is the origin, 0 comma 0.", None, "slope 1, y-intercept (0, 0)"),
    ]),
    dict(title="Add: f(x) + 8", pts=[-4, 2, 6], steps=[
        ("Now add 8 to every output: k(x) = f(x) + 8.", None, None, "k(x) = f(x) + 8"),
        ("Watch: every point moves up 8 units.", None, (1, 8), None),
        ("The slope is still 1, so the two lines are parallel.", None, None, "slope 1 (same): parallel"),
        ("Only the y-intercept changed, from (0, 0) to (0, 8).", "Only the y-intercept changed, from 0 to 8.", None, "y-intercept (0, 8)"),
        ("f(x) + d moves the graph up d units. This is a vertical translation.", None, None, "k(x) = x + 8"),
    ]),
    dict(title="Subtract: f(x) − 7", pts=[-4, 2, 6], steps=[
        ("Subtracting moves the graph down: j(x) = f(x) − 7.", None, None, "j(x) = f(x) − 7"),
        ("Every point moves down 7 units.", None, (1, -7), None),
        ("Same slope, 1. The y-intercept is now (0, −7).", "Same slope, 1. The y-intercept is now negative 7.", None, "j(x) = x − 7"),
    ]),
    dict(title="Multiply: 2 · f(x)", pts=[-4, 2, 4], label=True, steps=[
        ("Now multiply every output by 2: h(x) = 2 · f(x).", None, None, "h(x) = 2 · f(x)"),
        ("Each output doubles. (2, 2) becomes (2, 4), and (4, 4) becomes (4, 8).", None, (2, 0), None),
        ("The origin does not move, because 2 times 0 is still 0.", None, None, None),
        ("The line is steeper. Its slope is now 2.", None, None, "slope 2: steeper"),
        ("This is a vertical stretch by a factor of 2.", None, None, "h(x) = 2x"),
    ]),
    dict(title="Multiply: (1/3) · f(x)", pts=[-6, 3, 6], label=True, steps=[
        ("Multiply by one third: g(x) = (1/3) · f(x).", "Multiply by one third. g of x equals one third times f of x.", None, "g(x) = (1/3) · f(x)"),
        ("Each output is one third as big. (3, 3) becomes (3, 1), and (6, 6) becomes (6, 2).", None, (1 / 3, 0), None),
        ("The slope is 1/3, so the line is less steep.", "The slope is one third, so the line is less steep.", None, "slope 1/3: less steep"),
        ("A factor between 0 and 1 is a vertical compression.", None, None, "g(x) = (1/3)x"),
    ]),
    dict(title="A negative sign: −f(x)", pts=[-4, 2, 6], label=True, steps=[
        ("A negative sign changes the sign of every output: r(x) = −f(x).", "A negative sign changes the sign of every output. r of x equals negative f of x.", None, "r(x) = −f(x)"),
        ("(2, 2) becomes (2, −2). The graph reflects across the x-axis.", "2 comma 2 becomes 2 comma negative 2. The graph reflects across the x-axis.", (-1, 0), None),
        ("The slope changes from 1 to −1.", "The slope changes from 1 to negative 1.", None, "slope −1: reflection"),
    ]),
    dict(title="Both: 2 · f(x) + 3", pts=[-2, 2, 4], steps=[
        ("You can do both: g(x) = 2 · f(x) + 3.", None, None, "g(x) = 2 · f(x) + 3"),
        ("First the 2 stretches the line. The slope becomes 2.", None, (2, 0), "a = 2: slope 2"),
        ("Then the 3 moves it up 3. The y-intercept becomes (0, 3).", "Then the 3 moves it up 3. The y-intercept becomes 3.", (2, 3), "d = 3: y-intercept (0, 3)"),
        ("So g(x) = 2x + 3. The a-value changes the slope; the d-value changes the y-intercept.", None, None, "g(x) = 2x + 3"),
    ]),
    dict(title="Your turn", pts=[-2, 1, 3], steps=[
        ("Describe g(x) = 3 · f(x) − 2. What are its slope and y-intercept?", "Describe g of x equals 3 times f of x minus 2. What are its slope and y-intercept?", None, "g(x) = 3 · f(x) − 2"),
        ("Pause the video and try it.  PAUSE 5", "Pause the video and try it.", None, None),
        ("Vertical stretch by 3, then down 2. Slope 3, y-intercept (0, −2).", "It is a vertical stretch by 3, then a translation down 2. The slope is 3, and the y-intercept is negative 2.", (3, -2), "slope 3, y-intercept (0, −2)"),
        ("g(x) = 3x − 2.", "So g of x equals 3 x minus 2.", None, "g(x) = 3x − 2"),
    ]),
    dict(kind="title", title="g(x) = a · f(x) + d", sub="a changes the slope  ·  d changes the y-intercept", steps=[
        ("Adding d moves the graph up or down. The slope stays the same.", None, None, None),
        ("Multiplying by a changes the slope: steeper if a is greater than 1, less steep between 0 and 1, and a negative a reflects it.", None, None, None),
        ("Now try the matching on page 284 of your book.", None, None, None),
    ]),
]
SCENES_2 = [
    dict(kind="title", title="Vertical and Horizontal Transformations", sub="Module 2 · Topic 2 · Lesson 2",
         steps=[("Last lesson we changed the outputs of f(x) = x. Today we change the inputs, and compare the two.", None, None, None)]),
    dict(title="Move right: f(x − 5)", pts=[-2, 0, 2], label=True, steps=[
        ("Translate f(x) = x right 5 units: every point moves 5 units to the right.", None, dict(h=5), "m(x) = f(x − 5)"),
        ("(0, 0) moves to (5, 0), and (2, 2) moves to (7, 2).", "0 comma 0 moves to 5 comma 0, and 2 comma 2 moves to 7 comma 2.", None, None),
        ("The outputs stay the same. Only the inputs change: each x-value goes up by 5.", None, None, "inputs + 5, outputs the same"),
        ("This graph is m(x) = f(x − 5). Subtracting inside the parentheses moves the graph right.",
         "This graph is m of x equals f of x minus 5. Subtracting inside the parentheses moves the graph right.", None, None),
        ("Careful: x − 5 moves right, not left. It is the opposite of what the sign looks like.",
         "Careful. x minus 5 moves right, not left. It is the opposite of what the sign looks like.", None, "f(x − h): right h"),
    ]),
    dict(title="Move left: f(x + 3)", pts=[-2, 0, 2], label=True, steps=[
        ("Adding inside the parentheses moves the graph left: t(x) = f(x + 3).",
         "Adding inside the parentheses moves the graph left. t of x equals f of x plus 3.", dict(h=-3), "t(x) = f(x + 3)"),
        ("(0, 0) moves to (−3, 0). Every point moves 3 units left.",
         "0 comma 0 moves to negative 3 comma 0. Every point moves 3 units left.", None, "f(x + h): left h"),
    ]),
    dict(title="Right 5 or down 5?", pts=[-2, 2, 6], steps=[
        ("Move f(x) = x right 5 units. We get the line y = x − 5.",
         "Move f of x equals x right 5 units. We get the line y equals x minus 5.", dict(h=5), "f(x − 5) = x − 5"),
        ("Now start over, and move f(x) down 5 units instead.", "Now start over, and move f of x down 5 units instead.",
         dict(reset=True, d=-5), "f(x) − 5 = x − 5"),
        ("It lands on the same line! For f(x) = x, right 5 is the same as down 5.",
         "It lands on the same line! For f of x equals x, right 5 is the same as down 5.", None, "right n = down n (for f(x) = x)"),
    ]),
    dict(title="Is it true for every line?", f=(2, -1, "j(x) = 2x − 1"), fpos=(9.6, 5), pts=[-1, 1, 2], steps=[
        ("Try j(x) = 2x − 1. Move it up 4: q(x) = j(x) + 4 = 2x + 3.",
         "Try j of x equals 2 x minus 1. Move it up 4. q of x equals j of x plus 4, which is 2 x plus 3.", dict(d=4), "q(x) = j(x) + 4 = 2x + 3"),
        ("Now start over and move j(x) left 4: r(x) = j(x + 4).",
         "Now start over and move j of x left 4. r of x equals j of x plus 4, inside the parentheses.", dict(reset=True, h=-4),
         "r(x) = j(x + 4) = 2x + 7"),
        ("These are not the same line. r(x) = 2(x + 4) − 1 = 2x + 7.",
         "These are not the same line. r of x equals 2 times x plus 4, minus 1, which is 2 x plus 7.", None, None),
        ("With slope 2, moving left 4 is the same as moving up 8, because 2 times 4 is 8.", None, None, "left 4 = up 8 (slope 2)"),
        ("So right n equals down n only when the slope is 1.", None, None, None),
    ]),
    dict(title="Stretch outputs or inputs?", pts=[-4, 2, 4], label=True, steps=[
        ("Multiply the outputs of f(x) = x by 2: a(x) = 2 · f(x). (2, 2) becomes (2, 4).",
         "Multiply the outputs of f of x equals x by 2. a of x equals 2 times f of x. 2 comma 2 becomes 2 comma 4.", dict(a=2),
         "a(x) = 2 · f(x) = 2x"),
        ("Now start over and change the inputs instead: b(x) = f(2x). Each x-value is multiplied by 1/2.",
         "Now start over and change the inputs instead. b of x equals f of 2 x. Each x value is multiplied by one half.",
         dict(reset=True, b=2), "b(x) = f(2x) = 2x"),
        ("(4, 4) moves to (2, 4). The graph is squeezed toward the y-axis: a horizontal compression by 1/2.",
         "4 comma 4 moves to 2 comma 4. The graph is squeezed toward the y-axis. That is a horizontal compression by a factor of one half.",
         None, "f(bx): horizontal, factor 1/b"),
        ("Same line, y = 2x. For f(x) = x, a vertical stretch by 2 equals a horizontal compression by 1/2.",
         "Same line, y equals 2 x. For f of x equals x, a vertical stretch by 2 is the same as a horizontal compression by one half.",
         None, "vertical n = horizontal 1/n"),
    ]),
    dict(title="The other way", pts=[-4, 2, 4], label=True, steps=[
        ("Outputs times 1/2: c(x) = (1/2) · f(x). The line gets less steep.",
         "Outputs times one half. c of x equals one half times f of x. The line gets less steep.", dict(a=0.5), "c(x) = (1/2) · f(x) = (1/2)x"),
        ("Inputs times 1/2: d(x) = f((1/2)x). The graph stretches away from the y-axis. Same line again.",
         "Inputs times one half. d of x equals f of one half x. The graph stretches away from the y-axis. Same line again.",
         dict(reset=True, b=0.5), "d(x) = f((1/2)x) = (1/2)x"),
    ]),
    dict(kind="list", title="Summary: inside or outside?", steps=[
        ("Outside the parentheses changes the outputs: the graph moves up or down, or stretches vertically.", None, None,
         "Outside changes the outputs\nf(x) + d: moves up d\na · f(x): stretches or compresses vertically"),
        ("Inside the parentheses changes the inputs: the graph moves left or right, or stretches horizontally.", None, None,
         "Inside changes the inputs\nf(x − h): moves right h;  f(x + h): moves left h\nf(bx): stretches or compresses horizontally, factor 1/b"),
        ("Inside works the opposite way: minus moves right, and times 2 squeezes by one half.", None, None,
         "Inside is the opposite of what it looks like: minus moves right, times 2 squeezes"),
        ("For f(x) = x, right n is the same as down n. For other slopes, it is not.",
         "For f of x equals x, right n is the same as down n. For other slopes, it is not.", None, "f(x) = x only: right n = down n"),
    ]),
    dict(title="Your turn", pts=[-2, 0, 2], label=True, steps=[
        ("Describe g(x) = f(x + 5), where f(x) = x. Which way does it move?",
         "Describe g of x equals f of x plus 5, where f of x equals x. Which way does it move?", None, "g(x) = f(x + 5)"),
        ("Pause the video and try it.  PAUSE 5", "Pause the video and try it.", None, None),
        ("Left 5 units. Every point moves 5 to the left.", None, dict(h=-5), "left 5"),
        ("Simplified, g(x) = x + 5. For f(x) = x, that is the same line as moving up 5.",
         "Simplified, g of x equals x plus 5. For f of x equals x, that is the same line as moving up 5.", None, "g(x) = x + 5"),
        ("Now try Show Me What You've Got on page 301 of your book.", None, None, None),
    ]),
]
SCENES_3 = [
    dict(kind="title", title="Slopes of Perpendicular Lines", sub="Module 2 · Topic 2 · Lesson 3",
         steps=[("Parallel lines have the same slope. Today: what happens to the slope when we turn a line 90 degrees?", None, None, None)]),
    dict(title="Turn a line 90°", f=(5 / 8, 0, "slope 5/8"), fpos=(9.6, 3.2), pts=[0, 8], label=True, steps=[
        ("Here is a line through A(0, 0) and B(8, 5). Its slope is rise over run: 5/8.",
         "Here is a line through A, at 0 comma 0, and B, at 8 comma 5. Its slope is rise over run: 5 eighths.", None, "slope of AB = 5/8"),
        ("Rotate it 90° counterclockwise about the origin.", "Rotate it 90 degrees counterclockwise about the origin.", dict(rot=90), None),
        ("B(8, 5) lands on (−5, 8). The x and y switch places, and one sign changes.",
         "B, at 8 comma 5, lands on negative 5 comma 8. The x and y switch places, and one sign changes.", None, "(8, 5) → (−5, 8)"),
        ("The new slope is 8 over −5, which is −8/5.", "The new slope is 8 over negative 5, which is negative 8 fifths.", None, "new slope = −8/5"),
        ("5/8 and −8/5: flip the fraction and change the sign. These are negative reciprocals.",
         "5 eighths and negative 8 fifths. Flip the fraction and change the sign. These are negative reciprocals.", None,
         "negative reciprocals"),
    ]),
    dict(title="Multiply the slopes", f=(2, 0, "y = 2x"), fpos=(9.6, 7), pts=[1, 3], label=True, steps=[
        ("Try a line with slope 2, and turn it 90°.", "Try a line with slope 2, and turn it 90 degrees.", dict(rot=90), "slope 2"),
        ("(1, 2) moves to (−2, 1). The new slope is −1/2.",
         "1 comma 2 moves to negative 2 comma 1. The new slope is negative one half.", None, "new slope −1/2"),
        ("Multiply the slopes: 2 times −1/2 is −1.", "Multiply the slopes. 2 times negative one half is negative 1.", None, "2 · (−1/2) = −1"),
        ("If two lines are perpendicular, the product of their slopes is −1.",
         "If two lines are perpendicular, the product of their slopes is negative 1.", None, "perpendicular: product −1"),
    ]),
    dict(title="Horizontal and vertical", f=(0, 3, "y = 3"), fpos=(9.6, 2.2), center=(2, 3), pts=[-4, 6], label=True, steps=[
        ("A horizontal line, like y = 3, has slope 0: y never changes.", None, None, "y = 3: slope 0"),
        ("Turn it 90° about (2, 3). It becomes the vertical line x = 2.",
         "Turn it 90 degrees about the point 2 comma 3. It becomes the vertical line x equals 2.", dict(rot=90), "x = 2"),
        ("On a vertical line, x never changes. The run is 0, and we cannot divide by 0, so the slope is undefined.", None, None,
         "x = 2: slope undefined"),
        ("Every horizontal line is perpendicular to every vertical line.", None, None, "horizontal and vertical: perpendicular"),
    ]),
    dict(title="Write a perpendicular line", f=(2, 1, "y = 2x + 1"), fpos=(9.6, 6.4), center=(1.6, 4.2),
         marks=[(6, 2, "(6, 2)", "tr")], steps=[
        ("Write the line through (6, 2) that is perpendicular to y = 2x + 1.",
         "Write the line through 6 comma 2 that is perpendicular to y equals 2 x plus 1.", None, "given: y = 2x + 1 and the point (6, 2)"),
        ("The given slope is 2, so the perpendicular slope is its negative reciprocal, −1/2.",
         "The given slope is 2, so the perpendicular slope is its negative reciprocal, negative one half.", None, "m = −1/2"),
        ("Use point-slope form: y − 2 = −1/2 (x − 6).", "Use point slope form. y minus 2 equals negative one half times x minus 6.",
         None, "y − 2 = −1/2 (x − 6)"),
        ("Simplify: y − 2 = −1/2 x + 3, so y = −1/2 x + 5.",
         "Simplify. y minus 2 equals negative one half x, plus 3. So y equals negative one half x, plus 5.", dict(rot=90), "y = −1/2 x + 5"),
        ("Check: the red line goes through (6, 2) and crosses the blue line at a right angle.",
         "Check. The red line goes through 6 comma 2, and crosses the blue line at a right angle.", None, None),
    ]),
    dict(kind="list", title="Summary", steps=[
        ("Parallel lines have the same slope.", None, None, "Parallel lines\nsame slope"),
        ("Perpendicular lines have negative reciprocal slopes: flip the fraction and change the sign. Their product is −1.",
         "Perpendicular lines have negative reciprocal slopes. Flip the fraction and change the sign. Their product is negative 1.",
         None, "Perpendicular lines\nnegative reciprocal slopes: flip the fraction, change the sign\nthe product of the slopes is −1"),
        ("A horizontal line y = c has slope 0. A vertical line x = c has an undefined slope. They are always perpendicular.",
         "A horizontal line, y equals c, has slope 0. A vertical line, x equals c, has an undefined slope. They are always perpendicular.",
         None, "Horizontal and vertical\ny = c: slope 0;  x = c: slope undefined\nalways perpendicular to each other"),
    ]),
    dict(title="Your turn", f=(0.75, 0, "slope 3/4"), fpos=(9.6, 5.6), pts=[-4, 4], label=True, steps=[
        ("Line j has slope 3/4. What is the slope of a line perpendicular to j?",
         "Line j has slope 3 fourths. What is the slope of a line perpendicular to j?", None, "j: slope 3/4"),
        ("Pause the video and try it.  PAUSE 5", "Pause the video and try it.", None, None),
        ("−4/3. Flip 3/4 to 4/3 and change the sign.", "Negative 4 thirds. Flip 3 fourths to 4 thirds, and change the sign.",
         dict(rot=90), "perpendicular slope −4/3"),
        ("Check: 3/4 times −4/3 is −1.", "Check. 3 fourths times negative 4 thirds is negative 1.", None, "3/4 · (−4/3) = −1"),
        ("Now try Things Aren't Always What They Seem on page 314 of your book.", None, None, None),
    ]),
]

SCENES_4 = [
    dict(kind="title", title="Comparing Linear Functions", sub="in different forms  ·  Module 2 · Topic 2 · Lesson 4",
         steps=[("A linear function can be an equation, a table, a graph, or a description. Today we compare them.", None, None, None)]),
    dict(kind="list", title="Find two things in every form", steps=[
        ("To compare, find the rate of change, which is the slope, and the initial value, which is the y-intercept.", None, None,
         "Rate of change (slope) and initial value (y-intercept)"),
        ("In an equation y = mx + b, the rate is m and the initial value is b.",
         "In an equation, y equals m x plus b, the rate is m and the initial value is b.", None, "Equation y = mx + b\nrate m; start b"),
        ("In a table, the rate is the change in y divided by the change in x. The initial value is y when x is 0.", None, None,
         "Table\nrate = change in y ÷ change in x; start = y when x = 0"),
        ("On a graph, the rate is rise over run. The initial value is where the line crosses the y-axis.", None, None,
         "Graph\nrate = rise ÷ run; start = where it crosses the y-axis"),
        ("In a description, words like each or per give the rate. The starting amount is the initial value.", None, None,
         "Description\n“each” or “per” = rate; the starting amount = start"),
    ]),
    dict(title="Table vs. graph", f=(0.5, 6, "B (graph)"), fpos=(-1, 8.8), marks=[(0, 3, "(0, 3)"), (1, 5, "(1, 5)"), (3, 9, "(3, 9)", "l")], steps=[
        ("Function A is a table. Function B is the blue graph. Which grows faster, and which starts higher?", None, None,
         "A (table): x 0, 1, 3 → y 3, 5, 9"),
        ("Table: from (0, 3) to (1, 5), y goes up 2 when x goes up 1. A's rate is 2, and it starts at 3.",
         "In the table, from 0 comma 3 to 1 comma 5, y goes up 2 when x goes up 1. A's rate is 2, and it starts at 3.",
         dict(m=2, c=3), "A: rate 2, starts at 3"),
        ("Graph: B rises 1 for every 2 to the right, so its rate is 1/2. It crosses the y-axis at 6.",
         "On the graph, B rises 1 for every 2 to the right, so its rate is one half. It crosses the y-axis at 6.", None,
         "B: rate 1/2, starts at 6"),
        ("A grows faster, because 2 is greater than 1/2. B starts higher, because 6 is greater than 3.",
         "A grows faster, because 2 is greater than one half. B starts higher, because 6 is greater than 3.", None,
         "A grows faster; B starts higher"),
    ]),
    dict(title="Equation vs. table", f=(3, -2, "A: y = 3x − 2"), fpos=(9.6, 7.6), marks=[(1, 4, "(1, 4)", "l"), (2, 6, "(2, 6)", "l"), (4, 10, None)], steps=[
        ("Function A is the equation y = 3x − 2. Its rate is 3, and it starts at −2.",
         "Function A is the equation y equals 3 x minus 2. Its rate is 3, and it starts at negative 2.", None, "A: rate 3, starts at −2"),
        ("Function B is a table: x is 1, 2, 4 and y is 4, 6, 10.", None, None, "B (table): x 1, 2, 4 → y 4, 6, 10"),
        ("When x goes up 1, y goes up 2, so B's rate is 2. One step back from (1, 4), at x = 0, y is 2.",
         "When x goes up 1, y goes up 2, so B's rate is 2. One step back from 1 comma 4, at x equals 0, y is 2.",
         dict(m=2, c=2), "B: rate 2, starts at 2"),
        ("A is steeper, so it grows faster. B starts higher. They meet at (4, 10).",
         "A is steeper, so it grows faster. B starts higher. They meet at 4 comma 10.", None, "A grows faster; B starts higher"),
    ]),
    dict(title="Description vs. graph", f=(1, 4, "B (graph)"), fpos=(-1.5, 5), steps=[
        ("Plant A is 2 cm tall and grows 1.5 cm each week. Each gives the rate, and 2 cm is the start.",
         "Plant A is 2 centimeters tall, and grows 1.5 centimeters each week. The word each gives the rate, and 2 centimeters is the start.",
         None, "A: rate 1.5 cm per week, starts at 2 cm"),
        ("So Plant A is y = 1.5x + 2, where x is the number of weeks.", "So plant A is y equals 1.5 x plus 2, where x is the number of weeks.",
         dict(m=1.5, c=2), "A: y = 1.5x + 2"),
        ("Plant B is the blue graph. It starts at 4 cm and grows 1 cm each week.",
         "Plant B is the blue graph. It starts at 4 centimeters and grows 1 centimeter each week.", None, "B: rate 1 cm per week, starts at 4 cm"),
        ("A grows faster, but B starts taller. They are the same height, 8 cm, at week 4.",
         "A grows faster, but B starts taller. They are the same height, 8 centimeters, at week 4.", None, "same height at week 4"),
    ]),
    dict(title="Parallel, perpendicular, or neither?", f=(4, -3, "y = 4x − 3"), fpos=(9.6, 6.6),
         marks=[(-4, 3, None), (0, 2, None), (2, 1.5, None), (8, 0, None)], steps=[
        ("Is the line through this table parallel, perpendicular, or neither to y = 4x − 3?",
         "Is the line through this table parallel, perpendicular, or neither, to y equals 4 x minus 3?", None, "x −4, 0, 2, 8 → y 3, 2, 1.5, 0"),
        ("From (−4, 3) to (0, 2), y goes down 1 while x goes up 4. The slope is −1/4.",
         "From negative 4 comma 3, to 0 comma 2, y goes down 1 while x goes up 4. The slope is negative one fourth.",
         dict(m=-0.25, c=2), "table slope −1/4"),
        ("4 times −1/4 is −1. The slopes are negative reciprocals, so the lines are perpendicular.",
         "4 times negative one fourth is negative 1. The slopes are negative reciprocals, so the lines are perpendicular.", None,
         "4 · (−1/4) = −1: perpendicular"),
    ]),
    dict(kind="list", title="Comparing", steps=[
        ("The greater rate of change grows faster, and its graph is steeper.", None, None, "Greater rate of change\ngrows faster; steeper graph"),
        ("The greater initial value starts higher.", None, None, "Greater initial value\nstarts higher"),
        ("Same slope means parallel. Slopes that multiply to −1 mean perpendicular.",
         "Same slope means parallel. Slopes that multiply to negative 1 mean perpendicular.", None,
         "Parallel or perpendicular\nsame slope: parallel; product −1: perpendicular"),
    ]),
    dict(title="Your turn", f=(5, 1, "A: y = 5x + 1"), fpos=(9.6, 8), marks=[(0, -3, "(0, −3)"), (1, 3, "(1, 3)"), (2, 9, "(2, 9)")], steps=[
        ("A: y = 5x + 1. B: a table with x 0, 1, 2 and y −3, 3, 9. Which has the greater rate? Which starts higher?",
         "A is y equals 5 x plus 1. B is a table, with x equal to 0, 1, 2, and y equal to negative 3, 3, 9. Which has the greater rate of change? Which starts higher?",
         None, "B (table): x 0, 1, 2 → y −3, 3, 9"),
        ("Pause the video and try it.  PAUSE 5", "Pause the video and try it.", None, None),
        ("B goes up 6 each time x goes up 1, so B's rate is 6. That is greater than 5.", None, dict(m=6, c=-3), "B: rate 6 > 5"),
        ("A starts higher, because 1 is greater than −3.", "A starts higher, because 1 is greater than negative 3.", None, "A starts higher: 1 > −3"),
        ("Now try Function Maker Space on page 325 of your book.", None, None, None),
    ]),
]
LESSONS = {1: ("T2-Lesson1-Transformations.mp4", SCENES_1), 2: ("T2-Lesson2-Horizontal-Transformations.mp4", SCENES_2),
           3: ("T2-Lesson3-Perpendicular-Lines.mp4", SCENES_3), 4: ("T2-Lesson4-Comparing-Functions.mp4", SCENES_4)}


def spoken(cap):
    s = re.sub(r"\s*PAUSE \d+", "", cap)
    for a, b in [("f(x)", "f of x"), ("g(x)", "g of x"), ("h(x)", "h of x"), ("k(x)", "k of x"), ("j(x)", "j of x"),
                 ("r(x)", "r of x"), (" · ", " times "), ("−", "minus ")]:
        s = s.replace(a, b)
    return s


def speak(text, path):  # Microsoft neural voice (the Edge Read Aloud voices); returns seconds
    asyncio.run(edge_tts.Communicate(text, VOICE, rate=RATE).save(path))
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                       capture_output=True, text=True, check=True)
    return float(r.stdout)


def wrap(d, text, font, width):
    lines, cur = [], ""
    for word in text.split():
        t = (cur + " " + word).strip()
        if d.textlength(t, font=font) > width and cur:
            lines.append(cur); cur = word
        else:
            cur = t
    return lines + [cur] if cur else lines


def ease(t): t = max(0.0, min(1.0, t)); return t * t * (3 - 2 * t)


def grid():
    im = Image.new("RGB", (W, H), "white"); d = ImageDraw.Draw(im)
    for i in range(-R, R + 1):
        x0, y0 = px(i, -R); x1, y1 = px(i, R)
        d.line([x0, y0, x1, y1], fill=AX if i == 0 else GRID, width=3 if i == 0 else 1)
        x0, y0 = px(-R, i); x1, y1 = px(R, i)
        d.line([x0, y0, x1, y1], fill=AX if i == 0 else GRID, width=3 if i == 0 else 1)
    for i in range(-R + 2, R, 2):
        if i:
            x, y = px(i, 0); d.text((x, y + 4), str(i).replace("-", "−"), fill=MUTED, font=F[18], anchor="mt")
            x, y = px(0, i); d.text((x - 6, y), str(i).replace("-", "−"), fill=MUTED, font=F[18], anchor="rm")
    d.text(px(R, 0), " x", fill=AX, font=F[26], anchor="lb"); d.text(px(0, R), "  y", fill=AX, font=F[26], anchor="lt")
    return im


def clip_line(d, a, b, color, width):  # y = a x + b clipped to the square
    pts = []
    for x in (-R, R):
        y = a * x + b
        if -R <= y <= R: pts.append((x, y))
    if a:
        for y in (-R, R):
            x = (y - b) / a
            if -R < x < R: pts.append((x, y))
    if len(pts) >= 2:
        pts.sort(); d.line([*px(*pts[0]), *px(*pts[-1])], fill=color, width=width)


def fmt(v):
    v = round(v, 2)
    if abs(v - round(v)) < 1e-6: v = int(round(v))
    return str(v).replace("-", "−")



START = dict(a=1, ib=1, h=0, d=0, rot=0, m=None, c=None)


def mover(sc, T):  # where a parent point goes: a · f(b(x − h)) + d, then turned rot° about the scene's center
    cx, cy = sc.get("center", (0, 0))
    co, si = math.cos(math.radians(T["rot"])), math.sin(math.radians(T["rot"]))
    def go(x, y):
        x, y = x * T["ib"] + T["h"], T["a"] * y + T["d"]
        return cx + (x - cx) * co - (y - cy) * si, cy + (x - cx) * si + (y - cy) * co
    return go


def red_line(sc, T):  # the red line as two points on it
    if T["m"] is not None:
        return (0, T["c"]), (1, T["m"] + T["c"])
    p, q, _ = sc.get("f", (1, 0, ""))
    go = mover(sc, T)
    return go(-30, -30 * p + q), go(30, 30 * p + q)


def clip_seg(d, P, Q, color, width):  # the whole line through P and Q, clipped to the square (works for vertical lines)
    (x0, y0), (x1, y1) = P, Q
    vx, vy, ts = x1 - x0, y1 - y0, []
    for k in (-R, R):
        if abs(vx) > 1e-9:
            t = (k - x0) / vx
            if -R - 1e-6 <= y0 + t * vy <= R + 1e-6: ts.append(t)
        if abs(vy) > 1e-9:
            t = (k - y0) / vy
            if -R - 1e-6 <= x0 + t * vx <= R + 1e-6: ts.append(t)
    if len(ts) >= 2:
        a, b = min(ts), max(ts)
        d.line([*px(x0 + a * vx, y0 + a * vy), *px(x0 + b * vx, y0 + b * vy)], fill=color, width=width)


def frame(base, sc, T, ghost, show_g, panel, cap):
    im = base.copy(); d = ImageDraw.Draw(im)
    p, q, flabel = sc.get("f", (1, 0, "f(x) = x"))
    if sc.get("kind") in ("title", "list"):
        d.rectangle([0, 0, W, H - 100], fill="white")
    if sc.get("kind") == "title":
        d.text((W / 2, 250), sc["title"], fill=INK, font=FB[60], anchor="mm")
        d.text((W / 2, 330), sc["sub"], fill=BLUE, font=FB[34], anchor="mm")
    elif sc.get("kind") == "list":
        d.text((80, 50), sc["title"], fill=INK, font=FB[44])
        y = 140
        for t in panel:  # first line bold, the rest indented
            for j, part in enumerate(t.split("\n")):
                for ln in wrap(d, part, FB[34] if j == 0 else F[34], W - 220):
                    d.text((80 if j == 0 else 120, y), ln, fill=BLUE if j == 0 else INK, font=FB[34] if j == 0 else F[34]); y += 44
            y += 22
    else:
        if ghost: clip_seg(d, *ghost, "#9ca3af", 4)
        clip_line(d, p, q, BLUE, 5)
        d.text(px(*sc.get("fpos", (7.2, 8.6))), flabel, fill=BLUE, font=FB[26], anchor="rm")
        for x in sc.get("pts", []):
            xp, yp = px(x, p * x + q); d.ellipse([xp - 7, yp - 7, xp + 7, yp + 7], fill=BLUE)
        for x, y, lab, *side in sc.get("marks", []):  # fixed points, such as table values; label below right, "l" left, "tr" above right
            xp, yp = px(x, y); d.ellipse([xp - 7, yp - 7, xp + 7, yp + 7], fill=INK)
            at = {"l": ((xp - 12, yp), "rm"), "tr": ((xp + 12, yp - 8), "lb")}.get(side[0] if side else "", ((xp + 12, yp + 4), "lt"))
            if lab:
                d.rectangle(d.textbbox(at[0], lab, font=F[26], anchor=at[1]), fill="white")  # stays readable over grid numbers
                d.text(at[0], lab, fill=INK, font=F[26], anchor=at[1])
        if show_g:
            clip_seg(d, *red_line(sc, T), RED, 5)
            go = mover(sc, T)
            for x in (sc.get("pts", []) if T["m"] is None else []):
                x2, y2 = go(x, p * x + q)
                if not (-R <= x2 <= R and -R <= y2 <= R): continue
                x0, y0 = px(x, p * x + q); x1, y1 = px(x2, y2)
                if abs(x1 - x0) + abs(y1 - y0) > 4: d.line([x0, y0, x1, y1], fill=RED, width=2)
                d.ellipse([x1 - 7, y1 - 7, x1 + 7, y1 + 7], fill=RED)
                if sc.get("label"): d.text((x1 + 12, y1 - 10), f"({fmt(x2)}, {fmt(y2)})", fill=RED, font=F[26], anchor="lb")
        d.text((680, 40), sc["title"], fill=INK, font=FB[44])
        y = 110
        for i, t in enumerate(panel):
            col = RED if i == len(panel) - 1 and show_g else INK
            for ln in wrap(d, t, FB[34] if i == 0 else F[34], 560):
                d.text((680, y), ln, fill=col if i else BLUE, font=FB[34] if i == 0 else F[34]); y += 44
            y += 14
    d.rectangle([0, H - 100, W, H], fill="#111827")
    lines = wrap(d, re.sub(r"\s*PAUSE \d+", "", cap), F[30], W - 80)
    for i, ln in enumerate(lines[:2]):
        d.text((W / 2, H - 50 + (i - (len(lines[:2]) - 1) / 2) * 36), ln, fill="white", font=F[30], anchor="mm")
    return im


def render(name, scenes):
    out = os.path.join(VIDEOS, name)
    os.makedirs(VIDEOS, exist_ok=True)
    tmp = tempfile.mkdtemp()
    base = grid()
    wavs, n = [], 0
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "26",
                           os.path.join(tmp, "v.mp4")], stdin=subprocess.PIPE)
    for sc in scenes:
        p, q, _ = sc.get("f", (1, 0, ""))
        T, ghost, panel = dict(START), None, []
        show_g = False  # g appears on the step that first moves it, so it never hides f
        for cap, say, move, pline in sc["steps"]:
            wav = os.path.join(tmp, f"s{n:03d}.mp3"); n += 1
            dur = speak(say or spoken(cap), wav) + 0.6
            m = re.search(r"PAUSE (\d+)", cap)
            hold = float(m.group(1)) if m else 0.0
            nf = round((dur + hold) * FPS)  # audio slot = whole frames, so sound and picture never drift
            wavs.append((wav, nf / FPS))
            if pline: panel.append(pline)
            if isinstance(move, tuple): move = dict(a=move[0], d=move[1])
            move = dict(move or {})
            if move.pop("reset", False):
                ghost = red_line(sc, T) if show_g else None
                T = dict(START)
            if "b" in move: move["ib"] = 1 / move.pop("b")  # animate 1/b so points slide at an even speed
            if "m" in move and T["m"] is None: T["m"], T["c"] = p, q  # a set line grows out of f
            T0, goal = dict(T), dict(T, **move)
            if move: show_g = True
            for f in range(nf):
                if move:
                    k = ease(f / FPS / min(2.0, dur))
                    T = {key: None if goal[key] is None else T0[key] + (goal[key] - T0[key]) * k for key in T0}
                ff.stdin.write(frame(base, sc, T, ghost, show_g, panel, cap).tobytes())
            T = goal
    ff.stdin.close(); ff.wait()
    # audio: each clip padded with silence to its slot length, then joined
    lst = os.path.join(tmp, "a.txt")
    with open(lst, "w") as fh:
        for i, (wav, slot) in enumerate(wavs):
            padded = os.path.join(tmp, f"p{i:03d}.wav")
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-af", f"apad=whole_dur={slot:.3f}",
                            "-ar", "22050", "-ac", "1", padded], check=True)
            fh.write(f"file '{padded}'\n")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(tmp, "v.mp4"), "-f", "concat", "-safe", "0",
                    "-i", lst, "-c:v", "copy", "-c:a", "aac", "-b:a", "96k", "-shortest", "-movflags", "+faststart", out],
                   check=True)
    print("wrote", out, f"{sum(s for _, s in wavs):.0f} s")


if __name__ == "__main__":
    for arg in sys.argv[1:] or LESSONS:
        render(*LESSONS[int(arg)])

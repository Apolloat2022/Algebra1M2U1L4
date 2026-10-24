# End of Topic 2 Assessment (original items: the publisher's Assessments book has no Topic 2 test; items cover the
# TE Assessment Summary TEKS A.2A, A.2C, A.2E, A.2F, A.2G, A.3C, A.3E across Lessons 1-4).
# Writes General, Section 504 (same items + access supports) and IEP (modified) decks plus an answer key for each,
# as make_pptx.py HTML, converts them, then removes the HTML.  Run: python make_t2_assessment.py [--keep]
import subprocess, sys
from make_assessment_accom import ROOT, g, vtbl, ch, tip, work, B

N = 14
TEST, SUB = "Topic 2 Assessment", "End of Topic Assessment"  # titles; make_t2_retake.py swaps them
F = lambda a, b: "{{" + f"{a}|{b}" + "}}"  # stacked fraction for make_pptx.py
fx = lambda s: f"<i>{s}</i>"
x, y = fx("x"), fx("y")


def deck(label, foot, directions, ref, qs, notes):
    def slide(body, n=None, aside=""):
        head = f'<h3>Question {n} of {N}</h3>' if n else ""
        return (f'<section class="slide">{head}<div style="font-size:30px">{body}</div><p class="foot">{foot}</p>'
                + (f'<aside class="notes">{aside}</aside>' if aside else "") + "</section>")
    out = [slide(f'<h1>Topic 2: Transforming and Comparing Linear Functions</h1><h3>{SUB} · {label}</h3>'
                 f'<p>Name {B}{B}{B} &nbsp; Date {B}{B}</p><div class="card">{directions}</div>', aside=notes)]
    out += [slide(ref)] if ref else []
    out += [slide(b, n) for n, b in enumerate(qs, 1)]
    out.append(slide('<h2>You are done!</h2><p>Go back and check each answer.</p>'
                     '<p>Did you answer <b>every</b> question?</p><p>Did you include <b>units</b> and <b>explanations</b> where asked?</p>'
                     '<p>Raise your hand when you are finished.</p>'))
    return f'<!doctype html><meta charset="utf-8"><title>{TEST} · {label}</title><body>' + "".join(out) + "</body>"


card = lambda t: f'<div class="card"><p style="font-size:21px">{t}</p></div>'
REF = ('<h2>Reference Sheet</h2><div class="grid3" style="gap:14px">'
       + card(f"<b>Vertical changes</b><br>{y} = <i>a</i>·<i>f</i>({x}) + <i>d</i><br>|<i>a</i>| &gt; 1 stretch, 0 &lt; |<i>a</i>| &lt; 1 compress<br><i>a</i> &lt; 0 reflect across the {x}-axis<br><i>d</i> &gt; 0 up, <i>d</i> &lt; 0 down")
       + card(f"<b>Horizontal changes</b><br>{y} = <i>f</i>({x} − <i>c</i>)<br><i>f</i>({x} − 3): right 3<br><i>f</i>({x} + 3): left 3")
       + card(f"<b>Slope</b><br><i>m</i> = {F('y₂ − y₁', 'x₂ − x₁')}")
       + card(f"<b>Parallel lines</b><br>same slope<br><b>Perpendicular lines</b><br>slopes are negative reciprocals: 2 and −{F(1, 2)}")
       + card(f"<b>Slope-intercept form</b><br>{y} = <i>mx</i> + <i>b</i><br><b>Point-slope form</b><br>{y} − <i>y</i>₁ = <i>m</i>({x} − <i>x</i>₁)")
       + card(f"<b>Standard form</b><br><i>Ax</i> + <i>By</i> = <i>C</i><br>Solve for {y} to find the slope.")
       + card("<b>Rate of change</b> = slope<br><b>Initial value</b> = <i>y</i>-intercept")
       + card(f"<b>Domain</b> = the {x}-values (inputs)<br><b>Range</b> = the {y}-values (outputs)")
       + card("<b>Compare functions</b><br>Set the two expressions equal to find where they meet.") + "</div>")


def g4(mark):
    return ("<div>" + g(440, 400, [-6, 6], [-6, 6], [1, 2], [1, 2],
                        [dict(p=[[0, 0], [1, 1]], dash=True, label="f(x)"), dict(p=[[0, -3], [1, -2]], c="a", label="g(x)")],
                        [[0, -3, "(0, −3)"]] if mark else [[0, -3, ""]]) + "</div>")


def g13(mark):
    return ("<div>" + g(440, 380, [-2, 6], [-3, 4], [1, 1], [1, 1], [dict(p=[[0, -1], [3, 1]], c="a")],
                        [[0, -1, "(0, −1)" if mark else ""], [3, 1, "(3, 1)" if mark else ""]])
            + '<p class="small muted">Function <i>p</i></p></div>')


GYM = vtbl(["Months", "Gym A Cost ($)"], [[0, 50], [1, 75], [2, 100], [3, 125], [4, 150]], 24)
GYMTXT = (f'<p>Gym A\'s total cost is shown in the table. Gym B\'s total cost is <i>c</i> = 35<i>m</i> + 20, '
          'where <i>m</i> is the number of months.</p>')
row = lambda a, b: f'<div class="row" style="gap:40px">{a}<div>{b}</div></div>'

# ---------------------------------------------------------------- General / Section 504: the same 14 items
STD = [
 f'<p>The graph of <i>f</i>({x}) = {x} is transformed to make <i>g</i>({x}) = {x} − 4.</p><p>Which describes the <b>transformation</b>?</p>'
 + ch("ABCD", "A translation up 4 units", "A translation left 4 units", "A translation down 4 units", "A vertical dilation by a factor of −4"),
 f'<p>Which function is a <b>reflection</b> of <i>f</i>({x}) = {x} across the {x}-axis <b>and</b> a <b>vertical dilation</b> by a factor of 3?</p>'
 + ch("FGHJ", f"<i>g</i>({x}) = 3{x}", f"<i>g</i>({x}) = −(1/3){x}", f"<i>g</i>({x}) = {x} − 3", f"<i>g</i>({x}) = −3{x}"),
 f'<p>Let <i>f</i>({x}) = {x} and <i>g</i>({x}) = 2<i>f</i>({x}) + 5.</p><p>Write <i>g</i>({x}) in <b>slope-intercept form</b>. '
 f'Then describe the <b>two transformations</b> of <i>f</i>({x}) that produce <i>g</i>({x}).</p>' + work,
 row(g4(False), f'<p>The graph shows <i>f</i>({x}) = {x} (dashed) and a transformed function <i>g</i>({x}).</p><p>Which equation represents <i>g</i>({x})?</p>'
     + ch("ABCD", f"<i>g</i>({x}) = <i>f</i>({x}) + 3", f"<i>g</i>({x}) = <i>f</i>({x}) − 3", f"<i>g</i>({x}) = <i>f</i>({x} + 3)", f"<i>g</i>({x}) = −3<i>f</i>({x})")),
 f'<p>Let <i>f</i>({x}) = {x} and <i>h</i>({x}) = <i>f</i>({x} + 6).</p><p>Describe the <b>horizontal translation</b>. '
 'Then name the <b>vertical translation</b> that produces the same graph.</p>' + work,
 f'<p>The graph of <i>f</i>({x}) = 2{x} is translated <b>right 3 units</b>.</p><p>Which function represents the new graph?</p>'
 + ch("FGHJ", f"<i>g</i>({x}) = 2{x} + 6", f"<i>g</i>({x}) = 2{x} − 3", f"<i>g</i>({x}) = 2{x} − 6", f"<i>g</i>({x}) = 2{x} + 3"),
 '<p>A line passes through the points (−2, 5) and (4, 1).</p><p>Determine the <b>slope</b> of the line. Then give the slope of a line '
 '<b>parallel</b> to it and the slope of a line <b>perpendicular</b> to it.</p>' + work,
 f'<p>Which equation represents a line <b>perpendicular</b> to {y} = 4{x} − 1 that passes through the point (8, 3)?</p>'
 + ch("ABCD", f"{y} = 4{x} − 29", f"{y} = (1/4){x} + 1", f"{y} = −(1/4){x} + 1", f"{y} = −(1/4){x} + 5"),
 f'<p>Write the equation in <b>slope-intercept form</b> of the line <b>parallel</b> to {y} = −3{x} + 7 that passes through the point (2, −4).</p>' + work,
 f'<p>Which statement describes the lines</p><p class="eq">2{x} + 3{y} = 6 &nbsp; and &nbsp; {y} = (3/2){x} − 4?</p>'
 + ch("FGHJ", "They are parallel.", "They are perpendicular.", "They are neither parallel nor perpendicular.", "They are the same line."),
 row(GYM, GYMTXT + '<p>Which gym has the greater <b>rate of change</b>? Which gym has the greater <b>initial value</b>? '
     'Explain what each means in terms of the problem situation.</p>' + work),
 row(GYM, GYMTXT + '<p>After how many months do the two gyms cost the <b>same</b> total amount? What is that cost? '
     'Which gym costs less for <b>6 months</b>?</p>' + work),
 row(g13(False), f'<p>Which function has a <b>greater rate of change</b> than function <i>p</i> shown in the graph?</p>'
     + ch("ABCD", f"{y} = 0.5{x} + 4", f"2{x} − 3{y} = 6", f"{y} = (3/4){x} − 2", "The line through (0, 1) and (2, 2)")),
 '<p>A tank holds 300 gallons of water. It drains at a constant rate of 15 gallons per minute. The function '
 '<i>w</i>(<i>t</i>) = 300 − 15<i>t</i> gives the gallons left after <i>t</i> minutes.</p><p>What is the <b>range</b> of the function for this situation?</p>'
 + ch("FGHJ", "0 ≤ <i>t</i> ≤ 20", "0 ≤ <i>w</i>(<i>t</i>) ≤ 300", "0 ≤ <i>w</i>(<i>t</i>) ≤ 20", "<i>w</i>(<i>t</i>) ≥ 0"),
]

# ---------------------------------------------------------------- IEP: 3 choices, chunked steps, tips, frames
IEP = [
 f'<p>The graph of <i>f</i>({x}) = {x} becomes <i>g</i>({x}) = {x} − 4. What is the <b>transformation</b>?</p>'
 + tip(f"− 4 is outside, so it subtracts 4 from every output ({y}-value).") + ch("ABC", "Up 4 units", "Down 4 units", "Left 4 units"),
 f'<p>Which function <b>reflects</b> <i>f</i>({x}) = {x} across the {x}-axis <b>and</b> stretches it by a factor of 3?</p>'
 + tip("A negative number in front of <i>x</i> reflects the line. A number bigger than 1 makes it steeper.")
 + ch("ABC", f"<i>g</i>({x}) = −3{x}", f"<i>g</i>({x}) = 3{x}", f"<i>g</i>({x}) = {x} − 3"),
 f'<p>Let <i>f</i>({x}) = {x} and <i>g</i>({x}) = 2<i>f</i>({x}) + 5.</p><p>Step 1: Replace <i>f</i>({x}) with {x}: <i>g</i>({x}) = {B}{x} + {B}</p>'
 f'<p>Step 2: The 2 is a vertical <b>dilation / translation</b> (circle one) by a factor of {B}.</p>'
 f'<p>Step 3: The + 5 moves the graph <b>up / down</b> (circle one) {B} units.</p>',
 row(g4(True), f'<p>The dashed line is <i>f</i>({x}) = {x}. Which equation is <i>g</i>({x})?</p>'
     + tip("<i>f</i> crosses the <i>y</i>-axis at 0. <i>g</i> crosses at −3. So <i>g</i> is 3 units down.")
     + ch("ABC", f"<i>g</i>({x}) = <i>f</i>({x}) + 3", f"<i>g</i>({x}) = <i>f</i>({x}) − 3", f"<i>g</i>({x}) = −3<i>f</i>({x})")),
 f'<p>Let <i>f</i>({x}) = {x} and <i>h</i>({x}) = <i>f</i>({x} + 6).</p>' + tip("Inside the parentheses, the graph moves the <b>opposite</b> way of the sign.")
 + f'<p>Step 1: <i>h</i>({x}) = {x} + {B}</p><p>Step 2: The graph moves <b>left / right</b> (circle one) {B} units.</p>'
 f'<p>Step 3: For <i>f</i>({x}) = {x}, that is the same graph as moving <b>up / down</b> (circle one) {B} units.</p>',
 f'<p>The graph of <i>f</i>({x}) = 2{x} moves <b>right 3 units</b>. Which function is the new graph?</p>'
 + tip(f"Right 3 means replace {x} with ({x} − 3): <i>g</i>({x}) = 2({x} − 3). Then distribute the 2.")
 + ch("ABC", f"<i>g</i>({x}) = 2{x} − 3", f"<i>g</i>({x}) = 2{x} − 6", f"<i>g</i>({x}) = 2{x} + 6"),
 '<p>A line passes through (−2, 5) and (4, 1).</p>'
 + f'<p>Step 1: Slope <i>m</i> = {F("1 − 5", "4 − (−2)")} = {F(B, B)} = {B}</p><p>Step 2: <b>Parallel</b> slope (the same): {B}</p>'
 f'<p>Step 3: <b>Perpendicular</b> slope (flip the fraction and change the sign): {B}</p>',
 f'<p>Which line is <b>perpendicular</b> to {y} = 4{x} − 1 and passes through (8, 3)?</p>'
 + tip(f"Perpendicular slope: flip 4 = {F(4, 1)} and change the sign → −{F(1, 4)}. Then check: put in {x} = 8. Do you get {y} = 3?")
 + ch("ABC", f"{y} = 4{x} − 29", f"{y} = −(1/4){x} + 1", f"{y} = −(1/4){x} + 5"),
 f'<p>Write the equation of the line <b>parallel</b> to {y} = −3{x} + 7 through the point (2, −4).</p>'
 + f'<p>Step 1: Parallel slope <i>m</i> = {B}</p><p>Step 2: Point-slope form: {y} − (−4) = {B}({x} − 2)</p>'
 f'<p>Step 3: Distribute, then subtract 4: {y} = {B}{x} + {B}</p>',
 f'<p>Are these lines parallel, perpendicular, or neither?</p><p class="eq">2{x} + 3{y} = 6 &nbsp; and &nbsp; {y} = (3/2){x} − 4</p>'
 + tip(f"Solve 2{x} + 3{y} = 6 for {y}: {y} = −(2/3){x} + 2. Compare −{F(2, 3)} with {F(3, 2)}.")
 + ch("ABC", "Parallel", "Perpendicular", "Neither"),
 row(GYM, GYMTXT + f'<p>Gym A: starts at ${B}, goes up ${B} each month.</p><p>Gym B: starts at ${B}, goes up ${B} each month.</p>'
     f'<p>Greater <b>rate of change</b>: Gym {B}. &nbsp; Greater <b>initial value</b>: Gym {B}.</p>'),
 row(GYM, GYMTXT + f'<p>When do they cost the same? Solve 50 + 25<i>m</i> = 20 + 35<i>m</i>.</p>'
     f'<p>Step 1: Subtract 20 and 25<i>m</i>: {B} = {B}<i>m</i>, so <i>m</i> = {B} months. Cost: ${B}</p>'
     f'<p>Step 2: For 6 months: Gym A = ${B}, Gym B = ${B}. Gym {B} costs less.</p>'),
 row(g13(True), f'<p>Function <i>p</i> has a slope of {F(2, 3)} ≈ 0.67. Which function has a <b>greater</b> rate of change?</p>'
     + tip("Find each slope and compare decimals: which is bigger than 0.67?")
     + ch("ABC", f"{y} = 0.5{x} + 4", f"2{x} − 3{y} = 6", f"{y} = (3/4){x} − 2")),
 '<p>A 300-gallon tank drains 15 gallons each minute: <i>w</i>(<i>t</i>) = 300 − 15<i>t</i>.</p><p>What is the <b>range</b>?</p>'
 + tip("Range = the outputs, <i>w</i>(<i>t</i>) gallons. The most water is 300. The least is 0.")
 + ch("ABC", "0 ≤ <i>t</i> ≤ 20", "0 ≤ <i>w</i>(<i>t</i>) ≤ 300", "<i>w</i>(<i>t</i>) ≥ 0"),
]

DIRS = ('<p><b>Directions:</b> Read each question carefully. You may use a calculator. For multiple choice, choose <b>one</b> answer. '
        'For the other questions, show your work and explain your thinking.</p>')
DIR504 = ('<p><b>Directions:</b> Read each question carefully. You may use a calculator and the reference sheet. '
          'For multiple choice, choose <b>one</b> answer. For the other questions, show your work and include units.</p>'
          '<p>One question is on each slide. Take your time. Ask your teacher if you need a break or a question read aloud.</p>')
DIRIEP = ('<p><b>Directions:</b> Read each question carefully. You may use a calculator and the reference sheet. '
          'For multiple choice, choose <b>one</b> answer. Use the steps and tips. Fill in each blank.</p>'
          '<p>One question is on each slide. Take your time. Ask your teacher if you need a break or a question read aloud.</p>')
NGEN = ("End of Topic 2 Assessment, Day 10 (Tue Nov 3, the district test date); review Nov 2, retakes Nov 4. Original items: the publisher's Assessments book has no "
        "Topic 2 test, so these 14 items cover the TE Assessment Summary TEKS (A.2A, A.2C, A.2E, A.2F, A.2G, A.3C, A.3E): "
        "Q1-4 Lesson 1, Q5-6 Lesson 2, Q7-10 Lesson 3, Q11-14 Lesson 4.")
N504 = ("Section 504 version: the same 14 items, wording and answer choices as the general test, so it is graded with the same key. "
        "Only access changes: one question per slide, larger font, key words in bold, a reference sheet and work space. Apply the student's "
        "plan: extended time, breaks, read-aloud, small-group or separate setting, preferential seating.")
NIEP = ("IEP version: same 14 skills, modified. Multiple choice has 3 choices; written items are chunked into steps with blanks and "
        "circle-one frames; tips define vocabulary; key points are labeled on the graphs. Grade with the IEP answer key. "
        "Apply the student's IEP accommodations as well: extended time, breaks, read-aloud, small-group setting.")

# ---------------------------------------------------------------- answer keys
PTS = [1, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 2, 1, 1]  # 1 per multiple choice, 2 per written item
WORK = [
 "x − 4 subtracts 4 from every output. (It is also right 4, which is not a choice.)",
 "a = −3: negative reflects across the x-axis, |−3| = 3 stretches.",
 "g(x) = 2x + 5. 1 pt equation, 1 pt both transformations.",
 "g crosses the y-axis at −3, parallel to f: 3 units down.",
 "h(x) = x + 6. 1 pt left 6, 1 pt up 6.",
 "g(x) = 2(x − 3) = 2x − 6.",
 "(1 − 5) ÷ (4 − (−2)) = −4/6. 1 pt slope, 1 pt parallel and perpendicular.",
 "Perpendicular slope −1/4. 3 = (−1/4)(8) + b → b = 5. (A is parallel; the others miss (8, 3).)",
 "y + 4 = −3(x − 2) → y = −3x + 6 − 4. 1 pt slope, 1 pt equation.",
 "2x + 3y = 6 → y = (−2/3)x + 2. (−2/3)(3/2) = −1.",
 "Gym A: $25/month, starts $50. Gym B: $35/month, starts $20 (joining fee). 1 pt each comparison with meaning.",
 "50 + 25m = 20 + 35m → 30 = 10m. 6 months: A = 50 + 150 = $200, B = 20 + 210 = $230. 1 pt meet, 1 pt 6 months.",
 "p: slope 2/3 ≈ 0.67. 3/4 = 0.75 is greater; 2x − 3y = 6 has slope 2/3 (equal); 0.5 is less.",
 "Outputs: 300 gallons at t = 0 down to 0 gallons at t = 20."]
WRITTEN = {3: "g(x) = 2x + 5; vertical dilation by a factor of 2, translation up 5", 5: "Left 6 units; same as up 6 units (h(x) = x + 6)",
           7: "m = −2/3; parallel −2/3; perpendicular 3/2", 9: "y = −3x + 2",
           11: "Gym B has the greater rate ($35 vs $25 per month); Gym A has the greater initial value ($50 vs $20)",
           12: "3 months, $125; Gym A costs less for 6 months ($200 vs $230)"}
MC = {"GEN": {1: "C. down 4", 2: "J. g(x) = −3x", 4: "B. f(x) − 3", 6: "H. 2x − 6", 8: "D. y = (−1/4)x + 5", 10: "G. perpendicular",
              13: "C. y = (3/4)x − 2", 14: "G. 0 ≤ w(t) ≤ 300"},
      "IEP": {1: "B. down 4", 2: "A. g(x) = −3x", 4: "B. f(x) − 3", 6: "B. 2x − 6", 8: "C. y = (−1/4)x + 5", 10: "B. perpendicular",
              13: "C. y = (3/4)x − 2", 14: "B. 0 ≤ w(t) ≤ 300"}}
IEP_FRAMES = {3: "Blanks: 2 · 5 · circle dilation · 2 · circle up · 5", 5: "Blanks: 6 · circle left · 6 · circle up · 6",
              7: "Blanks: −4/6 · −2/3 · −2/3 · 3/2", 9: "Blanks: −3 · −3 · −3 · 2", 11: "Blanks: 50 · 25 · 20 · 35 · B · A",
              12: "Blanks: 30 · 10 · 3 · 125 · 200 · 230 · A"}


def key(kind, label, foot):
    def answer(q):
        a = MC[kind].get(q) or WRITTEN[q]
        return a + (f'<br><span class="muted">{IEP_FRAMES[q]}</span>' if kind == "IEP" and q in IEP_FRAMES else "")
    def slide(body):
        return f'<section class="slide"><div>{body}</div><p class="foot">{foot} · Answer Key (teacher copy)</p></section>'
    grading = ("Section 504 and General use this same key: same items and letters." if kind == "GEN" else
               "IEP Form: 3 choices per multiple-choice item; written answers match the general test.")
    out = [slide(f'<h1>Answer Key</h1><h3>{TEST} · {label}</h3><p>{grading}</p>'
                 f'<p>1 point per multiple-choice item, 2 points per written item. Total: <b>{sum(PTS)} points</b>.</p>'
                 '<p class="warn">Teacher copy. Do not share with students.</p>')]
    for start in (1, 5, 9, 13):
        qs = range(start, min(start + 4, N + 1))
        rows = "".join(f'<tr><td><b>{q}</b> ({PTS[q-1]} pt)</td><td>{answer(q)}</td><td>{WORK[q-1]}</td></tr>' for q in qs)
        out.append(slide(f'<h2>Questions {qs[0]}–{qs[-1]}</h2><table style="font-size:20px"><tr><th>Q</th><th>Answer</th><th>Work / meaning</th></tr>{rows}</table>'))
    quick = " · ".join(f"{q} {MC[kind][q].split('.')[0]}" if q in MC[kind] else f"{q} {WRITTEN[q].split(';')[0]}" for q in range(1, N + 1))
    out.append(slide(f'<h2>Quick key</h2><p>{quick}</p>'))
    return f'<!doctype html><meta charset="utf-8"><title>{TEST} Answer Key · {label}</title><body>' + "".join(out) + "</body>"


if __name__ == "__main__":
    assert len(STD) == len(IEP) == len(PTS) == len(WORK) == N
    assert all(q in MC["GEN"] or q in WRITTEN for q in range(1, N + 1)) and MC["GEN"].keys() == MC["IEP"].keys()
    jobs = [("Module 2 topic 2", "Topic2-Assessment", deck("General", "Topic 2 Assessment", DIRS, "", STD, NGEN)),
            ("Module 2 topic 2", "Topic2-Assessment-ANSWER-KEY", key("GEN", "General and Section 504", "Topic 2 Assessment")),
            ("Section 504", "Topic2-Assessment-504", deck("Section 504 Version", "Topic 2 Assessment · Section 504 Version", DIR504, REF, STD, N504)),
            ("Section 504", "Topic2-Assessment-504-ANSWER-KEY", key("GEN", "Section 504 Version", "Topic 2 Assessment · Section 504 Version")),
            ("IEP", "Topic2-Assessment-IEP", deck("IEP Version", "Topic 2 Assessment · IEP Version", DIRIEP, REF, IEP, NIEP)),
            ("IEP", "Topic2-Assessment-IEP-ANSWER-KEY", key("IEP", "IEP Version", "Topic 2 Assessment · IEP Version"))]
    for folder, name, html in jobs:
        src = ROOT / folder / f"{name}.html"
        src.write_text(html, encoding="utf-8")
        subprocess.run([sys.executable, str(ROOT / "make_pptx.py"), f"{folder}/{name}.html"], cwd=ROOT, check=True)
        if "--keep" not in sys.argv:
            src.unlink()

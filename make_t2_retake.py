# Topic 2 Retake (Wed Nov 4): the End of Topic 2 Assessment with new numbers. Same 14 skills, order, item types,
# A-D / F-J letters and points; General, Section 504 and IEP decks plus an answer key for each, built with the
# assessment's own deck() and key() (make_t2_assessment.py), then converted by make_pptx.py.  Run: python make_t2_retake.py
import subprocess, sys
import make_t2_assessment as A
from make_assessment_accom import ROOT, g, vtbl, ch, tip, work, B

F, x, y, row = A.F, A.x, A.y, A.row


def g4(mark):
    return ("<div>" + g(440, 400, [-6, 6], [-6, 6], [1, 2], [1, 2],
                        [dict(p=[[0, 0], [1, 1]], dash=True, label="f(x)"), dict(p=[[0, 2], [1, 3]], c="a", label="g(x)")],
                        [[0, 2, "(0, 2)" if mark else ""]]) + "</div>")


def g13(mark):
    return ("<div>" + g(440, 380, [-2, 6], [-1, 6], [1, 1], [1, 1], [dict(p=[[0, 2], [4, 5]], c="a")],
                        [[0, 2, "(0, 2)" if mark else ""], [4, 5, "(4, 5)" if mark else ""]])
            + '<p class="small muted">Function <i>p</i></p></div>')


PLAN = vtbl(["Months", "Plan A Cost ($)"], [[0, 30], [1, 45], [2, 60], [3, 75], [4, 90]], 24)
PLANTXT = (f'<p>Plan A\'s total cost is shown in the table. Plan B\'s total cost is <i>c</i> = 20<i>m</i> + 10, '
           'where <i>m</i> is the number of months.</p>')

STD = [
 f'<p>The graph of <i>f</i>({x}) = {x} is transformed to make <i>g</i>({x}) = {x} + 3.</p><p>Which describes the <b>transformation</b>?</p>'
 + ch("ABCD", "A translation down 3 units", "A translation up 3 units", "A translation right 3 units", "A vertical dilation by a factor of 3"),
 f'<p>Which function is a <b>reflection</b> of <i>f</i>({x}) = {x} across the {x}-axis <b>and</b> a <b>vertical dilation</b> by a factor of {F(1, 2)}?</p>'
 + ch("FGHJ", f"<i>g</i>({x}) = (1/2){x}", f"<i>g</i>({x}) = −2{x}", f"<i>g</i>({x}) = −(1/2){x}", f"<i>g</i>({x}) = {x} − (1/2)"),
 f'<p>Let <i>f</i>({x}) = {x} and <i>g</i>({x}) = 3<i>f</i>({x}) − 4.</p><p>Write <i>g</i>({x}) in <b>slope-intercept form</b>. '
 f'Then describe the <b>two transformations</b> of <i>f</i>({x}) that produce <i>g</i>({x}).</p>' + work,
 row(g4(False), f'<p>The graph shows <i>f</i>({x}) = {x} (dashed) and a transformed function <i>g</i>({x}).</p><p>Which equation represents <i>g</i>({x})?</p>'
     + ch("ABCD", f"<i>g</i>({x}) = <i>f</i>({x}) − 2", f"<i>g</i>({x}) = −2<i>f</i>({x})", f"<i>g</i>({x}) = <i>f</i>({x}) + 2", f"<i>g</i>({x}) = <i>f</i>({x} − 2)")),
 f'<p>Let <i>f</i>({x}) = {x} and <i>h</i>({x}) = <i>f</i>({x} − 5).</p><p>Describe the <b>horizontal translation</b>. '
 'Then name the <b>vertical translation</b> that produces the same graph.</p>' + work,
 f'<p>The graph of <i>f</i>({x}) = 3{x} is translated <b>left 2 units</b>.</p><p>Which function represents the new graph?</p>'
 + ch("FGHJ", f"<i>g</i>({x}) = 3{x} + 2", f"<i>g</i>({x}) = 3{x} + 6", f"<i>g</i>({x}) = 3{x} − 6", f"<i>g</i>({x}) = 3{x} − 2"),
 '<p>A line passes through the points (−4, −1) and (2, 3).</p><p>Determine the <b>slope</b> of the line. Then give the slope of a line '
 '<b>parallel</b> to it and the slope of a line <b>perpendicular</b> to it.</p>' + work,
 f'<p>Which equation represents a line <b>perpendicular</b> to {y} = 2{x} + 5 that passes through the point (4, 1)?</p>'
 + ch("ABCD", f"{y} = 2{x} − 7", f"{y} = (1/2){x} − 1", f"{y} = −(1/2){x} + 3", f"{y} = −(1/2){x} + 1"),
 f'<p>Write the equation in <b>slope-intercept form</b> of the line <b>parallel</b> to {y} = 4{x} − 3 that passes through the point (−1, 2).</p>' + work,
 f'<p>Which statement describes the lines</p><p class="eq">4{x} − 2{y} = 6 &nbsp; and &nbsp; {y} = 2{x} + 5?</p>'
 + ch("FGHJ", "They are parallel.", "They are perpendicular.", "They are neither parallel nor perpendicular.", "They are the same line."),
 row(PLAN, PLANTXT + '<p>Which plan has the greater <b>rate of change</b>? Which plan has the greater <b>initial value</b>? '
     'Explain what each means in terms of the problem situation.</p>' + work),
 row(PLAN, PLANTXT + '<p>After how many months do the two plans cost the <b>same</b> total amount? What is that cost? '
     'Which plan costs less for <b>6 months</b>?</p>' + work),
 row(g13(False), f'<p>Which function has a <b>greater rate of change</b> than function <i>p</i> shown in the graph?</p>'
     + ch("ABCD", f"{y} = 0.6{x} + 1", f"3{x} − 4{y} = 8", "The line through (0, 0) and (2, 1)", f"{y} = {x} − 3")),
 '<p>A tank holds 240 gallons of water. It drains at a constant rate of 12 gallons per minute. The function '
 '<i>w</i>(<i>t</i>) = 240 − 12<i>t</i> gives the gallons left after <i>t</i> minutes.</p><p>What is the <b>range</b> of the function for this situation?</p>'
 + ch("FGHJ", "0 ≤ <i>t</i> ≤ 20", "<i>w</i>(<i>t</i>) ≥ 0", "0 ≤ <i>w</i>(<i>t</i>) ≤ 240", "0 ≤ <i>w</i>(<i>t</i>) ≤ 20"),
]

IEP = [
 f'<p>The graph of <i>f</i>({x}) = {x} becomes <i>g</i>({x}) = {x} + 3. What is the <b>transformation</b>?</p>'
 + tip(f"+ 3 is outside, so it adds 3 to every output ({y}-value).") + ch("ABC", "Up 3 units", "Down 3 units", "Right 3 units"),
 f'<p>Which function <b>reflects</b> <i>f</i>({x}) = {x} across the {x}-axis <b>and</b> changes it by a factor of {F(1, 2)}?</p>'
 + tip("A negative number in front of <i>x</i> reflects the line. A number between 0 and 1 makes it less steep.")
 + ch("ABC", f"<i>g</i>({x}) = (1/2){x}", f"<i>g</i>({x}) = −(1/2){x}", f"<i>g</i>({x}) = −2{x}"),
 f'<p>Let <i>f</i>({x}) = {x} and <i>g</i>({x}) = 3<i>f</i>({x}) − 4.</p><p>Step 1: Replace <i>f</i>({x}) with {x}: <i>g</i>({x}) = {B}{x} − {B}</p>'
 f'<p>Step 2: The 3 is a vertical <b>dilation / translation</b> (circle one) by a factor of {B}.</p>'
 f'<p>Step 3: The − 4 moves the graph <b>up / down</b> (circle one) {B} units.</p>',
 row(g4(True), f'<p>The dashed line is <i>f</i>({x}) = {x}. Which equation is <i>g</i>({x})?</p>'
     + tip("<i>f</i> crosses the <i>y</i>-axis at 0. <i>g</i> crosses at 2. So <i>g</i> is 2 units up.")
     + ch("ABC", f"<i>g</i>({x}) = <i>f</i>({x}) − 2", f"<i>g</i>({x}) = <i>f</i>({x}) + 2", f"<i>g</i>({x}) = −2<i>f</i>({x})")),
 f'<p>Let <i>f</i>({x}) = {x} and <i>h</i>({x}) = <i>f</i>({x} − 5).</p>' + tip("Inside the parentheses, the graph moves the <b>opposite</b> way of the sign.")
 + f'<p>Step 1: <i>h</i>({x}) = {x} − {B}</p><p>Step 2: The graph moves <b>left / right</b> (circle one) {B} units.</p>'
 f'<p>Step 3: For <i>f</i>({x}) = {x}, that is the same graph as moving <b>up / down</b> (circle one) {B} units.</p>',
 f'<p>The graph of <i>f</i>({x}) = 3{x} moves <b>left 2 units</b>. Which function is the new graph?</p>'
 + tip(f"Left 2 means replace {x} with ({x} + 2): <i>g</i>({x}) = 3({x} + 2). Then distribute the 3.")
 + ch("ABC", f"<i>g</i>({x}) = 3{x} + 2", f"<i>g</i>({x}) = 3{x} + 6", f"<i>g</i>({x}) = 3{x} − 6"),
 '<p>A line passes through (−4, −1) and (2, 3).</p>'
 + f'<p>Step 1: Slope <i>m</i> = {F("3 − (−1)", "2 − (−4)")} = {F(B, B)} = {B}</p><p>Step 2: <b>Parallel</b> slope (the same): {B}</p>'
 f'<p>Step 3: <b>Perpendicular</b> slope (flip the fraction and change the sign): {B}</p>',
 f'<p>Which line is <b>perpendicular</b> to {y} = 2{x} + 5 and passes through (4, 1)?</p>'
 + tip(f"Perpendicular slope: flip 2 = {F(2, 1)} and change the sign → −{F(1, 2)}. Then check: put in {x} = 4. Do you get {y} = 1?")
 + ch("ABC", f"{y} = 2{x} − 7", f"{y} = −(1/2){x} + 3", f"{y} = −(1/2){x} + 1"),
 f'<p>Write the equation of the line <b>parallel</b> to {y} = 4{x} − 3 through the point (−1, 2).</p>'
 + f'<p>Step 1: Parallel slope <i>m</i> = {B}</p><p>Step 2: Point-slope form: {y} − 2 = {B}({x} − (−1))</p>'
 f'<p>Step 3: Distribute, then add 2: {y} = {B}{x} + {B}</p>',
 f'<p>Are these lines parallel, perpendicular, or neither?</p><p class="eq">4{x} − 2{y} = 6 &nbsp; and &nbsp; {y} = 2{x} + 5</p>'
 + tip(f"Solve 4{x} − 2{y} = 6 for {y}: {y} = 2{x} − 3. Compare the slopes 2 and 2.")
 + ch("ABC", "Parallel", "Perpendicular", "Neither"),
 row(PLAN, PLANTXT + f'<p>Plan A: starts at ${B}, goes up ${B} each month.</p><p>Plan B: starts at ${B}, goes up ${B} each month.</p>'
     f'<p>Greater <b>rate of change</b>: Plan {B}. &nbsp; Greater <b>initial value</b>: Plan {B}.</p>'),
 row(PLAN, PLANTXT + f'<p>When do they cost the same? Solve 30 + 15<i>m</i> = 10 + 20<i>m</i>.</p>'
     f'<p>Step 1: Subtract 10 and 15<i>m</i>: {B} = {B}<i>m</i>, so <i>m</i> = {B} months. Cost: ${B}</p>'
     f'<p>Step 2: For 6 months: Plan A = ${B}, Plan B = ${B}. Plan {B} costs less.</p>'),
 row(g13(True), f'<p>Function <i>p</i> has a slope of {F(3, 4)} = 0.75. Which function has a <b>greater</b> rate of change?</p>'
     + tip("Find each slope and compare decimals: which is bigger than 0.75?")
     + ch("ABC", f"{y} = 0.6{x} + 1", f"3{x} − 4{y} = 8", f"{y} = {x} − 3")),
 '<p>A 240-gallon tank drains 12 gallons each minute: <i>w</i>(<i>t</i>) = 240 − 12<i>t</i>.</p><p>What is the <b>range</b>?</p>'
 + tip("Range = the outputs, <i>w</i>(<i>t</i>) gallons. The most water is 240. The least is 0.")
 + ch("ABC", "0 ≤ <i>t</i> ≤ 20", "0 ≤ <i>w</i>(<i>t</i>) ≤ 240", "<i>w</i>(<i>t</i>) ≥ 0"),
]

WORK = [
 "x + 3 adds 3 to every output. (It is also left 3, which is not a choice; right 3 is wrong.)",
 "a = −1/2: negative reflects across the x-axis, |−1/2| = 1/2 compresses.",
 "g(x) = 3x − 4. 1 pt equation, 1 pt both transformations.",
 "g crosses the y-axis at 2, parallel to f: 2 units up. (f(x − 2) = x − 2 is down 2.)",
 "h(x) = x − 5. 1 pt right 5, 1 pt down 5.",
 "g(x) = 3(x + 2) = 3x + 6.",
 "(3 − (−1)) ÷ (2 − (−4)) = 4/6. 1 pt slope, 1 pt parallel and perpendicular.",
 "Perpendicular slope −1/2. 1 = (−1/2)(4) + b → b = 3. (A is parallel; B has the wrong sign; D misses (4, 1).)",
 "y − 2 = 4(x + 1) → y = 4x + 4 + 2. 1 pt slope, 1 pt equation.",
 "4x − 2y = 6 → y = 2x − 3. Same slope 2, different y-intercepts.",
 "Plan A: $15/month, starts $30. Plan B: $20/month, starts $10. 1 pt each comparison with meaning.",
 "30 + 15m = 10 + 20m → 20 = 5m. 6 months: A = 30 + 90 = $120, B = 10 + 120 = $130. 1 pt meet, 1 pt 6 months.",
 "p: slope 3/4 = 0.75. y = x − 3 has slope 1 (greater); 3x − 4y = 8 has slope 3/4 (equal); 0.6 and 0.5 are less.",
 "Outputs: 240 gallons at t = 0 down to 0 gallons at t = 20."]
WRITTEN = {3: "g(x) = 3x − 4; vertical dilation by a factor of 3, translation down 4", 5: "Right 5 units; same as down 5 units (h(x) = x − 5)",
           7: "m = 2/3; parallel 2/3; perpendicular −3/2", 9: "y = 4x + 6",
           11: "Plan B has the greater rate ($20 vs $15 per month); Plan A has the greater initial value ($30 vs $10)",
           12: "4 months, $90; Plan A costs less for 6 months ($120 vs $130)"}
MC = {"GEN": {1: "B. up 3", 2: "H. g(x) = −(1/2)x", 4: "C. f(x) + 2", 6: "G. 3x + 6", 8: "C. y = (−1/2)x + 3", 10: "F. parallel",
              13: "D. y = x − 3", 14: "H. 0 ≤ w(t) ≤ 240"},
      "IEP": {1: "A. up 3", 2: "B. g(x) = −(1/2)x", 4: "B. f(x) + 2", 6: "B. 3x + 6", 8: "B. y = (−1/2)x + 3", 10: "A. parallel",
              13: "C. y = x − 3", 14: "B. 0 ≤ w(t) ≤ 240"}}
IEP_FRAMES = {3: "Blanks: 3 · 4 · circle dilation · 3 · circle down · 4", 5: "Blanks: 5 · circle right · 5 · circle down · 5",
              7: "Blanks: 4/6 · 2/3 · 2/3 · −3/2", 9: "Blanks: 4 · 4 · 4 · 6", 11: "Blanks: 30 · 15 · 10 · 20 · B · A",
              12: "Blanks: 20 · 5 · 4 · 90 · 120 · 130 · A"}

NOTE = ("Topic 2 Retake, Wed Nov 4 (the day after the End of Topic 2 Assessment). Same 14 skills, order, item types and points as the "
        "test, with new numbers: Q1-4 Lesson 1, Q5-6 Lesson 2, Q7-10 Lesson 3, Q11-14 Lesson 4.")

if __name__ == "__main__":
    A.TEST, A.SUB = "Topic 2 Retake", "Retake"
    A.STD, A.IEP, A.WORK, A.WRITTEN, A.MC, A.IEP_FRAMES = STD, IEP, WORK, WRITTEN, MC, IEP_FRAMES
    assert len(STD) == len(IEP) == len(A.PTS) == len(WORK) == A.N
    assert all(q in MC["GEN"] or q in WRITTEN for q in range(1, A.N + 1)) and MC["GEN"].keys() == MC["IEP"].keys()
    jobs = [("Module 2 topic 2", "Topic2-Retake", A.deck("General", "Topic 2 Retake", A.DIRS, "", STD, NOTE)),
            ("Module 2 topic 2", "Topic2-Retake-ANSWER-KEY", A.key("GEN", "General and Section 504", "Topic 2 Retake")),
            ("Section 504", "Topic2-Retake-504", A.deck("Section 504 Version", "Topic 2 Retake · Section 504 Version", A.DIR504, A.REF, STD, NOTE + " " + A.N504)),
            ("Section 504", "Topic2-Retake-504-ANSWER-KEY", A.key("GEN", "Section 504 Version", "Topic 2 Retake · Section 504 Version")),
            ("IEP", "Topic2-Retake-IEP", A.deck("IEP Version", "Topic 2 Retake · IEP Version", A.DIRIEP, A.REF, IEP, NOTE + " " + A.NIEP)),
            ("IEP", "Topic2-Retake-IEP-ANSWER-KEY", A.key("IEP", "IEP Version", "Topic 2 Retake · IEP Version"))]
    for folder, name, html in jobs:
        src = ROOT / folder / f"{name}.html"
        src.write_text(html, encoding="utf-8")
        subprocess.run([sys.executable, str(ROOT / "make_pptx.py"), f"{folder}/{name}.html"], cwd=ROOT, check=True)
        if "--keep" not in sys.argv:
            src.unlink()

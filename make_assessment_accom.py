# Writes the Topic 1 assessment as two make_pptx.py-style HTML decks (IEP = modified Form M,
# 504 = original items with access supports only), runs make_pptx.py on each, then removes the HTML.
# Run: python make_assessment_accom.py  (answer keys: make_assessment_keys.py)
import json, subprocess, sys, pathlib

ROOT = pathlib.Path(__file__).parent

def g(w, h, x, y, gx, gy, lines=(), pts=()):
    return "<div class=\"graph\" data-g='" + json.dumps(dict(w=w, h=h, x=x, y=y, gx=gx, gy=gy, lines=list(lines), pts=list(pts))) + "'></div>"

def gracie(marked):
    return ("<div>" + g(530, 360, [0, 45], [0, 3], [2.5, 5], [1/6, 1], [dict(p=[[0, 8/3], [40, 0]], seg=True)],
                        [[10, 2, "(10, 2)"], [25, 1, "(25, 1)"]] if marked else [])
            + '<p class="small muted"><b>Gracie\'s Walk Home</b>. Across: Time (minutes). Up: Distance from Home (miles).</p></div>')

def eggs():
    return ("<div>" + g(500, 360, [0, 10], [0, 20], [1, 1], [2, 2], pts=[[k, 20 - 2*k, ""] for k in range(11)])
            + '<p class="small muted">Across: Batches of Muffins (<i>x</i>). Up: Number of Eggs Remaining (<i>y</i>).</p></div>')

def tbl(rows, size=26):
    th = lambda c: f'<th style="font-style:normal">{c}</th>'
    return f'<table class="tbl" style="font-size:{size}px">' + "".join(
        "<tr>" + th(r[0]) + "".join(f"<td>{c}</td>" for c in r[1:]) + "</tr>"
        for r in rows) + "</table>"

def vtbl(head, body, size=26):
    th = "".join(f'<th style="font-style:normal">{h}</th>' for h in head)
    return f'<table class="tbl" style="font-size:{size}px"><tr>{th}</tr>' + "".join(
        "<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in body) + "</table>"

def ch(letters, *opts):
    return "".join(f"<p>○ &nbsp;<b>{l}.</b> &nbsp;{o}</p>" for l, o in zip(letters, opts))

tip = lambda t: f'<p class="warn">{t}</p>'
work = '<p class="think">Show your work here, or on your scratch paper.</p>'
B = "________"

def deck(label, title, directions, ref, qs, notes):
    def slide(body, n=None, aside=""):
        head = f'<h3>Question {n} of 14</h3>' if n else ""
        foot = f'<p class="foot">Topic 1 Assessment · {label}</p>'
        return (f'<section class="slide">{head}<div style="font-size:30px">{body}</div>{foot}'
                + (f'<aside class="notes">{aside}</aside>' if aside else "") + "</section>")
    out = [slide(f'<h1>Topic 1: Linear Functions</h1><h3>End of Topic Assessment · {label}</h3>'
                 f'<p>Name {B}{B}{B} &nbsp; Date {B}{B}</p><div class="card">{directions}</div>', aside=notes),
           slide(ref)]
    out += [slide(b, n) for n, b in enumerate(qs, 1)]
    out.append(slide('<h2>You are done!</h2><p>Go back and check each answer.</p>'
                     '<p>Did you answer <b>every</b> question?</p><p>Did you include <b>units</b> and <b>explanations</b> where asked?</p>'
                     '<p>Raise your hand when you are finished.</p>'))
    return f'<!doctype html><meta charset="utf-8"><title>{title}</title><body>' + "".join(out) + "</body>"

REF = ('<h2>Reference Sheet</h2><div class="grid3" style="gap:14px">'
       '<div class="card"><p style="font-size:23px"><b>Slope / rate of change</b><br><i>m</i> = {{change in y|change in x}}<br><i>m</i> = {{y₂ − y₁|x₂ − x₁}}</p></div>'
       '<div class="card"><p style="font-size:23px"><b>Slope-intercept form</b><br><i>y</i> = <i>mx</i> + <i>b</i><br><i>m</i> = slope, <i>b</i> = <i>y</i>-intercept</p></div>'
       '<div class="card"><p style="font-size:23px"><b>Point-slope form</b><br><i>y</i> − <i>y</i>₁ = <i>m</i>(<i>x</i> − <i>x</i>₁)</p></div>'
       '<div class="card"><p style="font-size:23px"><b>Standard form</b><br><i>Ax</i> + <i>By</i> = <i>C</i><br>Solve for <i>y</i> to find the slope.</p></div>'
       '<div class="card"><p style="font-size:23px"><b>Intercepts</b><br><i>x</i>-intercept: <i>y</i> = 0<br><i>y</i>-intercept: <i>x</i> = 0</p></div>'
       '<div class="card"><p style="font-size:23px"><b>Correlation <i>r</i></b><br>Near 1 or −1: strong. Near 0: weak.<br><i>r</i> &gt; 0 positive, <i>r</i> &lt; 0 negative</p></div>'
       '<div class="card"><p style="font-size:23px"><b>Calculator: line of best fit</b><br>STAT → EDIT: <i>x</i> in L1, <i>y</i> in L2<br>STAT → CALC → LinReg(ax+b)</p></div>'
       '<div class="card"><p style="font-size:23px"><b>Domain</b> = the <i>x</i>-values (inputs)<br><b>Range</b> = the <i>y</i>-values (outputs)</p></div>'
       '<div class="card"><p style="font-size:23px"><b>Causation</b>: one event <b>makes</b> the other event happen.</p></div></div>')

temps = [90, 99, 98, 99, 104, 108, 109, 110, 112, 100, 91, 90]
T4 = (tbl([["Month", *range(1, 7)], ["Temp (°F)", *temps[:6]]], 24) + tbl([["Month", *range(7, 13)], ["Temp (°F)", *temps[6:]]], 24))
GR = "Use the graph of Gracie's walk home from school."

# ---------------------------------------------------------------- Section 504: original items, access supports only
S504 = [
 '<p>The table shows Lucia\'s salary for different years.</p>' + tbl([["Year", 2000, 2001, 2002, 2003], ["Salary ($)", "40,000", "42,000", "46,000", "44,500"]])
 + '<p>Which linear function <b>best models</b> the data if <i>x</i> represents the number of <b>years since 2000</b>?</p>'
 + ch("ABCD", "<i>y</i> = 39,625<i>x</i> + 4375", "<i>y</i> = 4375<i>x</i> + 39,625", "<i>y</i> = 1750<i>x</i> + 40,500", "<i>y</i> = 40,500<i>x</i> + 1750"),
 '<p>Which situation <b>best</b> represents <b>causation</b>?</p>'
 + ch("FGHJ", "When you are at the beach, you get wet.", "When you study for a test, your classmate studies too.", "When you carry an umbrella to school, it rains.", "When you don't brush your teeth, you get cavities."),
 '<div class="row" style="gap:40px">' + vtbl(["Number of Cookies Sold", "Profit (dollars)"], [[4, "−1.50"], [5, "1.25"], [6, "4.00"], [7, "6.75"]])
 + '<div><p>Nia is selling cookies at a constant price to raise money for charity. The table shows her profit.</p>'
   '<p>Determine the <b>rate of change</b> for the problem situation. Be sure to include <b>units</b> of measure.</p>' + work + '</div></div>',
 '<p>The table shows the monthly high temperature for Austin, Texas, in degrees Fahrenheit over a 12-month period.</p>' + T4
 + '<p>What does the <b>correlation coefficient</b> for the data indicate about the <b>strength</b> of the linear association between the month and the temperature?</p>'
 + '<div class="row" style="gap:20px"><div>' + ch("AB", "Weak negative correlation", "Strong negative correlation") + '</div><div>' + ch("CD", "Weak positive correlation", "Strong positive correlation") + '</div></div>',
 '<p>The table shows the decrease in the amount of chicken feed in a farmer\'s barn over a seven-month period.</p>'
 + tbl([["Month", "March", "April", "May", "June", "July", "Aug.", "Sept."], ["Pounds", 950, 873, 796, 719, 642, 565, 488]], 24)
 + '<p>Determine a <b>linear function</b> that represents <i>y</i>, the number of pounds of chicken feed, in terms of <i>x</i>, the number of <b>months since March</b>.</p>' + work,
 '<div class="row" style="gap:40px">' + vtbl(["Time (hours)", "Money (dollars)"], [[h, m] for h, m in zip(range(8), [0, 16, 35, 47, 60, 69, 90, 103])], 22)
 + '<div><p>The table shows the amount Omar earns at his job based on the number of hours he works.</p>'
   '<p>Based on the table, what is the <b>best prediction</b> of the amount Omar earns for <b>9 hours</b> of work?</p>'
 + ch("FGHJ", "$34.61", "$128.00", "$131.46", "$189") + '</div></div>',
 '<p>What is the <b>slope</b> of the line represented by the equation</p><p class="eq">15<i>x</i> + 3<i>y</i> = 45?</p>' + work,
 '<p>What is the equation in <b>slope-intercept form</b> of a line with a slope of {{1|3}} that passes through the point (−1, −2)?</p>' + work,
 '<div class="row" style="gap:40px">' + vtbl(["Time (minutes)", "Water Left in the Tub (liters)"], [[0, 360], [2, 240], ["3.5", 150], [5, 60]])
 + '<div><p>The water level in a tub is changing at a constant rate. The table shows the relationship between the time in minutes, <i>x</i>, and the amount of water in liters, <i>y</i>.</p>'
   '<p>Determine the <b>rate of change</b> of the water level with respect to time. Then, <b>interpret</b> the rate of change in terms of the problem situation.</p></div></div>' + work,
 '<div class="row" style="gap:40px">' + gracie(False) + f'<div><p>{GR}</p><p>Identify the <b><i>x</i>-intercept</b> and explain its meaning in terms of the problem situation.</p>' + work + '</div></div>',
 '<div class="row" style="gap:40px">' + gracie(False) + f'<div><p>{GR}</p><p>Identify the <b><i>y</i>-intercept</b> and explain its meaning in terms of the problem situation.</p>' + work + '</div></div>',
 '<div class="row" style="gap:40px">' + gracie(False) + f'<div><p>{GR}</p><p>Calculate the <b>slope</b> of the linear function and explain its meaning in terms of the problem situation.</p>' + work + '</div></div>',
 '<p>What is the value of</p><p class="eq"><i>f</i>(<i>x</i>) = 23.2<i>x</i> + 2.5 &nbsp;at&nbsp; <i>x</i> = −4.2?</p>' + ch("ABCD", "−99.94", "−94.94", "−29.9", "21.5"),
 '<div class="row" style="gap:40px">' + eggs() + '<div><p>Miguel has 20 eggs. His muffin recipe uses two eggs per batch. The graph shows <i>y</i>, the number of eggs remaining, and <i>x</i>, the number of batches he bakes.</p>'
   '<p>What is the <b>domain</b> of the function for this situation?</p>'
 + ch("FGHJ", "0 ≤ <i>x</i> ≤ 10", "{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10}", "0 ≤ <i>y</i> ≤ 20", "{0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20}") + '</div></div>',
]

# ---------------------------------------------------------------- IEP: modified Form M (3 choices, chunked steps, tips, frames)
IEP = [
 '<p>The table shows Lucia\'s salary. Let <i>x</i> = the number of years <b>since 2000</b>.</p>'
 + tbl([["Year", 2000, 2001, 2002, 2003], ["x", 0, 1, 2, 3], ["Salary ($)", "40,000", "42,000", "46,000", "44,500"]])
 + '<p>Which linear function <b>best models</b> the data?</p>' + tip("Tip: Use LinReg on your calculator (see the reference sheet).")
 + ch("ABC", "<i>y</i> = 4375<i>x</i> + 39,625", "<i>y</i> = 1750<i>x</i> + 40,500", "<i>y</i> = 40,500<i>x</i> + 1750"),
 '<p>Which situation shows <b>causation</b>?</p>' + tip("Causation means one event <b>makes</b> the other event happen.")
 + ch("ABC", "When you study for a test, your classmate studies too.", "When you carry an umbrella to school, it rains.", "When you don't brush your teeth, you get cavities."),
 '<div class="row" style="gap:40px">' + vtbl(["Cookies Sold", "Profit (dollars)"], [[4, "−1.50"], [5, "1.25"], [6, "4.00"], [7, "6.75"]])
 + f'<div><p>Nia sells cookies at a constant price. The table shows her profit. What is the <b>rate of change</b>?</p>'
   f'<p>Step 1: Change in profit (4 to 5 cookies) = {B} dollars</p><p>Step 2: Change in cookies = {B} cookie</p>'
   f'<p>Step 3: Rate of change = {B} dollars per cookie</p></div></div>',
 '<p>The tables show the monthly high temperature in Austin, Texas.</p>' + T4
 + '<p>What does the correlation coefficient say about the <b>strength</b> of the linear association?</p>'
 + tip("Find <i>r</i> with your calculator. Close to 0 = weak. Close to 1 or −1 = strong.")
 + ch("ABC", "Weak negative correlation", "Weak positive correlation", "Strong positive correlation"),
 '<p>The table shows the pounds of chicken feed in a barn. Let <i>x</i> = months <b>since March</b>.</p>'
 + tbl([["Month", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep"], ["x", 0, 1, 2, 3, 4, 5, 6], ["Pounds (y)", 950, 873, 796, 719, 642, 565, 488]], 24)
 + f'<p>Write a linear function for <i>y</i>, the pounds of chicken feed.</p><p>Starting amount when <i>x</i> = 0: <i>b</i> = {B}</p>'
   f'<p>Change each month: <i>m</i> = {B}</p><p><i>y</i> = {B}<i>x</i> + {B}</p>',
 '<div class="row" style="gap:40px">' + vtbl(["Hours (x)", "Money, $ (y)"], [[h, m] for h, m in zip(range(8), [0, 16, 35, 47, 60, 69, 90, 103])], 22)
 + '<div><p>The table shows how much Omar earns for the hours he works.</p><p>What is the best prediction of what Omar earns for <b>9 hours</b>?</p>'
 + tip("Step 1: Use LinReg to find the line of best fit.<br>Step 2: Put <i>x</i> = 9 into the equation.") + ch("ABC", "$128.00", "$131.46", "$189.00") + '</div></div>',
 '<p>What is the <b>slope</b> of the line 15<i>x</i> + 3<i>y</i> = 45?</p>' + tip("Solve for <i>y</i> to get <i>y</i> = <i>mx</i> + <i>b</i>.")
 + f'<p>Step 1: Subtract 15<i>x</i> from both sides: 3<i>y</i> = {B}{B}</p><p>Step 2: Divide every term by 3: <i>y</i> = {B}{B}</p><p>Slope <i>m</i> = {B}</p>',
 '<p>Write the equation in <b>slope-intercept form</b> of the line with slope {{1|3}} through the point (−1, −2).</p>'
 + tip("Point-slope form: <i>y</i> − <i>y</i>₁ = <i>m</i>(<i>x</i> − <i>x</i>₁). Here <i>m</i> = 1/3, <i>x</i>₁ = −1, <i>y</i>₁ = −2.")
 + f'<p>Step 1: Fill in: <i>y</i> − ({B}) = {B}(<i>x</i> − ({B}))</p><p>Step 2: Simplify: <i>y</i> + 2 = {{{{1|3}}}}(<i>x</i> + 1)</p>'
   f'<p>Step 3: Distribute, then subtract 2: <i>y</i> = {B}{B}{B}</p>',
 '<div class="row" style="gap:40px">' + vtbl(["Time, min (x)", "Water left, L (y)"], [[0, 360], [2, 240], ["3.5", 150], [5, 60]])
 + f'<div><p>The water in a tub drains at a constant rate.</p><p>Step 1: Use (0, 360) and (2, 240).<br>Rate = {{{{240 − 360|2 − 0}}}} = {B} liters per minute</p>'
   f'<p>Step 2: The water level goes <b>up / down</b> (circle one) by {B} liters every minute.</p></div></div>',
 '<div class="row" style="gap:40px">' + gracie(True) + f'<div><p>{GR}</p><p>What is the <b><i>x</i>-intercept</b>? What does it mean?</p>'
 + tip("Each box across is 2.5 minutes. Each box up is 1/6 of a mile.")
 + f'<p><i>x</i>-intercept = ({B}, 0)</p><p>After {B} minutes, Gracie is {B} miles from home. (She is {B}.)</p></div></div>',
 '<div class="row" style="gap:40px">' + gracie(True) + f'<div><p>{GR}</p><p>What is the <b><i>y</i>-intercept</b>? What does it mean?</p>'
 + tip("Each box up is 1/6 of a mile.")
 + f'<p><i>y</i>-intercept = (0, {B})</p><p>At 0 minutes (when she leaves school), Gracie is {B} miles from home.</p></div></div>',
 '<div class="row" style="gap:40px">' + gracie(True) + f'<div><p>{GR}</p><p>Find the <b>slope</b>. What does it mean?</p>'
 + f'<p>Use the marked points (10, 2) and (25, 1):<br><i>m</i> = {{{{1 − 2|25 − 10}}}} = {B} mile per minute</p>'
   f'<p>Gracie gets {B} mile <b>closer to / farther from</b> (circle one) home every minute.</p></div></div>',
 '<p>What is the value of <i>f</i>(<i>x</i>) = 23.2<i>x</i> + 2.5 when <i>x</i> = −4.2?</p>'
 + tip("Replace <i>x</i> with −4.2: <i>f</i>(−4.2) = 23.2(−4.2) + 2.5. You may use a calculator.") + ch("ABC", "−99.94", "−94.94", "21.5"),
 '<div class="row" style="gap:40px">' + eggs() + '<div><p>Miguel has 20 eggs. Each batch of muffins uses 2 eggs.</p><p>What is the <b>domain</b> of the function?</p>'
 + tip("Domain = the <i>x</i>-values. He can only bake <b>whole</b> batches.")
 + ch("ABC", "0 ≤ <i>x</i> ≤ 10", "{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10}", "{0, 2, 4, 6, 8, 10, …, 20}") + '</div></div>',
]

DIR504 = ('<p><b>Directions:</b> Read each question carefully. You may use a calculator and the reference sheet. '
          'For multiple choice, choose <b>one</b> answer. For the other questions, show your work and include units.</p>'
          '<p>One question is on each slide. Take your time. Ask your teacher if you need a break or a question read aloud.</p>')
DIRIEP = ('<p><b>Directions:</b> Read each question carefully. You may use a calculator and the reference sheet. '
          'For multiple choice, choose <b>one</b> answer. Use the steps and tips. Fill in each blank.</p>'
          '<p>One question is on each slide. Take your time. Ask your teacher if you need a break or a question read aloud.</p>')
N504 = ("Section 504 version: the same 14 items, wording and answer choices as the original End of Topic Assessment, so it is graded with the "
        "original answer key (assessment/Topic1-Assessment-Original-ANSWER-KEY.pdf). Only access changes: one question per slide, larger font, key words in bold, "
        "reference sheet, work space, a split temperature table, and the Gracie graph repeated on questions 10 to 12. Apply the student's plan: extended time, "
        "breaks, read-aloud, small-group or separate setting, preferential seating.")
NIEP = ("IEP version: the modified Form M. Multiple choice has 3 choices; open items are chunked into steps with blanks and sentence frames; tips define "
        "vocabulary; x-rows are added to the tables in Q1 and Q5; two points are marked on the Gracie graph. Grade with the Form M answer key "
        "(assessment/Topic1-Assessment-FormM-ANSWER-KEY.pdf). "
        "Apply the student's IEP accommodations as well: extended time, breaks, read-aloud, small-group setting.")

if __name__ == "__main__":
    for folder, name, label, dirs, qs, notes in [
            ("IEP", "Topic1-Assessment-IEP", "IEP Version", DIRIEP, IEP, NIEP),
            ("Section 504", "Topic1-Assessment-504", "Section 504 Version", DIR504, S504, N504)]:
        src = ROOT / folder / f"{name}.html"
        src.write_text(deck(label, f"Topic 1 Assessment · {label}", dirs, REF, qs, notes), encoding="utf-8")
        r = subprocess.run([sys.executable, str(ROOT / "make_pptx.py"), f"{folder}/{name}.html"], cwd=ROOT)
        if "--keep" not in sys.argv:
            src.unlink()

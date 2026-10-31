# Topic 1 Review (Tue Nov 17): mirrors the 11-item Module 3 Topic 1 End of Topic Assessment
# (materials/Secondary Mathematics Algebra Module 3 Topic 1 Assements Student Edition.pdf) item for item:
# same skill and format, new numbers. Part 2 adds 4 extra-practice items.
# Writes printed General + key, Section 504 (same items, general key), IEP (3 choices, tips, step frames) + key,
# and online self-check pages (General / 504 / IEP).   Run: python make_m3t1_review.py
import json, re, subprocess
from pathlib import Path

import make_t2_review_test as RT   # print CSS + fractions
import make_t2_practice as MP      # online page shell (mc.js)
import make_accom_lessons as A     # HELP text for IEP/504 online pages

ROOT = Path(__file__).parent
OUT = ROOT / "Module 3 topic 1"
FOLDER = {"504": ROOT / "Section 504", "IEP": ROOT / "IEP"}
EDGE = RT.EDGE
KEY = False
fr = RT.fr
i = lambda s: f"<i>{s}</i>"
x, y, m, n, t, k, h = (i(c) for c in "xymntkh")


def it(q, kind, ans, choices, why, tip, frames, pos=0, iep3=None):
    """choices: first is correct (online + printed MC). pos = printed letter of the right answer.
    frames: IEP fill-in steps; [[...]] is a blank that is filled in red on the key. iep3: IEP's 3 choices (first correct)."""
    return dict(q=q, kind=kind, ans=ans, choices=choices, why=why, tip=tip, frames=frames, pos=pos, iep3=iep3 or choices[:3])


def numline(lo=-10, hi=2, mark=None, left=True, open_=True):
    W, u = 520, 520 / (hi - lo + 2)
    X = lambda v: (v - lo + 1) * u
    s = f'<svg class="g" width="{W}" height="56" viewBox="0 0 {W} 56"><line x1="4" y1="24" x2="{W - 4}" y2="24" stroke="#111" stroke-width="1.5"/>'
    s += f'<path d="M4 24l9-5v10zM{W - 4} 24l-9-5v10z" fill="#111"/>'
    for v in range(lo, hi + 1):
        s += f'<line x1="{X(v)}" y1="18" x2="{X(v)}" y2="30" stroke="#111"/><text x="{X(v)}" y="46" font-size="12" text-anchor="middle">{str(v).replace("-", "−")}</text>'
    if KEY and mark is not None:
        end = 6 if left else W - 6
        s += f'<line x1="{X(mark)}" y1="24" x2="{end}" y2="24" stroke="{RT.RED}" stroke-width="5"/>'
        s += f'<circle cx="{X(mark)}" cy="24" r="7" fill="{"#fff" if open_ else RT.RED}" stroke="{RT.RED}" stroke-width="3"/>'
    return s + "</svg>"


def items():
    return [
        # 1 (test Q1): equation from a savings context
        it(f"Jayden has $40 in his bank account. He deposits $15 each week to save for new headphones. Which equation can be used to "
           f"determine the amount that Jayden has saved, {y}, after {x} weeks?", "mc", None,
           [f"{y} = 15{x} + 40", f"{y} = 15 + 40{x}", f"{y} = −15{x} + 40", f"{y} = −40{x} + 15"],
           "$15 per week is the rate (multiplies x); the $40 he starts with is the constant.",
           "Rate × weeks + starting amount.", [f"Rate per week = [[15]]", f"Starting amount = [[40]]", f"{y} = [[15]]{x} + [[40]]"], pos=1),
        # 2 (test Q2): distribute both sides, no solution
        it(f"What value of {k} makes the equation 5 − 4({k} + 3) = 9 − 2(2{k} + 6) true?", "mc", None,
           ["No solution", "1", "2", "4"],
           "Left: 5 − 4k − 12 = −4k − 7. Right: 9 − 4k − 12 = −4k − 3. Same k-term, different constants → no solution.",
           "Distribute, then combine like terms on each side. Same variable terms + different numbers = no solution.",
           [f"Left side: 5 − 4{k} − 12 = [[−4k − 7]]", f"Right side: 9 − 4{k} − 12 = [[−4k − 3]]", "−7 = −3 is [[false]], so: [[No solution]]"], pos=3),
        # 3 (test Q3): inequality with a negative coefficient
        it(f"What is the solution set for 3(4 − {t}) &gt; −2{t} + 15?", "mc", None,
           [f"{t} &lt; −3", f"{t} &gt; −3", f"{t} &lt; 3", f"{t} ≥ 3"],
           "12 − 3t > −2t + 15 → −t > 3 → divide by −1 and flip: t < −3.",
           "Dividing or multiplying by a negative <b>flips</b> the inequality sign.",
           [f"Distribute: [[12 − 3t]] &gt; −2{t} + 15", f"Add 2{t}, subtract 12: [[−t]] &gt; [[3]]", f"Divide by −1 and flip: {t} [[&lt;]] [[−3]]"], pos=3,
           iep3=[f"{t} &lt; −3", f"{t} &gt; −3", f"{t} &gt; 3"]),
        # 4 (test Q4): decimals, variables on both sides
        it(f"Solve the equation shown.<br>0.3(4{x} − 6) = −1.8{x} + 4.2", "open", f"{x} = 2",
           [f"{x} = 2", f"{x} = 0.8", f"{x} = −2", f"{x} = 4"],
           "1.2x − 1.8 = −1.8x + 4.2 → 3x = 6 → x = 2. Check: 0.3(2) = 0.6 and −3.6 + 4.2 = 0.6 ✓",
           "Distribute the 0.3 to both terms first.",
           [f"Distribute: [[1.2x]] − [[1.8]] = −1.8{x} + 4.2", f"Add 1.8{x} and 1.8: [[3]]{x} = [[6]]", f"{x} = [[2]]"]),
        # 5 (test Q5): one / none / infinite with a fraction
        it(f"Does the equation shown below have one solution, no solution, or an infinite number of solutions? Explain your reasoning.<br>"
           f"{fr(1, 3)}(12{x} + 30) = 4({x} + 2) + 2", "open", "Infinite solutions: both sides simplify to 4x + 10",
           ["Infinite solutions", "One solution", "No solution", f"{x} = 10"],
           "Left: 4x + 10. Right: 4x + 8 + 2 = 4x + 10. The sides are identical, so every x works.",
           "Simplify each side. Identical sides = infinite. Same x-term, different numbers = none.",
           [f"Left: {fr(1, 3)}(12{x}) + {fr(1, 3)}(30) = [[4x + 10]]", f"Right: 4{x} + 8 + 2 = [[4x + 10]]", "Answer: [[infinite solutions]]"]),
        # 6 (test Q6): write a cost equation
        it(f"Maya goes to a school store. She buys 4 notebooks that cost $1.75 each and some pens for $1.20 each. "
           f"Write an equation for the total cost, {y}, when Maya buys {x} pens.", "open", f"{y} = 1.20{x} + 7.00",
           [f"{y} = 1.20{x} + 7.00", f"{y} = 1.75{x} + 4.80", f"{y} = 4{x} + 1.20", f"{y} = 7{x} + 1.20"],
           "Notebooks are a fixed $7.00 (4 × 1.75). Pens change: $1.20 per pen → y = 1.20x + 7.00.",
           "The thing that changes (pens) gets the x. Fixed items become the constant.",
           ["Notebooks: 4 × 1.75 = [[7.00]]", f"Pens: [[1.20]]{x}", f"{y} = [[1.20]]{x} + [[7.00]]"]),
        # 7 (test Q7): standard → slope-intercept
        it(f"Rewrite the equation in slope-intercept form.<br>2{x} + 5{y} = 15", "open", f"{y} = −{fr(2, 5)}{x} + 3",
           [f"{y} = −2/5 {x} + 3", f"{y} = 2/5 {x} + 3", f"{y} = −2{x} + 15", f"{y} = −5/2 {x} + 15/2"],
           "5y = −2x + 15 → divide every term by 5: y = −2/5 x + 3.",
           f"Get {y} alone: move the {x}-term, then divide <b>every</b> term by the number in front of {y}.",
           [f"Subtract 2{x}: 5{y} = [[−2x]] + 15", f"Divide every term by [[5]]", f"{y} = [[−2/5]]{x} + [[3]]"]),
        # 8 (test Q8): literal equation
        it(f"The formula for the volume of a rectangular prism is {i('V')} = {i('ℓwh')}. Solve the equation for {h}.", "open",
           f"{h} = {fr(i('V'), i('ℓw'))}",
           [f"{h} = V/(ℓw)", f"{h} = Vℓw", f"{h} = V − ℓw", f"{h} = ℓw/V"],
           "h is multiplied by ℓw, so divide both sides by ℓw.",
           f"Undo what is being done to {h}. It is multiplied by ℓ{i('w')}, so divide.",
           [f"{h} is multiplied by [[ℓw]]", "Divide both sides by [[ℓw]]", f"{h} = [[V/(ℓw)]]"]),
        # 9 (test Q9): solve + graph inequality
        it(f"Solve the inequality, and graph the solution on the number line.<br>2.5{m} − 3 &lt; −1.5({m} + 18)", "open+nl",
           f"{m} &lt; −6 (open circle at −6, shade left)",
           [f"{m} &lt; −6", f"{m} &gt; −6", f"{m} &lt; 6", f"{m} ≤ −6"],
           "2.5m − 3 < −1.5m − 27 → add 1.5m and 3: 4m < −24 → m < −6. Open circle at −6, shade left.",
           "Open circle for &lt; or &gt;. Closed circle for ≤ or ≥.",
           [f"Distribute: 2.5{m} − 3 &lt; [[−1.5m − 27]]", f"Add 1.5{m} and 3: [[4]]{m} &lt; [[−24]]",
            f"{m} [[&lt;]] [[−6]] → [[open]] circle at −6, shade [[left]]"]),
        # 10 (test Q10): point-slope → slope-intercept
        it(f"Rewrite the equation {y} − 4 = 3({x} + 2) in slope-intercept form.", "open", f"{y} = 3{x} + 10",
           [f"{y} = 3{x} + 10", f"{y} = 3{x} + 6", f"{y} = 3{x} − 2", f"{y} = 3{x} + 2"],
           "y − 4 = 3x + 6 → add 4: y = 3x + 10.",
           "Distribute, then add the number on the y side to both sides.",
           [f"Distribute: {y} − 4 = [[3x + 6]]", "Add [[4]] to both sides", f"{y} = [[3x + 10]]"]),
        # 11 (test Q11): equal areas
        it(f"A triangle has a height of (3{n} − 6) inches and a base of 10 inches. A rectangle has a length of 5 inches and a width of "
           f"({n} + 4) inches. The area of the triangle is equal to the area of the rectangle. What is the value of {n}?", "open", f"{n} = 5",
           [f"{n} = 5", f"{n} = 1", f"{n} = 2.5", f"{n} = 13"],
           "½(10)(3n − 6) = 5(n + 4) → 15n − 30 = 5n + 20 → 10n = 50 → n = 5. Check: both areas are 45 in².",
           "Triangle area = ½ · base · height. Rectangle area = length · width. Set them equal.",
           [f"Triangle: ½ · 10 · (3{n} − 6) = [[15n − 30]]", f"Rectangle: 5({n} + 4) = [[5n + 20]]", f"15{n} − 30 = 5{n} + 20 → {n} = [[5]]"]),
        # ---- Part 2 extra practice
        it("Which equation has <b>no solution</b>?", "mc", None,
           [f"3({x} − 2) = 3{x} + 5", f"3({x} − 2) = 3{x} − 6", f"3({x} − 2) = 2{x} + 5", f"3{x} − 2 = 2{x} − 3"],
           "3x − 6 = 3x + 5: same x-term, different constants. (G is infinite; H and J have one solution.)",
           "Simplify each one. Look for the same x-term but different numbers.", [], pos=0),
        it(f"What is the solution set for −4{x} + 7 ≥ 19?", "mc", None,
           [f"{x} ≤ −3", f"{x} ≥ −3", f"{x} ≤ 3", f"{x} ≥ −6.5"],
           "−4x ≥ 12 → divide by −4 and flip: x ≤ −3.", "Divide by a negative → flip the sign.",
           ["Subtract 7: −4" + x + " ≥ [[12]]", f"Divide by −4 and flip: {x} [[≤]] [[−3]]"], pos=2),
        it(f"The perimeter of a rectangle is {i('P')} = 2{i('ℓ')} + 2{i('w')}. Solve for {i('w')}.", "open",
           f"{i('w')} = {fr(i('P') + ' − 2' + i('ℓ'), 2)}",
           [f"w = (P − 2ℓ)/2", f"w = P − 2ℓ", f"w = (P + 2ℓ)/2", f"w = P/2 − 2ℓ"],
           "Subtract 2ℓ from both sides, then divide by 2: w = (P − 2ℓ)/2 (or w = P/2 − ℓ).",
           "Undo the adding first, then the multiplying.",
           ["Subtract 2ℓ: 2w = [[P − 2ℓ]]", "Divide by [[2]]: w = [[(P − 2ℓ)/2]]"]),
        it("A gym charges a $25 sign-up fee plus $8 per class. Lena can spend at most $90. Write and solve an inequality for the "
           "number of classes, " + i("c") + ", she can take.", "open", "25 + 8" + i("c") + " ≤ 90 → " + i("c") + " ≤ 8.125, so at most 8 classes",
           ["At most 8 classes", "At least 8 classes", "At most 11 classes", "At most 14 classes"],
           "25 + 8c ≤ 90 → 8c ≤ 65 → c ≤ 8.125. Classes are whole numbers, so 8.",
           "“At most” means ≤.", ["25 + 8" + i("c") + " [[≤]] 90", "8" + i("c") + " ≤ [[65]]", i("c") + " ≤ [[8.125]] → at most [[8]] classes"]),
    ]


ITEMS = items


def blanks(s):
    return re.sub(r"\[\[(.+?)\]\]", lambda g: f'<span class="bl">{g.group(1) if KEY else ""}</span>', s)


def printed(q, num, iep):
    L = "ABCD" if num % 2 else "FGHJ"
    body = f"<p>{q['q']}</p>"
    if iep:
        body += RT.tip(q["tip"])
        body += "".join(f"<p>Step {j}: {blanks(f)}</p>" for j, f in enumerate(q["frames"], 1))
    if q["kind"] == "mc":
        ch = q["iep3"] if iep else q["choices"]
        pos = min(q["pos"], len(ch) - 1)
        order = ch[1:pos + 1] + [ch[0]] + ch[pos + 1:]
        body += '<div class="mc">' + "".join(
            f'<p class="{"ok" if KEY and c == ch[0] else ""}"><b>{l}.</b> {c}</p>' for l, c in zip(L, order)) + "</div>"
        if KEY and not iep:
            body += f'<div class="ans"><div class="why">{q["why"]}</div></div>'
    else:
        if q["kind"] == "open+nl":
            body += numline(-10, 2, -6, left=True, open_=True)
        if not iep:
            body += '<div class="work"></div>'
        body += f'<p class="blank">Answer: <span class="ln">{q["ans"] if KEY else ""}</span></p>'
        if KEY and not iep:
            body += f'<div class="ans"><div class="why">{q["why"]}</div></div>'
    return body


REF = """<div class="ref"><p><b>Reference box</b></p>
<p><b>Solving:</b> distribute → combine like terms → get the variable on one side → undo + and − → undo × and ÷. Check by substituting.</p>
<p><b>Same</b> sides (3x + 5 = 3x + 5): infinite solutions · <b>same x-term, different numbers</b> (3x + 5 = 3x + 2): no solution.</p>
<p><b>Inequalities:</b> multiply or divide by a negative → <b>flip</b> the sign. &lt; or &gt;: open circle · ≤ or ≥: closed circle.</p>
<p>Slope-intercept form: <b>y = mx + b</b> · Standard form: <b>Ax + By = C</b> · Triangle area = ½bh · Rectangle area = ℓw</p></div>"""


def build(key, kind=None):
    global KEY
    KEY = key
    iep, big = kind == "IEP", kind in ("IEP", "504")
    qs = ITEMS()
    label = {"IEP": " · IEP", "504": " · Section 504"}.get(kind, "")
    dirs = ("<b>Directions:</b> This review has the same kinds of questions as the Topic 1 test, in the same order. "
            + ("Use the tips and fill in each step. Choose <b>one</b> answer for multiple choice." if iep else
               "Show your work. For multiple choice, choose one answer.")
            + " Finish Part 1 (just like the test) first; Part 2 is extra practice."
            + (" One question per page. You may use the reference box and a calculator. Ask if you need a question read aloud." if big else ""))
    body = (f'<header><h1>Topic 1 Review{label}{" · ANSWER KEY" if key else ""}</h1>'
            '<p class="sub">Algebra I · Module 3, Topic 1: Linear Equations and Inequalities · Tuesday, Nov 17 · Test Wed Nov 18</p>'
            + ("" if key else '<p class="sub">Name ______________________________ &nbsp; Period _____ &nbsp; Date __________</p>')
            + f'</header><p class="dir">{dirs}</p>' + (REF if big else "")
            + '<div class="part">Part 1 · Just like the test (Questions 1–11)</div>')
    for num, q in enumerate(qs, 1):
        if num == 12:
            body += '<div class="part" style="break-before:page">Part 2 · Extra practice (Questions 12–15)</div>'
        body += (f'<div class="q"{" style=break-before:auto" if big and num in (1, 12) else ""}>'
                 f'<div class="n">{num}.</div><div>{printed(q, num, iep)}</div></div>')
    name = "T1-Review" + ("-IEP" if iep else "-504" if big else "") + ("-ANSWER-KEY" if key else "")
    folder = OUT / "REVIEW"
    folder.mkdir(exist_ok=True)
    src = folder / f"{name}.html"
    css = RT.CSS + (RT.CSS504 if big else "") + ".bl{display:inline-block;min-width:.9in;border-bottom:1.5px solid #111;text-align:center;color:#c8102e;font-weight:bold}"
    src.write_text(f"<!doctype html><meta charset='utf-8'><title>{name}</title><style>{css}</style>{body}", encoding="utf-8")
    pdf = folder / f"{name}.pdf"
    subprocess.run([EDGE, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={pdf}", src.as_uri()],
                   check=True, capture_output=True)
    src.unlink()
    print(pdf)


def strip(s):  # online pages: plain text math
    s = re.sub(r'<span class="fr"><span>(.*?)</span><span>(.*?)</span></span>', r"\1/\2", s)
    return s.replace("&lt;", "<").replace("&gt;", ">")


def unbr(f):
    return re.sub(r"\[\[(.+?)\]\]", r"", f)


def online():
    global KEY
    KEY = False
    qs = ITEMS()
    data = [{"q": strip(q["q"]), "choices": q["choices"], "why": strip(q["why"])} | ({"letters": "FGHJ"} if j % 2 else {})
            for j, q in enumerate(qs)]
    MP.OUT = OUT
    name = "m3t1-review.html"
    MP.page(name, "Topic 1 Review · Linear Equations and Inequalities", "Module 3 · Topic 1 · Review · Tue Nov 17", "Topic 1 Review",
            "Questions 1–11 are just like the test, in the same order; 12–15 are extra practice. Pick an answer to see if you are right.",
            "homework", data)
    s = (OUT / name).read_text(encoding="utf-8")
    for kind, lab in (("504", "Section 504"), ("IEP", "IEP")):
        accom = {"readAloud": True}
        if kind == "IEP":
            accom["choices"] = 3
            accom["add"] = [{"extra": f'<p style="margin:8px 0 2px;padding:6px 12px;border-left:4px solid #2f6fdd;background:rgba(47,111,221,.08);border-radius:4px"><b>Tip:</b> {strip(q["tip"])}</p>',
                             "why": "Here is how:" + "".join(f"<br><b>{j}.</b> {strip(unbr(f))}" for j, f in enumerate(q["frames"], 1))}
                            for q in qs]
        t = s.replace("</title>", f" · {lab}</title>", 1).replace('<div class="wrap">', '<div class="wrap big">', 1)
        t = re.sub(r'(<p class="eyebrow">.*?)</p>', lambda g: f"{g.group(1)} · {lab} Version</p>", t, count=1)
        t = re.sub(r'(<p class="muted">.*?</p>)', lambda g: g.group(1) + f'\n  <div class="card ref"><p>{A.HELP[kind]}</p>{REF[REF.index("<p><b>Solving"):-6]}</div>', t, count=1)
        t = t.replace('</script>\n<script src="../mc.js">', f'window.MC.accom = {json.dumps(accom, ensure_ascii=False)};\n</script>\n<script src="../mc.js">')
        assert "window.MC.accom" in t
        (FOLDER[kind] / f"m3t1-review-{kind}.html").write_text(t, encoding="utf-8")
    print("online pages written")


if __name__ == "__main__":
    for q in ITEMS():  # every item has a correct first choice and 4 choices
        assert len(q["choices"]) == 4 and len(q["iep3"]) == 3 and q["iep3"][0] == q["choices"][0]
    build(False); build(True)
    build(False, "504")          # graded with the general key: same items and letters
    build(False, "IEP"); build(True, "IEP")
    online()

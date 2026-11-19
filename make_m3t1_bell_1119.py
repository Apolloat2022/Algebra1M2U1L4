"""Thu 11/19 bell work (printed) and exit ticket (online, m3t1-exit-ticket-thu-11-19): Topic 1 mixed review (Lessons 1-3) for the test-finish / EDIA day.
Skill-based, new numbers, not test twins. Builds general / 504 / IEP sheets + keys into Module 3 topic 1/BELL WORK.
Run:  python make_m3t1_bell_1119.py"""
import make_m3t1_lessons as L

bq = L.bq
BELL = [
 bq("What value of [[x]] makes [[5(x − 1) = 2x + 7]] true?", ["[[4]]", "[[8/3]]", "[[−4]]", "[[12]]"],
    "Distribute: [[5x − 5 = 2x + 7]]. Subtract [[2x]]: [[3x − 5 = 7]]. Add 5: [[3x = 12]], [[x = 4]]. 8/3 forgets to multiply the 1.",
    "distribute, then get [[x]] on one side", ["Distribute: [[5x − 5 = 2x + 7]].", "Subtract [[2x]]: [[3x − 5 = 7]].", "Add 5: [[3x = 12]].", "Divide by 3: [[x = 4]]."]),
 bq("How many solutions does [[2(3x − 4) = 6x − 8]] have?", ["Infinite solutions", "No solution", "One solution, [[x = 0]]", "One solution, [[x = −8]]"],
    "Distribute: [[6x − 8 = 6x − 8]]. Same [[x]]-term and same number: always true.", "same [[x]]-term + same number → infinite",
    ["Distribute: [[6x − 8]].", "Both sides are [[6x − 8]].", "Always true: infinite solutions."]),
 bq("[[A = ½bh]]. Which equation is solved for [[h]]?", ["[[h = 2A/b]]", "[[h = A/(2b)]]", "[[h = 2Ab]]", "[[h = A − ½b]]"],
    "Multiply both sides by 2: [[2A = bh]]. Divide by [[b]]: [[h = 2A/b]].", "undo everything around [[h]]",
    ["Multiply by 2: [[2A = bh]].", "Divide by [[b]]: [[h = 2A/b]]."]),
 bq("What is the solution set of [[9 − 3x < 15]]?", ["[[x > −2]]", "[[x < −2]]", "[[x > 2]]", "[[x < −8]]"],
    "Subtract 9: [[−3x < 6]]. Divide by [[−3]] and flip: [[x > −2]].", "÷ by a negative → flip the sign",
    ["Subtract 9: [[−3x < 6]].", "Divide by [[−3]]: [[6 ÷ −3 = −2]].", "Negative divisor: flip [[<]] to [[>]]: [[x > −2]]."]),
]

EXIT = [
 bq("What value of [[x]] makes [[4x + 3 = 2(x − 5) + 1]] true?", ["[[−6]]", "[[−3.5]]", "[[6]]", "[[−2]]"],
    "Distribute: [[4x + 3 = 2x − 9]]. Subtract [[2x]]: [[2x + 3 = −9]]. Subtract 3: [[2x = −12]], [[x = −6]].",
    "distribute, then get [[x]] on one side", ["Distribute: [[2x − 10 + 1 = 2x − 9]].", "Subtract [[2x]]: [[2x + 3 = −9]].", "Subtract 3: [[2x = −12]].", "Divide by 2: [[x = −6]]."]),
 bq("What is the [[x]]-intercept of [[y = 3x − 12]]?", ["[[(4, 0)]]", "[[(−4, 0)]]", "[[(0, −12)]]", "[[(12, 0)]]"],
    "Put 0 in for [[y]]: [[0 = 3x − 12]], [[3x = 12]], [[x = 4]].", "[[x]]-intercept: put 0 in for [[y]]",
    ["[[0 = 3x − 12]].", "Add 12: [[12 = 3x]].", "Divide by 3: [[x = 4]], so [[(4, 0)]]."]),
 bq("Sam has 56 points and earns 6 points per quiz, [[q]]. He needs at least 80 points. Which inequality shows this?",
    ["[[56 + 6q ≥ 80]]", "[[56 + 6q ≤ 80]]", "[[6 + 56q ≥ 80]]", "[[56 + 6q > 80]]"],
    "Start 56, add 6 per quiz. At least 80 means 80 or more: [[≥]].", "at least = this much or more ([[≥]])",
    ["Start: 56.", "Rate: 6 per quiz: [[6q]].", "At least 80: [[≥ 80]]."]),
 bq("What is the solution set of [[−2(x + 1) ≥ 10]]?", ["[[x ≤ −6]]", "[[x ≥ −6]]", "[[x ≤ −4]]", "[[x ≥ −4]]"],
    "Distribute: [[−2x − 2 ≥ 10]]. Add 2: [[−2x ≥ 12]]. Divide by [[−2]] and flip: [[x ≤ −6]].", "÷ by a negative → flip the sign",
    ["Distribute: [[−2x − 2 ≥ 10]].", "Add 2: [[−2x ≥ 12]].", "Divide by [[−2]] and flip: [[x ≤ −6]]."]),
]


def exit_pages(tag):
    """Online exit ticket (general / 504 / IEP), same accommodations as the lesson bell work pages."""
    import json, re
    A, MP = L.A, L.MP
    name = "m3t1-exit-ticket-thu-11-19.html"
    qs = [{k: q[k] for k in ("q", "choices", "why")} | ({"letters": "FGHJ"} if i % 2 else {}) for i, q in enumerate(EXIT)]
    MP.OUT = L.OUT
    MP.page(name, "Topic 1 Exit Ticket · Thu 11/19", "Module 3 · Topic 1 · Thursday 11/19 · Exit Ticket", "Exit Ticket: Show What You Know",
            "Work each question on paper first. Answer all 4, then submit and show your teacher your score.", "quiz", qs)
    s = (L.OUT / name).read_text(encoding="utf-8")
    for kind in ("504", "IEP"):
        accom = {"readAloud": True}
        if kind == "IEP":
            accom["choices"] = 3
            accom["add"] = [{"extra": f'<p class="formula" style="margin:8px 0 2px;padding:6px 12px;border-left:4px solid #2f6fdd;background:rgba(47,111,221,.08);'
                                      f'border-radius:4px"><b>Formula:</b> {A.mt(q["formula"])}</p>',
                             "why": "Here is how:" + "".join(f"<br><b>{j}.</b> {t}" for j, t in enumerate(q["steps"], 1))} for q in EXIT]
        ref = f'<div class="card ref"><p>{A.HELP[kind]}</p>' + "".join(f"<p>{r}</p>" for r in L.ACC[tag]["ref"]) + "</div>"
        t = s.replace("</title>", f" · {L.LABEL[kind]}</title>", 1).replace('<div class="wrap">', '<div class="wrap big">', 1)
        t = re.sub(r'(<p class="eyebrow">.*?)</p>', lambda m: f"{m.group(1)} · {L.LABEL[kind]} Version</p>", t, count=1)
        t = re.sub(r'(<p class="muted">.*?</p>)', lambda m: m.group(1) + "\n  " + ref, t, count=1)
        t = t.replace('</script>\n<script src="../mc.js">', f'window.MC.accom = {json.dumps(accom, ensure_ascii=False)};\n</script>\n<script src="../mc.js">')
        assert "window.MC.accom" in t
        (L.FOLDER[kind] / f"{name[:-5]}-{kind}.html").write_text(t, encoding="utf-8")
    print(name, "+ 504 + IEP")


if __name__ == "__main__":
    assert all(len(set(q["choices"])) == 4 for q in BELL + EXIT)
    tag = "1–3"
    L.ACC[tag] = {"ref": [L.ACC[1]["ref"][0], L.ACC[1]["ref"][3], L.ACC[2]["ref"][3], L.ACC[3]["ref"][2]]}
    items = [dict(num=k, q=q["q"], choices=L.print_order(q["choices"], (k + 1) % 4), letters="FGHJ" if k % 2 == 0 else "ABCD",
                  answer=q["choices"][0], why=q["why"], tip=q["formula"], frames=None) for k, q in enumerate(BELL, 1)]
    for kind in (None, "504", "IEP"):
        for key in (False, True):
            name = f"T1-Bell-Work-Thu-11-19{f'-{kind}' if kind else ''}{'-ANSWER-KEY' if key else ''}"
            L.sheet(name, "BELL WORK", tag, items, key, kind)
            print(name)
    exit_pages(tag)

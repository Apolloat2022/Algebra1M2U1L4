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

# Exit ticket from the Topic 1 test standards report: A1.5.A (4 test items) x2, A1.12.E (3), A1.2.C (2), A1.5.B (2). Skill-based, not test twins.
EXIT = [
 bq("[[x]]: 0, 2, 4 and [[y]]: 3, 7, 11. Which equation fits this table?", ["[[y = 2x + 3]]", "[[y = 3x + 2]]", "[[y = 4x + 3]]", "[[y = 2x + 7]]"],  # A1.2.C
    "[[y]] goes up 4 when [[x]] goes up 2: slope [[4/2 = 2]]. At [[x = 0]], [[y = 3]]: [[y = 2x + 3]].", "slope = change in [[y]] ÷ change in [[x]]; start = [[y]] when [[x = 0]]",
    ["Change in [[y]]: [[7 − 3 = 4]]. Change in [[x]]: [[2 − 0 = 2]].", "Slope: [[4 ÷ 2 = 2]].", "When [[x = 0]], [[y = 3]].", "[[y = 2x + 3]]."]),
 bq("What value of [[x]] makes [[7x − 4 = 3x + 16]] true?", ["[[5]]", "[[20]]", "[[−5]]", "[[1.2]]"],  # A1.5.A
    "Subtract [[3x]]: [[4x − 4 = 16]]. Add 4: [[4x = 20]]. Divide by 4: [[x = 5]].", "get [[x]] on one side, then undo + and ×",
    ["Subtract [[3x]]: [[4x − 4 = 16]].", "Add 4: [[4x = 20]].", "Divide by 4: [[x = 5]]."]),
 bq("What value of [[x]] makes [[3(2x − 1) − x = 12]] true?", ["[[3]]", "[[2.6]]", "[[−3]]", "[[1.8]]"],  # A1.5.A
    "Distribute: [[6x − 3 − x = 12]]. Combine: [[5x − 3 = 12]]. Add 3: [[5x = 15]], [[x = 3]]. 2.6 forgets to multiply the 1.",
    "distribute, combine like terms, then solve", ["Distribute: [[6x − 3 − x = 12]].", "Combine: [[5x − 3 = 12]].", "Add 3: [[5x = 15]].", "Divide by 5: [[x = 3]]."]),
 bq("What is the solution set of [[4 − 2x ≤ 3x + 19]]?", ["[[x ≥ −3]]", "[[x ≤ −3]]", "[[x ≥ 3]]", "[[x ≤ 3]]"],  # A1.5.B
    "Subtract [[3x]]: [[4 − 5x ≤ 19]]. Subtract 4: [[−5x ≤ 15]]. Divide by [[−5]] and flip: [[x ≥ −3]].", "÷ by a negative → flip the sign",
    ["Subtract [[3x]]: [[4 − 5x ≤ 19]].", "Subtract 4: [[−5x ≤ 15]].", "Divide by [[−5]] and flip: [[x ≥ −3]]."]),
 bq("[[P = 2l + 2w]]. Which equation is solved for [[w]]?", ["[[w = (P − 2l)/2]]", "[[w = P/2 − 2l]]", "[[w = (P + 2l)/2]]", "[[w = 2P − 2l]]"],  # A1.12.E
    "Subtract [[2l]]: [[P − 2l = 2w]]. Divide everything by 2: [[w = (P − 2l)/2]].", "undo everything around [[w]]; ÷ the whole side",
    ["Subtract [[2l]]: [[P − 2l = 2w]].", "Divide the whole side by 2: [[w = (P − 2l)/2]]."]),
]


def exit_pages(tag):
    """Online exit ticket (general / 504 / IEP), same accommodations as the lesson bell work pages."""
    import json, re
    A, MP = L.A, L.MP
    name = "m3t1-exit-ticket-thu-11-19.html"
    qs = [{k: q[k] for k in ("q", "choices", "why")} | ({"letters": "FGHJ"} if i % 2 else {}) for i, q in enumerate(EXIT)]
    MP.OUT = L.OUT
    MP.page(name, "Topic 1 Exit Ticket · Thu 11/19", "Module 3 · Topic 1 · Thursday 11/19 · Exit Ticket", "Exit Ticket: Show What You Know",
            "Work each question on paper first. Answer all 5, then submit and show your teacher your score.", "quiz", qs)
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

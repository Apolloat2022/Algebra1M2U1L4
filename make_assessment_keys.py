# Answer-key decks for the IEP and Section 504 Topic 1 assessments (data from the Oct 14 make_mod.py keys),
# written as make_pptx.py HTML, converted, then the HTML removed.  Run: python make_assessment_keys.py
import subprocess, sys, pathlib

ROOT = pathlib.Path(__file__).parent
PTS = [1, 1, 2, 1, 2, 1, 1, 2, 2, 2, 2, 2, 1, 1]  # 1 per multiple choice, 2 per written item (value + units/meaning)
WORK = [
 "LinReg with x = years since 2000: a = 1750, b = 40,500.",
 "Not brushing causes cavities. The others are coincidence or reversed.",
 "(1.25 − (−1.50)) ÷ (5 − 4) = 2.75. Profit goes up $2.75 per cookie.",
 "LinReg gives r ≈ 0.04: positive but close to 0, so weak.",
 "x = 0 in March, so b = 950. Each month changes by −77.",
 "LinReg: y ≈ 14.357x + 2.25. At x = 9: ≈ 131.46.",
 "3y = −15x + 45 → y = −5x + 15.",
 "y + 2 = (1/3)(x + 1) → y = (1/3)x + 1/3 − 2.",
 "(240 − 360) ÷ (2 − 0) = −60. Meaning: the water goes down 60 L each minute.",
 "Meaning: after 40 minutes Gracie is 0 miles from home (she is home).",
 "Meaning: she starts 2 2/3 miles from home (school is 2 2/3 mi away).",
 "(1 − 2) ÷ (25 − 10) = −1/15. Meaning: 1/15 mile closer to home each minute.",
 "23.2(−4.2) + 2.5 = −97.44 + 2.5.",
 "Domain = x-values; only whole batches, 0 to 10."]
WRITTEN = {3: "$2.75 per cookie", 5: "y = −77x + 950", 7: "m = −5", 8: "y = (1/3)x − 5/3", 9: "−60 liters per minute",
           10: "(40, 0)", 11: "(0, 2 2/3)", 12: "−1/15 mile per minute"}
MC = {"504": {1: "C. y = 1750x + 40,500", 2: "J. don't brush → cavities", 4: "C. Weak positive", 6: "H. $131.46",
              13: "B. −94.94", 14: "G. {0, 1, 2, …, 10}"},
      "IEP": {1: "B. y = 1750x + 40,500", 2: "C. don't brush → cavities", 4: "B. Weak positive", 6: "B. $131.46",
              13: "B. −94.94", 14: "B. {0, 1, 2, …, 10}"}}
IEP_FRAMES = {3: "Blanks: 2.75 · 1 · 2.75", 5: "Blanks: b = 950 · m = −77", 7: "Blanks: −15x + 45 · −5x + 15 · −5",
              8: "Blanks: −2 · 1/3 · −1", 9: "Blanks: −60 · circle down · 60", 10: "Blanks: 40 · 40 · 0 · home",
              11: "Blanks: 2 2/3 · 2 2/3", 12: "Blanks: −1/15 · 1/15 · circle closer to"}


def deck(kind, label):
    def answer(q):
        a = MC[kind].get(q) or WRITTEN[q]
        return a + (f'<br><span class="muted">{IEP_FRAMES[q]}</span>' if kind == "IEP" and q in IEP_FRAMES else "")
    def slide(body, notes=""):
        return (f'<section class="slide"><div>{body}</div><p class="foot">Topic 1 Assessment · {label} · Answer Key (teacher copy)</p>'
                + (f'<aside class="notes">{notes}</aside>' if notes else "") + "</section>")
    grading = ("Grade with the original scoring: same items and letters as the standard form." if kind == "504" else
               "Grade with Form M: 3 choices per multiple-choice item; written answers are the same as the original.")
    out = [slide(f'<h1>Answer Key</h1><h3>Topic 1 Assessment · {label}</h3>'
                 f'<p>{grading}</p><p>1 point per multiple-choice item, 2 points per written item (1 for the value, 1 for units or meaning). '
                 f'Total: <b>{sum(PTS)} points</b>.</p><p class="warn">Teacher copy. Do not share with students.</p>')]
    for start in (1, 5, 9, 13):
        qs = range(start, min(start + 4, 15))
        rows = "".join(f'<tr><td><b>{q}</b> ({PTS[q-1]} pt)</td><td>{answer(q)}</td><td>{WORK[q-1]}</td></tr>' for q in qs)
        out.append(slide(f'<h2>Questions {qs[0]}–{qs[-1]}</h2><table style="font-size:20px"><tr><th>Q</th><th>Answer</th><th>Work / meaning</th></tr>{rows}</table>'))
    quick = " · ".join(f"{q} {(MC[kind].get(q) or WRITTEN[q]).split('.')[0] if q in MC[kind] else WRITTEN[q]}" for q in range(1, 15))
    out.append(slide(f'<h2>Quick key</h2><p>{quick}</p>'))
    return f'<!doctype html><meta charset="utf-8"><title>Topic 1 Assessment Answer Key · {label}</title><body>' + "".join(out) + "</body>"


for folder, kind, label in [("IEP", "IEP", "IEP Version"), ("Section 504", "504", "Section 504 Version")]:
    src = ROOT / folder / f"Topic1-Assessment-{kind}-ANSWER-KEY.html"
    src.write_text(deck(kind, label), encoding="utf-8")
    subprocess.run([sys.executable, str(ROOT / "make_pptx.py"), f"{folder}/{src.name}"], cwd=ROOT)
    src.unlink()

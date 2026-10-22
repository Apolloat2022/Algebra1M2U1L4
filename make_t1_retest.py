# Module 2 Topic 1 Retest (Retest-Alg1M2T1): three forms of the four Edia retest items (point from point-slope form,
# point-slope to slope-intercept, line from a slope and a point, slope from standard form) plus an answer key.
# Writes assessment/Retest-Alg1M2T1.html (printable), .pdf and .pptx, and the same three for the -ANSWER-KEY.
# PDFs print through headless Edge; the PowerPoints go through make_pptx.py.  Run: python make_t1_retest.py
import pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "assessment"
NAME = "Retest-Alg1M2T1"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
x, y = "<i>x</i>", "<i>y</i>"

# (form, [(question, answer, work)] * 4); questions take F(a, b), a fraction for the target format
FORMS = [
 ("A", lambda F: [
  (f"What is the point of the line given by the point-slope equation {y} − 5 = {F(2, 3)}({x} + 1)? Enter your answer as an ordered pair.",
   "(−1, 5)", "y − y₁ = m(x − x₁): x₁ = −1, y₁ = 5."),
  (f"Rewrite the equation in slope-intercept form. Simplify your answer.<br><b>{y} − 2 = 3({x} − 4)</b>",
   "y = 3x − 10", "y − 2 = 3x − 12 → y = 3x − 10"),
  (f"What is the equation in slope-intercept form of a line with a slope of {F(1, 3)} that passes through the point (−3, 2)?",
   "y = (1/3)x + 3", "2 = (1/3)(−3) + b → 2 = −1 + b → b = 3"),
  (f"What is the slope of the line given by the equation 2{x} + 5{y} = 10?",
   "−2/5", "5y = −2x + 10 → y = (−2/5)x + 2")]),
 ("B", lambda F: [
  (f"What is the point of the line given by the point-slope equation {y} + 2 = {F(5, 4)}({x} − 8)? Enter your answer as an ordered pair.",
   "(8, −2)", "y + 2 = y − (−2): x₁ = 8, y₁ = −2."),
  (f"Rewrite the equation in slope-intercept form. Simplify your answer.<br><b>{y} + 5 = −2({x} − 1)</b>",
   "y = −2x − 3", "y + 5 = −2x + 2 → y = −2x − 3"),
  (f"What is the equation in slope-intercept form of a line with a slope of {F(3, 4)} that passes through the point (4, −1)?",
   "y = (3/4)x − 4", "−1 = (3/4)(4) + b → −1 = 3 + b → b = −4"),
  (f"What is the slope of the line given by the equation 4{x} − 2{y} = 8?",
   "2", "−2y = −4x + 8 → y = 2x − 4")]),
 ("C", lambda F: [
  (f"What is the point of the line given by the point-slope equation {y} − 7 = −{F(1, 2)}({x} + 3)? Enter your answer as an ordered pair.",
   "(−3, 7)", "x + 3 = x − (−3): x₁ = −3, y₁ = 7."),
  (f"Rewrite the equation in slope-intercept form. Simplify your answer.<br><b>{y} − 6 = 5({x} + 2)</b>",
   "y = 5x + 16", "y − 6 = 5x + 10 → y = 5x + 16"),
  (f"What is the equation in slope-intercept form of a line with a slope of −{F(2, 5)} that passes through the point (5, 1)?",
   "y = −(2/5)x + 3", "1 = (−2/5)(5) + b → 1 = −2 + b → b = 3"),
  (f"What is the slope of the line given by the equation 6{x} + 3{y} = 9?",
   "−2", "3y = −6x + 9 → y = −2x + 3")]),
]
TITLE = "Retest · Algebra I Module 2 Topic 1"
DIRS = "Answer each question. Show your work, then write your answer in the box. Write points as ordered pairs (<i>x</i>, <i>y</i>)."

# ---------------------------------------------------------------- printable HTML -> PDF
CSS = """<style>
 @page{size:letter;margin:.6in}
 body{font:15pt/1.45 Calibri,Arial,sans-serif;color:#111;margin:0}
 .page{break-after:page} .page:last-child{break-after:auto}
 h1{font-size:22pt;margin:0} h2{font-size:15pt;margin:2px 0 10px;color:#444;font-weight:normal}
 .hdr{border-bottom:2px solid #222;padding-bottom:6px;margin-bottom:12px}
 .q{display:flex;gap:10px;margin:0 0 16px;break-inside:avoid} .n{font-weight:bold;min-width:24px}
 .q>div{flex:1} .work{height:140px;border:1px solid #bbb;border-radius:6px;margin:8px 0 6px;padding:4px 8px;color:#888;font-size:11pt}
 .ans{border:1.5px solid #222;border-radius:6px;padding:6px 10px;width:60%}
 .fr{display:inline-flex;flex-direction:column;vertical-align:middle;text-align:center;font-size:.85em;line-height:1.1}
 .fr span:first-child{border-bottom:1px solid currentColor;padding:0 2px}
 table{border-collapse:collapse;width:100%;font-size:13pt} td,th{border:1px solid #999;padding:6px 8px;text-align:left;vertical-align:top}
 .key{color:#b00;font-weight:bold;white-space:nowrap} .muted{color:#555}
</style>"""
FH = lambda a, b: f'<span class="fr"><span>{a}</span><span>{b}</span></span>'
head = lambda sub: f'<div class="hdr"><div><h1>{TITLE}</h1><h2>{sub}</h2></div><div>Name ____________________ &nbsp; Date __________</div></div>'


def student_html():
    pages = []
    for form, qs in FORMS:
        items = "".join(f'<div class="q"><span class="n">{n}.</span><div>{q}<div class="work">Show your work here</div>'
                        f'<div class="ans">Answer:</div></div></div>' for n, (q, _, _) in enumerate(qs(FH), 1))
        pages.append(f'<section class="page">{head(f"Form {form} · 4 questions")}<p class="muted">{DIRS}</p>{items}</section>')
    return f'<!doctype html><meta charset="utf-8"><title>{NAME}</title>{CSS}<body>' + "".join(pages) + "</body>"


def key_html():
    rows = "".join(f'<tr><td><b>{form}{n}</b></td><td>{q}</td><td class="key">{a}</td><td>{w}</td></tr>'
                   for form, qs in FORMS for n, (q, a, w) in enumerate(qs(FH), 1))
    return (f'<!doctype html><meta charset="utf-8"><title>{NAME} Answer Key</title>{CSS}<body><section class="page">'
            f'<div class="hdr"><div><h1>{TITLE}</h1><h2>Answer Key · Forms A, B, C (teacher copy)</h2></div></div>'
            '<p class="muted">1 point each. Item 1 matches the original retest item 1 on every form, item 2 matches item 2, and so on.</p>'
            f'<table><tr><th>Item</th><th>Question</th><th>Answer</th><th>Work</th></tr>{rows}</table></section></body>')


# ---------------------------------------------------------------- make_pptx.py decks
FP = lambda a, b: "({{" + f"{a}|{b}" + "}})"  # make_pptx flattens fractions, so keep them in parentheses
slide = lambda body, foot=TITLE: f'<section class="slide">{body}<p class="foot">{foot}</p></section>'


def student_deck():
    out = [slide(f'<h1>{TITLE}</h1><h3>Forms A, B, C</h3><p>Name ____________________ &nbsp; Date __________</p>'
                 f'<div class="card"><p>{DIRS}</p></div>')]
    for form, qs in FORMS:
        out.append(f'<section class="slide divider"><h1>Form {form}</h1></section>')
        out += [slide(f'<h3>Form {form} · Question {n} of 4</h3><div style="font-size:32px"><p>{q}</p>'
                      '<p class="think">Show your work here.</p><p>Answer: ____________________</p></div>', f"{TITLE} · Form {form}")
                for n, (q, _, _) in enumerate(qs(FP), 1)]
    return f'<!doctype html><meta charset="utf-8"><title>{NAME}</title><body>' + "".join(out) + "</body>"


def key_deck():
    out = [slide(f'<h1>Answer Key</h1><h3>{TITLE} · Forms A, B, C</h3><p>1 point per item.</p>'
                 '<p class="warn">Teacher copy. Do not share with students.</p>', f"{TITLE} · Answer Key")]
    for form, qs in FORMS:
        rows = "".join(f'<tr><td><b>{n}</b></td><td>{a}</td><td>{w}</td></tr>' for n, (_, a, w) in enumerate(qs(FP), 1))
        out.append(slide(f'<h2>Form {form}</h2><table style="font-size:24px"><tr><th>Q</th><th>Answer</th><th>Work</th></tr>{rows}</table>',
                         f"{TITLE} · Answer Key"))
    return f'<!doctype html><meta charset="utf-8"><title>{NAME} Answer Key</title><body>' + "".join(out) + "</body>"


if __name__ == "__main__":
    assert all(len(qs(FH)) == 4 for _, qs in FORMS)
    for name, page, deck in [(NAME, student_html(), student_deck()), (f"{NAME}-ANSWER-KEY", key_html(), key_deck())]:
        html = OUT / f"{name}.html"
        html.write_text(page, encoding="utf-8")
        subprocess.run([EDGE, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={OUT / f'{name}.pdf'}", html.as_uri()], check=True, capture_output=True)
        src = OUT / f"{name}-deck.html"
        src.write_text(deck, encoding="utf-8")
        subprocess.run([sys.executable, str(ROOT / "make_pptx.py"), f"assessment/{src.name}"], cwd=ROOT, check=True)
        src.unlink()
        (OUT / f"{name}-deck.pptx").replace(OUT / f"{name}.pptx")

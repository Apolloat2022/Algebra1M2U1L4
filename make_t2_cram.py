# Catch-up day, Mon Oct 26: the starred (essential) parts of Topic 2 Lessons 1.2-1.4 and 2.1-2.3 in one 45-minute class,
# so Lesson 3 can start Tuesday and the test stays on Tue Nov 3. Slides are copied from the Lesson 1 and 2 decks (General,
# IEP, Section 504), so those stay the single source; a plan slide, an exit check and tonight's homework are added.
# Writes t2-catchup-day-lessons1-2[-IEP|-504].html beside each deck, then the .pptx.  Run: python make_t2_cram.py
import re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).parent
DIRS = [ROOT / "Module 2 topic 2", ROOT / "IEP", ROOT / "Section 504"]
SFX = ["", "-IEP", "-504"]
L1, L2 = "t2-lesson1-transforming-linear-functions", "t2-lesson2-vertical-horizontal-transformations"
# slide indexes in the General decks (504 decks hold the same slides, found by title) and in the IEP decks
PICK = {0: {L1: [12, 13, 15, 16, 19], L2: [5, 6, 8, 11, 14]},
        1: {L1: [5, 8, 11, 13], L2: [4, 5, 6, 7, 8, 11]}}
NAME = "t2-catchup-day-lessons1-2"
sections = lambda s: re.findall(r'<section[^>]*>.*?</section>', s, re.S)
title_of = lambda x: re.search(r'<h[123][^>]*>(.*?)</h[123]>', x, re.S).group(1)
mt = lambda s: '<span class="mt">' + re.sub(r"[A-Za-z]", r"<i>\g<0></i>", s) + "</span>"


def sec(eyebrow, h2, body, notes, divider=False):
    return (f'<section class="slide{" divider" if divider else ""}">\n  <p class="eyebrow">{eyebrow}</p>\n  <h2>{h2}</h2>\n  {body}\n'
            f'  <aside class="notes">{notes}</aside>\n</section>\n')


def plan(kind):
    label = ["", " · IEP Version", " · Section 504 Version"][kind]
    items = [("5 min", "Bell work while you take attendance (Lesson 2, Day 1)"),
             ("10 min", "Lesson 1: parallel lines (1.2) and vertical dilations (1.3) ★"),
             ("7 min", f"Lesson 1: both at once, {mt('g(x) = a · f(x) + d')} (1.4) ★"),
             ("15 min", "Lesson 2: horizontal translations and dilations, inside vs. outside (2.1–2.3) ★"),
             ("8 min", "Exit check, then homework")]
    rows = "".join(f'<tr><td style="white-space:nowrap"><b>{t}</b></td><td>{w}</td></tr>' for t, w in items)
    return sec(f"Catch-Up Day · Monday, October 26 · Topic 2 Lessons 1–2{label}", "Today: the essentials of Lessons 1 and 2",
               f'<table class="tbl" style="font-size:26px;margin-top:8px">{rows}</table>'
               '<p style="font-size:22px;margin-top:14px">★ = essential in the 150-day pacing guide. Lesson 3 starts tomorrow; the Topic 2 test is Tuesday, November 3.</p>',
               "Added for the catch-up day; not from the textbook. The class finished Activity 1.1, so this one class covers only the starred "
               "activities left in Lessons 1 and 2. Skip Activity 1.5 and both Talk the Talks; they are not on the test. Keep each part to "
               "its time: show the slide, do one example together, move on. The homework tonight practices the same skills in the test's style.")


def exit_check():
    q = [(f"{mt('f(x) = x')} and {mt('g(x) = 2f(x) − 3')}. Describe the transformations and write {mt('g(x)')}.",
          f"Vertical dilation by 2, then down 3: {mt('g(x) = 2x − 3')}"),
         (f"Write the line parallel to {mt('y = 3x + 1')} through {mt('(2, 4)')}.",
          f"Same slope 3: {mt('4 = 3(2) + b')}, {mt('b = −2')}. {mt('y = 3x − 2')}"),
         (f"{mt('f(x) = x')} and {mt('h(x) = f(x + 4)')}. Which way does the graph move?",
          f"Inside: the opposite way. Left 4, the same as up 4: {mt('h(x) = x + 4')}")]
    body = "".join(f'<div class="card"><p class="small"><b>{k}.</b> {t}</p><div class="step pop ans" style="font-size:20px">{a}</div></div>'
                   for k, (t, a) in enumerate(q, 1))
    return sec("Catch-Up Day · Exit Check", "Show what you know", f'<div class="col" style="gap:12px">{body}</div>',
               "Students answer on paper, then click to reveal each answer. Anyone who misses question 3 needs the inside/outside rule "
               "again tomorrow during bell work.")


def homework(kind):
    s, pre = SFX[kind], ("" if kind == 0 else "../Module%202%20topic%202/")
    link = lambda n: f'<a class="go" href="t2-lesson{n}-homework{s}.html" target="_blank" onclick="event.stopPropagation()">Lesson {n} homework →</a>'
    return sec("Catch-Up Day · Tonight", "Homework: practice for the test",
               f'<p style="font-size:28px">{link(1)} &nbsp; · &nbsp; {link(2)}</p>'
               '<p style="font-size:24px">Questions 11–14 on each are written like the End of Topic 2 Assessment.</p>'
               '<p style="font-size:24px">Tomorrow: Lesson 3, Determining Slopes of Perpendicular Lines.</p>',
               "Both homework pages grade themselves and explain each answer.", divider=True)


def build(kind):
    folder, sfx = DIRS[kind], SFX[kind]
    src = {n: sections((folder / f"{n}{sfx}.html").read_text(encoding="utf-8")) for n in (L1, L2)}
    if kind == 2:  # 504: the general slides, matched by title
        gen = {n: sections((DIRS[0] / f"{n}.html").read_text(encoding="utf-8")) for n in (L1, L2)}
        pick = {n: [[title_of(x) for x in src[n]].index(title_of(gen[n][i])) for i in PICK[0][n]] for n in (L1, L2)}
    else:
        pick = PICK[kind]
    head, rest = (folder / f"{L1}{sfx}.html").read_text(encoding="utf-8").split('<div id="stage">', 1)
    tail = rest.split("\n</div>\n", 1)[1]
    label = ["", " · IEP", " · Section 504"][kind]
    head = re.sub(r"<title>.*?</title>", f"<title>Topic 2 Catch-Up Day: Lessons 1–2{label}</title>", head, count=1)
    bell = src[L2][[title_of(x) for x in src[L2]].index(title_of(src[L2][1]))] if kind == 2 else src[L2][1]  # Lesson 2 Day 1 bell work
    slides = [plan(kind), bell.replace('<p class="eyebrow">', '<p class="eyebrow">Catch-Up · Lesson 2 · ', 1) + "\n"]
    for n, lesson in ((L1, 1), (L2, 2)):
        for i in pick[n]:
            x = re.sub(r'(<p class="eyebrow">)(?:Day \d · )?', rf"\1Catch-Up · Lesson {lesson} · ", src[n][i], count=1)
            slides.append(x + "\n")
    slides += [exit_check(), homework(kind)]
    out = folder / f"{NAME}{sfx}.html"
    out.write_text(head + '<div id="stage">\n' + "".join(slides) + "\n</div>\n" + tail, encoding="utf-8")
    subprocess.run([sys.executable, str(ROOT / "make_pptx.py"), out.relative_to(ROOT).as_posix()], cwd=ROOT, check=False)
    return out.name, len(slides)


if __name__ == "__main__":
    for kind in (0, 1, 2):
        print(*build(kind))

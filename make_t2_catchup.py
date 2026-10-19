# Topic 2 web decks with a Topic 1 Catch-Up: about 15 minutes of Topic 1 Lessons 5-6 at the start of each Topic 2
# lesson day, spread across Lessons 1-4. Slides are copied as-is from the Lesson 5/6 decks (General) and their IEP
# decks (IEP), so the originals stay the single source. Writes *-catchup.html next to each Topic 2 deck.
# Run: python make_t2_catchup.py
import re
from pathlib import Path

ROOT = Path(__file__).parent
T2 = ROOT / "Module 2 topic 2"
IEP = ROOT / "IEP"
SRC = {"L5": (ROOT / "lesson5/using-linear-equations-lesson5.html", IEP / "lesson5-using-linear-equations-IEP.html"),
       "L6": (ROOT / "lesson6/making-sense-of-representations-lesson6.html", IEP / "lesson6-representations-IEP.html")}
NAMES = {1: "t2-lesson1-transforming-linear-functions", 2: "t2-lesson2-vertical-horizontal-transformations",
         3: "t2-lesson3-perpendicular-slopes", 4: "t2-lesson4-comparing-linear-functions"}

# (topic 2 lesson, pacing day, source lesson, general slide indexes, IEP slide indexes, title, why it fits today)
BLOCKS = [
 (1, 1, "L5", [4, 6, 7, 11], [4, 5, 6, 7, 8], "Graphing from slope-intercept form",
  "Today's g(x) = a · f(x) + d is slope-intercept form: a is the slope and d is the y-intercept."),
 (1, 2, "L5", [14, 15], [9], "Graphing from point-slope form",
  "Activity 1.2 writes parallel lines with point-slope form, so practice it first."),
 (1, 3, "L5", [17, 18, 21], [10, 11], "Standard form and intercepts",
  "Graphing with the intercepts is a fast check on the transformed graphs in Activity 1.4."),
 (2, 5, "L5", [26, 28, 30], [12, 13], "Slope and y-intercept from any form",
  "Lesson 2 rewrites f(x − c) in slope-intercept form, so you must read the slope and intercept from any form."),
 (2, 6, "L6", [5, 7, 11], [4, 5, 6, 7], "Linear or nonlinear?",
  "A transformation of a linear function is still linear: the rate of change stays constant."),
 (3, 8, "L6", [14, 15, 16, 17], [8, 9], "Write, evaluate and solve a function in context",
  "Lesson 3 evaluates slopes and points; this practices using function notation in a story."),
 (3, 9, "L6", [18, 19, 20], [10], "Changing the situation changes the function",
  "Giving away 3 T-shirts shifts the function: the same idea as a Topic 2 translation."),
 (4, 10, "L6", [21, 22, 23], [11], "General form and factored form",
  "Lesson 4 compares functions in different forms; general and factored form are two more forms."),
 (4, 11, "L6", [26, 27, 30], [12], "Three ways to write a function; four views",
  "Lesson 4 compares tables, graphs, equations and descriptions: the same four views."),
]
PRACTICE = {"L5": "lesson5", "L6": "lesson6"}

sections = lambda s: re.findall(r'<section[^>]*>.*?</section>', s, re.S)


def go(href, text):
    return f'<a class="go" href="{href}" target="_blank" onclick="event.stopPropagation()">{text}</a>'


def divider(eyebrow, h1, body, notes):
    return (f'<section class="slide divider">\n  <p class="eyebrow">{eyebrow}</p>\n  <h1>{h1}</h1>\n  {body}\n'
            f'  <aside class="notes">{notes}</aside>\n</section>')


def block(src, idx, iep, day, title, why):
    lesson = "Lesson 5" if src == "L5" else "Lesson 6"
    slides = sections(SRC[src][iep].read_text(encoding="utf-8"))
    pre = PRACTICE[src]
    links = (f'{go(f"{pre}-homework-IEP.html", "Homework →")} · {go(f"{pre}-quiz-IEP.html", "Quiz →")}' if iep else
             f'{go(f"../{pre}/{pre}-homework.html", "Homework →")} · {go(f"../{pre}/{pre}-quiz.html", "Quiz →")}')
    out = [divider(f"Topic 1 Catch-Up · Day {day} · about 15 minutes", f"Topic 1 {lesson}: {title}",
                   f'<p style="font-size:30px;max-width:1000px">{why}</p>\n  <p style="font-size:24px">Topic 1 {lesson} practice: {links}</p>',
                   f"Catch-up from Topic 1 {lesson} so the class is ready for the End of Topic 1 Assessment (Lessons 1–6). "
                   "Keep it to about 15 minutes, then go back to the Topic 2 lesson.")]
    for i in idx:
        out.append(re.sub(r'(<p class="eyebrow">)(?:Day \d+ · |Lesson \d · )?', rf'\1Topic 1 Catch-Up · {lesson} · ', slides[i], count=1))
    return out


def back(n):
    return divider(f"Topic 2 · Lesson {n}", "Back to Topic 2", '<p style="font-size:30px">Catch-up done. Now today\'s Topic 2 lesson.</p>',
                   "End of the Topic 1 Catch-Up. Continue with the Topic 2 lesson.")


def build(n, iep):
    path = (IEP / f"{NAMES[n]}-IEP.html") if iep else (T2 / f"{NAMES[n]}.html")
    s = path.read_text(encoding="utf-8")
    secs = sections(s)
    mine = [b for b in BLOCKS if b[0] == n]
    if iep:  # IEP decks put every day's bell work first: one catch-up run after them, one block per day
        last_bell = max(i for i, x in enumerate(secs) if re.search(r'class="eyebrow">[^<]*Bell Work', x))
        add = {last_bell: sum((block(b[2], b[4], True, b[1], b[5], b[6]) for b in mine), []) + [back(n)]}
    else:  # general decks: after each day's bell work slide
        bells = [i for i, x in enumerate(secs) if re.search(r'class="eyebrow">[^<]*Bell Work', x)]
        assert len(bells) == len(mine), (n, bells)
        add = {i: block(b[2], b[3], False, b[1], b[5], b[6]) + [back(n)] for i, b in zip(bells, mine)}
    new = []
    for i, x in enumerate(secs):
        if i == 0:
            x = x.replace("</h1>", '</h1>\n  <p class="warn" style="font-size:22px">This version adds a 15-minute Topic 1 Catch-Up '
                          '(Lessons 5–6) at the start of each day.</p>', 1)
        new += [x] + add.get(i, [])
    head, tail = s[:s.index(secs[0])], s[s.index(secs[-1]) + len(secs[-1]):]
    head = head.replace("</title>", " + Topic 1 Catch-Up</title>", 1)
    out = path.with_name(path.stem + "-catchup.html")
    out.write_text(head + "\n".join(new) + tail, encoding="utf-8")
    return out, len(new)


if __name__ == "__main__":
    for n in NAMES:
        for iep in (False, True):
            print(*build(n, iep))

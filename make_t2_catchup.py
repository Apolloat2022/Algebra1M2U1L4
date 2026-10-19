# Topic 2 web decks with a Topic 1 Catch-Up: about 15 minutes of Topic 1 Lessons 5-6 at the start of each Topic 2
# lesson day, spread across Lessons 1-4. Slides are copied as-is from the Lesson 5/6 decks (General) and their IEP
# and Section 504 decks, so the originals stay the single source. Writes *-catchup.html next to each Topic 2 deck.
# Run: python make_t2_catchup.py
import re
from pathlib import Path

ROOT = Path(__file__).parent
T2 = ROOT / "Module 2 topic 2"
IEP = ROOT / "IEP"
S504 = ROOT / "Section 504"
SRC = {"L5": (ROOT / "lesson5/using-linear-equations-lesson5.html", IEP / "lesson5-using-linear-equations-IEP.html",
              S504 / "lesson5-using-linear-equations-504.html"),
       "L6": (ROOT / "lesson6/making-sense-of-representations-lesson6.html", IEP / "lesson6-representations-IEP.html",
              S504 / "lesson6-representations-504.html")}
NAMES = {1: "t2-lesson1-transforming-linear-functions", 2: "t2-lesson2-vertical-horizontal-transformations",
         3: "t2-lesson3-perpendicular-slopes", 4: "t2-lesson4-comparing-linear-functions"}

# (topic 2 lesson, pacing day, source lesson, general slide indexes (504 uses the same slides, found by title),
#  IEP slide indexes, title, why it fits today)
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
# expected dates on the 150-day calendar (Topic 2 starts Mon Oct 19, 2026)
DATES = {1: "Mon, Oct 19", 2: "Tue, Oct 20", 3: "Wed, Oct 21", 5: "Mon, Oct 26", 6: "Tue, Oct 27", 8: "Thu, Oct 29",
         9: "Mon, Nov 2", 10: "Tue, Nov 3", 11: "Wed, Nov 4"}
small = lambda t: f'<p class="muted" style="font-size:18px">{t}</p>'

sections = lambda s: re.findall(r'<section[^>]*>.*?</section>', s, re.S)


def go(href, text):
    return f'<a class="go" href="{href}" target="_blank" onclick="event.stopPropagation()">{text}</a>'


def divider(eyebrow, h1, body, notes):
    return (f'<section class="slide divider">\n  <p class="eyebrow">{eyebrow}</p>\n  <h1>{h1}</h1>\n  {body}\n'
            f'  <aside class="notes">{notes}</aside>\n</section>')


def title_of(x):
    return re.search(r'<h[123][^>]*>(.*?)</h[123]>', x, re.S).group(1)


def block(src, idx, kind, day, title, why):  # kind: 0 General, 1 IEP, 2 Section 504
    lesson = "Lesson 5" if src == "L5" else "Lesson 6"
    slides = sections(SRC[src][kind].read_text(encoding="utf-8"))
    if kind == 2:  # 504 decks add plan/vocabulary/notes slides, so match the general slides by title
        gen = sections(SRC[src][0].read_text(encoding="utf-8"))
        titles = [title_of(x) for x in slides]
        idx = [titles.index(title_of(gen[i])) for i in idx]
    pre = PRACTICE[src]
    sfx = {1: "-IEP", 2: "-504"}.get(kind)
    links = (f'{go(f"{pre}-homework{sfx}.html", "Homework →")} · {go(f"{pre}-quiz{sfx}.html", "Quiz →")}' if sfx else
             f'{go(f"../{pre}/{pre}-homework.html", "Homework →")} · {go(f"../{pre}/{pre}-quiz.html", "Quiz →")}')
    out = [divider(f"Topic 1 Catch-Up · Day {day} · about 15 minutes", f"Topic 1 {lesson}: {title}",
                   small(f"Expected date: {DATES[day]}") + f'\n  <p style="font-size:30px;max-width:1000px">{why}</p>\n  <p style="font-size:24px">Topic 1 {lesson} practice: {links}</p>',
                   f"Catch-up from Topic 1 {lesson} so the class is ready for the End of Topic 1 Assessment (Lessons 1–6). "
                   "Keep it to about 15 minutes, then go back to the Topic 2 lesson.")]
    for i in idx:
        out.append(re.sub(r'(<p class="eyebrow">)(?:Day \d+ · |Lesson \d · )?', rf'\1Topic 1 Catch-Up · {lesson} · ', slides[i], count=1))
    return out


def back(n):
    return divider(f"Topic 2 · Lesson {n}", "Back to Topic 2", '<p style="font-size:30px">Catch-up done. Now today\'s Topic 2 lesson.</p>',
                   "End of the Topic 1 Catch-Up. Continue with the Topic 2 lesson.")


def build(n, kind):
    path = [T2 / f"{NAMES[n]}.html", IEP / f"{NAMES[n]}-IEP.html", S504 / f"{NAMES[n]}-504.html"][kind]
    s = path.read_text(encoding="utf-8")
    secs = sections(s)
    mine = [b for b in BLOCKS if b[0] == n]
    if kind == 1:  # IEP decks put every day's bell work first: one catch-up run after them, one block per day
        last_bell = max(i for i, x in enumerate(secs) if re.search(r'class="eyebrow">[^<]*Bell Work', x))
        add = {last_bell: sum((block(b[2], b[4], 1, b[1], b[5], b[6]) for b in mine), []) + [back(n)]}
    else:  # General and 504 decks: after each day's bell work slide
        bells = [i for i, x in enumerate(secs) if re.search(r'class="eyebrow">[^<]*Bell Work', x)]
        assert len(bells) == len(mine), (n, bells)
        add = {i: block(b[2], b[3], kind, b[1], b[5], b[6]) + [back(n)] for i, b in zip(bells, mine)}
    days = [b[1] for b in mine]  # lesson day k -> pacing day
    date = lambda k: DATES[days[int(k) - 1]]
    new = []
    for i, x in enumerate(secs):
        if i == 0:
            x = x.replace("</h1>", '</h1>\n  <p class="warn" style="font-size:22px">This version adds a 15-minute Topic 1 Catch-Up '
                          '(Lessons 5–6) at the start of each day.</p>\n  '
                          + small("Expected dates: " + " · ".join(f"Day {k}: {DATES[d]}" for k, d in enumerate(days, 1))), 1)
        # small expected date on each bell work eyebrow and each "Day N" divider
        x = re.sub(r'(<p class="eyebrow">Day (\d) · Bell Work[^<]*)', lambda m: f"{m.group(1)} · {date(m.group(2))}", x, count=1)
        x = re.sub(r'(<section class="slide divider">.*?<h1>Day (\d)</h1>)',
                   lambda m: m.group(1) + "\n  " + small(f"Expected date: {date(m.group(2))}"), x, count=1, flags=re.S)
        new += [x] + add.get(i, [])
    head, tail = s[:s.index(secs[0])], s[s.index(secs[-1]) + len(secs[-1]):]
    head = head.replace("</title>", " + Topic 1 Catch-Up</title>", 1)
    out = path.with_name(path.stem + "-catchup.html")
    out.write_text(head + "\n".join(new) + tail, encoding="utf-8")
    return out, len(new)


if __name__ == "__main__":
    for n in NAMES:
        for kind in (0, 1, 2):
            print(*build(n, kind))

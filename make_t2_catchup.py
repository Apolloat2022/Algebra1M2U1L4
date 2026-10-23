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
    out = [divider(f"Topic 1 Catch-Up · {DATES[day]} · about 15 minutes", f"Topic 1 {lesson}: {title}",
                   f'<p style="font-size:30px;max-width:1000px">{why}</p>\n  <p style="font-size:24px">Topic 1 {lesson} practice: {links}</p>',
                   f"Catch-up from Topic 1 {lesson} so the class is ready for the End of Topic 1 Assessment (Lessons 1–6). "
                   "Keep it to about 15 minutes, then go back to the Topic 2 lesson.")]
    for i in idx:
        out.append(re.sub(r'(<p class="eyebrow">)(?:Day \d+ · |Lesson \d · )?', rf'\1Topic 1 Catch-Up · {lesson} · ', slides[i], count=1))
    return out


def back(n):
    return divider(f"Topic 2 · Lesson {n}", "Back to Topic 2", '<p style="font-size:30px">Catch-up done. Now today\'s Topic 2 lesson.</p>',
                   "End of the Topic 1 Catch-Up. Continue with the Topic 2 lesson.")


LONG = {1: "Monday, October 19", 2: "Tuesday, October 20", 3: "Wednesday, October 21", 5: "Monday, October 26",
        6: "Tuesday, October 27", 8: "Thursday, October 29", 9: "Monday, November 2", 10: "Tuesday, November 3",
        11: "Wednesday, November 4"}
# what the next class is after each lesson's last day (from topic2-pacing-150.html)
AFTER = {3: "Next class: Thursday, October 22. Skills Practice day: Lesson 1 quiz and Topic 1 Lesson 5 homework. "
            "Then Lesson 2 starts Monday, October 26.",
         6: "Next class: Wednesday, October 28. Skills Practice day: Lesson 2 quiz and Topic 1 Lesson 5 quiz. "
            "Then Lesson 3 starts Thursday, October 29.",
         9: "Next class: Tuesday, November 3. Open the Lesson 4 deck.",
         11: "Next class: Thursday, November 5. End of Topic 1 Assessment. Lesson 3 and 4 quizzes go home as homework."}
# IEP decks are not split by day: which content slides belong to each lesson day
IEP_DAYS = {1: [[4, 5, 6, 7], [11, 12, 13, 8], [9, 10, 14]], 2: [[3, 4, 5, 6, 7, 8, 9, 10], [11, 12]],
            3: [[3, 4, 5, 6, 7], [8, 9, 10, 11, 12]], 4: [[3, 4, 5, 6, 7, 8], [9, 10, 11, 12]]}


def start(n, k, total, d, topic, eq=""):
    return divider(f"Topic 2 · Lesson {n} · Day {k} of {total} · Start here", f"Start: {LONG[d]}",
                   f'<p style="font-size:28px">Today: bell work → Topic 1 catch-up ({topic}) → Lesson {n}, Day {k}.</p>' + eq,
                   f"Class starts here on {LONG[d]}.")


def stop(n, k, d, nxt):
    text = AFTER.get(d) or f"Next class: {LONG[nxt]}. Start at the next slide, “Start: {LONG[nxt]}.”"
    return divider(f"Topic 2 · Lesson {n} · End of Day {k}", f"Stop here: {LONG[d]}",
                   f'<p style="font-size:30px;max-width:1000px">{text}</p>', f"Class ends here on {LONG[d]}.")


def build(n, kind):
    path = [T2 / f"{NAMES[n]}.html", IEP / f"{NAMES[n]}-IEP.html", S504 / f"{NAMES[n]}-504.html"][kind]
    s = path.read_text(encoding="utf-8")
    secs = sections(s)
    mine = [b for b in BLOCKS if b[0] == n]
    days = [b[1] for b in mine]  # lesson day k -> pacing day
    ev = lambda x, t: re.search(rf'class="eyebrow">[^<]*{t}', x)
    bells = [i for i, x in enumerate(secs) if ev(x, "Bell Work")]
    assert len(bells) == len(mine), (n, bells)
    for i in bells:  # small expected date on each bell work eyebrow
        secs[i] = re.sub(r'(<p class="eyebrow">Day (\d) · Bell Work[^<]*)',
                         lambda m: f"{m.group(1)} · {DATES[days[int(m.group(2)) - 1]]}", secs[i], count=1)
    catch = [block(b[2], b[4] if kind == 1 else b[3], kind, b[1], b[5], b[6]) + [back(n)] for b in mine]
    title = secs[0].replace("</h1>", '</h1>\n  <p class="warn" style="font-size:22px">Adds a 15-minute Topic 1 Catch-Up '
                            '(Lessons 5–6) each day · ' + " · ".join(f"Day {k}: {DATES[d]}" for k, d in enumerate(days, 1))
                            + '</p>', 1)
    # one list of slides per lesson day, each opening with its bell work
    if kind == 1:  # IEP: every bell work is up front and the lesson is not split by day, so regroup by day
        chunks = [[secs[bells[k]]] + catch[k] + [secs[i] for i in idx] for k, idx in enumerate(IEP_DAYS[n])]
        used = {0, len(secs) - 1, *bells, *sum(IEP_DAYS[n], [])}
        assert used == set(range(len(secs))), (n, set(range(len(secs))) - used)
        tail = [secs[-1]]
        starts = [start(n, k + 1, len(days), d, b[5]) for k, (d, b) in enumerate(zip(days, mine))]
    else:  # General and 504: days are already in order, split at the "Day N" dividers; tail starts at the answered EQ
        divs = [i for i, x in enumerate(secs) if 'class="slide divider"' in x[:40] and re.search(r"<h1>Day \d</h1>", x)]
        end = next(i for i, x in enumerate(secs) if ev(x, "Essential Question · Answered"))
        exit_ = next(i for i, x in enumerate(secs) if ev(x, "Exit Ticket"))
        bounds = [1] + [i + 1 for i in divs] + [end]
        chunks = []
        for k in range(len(days)):
            day = secs[bounds[k]:bounds[k + 1] - (1 if k + 1 < len(days) else 0)]  # drop the next "Day N" divider
            b = day.index(secs[bells[k]])
            chunks.append(day[:b + 1] + catch[k] + day[b + 1:])
        chunks[-1] += secs[end:exit_ + 1]  # the last day ends with the answered EQ and the exit ticket
        tail = secs[exit_ + 1:]
        eqs = [""] + [re.search(r'<p class="step".*?</p>', secs[i], re.S).group(0) for i in divs]
        starts = [start(n, k + 1, len(days), d, b[5], f"\n  {eq}" if eq else "") for k, (d, b, eq) in enumerate(zip(days, mine, eqs))]
    new = [title]
    for k, d in enumerate(days):
        new += [starts[k]] + chunks[k] + [stop(n, k + 1, d, days[k + 1] if k + 1 < len(days) else None)]
    new += tail
    head, tail = s[:s.index(secs[0])], s[s.index(secs[-1]) + len(secs[-1]):]
    head = head.replace("</title>", " + Topic 1 Catch-Up</title>", 1)
    out = path.with_name(path.stem + "-catchup.html")
    out.write_text(head + "\n".join(new) + tail, encoding="utf-8")
    return out, len(new)


if __name__ == "__main__":
    for n in NAMES:
        for kind in (0, 1, 2):
            print(*build(n, kind))

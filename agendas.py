"""Today's Agenda slides: one place for every dated agenda.
- slide(...) builds the agenda slide (same look as the Mon Nov 2 review deck).
- DECKS: lesson decks shown on an agenda day get it as slide 2 (General, IEP and 504 versions).
Run:  python agendas.py   -> inserts/refreshes slide 2 in those decks and rebuilds their .pptx.
make_m3t1_lessons.py calls inject() itself; after rerunning any Module 2 deck generator, rerun this."""
import re, subprocess, sys
from pathlib import Path

import make_t2_decks as D

ROOT = Path(__file__).parent
FIRST = "📚 Walk in, grab your book, take your seat!"
BAR = '<p style="font-size:26px;font-weight:600;margin:0 0 14px;padding:8px 14px;border-radius:10px;background:#eef3fc">'


def slide(eyebrow, h, items, end, color, notes, first=FIRST):
    body = (f'{BAR}{first}</p><div class="col" style="gap:14px;font-size:28px">' + "".join(
        f'<p style="margin:0"><b style="display:inline-block;width:46px;height:46px;line-height:46px;text-align:center;border-radius:50%;background:{color};color:#fff;margin-right:14px">{n}</b>'
        f'<b>{t}</b> · {w}</p>' for n, (t, w) in enumerate(items, 1)) + f'</div><p style="font-size:36px;margin-top:20px;text-align:center"><b>{end}</b></p>')
    return D.sec(eyebrow, h, body, notes).replace('<section class="slide', '<section data-agenda class="slide', 1)


# Test review day routine (every review day from Nov 17 on): one copy, used by every review-day agenda
REVIEW_ITEMS = [("Test Review on EDIA", "Go to your seat and open your Chromebook. Show your work on paper."),
                ("Missed one? Look → Watch → Ask", "Reread it and check your work, watch that lesson’s video, ask a partner, then your teacher."),
                ("Fix it", "Write the number, what went wrong and the right answer. Try it again. Goal: 80% or higher!"),
                ("At home tonight", "Redo only the questions you missed on EDIA. Bring your fix-it list.")]

TUE = dict(eyebrow="📝 Test Day · Topic 2 Test", h="📅 Today’s Agenda · Tuesday, Nov 3",
           items=[("Clear your desk", "Only a pencil stays out."), ("Chromebook ready", "You will enter your answers on it."),
                  ("Calculator + formula sheet", "Get them now."), ("Take the test", "10 questions. Read carefully, check your work.")],
           end="Good luck! You’ve got this! 🍀", color="#b00020", first="🪑 Walk in and take your seat quickly.",
           notes="Leave this up as students walk in. Same for all 6 periods. Retakes Wed Nov 4.")
WED = dict(eyebrow="🔁 Retake Day", h="📅 Today’s Agenda · Wednesday, Nov 4",
           items=[("Retaking? Get set up", "Clear desk, Chromebook ready, calculator + formula sheet."),
                  ("Not retaking? Lesson 4", "Comparing Linear Functions: slides, then the homework on your Chromebook."),
                  ("Quiet room", "Work silently so retakers can focus. Raise your hand for help."),
                  ("Done early?", "Take the Lesson 4 quiz.")],
           end="Second chance, best effort! 💪", color="#1f8a4c",
           notes="Leave this up as students walk in. Same for all 6 periods. Module 3 Topic 1 starts Thu Nov 5.")
THU = dict(eyebrow="🚀 Welcome to Module 3!", h="📅 Today’s Agenda · Thursday, Nov 5",
           items=[("Bell Work", "Four warm-ups. Start as soon as you sit down."),
                  ("Lesson 1: Solving Linear Equations", "Getting Started, then Activities 1.1 and 1.2 (SE pp. 345–350)."),
                  ("Finished early?", "Show your work to your teacher, then help other students."),
                  ("Exit Ticket", "Four questions to show what you learned.")],
           end="New module, fresh start. Let’s go! 🚀", color="#0b6b3a", notes="Leave this up as students walk in. Same for all 6 periods.")

# deck stem (General name) -> agenda; the -IEP / -504 copies get the same slide
DECKS = {"t2-lesson4-comparing-linear-functions": WED, "m3t1-lesson1-solving-linear-equations": THU}
WHERE = {"t2-lesson4-comparing-linear-functions": "Module 2 topic 2", "m3t1-lesson1-solving-linear-equations": "Module 3 topic 1"}


def inject(path):
    """Put the deck's agenda in as slide 2 (replacing an older one). Returns True if the deck has an agenda."""
    path = Path(path)
    a = DECKS.get(re.sub(r"-(IEP|504)$", "", path.stem))
    if not a:
        return False
    s = re.sub(r'<section data-agenda class="slide.*?</section>\n', "", path.read_text(encoding="utf-8"), flags=re.S)
    i = s.index("</section>\n") + len("</section>\n")
    path.write_text(s[:i] + slide(**a) + s[i:], encoding="utf-8")
    return True


def pptx(path):
    r = subprocess.run([sys.executable, str(ROOT / "make_pptx.py"), Path(path).relative_to(ROOT).as_posix()], capture_output=True, text=True)
    print(" ", (r.stdout.strip().splitlines() or ["?"])[-1])


if __name__ == "__main__":
    for stem, folder in WHERE.items():
        for p in (ROOT / folder / f"{stem}.html", ROOT / "IEP" / f"{stem}-IEP.html", ROOT / "Section 504" / f"{stem}-504.html"):
            assert inject(p), p
            print(p.relative_to(ROOT))
            pptx(p)

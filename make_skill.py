"""Package skill/ as a Claude skill zip (upload at claude.ai → Settings → Capabilities → Skills).

The zip gets the current make_pptx.py and make_lesson_key.py, skill/add_answers.py, skill/SKILL.md and
template.html: the Topic 2 Lesson 1 deck cut to a few sample slides.  Run:  python make_skill.py
"""
import re
import zipfile
from pathlib import Path

HERE = Path(__file__).parent
NAME = "bluebonnet-algebra-slides"
DECK = HERE / "Module 2 topic 2" / "t2-lesson1-transforming-linear-functions.html"
KEEP = [0, 1, 4]  # title, bell work, table + graph with steps (section indexes); the first divider is added

src = DECK.read_text(encoding="utf-8")
secs = list(re.finditer(r"<section class=\"slide[^\"]*\">.*?</section>\n*", src, re.S))
divider = next(i for i, m in enumerate(secs) if "divider" in m.group(0)[:40])
keep = [secs[i].group(0) for i in sorted({*KEEP, divider})]
template = src[:secs[0].start()] + "".join(keep) + src[secs[-1].end():]

out = HERE / "skill" / f"{NAME}.zip"
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    z.write(HERE / "skill" / "SKILL.md", f"{NAME}/SKILL.md")
    z.writestr(f"{NAME}/template.html", template)
    for f in ["make_pptx.py", "make_lesson_key.py", "skill/add_answers.py"]:
        z.write(HERE / f, f"{NAME}/scripts/{Path(f).name}")
print(f"wrote {out.relative_to(HERE)}: {len(keep)} template slides")

"""Add red click-to-reveal answers (and slide numbers) to a publisher .pptx.

Run:  python add_answers.py Lesson.pptx answers.json [out.pptx]

answers.json:
{
  "answers": {"7": [[x, y, w, h, size, "text"], [x, y, w, h, size, "text", "with"]], ...},
  "notes": {"7": "teacher note added to the slide's speaker notes"},
  "corrections": ["Teacher Edition notes for this deck", "Slide 12: the TE answer ... is wrong; ..."],
  "after": 39
}
Boxes sit on a 1920 x 1080 grid over the slide; size is in points. Extra fields: "with" shows the
box on the same click as the box before it, "center" centers its text. "corrections" (optional) adds
a slide after slide "after"; its first line is the heading. Standard library only.
"""
import json
import sys
from pathlib import Path

import make_lesson_key as mk

src = Path(sys.argv[1])
spec = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
out = Path(sys.argv[3]) if len(sys.argv) > 3 else src.with_name(src.stem + "_with_answers.pptx")
ans = {int(k): [tuple(b) for b in v] for k, v in spec["answers"].items()}
notes = {int(k): v for k, v in spec.get("notes", {}).items()}
corr = [(t, None) for t in spec.get("corrections") or []]
mk.annotate(src, out, ans, notes, corr, spec.get("after", 1))

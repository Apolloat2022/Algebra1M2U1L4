"""Build archive.html: every deployable class material, grouped by folder, for reuse next year.
Rerun after adding materials:  python make_archive.py
Source of truth = git (tracked + new-but-not-ignored files), so every link is something that deploys."""
import html, subprocess
from collections import defaultdict
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).parent
EXTS = {".html": "Page", ".pdf": "PDF", ".pptx": "PowerPoint", ".mp4": "Video"}
SKIP_TOP = {"graft", "api", "skill", "materials"}
SKIP_FILES = {"index.html", "teacher.html", "archive.html", "archive-module2.html"}

files = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard"],
                       cwd=ROOT, capture_output=True, text=True, check=True).stdout.splitlines()
TOPICS = ["Module 3 · Topic 1", "Module 2 · Topic 2", "Module 2 · Topic 1"]
CATS = ["Lesson slides", "Videos", "Bell work", "Exit tickets", "Homework & quizzes", "Lesson plans", "Reviews & tests", "Publisher slides", "Posters"]
VERS = {"General": 0, "IEP": 1, "504": 2}

def topic(p):
    s, n = p.as_posix().lower(), p.name.lower()
    if s.startswith("module 3 topic 1") or n.startswith("m3t1-"):
        return TOPICS[0]
    if s.startswith(("module 2 topic 2", "assessment/m2 topic 2")) or n.startswith(("t2-", "topic2-")):
        return TOPICS[1]
    return TOPICS[2]  # lesson4-6 folders, Topic 1 tests and retests

def cat(p):
    s, n = p.as_posix().lower(), p.name.lower()
    if "lesson plan" in s: return "Lesson plans"
    if p.suffix.lower() == ".mp4": return "Videos"
    if "bell" in n: return "Bell work"
    if "exit" in n: return "Exit tickets"
    if "homework" in n or "quiz" in n or "edia" in n: return "Homework & quizzes"
    if any(k in s for k in ("assessment", "review", "retake", "retest")): return "Reviews & tests"
    if n.startswith("blmathematics"): return "Publisher slides"
    if "poster" in n: return "Posters"
    return "Lesson slides"

def ver(p):
    s = p.as_posix()
    return "IEP" if "IEP" in s else "504" if "504" in s else "General"

paths = [Path(f) for f in files]
kept = {p.as_posix() for p in paths}
groups = defaultdict(lambda: defaultdict(list))
dupes = 0
for p in paths:
    f = p.as_posix()
    if p.suffix.lower() not in EXTS or p.parts[0] in SKIP_TOP or f in SKIP_FILES or not (ROOT / f).exists():
        continue
    if p.suffix.lower() == ".html" and p.with_suffix(".pdf").as_posix() in kept and "<script" not in (ROOT / f).read_text(encoding="utf-8", errors="ignore"):  # the HTML a PDF was printed from: list the PDF only
        dupes += 1
        continue
    groups[topic(p)][cat(p)].append(p)

sections = []
for t in TOPICS:
    if t not in groups:
        continue
    blocks = []
    for c in CATS:
        ps = sorted(groups[t].get(c, []), key=lambda p: (VERS[ver(p)], p.name.lower()))
        if not ps:
            continue
        items = "".join(
            f'<li><a href="{quote(p.as_posix())}">{html.escape(p.stem)}</a> <span class="t">{EXTS[p.suffix.lower()]}</span>'
            f'{"" if ver(p) == "General" else f" <span class=v>{ver(p)}</span>"}</li>' for p in ps)
        blocks.append(f'<section><h3>{c} <span class="n">{len(ps)}</span></h3><ul>{items}</ul></section>')
    n = sum(map(len, groups[t].values()))
    sections.append(f'<details open><summary><h2>{t} <span class="n">{n} files</span></h2></summary>{"".join(blocks)}</details>')

total = sum(len(v) for g in groups.values() for v in g.values())
(ROOT / "archive.html").write_text(f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Materials Archive</title>
<style>
:root{{--bg:#fff;--fg:#1a1a1a;--mute:#666;--line:#ddd;--acc:#3050b8}}
@media (prefers-color-scheme:dark){{:root{{--bg:#15171c;--fg:#e8e8e8;--mute:#9a9a9a;--line:#333;--acc:#8aa4ff}}}}
body{{background:var(--bg);color:var(--fg);font:15px/1.45 Segoe UI,Arial,sans-serif;margin:0 auto;max-width:960px;padding:16px}}
a{{color:var(--acc)}} h1{{margin:4px 0}} .sub{{color:var(--mute);margin:0 0 12px}}
input{{width:100%;box-sizing:border-box;padding:9px 12px;font:inherit;border:1px solid var(--line);border-radius:8px;background:var(--bg);color:var(--fg)}}
summary{{cursor:pointer;border-bottom:2px solid var(--line);margin-top:22px}} summary h2{{display:inline;font-size:20px}}
h3{{font-size:15px;margin:14px 0 4px}} .v{{font-size:11px;font-weight:600;padding:0 5px;border-radius:4px;background:var(--acc);color:var(--bg)}}
ul{{columns:2 320px;margin:0;padding-left:18px}} li{{break-inside:avoid;margin:2px 0}}
.t,.n{{color:var(--mute);font-size:12px}}
</style></head><body>
<p class="sub"><a href="teacher.html">← Teacher page</a> · <a href="index.html">Student home</a></p>
<h1>Algebra I Materials Archive</h1>
<p class="sub">{total} files from 2026–27, grouped by topic and type, to reuse next year. Tags mark IEP and 504 versions.</p>
<p><strong><a href="archive-module2.html">Module 2 teacher page (Topics 1–2, organized by lesson and day) →</a></strong></p>
<p class="sub">Rebuild with <code>python make_archive.py</code>.</p>
<input id="q" type="search" placeholder="Filter, e.g. lesson3, quiz, IEP, answer key" aria-label="Filter materials">
{''.join(sections)}
<script>
q.oninput=()=>{{const s=q.value.toLowerCase();document.querySelectorAll('details').forEach(d=>d.open=true);document.querySelectorAll('section').forEach(sec=>{{let n=0;
sec.querySelectorAll('li').forEach(li=>{{const ok=li.textContent.toLowerCase().includes(s);li.hidden=!ok;n+=ok}});sec.hidden=!n}})}};
</script>
</body></html>
""", encoding="utf-8")
print(f"archive.html: {total} files in {len(groups)} topics ({dupes} duplicate HTML sources hidden)")

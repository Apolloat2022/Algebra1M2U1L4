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
SKIP_FILES = {"index.html", "teacher.html", "archive.html"}

files = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard"],
                       cwd=ROOT, capture_output=True, text=True, check=True).stdout.splitlines()
groups = defaultdict(list)
for f in files:
    p = Path(f)
    if p.suffix.lower() in EXTS and p.parts[0] not in SKIP_TOP and f not in SKIP_FILES and (ROOT / f).exists():
        groups[str(p.parent).replace("\\", "/")].append(p)

def order(d):  # Module folders first (in course order), then the rest
    return (not d.lower().startswith("module"), d.lower())

sections = []
for d in sorted(groups, key=order):
    items = "".join(
        f'<li><a href="{quote(p.as_posix())}">{html.escape(p.stem)}</a> <span class="t">{EXTS[p.suffix.lower()]}</span></li>'
        for p in sorted(groups[d], key=lambda p: p.name.lower()))
    title = "Top level" if d == "." else d
    sections.append(f'<section><h2>{html.escape(title)} <span class="n">{len(groups[d])}</span></h2><ul>{items}</ul></section>')

total = sum(map(len, groups.values()))
(ROOT / "archive.html").write_text(f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Materials Archive</title>
<style>
:root{{--bg:#fff;--fg:#1a1a1a;--mute:#666;--line:#ddd;--acc:#3050b8}}
@media (prefers-color-scheme:dark){{:root{{--bg:#15171c;--fg:#e8e8e8;--mute:#9a9a9a;--line:#333;--acc:#8aa4ff}}}}
body{{background:var(--bg);color:var(--fg);font:15px/1.45 Segoe UI,Arial,sans-serif;margin:0 auto;max-width:960px;padding:16px}}
a{{color:var(--acc)}} h1{{margin:4px 0}} .sub{{color:var(--mute);margin:0 0 12px}}
input{{width:100%;box-sizing:border-box;padding:9px 12px;font:inherit;border:1px solid var(--line);border-radius:8px;background:var(--bg);color:var(--fg)}}
h2{{font-size:17px;border-bottom:1px solid var(--line);padding-bottom:4px;margin:22px 0 6px}}
ul{{columns:2 320px;margin:0;padding-left:18px}} li{{break-inside:avoid;margin:2px 0}}
.t,.n{{color:var(--mute);font-size:12px}}
</style></head><body>
<p class="sub"><a href="teacher.html">← Teacher page</a> · <a href="index.html">Student home</a></p>
<h1>Algebra I Materials Archive</h1>
<p class="sub">{total} files from 2026–27, grouped by folder, to reuse next year. Rebuild with <code>python make_archive.py</code>.</p>
<input id="q" type="search" placeholder="Filter, e.g. lesson3, quiz, IEP, answer key" aria-label="Filter materials">
{''.join(sections)}
<script>
q.oninput=()=>{{const s=q.value.toLowerCase();document.querySelectorAll('section').forEach(sec=>{{let n=0;
sec.querySelectorAll('li').forEach(li=>{{const ok=li.textContent.toLowerCase().includes(s);li.hidden=!ok;n+=ok}});sec.hidden=!n}})}};
</script>
</body></html>
""", encoding="utf-8")
print(f"archive.html: {total} files in {len(groups)} folders")

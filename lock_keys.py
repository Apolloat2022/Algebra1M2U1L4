"""Password-lock every deployed answer key (and other answer-bearing teacher PDFs) that is still open.
Two passwords, both from the environment so they never land in the repo:
  DAILY_PW  bell work, exit tickets, whiteboard/board work, teaching scripts and plans
  KEYS_PW   everything else: test, review and how-to-solve keys, AI Tutor files
Run before committing new keys:   $env:DAILY_PW = '...'; $env:KEYS_PW = '...'; python lock_keys.py
Already-locked PDFs are skipped. The Game Plan book has its own password (make_game_plan.py)."""
import os, re, subprocess, sys
from pathlib import Path
import fitz

ROOT = Path(__file__).parent
KEYISH = re.compile(r"ANSWER-KEY|Teacher-Key|How-To-Solve|AI-Tutor|Teaching-Script|Teacher-Plan", re.I)
DAILY = re.compile(r"BELL WORK/|EXIT TICKET/|Bell-Work|Bell-Whiteboard|Board-Work|Exit-Ticket|Teaching-Script|Teacher-Plan", re.I)


def password(path, daily, keys):
    return daily if DAILY.search(path) else keys


def main():
    daily, keys = os.environ.get("DAILY_PW"), os.environ.get("KEYS_PW")
    if not (daily and keys):
        sys.exit("set DAILY_PW and KEYS_PW first")
    files = subprocess.run(["git", "ls-files", "*.pdf"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.splitlines()
    n = 0
    for f in files:
        p = ROOT / f
        if f.startswith("Game Plan/") or not KEYISH.search(p.name):
            continue
        d = fitz.open(p)
        if d.needs_pass:
            continue
        pw = password(f, daily, keys)
        tmp = p.with_suffix(".tmp.pdf")
        d.save(tmp, encryption=fitz.PDF_ENCRYPT_AES_256, user_pw=pw, owner_pw=pw)
        d.close(); tmp.replace(p)
        assert fitz.open(p).needs_pass, f
        n += 1; print("locked", f)
    print(n, "locked")


if __name__ == "__main__":
    assert password("Module 3 topic 1/BELL WORK/T1-Bell-Work-Mon-11-16-ANSWER-KEY.pdf", "d", "k") == "d"
    assert password("Module 3 topic 1/EXIT TICKET/T1-Exit-Ticket-Mon-11-16-ANSWER-KEY.pdf", "d", "k") == "d"
    assert password("Module 3 topic 1/LESSON PLANS/M3T1-Lesson1-Teaching-Script.pdf", "d", "k") == "d"
    assert password("assessment/M3 TOPIC 1/M3T1-End-of-Topic-ANSWER-KEY-DETAILED.pdf", "d", "k") == "k"
    assert password("Module 3 topic 1/REVIEW/T1-Review-ANSWER-KEY.pdf", "d", "k") == "k"
    main()

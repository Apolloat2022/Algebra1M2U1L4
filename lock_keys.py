"""Password-lock every deployed answer key (and other answer-bearing teacher PDFs) that is still open.
Run before committing new keys:   $env:KEYS_PW = '...'; python lock_keys.py
The password comes from KEYS_PW so it never lands in the repo. Already-locked PDFs are skipped."""
import os, re, subprocess, sys
from pathlib import Path
import fitz

ROOT = Path(__file__).parent
# answer keys, worked solutions, and the IEP AI-tutor file (it carries answers)
KEYISH = re.compile(r"ANSWER-KEY|Teacher-Key|How-To-Solve|AI-Tutor", re.I)

def main():
    pw = os.environ.get("KEYS_PW") or sys.exit("set KEYS_PW first")
    files = subprocess.run(["git", "ls-files", "*.pdf"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.splitlines()
    n = 0
    for f in files:
        p = ROOT / f
        if not KEYISH.search(p.name):
            continue
        d = fitz.open(p)
        if d.needs_pass:
            continue
        tmp = p.with_suffix(".tmp.pdf")
        d.save(tmp, encryption=fitz.PDF_ENCRYPT_AES_256, user_pw=pw, owner_pw=pw)
        d.close(); tmp.replace(p)
        assert fitz.open(p).needs_pass, f
        n += 1; print("locked", f)
    print(n, "locked")

if __name__ == "__main__":
    main()

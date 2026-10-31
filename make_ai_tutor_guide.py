# MagicSchool AI Tutor guide for Module 2 Topic 2, Lessons 1-3.
# Makes a printable student handout (PDF) and one narrated, captioned video for IEP/504 students.
# Slides and the handout print through headless Edge; narration is edge-tts; ffmpeg stitches the video.
# Run: python make_ai_tutor_guide.py
import asyncio, html, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import edge_tts

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
OUT = Path(__file__).parent / "Module 2 topic 2" / "LESSON PLANS"
VOICE, RATE = "en-US-AriaNeural", "-12%"  # slower than default on purpose: processing time
W, H = 1280, 720

LESSONS = [
    ("Lesson 1 · Transforming Linear Functions", [
        "If f(x) = x and g(x) = 3·f(x), what happens to the graph? Show me with a table.",
        "What's the difference between g(x) = 2f(x) and g(x) = f(2x) when f(x) = x?",
        "How do I find the value of a in m(x) = a·f(x) from a graph?",
        "When does multiplying by a make a line steeper or flatter? What if a is negative?",
        "Let f(x) = x + 2. Are 3f(x) and f(3x) the same function? Go step by step.",
    ]),
    ("Lesson 2 · Vertical and Horizontal Transformations", [
        "Why does f(x − 2) move the graph right and not left?",
        "What's the difference between f(x) + 4 and f(x + 4)?",
        "Here's a table for f(x). How do I shift it 2 units right and find the new y-intercept?",
        "Does a horizontal translation change the x-values or the y-values in a table?",
        "A food truck charges $50 plus $12 per hour, for at most 8 hours. How do I find the domain and range?",
    ]),
    ("Lesson 3 · Slopes of Perpendicular Lines", [
        "How do I find the slope of a line perpendicular to y = (3/4)x − 2?",
        "What does \"negative reciprocal\" mean? Give me 3 examples to try.",
        "How do I write the equation of a line through (4, 0) that's parallel to y = −1.5x + 2.4?",
        "A line crosses the x-axis at 6. What point is that, and how do I use it in an equation?",
        "How do I write point-slope form from a graph?",
        "Why is the slope of x = 5 undefined, but the slope of y = 5 is zero?",
        "How can I tell if two lines are parallel, perpendicular, or neither?",
    ]),
]
HELPERS = [
    "Explain it in shorter steps.",
    "Use simpler words, please.",
    "Show me an example first, then let me try one.",
    "Give me a hint, not the answer.",
    "Check my work: [type your steps].",
]

# ---------- handout ----------
CSS = """
@page { size: letter; margin: 0.5in 0.6in; }
body { font-family: Arial, Helvetica, sans-serif; font-size: 12.5pt; line-height: 1.35; color: #111; background: #fff; margin: 0; }
h1 { font-size: 20pt; margin: 0 0 2px; } .sub { margin: 0 0 10px; font-size: 11pt; }
.name { margin: 4px 0 10px; } h2 { font-size: 14pt; margin: 12px 0 4px; padding: 3px 8px; background: #e8eefb; border-left: 5px solid #2f6fdd; }
ol, ul { margin: 2px 0 4px; padding-left: 26px; } li { margin: 2px 0; }
.box { border: 2px solid #111; border-radius: 6px; padding: 6px 12px; margin: 8px 0; }
.q li { list-style: none; position: relative; } .q li::before { content: "☐"; position: absolute; left: -22px; }
.say { font-weight: bold; } .pb { break-before: page; }
.line { border-bottom: 1px solid #555; height: 24px; }
"""

def handout():
    def qlist(qs): return '<ul class="q">' + "".join(f"<li>{html.escape(q)}</li>" for q in qs) + "</ul>"
    body = f"""
<h1>Using the MagicSchool AI Tutor</h1>
<p class="sub">Algebra I · Module 2, Topic 2 · Lessons 1–3 · Use this to study for the Topic 2 Test</p>
<p class="name">Name ______________________________ &nbsp; Period ______ &nbsp; Date __________</p>
<div class="box"><b>How to use it</b>
<ol><li>Open the MagicSchool link your teacher posted in Schoology.</li>
<li>Pick <b>one</b> question below. Type it in, or copy and paste it.</li>
<li>Read the answer. If it's confusing, use a <b>Helper phrase</b>.</li>
<li>Try a problem yourself, then ask the tutor to check your work.</li>
<li>Check the box ☐ next to each question you finish.</li></ol></div>
<div class="box"><b>Helper phrases</b> (type these any time)
<ul>{"".join(f'<li class="say">“{html.escape(h)}”</li>' for h in HELPERS)}</ul></div>
<h2>{LESSONS[0][0]}</h2>{qlist(LESSONS[0][1])}
<h2>{LESSONS[1][0]}</h2>{qlist(LESSONS[1][1])}
<h2 class="pb">{LESSONS[2][0]}</h2>{qlist(LESSONS[2][1])}
<h2>Review: all three lessons</h2>
<ul class="q"><li>“Quiz me with 5 questions like the Topic 2 test. Give me one at a time and wait for my answer before you explain.”</li>
<li>“I got this one wrong: [paste the problem]. Don't give me the answer. Give me a hint first.”</li></ul>
<div class="box"><b>Remember</b>
<ul><li>The tutor helps you <b>think</b>. It is not for copying answers.</li>
<li>One question at a time. Take a break when you need one.</li>
<li>Still stuck? Write your question down and bring it to class.</li></ul></div>
<p><b>One thing I learned:</b></p><div class="line"></div><div class="line"></div>
<p><b>One question I still have:</b></p><div class="line"></div><div class="line"></div>
"""
    src = OUT / "M2T2-AI-Tutor-Questions.html"
    src.write_text(f"<!doctype html><meta charset='utf-8'><title>AI Tutor Questions</title><style>{CSS}</style>{body}", encoding="utf-8")
    pdf = OUT / "M2T2-AI-Tutor-Questions.pdf"
    subprocess.run([EDGE, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf}", src.as_uri()], check=True, capture_output=True)
    src.unlink()
    return pdf

# ---------- video ----------
# Each slide: (title, bullet lines, [(caption, spoken)]). Caption is what's shown; spoken is how TTS should say it.
def f_(s):  # make math read aloud naturally
    for a, b in [("f(x − 2)", "f of x minus 2"), ("f(x + 4)", "f of x plus 4"), ("f(x) + 4", "f of x, plus 4"),
                 ("3·f(x)", "3 times f of x"), ("f(2x)", "f of 2x"), ("2f(x)", "2 times f of x"), ("f(x)", "f of x"),
                 ("g(x)", "g of x"), ("(3/4)x − 2", "three fourths x, minus 2"), ("x = 5", "x equals 5"), ("y = 5", "y equals 5"),
                 ("(4, 0)", "the point 4 comma 0"), ("−1.5x + 2.4", "negative 1 point 5 x, plus 2 point 4"), ("−", "minus")]:
        s = s.replace(a, b)
    return s

SLIDES = [
    ("Using the AI Tutor", ["Algebra I · Module 2, Topic 2", "Lessons 1, 2, and 3"],
     ["Hi! This video shows you how to use the MagicSchool AI Tutor to study for the Topic 2 test.",
      "Grab your handout. It has every question in this video.",
      "You can pause this video any time, and watch it again as many times as you want."]),
    ("What the AI Tutor is for", ["✔ Explains ideas", "✔ Gives hints", "✔ Checks your work", "✘ Not for copying answers"],
     ["The AI tutor is like a helper who is always ready.",
      "It can explain an idea, give you a hint, or check your work.",
      "It is not for copying answers. The goal is for you to understand the math."]),
    ("How to use it: 4 steps", ["1. Open the link in Schoology", "2. Pick ONE question", "3. Read the answer", "4. Try one yourself"],
     ["Step 1. Open the MagicSchool link your teacher posted in Schoology.",
      "Step 2. Pick one question from your handout. Type it in, or copy and paste it.",
      "Step 3. Read the answer slowly.",
      "Step 4. Try a problem yourself, and ask the tutor to check it.",
      "Then check the box on your handout."]),
    ("Helper phrases", [f"“{h}”" for h in HELPERS],
     ["If an answer is too long or confusing, that's okay. Use a helper phrase.",
      "Type: Explain it in shorter steps. Or: Use simpler words, please.",
      "You can ask for an example first, or ask for a hint instead of the answer.",
      "The tutor will try again, as many times as you need."]),
    (LESSONS[0][0], LESSONS[0][1][:3],
     ["Lesson 1 is about transforming linear functions, like multiplying f of x by a number.",
      "Try asking: " + LESSONS[0][1][0],
      "Or ask: " + LESSONS[0][1][1],
      "This one is tricky, so ask the tutor to show both graphs."]),
    (LESSONS[1][0], LESSONS[1][1][:3],
     ["Lesson 2 is about sliding a graph up, down, left, or right.",
      "Try asking: " + LESSONS[1][1][0],
      "Or ask: " + LESSONS[1][1][1],
      "Remember: a change inside the parentheses moves the graph left or right."]),
    (LESSONS[2][0], [LESSONS[2][1][0], LESSONS[2][1][1], LESSONS[2][1][5]],
     ["Lesson 3 is about parallel and perpendicular lines.",
      "Try asking: " + LESSONS[2][1][0],
      "Or ask: What does negative reciprocal mean? Give me 3 examples to try.",
      "You can also ask: " + LESSONS[2][1][5]]),
    ("Quiz yourself", ["“Quiz me with 5 questions like the Topic 2 test.", "Give me one at a time and wait for my answer.”"],
     ["When you're ready, let the tutor quiz you.",
      "Type: Quiz me with 5 questions like the Topic 2 test. Give me one at a time and wait for my answer.",
      "Take your time on each one. There is no timer."]),
    ("Got one wrong?", ["“I got this one wrong: [paste it].", "Don't give me the answer.", "Give me a hint first.”"],
     ["Getting a problem wrong is part of learning.",
      "Paste the problem and type: Don't give me the answer. Give me a hint first.",
      "Then try again with the hint."]),
    ("You've got this!", ["☐ One question at a time", "☐ Take breaks", "☐ Write down what you learned", "☐ Bring questions to class"],
     ["Remember: one question at a time, and take a break when you need one.",
      "At the end, write one thing you learned and one question you still have.",
      "Bring your questions to class. You've got this!"]),
]

SLIDE_CSS = f"""
html,body{{margin:0;width:{W}px;height:{H}px;overflow:hidden;background:#fffdf6;font-family:Arial,Helvetica,sans-serif;color:#111}}
.t{{background:#2f6fdd;color:#fff;font-size:44px;font-weight:bold;padding:26px 50px}}
ul{{list-style:none;margin:30px 50px;padding:0}} li{{font-size:34px;line-height:1.3;margin:0 0 18px}}
.n{{position:absolute;right:30px;top:32px;color:#fff;font-size:22px}}
"""

def shoot(html_text, png):
    src = png.with_suffix(".html")
    src.write_text(html_text, encoding="utf-8")
    subprocess.run([EDGE, "--headless", "--disable-gpu", "--hide-scrollbars", f"--window-size={W},{H}",
                    f"--screenshot={png}", src.as_uri()], check=True, capture_output=True)

def wrap(draw, text, font, width):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= width: cur = t
        else: lines.append(cur); cur = w
    return lines + [cur]

def caption(base, text, out):  # big high-contrast caption bar along the bottom
    img = Image.open(base).convert("RGB").resize((W, H))
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype("arialbd.ttf", 30)
    lines = wrap(d, text, font, W - 120)
    bh = 24 + 40 * len(lines)
    d.rectangle([0, H - bh, W, H], fill="#111")
    for i, ln in enumerate(lines):
        d.text((W // 2, H - bh + 14 + 40 * i), ln, font=font, fill="#ffef5a", anchor="ma")
    img.save(out)

def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True, check=True).stdout)

def srt_time(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

async def video():
    tmp = Path(tempfile.mkdtemp())
    segs, srt, t = [], [], 0.0
    for si, (title, bullets, lines) in enumerate(SLIDES):
        base = tmp / f"s{si}.png"
        shoot(f"<!doctype html><meta charset='utf-8'><style>{SLIDE_CSS}</style><div class='t'>{html.escape(title)}"
              f"<span class='n'>{si + 1} / {len(SLIDES)}</span></div><ul>"
              + "".join(f"<li>{html.escape(b)}</li>" for b in bullets) + "</ul>", base)
        for li, text in enumerate(lines):
            png, mp3, mp4 = tmp / f"s{si}_{li}.png", tmp / f"s{si}_{li}.mp3", tmp / f"s{si}_{li}.mp4"
            caption(base, text, png)
            await edge_tts.Communicate(f_(text), VOICE, rate=RATE).save(str(mp3))
            d = dur(mp3) + (1.6 if li == len(lines) - 1 else 0.8)  # pauses between sentences and slides
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", png, "-i", mp3, "-af", "apad", "-t", f"{d:.2f}",
                            "-r", "24", "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p",
                            "-c:a", "aac", "-ar", "44100", "-ac", "2", mp4], check=True)
            segs.append(mp4)
            srt.append(f"{len(srt) + 1}\n{srt_time(t)} --> {srt_time(t + d - 0.3)}\n{text}\n")
            t += d
    (tmp / "list.txt").write_text("".join(f"file '{p.as_posix()}'\n" for p in segs))
    mp4 = OUT / "M2T2-AI-Tutor-Video-IEP-504.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", tmp / "list.txt", "-c", "copy",
                    "-movflags", "+faststart", mp4], check=True)
    (OUT / "M2T2-AI-Tutor-Video-IEP-504.srt").write_text("\n".join(srt), encoding="utf-8")
    return mp4, t

if __name__ == "__main__":
    print(handout())
    mp4, t = asyncio.run(video())
    print(mp4, f"{t / 60:.1f} min")

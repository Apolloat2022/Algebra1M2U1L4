"""Narrated explainer video for Module 2 Topic 2 Lesson 1 (vertical translations, dilations, reflections).
Draws frames with Pillow, speaks each caption with the Windows narrator (System.Speech), joins them with ffmpeg.
Run:  python make_t2_video.py      ->  Module 2 topic 2/videos/T2-Lesson1-Transformations.mp4"""
import os, re, subprocess, tempfile, wave
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1280, 720, 24
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Module 2 topic 2", "videos", "T2-Lesson1-Transformations.mp4")
VOICE, RATE = "Microsoft Zira Desktop", -1
FONT = "C:/Windows/Fonts/calibri.ttf"
BOLD = "C:/Windows/Fonts/calibrib.ttf"
F = {s: ImageFont.truetype(FONT, s) for s in (18, 26, 30, 34)}
FB = {s: ImageFont.truetype(BOLD, s) for s in (26, 34, 44, 60)}
INK, GRID, AX, BLUE, RED, GREEN, MUTED = "#1d2433", "#e3e7ee", "#5b6478", "#2563eb", "#dc2626", "#15803d", "#6b7280"

# graph: x and y from -10 to 10 in a square on the left
GX, GY, GS, R = 50, 30, 570, 10
def px(x, y): return GX + (x + R) / (2 * R) * GS, GY + (R - y) / (2 * R) * GS

# Each scene: title, points to track, starting (a, d) of g(x) = a·f(x) + d (None: no g yet), and steps.
# A step: (caption, spoken text or None, new (a, d) or None, panel line or None). "PAUSE n" in the caption = n s of quiet.
SCENES = [
    dict(kind="title", title="Transforming Linear Functions", sub="Module 2 · Topic 2 · Lesson 1",
         steps=[("Today: what adding, multiplying, and a negative sign do to the graph of f(x) = x.", None, None, None)]),
    dict(title="The parent function", pts=[-4, 2, 6], g=None, steps=[
        ("This is f(x) = x.", None, None, "f(x) = x"),
        ("Every output equals its input: (2, 2), (6, 6), (−4, −4).", "Every output equals its input. 2 goes to 2, 6 goes to 6, negative 4 goes to negative 4.", None, None),
        ("Its slope is 1 and its y-intercept is (0, 0).", "Its slope is 1, and its y-intercept is the origin, 0 comma 0.", None, "slope 1, y-intercept (0, 0)"),
    ]),
    dict(title="Add: f(x) + 8", pts=[-4, 2, 6], g=(1, 0), steps=[
        ("Now add 8 to every output: k(x) = f(x) + 8.", None, None, "k(x) = f(x) + 8"),
        ("Watch: every point moves up 8 units.", None, (1, 8), None),
        ("The slope is still 1, so the two lines are parallel.", None, None, "slope 1 (same): parallel"),
        ("Only the y-intercept changed, from (0, 0) to (0, 8).", "Only the y-intercept changed, from 0 to 8.", None, "y-intercept (0, 8)"),
        ("f(x) + d moves the graph up d units. This is a vertical translation.", None, None, "k(x) = x + 8"),
    ]),
    dict(title="Subtract: f(x) − 7", pts=[-4, 2, 6], g=(1, 0), steps=[
        ("Subtracting moves the graph down: j(x) = f(x) − 7.", None, None, "j(x) = f(x) − 7"),
        ("Every point moves down 7 units.", None, (1, -7), None),
        ("Same slope, 1. The y-intercept is now (0, −7).", "Same slope, 1. The y-intercept is now negative 7.", None, "j(x) = x − 7"),
    ]),
    dict(title="Multiply: 2 · f(x)", pts=[-4, 2, 4], g=(1, 0), label=True, steps=[
        ("Now multiply every output by 2: h(x) = 2 · f(x).", None, None, "h(x) = 2 · f(x)"),
        ("Each output doubles. (2, 2) becomes (2, 4), and (4, 4) becomes (4, 8).", None, (2, 0), None),
        ("The origin does not move, because 2 times 0 is still 0.", None, None, None),
        ("The line is steeper. Its slope is now 2.", None, None, "slope 2: steeper"),
        ("This is a vertical stretch by a factor of 2.", None, None, "h(x) = 2x"),
    ]),
    dict(title="Multiply: (1/3) · f(x)", pts=[-6, 3, 6], g=(1, 0), label=True, steps=[
        ("Multiply by one third: g(x) = (1/3) · f(x).", "Multiply by one third. g of x equals one third times f of x.", None, "g(x) = (1/3) · f(x)"),
        ("Each output is one third as big. (3, 3) becomes (3, 1), and (6, 6) becomes (6, 2).", None, (1 / 3, 0), None),
        ("The slope is 1/3, so the line is less steep.", "The slope is one third, so the line is less steep.", None, "slope 1/3: less steep"),
        ("A factor between 0 and 1 is a vertical compression.", None, None, "g(x) = (1/3)x"),
    ]),
    dict(title="A negative sign: −f(x)", pts=[-4, 2, 6], g=(1, 0), label=True, steps=[
        ("A negative sign changes the sign of every output: r(x) = −f(x).", "A negative sign changes the sign of every output. r of x equals negative f of x.", None, "r(x) = −f(x)"),
        ("(2, 2) becomes (2, −2). The graph reflects across the x-axis.", "2 comma 2 becomes 2 comma negative 2. The graph reflects across the x-axis.", (-1, 0), None),
        ("The slope changes from 1 to −1.", "The slope changes from 1 to negative 1.", None, "slope −1: reflection"),
    ]),
    dict(title="Both: 2 · f(x) + 3", pts=[-2, 2, 4], g=(1, 0), steps=[
        ("You can do both: g(x) = 2 · f(x) + 3.", None, None, "g(x) = 2 · f(x) + 3"),
        ("First the 2 stretches the line. The slope becomes 2.", None, (2, 0), "a = 2: slope 2"),
        ("Then the 3 moves it up 3. The y-intercept becomes (0, 3).", "Then the 3 moves it up 3. The y-intercept becomes 3.", (2, 3), "d = 3: y-intercept (0, 3)"),
        ("So g(x) = 2x + 3. The a-value changes the slope; the d-value changes the y-intercept.", None, None, "g(x) = 2x + 3"),
    ]),
    dict(title="Your turn", pts=[-2, 1, 3], g=None, steps=[
        ("Describe g(x) = 3 · f(x) − 2. What are its slope and y-intercept?", "Describe g of x equals 3 times f of x minus 2. What are its slope and y-intercept?", None, "g(x) = 3 · f(x) − 2"),
        ("Pause the video and try it.  PAUSE 5", "Pause the video and try it.", None, None),
        ("Vertical stretch by 3, then down 2. Slope 3, y-intercept (0, −2).", "It is a vertical stretch by 3, then a translation down 2. The slope is 3, and the y-intercept is negative 2.", (3, -2), "slope 3, y-intercept (0, −2)"),
        ("g(x) = 3x − 2.", "So g of x equals 3 x minus 2.", None, "g(x) = 3x − 2"),
    ]),
    dict(kind="title", title="g(x) = a · f(x) + d", sub="a changes the slope  ·  d changes the y-intercept", steps=[
        ("Adding d moves the graph up or down. The slope stays the same.", None, None, None),
        ("Multiplying by a changes the slope: steeper if a is greater than 1, less steep between 0 and 1, and a negative a reflects it.", None, None, None),
        ("Now try the matching on page 284 of your book.", None, None, None),
    ]),
]


def spoken(cap):
    s = re.sub(r"\s*PAUSE \d+", "", cap)
    for a, b in [("f(x)", "f of x"), ("g(x)", "g of x"), ("h(x)", "h of x"), ("k(x)", "k of x"), ("j(x)", "j of x"),
                 ("r(x)", "r of x"), (" · ", " times "), ("−", "minus ")]:
        s = s.replace(a, b)
    return s


def speak(text, path):
    ps = (f"Add-Type -AssemblyName System.Speech; $s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
          f"$s.SelectVoice('{VOICE}'); $s.Rate = {RATE}; $s.SetOutputToWaveFile('{path}'); "
          f"$s.Speak([IO.File]::ReadAllText('{path}.txt')); $s.Dispose()")
    open(path + ".txt", "w", encoding="utf8").write(text)
    subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=True)
    with wave.open(path) as w:
        return w.getnframes() / w.getframerate()


def wrap(d, text, font, width):
    lines, cur = [], ""
    for word in text.split():
        t = (cur + " " + word).strip()
        if d.textlength(t, font=font) > width and cur:
            lines.append(cur); cur = word
        else:
            cur = t
    return lines + [cur] if cur else lines


def ease(t): t = max(0.0, min(1.0, t)); return t * t * (3 - 2 * t)


def grid():
    im = Image.new("RGB", (W, H), "white"); d = ImageDraw.Draw(im)
    for i in range(-R, R + 1):
        x0, y0 = px(i, -R); x1, y1 = px(i, R)
        d.line([x0, y0, x1, y1], fill=AX if i == 0 else GRID, width=3 if i == 0 else 1)
        x0, y0 = px(-R, i); x1, y1 = px(R, i)
        d.line([x0, y0, x1, y1], fill=AX if i == 0 else GRID, width=3 if i == 0 else 1)
    for i in range(-R + 2, R, 2):
        if i:
            x, y = px(i, 0); d.text((x, y + 4), str(i).replace("-", "−"), fill=MUTED, font=F[18], anchor="mt")
            x, y = px(0, i); d.text((x - 6, y), str(i).replace("-", "−"), fill=MUTED, font=F[18], anchor="rm")
    d.text(px(R, 0), " x", fill=AX, font=F[26], anchor="lb"); d.text(px(0, R), "  y", fill=AX, font=F[26], anchor="lt")
    return im


def clip_line(d, a, b, color, width):  # y = a x + b clipped to the square
    pts = []
    for x in (-R, R):
        y = a * x + b
        if -R <= y <= R: pts.append((x, y))
    if a:
        for y in (-R, R):
            x = (y - b) / a
            if -R < x < R: pts.append((x, y))
    if len(pts) >= 2:
        pts.sort(); d.line([*px(*pts[0]), *px(*pts[-1])], fill=color, width=width)


def fmt(v):
    v = round(v, 2)
    if abs(v - round(v)) < 1e-6: v = int(round(v))
    return str(v).replace("-", "−")


def frame(base, sc, a, d_, show_g, panel, cap):
    im = base.copy(); d = ImageDraw.Draw(im)
    if sc.get("kind") == "title":
        d.rectangle([0, 0, W, H - 100], fill="white")
        d.text((W / 2, 250), sc["title"], fill=INK, font=FB[60], anchor="mm")
        d.text((W / 2, 330), sc["sub"], fill=BLUE, font=FB[34], anchor="mm")
    else:
        clip_line(d, 1, 0, BLUE, 5)
        d.text(px(7.2, 8.6), "f(x) = x", fill=BLUE, font=FB[26], anchor="rm")
        for x in sc["pts"]:
            xp, yp = px(x, x); d.ellipse([xp - 7, yp - 7, xp + 7, yp + 7], fill=BLUE)
        if show_g:
            clip_line(d, a, d_, RED, 5)
            for x in sc["pts"]:
                y = a * x + d_
                if not -R <= y <= R: continue
                x0, y0 = px(x, x); x1, y1 = px(x, y)
                if abs(y1 - y0) > 4: d.line([x0, y0, x1, y1], fill=RED, width=2)
                d.ellipse([x1 - 7, y1 - 7, x1 + 7, y1 + 7], fill=RED)
                if sc.get("label"): d.text((x1 + 12, y1 - 10), f"({fmt(x)}, {fmt(y)})", fill=RED, font=F[26], anchor="lb")
        d.text((680, 40), sc["title"], fill=INK, font=FB[44])
        y = 110
        for i, t in enumerate(panel):
            col = RED if i == len(panel) - 1 and show_g else INK
            for ln in wrap(d, t, FB[34] if i == 0 else F[34], 560):
                d.text((680, y), ln, fill=col if i else BLUE, font=FB[34] if i == 0 else F[34]); y += 44
            y += 14
    d.rectangle([0, H - 100, W, H], fill="#111827")
    lines = wrap(d, re.sub(r"\s*PAUSE \d+", "", cap), F[30], W - 80)
    for i, ln in enumerate(lines[:2]):
        d.text((W / 2, H - 50 + (i - (len(lines[:2]) - 1) / 2) * 36), ln, fill="white", font=F[30], anchor="mm")
    return im


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    tmp = tempfile.mkdtemp()
    base = grid()
    wavs, n = [], 0
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "26",
                           os.path.join(tmp, "v.mp4")], stdin=subprocess.PIPE)
    for sc in SCENES:
        a, d_ = sc.get("g") or (1, 0)
        show_g = False  # g appears on the step that first moves it, so it never hides f
        panel = []
        for cap, say, target, pline in sc["steps"]:
            wav = os.path.join(tmp, f"s{n:03d}.wav"); n += 1
            dur = speak(say or spoken(cap), wav) + 0.6
            m = re.search(r"PAUSE (\d+)", cap)
            hold = float(m.group(1)) if m else 0.0
            nf = round((dur + hold) * FPS)  # audio slot = whole frames, so sound and picture never drift
            wavs.append((wav, nf / FPS))
            if pline: panel.append(pline)
            a0, d0 = a, d_
            if target: show_g = True
            for f in range(nf):
                k = ease(f / FPS / min(2.0, dur)) if target else 0
                if target: a, d_ = a0 + (target[0] - a0) * k, d0 + (target[1] - d0) * k
                ff.stdin.write(frame(base, sc, a, d_, show_g, panel, cap).tobytes())
            if target: a, d_ = target
    ff.stdin.close(); ff.wait()
    # audio: each clip padded with silence to its slot length, then joined
    lst = os.path.join(tmp, "a.txt")
    with open(lst, "w") as fh:
        for i, (wav, slot) in enumerate(wavs):
            padded = os.path.join(tmp, f"p{i:03d}.wav")
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-af", f"apad=whole_dur={slot:.3f}",
                            "-ar", "22050", "-ac", "1", padded], check=True)
            fh.write(f"file '{padded}'\n")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(tmp, "v.mp4"), "-f", "concat", "-safe", "0",
                    "-i", lst, "-c:v", "copy", "-c:a", "aac", "-b:a", "96k", "-shortest", "-movflags", "+faststart", OUT],
                   check=True)
    print("wrote", OUT, f"{sum(s for _, s in wavs):.0f} s")


if __name__ == "__main__":
    main()

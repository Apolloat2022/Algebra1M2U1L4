"""Lesson 4 publisher slides with answers, in the style of
materials/BLMathematics_Geom_M1_T4_L2_LessonSlides_ENG_2026_with_answers.pptx:
each slide is the publisher slide, and red answer boxes appear on click.

Slides come from the publisher PDF, rendered by pdf.js in headless Chrome (needs Chrome and
internet for cdnjs). Answers are from the Teacher Edition (Module 2, pp. 201-216), each one
re-checked; where the TE was wrong or incomplete the slide notes say "TE correction" and the
last slide lists every change.  Standard library only.  Run:  python make_lesson_key.py
"""
import http.server
import shutil
import subprocess
import tempfile
import threading
import urllib.request
import zipfile
from pathlib import Path

import make_pptx as mp  # package helpers: rels, notes, timing, theme

HERE = Path(__file__).parent
PDF = HERE / "BLMathematics_AlgI_M2_T1_L4_LessonSlides_ENG_2025-5000x2813-ed06aa3.pdf"
OUT = HERE / "lesson4" / "BLMathematics_AlgI_M2_T1_L4_LessonSlides_ENG_with_answers.pptx"
PDFJS = "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/"
CHROME = [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
          r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"]
PX = 6350  # EMU per px: answer boxes are placed on a 1920 x 1080 grid over the 16:9 slide
RED = "FF0000"

# page -> [(x, y, w, h, size_pt, text)], placed in the slide's empty space
ANS = {
    4: [(137, 780, 1700, 260, 22,
         "Yes. Point-slope form: y − y1 = m(x − x1), where m is the slope and (x1, y1) is a point on the "
         "line. A horizontal line is y = c (slope 0). A vertical line is x = c (slope undefined).")],
    7: [(636, 830, 1200, 70, 26, "y = −3x + 14")],
    8: [(632, 450, 1200, 70, 26, "y = −2x + 16"),
        (632, 855, 1250, 110, 24, "m = (12 − 15)/(4 − 2) = −3/2\ny = −(3/2)x + 18")],
    9: [(218, 420, 1600, 260, 24,
         "Sample answer: The slope and y-intercept were given for Pool A. The slope was given for Pool B, "
         "but I had to calculate the y-intercept. I had to calculate the slope and y-intercept for Pool C.")],
    10: [(137, 400, 1650, 200, 24,
          "Summary: Real-world situations modeling linear relationships can be expressed as an equation in "
          "slope-intercept form, y = mx + b, where m is the slope and b is the y-intercept.")],
    15: [(209, 715, 1650, 340, 22,
          "−(1/2)(x − 2) = y − 6  →  −(1/2)x + 1 = y − 6  →  y = −(1/2)x + 7\n"
          "Both forms show the slope. Point-slope form shows a point on the line (which may not be the "
          "y-intercept); slope-intercept form shows the y-intercept.")],
    16: [(206, 440, 1500, 70, 26, "y − 12 = −8(x − 3)"),
         (206, 700, 1500, 70, 26, "y − 5 = (2/3)(x + 4)")],
    17: [(209, 420, 1500, 70, 26, "y − 14 = 1.1(x − 10)"),
         (209, 710, 1500, 70, 26, "y − 7 = −(3/8)(x − 50)")],
    18: [(980, 320, 880, 320, 26,
          "m = (20 − 102)/(42 − 35) = −82/7\ny − 20 = −(82/7)(x − 42)\nor  y − 102 = −(82/7)(x − 35)")],
    19: [(560, 330, 1300, 120, 26, "Sample answer:\ny + 6 = 0(x − 1)"),
         (218, 815, 1650, 240, 22,
          "y + 6 = 0(x − 1)  →  y + 6 = 0  →  y = −6\n"
          "There is no x-term: y is −6 for every x. It is a constant function (a horizontal line).")],
    20: [(300, 545, 1550, 60, 20, "Slope-intercept form: m and b go straight into y = mx + b."),
         (300, 680, 1550, 60, 20, "Calculate the slope first, then use point-slope form with either point."),
         (300, 815, 1550, 60, 20, "Point-slope form: use m and the point (x1, y1) directly.")],
    21: [(137, 400, 1650, 200, 24,
          "Summary: The point-slope form of a linear equation is y − y1 = m(x − x1), where m is the slope "
          "of the line and (x1, y1) is any point on the line.")],
    24: [(300, 785, 1550, 160, 24, "The equation has no x-term: y stays the same for every x. The slope is 0.")],
    25: [(534, 460, 980, 190, 21,
          "A horizontal line through (0, −6). The slope is 0 because y never changes: the rise is 0, "
          "so rise ÷ run = 0."),
         (534, 800, 1320, 200, 22,
          "The equation says y is always −6. Every y-value in the table is −6, and every point on the "
          "graph has a y-value of −6.")],
    26: [(680, 470, 1150, 230, 24, "y = 11\nHorizontal line; slope 0; y-intercept (0, 11)"),
         (296, 850, 1550, 140, 24, "y = −3.75\nHorizontal line; slope 0; y-intercept (0, −3.75)")],
    27: [(300, 545, 1200, 140, 22,
          "All the x-values are the same (−2) instead of all the y-values; this time the y-values change."),
         (300, 820, 1200, 70, 26, "x = −2")],
    28: [(218, 330, 1600, 70, 24, "A vertical line through (−2, 0)."),
         (218, 590, 1600, 130, 22, "m = (14 − 5)/(−2 − (−2)) = 9/0. You cannot divide by 0, so the slope is "
                                   "undefined."),
         (218, 865, 1650, 200, 22,
          "There is no y-intercept. The line x = −2 is parallel to the y-axis and never crosses it "
          "(x is never 0).")],
    29: [(700, 480, 1150, 250, 24, "x = 17/2  (x = 8.5)\nVertical line through (17/2, 0); slope undefined")],
    30: [(218, 385, 1600, 120, 24, "x = −7\nVertical line through (−7, 0); slope undefined"),
         (218, 780, 1650, 220, 22,
          "Sample: x-values 3, 3, 3 with y-values −1, 0, 5 give x = 3. Any table whose x-values are all "
          "the same number c gives the vertical line x = c.")],
    32: [(137, 400, 1700, 200, 22,
          "Summary: A horizontal line is y = a constant (no change in y, so the slope is 0). A vertical line "
          "is x = a constant (no change in x, so the slope is undefined)."),
         (137, 830, 1700, 200, 22,
          "Yes, point-slope form: y − y1 = m(x − x1). Horizontal line: y = c. Vertical line: x = c.")],
    37: [(608, 610, 1250, 440, 22,
          "Explanations will vary.\nA: y − 200 = −5(x − 24)     B: y = (1/2)x + 40\n"
          "C: y − x = 2     D: y = −(3/4)x + 33/2\nE: y = 8x + 120     F: y = 1.2x + 9")],
    38: [(308, 480, 1450, 130, 21,
          "Graph A falls from left to right (negative slope, −5); Graph C rises (positive slope, 1). "
          "The sign of m in y = mx + b shows this."),
         (308, 815, 1550, 220, 21,
          "Graph A: (0, 320). Graph C: (0, 2). In y = mx + b the y-intercept is (0, b), the number that is "
          "added: A is y = −5x + 320 and C is y = x + 2.")],
    39: [(226, 420, 1600, 200, 24,
          "Graph A: slope −5. Graph C: slope 1.\nThe slope is the coefficient of x when the equation is "
          "written in slope-intercept form.")],
    40: [(308, 475, 1060, 120, 20,
          "Table D: m = (9 − 15)/(10 − 2) = −6/8 = −3/4\nTable E: m = (264 − 216)/(18 − 12) = 48/6 = 8"),
         (308, 800, 1550, 260, 21,
          "It is the y-value when x = 0. If (0, y) is not in the table, find the slope, then substitute a "
          "point to solve for b.  Table D: b = 33/2.  Table E: b = 120.")],
    41: [(226, 420, 1620, 620, 22,
          "Context B: The term (1/2)x means Juliana reads one page every two minutes, or 1/2 page per "
          "minute; x is the number of minutes. The term 40 is the number of pages she had already read.\n"
          "Context F: The term 1.2x means each additional topping costs $1.20; x is the number of "
          "additional toppings. The term 9 is the cost of a large pizza.")],
    42: [(137, 400, 1650, 120, 24,
          "Summary: Linear relationships can be modeled using graphs, tables, contexts, and equations.")],
    45: [(228, 815, 740, 150, 24, "Slope 3/5; y-intercept (0, −4)"),
         (975, 815, 880, 150, 24, "Slope 2; point (−1, 6)")],
    46: [(137, 385, 800, 150, 24, "Slope 2; point (0, −4), which is also the y-intercept"),
         (975, 385, 880, 150, 24, "Slope −2/7; y-intercept (0, 0)"),
         (137, 750, 800, 150, 24, "Slope −1; point (4, −5)"),
         (975, 750, 880, 200, 24, "Slope 0; y-intercept (0, 19); a horizontal line")],
    47: [(218, 500, 1600, 450, 24,
          "Sample answer: Omar earns 4 credits for each game he plays. After playing 2 games today, he has "
          "56 credits.\nPoint-slope form: y − 56 = 4(x − 2)\nSlope-intercept form: y = 4x + 48")],
    48: [(137, 400, 1700, 130, 22,
          "Summary: Characteristics of linear relationships can be identified when their equations are "
          "written in slope-intercept form and point-slope form."),
         (137, 790, 1700, 200, 22,
          "Yes, point-slope form: y − y1 = m(x − x1). Horizontal line: y = c. Vertical line: x = c.")],
    54: [(230, 470, 760, 80, 26, "y = (1/2)x − 7/2"),
         (1080, 470, 760, 80, 26, "y = (4/3)x − 8"),
         (230, 820, 760, 80, 26, "y = −(2/3)x + 2"),
         (1080, 820, 760, 80, 26, "y = (1/8)x − 2")],
}

NOTES = {
    4: "TE correction: the TE sample answer names the slopes of horizontal and vertical lines but not their "
       "equations; y = c and x = c added.",
    18: "Added: the same line written through the other point, (35, 102).",
    25: "TE correction: part b asks why the slope makes sense; the TE answer only describes the graph. "
        "Reason added: y never changes, so the rise is 0.",
    28: "TE correction (part e): the TE says the line 'does not slope toward the y-axis'. The accurate reason: "
        "x = −2 is parallel to the y-axis and never reaches x = 0.",
    30: "Added a sample table for part c (TE: answers will vary).",
    38: "TE correction (part b): the TE never states the y-intercepts. Added (0, 320) and (0, 2).",
    40: "Added the b-values for Tables D and E: y = −(3/4)x + 33/2 and y = 8x + 120.",
    41: "TE correction: the TE calls the reader in Context B 'Michele'; the cutout card (b) names Juliana.",
    47: "TE correction: the question asks for point-slope AND slope-intercept form; the TE gives only "
        "point-slope. Added y = 4x + 48.",
    51: "Card matches (from slide 37): a. y − 200 = −5(x − 24); b. y = (1/2)x + 40; c. y − x = 2; "
        "d. y = −(3/4)x + 33/2; e. y = 8x + 120; f. y = 1.2x + 9.",
    54: "Answers from the Lesson 4 Assignment Prepare section, TE p. 216 (checked).",
}

CORRECTIONS = [
    ("Teacher Edition corrections in this deck", None),
    ("Activity 4.2 Q1b: the TE does not explain why a slope of 0 makes sense. Added: y never changes, so the "
     "rise is 0.", None),
    ("Activity 4.2 Q3e: the TE says the line 'does not slope toward the y-axis'. Corrected: x = −2 is "
     "parallel to the y-axis and never crosses it.", None),
    ("Activity 4.3 Q2b: the TE never identifies the y-intercepts. Added (0, 320) and (0, 2).", None),
    ("Activity 4.3 Q4: the TE names the reader 'Michele'; the cutout card says Juliana. Corrected.", None),
    ("Talk the Talk Q2: the TE omits the slope-intercept form. Added y = 4x + 48.", None),
    ("Essential Question: added the equations y = c (horizontal) and x = c (vertical).", None),
    ("Every other TE answer was re-solved and is correct, including the Lesson 4 Assignment (pp. 215-216).",
     "16171D"),
]


def render(pdf, out):
    """Rasterise every PDF page to out/pNNN.jpg with pdf.js in headless Chrome."""
    web = Path(tempfile.mkdtemp())
    for f in ("pdf.min.js", "pdf.worker.min.js"):  # worker must be same-origin, so serve both locally
        urllib.request.urlretrieve(PDFJS + f, web / f)
    shutil.copy(pdf, web / "slides.pdf")
    (web / "index.html").write_text(
        "<!doctype html><script src='pdf.min.js'></script><script>"
        "pdfjsLib.GlobalWorkerOptions.workerSrc='pdf.worker.min.js';"
        "(async()=>{const pdf=await pdfjsLib.getDocument('slides.pdf').promise;"
        "for(let i=1;i<=pdf.numPages;i++){const pg=await pdf.getPage(i);"
        "const vp=pg.getViewport({scale:2560/pg.getViewport({scale:1}).width});"
        "const c=document.createElement('canvas');c.width=vp.width;c.height=vp.height;"
        "const x=c.getContext('2d');x.fillStyle='#fff';x.fillRect(0,0,c.width,c.height);"
        "await pg.render({canvasContext:x,viewport:vp}).promise;"
        "await fetch('/save?p='+i,{method:'POST',body:await new Promise(r=>c.toBlob(r,'image/jpeg',0.9))});}"
        "await fetch('/done',{method:'POST'});})()"
        ".catch(e=>fetch('/err',{method:'POST',body:String(e.stack||e)}));</script>")
    errors = []

    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(s, *a, **k):
            super().__init__(*a, directory=str(web), **k)

        def log_message(s, *a):
            pass

        def do_POST(s):
            body = s.rfile.read(int(s.headers.get("Content-Length", 0)))
            if s.path.startswith("/save"):
                (out / f"p{int(s.path.split('=')[1]):03d}.jpg").write_bytes(body)
            elif s.path == "/err":
                errors.append(body.decode())
            s.send_response(200)
            s.end_headers()
            if s.path in ("/done", "/err"):
                threading.Thread(target=s.server.shutdown).start()

    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H)
    exe = next(p for p in CHROME if Path(p).exists())
    chrome = subprocess.Popen([exe, "--headless=new", "--disable-gpu", f"--user-data-dir={web / 'profile'}",
                               "--remote-debugging-port=0", f"http://127.0.0.1:{srv.server_port}/index.html"],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        srv.serve_forever()  # ponytail: no timeout; Ctrl+C if Chrome never loads the page
    finally:
        chrome.kill()
    if errors:
        raise SystemExit("pdf.js failed: " + errors[0])
    return sorted(out.glob("p*.jpg"))


def text_box(sid, x, y, w, h, size, text, color=RED, bold=False):
    b = ' b="1"' if bold else ""
    paras = "".join(
        f'<a:p><a:pPr><a:spcAft><a:spcPts val="300"/></a:spcAft></a:pPr><a:r><a:rPr lang="en-US" sz="{size * 100}"'
        f'{b} dirty="0"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
        f'<a:latin typeface="Arial"/><a:cs typeface="Arial"/></a:rPr><a:t>{mp.esc(t)}</a:t></a:r></a:p>'
        for t in text.split("\n"))
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="Answer {sid}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{x * PX}" y="{y * PX}"/><a:ext cx="{w * PX}" cy="{h * PX}"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr><p:txBody><a:bodyPr wrap="square" '
            'lIns="45720" tIns="18288" rIns="45720" bIns="18288" anchor="t"><a:noAutofit/></a:bodyPr><a:lstStyle/>'
            f'{paras}</p:txBody></p:sp>')


def slide_xml(shapes, steps):
    return (mp.HDR + f'<p:sld {mp.NS}><p:cSld><p:spTree>{mp.GRP}{shapes}</p:spTree></p:cSld>'
            '<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>' + mp.timing_xml(steps) + '</p:sld>')


PIC = ('<p:pic><p:nvPicPr><p:cNvPr id="2" name="Slide"/><p:cNvPicPr><a:picLocks noGrp="1" noChangeAspect="1"/>'
       '</p:cNvPicPr><p:nvPr/></p:nvPicPr><p:blipFill><a:blip r:embed="rId3"/><a:stretch><a:fillRect/></a:stretch>'
       '</p:blipFill><p:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="12192000" cy="6858000"/></a:xfrm>'
       '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>')
MASTER = (mp.HDR + f'<p:sldMaster {mp.NS}><p:cSld><p:bg><p:bgPr><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill>'
          f'<a:effectLst/></p:bgPr></p:bg><p:spTree>{mp.GRP}</p:spTree></p:cSld><p:clrMap {mp.CLRMAP}/>'
          '<p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst></p:sldMaster>')


def build(images):
    slides = []  # (xml, notes, image or None)
    for k, img in enumerate(images, 1):
        boxes = ANS.get(k, [])
        shapes = PIC + "".join(text_box(10 + j, *b) for j, b in enumerate(boxes))
        slides.append((slide_xml(shapes, [("fade", [10 + j]) for j in range(len(boxes))]), NOTES.get(k, ""), img))
        if k == 54:  # corrections summary goes before the acknowledgment pages
            y, shapes = 90, ""
            for j, (t, color) in enumerate(CORRECTIONS):
                first = j == 0
                h = 110 if first else 105
                shapes += text_box(10 + j, 137, y, 1700, h, 34 if first else 21, ("" if first else "• ") + t,
                                   color or ("2E7D4F" if first else RED), bold=first)
                y += h
            slides.append((slide_xml(shapes, []), "Summary of every change from the Teacher Edition answers.", None))

    n = len(slides)
    ct = ('<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="xml" ContentType="application/xml"/><Default Extension="jpg" ContentType="image/jpeg"/>'
          f'<Override PartName="/ppt/presentation.xml" ContentType="{mp.CT}presentation.main+xml"/>'
          f'<Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="{mp.CT}slideMaster+xml"/>'
          f'<Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="{mp.CT}slideLayout+xml"/>'
          f'<Override PartName="/ppt/notesMasters/notesMaster1.xml" ContentType="{mp.CT}notesMaster+xml"/>'
          '<Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>'
          '<Override PartName="/ppt/theme/theme2.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>')
    ct += "".join(f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="{mp.CT}slide+xml"/>'
                  f'<Override PartName="/ppt/notesSlides/notesSlide{i}.xml" ContentType="{mp.CT}notesSlide+xml"/>'
                  for i in range(1, n + 1))
    pres_rels = [("rId1", "slideMaster", "slideMasters/slideMaster1.xml"),
                 ("rId2", "notesMaster", "notesMasters/notesMaster1.xml"), ("rId3", "theme", "theme/theme1.xml")]
    pres_rels += [(f"rId{10 + i}", "slide", f"slides/slide{i}.xml") for i in range(1, n + 1)]
    pres = (mp.HDR + f'<p:presentation {mp.NS}><p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/>'
            '</p:sldMasterIdLst><p:notesMasterIdLst><p:notesMasterId r:id="rId2"/></p:notesMasterIdLst><p:sldIdLst>'
            + "".join(f'<p:sldId id="{255 + i}" r:id="rId{10 + i}"/>' for i in range(1, n + 1)) +
            '</p:sldIdLst><p:sldSz cx="12192000" cy="6858000"/><p:notesSz cx="6858000" cy="9144000"/></p:presentation>')

    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", mp.HDR + '<Types xmlns="http://schemas.openxmlformats.org/package/2006/'
                   f'content-types">{ct}</Types>')
        z.writestr("_rels/.rels", mp.rels([("rId1", "officeDocument", "ppt/presentation.xml")]))
        z.writestr("ppt/presentation.xml", pres)
        z.writestr("ppt/_rels/presentation.xml.rels", mp.rels(pres_rels))
        z.writestr("ppt/theme/theme1.xml", mp.theme("Point-Slope Form of a Line"))
        z.writestr("ppt/theme/theme2.xml", mp.theme("Notes"))
        z.writestr("ppt/slideMasters/slideMaster1.xml", MASTER)
        z.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels", mp.rels([
            ("rId1", "slideLayout", "../slideLayouts/slideLayout1.xml"), ("rId2", "theme", "../theme/theme1.xml")]))
        z.writestr("ppt/slideLayouts/slideLayout1.xml", mp.LAYOUT)
        z.writestr("ppt/slideLayouts/_rels/slideLayout1.xml.rels", mp.rels([
            ("rId1", "slideMaster", "../slideMasters/slideMaster1.xml")]))
        z.writestr("ppt/notesMasters/notesMaster1.xml", mp.NOTES_MASTER)
        z.writestr("ppt/notesMasters/_rels/notesMaster1.xml.rels", mp.rels([("rId1", "theme", "../theme/theme2.xml")]))
        for i, (xml, notes, img) in enumerate(slides, 1):
            items = [("rId1", "slideLayout", "../slideLayouts/slideLayout1.xml"),
                     ("rId2", "notesSlide", f"../notesSlides/notesSlide{i}.xml")]
            if img:
                z.write(img, f"ppt/media/slide{i}.jpg", zipfile.ZIP_STORED)
                items.append(("rId3", "image", f"../media/slide{i}.jpg"))
            z.writestr(f"ppt/slides/slide{i}.xml", xml)
            z.writestr(f"ppt/slides/_rels/slide{i}.xml.rels", mp.rels(items))
            z.writestr(f"ppt/notesSlides/notesSlide{i}.xml", mp.notes_xml(notes))
            z.writestr(f"ppt/notesSlides/_rels/notesSlide{i}.xml.rels", mp.rels([
                ("rId1", "notesMaster", "../notesMasters/notesMaster1.xml"), ("rId2", "slide", f"../slides/slide{i}.xml")]))
    print(f"wrote {OUT.relative_to(HERE)}: {n} slides, {sum(map(len, ANS.values()))} answers")


if __name__ == "__main__":
    tmp = Path(tempfile.mkdtemp())
    pages = render(PDF, tmp)
    assert len(pages) >= max(ANS), f"PDF rendered {len(pages)} pages; answers expect {max(ANS)}"
    build(pages)

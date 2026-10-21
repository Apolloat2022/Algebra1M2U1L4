"""Publisher lesson slides with answers, in the style of
materials/BLMathematics_Geom_M1_T4_L2_LessonSlides_ENG_2026_with_answers.pptx:
each slide is the publisher slide, and red answer boxes appear on click.

Lesson 4 exists only as a PDF, so its slides are rendered by pdf.js in headless Chrome (needs
Chrome and internet for cdnjs) and the answers sit over the pictures. Lessons 5-6 are editable
.pptx files, so the answers are added to the original slides. Answers come from the Teacher
Edition, each one re-checked; where the TE was wrong or incomplete the slide notes say "TE
correction" and an added slide lists every change.  Standard library only.
Run:  python make_lesson_key.py [4 5 6]     (no arguments: every lesson)
"""
import http.server
import re
import shutil
import subprocess
import sys
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
ANS4 = {
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

NOTES4 = {
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

CORRECTIONS4 = [
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


def text_box(sid, x, y, w, h, size, text, color=RED, bold=False, font="Arial", center=False):
    b = ' b="1"' if bold else ""
    face = f'<a:latin typeface="{font}"/><a:cs typeface="{font}"/>' if font else ""  # None: the deck's theme font
    paras = "".join(
        f'<a:p><a:pPr marL="0" indent="0" algn="{"ctr" if center else "l"}"><a:spcBef><a:spcPts val="0"/></a:spcBef><a:spcAft><a:spcPts val="300"/>'
        f'</a:spcAft><a:buNone/></a:pPr><a:r><a:rPr lang="en-US" sz="{size * 100}"'
        f'{b} dirty="0"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
        f'{face}</a:rPr><a:t>{mp.esc(t)}</a:t></a:r></a:p>'
        for t in text.split("\n"))
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="Answer {sid}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{x * PX}" y="{y * PX}"/><a:ext cx="{w * PX}" cy="{h * PX}"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr><p:txBody><a:bodyPr wrap="square" '
            f'lIns="45720" tIns="18288" rIns="45720" bIns="18288" anchor="{"ctr" if center else "t"}"><a:noAutofit/></a:bodyPr><a:lstStyle/>'
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


def corrections_shapes(corrections, sid, font="Arial"):
    """First entry is the heading; a second element of None means red text."""
    y, h, shapes = 90, 980 // len(corrections), ""
    for j, (t, color) in enumerate(corrections):
        first = j == 0
        shapes += text_box(sid + j, 137, y, 1700, h, 34 if first else 21, ("" if first else "• ") + t,
                           color or ("2E7D4F" if first else RED), bold=first, font=font)
        y += h
    return shapes


def build(images):
    slides = []  # (xml, notes, image or None)
    page = lambda k: mp.num_xml(999, k, 1790 * PX, 1040 * PX, 110 * PX, 32 * PX)  # bottom-right page number
    for k, img in enumerate(images, 1):
        boxes = ANS4.get(k, [])
        shapes = PIC + "".join(text_box(10 + j, *b) for j, b in enumerate(boxes)) + page(len(slides) + 1)
        slides.append((slide_xml(shapes, [("fade", [10 + j]) for j in range(len(boxes))]), NOTES4.get(k, ""), img))
        if k == 54:  # corrections summary goes before the acknowledgment pages
            slides.append((slide_xml(corrections_shapes(CORRECTIONS4, 10) + page(len(slides) + 1), []),
                           "Summary of every change from the Teacher Edition answers.", None))

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
    print(f"wrote {OUT.relative_to(HERE)}: {n} slides, {sum(map(len, ANS4.values()))} answers")


# ---------------------------------------------------------------- Lessons 5-6: annotate the publisher .pptx
# The publisher decks are editable, so the answers go into the original slides (as in the Geometry deck)
# instead of over pictures of them.

WITH, CENTER = "with", "center"  # optional extra fields of an answer box (see annotate)

ANS5 = {
    4: [(137, 790, 1700, 285, 19,
         "Yes. Use the form of the equation instead of a table of values.\n"
         "Slope-intercept: plot the y-intercept, then count the slope (rise over run) to plot more points.\n"
         "Point-slope: plot the point (x1, y1), then count the slope.\n"
         "Standard form: calculate and plot the x- and y-intercepts, then connect them.")],
    7: [(137, 595, 800, 130, 18, "Slope 2/3; y-intercept (0, 7). Plot (0, 7), go up 2 and right 3 to (3, 9), "
                                 "then draw the line."),
        (975, 595, 850, 130, 18, "A vertical line through (−4, 0); the slope is undefined. Draw the vertical "
                                 "line where every x-value is −4."),
        (137, 825, 800, 200, 18, "Slope 5; point (−1, 3). Plot (−1, 3), go up 5 and right 1 to (0, 8), then "
                                 "draw the line."),
        (975, 825, 850, 200, 18, "The slope and intercept are not shown. Find points: (2, 2) and (10, 5) are "
                                 "on the line (slope 3/8, y-intercept (0, 5/4)). Plot them and connect.")],
    8: [(137, 610, 1650, 200, 22,
         "Summary: Characteristics of linear relationships can be identified when their equations are written in "
         "different forms, such as slope-intercept form, point-slope form, and standard form.")],
    14: [(1300, 520, 580, 420, 20,
          "Plot the y-intercept (0, −1).\nSlope 3/2: up 3, right 2 → (2, 2), (4, 5).\nDown 3, left 2 → (−2, −4).\n"
          "Draw the line through the points.")],
    15: [(920, 420, 900, 380, 24,
          "Plot the y-intercept (0, 3).\nSlope −5/2: down 5, right 2 → (2, −2).\nUp 5, left 2 → (−2, 8).\n"
          "Draw the line through the points.")],
    16: [(905, 420, 490, 560, 21,
          "Plot the y-intercept (0, 25).\nSlope 10/1: up 10, right 1 → (1, 35), (2, 45).\nDown 10, left 1 → "
          "(−1, 15), (−2, 5).\nDraw the line.")],
    17: [(130, 600, 490, 460, 21,
          "y = 15x + 30\nx = number of lawns mowed, y = total savings ($).\nStart at (0, 30); go up 15 for each "
          "lawn: (2, 60), (4, 90), (6, 120).")],
    18: [(1330, 430, 560, 600, 20,
          "y = 20x − 130\nx = time (minutes), y = depth (feet).\nStart at (0, −130) and rise 20 each minute: "
          "(1, −110), (5, −30).\nThe diver reaches the surface (y = 0) at 6.5 minutes, so the graph ends at "
          "(6.5, 0).")],
    19: [(137, 460, 1650, 130, 22,
          "Summary: An equation in slope-intercept form can be graphed by plotting the y-intercept and then using "
          "the slope to locate two more points by counting from that point."),
         (137, 985, 1650, 90, 20, "Yes: use the y-intercept and the slope from the equation instead of a table.")],
    25: [(137, 530, 1500, 90, 30, "y − 50 = 5(x − 3)")],
    26: [(1338, 950, 575, 125, 17,
          "Point (3, 50); slope 5/1 (or −5/−1).\nMore points: (2, 45), (4, 55), (6, 65).")],
    27: [(511, 620, 780, 420, 22,
          "Slope −3/4; point (14, 5).\nFrom (14, 5): up 3, left 4 → (10, 8), (6, 11), (2, 14).\n"
          "The line crosses the y-axis at (0, 15.5).")],
    28: [(980, 420, 880, 420, 24,
          "Slope 1/2; point (−6, −8).\nFrom (−6, −8): up 1, right 2 → (−4, −7), (−2, −6), (0, −5), (2, −4).")],
    29: [(1209, 845, 690, 230, 17,
          "x = time (seconds), y = depth (meters)\ny + 25.8 = −0.3(x − 90)\nPlot (90, −25.8), then (190, −55.8).")],
    30: [(137, 610, 1650, 200, 22,
          "Summary: An equation in point-slope form can be graphed by plotting the known point and then using "
          "the slope to locate two more points by counting from that point.")],
    34: [(209, 510, 700, 170, 20, "The money from student tickets: $5 times the number of student tickets sold."),
         (960, 510, 800, 170, 20, "The money from adult tickets: $8 times the number of adult tickets sold."),
         (209, 770, 1400, 100, 20, "The total money collected in ticket sales, $1600.")],
    35: [(137, 430, 1600, 400, 22,
          "Either variable could be independent. The number of student tickets needed to reach $1600 depends on "
          "the number of adult tickets sold, or vice versa.")],
    37: [(137, 430, 1650, 420, 22,
          "x-intercept: 5x + 8(0) = 1600 → x = 320 → (320, 0). If 320 student tickets are sold, no adult tickets "
          "are needed to collect $1600.\n"
          "y-intercept: 5(0) + 8y = 1600 → y = 200 → (0, 200). If 200 adult tickets are sold, no student tickets "
          "are needed to collect $1600.")],
    38: [(1330, 450, 560, 400, 22,
          "Plot (320, 0) and (0, 200) and connect them. Only the segment between the intercepts makes sense: "
          "ticket counts cannot be negative.")],
    39: [(137, 430, 1600, 300, 24,
          "m = (0 − 200)/(320 − 0) = −5/8\nThe number of adult tickets decreases by 5 for every 8 more student "
          "tickets sold.")],
    # table cells: columns at x 227/543/812/1084, rows at y 469/569/691/791 (heights from the publisher's fallback)
    40: [(543, 469, 269, 100, 22, "(6/5, 0)", CENTER), (812, 469, 272, 100, 22, "(0, 3)", CENTER),
         (1084, 469, 267, 100, 22, "m = −5/2", CENTER),
         (227, 569, 316, 122, 22, "3x + 4y = 7", CENTER), (812, 569, 272, 122, 22, "(0, 7/4)", CENTER),
         (227, 691, 316, 100, 22, "2x − 3y = 9", CENTER), (543, 691, 269, 100, 22, "(9/2, 0)", CENTER),
         (543, 791, 269, 100, 22, "(−11/5, 0)", CENTER), (812, 791, 272, 100, 22, "(0, 11/7)", CENTER),
         (1084, 791, 267, 100, 22, "m = 5/7", CENTER),
         (1380, 420, 500, 420, 18, "Check each row: x-intercept (C/A, 0), y-intercept (0, C/B), slope −A/B.\n"
                                   "Row 2: the given x-intercept 7/3 and slope −3/4 give 3x + 4y = 7.\n"
                                   "Row 3: the slide's y-intercept (0, 23) is a typo for (0, −3).")],
    41: [(720, 420, 1100, 70, 24, "(C/A, 0)"), (720, 510, 1100, 70, 24, "(0, C/B)"),
         (720, 600, 1100, 70, 24, "m = −A/B"),
         (137, 720, 1600, 200, 20, "Example: 5x + 2y = 6 has x-intercept (6/5, 0), y-intercept (0, 6/2) = (0, 3), "
                                   "and slope −5/2.")],
    42: [(610, 470, 240, 60, 24, "Line 3"), (610, 612, 240, 60, 24, "Line 1"), (610, 754, 240, 60, 24, "Line 2"),
         (124, 930, 1700, 140, 18,
          "All three lines have y-intercept (0, 5), so match by slope: 3x − 12y = −60 has m = 1/4, 6x − 2y = −10 "
          "has m = 3, 9x − 9y = −45 has m = 1. The steepest line (Line 1) has the greatest slope.")],
    43: [(146, 975, 1100, 100, 17,
          "x = 5-minute periods of jumping rope, y = 5-minute periods of running: 20x + 50y = 500. "
          "Intercepts (25, 0) and (0, 10).")],
    44: [(1250, 520, 620, 460, 22,
          "x = student tickets, y = adult tickets\n5x + 6y = 270\nIntercepts (54, 0) and (0, 45); connect them.")],
    46: [(1110, 418, 760, 60, 24, "m = 3  →  3x − y = 4"), (1110, 542, 760, 60, 24, "m = −4  →  4x + y = −1"),
         (1110, 662, 760, 60, 24, "m = 1/2  →  x − 2y = −8")],
    47: [(137, 400, 1650, 200, 22,
          "Summary: The standard form of a linear equation is Ax + By = C, where A, B, and C are integers and A and "
          "B are not both zero. It can be graphed by calculating and plotting the intercepts."),
         (137, 985, 1650, 90, 20, "Yes: in standard form, the two intercepts give two points to graph.")],
    52: [(137, 570, 700, 130, 22, "Slope 11; y-intercept (0, −9)"),
         (974, 570, 800, 130, 22, "Slope −2/3; y-intercept (0, 45)"),
         (137, 840, 700, 130, 22, "Slope 10; y-intercept (0, −45)"),
         (974, 840, 800, 130, 22, "Slope −3/4; y-intercept (0, 3)")],
    53: [(137, 340, 780, 110, 22, "Slope 6; y-intercept (0, −27)"),
         (960, 340, 860, 110, 22, "Slope 0; y-intercept (0, 9)"),
         (137, 600, 780, 110, 22, "Slope 1/3; y-intercept (0, −4)"),
         (960, 600, 860, 110, 22, "Slope undefined; no y-intercept (vertical line)"),
         (137, 890, 780, 110, 22, "Slope 3; y-intercept (0, 7)"),
         (960, 890, 860, 110, 22, "Slope −1/2; y-intercept (0, 9)")],
    54: [(137, 400, 1650, 300, 22,
          "Summary: The slope can be read directly from slope-intercept or point-slope form, or calculated as "
          "−A/B from standard form Ax + By = C. The y-intercept can be found in any form by substituting x = 0.")],
    59: [(370, 268, 560, 70, 26, "2x + 3y = 36"),
         (960, 340, 900, 180, 20, "Standard form: points per question times the number of questions gives the "
                                  "total, so the equation comes straight from the context."),
         (960, 620, 900, 300, 20, "I plotted the intercepts (18, 0) and (0, 12) and connected them. Only "
                                  "whole-number scores make sense, so the solutions are the whole-number points "
                                  "on that segment.")],
    60: [(440, 465, 500, 70, 26, "y = 5x + 20"),
         (960, 530, 900, 180, 20, "Slope-intercept form: the starting amount ($20) and the rate ($10 every 2 weeks, "
                                  "or $5 per week) are given."),
         (960, 790, 900, 260, 20, "I plotted the y-intercept (0, 20) and used the slope 5/1 to plot (2, 30), "
                                  "(4, 40), and (10, 70).")],
    61: [(760, 400, 1130, 230, 18,
          "+ Shows the slope and y-intercept; easy to write from a starting value and a rate, and easy to graph.\n"
          "− Less helpful when the y-intercept is not known or not meaningful."),
         (760, 670, 1130, 230, 18,
          "+ Written from any point and the slope; graph by starting at that point.\n− The y-intercept is not shown."),
         (760, 935, 1130, 140, 18,
          "+ Fits 'total' contexts; both intercepts are easy to find and graph.\n− The slope must be calculated "
          "(m = −A/B).")],
    62: [(137, 400, 1650, 200, 22,
          "Summary: Different forms of equations, such as standard form, slope-intercept form, and point-slope form, "
          "can be used to represent linear relationships."),
         (137, 985, 1650, 90, 20, "Yes: choose the form that fits the information given, then graph from it.")],
    65: [(780, 395, 1000, 80, 26, "m = (12 − 10)/(3 − 0) = 2/3"),
         (780, 615, 1000, 80, 26, "m = (−4.5 − 4.5)/(1 − (−1)) = −9/2"),
         (780, 845, 1000, 80, 26, "m = (12 − 0)/(0 − 21) = −4/7")],
}

NOTES5 = {
    4: "TE correction: the TE's sample answer is copied from Lesson 4 (point-slope form, slopes of horizontal and "
       "vertical lines). It does not answer this lesson's question about graphing from an equation.",
    17: "The TE writes y = 30 + 15x; same line. Only whole lawns make sense, so the solutions are whole-number points.",
    29: "TE correction: the TE defines x as time in minutes; the rate (0.3 m per second) and the 90 seconds make "
        "x seconds. Also note the y-intercept (0, 1.2): the ROV starts 1.2 m above the water, on the boat. "
        "The problem says 'submarine' but means the ROV.",
    40: "TE correction: the TE gives the y-intercept of 3x + 4y = 7 as (0, 4/3). It is (0, 7/4): 4y = 7, y = 7/4. "
        "Slide typo: row 3 shows the y-intercept as (0, 23); for 2x − 3y = 9 it is (0, −3) (the minus sign became a 2).",
    57: "TE correction: the last bullet ('Match each transformed graph to the equation in the table, written in "
        "terms of f(x)') belongs to a different lesson. There are no transformed graphs or table here; skip it.",
    59: "Ask students why the graph could be drawn as points: only whole numbers of questions make sense.",
}

CORRECTIONS5 = [
    ("Teacher Edition corrections in this deck", None),
    ("Essential Question: the TE's sample answer is copied from Lesson 4. Replaced with how to graph from each "
     "form.", None),
    ("Activity 5.2 Q3 (ROV): the TE defines x in minutes; it is seconds. The equation is y + 25.8 = −0.3(x − 90).",
     None),
    ("Activity 5.3 Q6 table: the TE gives the y-intercept of 3x + 4y = 7 as (0, 4/3). Corrected to (0, 7/4).", None),
    ("Activity 5.3 Q6 table (slide 40): the slide shows the y-intercept of 2x − 3y = 9 as (0, 23). It is (0, −3).",
     None),
    ("Talk the Talk: the bullet about matching transformed graphs to f(x) belongs to another lesson.", None),
    ("Lesson 5 Assignment Q4d: the TE calls the buyer 'Eugenie'; the problem says Brianna.", None),
    ("Every other TE answer was re-solved and is correct, including the Assignment and Prepare (pp. 235-237).",
     "16171D"),
]


def clicks(groups, start):
    """One Appear-on-click per group of shape ids, numbered from start (the Geometry deck uses the same effect)."""
    out, ids = "", iter(range(start, 100000))
    for group in groups:
        effects = ""
        for j, sid in enumerate(group):
            node = "clickEffect" if j == 0 else "withEffect"
            effects += (f'<p:par><p:cTn id="{next(ids)}" presetID="1" presetClass="entr" presetSubtype="0" fill="hold" '
                        f'nodeType="{node}"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst><p:set><p:cBhvr>'
                        f'<p:cTn id="{next(ids)}" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst>'
                        f'</p:cTn><p:tgtEl><p:spTgt spid="{sid}"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility'
                        '</p:attrName></p:attrNameLst></p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set>'
                        '</p:childTnLst></p:cTn></p:par>')
        out += (f'<p:par><p:cTn id="{next(ids)}" fill="hold"><p:stCondLst><p:cond delay="indefinite"/></p:stCondLst>'
                f'<p:childTnLst><p:par><p:cTn id="{next(ids)}" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst>'
                f'<p:childTnLst>{effects}</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par>')
    return out


def add_clicks(x, ids):
    """Append click reveals to the slide's main animation sequence, creating the timing tree if needed."""
    if "<p:timing>" not in x:
        timing = ('<p:timing><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot">'
                  '<p:childTnLst><p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq">'
                  f'<p:childTnLst>{clicks(ids, 3)}</p:childTnLst></p:cTn><p:prevCondLst><p:cond evt="onPrev" delay="0">'
                  '<p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst><p:nextCondLst><p:cond evt="onNext" '
                  'delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst></p:seq></p:childTnLst></p:cTn>'
                  '</p:par></p:tnLst></p:timing>')
        at = x.find("<p:extLst>", x.find("</p:clrMapOvr>"))  # timing sits before the slide's trailing extLst
        at = at if at != -1 else x.rfind("</p:sld>")
        return x[:at] + timing + x[at:]
    seq = x.find('nodeType="mainSeq"')
    end = x.find("</p:childTnLst></p:cTn><p:prevCondLst>", seq)
    if seq == -1 or end == -1:
        raise SystemExit("slide has animations but no main sequence; add its answers by hand")
    start = max(map(int, re.findall(r'<p:cTn id="(\d+)"', x))) + 1
    return x[:end] + clicks(ids, start) + x[end:]


def annotate(src, out, ans, notes, corrections, after):
    files = {}
    with zipfile.ZipFile(src) as z:
        for n in z.namelist():
            files[n] = z.read(n)
    text = lambda n: files[n].decode("utf-8")
    rel_map = lambda n: {re.search(r'Id="(\w+)"', r).group(1): re.search(r'Target="([^"]+)"', r).group(1)
                         for r in re.findall(r"<Relationship [^>]*>", text(n))}
    pres, prels = text("ppt/presentation.xml"), rel_map("ppt/_rels/presentation.xml.rels")
    ids = re.findall(r'<p:sldId [^>]*r:id="(rId\d+)"', pres)
    order = ["ppt/" + prels[r] for r in ids]
    assert len(order) >= max(ans), f"{src.name} has {len(order)} slides; answers expect {max(ans)}"

    after = after if corrections else len(order)  # no corrections slide: nothing shifts the page numbers
    page = lambda sid, k: mp.num_xml(sid, k, 1790 * PX, 1040 * PX, 110 * PX, 32 * PX)  # bottom-right page number
    for k, path in enumerate(order, 1):
        x, boxes = text(path), ans.get(k, [])
        top = max(map(int, re.findall(r'<p:cNvPr id="(\d+)"', x)))
        x = x.replace("</p:spTree>", page(top + 1000, k + (k > after)) + "</p:spTree>", 1)
        files[path] = x.encode("utf-8")
        if boxes:
            base = max(map(int, re.findall(r'<p:cNvPr id="(\d+)"', x))) + 1
            shapes = "".join(text_box(base + j, *b[:6], font=None, center=CENTER in b[6:]) for j, b in enumerate(boxes))
            x = x.replace("</p:spTree>", shapes + "</p:spTree>", 1)
            groups = []  # extra fields: WITH shows the box on the same click as the one before it; CENTER centers it
            for j, b in enumerate(boxes):
                if WITH in b[6:] and groups:
                    groups[-1].append(base + j)
                else:
                    groups.append([base + j])
            files[path] = add_clicks(x, groups).encode("utf-8")
        if k in notes:
            srels = rel_map(path.replace("slides/", "slides/_rels/") + ".rels")
            target = next((t for t in srels.values() if "notesSlide" in t), None)
            if target is None:
                print(f"WARNING slide {k}: no notes page for: {notes[k]}")
                continue
            npath = "ppt/notesSlides/" + target.rsplit("/", 1)[1]
            nx = text(npath)
            body = nx.find('type="body"')
            close = nx.find("</p:txBody>", body)
            para = f'<a:p><a:r><a:rPr lang="en-US" b="1" dirty="0"/><a:t>{mp.esc(notes[k])}</a:t></a:r></a:p>'
            files[npath] = (nx[:close] + para + nx[close:]).encode("utf-8")

    if corrections:  # corrections slide, on the layout of the slide it follows
        n = max(int(m) for m in re.findall(r"ppt/slides/slide(\d+)\.xml", " ".join(files))) + 1
        ref = order[after - 1]
        layout = next(t for t in rel_map(ref.replace("slides/", "slides/_rels/") + ".rels").values() if "slideLayout" in t)
        files[f"ppt/slides/slide{n}.xml"] = (mp.HDR + f'<p:sld {mp.NS}><p:cSld><p:spTree>{mp.GRP}'
                                             f'{corrections_shapes(corrections, 2, font=None)}{page(999, after + 1)}'
                                             '</p:spTree></p:cSld>'
                                             '<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>').encode("utf-8")
        files[f"ppt/slides/_rels/slide{n}.xml.rels"] = mp.rels([("rId1", "slideLayout", layout)]).encode("utf-8")
        ct = text("[Content_Types].xml")
        files["[Content_Types].xml"] = ct.replace(
            "</Types>", f'<Override PartName="/ppt/slides/slide{n}.xml" ContentType="{mp.CT}slide+xml"/></Types>').encode()
        rid = f"rId{max(int(r[3:]) for r in prels) + 1}"
        pr = text("ppt/_rels/presentation.xml.rels")
        files["ppt/_rels/presentation.xml.rels"] = pr.replace("</Relationships>", (
            f'<Relationship Id="{rid}" Type="{mp.REL}slide" Target="slides/slide{n}.xml"/></Relationships>')).encode()
        sid = max(map(int, re.findall(r'<p:sldId id="(\d+)"', pres))) + 1
        anchor = re.search(rf'<p:sldId [^>]*r:id="{ids[after - 1]}"/>', pres).group(0)
        files["ppt/presentation.xml"] = pres.replace(anchor, anchor + f'<p:sldId id="{sid}" r:id="{rid}"/>').encode()

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in files.items():
            z.writestr(name, data)
    print(f"wrote {out.name}: {len(order) + bool(corrections)} slides, {sum(map(len, ans.values()))} answers")


EQ6 = ("General form f(x) = ax + b: a (the leading coefficient) is the slope, its steepness and direction; "
       "b gives the y-intercept (0, b).\nFactored form f(x) = a(x − c): a is the slope; c is the zero, the "
       "x-intercept (c, 0).")


def row(y, h, *cells):  # one table row, centered in its cells and revealed on one click: cells are (x, w, text)
    return [(x, y, w, h, 18, t, CENTER, *(() if i == 0 else (WITH,))) for i, (x, w, t) in enumerate(cells)]


ANS6 = {
    7: [(115, 830, 1690, 245, 18, EQ6)],
    10: [(205, 900, 340, 140, 18, "Scenario: linear\nEquation: linear"),
         (561, 900, 700, 140, 18, "Scenario: nonlinear (halves each hour)\nEquation: nonlinear (x is an exponent)"),
         (1314, 900, 520, 140, 18, "Scenario: nonlinear (A = s²)\nEquation: linear")],
    11: [(210, 660, 400, 140, 20, "Not a function: x = 1 has three outputs"),
         (770, 660, 400, 140, 20, "Linear: the constant function y = 1"),
         (1331, 660, 450, 140, 20, "Linear: y = −15x − 90")],
    12: [(210, 840, 440, 100, 20, "Nonlinear function (a curve)"),
         (707, 840, 440, 100, 20, "Linear function"),
         (1262, 840, 520, 100, 20, "Not a function (vertical line)")],
    13: [(137, 400, 1650, 200, 22,
          "Summary: Methods exist to determine whether a context, equation, table, or graph represents a "
          "linear function.")],
    17: [(282, 820, 540, 120, 22, "f(x) = −0.25x + 5"),
         (845, 820, 550, 160, 20, "Not linear: the rate of change is 4, then 4, then 2.")],
    18: [(122, 505, 1280, 70, 21, "He earns $2.50 per pretzel (every amount ÷ pretzels = 2.5)."),
         (1428, 760, 470, 300, 19, "Yes, directly proportional: y/x = 2.5 for every row, and 0 pretzels "
                                   "would earn $0.")],
    19: [(137, 400, 1650, 80, 28, "y = 2.5x"), (137, 780, 1650, 80, 28, "2.5(75) = $187.50")],
    20: [(640, 940, 1250, 130, 20, "Each ride ticket costs $0.75 (the rate of change); the entrance fee is $6 "
                                   "(the y-intercept).")],
    21: [(137, 430, 1600, 120, 20, "No. 7.5 ÷ 2 = 3.75 but 9 ÷ 4 = 2.25: the ratio is not constant because of the "
                                   "$6 entrance fee."),
         (137, 600, 1600, 70, 24, "y = 0.75x + 6"),
         (137, 850, 1600, 100, 22, "0.75x + 6 = 20 → x ≈ 18.67, so she can buy 18 ride tickets.")],
    22: [(660, 800, 1220, 230, 19,
          "No. The rate is −24 gallons per hour (−6 every 1/4 hour), but the tank is not empty at 0 hours, so "
          "water ÷ time is not constant.")],
    23: [(137, 370, 1600, 80, 22, "175 gallons (169 + 6 at time 0)"),
         (137, 565, 1600, 70, 24, "y = 175 − 24x"),
         (137, 910, 1600, 120, 22, "175 − 24x = 0 → x ≈ 7.29 hours (about 7 hours 17.5 minutes)")],
    24: [(137, 400, 1650, 180, 22,
          "Summary: If a table represents a linear function, the slope, or average rate of change, is constant "
          "between all given points."),
         (137, 760, 1680, 300, 19, EQ6)],
    30: [(137, 470, 1600, 400, 22,
          "Sample answer: The line passes through (0, 0): 0 T-shirts earns $0. The slope is 15: Gracie earns $15 per "
          "T-shirt. Selling 4 T-shirts earns $60. In this situation only whole numbers of T-shirts, 0 or more, make "
          "sense.")],
    31: [(539, 380, 1240, 130, 20, "Both intercepts are (0, 0): if no T-shirts are sold, Gracie earns $0."),
         (539, 612, 1240, 70, 24, "E(t) = 15t"),
         (539, 1000, 1240, 80, 16, "(t, E(t)): t T-shirts sold and the $ earned; every point on the line is a "
                                   "solution of E(t) = 15t.")],
    32: [(137, 560, 520, 300, 20, "E(2) = 30: the point (2, 30); 2 T-shirts earn $30."),
         (680, 560, 520, 300, 20, "E(5) = 75: the point (5, 75); 5 T-shirts earn $75."),
         (1220, 560, 560, 300, 20, "E(2.75) = 41.25: the point exists on the line, but she cannot sell 2.75 "
                                   "T-shirts.")],
    34: [(137, 395, 1100, 150, 20, "6.67 T-shirts earn exactly $100. She can only sell whole shirts, so she must "
                                   "sell 7 to earn at least $100."),
         (137, 740, 1100, 230, 20, "E(t) is the dollars earned for t T-shirts. The goal is $100 earned, so 100 "
                                   "replaces E(t).")],
    37: [(137, 610, 780, 400, 20, "Equation: it may give an answer that does not make sense in the context (6.67 "
                                  "shirts), so it must be rounded up or down."),
         (960, 610, 800, 400, 20, "Graph: it can be hard to read an exact value from a graph.")],
    38: [(137, 400, 1650, 250, 22,
          "Summary: An equation or a graph can be used to determine the value of an independent variable. A graph "
          "may give only an approximate answer; an equation always gives an exact answer.")],
    41: [(1181, 910, 700, 160, 18, "Both lines have the same slope, 15 (the same rate of change), so they are "
                                   "parallel.")],
    42: [(512, 478, 1300, 120, 19,
          "G(0) = −45: the point (0, −45). If no T-shirts are sold, she is $45 short (the cost of the 3 free "
          "shirts). It does not make sense in the situation."),
         (512, 765, 1300, 140, 19,
          "G(t) = 0 at (3, 0): after selling 3 T-shirts, her earnings are $0; she has no money to return to her "
          "mom.")],
    44: [(137, 360, 1600, 80, 22, "15(t − 3) = 15t − 45 by the distributive property."),
         (137, 625, 1600, 200, 22,
          "15(t − 3) = 100 → t − 3 ≈ 6.67 → t ≈ 9.67. On the graph G(t) reaches $100 at about 9.67. She needs to "
          "sell 10 T-shirts.")],
    # table rows (y, height) as PowerPoint lays them out; columns at x 486/704/1208
    46: (row(368, 90, (487, 219, "T-shirts"), (706, 504, "Number of T-shirts sold"), (1210, 506, "Input"))
         + row(458, 88, (487, 219, "Dollars"), (706, 504, "Earnings for selling t T-shirts"), (1210, 506, "Output"))
         + row(604, 88, (487, 219, "$ per T-shirt"), (706, 504, "Selling price of a T-shirt"),
               (1210, 506, "Slope (rate of change)"))
         + row(692, 92, (487, 219, "T-shirts"), (706, 504, "T-shirts sold, not counting the 3 free"),
               (1210, 506, "The input minus a constant"))
         + row(844, 88, (487, 219, "Dollars"), (706, 504, "Earnings for t T-shirts at $15 each"),
               (1210, 506, "The rate times the input"))
         + row(932, 90, (487, 219, "Dollars"), (706, 504, "Money lost on the 3 free T-shirts"),
               (1210, 506, "Constant term: y-intercept (0, −45)"))),
    51: [(119, 500, 880, 200, 20, "a = 15, the slope: draw a slope triangle, right 1 and up 15 (for example from "
                                  "(3, 0) to (4, 15))."),
         (119, 820, 880, 120, 20, "b = −45: the y-intercept, (0, −45).")],
    53: [(122, 840, 960, 235, 18, "a = 15: slope triangle (right 1, up 15).\nc = 3: the x-intercept (3, 0).\n"
                                  "The zero is 3: 15(t − 3) = 0 when t = 3.")],
    54: [(137, 400, 1650, 180, 22,
          "Summary: The general form and the factored form of a linear function each have a structure that "
          "identifies characteristics of its graph."),
         (137, 760, 1680, 300, 19, EQ6)],
    60: [(466, 660, 1400, 360, 20,
          "Both lines have the same slope, 15, so they are parallel.\nThe graph shifted down 35: the y-intercept "
          "moved from (0, −45) to (0, −80) and the x-intercept from 3 to 5 1/3.")],
    61: [(137, 460, 1600, 80, 22, "6 T-shirts: F(t) = 15t − 80 is positive only when t > 5 1/3."),
         (137, 640, 1600, 80, 22, "12 T-shirts: 15t − 80 = 100 → 15t = 180 → t = 12.")],
    62: [(113, 640, 1330, 400, 22,
          "F(t) = G(t) − 35\nF(t) = 15t − 80: a = 15 is the slope (slope triangle); b = −80 is the y-intercept "
          "(0, −80).")],
    63: [(115, 480, 1178, 300, 24,
          "F(t) = 15(t − 16/3)\na = 15 is the slope; c = 16/3 = 5 1/3 is the zero, the x-intercept (5 1/3, 0).")],
    64: [(137, 400, 1650, 250, 22,
          "Summary: In general form f(x) = ax + b, a is the slope and b is the y-intercept. In factored form "
          "f(x) = a(x − c), a is the slope and c is the x-intercept, or zero, of the function.")],
    67: [(385, 463, 300, 60, 24, "always"), (385, 585, 300, 60, 24, "sometimes")],
    68: [(296, 243, 300, 60, 24, "always"), (296, 365, 300, 60, 24, "sometimes"),
         (296, 487, 300, 60, 24, "always"), (296, 553, 300, 60, 24, "always")],
    69: [(395, 612, 700, 70, 26, "25x − 45"), (425, 714, 700, 70, 26, "255"), (510, 816, 700, 70, 26, "x = −4")],
    70: [(335, 482, 700, 70, 26, "−6x + 24"), (355, 584, 700, 70, 26, "78"), (425, 684, 700, 70, 26, "x = 13")],
    71: [(137, 790, 1600, 250, 22,
          "General form: f(x) = 2x − 8: slope 2, y-intercept (0, −8).\n"
          "Factored form: f(x) = 2(x − 4): slope 2, zero 4 (x-intercept (4, 0)).")],
    72: [(900, 400, 900, 500, 22,
          "Plot (0, −8) and (4, 0) and draw the line (slope 2).\nIn factored form f(x) = 2(x − 4) the only zero is "
          "x = 4, so the line crosses the x-axis once. A non-horizontal line always crosses the x-axis exactly "
          "once.")],
    73: [(254, 494, 160, 60, 22, "−1"), (454, 494, 160, 60, 22, "−10", WITH),
         (254, 595, 160, 60, 22, "0"), (454, 595, 160, 60, 22, "−8", WITH),
         (254, 696, 160, 60, 22, "2"), (454, 696, 160, 60, 22, "−4", WITH),
         (254, 797, 160, 60, 22, "4"), (454, 797, 160, 60, 22, "0", WITH)],
    74: [(137, 400, 1650, 200, 22,
          "Summary: Both forms relate to the graph and table of the function. The equation always gives exact "
          "answers; the graph and table sometimes give only approximate values."),
         (137, 760, 1680, 300, 19, EQ6)],
    77: [(140, 400, 860, 500, 22,
          "General form: f(x) = 2x − 8\nFactored form: f(x) = 2(x − 4)\nGraph: a line through (0, −8) and (4, 0)\n"
          "Table: (0, −8), (2, −4), (4, 0), (6, 4)")],
    79: [(520, 354, 1000, 60, 24, "= −2(3) − 5 = −11"), (520, 420, 1000, 60, 24, "= 2(−1) = −2"),
         (520, 486, 1000, 60, 24, "= −1(−7) + 5 = 12"), (520, 552, 1000, 60, 24, "= 5(−5) + 5 = −20")],
}

NOTES6 = {
    31: "TE correction: the TE answers only the y-intercept (E(0) = 0). The question asks for both: the x- and "
        "y-intercepts are the same point, (0, 0). Also, in part 4 the TE writes f(t); the function is E(t).",
    33: "Slide typo: the last line of the Worked Example reads '6.67 = 1'. It should read 6.67 = t.",
    46: "Each click fills one row of the table.",
    61: "TE correction (part d): the TE says she needs 'an additional 6 T-shirts'. She needs to sell 12 T-shirts in "
        "all (6 more than the 6 she needs to break even).",
    71: "TE correction: the TE writes 'y-intercept = −8'. The y-intercept is the point (0, −8).",
}

CORRECTIONS6 = [
    ("Teacher Edition corrections in this deck", None),
    ("Activity 6.2 Q2: the TE gives only the y-intercept. Added: the x- and y-intercepts are both (0, 0).", None),
    ("Activity 6.2 Q4: the TE writes f(t); the function is E(t).", None),
    ("Activity 6.2 Worked Example (slide 33): the last line reads '6.67 = 1'; it should be 6.67 = t.", None),
    ("Activity 6.4 Q1d: the TE says 'an additional 6 T-shirts'. Clarified: she needs to sell 12 T-shirts in all.",
     None),
    ("Talk the Talk Q3a: the TE writes 'y-intercept = −8'; the y-intercept is the point (0, −8).", None),
    ("Every other TE answer was re-solved and is correct, including the Assignment and Prepare (pp. 255-256).",
     "16171D"),
]

PPTX = {5: (ANS5, NOTES5, CORRECTIONS5, 65),  # lesson -> answers, notes, corrections, slide the summary follows
        6: (ANS6, NOTES6, CORRECTIONS6, 79)}

# ---------------------------------------------------------------- Topic 2 Lesson 1: Transforming Linear Functions

def cells(x, y, *values, h=58, more=False):  # a table column filled top to bottom on one click (more: same click as before)
    return [(x, y + i * h, 116, h, 20, v, CENTER, *(() if i == 0 and not more else (WITH,))) for i, v in enumerate(values)]


ANS_T2_1 = {
    4: [(122, 700, 1690, 370, 17,
         "Translation: y = f(x) + d moves the graph up (d > 0) or down (d < 0) by |d| units. The slope stays the "
         "same, so the new line is parallel to the original; the y-intercept changes.\n"
         "Dilation: y = a · f(x) stretches the graph vertically when |a| > 1 and compresses it when 0 < |a| < 1; "
         "when a < 0 it is also reflected across the x-axis. The slope changes; for f(x) = x the new slope is a.")],
    7: [(110, 905, 640, 165, 18, "The points move straight up or straight down. There is no movement left "
                                 "or right.")],
    8: [(585, 522, 360, 144, 26, "(x, y + 4)", CENTER), (945, 522, 360, 144, 26, "(x, y − 4)", CENTER, WITH)],
    9: [(1240, 480, 640, 480, 20, "C(−8, −4) and D(8, 12): every point of AB moves up 4.\n"
                                  "The segments are parallel, with CD 4 units above AB.")],
    10: [(122, 400, 1700, 200, 22, "Each point moves straight up or down, away from the x-axis (twice as far). The "
                                   "segment gets steeper: a vertical stretch. When the factor is −2, the points also "
                                   "reflect across the x-axis.")],
    11: [(1250, 470, 640, 500, 20, "E(−8, −16) and F(8, 16).\nEF is steeper than AB (stretched vertically by a "
                                   "factor of 2); both pass through the origin.")],
    12: [(1250, 470, 640, 500, 20, "G(−8, 16) and H(8, −16).\nGH is steeper than AB, and it is reflected across "
                                   "the x-axis.")],
    18: [(122, 470, 1700, 130, 24, "Slope: 1;  y-intercept: (0, −5)\nm(x) = x − 5")],
    19: [*cells(1407, 685, "3", "4", "5", "6", "7"),
         (1026, 990, 860, 60, 18, "Graph p(x): the line through (0, 5), parallel to f(x)")],
    20: [(122, 420, 1700, 130, 24, "Slope: 1;  y-intercept: (0, 5)\np(x) = x + 5")],
    21: [(122, 770, 1700, 130, 24, "f(2) = 2 and p(2) = 7.\nThe vertical translation increased the value at x = 2 "
                                   "by 5.")],
    22: [(1490, 420, 410, 300, 22, "q(x) = j(x) + 4\nGraph: the line through (0, 3), parallel to j(x)")],
    23: [(526, 770, 1370, 55, 20, "a. r(x) = j(x) − 4  (graph: the line through (0, −5), parallel to j(x))"),
         (526, 830, 1370, 55, 20, "b. q(x) = 2x + 3;  r(x) = 2x − 5"),
         (526, 890, 1370, 110, 20, "c. All three have slope 2 but different y-intercepts: (0, −1), (0, 3), (0, −5). "
                                   "The lines are parallel, so they never intersect.")],
    29: [(122, 500, 1700, 130, 24, "No. Both lines have slope 2 and stay 4 units apart, so they are parallel.")],
    31: [(160, 395, 1600, 70, 24, "A′(x1, y1 + a)  and  B′(x2, y2 + a)"),
         (160, 570, 1600, 70, 24, "m = (y2 − y1) / (x2 − x1)"),
         (160, 750, 1600, 120, 24, "m = ((y2 + a) − (y1 + a)) / (x2 − x1) = (y2 − y1) / (x2 − x1)")],
    32: [(542, 400, 1350, 60, 22, "The slopes are the same."),
         (542, 640, 1350, 90, 22, "The graphs are parallel lines.")],
    34: [(122, 400, 1700, 130, 22, "Answers will vary. Catalina translates the given line up 5; James uses the "
                                   "slope formula with the point (2, 9). Both get y = (1/2)x + 8."),
         (122, 680, 1700, 200, 24, "y = −3x + 2\nParallel, so the slope is −3: 5 = −3(−1) + b, so b = 2.")],
    38: [*cells(1252, 776, "−8", "−4", "0", "4", "8"),
         (1400, 640, 480, 130, 20, "Graph a(x): through (0, 0) and (1, 4)")],
    39: [(122, 420, 1700, 130, 24, "Slope: 4;  y-intercept: (0, 0)\na(x) = 4x")],
    40: [*cells(1252, 732, "−4/3", "−2/3", "0", "2/3", "4/3"),
         (1400, 590, 480, 130, 20, "Graph b(x): through (0, 0) and (3, 2)")],
    41: [(122, 420, 1700, 130, 24, "Slope: 2/3;  y-intercept: (0, 0)\nb(x) = (2/3)x")],
    42: [*cells(1252, 732, "8", "4", "0", "−4", "−8"),
         (1400, 590, 480, 130, 20, "Graph c(x): through (0, 0) and (1, −4)")],
    43: [(122, 420, 1700, 130, 24, "Slope: −4;  y-intercept: (0, 0)\nc(x) = −4x")],
    44: [(122, 830, 1700, 130, 24, "f(−1) = −1 and c(−1) = 4.\nThe vertical dilation multiplied the value at x = −1 "
                                   "by −4.")],
    50: [(1450, 470, 450, 280, 18, "a. g(x) = 2x + 7\nVertical stretch by a factor of 2, then up 7. "
                                   "Graph: through (0, 7), slope 2."),
         (1450, 770, 450, 280, 18, "b. g(x) = 3x − 1\nVertical stretch by a factor of 3, then down 1. "
                                   "Graph: through (0, −1), slope 3.")],
    51: [(120, 840, 760, 220, 18, "g(x) = (1/3)x + 2\nVertical compression by a factor of 1/3, then up 2. "
                                  "Graph: through (0, 2), slope 1/3."),
         (860, 840, 900, 220, 18, "g(x) = (1/2)x − 3\nVertical compression by a factor of 1/2, then down 3. "
                                  "Graph: through (0, −3), slope 1/2.")],
    52: [(120, 830, 760, 230, 18, "g(x) = −x − 4\nReflection across the x-axis, then down 4. "
                                  "Graph: through (0, −4), slope −1."),
         (860, 830, 900, 230, 18, "g(x) = −(2/3)x + 5\nReflection across the x-axis and vertical compression by "
                                  "a factor of 2/3, then up 5. Graph: through (0, 5), slope −2/3.")],
    53: [(216, 840, 1540, 95, 18, "a. a changes the slope (for f(x) = x the slope becomes a: |a| > 1 steeper, "
                                  "0 < |a| < 1 less steep, a < 0 reflected). It does not change the y-intercept."),
         (216, 945, 1540, 95, 18, "b. d does not change the slope. It changes the y-intercept to (0, d): d > 0 moves "
                                   "the line up, d < 0 moves it down.")],
    59: [(546, 450, 1340, 120, 20, "Sample: a = 0 with d = 6, 4, 1 and −3: horizontal lines through each target "
                                   "(move the cannon to (0, d))."),
         (546, 700, 1340, 300, 18, "The cannon shoots in only one direction. Targets in Quadrant II (left of the "
                                   "y-axis): domain x ≤ 0. Targets in Quadrants I and IV: domain x ≥ 0.")],
    60: [(122, 895, 870, 180, 16, "Version B (a = 1 or −1; move d), clockwise from top left:\n"
                                  "a = −1, d = 2 (x ≤ 0);  a = 1, d = −1 (x ≥ 0);\n"
                                  "a = −1, d = −2 (x ≥ 0);  a = −1, d = −4 (x ≤ 0)"),
         (1010, 895, 880, 180, 16, "Version C (d = 0; change a), clockwise from top left:\n"
                                   "a = −3/2 (x ≤ 0);  a = 4/5 (x ≥ 0);\na = −3 (x ≥ 0);  a = −1/5 (x ≤ 0)")],
    65: [(1225, 418, 480, 56, 24, "f(x) + 8"),
         (540, 690, 1340, 60, 18, "k(x): f(x) translated up 8 units.", WITH),
         (1225, 484, 480, 56, 24, "2 · f(x)"),
         (540, 755, 1340, 60, 18, "h(x): f(x) stretched vertically by a factor of 2 (through the origin, steeper).",
          WITH),
         (1225, 550, 480, 56, 24, "(1/3) · f(x)"),
         (540, 820, 1340, 60, 18, "g(x): f(x) compressed vertically by a factor of 1/3 (through the origin, less "
                                  "steep).", WITH),
         (1225, 616, 480, 56, 24, "f(x) − 7"),
         (540, 885, 1340, 60, 18, "j(x): f(x) translated down 7 units.", WITH)],
    69: [(163, 985, 700, 80, 24, "f(x) = (2/3)x − 14/3"), (1125, 985, 700, 80, 24, "g(x) = −(1/4)x + 2")],
}

NOTES_T2_1 = {
    34: "Q1 has no single answer; let students defend either method.",
    50: "Slide typo: the second item is labeled 'a.'; it is item b.",
    52: "Slide typo: the first item is labeled 'a.'; it is item e.",
    53: "TE correction (part a): the TE says the slope 'increases' when a > 1 or a < −1 and 'decreases' between −1 "
        "and 1. That describes steepness, not slope: for a = −3 the slope is −3. For f(x) = x the new slope is a.",
    60: "The targets, read from the picture as the TE does: (−4, 6), (5, 4), (1, −3), (−5, 1). Other answers: "
        "Version B also a = 1, d = 10; a = −1, d = 9; a = 1, d = −4; a = 1, d = 6. TE correction: for the lower "
        "Quadrant II target the TE's alternative a = 1, d = 4 gives y = x + 4, which misses (−5, 1); it is d = 6. "
        "The TE's Version C slope −6/4 simplifies to −3/2.",
    69: "TE correction: the TE gives f(x) = (2/3)x − 5. The marked points (−8, −10), (−2, −6) and (4, −2) give slope "
        "2/3 and y-intercept (0, −14/3), so f(x) = (2/3)x − 14/3.",
}

CORRECTIONS_T2_1 = [
    ("Teacher Edition corrections in this deck", None),
    ("Activity 1.4 Q2a: the TE says the slope 'increases' or 'decreases'; it means steepness. For f(x) = x the new "
     "slope is a.", None),
    ("Activity 1.5 Q3 Version B: for the lower Quadrant II target (−5, 1), the TE's a = 1, d = 4 misses; it is "
     "a = 1, d = 6.", None),
    ("Prepare Q1: the TE gives f(x) = (2/3)x − 5. The graph's points give f(x) = (2/3)x − 14/3.", None),
    ("Slide typos: slide 50's second item 'a.' is b; slide 52's first item 'a.' is e.", None),
    ("Every other TE answer was re-solved and is correct, including the Assignment (pp. 285-286) and Prepare Q2.",
     "16171D"),
]

# ---------------------------------------------------------------- Topic 2 Lesson 2: Vertical and Horizontal Transformations

def blanks(x, ys, *values, w=440, size=22):  # answers in the empty space past a column of blank lines, one click each
    return [(x, y, w, 50, size, v) for y, v in zip(ys, values)]


ANS_T2_2 = {
    6: [(1600, 540, 300, 100, 18, "Domain:\nall real numbers"), (1600, 650, 300, 100, 18, "Range:\nall real numbers"),
        *blanks(800, [584, 652], "(8/3, 0)", "(0, −8)", w=170), *blanks(650, [720], "3", w=150),
        *blanks(770, [850], "Increasing", w=200, size=20),
        (1600, 400, 300, 130, 18, "Graph g(x): through (0, −8) and (3, 1)")],
    7: [(1590, 400, 310, 100, 18, "Domain:\nall real numbers"), (1590, 510, 310, 100, 18, "Range:\nall real numbers"),
        *blanks(800, [502, 570], "(7.5, 0)", "(0, 5)", w=160), *blanks(650, [638], "−2/3", w=150),
        *blanks(765, [772], "Decreasing", w=190, size=20),
        (1590, 280, 310, 110, 18, "Graph h(x): through (0, 5) and (3, 3)")],
    13: [*cells(1196, 734, "−5", "−4", "−3", "−2", "−1"), *cells(1312, 734, "−2", "−1", "0", "1", "2", more=True),
         (1450, 734, 440, 150, 20, "Graph t(x): through (−3, 0) and (0, 3)")],
    14: [*cells(1452, 659, "−2", "−1", "0", "1", "2"), *cells(1568, 659, "1", "2", "3", "4", "5", more=True),
         (82, 420, 380, 300, 20, "Graph w(x): through (0, 3) and (−3, 0). It is the same line as t(x).")],
    15: [(122, 380, 1700, 90, 20, "The input values. The output values stay the same."),
         (122, 558, 1700, 90, 20, "The output values. The input values stay the same."),
         (122, 736, 1700, 120, 20, "The graphs of t(x) and w(x) are the same line, y = x + 3, but their tables of "
                                   "values are different.")],
    16: [(122, 400, 1700, 130, 20, "Horizontal translations, y = f(x − c). The output values of the corresponding "
                                   "points stay the same."),
         (122, 636, 1700, 130, 20, "Vertical translations, y = f(x) + d. The input values of the corresponding "
                                   "points stay the same.")],
    17: [(122, 400, 1700, 80, 22, "A vertical translation down n units."),
         (122, 636, 1700, 80, 22, "A horizontal translation left n units.")],
    20: [(122, 945, 860, 130, 18, "b. q(x) = j(x) + 4\nGraph q(x): through (0, 3), slope 2"),
         (990, 945, 900, 130, 18, "d. r(x) = j(x + 4)\nGraph r(x): through (0, 7), slope 2")],
    21: [(122, 336, 1700, 70, 20, "The graphs are not the same. They are parallel lines with different y-intercepts."),
         (800, 560, 1080, 260, 20, "r(x) = j(x + 4) = 2(x + 4) − 1 = 2x + 8 − 1\nr(x) = 2x + 7\n"
                                   "The equations for q(x) and r(x) are not the same.")],
    22: [(1130, 450, 760, 200, 20, "Graph b(x): through (0, −5) and (2.5, 0), slope 2"),
         (1150, 915, 740, 60, 24, "b(x) = j(x − 2)")],
    23: [(1130, 450, 760, 200, 20, "Graph v(x): through (0, −3) and (1.5, 0), slope 2"),
         (1150, 915, 740, 60, 24, "v(x) = j(x) − 2")],
    24: [(122, 345, 1700, 60, 18, "The graphs are not the same. They are parallel lines with different y-intercepts."),
         (122, 600, 1700, 200, 22, "b(x) = j(x − 2) = 2(x − 2) − 1 = 2x − 5\nv(x) = j(x) − 2 = 2x − 1 − 2 = 2x − 3\n"
                                   "The equations for b(x) and v(x) are not the same.")],
    25: [(122, 395, 1700, 110, 20, "No. It is true only for f(x) = x. For j(x) = 2x − 1, right 2 gives 2x − 5 but "
                                   "down 2 gives 2x − 3."),
         (122, 630, 1700, 110, 20, "No. For j(x) = 2x − 1, left 4 gives r(x) = 2x + 7 but up 4 gives "
                                   "q(x) = 2x + 3.")],
    29: [(122, 620, 1690, 380, 20,
          "When f(x) is replaced by a·f(b(x − c)) + d, b and c affect the input values (horizontal "
          "transformations), while a and d affect the output values (vertical transformations).\n"
          "For f(x) = x, a translation right n gives the same graph as a translation down n, and a horizontal "
          "dilation by n gives the same graph as a vertical dilation by 1/n. For other linear functions these "
          "pairs are not the same.")],
    31: [*cells(1301, 679, "−4", "−2", "0", "2", "4"),
         (1440, 680, 450, 150, 20, "Graph a(x): through (0, 0) and (1, 2)")],
    32: [*cells(1184, 670, "−1", "−1/2", "0", "1/2", "1"),
         (1440, 670, 450, 150, 20, "Graph b(x): through (0, 0) and (1, 2), the same line as a(x)")],
    33: [(122, 380, 1700, 110, 22, "The graphs of a(x) and b(x) are the same line, y = 2x, but their tables of "
                                   "values are different.")],
    34: [*cells(1292, 707, "−8/5", "−4/5", "0", "4/5", "8/5"),
         (1430, 707, 460, 150, 20, "Graph c(x): through (0, 0) and (5, 4)")],
    35: [*cells(1174, 660, "−5/2", "−5/4", "0", "5/4", "5/2"),
         (1430, 660, 460, 150, 20, "Graph d(x): through (0, 0) and (5, 4), the same line as c(x)")],
    36: [(122, 380, 1700, 110, 22, "The graphs of c(x) and d(x) are the same line, y = (4/5)x, but their tables of "
                                   "values are different.")],
    37: [(122, 440, 1700, 70, 22, "A factor of 1/n."), (122, 680, 1700, 70, 22, "A factor of 1/n.")],
    41: [(780, 470, 1110, 580, 20,
          "No. It is true only for the parent function f(x) = x.\n"
          "Counterexample: m(x) = 2x − 1.\n"
          "n(x) = 3·m(x) = 3(2x − 1) = 6x − 3\n"
          "p(x) = m(3x) = 2(3x) − 1 = 6x − 1\n"
          "The graphs of n(x) and p(x) are parallel, not the same.\n"
          "Graph: m(x) through (0, −1), slope 2; n(x) through (0, −3) and p(x) through (0, −1), slope 6.")],
    45: [(1290, 500, 600, 400, 20, "f(x) is translated right 7 units.\nGraph g(x) = x − 7: through (7, 0) and "
                                   "(0, −7)")],
    46: [(1290, 270, 600, 400, 20, "f(x) is stretched vertically by a factor of 3.\nGraph g(x) = 3x: through "
                                   "(0, 0) and (2, 6)")],
    47: [(1290, 270, 600, 400, 20, "f(x) is translated up 2 units.\nGraph g(x) = x + 2: through (0, 2) and "
                                   "(−2, 0)")],
    48: [(1290, 270, 600, 400, 20, "f(x) is stretched horizontally by a factor of 2.\nGraph g(x) = (1/2)x: "
                                   "through (0, 0) and (4, 2)")],
    49: [(1290, 270, 600, 400, 20, "f(x) is translated down 4 units.\nGraph g(x) = x − 4: through (0, −4) and "
                                   "(4, 0)")],
    50: [(1290, 270, 600, 400, 20, "f(x) is translated left 5 units.\nGraph g(x) = x + 5: through (0, 5) and "
                                   "(−5, 0)")],
    55: [*blanks(945, [406, 472, 538, 604], "f(x) + 8", "2f(x)", "f((1/3)x)", "f(x − 7)")],
    59: [(180, 450, 400, 70, 24, "1/3"), (700, 450, 400, 70, 24, "−1/10"), (180, 720, 400, 70, 24, "5"),
         (700, 720, 400, 70, 24, "−4/5"), (180, 960, 400, 70, 24, "−1/c"), (700, 960, 400, 70, 24, "b/a")],
}

NOTES_T2_2 = {
    22: "Slide typo: the second item is labeled 'a.'; it is item b.",
    23: "Slide typo: both items are labeled 'a.'; they are items c and d.",
    41: "Counterexamples will vary: any linear function other than f(x) = x works, as long as students compare "
        "n·m(x) with m(nx).",
    46: "Slide typo: slides 46, 47, 49 and 50 number their item '1.'; they are items 2, 3, 5 and 6.",
    59: "TE correction: the TE prints the reciprocal of −10 as 1/10. It is −1/10, since (−10)(−1/10) = 1.",
}

CORRECTIONS_T2_2 = [
    ("Teacher Edition corrections in this deck", None),
    ("Prepare Q2: the TE gives the reciprocal of −10 as 1/10; it is −1/10.", None),
    ("Slide typos: slide 22's second item 'a.' is b; slide 23's two 'a.' items are c and d; slides 46, 47, 49 and "
     "50 are items 2, 3, 5 and 6, not '1.'", None),
    ("Every other TE answer was re-solved and is correct.", "16171D"),
]

# ---------------------------------------------------------------- Topic 2 Lesson 3: Determining Slopes of Perpendicular Lines

def rotated(x, a, b):  # one table column of the rotation table: A on row 1, B on row 2, one click
    return [(x, 883, 432, 62, 20, a, CENTER), (x, 945, 432, 62, 20, b, CENTER, WITH)]


ANS_T2_3 = {
    6: [*rotated(554, "A′(0, 0)", "B′(−5, 8)"), *rotated(986, "A″(0, 0)", "B″(−8, −5)"),
        *rotated(1418, "A‴(0, 0)", "B‴(5, −8)")],
    7: [(140, 380, 1700, 200, 20, "Each 90° counterclockwise rotation changes (x, y) to (−y, x): B(8, 5) → B′(−5, 8) "
                                  "→ B″(−8, −5) → B‴(5, −8). Endpoint A is the center of rotation, so it does not "
                                  "change."),
        (470, 740, 300, 60, 24, "m = 5/8"), (1120, 740, 400, 60, 24, "m = −8/5"),
        (470, 880, 300, 60, 24, "m = 5/8"), (1120, 880, 400, 60, 24, "m = −8/5")],
    8: [(616, 420, 1260, 300, 20, "AB and A″B″ (0° and 180°) have equal slopes, 5/8. A′B′ and A‴B‴ (90° and 270°) "
                                  "have equal slopes, −8/5. The two slopes are reciprocals with opposite signs: "
                                  "(5/8)(−8/5) = −1.")],
    13: [(122, 370, 1250, 150, 18, "Yes. Each line is rotated 90°, so the lines meet at a 90° angle, a right angle. "
                                   "Lines that form right angles are perpendicular."),
         (122, 620, 1280, 400, 20, "A: y = x;   A′: y = −x\nB: y = (1/3)x + 5;   B′: y = −3x + 5\n"
                                   "C: y = −(2/3)x + 9;   C′: y = (3/2)x − 4\n"
                                   "The slopes of each pair are reciprocals with opposite signs.")],
    17: [(122, 590, 1180, 470, 18, "Rotating R(a, b) 90° clockwise about O maps it onto line q at D(b, −a).\n"
                                   "Slope of p: m1 = b/a.   Slope of q: m2 = −a/b.\n"
                                   "−1/m2 = −1 ÷ (−a/b) = −1 · (b/−a) = b/a = m1, so m1 = −1/m2.\n"
                                   "The slopes are negative reciprocals.")],
    18: [(620, 430, 600, 60, 24, "m = −3/2"), (620, 656, 600, 60, 24, "m = 5/4"), (620, 872, 600, 60, 24, "m = 1/3")],
    22: [(122, 420, 1690, 260, 22, "Rotating a line 90° about a point maps (x, y) to (−y, x), so a slope b/a becomes "
                                   "−a/b. The slopes of perpendicular lines are negative reciprocals (their product "
                                   "is −1). Any vertical line is perpendicular to any horizontal line.")],
    24: [(880, 600, 1000, 300, 22, "Line p is the vertical line x = 4.\nLines q, r and s are the horizontal lines "
                                   "y = 4, y = 8 and y = 12.")],
    25: [(122, 430, 1700, 60, 22, "The value of y does not change: it changes by 0 units."),
         (122, 650, 1700, 150, 20, "The slope of any horizontal line is 0. The value of y stays the same, so "
                                   "m = (y2 − y1)/(x2 − x1) = 0/(x2 − x1) = 0.")],
    26: [(122, 380, 1700, 60, 22, "The value of x does not change: it changes by 0 units."),
         (122, 600, 1700, 150, 20, "The slope of any vertical line is undefined. The value of x stays the same, so "
                                   "m = (y2 − y1)/(x2 − x1) = (y2 − y1)/0, which is undefined.")],
    27: [(1010, 410, 880, 100, 18, "Always. All vertical lines have an undefined slope, so they are parallel."),
         (1010, 532, 880, 100, 18, "Always. All horizontal lines have slope 0, so they are parallel."),
         (122, 790, 1700, 80, 22, "Any vertical line and any horizontal line are always perpendicular.")],
    28: [(122, 372, 1700, 60, 22, "Horizontal line: y = −1;   vertical line: x = 2"),
         (122, 562, 1700, 60, 22, "y = 0  (a horizontal line through (1, 0))"),
         (122, 752, 1700, 60, 22, "x = 5  (a vertical line through (5, 6))")],
    32: [(540, 720, 1300, 340, 20, "The perpendicular slope is −1/2.\ny − 2 = −(1/2)(x − 6)\ny − 2 = −(1/2)x + 3\n"
                                   "y = −(1/2)x + 5")],
    33: [(140, 420, 1700, 200, 20, "The perpendicular slope is 4/3.\ny − (−8) = (4/3)(x − 3);   y + 8 = (4/3)x − 4;   "
                                   "y = (4/3)x − 12"),
         (140, 820, 1700, 240, 20, "m = (−9 − 3)/(−1 − (−5)) = −12/4 = −3, so the perpendicular slope is 1/3.\n"
                                   "y − 2 = (1/3)(x − 6);   y − 2 = (1/3)x − 2;   y = (1/3)x")],
    34: [(122, 430, 1700, 140, 20, "m = (4 − 1)/(0 − (−6)) = 3/6 = 1/2, so the perpendicular slope is −2.\n"
                                   "y − 7 = −2(x − (−2));   y − 7 = −2x − 4;   y = −2x + 3"),
         (122, 720, 1700, 200, 20, "m = (4 − 9)/(−4 − 5) = −5/−9 = 5/9, so the perpendicular slope is −9/5.\n"
                                   "y − 9 = −(9/5)(x − 5);   y − 9 = −(9/5)x + 9;   y = −(9/5)x + 18")],
    39: [(520, 740, 1060, 290, 18, "Jackson is correct. The axes have different scales. Lines a, b and c all have "
                                   "slope 1, so they are parallel. Lines d, e and f all have slope −1/4. Since "
                                   "1 · (−1/4) ≠ −1, the slopes are not negative reciprocals, so the lines are not "
                                   "perpendicular.")],
    43: [(1080, 425, 800, 60, 20, "Function: each input has exactly one output."),
         (1080, 559, 800, 60, 20, "Function: each input has exactly one output."),
         (1080, 693, 800, 60, 20, "Function: each input has exactly one output."),
         (1080, 827, 800, 60, 20, "Not a function: the input −1 has 4 different outputs.")],
}

NOTES_T2_3 = {
    24: "Read from the graph: G and K are on x = 4; H and G are on y = 4, F and J on y = 8, K and L on y = 12.",
    33: "TE wording slip (Q2): the TE says 'a line with a slope of 3/4'; the given line y = −(3/4)x has slope −3/4. "
        "The answer y = (4/3)x − 12 is correct. In Q3 to Q5 the TE writes the slope formula as (y2 − y1)/(y2 − y1); "
        "the denominator is x2 − x1. Its numbers are correct.",
    39: "The x-axis counts 1 unit per grid square and the y-axis 1 unit per 2 squares, so the lines look "
        "perpendicular but are not.",
}

CORRECTIONS_T2_3 = [
    ("Teacher Edition notes for this deck", None),
    ("Activity 3.3 Q2: the TE says the given line has slope 3/4; y = −(3/4)x has slope −3/4. Its answer, "
     "y = (4/3)x − 12, is correct.", None),
    ("Activity 3.3 Q3 to Q5: the TE prints the slope formula as (y2 − y1)/(y2 − y1); the denominator is x2 − x1. "
     "The computed slopes are correct.", None),
    ("Every TE answer was re-solved and is correct, including the Assignment (pp. 315-317) and Prepare.",
     "16171D"),
]

# ---------------------------------------------------------------- Topic 2 Lesson 4: Comparing Linear Functions in Different Forms

ANS_T2_4 = {
    7: [(122, 560, 800, 480, 18, "Sample answers: A (the table) is the only decreasing function (slope −2). D (the "
                                 "graph) is the only one whose y-intercept is not 0. C (the equation) is the only one "
                                 "with a slope between 0 and 1. B (the description) is the only one whose domain is "
                                 "whole numbers only.")],
    11: [(950, 740, 920, 120, 18, "b. The slope is −4. Neither parallel nor perpendicular to y = 4x − 3."),
         (720, 900, 1150, 120, 18, "a. The slope is 4. Parallel to y = 4x − 3.")],
    12: [(122, 400, 800, 150, 18, "c. The slope is 1/4. Neither parallel nor perpendicular to y = 4x − 3."),
         (1040, 800, 840, 150, 18, "d. The slope is 1/4. Neither parallel nor perpendicular to y = 4x − 3.")],
    13: [(212, 820, 700, 150, 18, "e. The slope is −1/4. Perpendicular to y = 4x − 3, since 4 · (−1/4) = −1."),
         (970, 420, 880, 150, 18, "f. The slope is 4 (dozen cookies per hour). Parallel to y = 4x − 3.")],
    18: [(122, 370, 1700, 70, 18, "Table and graph: x = weight of cardboard (tons); y = payout amount (dollars)."),
         (122, 720, 1700, 55, 24, "a. w(0.5) < j(0.5)     b. w(1) < j(1)     c. w(3) < j(3)"),
         (122, 790, 1700, 90, 18, "Travis pays $15 per ton: w(0.5) = 7.50, w(1) = 15, w(3) = 45. Hays pays $20 per "
                                  "ton: j(0.5) = 10, j(1) = 20, j(3) = 60.")],
    19: [(540, 420, 1340, 120, 18, "Both y-intercepts are 0: each center pays $0 for 0 tons of cardboard."),
         (540, 660, 1340, 150, 18, "Hays County: it pays $20 per ton, while Travis County pays only $15 per ton, "
                                   "so Hays pays more for any weight.")],
    23: [(122, 420, 1690, 420, 20,
          "Every representation (equation, table, graph or verbal description) shows the same key features: the "
          "slope or rate of change and the y-intercept or starting value. Compare functions by finding these in each "
          "form: equal slopes mean parallel lines, slopes with a product of −1 mean perpendicular lines, and the "
          "quantities and units tell what the slope and y-intercept mean in the situation.")],
    26: [(860, 760, 1000, 100, 18, "Joey's table columns: degrees Fahrenheit (left), degrees Celsius (right)")],
    27: [(122, 440, 1300, 120, 17, "Xavier's equation: x is degrees Celsius and J(x) is degrees Fahrenheit, so Xavier "
                                   "converts °C to °F. Joey's table converts °F to °C (50°F = 10°C)."),
         (122, 760, 620, 300, 16, "a. Joey's slope is about 5/9: each 9°F increase is about a 5°C increase. "
                                  "Xavier's slope is 9/5: each 5°C increase is a 9°F increase."),
         (760, 760, 640, 300, 16, "b. Joey's y-intercept is about −17.8: 0°F is about −17.8°C. Xavier's "
                                  "y-intercept is 32: 0°C is 32°F.")],
    32: [(490, 420, 1380, 140, 17, "Miguel saves the same amount each month and has $80 after 4 months, so the "
                                   "x-axis ticks are 1 month each and the y-axis ticks are $20 each. The origin is "
                                   "(0 months, $0 saved)."),
         (560, 760, 640, 300, 16, "a. Miguel's slope is 20: he saves $20 each month. Lauren's slope is 25: she "
                                  "saves $25 each month."),
         (1220, 760, 640, 300, 16, "b. Miguel's y-intercept is 0: he started with $0. Lauren's y-intercept is 25: "
                                   "she started with $25.")],
    36: [(140, 650, 1700, 100, 18, "Sample: Alejandra has read 2.5 pages of a book and reads 2.5 more pages every "
                                   "10 minutes (x = minutes from now, y = pages read). The slope is 1/4."),
         (140, 860, 1700, 70, 20, "Sample: y = 0.2x + 30 (slope 0.2 < 0.25)")],
    37: [(122, 450, 1050, 200, 17, "Sample: the graphed line has slope 1/3 ≈ 0.333 (through (0, −4) and (3, −3)). "
                                   "It is steeper than the table (1/4) and my equation (0.2)."),
         (122, 670, 1050, 200, 17, "Answers will vary: for example, finding the rate of change from two points and "
                                   "comparing the absolute values of the slopes.")],
    41: [(700, 395, 400, 60, 24, "x = 24"), (700, 559, 400, 60, 24, "x = 7.7"), (700, 705, 400, 60, 24, "x = 7.5"),
         (700, 855, 400, 60, 24, "x = 13")],
}

NOTES_T2_4 = {
    7: "Any choice is correct if the justification is. Function B (ratio 1 : 1) has slope 1; Function D passes "
       "through (0, 5).",
    31: "Slide typo: the introduction says 'Michelle opened her bank account'; the person is Lauren.",
    36: "TE wording slip: the TE's sample says Alejandra is 'at the middle of page 2'. Having read 2.5 pages puts her "
        "in the middle of page 3, so the situation here says 'has read 2.5 pages'.",
}

CORRECTIONS_T2_4 = [
    ("Teacher Edition notes for this deck", None),
    ("Slide typo: slide 31 calls Lauren 'Michelle'.", None),
    ("Talk the Talk Q1: the TE's sample starts Alejandra 'at the middle of page 2'; y = 2.5 pages read is the middle "
     "of page 3.", None),
    ("Every TE answer was re-solved and is correct, including the Assignment (pp. 327-330) and Prepare.", "16171D"),
]

TOPIC2 = HERE / "Module 2 topic 2"
PPTX_T2 = {1: (ANS_T2_1, NOTES_T2_1, CORRECTIONS_T2_1, 67),
           2: (ANS_T2_2, NOTES_T2_2, CORRECTIONS_T2_2, 57),
           3: (ANS_T2_3, NOTES_T2_3, CORRECTIONS_T2_3, 41),
           4: (ANS_T2_4, NOTES_T2_4, CORRECTIONS_T2_4, 39)}  # Topic 2 lesson -> as PPTX


if __name__ == "__main__":
    for arg in sys.argv[1:] or ["4", *map(str, PPTX), *(f"2.{n}" for n in PPTX_T2)]:
        if arg.startswith("2."):  # Topic 2 lessons: python make_lesson_key.py 2.1
            src = TOPIC2 / f"BLMathematics_AlgI_M2_T2_L{arg[2:]}_LessonSlides_ENG_2025.pptx"
            annotate(src, src.with_name(src.name.replace("2025", "with_answers")), *PPTX_T2[int(arg[2:])])
            continue
        lesson = int(arg)
        if lesson == 4:
            pages = render(PDF, Path(tempfile.mkdtemp()))
            assert len(pages) >= max(ANS4), f"PDF rendered {len(pages)} pages; answers expect {max(ANS4)}"
            build(pages)
            continue
        src = HERE / f"lesson{lesson}" / f"BLMathematics_AlgI_M2_T1_L{lesson}_LessonSlides_ENG_2025.pptx"
        annotate(src, src.with_name(f"BLMathematics_AlgI_M2_T1_L{lesson}_LessonSlides_ENG_with_answers.pptx"),
                 *PPTX[lesson])

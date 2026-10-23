"""Build a .pptx next to an HTML deck (default: lesson4/point-slope-form-lesson4.html).

The HTML deck is the single source: every element with class "step" becomes an
appear-on-click animation, <aside class="notes"> becomes the speaker notes.
Standard library only.  Run:  python make_pptx.py [lessonN/deck.html]
"""
import html
import json
import math
import re
import sys
import urllib.parse
import zipfile
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).parent
SRC = (HERE / (sys.argv[1] if len(sys.argv) > 1 else "lesson4/point-slope-form-lesson4.html")).resolve()
OUT = SRC.with_suffix(".pptx")
try:  # base for the deck's relative links
    SITE = "https://algebra1m2u1l4.vercel.app/" + SRC.parent.relative_to(HERE.resolve()).as_posix() + "/"
except ValueError:  # deck outside this repo (e.g. run from the Claude skill): links resolve beside the deck
    SITE = ""
LINKS = {}  # url -> rId for the slide being built; reset per slide

# Slide is 13.333 x 7.5 in; the HTML stage is 1280 x 720 px, so 96 px = 1 in.
EMU = 914400
SW, SH = 13.333, 7.5
PAD_X, PAD_TOP = 72 / 96, 48 / 96

# Bluebonnet Algebra I palette, matching the deck's :root tokens.
C = dict(ink="16171D", muted="5F6272", slope="C9561F", point="3050B8", ans="4F8A3C",
         ans_bg="EDF5E9", warn_bg="FDF3E7", card="FFFFFF", line="E3E4EC", rule="E6E8F2",
         paper="F7F7FB", ga="4F8A3C", gb="7A4FC4", gc="16171D")
BODY, MATH = "Segoe UI", "Cambria"

# ---------------------------------------------------------------- HTML -> tree
VOID = {"br", "link", "meta", "img", "hr", "input"}


class Node:
    def __init__(self, tag, attrs):
        self.tag, self.attrs, self.kids = tag, dict(attrs), []
        self.cls = set(self.attrs.get("class", "").split())
        self.style = dict(
            (k.strip(), v.strip()) for k, v in
            (d.split(":", 1) for d in self.attrs.get("style", "").split(";") if ":" in d))

    def els(self):
        return [k for k in self.kids if isinstance(k, Node)]

    def text(self):
        return "".join(k if isinstance(k, str) else k.text() for k in self.kids)


class Tree(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("root", [])
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs)
        self.stack[-1].kids.append(n)
        if tag not in VOID:
            self.stack.append(n)

    def handle_endtag(self, tag):
        for j in range(len(self.stack) - 1, 0, -1):
            if self.stack[j].tag == tag:
                del self.stack[j:]
                break

    def handle_data(self, data):
        self.stack[-1].kids.append(data)


def find_all(n, pred):
    out = []
    for k in n.els():
        if pred(k):
            out.append(k)
        out += find_all(k, pred)
    return out


def pxv(v):  # "30px" -> 30.0
    m = re.match(r"(-?[\d.]+)px", v or "")
    return float(m.group(1)) if m else None


# ---------------------------------------------------------------- text runs
def runs_of(node, st):
    out = []
    for k in node.kids:
        if isinstance(k, str):
            out.append([k, st])
            continue
        s = dict(st)
        if k.tag in ("b", "strong"):
            s["b"] = True
        if k.tag in ("i", "em"):
            s["i"] = True
        if k.tag == "sub":
            s["sub"] = True
        if k.tag == "a" and k.attrs.get("href"):
            s.update(href=k.attrs["href"], color=C["point"])
        if k.tag == "br":
            out.append(["\n", st])
            continue
        if "cm" in k.cls:
            s.update(color=C["slope"], b=True)
        if "cp" in k.cls:
            s.update(color=C["point"], b=True)
        if "muted" in k.cls:
            s["color"] = C["muted"]
        for g in ("ga", "gb", "gc"):
            if g in k.cls:
                s.update(color=C[g], b=True)
        if k.cls & {"eq", "mt"}:
            s["font"] = MATH
        if "sm" in k.cls and "eq" in k.cls:
            s["size"] = 31
        if "var(--body)" in k.style.get("font-family", ""):
            s["font"] = BODY
        if pxv(k.style.get("font-size")):
            s["size"] = pxv(k.style["font-size"])
        if "fr" in k.cls:
            num, den = k.els()[:2]
            parts = []
            for part in (num, den):
                r = runs_of(part, s)
                wrap = " " in part.text().strip()
                parts.append(([["(", s]] if wrap else []) + r + ([[")", s]] if wrap else []))
            out += parts[0] + [["/", s]] + parts[1]
            continue
        out += runs_of(k, s)
    return out


def clean_runs(runs):
    """Collapse HTML whitespace across run boundaries; trim block ends."""
    out, space = [], True
    for t, s in runs:
        if t == "\n":
            out.append(["\n", s]); space = True; continue
        t = re.sub(r"\s+", " ", t)
        if space:
            t = t.lstrip(" ")
        if not t:
            continue
        space = t.endswith(" ")
        out.append([t, s])
    while out and out[-1][0] != "\n" and out[-1][0].endswith(" "):
        out[-1][0] = out[-1][0].rstrip(" ")
        if not out[-1][0]:
            out.pop()
    return out


# ---------------------------------------------------------------- shapes
def esc(t):
    return html.escape(t, quote=True)


def emu(v):
    return int(round(v * EMU))


def rpr(s, base_size):
    size = s.get("size", base_size) * 0.75
    if s.get("sub"):
        size *= 0.85
    a = f'lang="en-US" sz="{int(round(size * 100))}" dirty="0"'
    a += ' b="1"' if s.get("b") else ""
    a += ' i="1"' if s.get("i") else ""
    a += ' baseline="-25000"' if s.get("sub") else ""
    a += f' spc="{s["spc"]}"' if s.get("spc") else ""
    a += ' cap="all"' if s.get("caps") else ""
    font = s.get("font", BODY)
    link = ""
    if s.get("href"):  # relative links point at the deployed site; rIds 1–2 are the layout and notes
        url = urllib.parse.urljoin(SITE, s["href"])
        link = f'<a:hlinkClick r:id="{LINKS.setdefault(url, f"rId{len(LINKS) + 3}")}"/>'
    return (f'<a:rPr {a}><a:solidFill><a:srgbClr val="{s.get("color", C["ink"])}"/></a:solidFill>'
            f'<a:latin typeface="{font}"/><a:cs typeface="{font}"/>{link}</a:rPr>')


def para_xml(runs, size, align):
    body = ""
    for t, s in runs:
        body += (f"<a:br>{rpr(s, size)}</a:br>" if t == "\n"
                 else f'<a:r>{rpr(s, size)}<a:t xml:space="preserve">{esc(t)}</a:t></a:r>')
    return (f'<a:p><a:pPr algn="{align}"><a:lnSpc><a:spcPct val="100000"/></a:lnSpc></a:pPr>{body}'
            f'<a:endParaRPr lang="en-US" sz="{int(size * 75)}" dirty="0"/></a:p>')


def sp_xml(sid, x, y, w, h, runs=None, size=26, align="l", fill=None, line=None, dash=False,
           geom="rect", ins=(0.04, 0.03), anchor="t", txbox=True):
    fill_x = f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>' if fill else "<a:noFill/>"
    if line:
        ln = (f'<a:ln w="{19050 if dash else 12700}"><a:solidFill><a:srgbClr val="{line}"/></a:solidFill>'
              + ('<a:prstDash val="dash"/>' if dash else "") + "</a:ln>")
    else:
        ln = "<a:ln><a:noFill/></a:ln>"
    av = '<a:avLst><a:gd name="adj" fmla="val 8000"/></a:avLst>' if geom == "roundRect" else "<a:avLst/>"
    li, ti = emu(ins[0]), emu(ins[1])
    txt = para_xml(runs or [], size, align)
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="Shape {sid}"/><p:cNvSpPr{' txBox="1"' if txbox else ''}/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm>'
            f'<a:prstGeom prst="{geom}">{av}</a:prstGeom>{fill_x}{ln}</p:spPr>'
            f'<p:txBody><a:bodyPr wrap="square" lIns="{li}" tIns="{ti}" rIns="{li}" bIns="{ti}" anchor="{anchor}">'
            f'<a:noAutofit/></a:bodyPr><a:lstStyle/>{txt}</p:txBody></p:sp>')


def num_xml(sid, n, x, y, cx, cy):
    """Page number (EMU box, right-aligned): a slidenum field, so PowerPoint renumbers it if slides move."""
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="Slide Number {sid}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr>'
            '<p:txBody><a:bodyPr wrap="none" lIns="0" tIns="0" rIns="0" bIns="0" anchor="b"><a:noAutofit/></a:bodyPr>'
            '<a:lstStyle/><a:p><a:pPr algn="r"/><a:fld id="{5C1A6E0B-3B1F-4D5E-9C7A-2F4B8D6E1A90}" type="slidenum">'
            f'<a:rPr lang="en-US" sz="1200" dirty="0"><a:solidFill><a:srgbClr val="{C["muted"]}"/></a:solidFill>'
            f'</a:rPr><a:t>{n}</a:t></a:fld></a:p></p:txBody></p:sp>')


def seg_xml(sid, x1, y1, x2, y2, color, width=9525, cap="flat", dash=False):
    if x2 < x1:
        x1, y1, x2, y2 = x2, y2, x1, y1
    flip = ' flipV="1"' if y2 < y1 else ""
    return (f'<p:cxnSp><p:nvCxnSpPr><p:cNvPr id="{sid}" name="Line {sid}"/><p:cNvCxnSpPr/><p:nvPr/></p:nvCxnSpPr>'
            f'<p:spPr><a:xfrm{flip}><a:off x="{emu(x1)}" y="{emu(min(y1, y2))}"/>'
            f'<a:ext cx="{emu(x2 - x1)}" cy="{emu(abs(y2 - y1))}"/></a:xfrm>'
            f'<a:prstGeom prst="line"><a:avLst/></a:prstGeom>'
            f'<a:ln w="{width}" cap="{cap}"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
            + ('<a:prstDash val="dash"/>' if dash else "") + '</a:ln></p:spPr></p:cxnSp>')


def line_xml(sid, x, y, w):
    return seg_xml(sid, x, y, x + w, y, C["line"])


# ---------------------------------------------------------------- graphs
# Same spec and geometry as graphSVG() in the HTML page (data-g attribute).
GM = dict(L=34, R=12, T=12, B=26)


def clip_line(p, xr, yr):
    (ax, ay), (bx, by) = p
    dx, dy = bx - ax, by - ay
    lo, hi = -math.inf, math.inf
    for q_p, q in ((-dx, ax - xr[0]), (dx, xr[1] - ax), (-dy, ay - yr[0]), (dy, yr[1] - ay)):
        if q_p == 0:
            if q < 0:
                return None
            continue
        r = q / q_p
        lo, hi = (max(lo, r), hi) if q_p < 0 else (lo, min(hi, r))
    return None if lo > hi else ((ax + lo * dx, ay + lo * dy), (ax + hi * dx, ay + hi * dy))


def ticks(a, b, t):
    v, out = math.ceil(a / t - 1e-9) * t, []
    while v <= b + 1e-9:
        out.append(round(v, 6))
        v += t
    return out


def num(v):
    return (str(int(v)) if float(v).is_integer() else str(v)).replace("-", "−")


def draw_graph(sl, g, ox, oy):
    """Draw graph spec g with its top-left at (ox, oy) inches; return height in inches."""
    W, H = g["w"], g["h"]
    (x0, x1), (y0, y1) = g["x"], g["y"]
    P = 1 / 96  # px -> in

    def X(v):
        return ox + (GM["L"] + (v - x0) / (x1 - x0) * (W - GM["L"] - GM["R"])) * P

    def Y(v):
        return oy + (GM["T"] + (y1 - v) / (y1 - y0) * (H - GM["T"] - GM["B"])) * P

    left, right, top, bot = ox + GM["L"] * P, ox + (W - GM["R"]) * P, oy + GM["T"] * P, oy + (H - GM["B"]) * P
    sl.add(lambda sid: sp_xml(sid, ox, oy, W * P, H * P, fill=C["card"], line=C["line"], geom="roundRect",
                              txbox=False))
    for v in ticks(x0, x1, g["gx"][0]):
        sl.add(lambda sid, v=v: seg_xml(sid, X(v), top, X(v), bot, C["rule"]))
    for v in ticks(y0, y1, g["gy"][0]):
        sl.add(lambda sid, v=v: seg_xml(sid, left, Y(v), right, Y(v), C["rule"]))
    ax = 0 if x0 <= 0 <= x1 else x0
    ay = 0 if y0 <= 0 <= y1 else y0
    sl.add(lambda sid: seg_xml(sid, X(ax), top, X(ax), bot, C["muted"], 19050))
    sl.add(lambda sid: seg_xml(sid, left, Y(ay), right, Y(ay), C["muted"], 19050))
    tick_st = dict(size=13, color=C["muted"])
    for v in ticks(x0, x1, g["gx"][1]):
        sl.add(lambda sid, v=v: sp_xml(sid, X(v) - 0.3, bot + 2 * P, 0.6, 0.2, [[num(v), tick_st]], 13, "ctr",
                                       ins=(0, 0)))
    for v in ticks(y0, y1, g["gy"][1]):
        sl.add(lambda sid, v=v: sp_xml(sid, left - 0.62, Y(v) - 0.1, 0.56, 0.2, [[num(v), tick_st]], 13, "r",
                                       ins=(0, 0), anchor="ctr"))
    def draw_points(own_steps=False):
        r = 5.5 * P
        for px_, py_, lab in g.get("pts", []):
            if own_steps and not sl.dry:
                sl.steps.append(("pop", [])); sl.open.append(len(sl.steps) - 1)
            sl.add(lambda sid, a=px_, b=py_: sp_xml(sid, X(a) - r, Y(b) - r, 2 * r, 2 * r, fill=C["point"],
                                                    geom="ellipse", txbox=False))
            if lab:
                sl.add(lambda sid, a=px_, b=py_, lab=lab: sp_xml(
                    sid, X(a) + 9 * P, Y(b) - 26 * P, 1.4, 0.22, [[lab, dict(size=15, b=True, color=C["point"])]],
                    15, "l", ins=(0, 0)))
            if own_steps and not sl.dry:
                sl.open.pop()

    if g.get("ptsStep"):  # each point appears on its own click, before the lines
        draw_points(own_steps=True)
    for ln in g.get("lines", []):
        c = ln["p"] if ln.get("seg") else clip_line(ln["p"], g["x"], g["y"])  # seg: just this segment
        if not c:
            continue
        own_step = ln.get("step") and not sl.dry
        if own_step:  # this line appears on its own click, drawn left to right
            sl.steps.append(("wipe", [])); sl.open.append(len(sl.steps) - 1)
        color = C["g" + ln["c"]] if ln.get("c") else C["ink"]
        sl.add(lambda sid, c=c, color=color, dash=ln.get("dash", False): seg_xml(
            sid, X(c[0][0]), Y(c[0][1]), X(c[1][0]), Y(c[1][1]), color, 38100, "rnd", dash))
        if ln.get("label"):
            e = c[0] if c[0][1] > c[1][1] else c[1]
            st = dict(size=17, i=True, font=MATH)
            if X(e[0]) > ox + W * P / 2:
                sl.add(lambda sid, e=e: sp_xml(sid, X(e[0]) - 12 * P - 2.6, Y(e[1]) + 2 * P, 2.6, 0.25,
                                               [[ln["label"], st]], 17, "r", ins=(0, 0)))
            else:
                sl.add(lambda sid, e=e: sp_xml(sid, X(e[0]) + 8 * P, Y(e[1]) + 2 * P, 2.6, 0.25,
                                               [[ln["label"], st]], 17, "l", ins=(0, 0)))
        if ln.get("dot"):  # a point at the segment's end, on the same click
            r = 5.5 * P
            sl.add(lambda sid, e=c[1]: sp_xml(sid, X(e[0]) - r, Y(e[1]) - r, 2 * r, 2 * r, fill=C["point"],
                                              geom="ellipse", txbox=False))
        if own_step:
            sl.open.pop()
    if not g.get("ptsStep"):
        draw_points()
    return H * P


# ---------------------------------------------------------------- layout
def est_lines(runs, size, width, font):
    em = 0.52 if font == MATH else 0.49
    per_line = max(1.0, width * 72 / (size * 0.75 * em))
    text = "".join(t for t, _ in runs)
    return sum(max(1, math.ceil(len(seg) / per_line)) for seg in text.split("\n")), text


class Slide:
    def __init__(self):
        self.shapes, self.steps, self.open, self.dry, self.next_id = [], [], [], 0, 2

    def add(self, xml_fn):
        if self.dry:
            return
        sid = self.next_id
        self.next_id += 1
        self.shapes.append(xml_fn(sid))
        if self.open:
            self.steps[self.open[-1]][1].append(sid)
        return len(self.shapes) - 1


TEXT_TAGS = {"p", "h1", "h2", "h3", "td", "th"}
BLOCK_SIZE = [("eyebrow", 16), ("foot", 15), ("small", 21), ("warn", 22), ("think", 25)]


def block_size(n, fs):
    if pxv(n.style.get("font-size")):
        return pxv(n.style["font-size"])
    if n.tag == "h1":
        return 110 if fs == "divider" else 76
    if n.tag == "h2":
        return 46
    if n.tag == "h3":
        return 28
    if "eq" in n.cls:
        return 60 if "big" in n.cls else 31 if "sm" in n.cls else 38
    for c, v in BLOCK_SIZE:
        if c in n.cls:
            return v
    return fs


def text_block(sl, n, x, y, w, fs, align="l", forced_w=None):
    size = block_size(n, fs)
    size = size if isinstance(size, (int, float)) else 26
    st = {"size": size}
    if n.tag in ("h1", "h2", "h3"):
        st["b"] = True
    if "eq" in n.cls:
        st["font"] = MATH
    if "eyebrow" in n.cls:
        st.update(b=True, caps=True, spc=150, color=C["muted"])
    if n.cls & {"muted", "foot"}:
        st["color"] = C["muted"]
    runs = clean_runs(runs_of(n, st))
    fill = line = None
    dash, geom, ins, anchor = False, "rect", (0.04, 0.03), "t"
    if "ans" in n.cls:
        runs = [["ANSWER   ", dict(size=15, b=True, spc=100, color=C["ans"], font=BODY)]] + runs
        fill, geom, ins, anchor = C["ans_bg"], "roundRect", (0.18, 0.07), "ctr"
    elif "warn" in n.cls:
        fill, geom, ins, anchor = C["warn_bg"], "roundRect", (0.18, 0.08), "ctr"
    elif "think" in n.cls:
        line, dash, geom, ins, anchor = C["point"], True, "roundRect", (0.25, 0.12), "ctr"
    elif "card" in n.cls:
        fill, line, geom, ins = C["card"], C["line"], "roundRect", (0.22, 0.17)
    boxed = fill or line
    font = st.get("font", BODY)
    if boxed and forced_w is None:  # shrink-wrap like CSS align-self:flex-start
        _, text = est_lines(runs, size, 99, font)
        longest = max(len(s) for s in text.split("\n"))
        em = 0.52 if font == MATH else 0.49
        w = min(w, longest * size * 0.75 * em / 72 * 1.08 + 2 * ins[0] + 0.1)
    if "think" in n.cls and pxv(n.style.get("max-width")) is None:
        w = min(w, 760 / 96)
    lines, _ = est_lines(runs, size, w - 2 * ins[0] - 0.05, font)
    h = lines * size * 0.75 * 1.2 / 72 + 2 * ins[1]
    if "ans" in n.cls:
        h += 0.04
    sl.add(lambda sid: sp_xml(sid, x, y, w, h, runs, size, align, fill, line, dash, geom, ins, anchor))
    return h


def gap_of(n, default):
    g = n.style.get("gap")
    if g:
        v = [pxv(p) for p in g.split()]
        return (v[0] / 96, (v[1] if len(v) > 1 else v[0]) / 96)
    return (default / 96, default / 96)


def tbl_size(n):
    return pxv(n.style.get("font-size")) or 30


def tbl_cols(n):  # each column fits its longest cell, at least 1.25 in
    rows = [r.els() for r in find_all(n, lambda k: k.tag == "tr")]
    per = tbl_size(n) * 0.75 * 0.52 / 72
    return [max([1.25] + [len(r[c].text().strip()) * per + 0.6 for r in rows if c < len(r)])
            for c in range(len(rows[0]))] if rows else [2.5]


def table_width(n):
    return sum(tbl_cols(n))


def lay_table(sl, n, x, y, w, fs):
    rows = find_all(n, lambda k: k.tag == "tr")
    ncol = len(rows[0].els())
    small = "tbl" in n.cls
    if small:
        widths = tbl_cols(n)
        w = sum(widths)
    else:
        frac = [0.2, 0.4, 0.4] if ncol == 3 else [0.45, 0.55]
        widths = [w * f for f in frac]
    top = y
    for r in rows:
        step = "step" in r.cls and not sl.dry
        if step:
            sl.steps.append(("rise", [])); sl.open.append(len(sl.steps) - 1)
        cells = r.els()
        size = tbl_size(n) if small else (26 if cells[0].tag == "th" else 24)
        hs = []
        for c, cw in zip(cells, widths):
            st = {"size": size, "font": MATH if small or "eq" in c.cls else BODY}
            if c.tag == "th":
                st.update(b=not small, i=small and c.style.get("font-style") != "normal")
            if "muted" in c.cls:
                st["color"] = C["muted"]
            runs = clean_runs(runs_of(c, st))
            lines, _ = est_lines(runs, size, cw - 0.3, st["font"])
            hs.append((runs, st, lines))
        rh = max(l for _, _, l in hs) * size * 0.75 * 1.2 / 72 + (0.16 if small else 0.22)
        cx = x
        for (runs, st, _), cw, c in zip(hs, widths, cells):
            fill = (C["rule"] if c.tag == "th" else C["card"]) if small else None
            ln = C["line"] if small else None
            cstep = "step" in c.cls and not sl.dry  # a single cell's text can appear on its own click
            if cstep:  # draw the empty cell now so the table has no hole
                sl.add(lambda sid, cx=cx, cw=cw, fill=fill, ln=ln, size=size: sp_xml(
                    sid, cx, y, cw, rh, None, size, "ctr", fill, ln))
                fill = ln = None
                sl.steps.append(("rise", [])); sl.open.append(len(sl.steps) - 1)
            sl.add(lambda sid, cx=cx, cw=cw, runs=runs, fill=fill, ln=ln, size=size: sp_xml(
                sid, cx, y, cw, rh, runs, size, "ctr" if small else "l", fill, ln, ins=(0.12, 0.05),
                anchor="ctr"))
            if cstep:
                sl.open.pop()
            cx += cw
        if not small:
            sl.add(lambda sid, yy=y + rh: line_xml(sid, x, yy, w))
        y += rh
        if step:
            sl.open.pop()
    return y - top, w


def lay(sl, n, x, y, w, fs, forced_h=None):
    """Lay out node n at (x, y) within width w; return its height."""
    if n.tag == "aside" or "foot" in n.cls:
        return None
    if pxv(n.style.get("font-size")):
        fs = pxv(n.style["font-size"])
    y += (pxv(n.style.get("margin-top")) or 0) / 96
    step = "step" in n.cls and not sl.dry
    if step:
        kind = "wipe" if "wipe" in n.cls else "pop" if "pop" in n.cls else "rise"
        sl.steps.append((kind, [])); sl.open.append(len(sl.steps) - 1)
    mt = (pxv(n.style.get("margin-top")) or 0) / 96

    if "graph" in n.cls:
        h = draw_graph(sl, json.loads(n.attrs["data-g"]), x, y)
    elif n.tag == "table":
        h, _ = lay_table(sl, n, x, y, w, fs)
    elif n.tag in TEXT_TAGS or n.cls & {"eq", "ans", "think"}:
        h = text_block(sl, n, x, y, w, fs)
    elif "card" in n.cls:
        px_, py_ = 22 / 96, 18 / 96
        at = len(sl.shapes)
        inner = stack(sl, n, x + px_, y + py_, w - 2 * px_, fs, gap_of(n, 10)[0])
        h = max(inner + 2 * py_, forced_h or 0)
        if not sl.dry:
            sid = sl.next_id; sl.next_id += 1
            sl.shapes.insert(at, sp_xml(sid, x, y, w, h, fill=C["card"], line=C["line"], geom="roundRect"))
            if sl.open:
                sl.steps[sl.open[-1]][1].insert(0, sid)
    elif "row" in n.cls:
        kids = [k for k in n.els() if k.tag != "aside"]
        g = gap_of(n, 36)[1]
        fixed = {id(k): table_width(k) for k in kids if k.tag == "table" and "tbl" in k.cls}
        fixed.update({id(k): json.loads(k.attrs["data-g"])["w"] / 96 for k in kids if "graph" in k.cls})
        flex_w = (w - sum(fixed.values()) - g * (len(kids) - 1)) / max(1, len(kids) - len(fixed))
        cx, h = x, 0
        for k in kids:
            kw = fixed.get(id(k), flex_w)
            h = max(h, lay(sl, k, cx, y, kw, fs) or 0)
            cx += kw + g
    elif "grid3" in n.cls:
        kids = n.els()
        gr, gc = gap_of(n, 18)
        cw = (w - 2 * gc) / 3
        h = 0
        for r0 in range(0, len(kids), 3):
            row = kids[r0:r0 + 3]
            sl.dry += 1
            rh = max(lay(sl, k, 0, 0, cw, fs) or 0 for k in row)
            sl.dry -= 1
            for j, k in enumerate(row):
                lay(sl, k, x + j * (cw + gc), y + h, cw, fs, forced_h=rh)
            h += rh + gr
        h -= gr
    else:  # section, .col, plain div
        h = stack(sl, n, x, y, w, fs, gap_of(n, 18 if n.tag == "section" else 14)[0])
    if step:
        sl.open.pop()
    return h + mt


def stack(sl, n, x, y, w, fs, gap):
    top = y
    for k in n.els():
        h = lay(sl, k, x, y, w, fs)
        if h is not None:
            y += h + gap
    return max(0, y - top - gap)


# ---------------------------------------------------------------- animation
def timing_xml(steps):
    steps = [s for s in steps if s[1]]
    if not steps:
        return ""
    ids = iter(range(3, 100000))
    clicks = ""
    for kind, sids in steps:
        effects = ""
        for j, sid in enumerate(sids):
            tgt = f'<p:tgtEl><p:spTgt spid="{sid}"/></p:tgtEl>'
            vis = (f'<p:set><p:cBhvr><p:cTn id="{next(ids)}" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/>'
                   f'</p:stCondLst></p:cTn>{tgt}<p:attrNameLst><p:attrName>style.visibility</p:attrName>'
                   f'</p:attrNameLst></p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set>')
            if kind == "wipe":
                preset, sub = 22, 8
                body = (f'<p:animEffect transition="in" filter="wipe(left)"><p:cBhvr><p:cTn id="{next(ids)}" '
                        f'dur="700"/>{tgt}</p:cBhvr></p:animEffect>')
            else:
                fade = (f'<p:animEffect transition="in" filter="fade"><p:cBhvr><p:cTn id="{next(ids)}" '
                        f'dur="500"/>{tgt}</p:cBhvr></p:animEffect>')

                def val(v):
                    return f'<p:fltVal val="{v}"/>' if re.fullmatch(r"[\d.]+", v) else f'<p:strVal val="{v}"/>'

                def anim(attr, frm, to):
                    return (f'<p:anim calcmode="lin" valueType="num"><p:cBhvr><p:cTn id="{next(ids)}" dur="500" '
                            f'fill="hold"/>{tgt}<p:attrNameLst><p:attrName>{attr}</p:attrName></p:attrNameLst>'
                            f'</p:cBhvr><p:tavLst><p:tav tm="0"><p:val>{val(frm)}</p:val></p:tav>'
                            f'<p:tav tm="100000"><p:val><p:strVal val="{to}"/></p:val></p:tav></p:tavLst></p:anim>')
                if kind == "pop":  # Zoom
                    preset, sub = 53, 16
                    body = fade + anim("ppt_w", "0", "#ppt_w") + anim("ppt_h", "0", "#ppt_h")
                else:  # Float In
                    preset, sub = 42, 0
                    body = fade + anim("ppt_x", "#ppt_x", "#ppt_x") + anim("ppt_y", "#ppt_y+.1", "#ppt_y")
            node = "clickEffect" if j == 0 else "withEffect"
            effects += (f'<p:par><p:cTn id="{next(ids)}" presetID="{preset}" presetClass="entr" '
                        f'presetSubtype="{sub}" fill="hold" nodeType="{node}"><p:stCondLst><p:cond delay="0"/>'
                        f'</p:stCondLst><p:childTnLst>{vis}{body}</p:childTnLst></p:cTn></p:par>')
        clicks += (f'<p:par><p:cTn id="{next(ids)}" fill="hold"><p:stCondLst><p:cond delay="indefinite"/>'
                   f'</p:stCondLst><p:childTnLst><p:par><p:cTn id="{next(ids)}" fill="hold"><p:stCondLst>'
                   f'<p:cond delay="0"/></p:stCondLst><p:childTnLst>{effects}</p:childTnLst></p:cTn></p:par>'
                   f'</p:childTnLst></p:cTn></p:par>')
    return ('<p:timing><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot">'
            '<p:childTnLst><p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq">'
            f'<p:childTnLst>{clicks}</p:childTnLst></p:cTn><p:prevCondLst><p:cond evt="onPrev" delay="0">'
            '<p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst><p:nextCondLst><p:cond evt="onNext" '
            'delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst></p:seq></p:childTnLst></p:cTn>'
            '</p:par></p:tnLst></p:timing>')


# ---------------------------------------------------------------- package parts
NS = ('xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
      'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"')
HDR = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/"
CT = "application/vnd.openxmlformats-officedocument.presentationml."
GRP = ('<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm>'
       '<a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm>'
       '</p:grpSpPr>')
CLRMAP = ('bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" '
          'accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"')


def rels(items, links=None):
    body = "".join(f'<Relationship Id="{i}" Type="{REL}{t}" Target="{tg}"/>' for i, t, tg in items)
    body += "".join(f'<Relationship Id="{i}" Type="{REL}hyperlink" Target="{esc(u)}" TargetMode="External"/>'
                    for u, i in (links or {}).items())
    return HDR + f'<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">{body}</Relationships>'


def theme(name):
    def clr(n, v):
        return f'<a:{n}><a:srgbClr val="{v}"/></a:{n}>'
    colors = (clr("dk1", C["ink"]) + clr("lt1", "FFFFFF") + clr("dk2", "233D94") + clr("lt2", C["paper"]) +
              clr("accent1", C["slope"]) + clr("accent2", C["point"]) + clr("accent3", C["ans"]) +
              clr("accent4", "7A5AC8") + clr("accent5", "C23B6B") + clr("accent6", "4F8A3C") +
              clr("hlink", C["point"]) + clr("folHlink", "7A5AC8"))
    solid = '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
    ln = f'<a:ln w="9525" cap="flat" cmpd="sng" algn="ctr">{solid}<a:prstDash val="solid"/></a:ln>'
    return (HDR + f'<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="{name}">'
            f'<a:themeElements><a:clrScheme name="Lesson">{colors}</a:clrScheme>'
            f'<a:fontScheme name="Lesson"><a:majorFont><a:latin typeface="{BODY}"/><a:ea typeface=""/>'
            f'<a:cs typeface=""/></a:majorFont><a:minorFont><a:latin typeface="{BODY}"/><a:ea typeface=""/>'
            f'<a:cs typeface=""/></a:minorFont></a:fontScheme>'
            f'<a:fmtScheme name="Lesson"><a:fillStyleLst>{solid * 3}</a:fillStyleLst>'
            f'<a:lnStyleLst>{ln * 3}</a:lnStyleLst>'
            f'<a:effectStyleLst>{"<a:effectStyle><a:effectLst/></a:effectStyle>" * 3}</a:effectStyleLst>'
            f'<a:bgFillStyleLst>{solid * 3}</a:bgFillStyleLst></a:fmtScheme></a:themeElements>'
            '<a:objectDefaults/><a:extraClrSchemeLst/></a:theme>')


def notes_xml(text):
    paras = "".join(f'<a:p><a:r><a:rPr lang="en-US" dirty="0"/><a:t>{esc(t)}</a:t></a:r></a:p>'
                    for t in text.split("\n") if t.strip()) or '<a:p><a:endParaRPr lang="en-US"/></a:p>'
    return (HDR + f'<p:notes {NS}><p:cSld><p:spTree>{GRP}'
            '<p:sp><p:nvSpPr><p:cNvPr id="2" name="Slide Image Placeholder 1"/><p:cNvSpPr><a:spLocks noGrp="1" '
            'noRot="1" noChangeAspect="1"/></p:cNvSpPr><p:nvPr><p:ph type="sldImg"/></p:nvPr></p:nvSpPr>'
            '<p:spPr/></p:sp><p:sp><p:nvSpPr><p:cNvPr id="3" name="Notes Placeholder 2"/><p:cNvSpPr>'
            '<a:spLocks noGrp="1"/></p:cNvSpPr><p:nvPr><p:ph type="body" idx="1"/></p:nvPr></p:nvSpPr>'
            f'<p:spPr/><p:txBody><a:bodyPr/><a:lstStyle/>{paras}</p:txBody></p:sp></p:spTree></p:cSld>'
            '<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:notes>')


NOTES_MASTER = (
    HDR + f'<p:notesMaster {NS}><p:cSld><p:bg><p:bgRef idx="1001"><a:schemeClr val="bg1"/></p:bgRef></p:bg>'
    f'<p:spTree>{GRP}'
    '<p:sp><p:nvSpPr><p:cNvPr id="2" name="Slide Image Placeholder 1"/><p:cNvSpPr><a:spLocks noGrp="1" '
    'noRot="1" noChangeAspect="1"/></p:cNvSpPr><p:nvPr><p:ph type="sldImg" idx="2"/></p:nvPr></p:nvSpPr>'
    '<p:spPr><a:xfrm><a:off x="685800" y="1143000"/><a:ext cx="5486400" cy="3086100"/></a:xfrm>'
    '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln w="12700"><a:solidFill><a:prstClr '
    'val="black"/></a:solidFill></a:ln></p:spPr></p:sp>'
    '<p:sp><p:nvSpPr><p:cNvPr id="3" name="Notes Placeholder 2"/><p:cNvSpPr><a:spLocks noGrp="1"/>'
    '</p:cNvSpPr><p:nvPr><p:ph type="body" sz="quarter" idx="3"/></p:nvPr></p:nvSpPr><p:spPr><a:xfrm>'
    '<a:off x="685800" y="4400550"/><a:ext cx="5486400" cy="3600450"/></a:xfrm><a:prstGeom prst="rect">'
    '<a:avLst/></a:prstGeom></p:spPr><p:txBody><a:bodyPr vert="horz" lIns="91440" tIns="45720" rIns="91440" '
    'bIns="45720" rtlCol="0"/><a:lstStyle/><a:p><a:pPr lvl="0"/><a:r><a:rPr lang="en-US"/><a:t>Notes</a:t>'
    '</a:r></a:p></p:txBody></p:sp></p:spTree></p:cSld>'
    f'<p:clrMap {CLRMAP}/><p:notesStyle><a:lvl1pPr marL="0" algn="l" defTabSz="914400" rtl="0" eaLnBrk="1" '
    'latinLnBrk="0" hangingPunct="1"><a:defRPr sz="1400" kern="1200"><a:solidFill><a:schemeClr val="tx1"/>'
    '</a:solidFill><a:latin typeface="+mn-lt"/><a:ea typeface="+mn-ea"/><a:cs typeface="+mn-cs"/></a:defRPr>'
    '</a:lvl1pPr></p:notesStyle></p:notesMaster>')

def brand_xml(x, y, s=0.3):
    """Bluebonnet Algebra I mark + wordmark (same drawing as the deck's #brand SVG, 32-unit grid)."""
    u = s / 32
    out, sid = [], 100

    def shape(geom, gx, gy, gw, gh, color, adj=None, alpha=None):
        nonlocal sid
        sid += 1
        av = f'<a:avLst><a:gd name="adj" fmla="val {adj}"/></a:avLst>' if adj else "<a:avLst/>"
        a = f'<a:alpha val="{alpha}"/>' if alpha else ""
        out.append(f'<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="Brand {sid}"/><p:cNvSpPr/><p:nvPr userDrawn="1"/></p:nvSpPr>'
                   f'<p:spPr><a:xfrm><a:off x="{emu(x + gx * u)}" y="{emu(y + gy * u)}"/>'
                   f'<a:ext cx="{emu(gw * u)}" cy="{emu(gh * u)}"/></a:xfrm><a:prstGeom prst="{geom}">{av}</a:prstGeom>'
                   f'<a:solidFill><a:srgbClr val="{color}">{a}</a:srgbClr></a:solidFill><a:ln><a:noFill/></a:ln></p:spPr></p:sp>')

    shape("roundRect", 0, 0, 32, 32, "3050B8", adj=25000)
    for cx, cy, r, al in [(16, 7.5, 2.3, None), (12.8, 11.8, 2.5, 92000), (19.2, 11.8, 2.5, 92000),
                          (16, 14.6, 2.6, None), (11.8, 17.6, 2.7, 82000), (20.2, 17.6, 2.7, 82000)]:
        shape("ellipse", cx - r, cy - r, 2 * r, 2 * r, "FFFFFF", alpha=al)
    shape("roundRect", 15.2, 20.5, 1.6, 6.5, "9FD18B", adj=50000)
    out.append(sp_xml(sid + 1, x + s + 0.06, y - 0.02, 1.9, s + 0.04,
                      [["Bluebonnet ", dict(size=15, color=C["ink"])],
                       ["Algebra I", dict(size=15, b=True, color=C["point"])]],
                      size=15, anchor="ctr", ins=(0.02, 0)))
    return "".join(out)


MASTER = (
    HDR + f'<p:sldMaster {NS}><p:cSld><p:bg><p:bgPr><a:pattFill prst="lgGrid"><a:fgClr><a:srgbClr '
    f'val="{C["rule"]}"/></a:fgClr><a:bgClr><a:srgbClr val="{C["paper"]}"/></a:bgClr></a:pattFill>'
    # Brand sits in the top-right margin, above PAD_TOP where slide content starts.
    f'<a:effectLst/></p:bgPr></p:bg><p:spTree>{GRP}{brand_xml(SW - PAD_X - 2.05, 0.14)}</p:spTree></p:cSld><p:clrMap {CLRMAP}/>'
    '<p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst></p:sldMaster>')

LAYOUT = (HDR + f'<p:sldLayout {NS} type="blank" preserve="1"><p:cSld name="Blank"><p:spTree>{GRP}'
          '</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>')


def build():
    src = SRC.read_text(encoding="utf-8")
    # same fraction shorthand the HTML page expands at load
    src = re.sub(r"\{\{(.+?)\|(.+?)\}\}", r'<span class="fr"><span>\1</span><span>\2</span></span>', src)
    title = re.search(r"<title>(.*?)</title>", src).group(1).split(" · ")[0]
    t = Tree()
    t.feed(src)
    sections = find_all(t.root, lambda n: n.tag == "section" and "slide" in n.cls)

    slides, warnings = [], []
    for k, sec in enumerate(sections, 1):
        LINKS.clear()
        sl = Slide()
        top = 2.3 if "divider" in sec.cls else PAD_TOP
        fs = "divider" if "divider" in sec.cls else 26
        if fs == "divider" and top + divider(Slide(), sec, top) > SH - 0.3:
            top, fs = 1.0, 76  # long divider (e.g. dated Start/Stop slides): start higher, smaller title
        h = stack(sl, sec, PAD_X, top, SW - 2 * PAD_X, 26, 18 / 96) if fs == 26 \
            else divider(sl, sec, top, fs)
        foot = next((n for n in sec.els() if "foot" in n.cls), None)
        if foot:  # bottom-aligned: measure on a scratch slide, then place so it ends 0.3 in from the edge
            fh = text_block(Slide(), foot, PAD_X, 0, SW - 2 * PAD_X, 15)
            text_block(sl, foot, PAD_X, SH - 0.3 - fh, SW - 2 * PAD_X, 15)
        sl.add(lambda sid: num_xml(sid, k, emu(SW - 1.0), emu(SH - 0.27), emu(0.75), emu(0.22)))  # under the foot line
        if top + h > SH - 0.3:
            warnings.append(f"slide {k}: content may run to {top + h:.2f} in (slide is {SH} in tall)")
        aside = next((n for n in sec.els() if n.tag == "aside"), None)
        notes = re.sub(r"\s+", " ", aside.text()).strip() if aside else ""
        body = "".join(sl.shapes)
        xml = (HDR + f'<p:sld {NS}><p:cSld><p:spTree>{GRP}{body}</p:spTree></p:cSld>'
               '<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>'
               '<p:transition spd="med"><p:fade/></p:transition>' + timing_xml(sl.steps) + '</p:sld>')
        slides.append((xml, notes, len([s for s in sl.steps if s[1]]), dict(LINKS)))

    n = len(slides)
    ct = ('<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="xml" ContentType="application/xml"/>'
          f'<Override PartName="/ppt/presentation.xml" ContentType="{CT}presentation.main+xml"/>'
          f'<Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="{CT}slideMaster+xml"/>'
          f'<Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="{CT}slideLayout+xml"/>'
          f'<Override PartName="/ppt/notesMasters/notesMaster1.xml" ContentType="{CT}notesMaster+xml"/>'
          '<Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>'
          '<Override PartName="/ppt/theme/theme2.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>'
          f'<Override PartName="/ppt/presProps.xml" ContentType="{CT}presProps+xml"/>'
          f'<Override PartName="/ppt/viewProps.xml" ContentType="{CT}viewProps+xml"/>'
          '<Override PartName="/ppt/tableStyles.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.tableStyles+xml"/>'
          '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
          '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>')
    for i in range(1, n + 1):
        ct += (f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="{CT}slide+xml"/>'
               f'<Override PartName="/ppt/notesSlides/notesSlide{i}.xml" ContentType="{CT}notesSlide+xml"/>')

    pres_rels = [("rId1", "slideMaster", "slideMasters/slideMaster1.xml"),
                 ("rId2", "notesMaster", "notesMasters/notesMaster1.xml"),
                 ("rId3", "theme", "theme/theme1.xml"),
                 ("rId4", "presProps", "presProps.xml"),
                 ("rId5", "viewProps", "viewProps.xml"),
                 ("rId6", "tableStyles", "tableStyles.xml")]
    pres_rels += [(f"rId{10 + i}", "slide", f"slides/slide{i}.xml") for i in range(1, n + 1)]
    sld_ids = "".join(f'<p:sldId id="{255 + i}" r:id="rId{10 + i}"/>' for i in range(1, n + 1))
    pres = (HDR + f'<p:presentation {NS} saveSubsetFonts="1">'
            '<p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst>'
            '<p:notesMasterIdLst><p:notesMasterId r:id="rId2"/></p:notesMasterIdLst>'
            f'<p:sldIdLst>{sld_ids}</p:sldIdLst><p:sldSz cx="12192000" cy="6858000"/>'
            '<p:notesSz cx="6858000" cy="9144000"/></p:presentation>')

    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", HDR + '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">' + ct + "</Types>")
        z.writestr("_rels/.rels", rels([
            ("rId1", "officeDocument", "ppt/presentation.xml"),
            ("rId2", "../package/2006/relationships/metadata/core-properties", "docProps/core.xml"),
            ("rId3", "extended-properties", "docProps/app.xml")]).replace(
            REL + "../package/2006/relationships/metadata/core-properties",
            "http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties"))
        z.writestr("docProps/core.xml", HDR + f'<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:title>{esc(title)}</dc:title><dc:subject>Bluebonnet Algebra I</dc:subject></cp:coreProperties>')
        z.writestr("docProps/app.xml", HDR + f'<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"><Application>Microsoft Office PowerPoint</Application><Slides>{n}</Slides><Notes>{n}</Notes></Properties>')
        z.writestr("ppt/presentation.xml", pres)
        z.writestr("ppt/_rels/presentation.xml.rels", rels(pres_rels))
        z.writestr("ppt/presProps.xml", HDR + f"<p:presentationPr {NS}/>")
        z.writestr("ppt/viewProps.xml", HDR + f'<p:viewPr {NS}><p:gridSpacing cx="76200" cy="76200"/></p:viewPr>')
        z.writestr("ppt/tableStyles.xml", HDR + '<a:tblStyleLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" def="{5C22544A-7EE6-4342-B048-85BDC9FD1C3A}"/>')
        z.writestr("ppt/theme/theme1.xml", theme(title))
        z.writestr("ppt/theme/theme2.xml", theme("Notes"))
        z.writestr("ppt/slideMasters/slideMaster1.xml", MASTER)
        z.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels", rels([
            ("rId1", "slideLayout", "../slideLayouts/slideLayout1.xml"), ("rId2", "theme", "../theme/theme1.xml")]))
        z.writestr("ppt/slideLayouts/slideLayout1.xml", LAYOUT)
        z.writestr("ppt/slideLayouts/_rels/slideLayout1.xml.rels", rels([
            ("rId1", "slideMaster", "../slideMasters/slideMaster1.xml")]))
        z.writestr("ppt/notesMasters/notesMaster1.xml", NOTES_MASTER)
        z.writestr("ppt/notesMasters/_rels/notesMaster1.xml.rels", rels([("rId1", "theme", "../theme/theme2.xml")]))
        for i, (xml, notes, _, links) in enumerate(slides, 1):
            z.writestr(f"ppt/slides/slide{i}.xml", xml)
            z.writestr(f"ppt/slides/_rels/slide{i}.xml.rels", rels([
                ("rId1", "slideLayout", "../slideLayouts/slideLayout1.xml"),
                ("rId2", "notesSlide", f"../notesSlides/notesSlide{i}.xml")], links))
            z.writestr(f"ppt/notesSlides/notesSlide{i}.xml", notes_xml(notes))
            z.writestr(f"ppt/notesSlides/_rels/notesSlide{i}.xml.rels", rels([
                ("rId1", "notesMaster", "../notesMasters/notesMaster1.xml"),
                ("rId2", "slide", f"../slides/slide{i}.xml")]))

    print(f"wrote {OUT.name}: {n} slides, {sum(c for _, _, c, _ in slides)} click animations, "
          f"{sum(1 for _, nt, *_ in slides if nt)} with notes")
    for w in warnings:
        print("WARNING", w)
    return not warnings


def divider(sl, sec, top, h1="divider"):
    y = top
    for k in sec.els():
        if k.tag == "aside":
            continue
        fs = 110 if k.tag == "h1" else 26
        h = lay(sl, k, PAD_X, y, SW - 2 * PAD_X, fs) if k.tag != "h1" else text_block(
            sl, k, PAD_X, y, SW - 2 * PAD_X, h1)
        y += (h or 0) + 18 / 96
    return y - top


if __name__ == "__main__":
    sys.exit(0 if build() else 1)

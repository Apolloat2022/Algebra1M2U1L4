---
name: bluebonnet-algebra-slides
description: Build Bluebonnet Algebra I lesson materials the way this teacher's course site does - HTML slide decks with click-by-click steps, converted to PowerPoint with page numbers; publisher LessonSlides .pptx files with red click-to-reveal answers placed in empty space; and IEP / Section 504 / catch-up versions. Use when the user asks for lesson slides, a PowerPoint, slides with answers, an answer key, bell work, homework, a quiz, or accommodated versions for Algebra I.
---

# Bluebonnet Algebra I slides

Materials for a Texas Algebra I class (Bluebonnet Learning Secondary Mathematics, Carnegie Learning).
Three jobs, each with a script in `scripts/` (Python 3, standard library only):

| Job | Input | Script | Output |
|---|---|---|---|
| Web deck → PowerPoint | an HTML deck in the engine below | `make_pptx.py deck.html` | `deck.pptx` beside it |
| Publisher slides with answers | `..._LessonSlides_ENG_2025.pptx` + `answers.json` | `add_answers.py deck.pptx answers.json [out.pptx]` | `..._with_answers.pptx` |
| New deck | the lesson content | start from `template.html` | an HTML deck, then the row above |

Copy uploaded files into a working folder first (uploads can be read-only), run the scripts from
`scripts/`, and put finished files in the outputs folder. Every PowerPoint gets a page number in the
bottom-right corner (a slide-number field, so it renumbers itself if slides move).

## 1. HTML deck engine (`template.html`)

One self-contained HTML file per lesson. The stage is 1280 × 720; keep everything inside it.

- `<section class="slide">` is one slide; `<section class="slide divider">` is a section break (big h1).
- First line of each slide: `<p class="eyebrow">Day 1 · Activity 1.1 · SE p. 272</p>`, then an `<h2>`.
- `class="step"` reveals on click (one click each, in order). Answers: `<div class="step pop eq sm ans">…</div>`.
- `<aside class="notes">` is the presenter note (it becomes the PowerPoint speaker notes).
- Math: `<span class="mt"><i>f</i>(<i>x</i>) = 2<i>x</i> − 1</span>`; use the real minus sign − .
  Fractions `{{a|b}}` stack on the web but come out flat ("a/b") in PowerPoint, so write a fraction
  coefficient as `({{1|4}})x`, never `{{1|4}}x`.
- Colors: `class="cm"` orange (slope / a), `class="cp"` blue (point / d).
- Layout: `div.row` (side by side), `div.col` (stacked), `div.card`, `table.tbl` (a `td.step` cell reveals).
- Graph: `<div class="graph" data-g='{"w":400,"h":400,"x":[-10,10],"y":[-10,10],"gx":[2,4],"gy":[2,4],"lines":[{"p":[[0,0],[1,1]],"label":"f(x)"},{"p":[[0,5],[1,6]],"label":"p(x)","c":"b","step":true}],"pts":[],"alt":"…"}'></div>`
  - line `c`: "a" orange, "b" purple, "c" black; `"seg": true` draws only between the two points;
    `"dash": true`; `"step": true` reveals on click. Keep labels short ("f(x)", not "f(x) = x").
- `<p class="foot">` sits at the bottom (credit line); `<p class="warn">` is a callout; `small`, `muted`.

`make_pptx.py` exits 1 and prints `WARNING slide N: content may run to X in` when a slide is taller
than 7.5 in. Anything under 7.5 in is fine; over that, shorten the text, cut a step, or split the slide.

## 2. Publisher slides with answers (`add_answers.py`)

Answers come from the Teacher Edition, and each one is re-solved before it goes on a slide. Where the
TE is wrong, put "TE correction: …" in the slide's notes and list it on the corrections slide.

`answers.json` boxes are `[x, y, w, h, size_pt, "text", ...]` on a 1920 × 1080 grid (the slide is
13.333 × 7.5 in, so 144 px = 1 in and 1 pt = 2 px). Answers are red, appear on click, and use the
deck's own font.

**Placement rules: answers go in empty space only.**
- Never on top of a printed blank line (`k(x) = ______`), a table border, a graph or question text.
  Put the answer just past the end of the blank (same row), or in clear space beside or below the item.
- Fill-in tables: centre the answer inside the empty cell (`"center"`).
- Graph answers: describe the graph in words beside the picture ("Graph p(x): the line through
  (0, 5), parallel to f(x)") rather than writing on the grid.
- To find where text ends, measure it: the deck text is usually Calibri; at 28 pt a character run's
  width in grid px is `ImageFont.truetype("calibri.ttf", 56).getlength(text)` (Pillow), starting at the
  text box's x + 14 px inset + any paragraph margin (`marL` EMU ÷ 6350).
- Then render and look: `soffice --headless --convert-to pdf out.pptx` and
  `pdftoppm -png -r 50 out.pdf page`, and view the answer pages. In a PDF every click-reveal shows at
  once, so this shows exactly where each answer lands. Fix any answer that touches a line or text.

## 3. Accommodated versions

- **IEP**: fewer, simpler items (3 answer choices instead of 4), worked steps, hint boxes, sentence
  frames, a reference card on tests; same TEKS.
- **Section 504**: the same items as general, with access supports only: "Today's Plan", "Key
  Vocabulary" and "Notes to Keep" slides, larger type, chunked directions, extra spacing.
- **Catch-up decks**: a 15-minute block of the missed lesson after each day's bell work, with dated
  "Start: Monday, October 19" and "Stop here: …" divider slides for each class day.

Answer keys: a separate `-ANSWER-KEY.pptx` with every answer shown (no click reveals).

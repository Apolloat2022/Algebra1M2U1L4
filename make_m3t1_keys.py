"""Module 3 Topic 1 publisher lesson slides with answers (same method as make_lesson_key.py for Module 2 Topic 2).
Red answers appear on click: inside the question's own text box, right under its letter (PowerPoint lays them out), or
in empty space beside number lines, tables and pictures. Every slide gets its Student Edition page; starred activities
(150-day pacing guide, Module 3 Topic 1 p. 3) get "★ Essential", skipped / optional ones a red badge.
Each answer was re-solved; Teacher Edition and slide errors go in the notes and on a corrections slide.
Run:  python make_m3t1_keys.py [1 2 3]   (reads Module 3 topic 1/BOOK SLIDES (original)/, writes ..._with_answers.pptx)"""
import sys
from pathlib import Path

import make_lesson_key as K

HERE = Path(__file__).parent / "Module 3 topic 1"
SRC = HERE / "BOOK SLIDES (original)"
WITH, CENTER = K.WITH, K.CENTER
pages = K.pages


def I(sp, p, text, size=20):  # inline answer: a red paragraph after paragraph p of text box sp
    return ("in", sp, p, text, size)


def B(x, y, w, h, size, text, *flags):  # floating box on the 1920 x 1080 grid, in empty space only
    return ("box", (x, y, w, h, size, text, *flags))


def split(spec):
    """{slide: [I(...)/B(...)]} -> answers {slide: [box]} and inline {slide: [(sp, p, [answer #])]}"""
    ans, inline = {}, {}
    for k, items in spec.items():
        for it in items:
            j = len(ans.setdefault(k, []))
            if it[0] == "in":
                _, sp, p, text, size = it
                ans[k].append((0, 0, 0, 0, size, text))
                inline.setdefault(k, []).append((sp, p, [j]))
            else:
                ans[k].append(it[1])
    return ans, inline


EQ1 = "Sample: Substitute the known output for the dependent variable, then use the properties of equality to isolate the variable. That value is the unknown input."
EQ2 = "Use the same properties of equality to isolate that one variable, treating every other letter like a number."
EQ3 = "Yes. Graphs and the properties of equality work the same way, except that multiplying or dividing both sides by a negative number reverses the inequality sign."

L1 = {
 11: [I(1, 1, "Sample: x + 3 = 5"), I(1, 4, "Sample: 4x + 12 = 20")],
 12: [I(1, 0, "Sample (a = 2): 2x + 12 = −2x + 20"), I(1, 3, "d. Sample (divide by 2): x + 6 = 10 − x")],
 13: [I(2, 0, "Substitute 2 for x (or solve): 2 + 6 = 10 − 2, so 8 = 8, a true statement.")],
 19: [B(205, 500, 740, 330, 18, "a. Harper: −3(2) + 14 = 18 − 5(2) → 8 = 8\nSofia: 2(2) = 5 − ½(2) → 4 = 4"),
      B(986, 500, 830, 330, 18, "b. Harper: subtract 14, add 5x: 2x = 4, so x = 2\nSofia: add ½x: (5/2)x = 5, multiply by 2/5: x = 2")],
 21: [I(2, 1, "Add 4x (addition property): 28x + 7 = 0. Subtract 7 (subtraction property): 28x = −7. Divide by 28 (division property): x = −¼.", 18)],
 22: [I(1, 0, "1.2x + 0.6 = 4x + 6.2 (distributive) → −2.8x + 0.6 = 6.2 (subtraction) → −2.8x = 5.6 (subtraction) → x = −2 (division)", 18),
      I(1, 5, "½x − 6 = 3 + 2x (commutative, associative) → −9 = (3/2)x (subtraction) → x = −6 (multiplication by 2/3)", 18)],
 23: [B(1420, 520, 460, 440, 18, "Daniel used the distributive property first; Chloe divided both sides by 4 first (division property). "
                                "Both then used the subtraction and division properties and got x = −1.")],
 28: [I(1, 1, "Sample: 2x = 2x and 2x + 5 = 2x + 5. No: using the properties of equality, the sentence stays true.")],
 29: [I(1, 1, "Sample: 2 + x = 3 + x and 5(2 + x) = 5(3 + x). No: using the properties of equality, the sentence stays false.")],
 31: [I(1, 1, "Infinite solutions: any value of the variable makes them true."), I(1, 4, "No solution: no value of the variable makes them true.")],
 32: [I(1, 0, "One solution, x = 0: the coefficients of x are different, and only 0 makes 2x = 3x true (0 = 0).")],
 40: [I(1, 2, "In fewest terms, the x-coefficients are the same but the constants are different."),
      I(1, 4, "In fewest terms, the x-coefficients and the constants are both the same (the two expressions are equivalent).")],
 44: [I(1, 0, "6(5 + 2x) = 8(x + 5) → 30 + 12x = 8x + 40 (distributive) → 4x + 30 = 40 (subtraction) → 4x = 10 (subtraction) → x = 2.5 (division)", 18)],
 45: [I(1, 3, EQ1, 18)],
 52: [B(560, 555, 380, 64, 24, "r = 10 in."), B(1400, 555, 420, 64, 24, "r = 2.5 ft"),
      B(560, 790, 380, 64, 24, "r ≈ 1.6 cm"), B(1400, 790, 420, 64, 24, "r ≈ 7.6 mm")],
}
NOTES1 = {12: "Slide typo: the second part is labeled c.; it is part d.",
          21: "Check: 24(−¼) + 7 = 1 and −4(−¼) = 1.",
          37: "Not essential on the 150-day calendar (one day for this lesson). Save Tic-Tac-Bingo for the Nov 19 retake day.",
          43: "Optional: not starred, but it matches End of Topic question 11 (equal areas)."}
CORR1 = [("Notes for this deck", None), ("Slide 12: two parts are labeled c.; the second is d.", None),
         ("Every Teacher Edition answer was re-solved and is correct, including Prepare (C = 2πr).", "16171D")]

L2 = {
 9: [I(1, 0, "Juan: w = P/2 − ℓ. Mia: ℓ = P/2 − w. Each solves P = 2ℓ + 2w for the side they need.")],
 10: [I(1, 0, "Multiply each by 2: 2w = P − 2ℓ and 2ℓ = P − 2w. Both rearrange to 2ℓ + 2w = P.")],
 14: [I(1, 2, "−2/3")],
 15: [I(1, 0, "(0, 4)"), I(1, 3, "(6, 0)"), I(1, 6, "Slope and y-intercept come straight from y = mx + b. For the x-intercept, substitute 0 for y and solve.", 18)],
 16: [I(1, 1, "4"), I(1, 4, "(0, −8)")],
 17: [I(1, 0, "(2, 0)"), I(1, 3, "The slope and x-intercept come from the equation (x − 2 = 0 at x = 2). Distribute, y = 4x − 8, for the y-intercept.", 18)],
 18: [I(1, 1, "3/2"), I(1, 4, "(0, −4)")],
 19: [I(1, 0, "(8/3, 0)"), I(1, 3, "Rewrite in slope-intercept form, y = (3/2)x − 4, for the slope and y-intercept. Substitute 0 for y for the x-intercept.", 18)],
 20: [I(5, 0, "Q1: slope-intercept form. Q2: point-slope form. Q3: standard form.")],
 21: [I(1, 2, "Slope −A/B; x-intercept (C/A, 0); y-intercept (0, C/B)")],
 22: [I(1, 1, "slope-intercept form or point-slope form"), I(1, 3, "point-slope form"), I(1, 5, "slope-intercept form")],
 23: [I(1, 0, "Slope-intercept form: graphing technology takes y = … directly."), I(1, 4, "y = 5x − 33"), I(3, 0, "y = 4x − 6")],
 24: [I(1, 1, "x − 2y = 15"), I(3, 0, "4x + y = 3"), I(1, 6, "x − 2y = −13"), I(5, 1, "4x + y = 9")],
 32: [I(1, 0, "Multiply both sides by 9/5: (9/5)C = F − 32. Add 32 to both sides: F = (9/5)C + 32.")],
 33: [I(1, 0, "Mateo is correct: 30°C = (9/5)(30) + 32 = 86°F, which is warmer than 77°F (77°F = 25°C).", 18)],
 34: [I(2, 0, "She distributed 5/9, multiplied both sides by 9, added 160, then divided by 5: F = (9/5)C + 32.", 18)],
 36: [I(1, 0, "In line 2 he did not distribute 5/9 to the 32."), I(2, 0, "He multiplied by 9 wrong: 9 · (5/9)F = 5F (not 45F) and 9 · (160/9) = 160 (not 1440).")],
 38: [I(1, 1, "9C = 5(F − 32) → 9C = 5F − 160 → 9C − 5F = −160")],
 43: [I(1, 1, "V = Bh, so h = V/B"), I(1, 6, "h = 450 ÷ 75 = 6 inches")],
 44: [I(1, 1, "V = (1/3)πr²h, so h = 3V/(πr²)")],
 45: [I(1, 0, "Volume (cubic units) divided by the base area (square units, r · r) leaves a linear unit for the height.")],
 46: [I(1, 1, "h = 2A/(b₁ + b₂)"), I(1, 4, "h = 2(24)/(9 + 7) = 48/16 = 3 cm")],
 47: [I(1, 1, "A = BZ − BC/D: multiply both sides by B, then subtract BC/D."),
      I(1, 5, "D = BC/(BZ − A): multiply by BD, move the D terms to one side, factor out D, divide by BZ − A.")],
 51: [I(1, 0, "h = S/(2πr)"), I(1, 3, "h = 37.68 ÷ (2 · 3.14 · 1.5) = 37.68 ÷ 9.42 = 4 in.")],
 52: [I(1, 0, "h = (S − 2πr²)/(2πr)"), I(1, 3, "h = (51.81 − 14.13) ÷ 9.42 = 4 in.")],
 53: [I(1, 3, EQ2, 18)],
 56: [B(520, 345, 380, 70, 24, "x = 5"), B(1260, 345, 450, 70, 24, "x ≤ −3"), B(520, 600, 380, 70, 24, "x > 7"), B(1260, 600, 450, 70, 24, "x < −4")],
}
NOTES2 = {24: "TE correction: the TE gives x − 2y = −7 and 4x + y = 7. With slope 1/2 through (−3, 5): y − 5 = ½(x + 3), so x − 2y = −13. "
              "With slope −4 through (2, 1): y − 1 = −4(x − 2), so y = −4x + 9 and 4x + y = 9.",
          30: "Slide typo: the formula shows C = −5/9(F − 32). It is C = 5/9(F − 32), as on slide 38 and in the Student Edition."}
CORR2 = [("Teacher Edition and slide corrections for this deck", None),
         ("Activity 2.1 Q10a (slope 1/2 through (−3, 5)): x − 2y = −13, not −7 as the TE says.", None),
         ("Activity 2.1 Q10b (slope −4 through (2, 1)): 4x + y = 9, not 7 as the TE says.", None),
         ("Slide 30: the formula has a stray minus sign; it is C = 5/9(F − 32).", None),
         ("Every other TE answer was re-solved and is correct.", "16171D")]

L3 = {
 9: [I(1, 0, "f(b) = 3.75b + 25")],
 10: [I(1, 1, "Independent: number of boxes sold. Dependent: total sales, in dollars."), I(1, 6, "Slope 3.75: each box sold adds $3.75 to total sales.")],
 11: [I(1, 0, "y-intercept 25: the $25 credit each camper starts with.")],
 16: [I(1, 1, "The horizontal line y = 1600 meets the graph at (420, 1600)."), I(1, 3, "420 boxes: the vertical line down from (420, 1600) meets the x-axis at 420.", 18)],
 17: [B(140, 560, 1100, 70, 22, "Closed circle at 420 only (b = 420)")],
 18: [I(2, 1, "Every number of boxes that earns Elijah $1600 or less.")],
 19: [B(680, 370, 1150, 70, 22, "f(b) ≤ 1600, so b ≤ 420"), B(720, 905, 1150, 100, 20, "Closed circle at 420, shaded left to 0")],
 20: [I(1, 0, "No. Only whole numbers of boxes from 0 to 420 make sense: he can't sell negative or partial boxes.")],
 21: [I(1, 1, "Every number of boxes that earns Elijah more than $1600."), I(1, 5, "f(b) > 1600, so b > 420")],
 22: [B(626, 620, 1200, 100, 20, "Open circle at 420, shaded right")],
 23: [I(1, 0, "No. Only whole numbers greater than 420 make sense: he can't sell partial boxes.")],
 24: [I(1, 0, "An open circle means the point is not included (< or >). A closed circle means it is included (≤ or ≥).")],
 25: [I(1, 1, "At least 240 boxes: b ≥ 240, or 3.75b + 25 ≥ 925")],
 26: [I(1, 0, "Fewer than 540 boxes: b < 540, or 3.75b + 25 < 2050"), I(1, 3, "c. Exactly 180 boxes: b = 180, or 3.75b + 25 = 700")],
 34: [I(2, 0, "At least 287 boxes: b ≥ 286.67, and he can't sell part of a box (286 boxes earns less than $1100).")],
 35: [I(1, 1, "3.75b + 25 < 600 → 3.75b < 575 → b < 153.3…  At most 153 boxes.")],
 36: [I(1, 0, "3.75b + 25 ≥ 1500 → 3.75b ≥ 1475 → b ≥ 393.3…  At least 394 boxes.")],
 37: [I(1, 0, "It doesn't change: solve it like an equation, using the properties of equality and number properties.")],
 41: [I(3, 0, "h(m) = −20m + 4800")],
 42: [I(2, 1, "Slope −20: the troop descends 20 feet every minute."), I(2, 4, "y-intercept 4800: they start at 4800 feet.")],
 43: [I(1, 0, "x-intercept 240: they reach sea level after 240 minutes (4 hours)."), I(1, 4, "0 ≤ m ≤ 240: from the start of the hike to sea level.")],
 44: [I(1, 0, "About 80 minutes or more: m > 80 (an oval around the part of the line below y = 3200).", 18)],
 45: [I(1, 0, "−20m + 4800 < 3200 → −20m < −1600 → m > 80"), I(1, 4, "5. The solution sets are the same, m > 80, whichever strategy is used.")],
 46: [B(1458, 343 + 110 * i, 282, 110, 18, v, CENTER, *(() if i == 0 else (WITH,))) for i, v in enumerate(["m < 80", "m ≤ 80", "m = 80", "m > 80", "m ≥ 80"])],
 47: [I(1, 0, "The inequality signs are reversed in every row."),
      I(1, 2, "c. h(m) has a negative coefficient, −20. Dividing by a negative number reverses the sign, so every row flips.")],
 55: [B(626, 480, 740, 420, 18, "a. Victoria moved the x-terms to the left, the constants to the right, then divided by 2: x ≥ −6."),
      B(1396, 480, 480, 420, 18, "b. Kai moved the x-terms to the right, the constants to the left, then divided by −2, which reversed the sign: −6 ≤ x.")],
 56: [I(1, 0, "The same: move the variables to one side and the constants to the other, then isolate the variable. For an inequality, "
              "reverse the sign when you multiply or divide by a negative.", 18)],
 58: [B(210, 430, 740, 400, 18, "a. Aaliyah distributed −4 first, moved the constants to the right, then divided by −4, which reversed the sign: x > ½."),
      B(996, 430, 860, 400, 18, "b. Ava divided both sides by −4 first, which reversed the sign, then added 6 to isolate x: x > ½.")],
 59: [I(1, 0, "It is the same: the distributive property removes the parentheses in an inequality just as in an equation.")],
 63: [B(1330, 470, 560, 100, 22, "a. x ≤ −21/2 (−10.5): closed circle, shade left"), B(1330, 800, 560, 100, 22, "b. x > −9: open circle, shade right")],
 64: [B(1150, 370, 700, 100, 22, "c. x ≥ 3: closed circle, shade right"), B(1150, 765, 700, 100, 22, "d. x > −1: open circle, shade right")],
 65: [I(3, 0, "True for all values of A, B, and C."), I(3, 2, "True only when C < 0."), I(3, 4, "Never true.")],
 66: [I(1, 3, EQ3, 18)],
 69: [I(2, 0, "Sample: (6, 0)"), I(4, 0, "Sample: (0, 3)"), I(6, 0, "Sample: (20, 0)")],
}
NOTES3 = {26: "Slide typo: both parts are labeled b.; the second is c.",
          27: "Slide typo: the summary says Activity 3.2; it is Activity 3.1.",
          45: "Slide typo: both questions are numbered 4; the second is 5.",
          47: "Slide typo: both parts are labeled b.; the second is c.",
          57: "Slide typo: the inequality is −4(x − 6) < 22, as in both students' work (the slide text says < 2). With 22: x > ½."}
CORR3 = [("Slide corrections for this deck", None),
         ("Slide 57: the inequality is −4(x − 6) < 22, not < 2 (the student work uses 22).", None),
         ("Slides 26 and 47: the second part labeled b. is c. Slide 45: the second question 4 is 5.", None),
         ("Slide 27: the summary is for Activity 3.1, not 3.2.", None),
         ("Every Teacher Edition answer was re-solved and is correct.", "16171D")]

LESSONS = {
 1: dict(spec=L1, notes=NOTES1, corr=CORR1, after=52,
         se=pages((2, 6, 345), (8, 15, 346), (16, 19, 347), (20, 22, 348), (23, 28, 349), (29, 34, 350), (36, 36, 345), (37, 42, 351),
                  (43, 45, 352), (47, 48, 353), (51, 52, 356)),
         stars=((8, 15), (16, 25), (26, 34)),
         skips=((37, 42, "Skip today: not essential (save Tic-Tac-Bingo for the retake day)", "Skip"),
                (43, 46, "Optional: like End of Topic question 11", "Optional"),
                (47, 50, "Skip today: Tic-Tac-Bingo materials", "Skip"))),
 2: dict(spec=L2, notes=NOTES2, corr=CORR2, after=56,
         se=pages((2, 4, 357), (6, 12, 358), (13, 17, 359), (18, 21, 360), (22, 26, 361), (28, 28, 357), (29, 33, 362), (34, 36, 363),
                  (37, 40, 364), (41, 45, 365), (46, 49, 366), (50, 54, 367), (55, 56, 370)),
         stars=((6, 12), (13, 26), (29, 40), (41, 49), (50, 54)), skips=()),
 3: dict(spec=L3, notes=NOTES3, corr=CORR3, after=69,
         se=pages((2, 5, 371), (7, 13, 372), (14, 17, 373), (18, 23, 374), (24, 28, 375), (30, 30, 371), (31, 34, 376), (35, 39, 377),
                  (40, 43, 378), (44, 49, 379), (51, 51, 371), (52, 56, 380), (57, 61, 381), (62, 67, 382), (68, 69, 385)),
         stars=((7, 13), (14, 28), (31, 39), (40, 49), (52, 61), (62, 67)), skips=()),
}

if __name__ == "__main__":
    for n in [int(a) for a in sys.argv[1:]] or LESSONS:
        c = LESSONS[n]
        ans, inline = split(c["spec"])
        src = SRC / f"BLMathematics_AlgI_M3_T1_L{n}_LessonSlides_ENG_2025.pptx"
        K.annotate(src, HERE / src.name.replace("2025", "with_answers"), ans, c["notes"], c["corr"], c["after"],
                   se=c["se"], stars=c["stars"], inline=inline, skips=c["skips"])

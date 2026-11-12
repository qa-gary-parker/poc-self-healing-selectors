from manim import *
from scenekit import *

LINE = "#2E332F"
SUITES = ["CSS selectors", "role locators", "test IDs"]
TESTS = ["invalid credentials", "logs in", "adds a task", "completes a task", "filters active", "filters completed", "active count"]
CODE_SIZE = 24


def code(s, size=22, color=PRIMARY, **kw):
    return Text(s, font=MONO, font_size=size, color=color, **kw)


def code_line(s, highlight=None, hcolor=ACCENT, size=CODE_SIZE):
    t = code(s, size)
    if highlight:
        span(t, s, highlight).set_color(hcolor)
    return t


def cell(w=1.6, h=0.66):
    box = RoundedRectangle(corner_radius=0.08, width=w, height=h, color=LINE, stroke_width=2)
    box.set_fill(LINE, opacity=0.35)
    return box


def count_color(n):
    return GOOD if n == 7 else BAD if n == 0 else WARN


def ticker(n, fmt, color, size, place, start=0, run_time=0.9):
    label = place(code(fmt.format(start), size, DIM))

    def tick(m, a):
        m.become(place(code(fmt.format(round(start + (n - start) * a)), size, color if a > 0.999 else PRIMARY)))

    return label, UpdateFromAlphaFunc(label, tick, run_time=run_time)


def fill(box, n, run_time=0.9):
    color = count_color(n)
    paint = box.animate.set_stroke(color).set_fill(color, opacity=0.16)
    if n == 0:
        label = code("0/7", 24, BAD).move_to(box)
        return label, AnimationGroup(paint, FadeIn(label, scale=1.3), run_time=run_time)
    label, tick = ticker(n, "{}/7", color, 24, lambda m: m.move_to(box), run_time=run_time)
    return label, AnimationGroup(paint, tick, run_time=run_time)


def table(cols, x=0.4):
    header = VGroup(*[code(c, 20, DIM) for c in cols])
    rows = VGroup()
    for suite in SUITES:
        cells = VGroup(*[cell() for _ in cols]).arrange(RIGHT, buff=0.24)
        rows.add(VGroup(txt(suite, 28), cells))
    rows.arrange(DOWN, buff=0.4)
    for row in rows:
        row[0].move_to([-5.4, row.get_y(), 0], aligned_edge=LEFT)
        row[1].move_to([x, row.get_y(), 0], aligned_edge=LEFT)
    for h, c in zip(header, rows[0][1]):
        h.next_to(c, UP, buff=0.24)
    return VGroup(header, rows)


def terminal(lines, width=None):
    texts = VGroup(*lines).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
    width = max(width or 0, texts.width + 0.8)
    box = RoundedRectangle(corner_radius=0.12, width=width, height=texts.height + 0.8, color=LINE, stroke_width=3)
    box.set_fill(LINE, opacity=0.3)
    texts.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.4)
    return VGroup(box, texts)


def repair_row(label, before, after, y, size=24):
    name = txt(label, 24, DIM).move_to([-6.2, y, 0], aligned_edge=LEFT)
    b = code(before, size, DIM).move_to([-2.9, y, 0], aligned_edge=LEFT)
    arr = arrow([b.get_right()[0] + 0.25, y, 0], [b.get_right()[0] + 1.05, y, 0], ACCENT)
    a = code(after, size, ACCENT).next_to(arr, RIGHT, buff=0.25)
    return VGroup(name, b, arr, a)


def underline(mob, color=WARN):
    return Line(mob.get_corner(DL) + DOWN * 0.08, mob.get_corner(DR) + DOWN * 0.08, color=color, stroke_width=4)


class S1Result(Timed):
    def construct(self):
        title = code("Playwright test-healer agent  ·  round 1", 22, DIM).to_edge(UP, buff=0.7)
        self.add(title)
        tests = VGroup(*[
            RoundedRectangle(corner_radius=0.06, width=0.42, height=0.42, color=BAD, stroke_width=2).set_fill(BAD, opacity=0.25)
            for _ in range(10)
        ]).arrange(RIGHT, buff=0.16).move_to([0, 2.1, 0])
        final = code("10/10 repaired", 64, GOOD).move_to([0, 0.9, 0])
        big, tick = ticker(10, "{}/10 repaired", GOOD, 64, lambda m: m.move_to(final, aligned_edge=RIGHT), run_time=1.1)
        time = code("4m 36s", 26, DIM)
        wrong = code("·  0 incorrect", 26, DIM)
        sub = VGroup(time, wrong).arrange(RIGHT, buff=0.3).next_to(final, DOWN, buff=0.3)
        self.at("fixed every broken test")
        self.play(LaggedStart(*[FadeIn(t, scale=0.6) for t in tests], lag_ratio=0.1), run_time=0.9)
        self.at("ten repairs")
        self.play(FadeIn(big, shift=UP * 0.2), run_time=0.3)
        self.play(tick, LaggedStart(*[t.animate.set_stroke(GOOD).set_fill(GOOD, opacity=0.25) for t in tests], lag_ratio=0.1, run_time=1.1))
        self.at("under five minutes")
        self.play(FadeIn(time, shift=UP * 0.15), run_time=0.5)
        self.at("none of them wrong")
        self.play(FadeIn(wrong, shift=UP * 0.15), run_time=0.5)

        head = code("next release:", 26, DIM)
        suite = code("healed CSS suite", 34, PRIMARY)
        zero = code("0/7", 34, BAD)
        VGroup(head, suite, zero).arrange(RIGHT, buff=0.35).move_to([0, -0.6, 0])
        self.at("one release later")
        self.play(
            VGroup(tests, big, sub).animate.scale(0.7).move_to([0, 1.7, 0]).set_opacity(0.45),
            FadeIn(VGroup(head, suite), shift=UP * 0.2),
            run_time=0.8, rate_func=smooth,
        )
        self.at("failed all seven")
        self.play(FadeIn(zero, scale=1.4), suite.animate.set_color(BAD), run_time=0.6)

        caption = txt("same fragility  ·  new names", 32, ACCENT).move_to([0, -2.2, 0])
        self.at("healing put the suite back")
        self.play(FadeIn(caption, shift=UP * 0.2), run_time=0.8, rate_func=smooth)
        self.at("here is why")
        self.play(self.camera_to(12.6, [0, -0.6, 0]), run_time=1.2, rate_func=smooth)
        self.end()


class S2Setup(Timed):
    DRIFT = 0.0015

    def construct(self):
        title = code("one app  ·  three versions", 22, DIM).to_edge(UP, buff=0.7)
        self.add(title)
        versions = flow(["v1", "v2  redesign", "v3  CSS modules"], width=3.6, gap=0.9, color=NOTE, size=24).move_to([0, 2.2, 0])
        boxes, arrows = versions
        note = code("same behaviour  ·  only the markup drifts", 20, DIM).next_to(versions, DOWN, buff=0.35)
        self.at("small task manager app")
        self.play(FadeIn(boxes[0], shift=UP * 0.2), run_time=0.6)
        self.at("three versions")
        self.play(LaggedStart(AnimationGroup(grow_arrow(arrows[0]), FadeIn(boxes[1], shift=RIGHT * 0.3)),
                              AnimationGroup(grow_arrow(arrows[1]), FadeIn(boxes[2], shift=RIGHT * 0.3)), lag_ratio=0.5), run_time=1.0)
        self.at("behaviour never changes")
        self.play(FadeIn(note), run_time=0.6)

        def details(items, box):
            group = VGroup(*[code(s, 21) for s in items]).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
            return group.next_to(note, DOWN, buff=0.7).set_x(box.get_x())

        v2 = details(["ids + classes renamed", "2 buttons → icons", "1 test ID renamed"], boxes[1])
        v3 = details(["every class hashed", "ids regenerated", "names + test IDs kept"], boxes[2])
        self.at("version two is a redesign")
        self.play(light_up(boxes[1], WARN), run_time=0.6)
        for phrase, item in zip(["every id and class", "two buttons", "one test id"], v2):
            self.at(phrase)
            self.play(FadeIn(item, shift=DOWN * 0.1), run_time=0.5)
        self.at("version three")
        self.play(light_up(boxes[2], WARN), run_time=0.6)
        self.at("every class is hashed")
        self.play(LaggedStart(FadeIn(v3[0], shift=DOWN * 0.1), FadeIn(v3[1], shift=DOWN * 0.1), lag_ratio=0.5), run_time=0.9)
        self.at("accessible names")
        self.play(FadeIn(v3[2], shift=DOWN * 0.1), run_time=0.5)

        samples = [
            ("CSS selectors", 'locator("#username")'),
            ("role locators", 'getByLabel("Username")'),
            ("test IDs", 'getByTestId("username-input")'),
        ]
        rows = VGroup(*[VGroup(txt(n, 30, DIM), code(s, 22, DIM)).arrange(DOWN, buff=0.16, aligned_edge=LEFT) for n, s in samples])
        rows.arrange(DOWN, buff=0.55, aligned_edge=LEFT).move_to([0, -0.2, 0])
        ref = code("tests/*.spec.ts  ·  login()", 16, DIM).next_to(rows, DOWN, buff=0.5).align_to(rows, LEFT)
        self.at("seven scenarios")
        self.play(
            FadeOut(VGroup(versions, note, v2, v3), shift=UP * 0.5),
            Transform(title, code("7 scenarios  ×  3 suites", 22, DIM).to_edge(UP, buff=0.7)),
            run_time=0.8, rate_func=smooth,
        )
        self.at("three ways")
        self.play(LaggedStart(*[FadeIn(r[0], shift=LEFT * 0.25) for r in rows], lag_ratio=0.2), run_time=0.7)
        for phrase, row in zip(["css selectors", "role locators", "and test"], rows):
            self.at(phrase)
            self.play(row[0].animate.set_color(PRIMARY), FadeIn(row[1], shift=LEFT * 0.2), run_time=0.5)
        self.play(FadeIn(ref), run_time=0.4)
        self.end()


class S3Drift(Timed):
    def construct(self):
        title = code("written once against v1  ·  never updated", 22, DIM).to_edge(UP, buff=0.7)
        self.add(title)
        header, rows = table(["v1", "v2"])
        self.at("against the redesign")
        self.play(FadeIn(header), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.3) for r in rows], lag_ratio=0.2), run_time=0.9)
        v1 = [fill(r[1][0], 7, 0.6) for r in rows]
        self.play(*[a for _, a in v1])
        role, role_anim = fill(rows[1][1][1], 5)
        self.at("role locator suite")
        self.play(role_anim)
        ids, ids_anim = fill(rows[2][1][1], 6)
        self.at("test id passed six")
        self.play(ids_anim)
        css, css_anim = fill(rows[0][1][1], 0, 0.7)
        self.at("the css suite passed none")
        self.play(css_anim, Indicate(rows[0][0], color=BAD, scale_factor=1.08))

        sels = ['locator("#username")', 'locator("#password")', 'locator("#login-btn")']
        login = terminal([code(s, 22) for s in sels]).move_to([-3.7, -0.3, 0])
        head = code("login()  ·  first step of all 7 tests", 18, DIM).next_to(login, UP, buff=0.25).align_to(login, LEFT)
        tests = VGroup()
        for name in TESTS:
            box = RoundedRectangle(corner_radius=0.06, width=3.3, height=0.44, color=BAD, stroke_width=2)
            box.set_fill(BAD, opacity=0.12)
            tests.add(VGroup(box, code(name, 16, BAD).move_to(box)))
        tests.arrange(DOWN, buff=0.1).move_to([3.6, -0.3, 0])
        links = VGroup(*[arrow(login.get_right(), t.get_left(), BAD, buff=0.15) for t in tests])
        self.at("every test logs in first")
        self.play(
            FadeOut(VGroup(header, rows[1], rows[2], role, ids, *[label for label, _ in v1]), shift=DOWN * 0.3),
            ReplacementTransform(VGroup(rows[0], css), login),
            FadeIn(head),
            run_time=0.9, rate_func=smooth,
        )
        self.at("three login selectors")
        self.play(*[s.animate.set_color(BAD) for s in login[1]], run_time=0.5)
        self.at("all seven tests")
        self.play(LaggedStart(*[grow_arrow(a) for a in links], lag_ratio=0.12), LaggedStart(*[FadeIn(t) for t in tests], lag_ratio=0.12), run_time=1.4)
        self.end()


class S4Heal(Timed):
    def construct(self):
        title = code("round 1  ·  healer vs v2", 22, DIM).to_edge(UP, buff=0.7)
        self.add(title)
        failing = card("10 failing", BAD, w=2.8, h=0.9, size=26).move_to([-4.6, 0.6, 0])
        healer = card("test-healer agent", ACCENT, w=3.6, h=0.9, size=26).move_to([0, 0.6, 0])
        fixed = card("10 repaired", GOOD, w=2.8, h=0.9, size=26).move_to([4.6, 0.6, 0])
        a1 = arrow(failing.get_right(), healer.get_left(), DIM)
        a2 = arrow(healer.get_right(), fixed.get_left(), DIM)
        time = code("4m 36s", 26, DIM)
        wrong = code("·  0 incorrect", 26, DIM)
        stats = VGroup(time, wrong).arrange(RIGHT, buff=0.3).next_to(healer, DOWN, buff=0.7)
        self.at("test healer agent")
        self.play(FadeIn(healer, scale=0.9), run_time=0.6)
        self.at("ten failures")
        self.play(FadeIn(failing, shift=RIGHT * 0.3), grow_arrow(a1), run_time=0.8)
        self.at("repaired all ten")
        self.play(grow_arrow(a2), FadeIn(fixed, shift=RIGHT * 0.3), run_time=0.8)
        self.at("four minutes")
        self.play(FadeIn(time, shift=UP * 0.15), run_time=0.5)
        self.at("every repair was correct")
        self.play(FadeIn(wrong, shift=UP * 0.15), run_time=0.5)

        head = code("every repair in kind", 22, ACCENT).move_to([-6.2, 2.0, 0], aligned_edge=LEFT)
        rows = [
            repair_row("CSS selectors", '"#username"', '"#field-user"', 0.8),
            repair_row("role locators", 'name: "Done"', 'name: "Complete"', -0.4),
            repair_row("test IDs", '"active-count"', '"task-counter"', -1.6),
        ]
        ref = code("tests → tests-healed  ·  commit 5ecdf1d", 16, DIM).move_to([-6.2, -2.8, 0], aligned_edge=LEFT)
        self.at("every repair was in kind")
        self.play(
            ReplacementTransform(healer, head),
            FadeOut(VGroup(failing, fixed, a1, a2, stats), shift=DOWN * 0.3),
            run_time=0.8, rate_func=smooth,
        )
        for row, (left, right) in zip(rows, [("a css selector", "a new css"), ("an accessible name", "a new accessible"), ("a test id", "a new test")]):
            self.at(left)
            self.play(FadeIn(row[0]), FadeIn(row[1], shift=RIGHT * 0.15), run_time=0.5)
            self.at(right)
            self.play(grow_arrow(row[2]), FadeIn(row[3], shift=RIGHT * 0.15), run_time=0.6)
        self.play(FadeIn(ref), run_time=0.4)
        self.end()


class S5NextRelease(Timed):
    def construct(self):
        title = code("healed at v2  ·  run against v3", 22, DIM).to_edge(UP, buff=0.7)
        self.add(title)
        header, rows = table(["v3"], x=1.4)
        cells = [r[1][0] for r in rows]
        self.at("the healed suites")
        self.play(FadeIn(header), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.4) for r in rows], lag_ratio=0.25), run_time=1.2, rate_func=smooth)
        role, role_anim = fill(cells[1], 7)
        self.at("role locators")
        self.play(role_anim)
        ids, ids_anim = fill(cells[2], 7)
        self.at("and test")
        self.play(ids_anim)
        css, css_anim = fill(cells[0], 0, 0.7)
        self.at("passed none")
        self.play(css_anim, Indicate(rows[0][0], color=BAD, scale_factor=1.08))

        lines = [
            ("5", 0, "async function login(page: Page) {", None),
            ("6", 1, 'await page.goto("/");', None),
            ("7", 1, 'await page.locator("#field-user").fill("demo");', '"#field-user"'),
            ("8", 1, 'await page.locator("#field-pass").fill("demo123");', '"#field-pass"'),
            ("9", 1, 'await page.locator(".submit-action").click();', '".submit-action"'),
            ("10", 0, "}", None),
        ]
        cw = code("M" * 20, CODE_SIZE).width / 20
        left, top, step = -5.6, 2.45, 0.52
        gutter, body = VGroup(), VGroup()
        for i, (n, indent, s, sel) in enumerate(lines):
            y = top - i * step
            gutter.add(code(n, CODE_SIZE - 4, DIM).move_to([left - 0.35, y, 0], aligned_edge=RIGHT))
            body.add(code_line(s, sel).move_to([left + indent * 4 * cw, y, 0], aligned_edge=LEFT))
        panel = RoundedRectangle(corner_radius=0.12, width=12.6, height=len(lines) * step + 0.9, color=LINE, stroke_width=3)
        panel.set_fill(LINE, opacity=0.3).move_to([0, top - (len(lines) - 1) * step / 2 + 0.12, 0])
        path = code("tests-healed/css-legacy.spec.ts", 18, DIM).next_to(panel, UP, buff=0.18).align_to(panel, LEFT)
        badge = code("round 1  ·  5ecdf1d", 18, ACCENT).next_to(panel, UP, buff=0.18).align_to(panel, RIGHT)
        self.at("the username selector")
        self.play(
            FadeOut(VGroup(header, rows[1], rows[2], role, ids), shift=DOWN * 0.3),
            ReplacementTransform(VGroup(rows[0], css), path),
            FadeOut(title, shift=UP * 0.3),
            FadeIn(panel),
            LaggedStart(*[FadeIn(VGroup(g, b), shift=UP * 0.12) for g, b in zip(gutter, body)], lag_ratio=0.08),
            run_time=1.1, rate_func=smooth,
        )
        self.play(FadeIn(badge), run_time=0.3)

        markup_src = '<input id="fld_9a2b" class="Login_input__k3x9">'
        markup = code_line(markup_src, 'id="fld_9a2b"', NOTE)
        mpanel = RoundedRectangle(corner_radius=0.12, width=markup.width + 0.8, height=0.95, color=NOTE, stroke_width=2)
        mpanel.set_fill(NOTE, opacity=0.08).move_to([0, -1.75, 0]).align_to(panel, LEFT)
        markup.move_to(mpanel).align_to(mpanel, LEFT).shift(RIGHT * 0.4)
        mtag = code("app/v3/index.html:24", 16, DIM).next_to(mpanel, UP, buff=0.14).align_to(mpanel, LEFT)
        self.at("renamed again")
        self.play(FadeIn(VGroup(mpanel, markup), shift=UP * 0.25), FadeIn(mtag), run_time=0.7, rate_func=smooth)

        sel7 = span(body[2], lines[2][2], '"#field-user"')
        cross = Line(sel7.get_left() + LEFT * 0.06, sel7.get_right() + RIGHT * 0.06, color=BAD, stroke_width=4)
        target = span(markup, markup_src, 'id="fld_9a2b"')
        link = DashedLine(target.get_top() + UP * 0.12, sel7.get_bottom() + DOWN * 0.1, color=BAD, stroke_width=3, dash_length=0.12)
        miss = code("no match", 18, BAD).next_to(link.get_center(), RIGHT, buff=0.35)
        rest = VGroup(*[m for i, m in enumerate(body) if i != 2], *[g for i, g in enumerate(gutter) if i != 2])
        self.at("pointed at nothing")
        self.play(
            self.camera_to(11.6, [-0.6, 0.2, 0]),
            rest.animate.set_opacity(0.3),
            sel7.animate.set_color(BAD),
            Create(cross), Create(link), FadeIn(miss, shift=LEFT * 0.1),
            run_time=0.9, rate_func=smooth,
        )

        badge2 = code("round 2  ·  3m 23s", 18, ACCENT).move_to(badge, aligned_edge=RIGHT)
        self.at("second round")
        self.play(
            self.camera_to(), FadeOut(badge, shift=UP * 0.2), FadeIn(badge2, shift=UP * 0.2),
            FadeOut(VGroup(cross, link, miss)), rest.animate.set_opacity(1),
            run_time=0.9, rate_func=smooth,
        )

        repaired = [
            ('await page.locator("#fld_9a2b").fill("demo");', '"#fld_9a2b"'),
            ('await page.locator("#fld_4c1d").fill("demo123");', '"#fld_4c1d"'),
            ('await page.locator(".Login_submit__w6f4").click();', '".Login_submit__w6f4"'),
        ]
        new_lines, swaps = [], []
        for k, (s, sel) in enumerate(repaired):
            old, old_s, old_sel = body[2 + k], lines[2 + k][2], lines[2 + k][3]
            new = code_line(s, sel).move_to(old, aligned_edge=LEFT)
            new_lines.append(new)
            a, b = old_s.index(old_sel), old_s.index(old_sel) + len(old_sel)
            na, nb = s.index(sel), s.index(sel) + len(sel)
            swaps.append(AnimationGroup(
                FadeOut(span(old, old_s, old_s[a:b]), shift=UP * 0.25),
                FadeIn(span(new, s, s[na:nb]), shift=UP * 0.25),
                ReplacementTransform(span(old, old_s, old_s[b:]), span(new, s, s[nb:])),
            ))
        self.at("repaired all seven")
        self.play(LaggedStart(*swaps, lag_ratio=0.3), run_time=1.6, rate_func=smooth)
        for k, new in enumerate(new_lines):
            self.remove(body[2 + k])
            self.add(new)

        unders = VGroup(*[underline(span(new_lines[k], repaired[k][0], h)) for k, h in enumerate(["9a2b", "4c1d", "w6f4"])])
        self.at("hashed class names")
        self.play(
            LaggedStart(*[Create(u) for u in unders], lag_ratio=0.25),
            *[span(n, s, sel).animate.set_color(WARN) for n, (s, sel) in zip(new_lines, repaired)],
            run_time=0.9,
        )

        quote = VGroup(
            code('"structurally fragile ...', 22),
            code('likely to regenerate on the next rebuild"', 22),
        ).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
        qpanel = RoundedRectangle(corner_radius=0.12, width=quote.width + 0.8, height=quote.height + 0.6, color=WARN, stroke_width=2)
        qpanel.set_fill(WARN, opacity=0.08).move_to(mpanel, aligned_edge=UL).shift(DOWN * 0.05)
        quote.move_to(qpanel).align_to(qpanel, LEFT).shift(RIGHT * 0.4)
        qtag = code("healer report  ·  round 2  ·  README.md:65", 16, DIM).move_to(mtag, aligned_edge=LEFT)
        self.at("the healer's own report")
        self.play(
            ReplacementTransform(mpanel, qpanel), FadeOut(markup, shift=UP * 0.15), FadeIn(quote, shift=UP * 0.15),
            ReplacementTransform(mtag, qtag), self.camera_to(13.6, [0, 0.1, 0]),
            run_time=0.9, rate_func=smooth,
        )
        rebuild = span(quote[1], 'likely to regenerate on the next rebuild"', "next rebuild")
        self.at("next rebuild")
        self.play(Create(underline(rebuild)), rebuild.animate.set_color(WARN), run_time=0.6)
        caption = txt("repaired in kind anyway", 30, ACCENT).next_to(qpanel, DOWN, buff=0.4).align_to(qpanel, LEFT)
        self.at("anyway", offset=-0.5)
        self.play(FadeIn(caption, shift=UP * 0.2), run_time=0.7, rate_func=smooth)
        self.end()


class S6Count(Timed):
    def construct(self):
        title = code("repairs across 2 releases", 22, DIM).to_edge(UP, buff=0.7)
        self.add(title)
        unit = 0.58
        bars = []
        for i, (suite, color) in enumerate([("CSS selectors", BAD), ("role locators", GOOD), ("test IDs", GOOD)]):
            y = 1.2 - i * 1.3
            label = txt(suite, 28).move_to([-6.2, y, 0], aligned_edge=LEFT)
            n = ValueTracker(0)
            bar = always_redraw(lambda n=n, y=y, color=color: Rectangle(
                width=max(n.get_value(), 0.02) * unit, height=0.6, color=color, stroke_width=2,
            ).set_fill(color, opacity=0.35).move_to([-2.6, y, 0], aligned_edge=LEFT))
            num = always_redraw(lambda n=n, bar=bar, color=color: code(str(round(n.get_value())), 28, color).next_to(bar, RIGHT, buff=0.25))
            bars.append((label, n, bar, num))
        split = code("round 1: 7  ·  round 2: 7", 16, DIM).move_to([-2.6, 1.2 - 0.48, 0], aligned_edge=UL)

        def grow(i, value, run_time):
            label, n, bar, num = bars[i]
            return n.animate(run_time=run_time, rate_func=smooth).set_value(value)

        labels = [b[0].set_color(DIM) for b in bars]
        self.at("count the repairs")
        self.play(LaggedStart(*[FadeIn(lb, shift=RIGHT * 0.25) for lb in labels], lag_ratio=0.2), run_time=0.8)
        label, _, bar, num = bars[0]
        self.at("the css suite needed")
        self.add(bar, num)
        self.play(label.animate.set_color(PRIMARY), grow(0, 7, 0.7))
        self.play(grow(0, 14, 0.7), FadeIn(split))
        for i, phrase, value in [(1, "role locators needed", 2), (2, "test id needed", 1)]:
            label, _, bar, num = bars[i]
            self.at(phrase)
            self.add(bar, num)
            self.play(label.animate.set_color(PRIMARY), grow(i, value, 0.6))

        caption = VGroup(
            txt("locator strategy set the cost", 30),
            txt("healing paid it again each release", 30, ACCENT),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.7)
        self.at("locator strategy")
        self.play(FadeIn(caption[0], shift=UP * 0.2), run_time=0.8)
        self.at("paid it again")
        self.play(FadeIn(caption[1], shift=UP * 0.2), self.camera_to(13.4, [0, -0.3, 0]), run_time=0.9, rate_func=smooth)
        self.end()


class S7Signal(Timed):
    def construct(self):
        title = code("the 2 role locator failures", 22, DIM).to_edge(UP, buff=0.7)
        self.add(title)
        tag = code("user-facing name changes", 20, WARN).next_to(title, DOWN, buff=0.3)
        rows = [
            repair_row("v1 → v2", 'button "Done"', 'button "Complete"', 1.3),
            repair_row("v1 → v2", 'button "Add"', 'button "Add task"', 0.2),
        ]
        for row in rows:
            row[2].set_color(WARN)
            row[3].set_color(WARN)
        self.at("real changes for users")
        self.play(FadeIn(tag, shift=DOWN * 0.15), run_time=0.5)
        for row, phrase in zip(rows, ["done became", "add became"]):
            self.at(phrase)
            self.play(FadeIn(row[0]), FadeIn(row[1]), grow_arrow(row[2]), FadeIn(row[3], shift=RIGHT * 0.15), run_time=0.8)

        heard_src = "app/v2/index.html:103  setAttribute('aria-label', 'Complete')"
        heard = code(heard_src, 18, DIM).move_to([-6.2, -1.0, 0], aligned_edge=LEFT)
        span(heard, heard_src, "'Complete'").set_color(WARN)
        repaired = txt("healer repaired both", 28, ACCENT)
        nobody = txt("nobody decided", 28, BAD)
        verdict = VGroup(repaired, txt("·", 28, DIM), nobody).arrange(RIGHT, buff=0.25).move_to([0, -2.3, 0])
        self.at("a screen reader user")
        self.play(FadeIn(heard, shift=UP * 0.15), run_time=0.7)
        self.at("the healer repaired both")
        self.play(FadeIn(VGroup(repaired, verdict[1]), shift=UP * 0.15), run_time=0.6)
        self.at("nobody decided")
        self.play(FadeIn(nobody, shift=UP * 0.15), run_time=0.6)

        steps = flow(["healer proposes", "pull request", "person decides why"], width=3.6, gap=0.55, color=DIM, size=22).move_to([0, 0.9, 0])
        boxes, links = steps
        self.at("so use the healer")
        self.play(
            FadeOut(VGroup(*rows, heard, verdict), shift=UP * 0.4),
            Transform(title, code("what to do instead", 22, DIM).to_edge(UP, buff=0.7)),
            FadeOut(tag),
            run_time=0.7, rate_func=smooth,
        )
        self.at("propose fixes")
        self.play(FadeIn(boxes[0], shift=RIGHT * 0.2), run_time=0.5)
        self.at("pull request")
        self.play(grow_arrow(links[0]), FadeIn(boxes[1], shift=RIGHT * 0.2), run_time=0.6)
        self.at("keep a person")
        self.play(grow_arrow(links[1]), FadeIn(boxes[2], shift=RIGHT * 0.2), run_time=0.6)
        self.at("why each test broke")
        self.play(light_up(boxes[0], ACCENT), light_up(boxes[2], GOOD), run_time=0.7)

        caveats = VGroup(
            code("caveats", 20, DIM),
            txt("drift written by me", 26),
            txt("one small app  ·  one healer", 26),
            txt("rerun on your own suite", 26),
        ).arrange(DOWN, buff=0.24, aligned_edge=LEFT).move_to([0, -1.9, 0])
        self.at("one caveat")
        self.play(steps.animate.set_opacity(0.35), FadeIn(caveats[0]), run_time=0.6)
        for phrase, item in zip(["i wrote the drift", "the app is small", "run it on your own"], caveats[1:]):
            self.at(phrase)
            self.play(FadeIn(item, shift=UP * 0.1), run_time=0.5)
        self.end()


class S8EndCard(Timed):
    DRIFT = 0

    def construct(self):
        # Right half stays empty for YouTube's end-screen elements
        brand = VGroup(Dot(radius=0.1, color=GOOD), code("gary-parker", 24, GOOD)).arrange(RIGHT, buff=0.2)
        brand.move_to([-6.1, 3.0, 0], aligned_edge=LEFT)
        rows = VGroup()
        for key, value in [
            ("SOURCE", "github.com/qa-gary-parker/\npoc-self-healing-selectors"),
            ("WRITE-UP", "garyparker.dev/blog/\nself-healing-tests-what-\nvendors-arent-telling-you"),
        ]:
            rows.add(VGroup(code(key, 16, DIM), code(value, 24, line_spacing=0.8)).arrange(DOWN, buff=0.18, aligned_edge=LEFT))
        rows.arrange(DOWN, buff=0.6, aligned_edge=LEFT).next_to(brand, DOWN, buff=0.9).align_to(brand, LEFT)
        summary = code("repairs  ·  CSS 14  ·  roles 2  ·  test IDs 1", 20, DIM).move_to([-6.1, -3.0, 0], aligned_edge=LEFT)
        self.add(brand, rows, summary)
        self.end(minimum=10.0)

from manim import *
from scenekit import *

LINE = "#2E332F"
SUITES = ["CSS selectors", "role locators", "test IDs"]
TESTS = ["invalid credentials", "logs in", "adds a task", "completes a task", "filters active", "filters completed", "active count"]


def code(s, size=22, color=PRIMARY, **kw):
    return Text(s, font=MONO, font_size=size, color=color, **kw)


def cell(w=1.6, h=0.66):
    box = RoundedRectangle(corner_radius=0.08, width=w, height=h, color=LINE, stroke_width=2)
    box.set_fill(LINE, opacity=0.35)
    return box


def count_color(n):
    return GOOD if n == 7 else BAD if n == 0 else WARN


def fill(box, n):
    color = count_color(n)
    label = code(f"{n}/7", 24, color).move_to(box)
    return AnimationGroup(box.animate.set_stroke(color).set_fill(color, opacity=0.16), FadeIn(label))


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


def show_row(row):
    return [FadeIn(row[0]), FadeIn(row[1]), grow_arrow(row[2]), FadeIn(row[3], shift=RIGHT * 0.15)]


def strike(mob, color=BAD):
    return Line(mob.get_left() + LEFT * 0.08, mob.get_right() + RIGHT * 0.08, color=color, stroke_width=4)


class S1Result(Narrated):
    def construct(self):
        title = code("Playwright test-healer agent  ·  round 1", 22, DIM).to_edge(UP, buff=0.7)
        big = code("10/10 repaired", 64, GOOD)
        sub = code("4m 36s  ·  0 incorrect", 26, DIM).next_to(big, DOWN, buff=0.3)
        VGroup(big, sub).move_to([0, 1.0, 0])
        with self.beat(0):
            self.play(FadeIn(title), run_time=0.6)
            self.play(FadeIn(big, scale=0.9), run_time=1.2)
            self.play(FadeIn(sub), run_time=0.6)
        nxt = VGroup(code("next release:", 26, DIM), code("healed CSS suite 0/7", 34, BAD)).arrange(RIGHT, buff=0.35)
        nxt.move_to([0, -1.3, 0])
        with self.beat(1):
            self.play(FadeIn(nxt, shift=UP * 0.2), run_time=1.2)
        caption = txt("same fragility  ·  new names", 32, ACCENT).to_edge(DOWN, buff=0.9)
        with self.beat(2):
            self.play(big.animate.set_opacity(0.35), sub.animate.set_opacity(0.35), run_time=0.6)
            self.play(FadeIn(caption, shift=UP * 0.2), run_time=1.0)
        self.clear_all()


class S2Setup(Narrated):
    def construct(self):
        versions = flow(["v1", "v2  redesign", "v3  CSS modules"], width=3.6, gap=0.9, color=NOTE, size=24)
        versions.move_to([0, 2.5, 0])
        boxes, arrows = versions
        note = code("same behaviour  ·  only the markup drifts", 20, DIM).next_to(versions, DOWN, buff=0.35)
        with self.beat(0):
            self.play(FadeIn(boxes[0]), run_time=0.6)
            self.play(grow_arrow(arrows[0]), FadeIn(boxes[1]), run_time=0.8)
            self.play(grow_arrow(arrows[1]), FadeIn(boxes[2]), run_time=0.8)
            self.play(FadeIn(note), run_time=0.6)

        def details(items, box):
            group = VGroup(*[code(s, 21) for s in items]).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
            return group.next_to(note, DOWN, buff=0.7).set_x(box.get_x())

        v2 = details(["ids + classes renamed", "2 buttons → icons", "1 test ID renamed"], boxes[1])
        v3 = details(["every class hashed", "ids regenerated", "names + test IDs kept"], boxes[2])
        with self.beat(1):
            self.play(light_up(boxes[1], WARN), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(t, shift=DOWN * 0.1) for t in v2], lag_ratio=0.7), run_time=3.6)
        with self.beat(2):
            self.play(light_up(boxes[2], WARN), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(t, shift=DOWN * 0.1) for t in v3], lag_ratio=0.7), run_time=3.6)
        with self.beat(3):
            self.clear_all()
            title = code("7 scenarios  ×  3 suites", 22, DIM).to_edge(UP, buff=0.7)
            samples = [
                ("CSS selectors", 'locator("#username")'),
                ("role locators", 'getByLabel("Username")'),
                ("test IDs", 'getByTestId("username-input")'),
            ]
            rows = VGroup(*[VGroup(txt(n, 30), code(s, 22, DIM)).arrange(DOWN, buff=0.16, aligned_edge=LEFT) for n, s in samples])
            rows.arrange(DOWN, buff=0.55, aligned_edge=LEFT).move_to([0, -0.2, 0])
            ref = code("tests/*.spec.ts  ·  login()", 16, DIM).next_to(rows, DOWN, buff=0.5).align_to(rows, LEFT)
            self.play(FadeIn(title), LaggedStart(*[FadeIn(r, shift=LEFT * 0.2) for r in rows], lag_ratio=0.5), run_time=2.6)
            self.play(FadeIn(ref), run_time=0.4)
        self.clear_all()


class S3Drift(Narrated):
    def construct(self):
        title = code("written once against v1  ·  never updated", 22, DIM).to_edge(UP, buff=0.7)
        header, rows = table(["v1", "v2"])
        with self.beat(0):
            self.play(FadeIn(title), FadeIn(header), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15), run_time=1.4)
            self.play(*[fill(r[1][0], 7) for r in rows], run_time=0.8)
            self.play(fill(rows[1][1][1], 5), run_time=0.6)
            self.play(fill(rows[2][1][1], 6), run_time=0.6)
        with self.beat(1):
            self.play(fill(rows[0][1][1], 0), Indicate(rows[0][0], color=BAD), run_time=0.9)
        with self.beat(2):
            self.clear_all(0.4)
            login = terminal([code(s, 22) for s in ['locator("#username")', 'locator("#password")', 'locator("#login-btn")']])
            login.move_to([-3.7, 0, 0])
            head = code("login form  ·  first step of all 7 tests", 18, DIM).next_to(login, UP, buff=0.25).align_to(login, LEFT)
            tests = VGroup()
            for name in TESTS:
                box = RoundedRectangle(corner_radius=0.06, width=3.3, height=0.44, color=BAD, stroke_width=2)
                box.set_fill(BAD, opacity=0.12)
                tests.add(VGroup(box, code(name, 16, BAD).move_to(box)))
            tests.arrange(DOWN, buff=0.1).move_to([3.6, 0, 0])
            links = VGroup(*[arrow(login.get_right(), t.get_left(), BAD, buff=0.15) for t in tests])
            self.play(FadeIn(head), FadeIn(login), run_time=0.8)
            self.play(LaggedStart(*[grow_arrow(a) for a in links], lag_ratio=0.12), LaggedStart(*[FadeIn(t) for t in tests], lag_ratio=0.12), run_time=1.8)
        self.clear_all()


class S4Heal(Narrated):
    def construct(self):
        title = code("round 1  ·  healer vs v2", 22, DIM).to_edge(UP, buff=0.7)
        failing = card("10 failing", BAD, w=2.8, h=0.9, size=26).move_to([-4.6, 0.6, 0])
        healer = card("test-healer agent", ACCENT, w=3.6, h=0.9, size=26).move_to([0, 0.6, 0])
        fixed = card("10 repaired", GOOD, w=2.8, h=0.9, size=26).move_to([4.6, 0.6, 0])
        a1 = arrow(failing.get_right(), healer.get_left(), DIM)
        a2 = arrow(healer.get_right(), fixed.get_left(), DIM)
        stats = code("4m 36s  ·  0 incorrect", 26, DIM).next_to(healer, DOWN, buff=0.7)
        with self.beat(0):
            self.play(FadeIn(title), FadeIn(failing), run_time=0.8)
            self.play(grow_arrow(a1), FadeIn(healer), run_time=1.0)
            self.play(grow_arrow(a2), FadeIn(fixed), run_time=1.0)
            self.play(FadeIn(stats), run_time=0.6)
        head = code("every repair in kind", 22, ACCENT).move_to([-6.2, 2.0, 0], aligned_edge=LEFT)
        rows = [
            repair_row("CSS selectors", '"#username"', '"#field-user"', 0.8),
            repair_row("role locators", 'name: "Done"', 'name: "Complete"', -0.4),
            repair_row("test IDs", '"active-count"', '"task-counter"', -1.6),
        ]
        ref = code("tests → tests-healed  ·  commit 5ecdf1d", 16, DIM).move_to([-6.2, -2.8, 0], aligned_edge=LEFT)
        with self.beat(1):
            self.play(*[FadeOut(m) for m in (failing, healer, fixed, a1, a2, stats)], run_time=0.5)
            self.play(FadeIn(head), run_time=0.5)
            self.play(*show_row(rows[0]), run_time=1.2)
        with self.beat(2):
            self.play(*show_row(rows[1]), run_time=1.2)
            self.play(*show_row(rows[2]), run_time=1.2)
            self.play(FadeIn(ref), run_time=0.4)
        self.clear_all()


class S5NextRelease(Narrated):
    def construct(self):
        title = code("healed at v2  ·  run against v3", 22, DIM).to_edge(UP, buff=0.7)
        header, rows = table(["v3"], x=1.4)
        with self.beat(0):
            self.play(FadeIn(title), FadeIn(header), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15), run_time=1.4)
        with self.beat(1):
            self.play(fill(rows[1][1][0], 7), fill(rows[2][1][0], 7), run_time=1.0)
            self.wait(1.2)
            self.play(fill(rows[0][1][0], 0), Indicate(rows[0][0], color=BAD), run_time=1.0)
        with self.beat(2):
            self.play(*[FadeOut(m) for m in self.mobjects if m is not title], run_time=0.4)
            old = code('"#username"', 28, DIM)
            mid = code('"#field-user"', 28, ACCENT)
            VGroup(old, mid).arrange(RIGHT, buff=1.6).move_to([-1.6, 1.2, 0])
            link = arrow(old.get_right(), mid.get_left(), ACCENT, buff=0.22)
            tags = VGroup(code("v1 test", 16, DIM).next_to(old, UP, buff=0.2), code("round 1 repair", 16, DIM).next_to(mid, UP, buff=0.2))
            markup = code('<input id="fld_9a2b">', 26, PRIMARY).move_to([-1.6, -0.6, 0]).align_to(mid, LEFT)
            mtag = code("v3 markup  ·  app/v3/index.html:24", 16, DIM).next_to(markup, DOWN, buff=0.2).align_to(markup, LEFT)
            cross = strike(mid)
            miss = code("no match", 20, BAD).next_to(mid, RIGHT, buff=0.35)
            self.play(FadeIn(old), FadeIn(tags[0]), run_time=0.5)
            self.play(grow_arrow(link), FadeIn(mid), FadeIn(tags[1]), run_time=0.8)
            self.play(FadeIn(markup), FadeIn(mtag), run_time=0.7)
            self.play(Create(cross), FadeIn(miss), mid.animate.set_color(BAD), run_time=0.8)
        with self.beat(3):
            self.play(*[FadeOut(m) for m in (old, mid, link, tags, markup, mtag, cross, miss)], run_time=0.5)
            r2 = code("round 2  ·  3m 23s  ·  7 repaired", 24, ACCENT).move_to([-6.2, 1.6, 0], aligned_edge=LEFT)
            fixes = [
                repair_row("username", '"#field-user"', '"#fld_9a2b"', 0.3, 22),
                repair_row("login button", '".submit-action"', '".Login_submit__w6f4"', -0.9, 22),
            ]
            self.play(FadeIn(r2), run_time=0.6)
            self.play(*show_row(fixes[0]), run_time=1.1)
            self.play(*show_row(fixes[1]), run_time=1.1)
        with self.beat(4):
            self.play(*[FadeOut(m) for m in (r2, *fixes)], run_time=0.5)
            quote = terminal([
                code('"structurally fragile ...', 24),
                code('likely to regenerate on the next rebuild"', 24),
            ])
            quote.move_to([0, 0.6, 0])
            who = code("healer report  ·  round 2  ·  README.md:65", 16, DIM).next_to(quote, DOWN, buff=0.25).align_to(quote, LEFT)
            after = txt("repaired in kind anyway", 32, ACCENT).next_to(who, DOWN, buff=0.8)
            self.play(FadeIn(quote), FadeIn(who), run_time=1.0)
            self.wait(1.6)
            self.play(FadeIn(after, shift=UP * 0.2), run_time=0.8)
        self.clear_all()


class S6Count(Narrated):
    def construct(self):
        title = code("repairs across 2 releases", 22, DIM).to_edge(UP, buff=0.7)
        with self.beat(0):
            self.play(FadeIn(title), run_time=0.6)
        unit = 0.58
        bars = VGroup()
        for i, (suite, n, color) in enumerate([("CSS selectors", 14, BAD), ("role locators", 2, GOOD), ("test IDs", 1, GOOD)]):
            y = 1.2 - i * 1.3
            label = txt(suite, 28).move_to([-6.2, y, 0], aligned_edge=LEFT)
            bar = Rectangle(width=n * unit, height=0.6, color=color, stroke_width=2).set_fill(color, opacity=0.35)
            bar.move_to([-2.6, y, 0], aligned_edge=LEFT)
            num = code(str(n), 28, color).next_to(bar, RIGHT, buff=0.25)
            bars.add(VGroup(label, bar, num))
        split = code("round 1: 7  ·  round 2: 7", 16, DIM).next_to(bars[0][1], DOWN, buff=0.14).align_to(bars[0][1], LEFT)
        with self.beat(1):
            self.play(FadeIn(bars[0][0]), GrowFromEdge(bars[0][1], LEFT), run_time=1.2)
            self.play(FadeIn(bars[0][2]), FadeIn(split), run_time=0.4)
            self.play(*[FadeIn(b[0]) for b in bars[1:]], *[GrowFromEdge(b[1], LEFT) for b in bars[1:]], run_time=0.9)
            self.play(*[FadeIn(b[2]) for b in bars[1:]], run_time=0.4)
        caption = VGroup(
            txt("locator strategy set the cost", 30),
            txt("healing paid it again each release", 30, ACCENT),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.7)
        with self.beat(2):
            self.play(FadeIn(caption[0], shift=UP * 0.2), run_time=0.9)
            self.play(FadeIn(caption[1], shift=UP * 0.2), run_time=0.9)
        self.clear_all()


class S7Signal(Narrated):
    def construct(self):
        title = code("the 2 role locator failures", 22, DIM).to_edge(UP, buff=0.7)
        rows = [
            repair_row("v1 → v2", 'button "Done"', 'button "Complete"', 1.3),
            repair_row("v1 → v2", 'button "Add"', 'button "Add task"', 0.2),
        ]
        for row in rows:
            row[3].set_color(WARN)
            row[2].set_color(WARN)
        tag = code("user-facing name change", 20, WARN).move_to([-2.9, -0.8, 0], aligned_edge=LEFT)
        with self.beat(0):
            self.play(FadeIn(title), run_time=0.5)
            self.play(*show_row(rows[0]), run_time=1.1)
            self.play(*show_row(rows[1]), run_time=1.1)
            self.play(FadeIn(tag), run_time=0.5)
        heard = code("app/v2/index.html:103  setAttribute('aria-label', 'Complete')", 18, DIM).move_to([-6.2, -1.7, 0], aligned_edge=LEFT)
        verdict = VGroup(txt("healer repaired both", 28, ACCENT), txt("·", 28, DIM), txt("nobody decided", 28, BAD)).arrange(RIGHT, buff=0.25)
        verdict.move_to([0, -2.8, 0])
        with self.beat(1):
            self.play(FadeIn(heard), run_time=0.7)
            self.wait(1.4)
            self.play(FadeIn(verdict, shift=UP * 0.2), run_time=1.0)
        with self.beat(2):
            self.clear_all(0.5)
            steps = flow(["healer proposes", "pull request", "person decides why"], width=3.6, gap=0.55, color=DIM, size=22)
            steps.move_to([0, 0.9, 0])
            boxes, links = steps
            self.play(FadeIn(boxes[0]), run_time=0.5)
            self.play(grow_arrow(links[0]), FadeIn(boxes[1]), run_time=0.6)
            self.play(grow_arrow(links[1]), FadeIn(boxes[2]), run_time=0.6)
            self.play(light_up(boxes[0], ACCENT), light_up(boxes[2], GOOD), run_time=0.7)
        with self.beat(3):
            caveats = VGroup(
                code("caveats", 20, DIM),
                txt("drift written by me", 26),
                txt("one small app  ·  one healer", 26),
                txt("rerun on your own suite", 26),
            ).arrange(DOWN, buff=0.24, aligned_edge=LEFT).move_to([0, -1.9, 0])
            self.play(steps.animate.set_opacity(0.35), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in caveats], lag_ratio=0.6), run_time=3.4)
        self.clear_all()


class S8EndCard(Narrated):
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
        start = self.renderer.time
        with self.beat(0):
            self.play(FadeIn(brand), FadeIn(rows), FadeIn(summary), run_time=0.6)
        self.wait(max(0.0, 10.0 - (self.renderer.time - start)))

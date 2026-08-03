# poc-self-healing-selectors

**The question:** every 2026 trend report leads with self-healing test automation.
Does healing actually reduce locator maintenance — or just automate paying for it?

**The answer:** the healer repaired every broken test quickly and correctly — and
**in kind**. Brittle CSS selectors came back as new brittle CSS selectors, which
broke again wholesale at the very next release. Meanwhile the suites written with
user-facing locators and test-id contracts needed one or two repairs *ever*, then
survived further drift untouched. Healing serviced the debt; it never paid it down.

> Exploratory PoC, throwaway by default. Written up in
> [Self-healing tests: what the vendors aren't telling you](https://garyparker.dev/blog/self-healing-tests-what-vendors-arent-telling-you).

## Method

A tiny task-manager app ([`app/`](app/)) exists in three versions simulating two
releases of realistic UI drift:

- **v1 → v2** — a redesign sprint: every id and class renamed (BEM-ish), two
  buttons became icon buttons (accessible names changed), one `data-testid`
  renamed. Behaviour identical.
- **v2 → v3** — a CSS-modules migration: every class hashed, ids regenerated.
  Accessible names and test-ids untouched. Behaviour identical.

Three suites cover the same 7 scenarios, differing only in locator strategy:

- [`css-legacy.spec.ts`](tests/css-legacy.spec.ts) — id/class CSS selectors, the way legacy suites are written
- [`aria-first.spec.ts`](tests/aria-first.spec.ts) — roles, labels, accessible names (what Playwright's docs recommend)
- [`test-ids.spec.ts`](tests/test-ids.spec.ts) — dedicated `data-testid` attributes

The healer is Playwright's official test-healer agent (`npx playwright
init-agents --loop=claude`), run headless. Round 1 healed the broken suites
against v2; the healed suites then ran against v3; round 2 healed the survivors'
wreckage against v3.

## Results

**Suite survival across drift** (written once against v1, never updated):

| Suite | v1 | v2 (redesign) | v3 (CSS-modules) |
|---|---|---|---|
| CSS legacy | 7/7 | **0/7** | 0/7 |
| ARIA-first | 7/7 | 5/7 | 5/7 |
| test-ids | 7/7 | 6/7 | 6/7 |

The CSS suite didn't degrade — it was annihilated. The login form's three
selectors alone took out all seven tests, because every test logs in first.

**Healing round 1 (against v2):** all 10 failures repaired in **4m 36s**, zero
incorrect repairs. Every repair was in-kind: CSS → new CSS (`#username` →
`#field-user`), accessible name → new accessible name (`Done` → `Complete`),
test-id → new test-id (`active-count` → `task-counter`).

**The healed suite against v3 — the finding that matters:**

| Healed suite | vs v3 |
|---|---|
| CSS legacy (healed at v2) | **0/7 — all broken again** |
| ARIA-first (healed at v2) | 7/7 |
| test-ids (healed at v2) | 7/7 |

**Healing round 2 (against v3):** the CSS suite needed a full second healing
round — all 7 repaired again in **3m 23s**, this time to hashed CSS-modules
classnames. The healer's own report flagged the repairs as "structurally
fragile... likely to regenerate on the next rebuild" — it diagnosed the problem
and repaired in-kind anyway, because translation is the only move it has. The
other two suites never needed touching again.

## What this means

1. **The healer is a locator-translation machine, not a quality-improvement
   machine.** It restores your suite to exactly the fragility it had before. Feed
   it brittleness, get freshly-broken brittleness back next release — forever.
2. **Locator strategy determined maintenance cost far more than healing did.**
   ARIA-first and test-id suites needed 2 and 1 repairs *total* across two
   releases; the CSS suite needed 14.
3. **Nothing is drift-proof.** The ARIA suite broke where a redesign changed what
   users actually see (buttons becoming icons) — arguably tests *should* flag
   that. Test-ids broke only where a developer broke the contract.
4. **Credit where due:** the healer was fast, 100% accurate here, and honoured
   each suite's locator style rather than imposing its own. The tool is good.
   The claim that it eliminates test maintenance is the problem.

## Caveats

- The drift is authored, not organic — modelled on realistic refactors (redesign,
  CSS-modules migration), but still synthetic and deliberately locator-hostile
  to CSS.
- One healer (Playwright's agent, Claude-backed), one app, small suites.
  Commercial self-healing tools use different mechanisms (weighted attribute
  matching, DOM history); this measures the agentic-repair variety.

## Reproduce

```bash
npm ci && npx playwright install chromium
APP_VERSION=v1 npx playwright test                        # 21/21 pass
APP_VERSION=v2 npx playwright test                        # 10 fail
APP_VERSION=v3 SUITE_DIR=tests-healed npx playwright test # healed suite vs next release
```

`tests/` is the untouched original; `tests-healed/` is what the healer produced.
Healing runs used `claude -p` with the agent definitions in `.claude/agents/`.

MIT. Public demo app written for this experiment — no real product code.

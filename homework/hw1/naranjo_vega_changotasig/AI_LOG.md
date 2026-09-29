# AI use log — Duel 1 (Naranjo · Vega · Changotasig)

Per [`resources/ai-policy.md`](../../../resources/ai-policy.md). Append an entry
every time an AI assistant materially shapes work we submit. The last field is
the one that is graded.

---

## The engine and its equivalence tests

**Student:** Nicolás Naranjo
**Tool:** opencode
**What I asked:** implement the benchmark layer (engine + starter +
harness + tests) for BFS/DFS/UCS/IDS/A\* with max-frontier and a hard deadline,
and verify it against the course engines.
**What I got:** `engine.py` (one loop, four disciplines, goal test on
*expansion*, deadline checked per iteration), `starter.py` (thin graded layer so
the copied tests still import `starter`), `test_engine.py` asserting our
BFS/DFS/UCS ≡ `search.search` and our A\* ≡ `gridworld.astar` by *expansion
count* over all 80 instances, plus dominance, equal-cost and timeout tests.
**What I did with it:** ran it. First run hung for 15 minutes, it was because
IDS on a weighted grid is tree
search with no transposition table, so it expands ~3^depth; a 16×16 grid
burned 5 M expansions in 20 s without solving. I then changed the test to
assert `status == timeout` after a 2 s budget instead of waiting forever, and
kept that behaviour as a *documented* result rather than silently "fixing" it
with a closed set, adding one would have changed what IDS means. All 8 tests
pass in 17 s. the 120 s benchmark cell later confirmed 29 M expansions per
timeout.
**Did I understand it?** Yes, i made the search algorithms in past weeks and just needed
to copy them here and ways to test them and get their statistics.

---

## HW1 — benchmark, analyses, figures

**Student:** Nicolás Naranjo
**Tool:** opencode
**What I asked:** write `harness.py` (protocol: 4 levels × 10 instances × 7
algorithms, 120 s timeout, incremental CSV), `analyses.py` (the four required
analyses) and `plots.py`, then run them.
**What I got:** resumable raw CSVs with cost/length/expansions/max-frontier/
seconds and a `status` column. `summary.csv` with medians, Q1/Q3 and timeout
counts over solved runs only. The four analyses as their own CSVs plus a
rendered witness instance for the BFS failure. Six figures.
**What I did with it:** reviewed the statistics myself, medians with IQR, not
means. Timeouts reported as timeouts and excluded from medians but counted next
to them (a size where everything timed out must not show a zero).
**Did I understand it?** Yes, i made the search algorithms in past weeks and just needed
to copy them here and ways to test them and get their statistics.

---

## HW1 — independent review of Part 1 before submission

**Student:** Nicolás Naranjo
**Tool:** opencode (a read-only review sub-agent, then the main session)
**What I asked:** have a separate agent review the whole Part 1 submission
against `hw-1-search.md`, spec compliance, code correctness, statistics, docs.
Re-running the tests and recomputing the numbers itself instead of trusting our
pipeline, and reporting prioritized findings without touching any file.
**What I got:** no blockers, 18/18 tests and 260/260 median/IQR triples
independently reproduced, plus eight real defects: README claims that were off
by orders of magnitude (DFS "5–10× the optimal" is really 1.3×–22× on the grid.
"IDS at 16×16 always times out" is really 5 of 10), the grid arm of analysis 3
running `h × 8` while the spec says `× 3`, an off-by-one in the IDS
`max_frontier` counter, `ids_equals_ucs` reading a timeout as "not equal", a
figure title asserting a speedup the data does not show, a stale docstring, and
a broken relative link.
**What I did with it:** verified every claim against the raw CSVs before
acting, and one of its findings was wrong (it called two README links broken.
resolving them by hand showed only the `AI_LOG` link was), which is exactly why
I re-checked instead of applying the list blind. Then fixed all seven real
findings, re-ran the benchmark from scratch (656 s) and every analysis and
figure. Fixing the timeout/inequality confusion introduced a fresh bug of my own
`None != ""` made 5 timeouts count as solved — which the very next run
exposed as "40/40 solved" against a raw file that says 5 timed out.
**Did I understand it?** Yes. The sub-agent was only used to make sure no bugs slip
past me in part 1.

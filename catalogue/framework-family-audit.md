# Framework Family Audit (8% cap)

Scope: all 440 catalogue entries, each assigned to exactly one family by its Framework field. Cap: no family above 8% of the catalogue, which is at most 35 entries.

## Result

Under this 26-family taxonomy **no family exceeds the cap**. The largest are Optimization, search and scheduling (35), Bayesian updating, bias and sampling (31), Dynamics, feedback and oscillation (28). Optimization sits exactly at the cap (35 of 440, 7.95%) with no headroom, and Bayesian has 4 spare. Any added or reassigned entry in Optimization breaches the cap, so that family is closed to new entries.

| Rank | Family | Entries | Share | Headroom to 35 |
|---|---|---|---|---|
| 1 | Optimization, search and scheduling | 35 | 8.0% | 0 |
| 2 | Bayesian updating, bias and sampling | 31 | 7.0% | 4 |
| 3 | Dynamics, feedback and oscillation | 28 | 6.4% | 7 |
| 4 | Game theory and strategic interaction | 25 | 5.7% | 10 |
| 5 | Logic, computation and formal languages | 24 | 5.5% | 11 |
| 6 | Graphs, networks and topology | 23 | 5.2% | 12 |
| 7 | Coding, cryptography and information | 21 | 4.8% | 14 |
| 8 | Institutions, culture and social relation | 20 | 4.5% | 15 |
| 9 | Language, meaning and convention | 17 | 3.9% | 18 |
| 10 | Symmetry, groups and algebra | 17 | 3.9% | 18 |
| 11 | Statistics: distributions, power laws and extremes | 17 | 3.9% | 18 |
| 12 | Inverse problems and inference from traces | 16 | 3.6% | 19 |
| 13 | Growth, decay and population dynamics | 15 | 3.4% | 20 |
| 14 | Thresholds, tipping points and cascades | 14 | 3.2% | 21 |
| 15 | Fair division, allocation and social choice | 14 | 3.2% | 21 |
| 16 | Queues, flows and throughput | 14 | 3.2% | 21 |
| 17 | Geometry, space and scale | 13 | 3.0% | 22 |
| 18 | Physical and engineering limits | 13 | 3.0% | 22 |
| 19 | Measurement, error and uncertainty propagation | 13 | 3.0% | 22 |
| 20 | Economics: value, scarcity and externalities | 13 | 3.0% | 22 |
| 21 | Coordination, protocols and distributed knowledge | 12 | 2.7% | 23 |
| 22 | Identity and continuity | 11 | 2.5% | 24 |
| 23 | Causal inference and performative feedback | 11 | 2.5% | 24 |
| 24 | Memory, cognition and embodied skill | 11 | 2.5% | 24 |
| 25 | Number, notation and calendars | 6 | 1.4% | 29 |
| 26 | Infinity, limits and continuity | 6 | 1.4% | 29 |
| | **Total** | **440** | 100% | |

## What the result depends on

The cap test is only as strict as the taxonomy is fine. The same catalogue gives different answers at different granularities, so the taxonomy has to be fixed before the cap means anything.

- **Inference and evidence (merging 4 families):** 75 entries, 17.0%. Breaches the cap if read as one family.
- **Dynamical systems (merging 3 families):** 57 entries, 13.0%. Breaches the cap if read as one family.
- **Strategic and economic structure (merging 4 families):** 64 entries, 14.5%. Breaches the cap if read as one family.

The inference cluster is the one to watch. The catalogue leans on evidence, selection and reconstruction as a motif, so a reviewer who treats those as one family would find about 17% of the catalogue in it. If the 8% cap is meant to protect against that kind of dominance, the taxonomy should be agreed on those terms. This audit uses the finer split because the families differ in the mathematics they actually require (Bayes' rule, inverse problems, causal graphs and heavy-tailed statistics are different tools).

## Method and its limits

- Each entry was given one family, assigned from its Framework text by keyword rules in priority order, then every assignment was read and corrected by hand. 22 entries matched no rule and were assigned by hand, and about 20 more were reassigned after review (for example a keyword match on "graph" inside "autobiographical").
- Single assignment hides overlap. Many entries belong to two families (for example 17.01 temporal sampling is both inverse-problem and sampling). A multi-label count would be higher for every family.
- The assignment uses the Framework field only. It does not test whether two entries with different framework labels dramatise the same story shape.
- Conceptual (C) entries are spread over Language, Identity, Institutions, Memory and Economics families, so the cap is tested for them too, but they are the least reliably categorised.
- Cycle 01 entries use a slightly different line format ("| Scale M") and were parsed together with the rest. All 440 matched.

## Recommendations

1. Adopt this 26-family list as the operational definition for the cap.
2. Treat Optimization (35, at cap) as closed and Bayesian (31) as near cap. Replacement entries should come from lower-count families such as Number and calendars, Infinity and limits, Identity, Causal inference or Memory.
3. Resolve the inference cluster question explicitly, since it is the one place where the answer changes with the reading.
4. Run the second audit (graphic treatments, the Look field) before committing the other five slate projects.
5. Keep the CSV beside the catalogue so the check can be rerun after any edit.

## Slate projects by family

- 01.01 The Department of Unclaimed Rooms: Language, meaning and convention
- 03.01 The Last Projectionist: Inverse problems and inference from traces
- 04.01 The Society for Perfect Endings: Logic, computation and formal languages
- 07.01 The Whale Beneath the Railway: Optimization, search and scheduling
- 08.01 Seven Minutes of Summer: Optimization, search and scheduling
- 11.01 A Country Made of Footnotes: Logic, computation and formal languages

Two pairs of slate projects share a family: 07.01 and 08.01 (Optimization), and 04.01 and 11.01 (Logic and formal languages). Optimization is at the cap, so one of 07.01 or 08.01 is a candidate for a different framing if any entry has to move. Otherwise the slate spans four families.

## Full assignment by family

### Optimization, search and scheduling (35)

- 01.20 Zoning the Dead: packing problems
- 03.02 The Ferry Without a River: optimal stopping
- 03.05 The Lighthouse Keeper's Shift Table: constraint satisfaction
- 03.07 The Cobbler of the Closed Mill: local versus global optima
- 03.14 The Night Watchmen's Round: art gallery theorem, coverage
- 03.15 The Salt Road Porters: knapsack and packing
- 05.09 The Dam's Operating Manual: minimax decisions under uncertainty
- 05.16 The Elevator to Nowhere: reachable states
- 07.01 The Whale Beneath the Railway: network dependence, constrained optimization
- 08.01 Seven Minutes of Summer: bounded reachability
- 09.02 Pilgrim's Shortest Road: traveling salesman, heuristics
- 09.03 The Repair Fleet: scheduling
- 09.06 The Lighthouse Circuit: Chinese postman problem
- 09.08 The Ferrymen of the Lagoon: state-space search
- 09.15 The Homing Pigeons' Map: gradient following
- 10.12 The Money Changers' Loop: arbitrage, negative cycles
- 10.20 The Last Ferry Home: interval scheduling
- 11.13 The Translation Tournament: optimization with competing objectives
- 13.12 The Expedition That Turned Back: optimal stopping, option value
- 13.14 The Factory’s Shorter Day: productivity curves, fatigue
- 14.01 The Woman Who Returned the Sun: scheduling, precedence constraints
- 14.03 The Minotaur of Building C: partially observable search
- 14.04 Twelve Tasks Before Closing: resource-constrained scheduling
- 14.09 The Stone on the Loading Ramp: potential functions, progress measures
- 14.11 The House of Opened Gifts: irreversible decisions, option value
- 15.02 A Door Wide Enough: constraint satisfaction, inclusive design
- 15.14 The Stair Count: path cost, heterogeneous metrics
- 16.12 The Marriage of Separate Calendars: periodic scheduling, institutional time
- 16.14 The Two Authors of One Ending: constraint negotiation, incompatible objectives
- 17.03 The House of Impossible Statements: satisfiability, minimal inconsistent subsets
- 20.06 The Detective of Missing Socks: combinatorics, search-space reduction
- 20.07 The Town That Optimized Its Picnic: multi-objective optimization, Pareto efficiency
- 21.02 The Room That Forgets One Object: finite memory, eviction policies
- 21.19 The Orchard of Branching Days: branching time, irreversible choice
- 22.17 Three Journeys of the Same Distance: heterogeneous path costs

### Bayesian updating, bias and sampling (31)

- 01.11 The Water Tower Census: sampling and survivorship bias
- 02.01 The Lodger's Arithmetic: Bayesian updating under filtered evidence
- 02.12 The Cellar Census: capture and recapture estimation
- 03.13 The Almanac Compilers: forecast calibration
- 04.03 The Court of Small Probabilities: base rates, prosecutor's fallacy
- 04.07 The Laboratory of Replicated Results: multiple comparisons
- 04.16 The Inspectorate of Honest Mistakes: error types
- 04.17 The Bell Curve Tribunal: regression to the mean
- 06.02 The Seed Vault Expedition: sampling, representativeness
- 06.11 The Bone Counters: minimum number of individuals
- 06.15 The Typology Wars: clustering, classification
- 06.18 The Reconstruction Committee: overfitting
- 06.20 The Last Dig Season: Bayesian search
- 10.18 The Interpreter at the Gate: base rates, false matches
- 12.01 The Census of Closed Curtains: missing-not-at-random data
- 12.02 The Photograph’s Other Edge: framing, evidential selection
- 12.03 The Catalogue of Almost Matches: entity resolution, nontransitive similarity
- 12.04 The Five Who Agreed: correlated evidence
- 12.07 The Archive Fire Lottery: survivorship bias
- 12.09 The Museum of Borrowed Faces: classification thresholds, asymmetric error costs
- 12.13 The Historian’s Favourite Century: selection bias, denominator neglect
- 12.16 The Unopened Boxes: value of information, search costs

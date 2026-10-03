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

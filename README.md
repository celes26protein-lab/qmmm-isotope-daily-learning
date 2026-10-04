# QM/MM Learning Log: Hydrogen Isotope Effects

A learning log of QM/MM simulations with AmberTools (`sander`),
aimed at hydrogen/deuterium isotope effects. Each step is a small, reproducible
experiment. **Negative results, mistakes and unverified points are kept in the
log on purpose**, because they were the most useful part of learning.

> **Status:** Step A is in progress (first full pass done, replicates not yet run).
> Steps B–D are planned. This is a learning project, not a validated protocol.

## Roadmap

| Step | System | Question | Status |
|---|---|---|---|
| [A](A_NMA_ND/) | N-methylacetamide (NMA) in water, N–H vs N–D | What does a mass change do in QM/MM? Which quantities change, which do not? | first pass done |
| B | Small proton-transfer model | Reaction coordinate; zero-point-energy correction for H vs D | planned |
| C | Small H-abstraction model (O–H, as in antioxidant chemistry) | Radicals / open-shell QM; barrier trends | planned |
| D | Hydrogen isotopes in a carbon nanotube | Quantum sieving; likely needs path-integral methods rather than plain QM/MM | planned |

## Environment

- macOS, conda environment `amber_env`
- AmberTools 24.8 (conda-forge build `cuda_None_nompi`: CPU only, no pmemd)
- `tleap`, `sander` (QM/MM), `cpptraj`, ParmEd
- Force field: ff14SB
- Water model: TIP3P
- Solvation : `solvatebox ... 10.0` (Å)
- QM methods tried: PM3, AM1, PM6, DFTB3 (semi-empirical / tight-binding)

## Foundations (done before step A)

Steps 0–4 were performed on N-methylacetamide (NMA = `ACE`+`NME`) and on the alanine
dipeptide (`ACE ALA NME`) in water. The NMA-in-water setup was based on the system 
used in Ross Walker's AMBER tutorial, A Simple Coupled Potential QM/MM Simulation. 
The input settings in this repository are my own and are not intended to reproduce the tutorial exactly.

| Step | System / QM region | Calculation | What was learned |
|---|---|---|---|
| 0 | NMA in water, MM only | minimisation + 1 ps MD | tleap → sander workflow |
| 1 | NMA, QM = whole NMA (`:1-2`), PM3 | minimisation + 0.1 ps QM/MM MD | reading `&qmmm`; 12 QM atoms, 0 link atoms |
| 2 | Alanine dipeptide, QM = ALA only (`:2`), PM3 | minimisation only | cutting covalent bonds at the boundary gives link atoms (`nlink = 2`, H caps, 1.09 Å) |
| 3 | Same dipeptide and structure | single points with PM3, AM1, PM6, DFTB3 | Mulliken charges depend strongly on the QM method |
| 4 | Same structure, PM6 | single points, QM region = ALA / ACE+ALA / whole dipeptide | charges near the boundary depend strongly on where the boundary is cut |

Selected numbers (alanine dipeptide, converged NPT structure, Mulliken charges):

| Atom (ALA) | PM3 | AM1 | PM6 | DFTB3 |
|---|---|---|---|---|
| N | -0.157 | -0.510 | -0.652 | -0.609 |
| carbonyl C | 0.320 | 0.202 | 0.338 | 0.386 |
| carbonyl O | -0.377 | -0.333 | -0.508 | -0.438 |

| QM region (PM6) | QM atoms | link atoms | N | carbonyl C | carbonyl O |
|---|---|---|---|---|---|
| ALA only | 10 | 2 | -0.652 | 0.338 | -0.508 |
| ACE+ALA | 16 | 1 | -0.391 | 0.395 | -0.455 |
| whole dipeptide | 22 | 0 | -0.384 | 0.548 | -0.644 |

These calculations were performed on a single structure, using one calculation 
per condition. They demonstrate how large the observed differences can be, but 
they are not benchmarks. No experimental data or higher-level electronic-structure 
calculations were used to determine which charge distribution is "correct."

## Lessons learned (mistakes included)

1. **"Finished" is not "converged".** `FINAL RESULTS` is printed even when the
   maximum number of minimisation cycles is reached. Always check `RMS`/`GMAX`.
   My first method comparison used unconverged structures (RMS ≈ 13) and had to be redone.
2. **Minimisation with SHAKE stalled** at the same RMS (≈ 13) after 314 steps and
   did not improve even after 2000+ steps; I did not find the cause. Minimising without
   SHAKE converged (RMS ≈ 0.09), followed by a short SHAKE-on relaxation MD.
3. **NPT needed more time than expected.** After the first 20 ps the density was
   still only ≈ 0.69–0.75 g/cm³ and rising (negative pressure, box shrinking);
   after ~70 ps in total it settled at ≈ 0.98 g/cm³.
4. **Two atom numberings exist in the output**: `QM_NO` (inside the QM region)
   and `MM_NO` (whole system). Do not mix them.
5. **Tools can fail silently.** ParmEd's command line printed "command not
   recognized", still wrote the output file and ended with "Done!"; the file was unchanged.
   Always re-read the result (see step A).

## Scope and Limitations

The calculations in Steps 0–4 are learning experiments, not systematic benchmarks.

In particular:
no statistical replicates were performed;
no convergence study with respect to simulation length was performed;
no systematic QM-method benchmark was performed;
no comparison with experimental observables was performed;
no higher-level QM reference calculation was used.

The numerical results should therefore be interpreted as observations from specific computational setups, rather than general quantitative conclusions about QM/MM accuracy.

## Future Direction

The longer-term goal is to understand where conventional QM/MM is useful for isotope effects and where it becomes insufficient.
In particular, the project will explore the transition from:

classical MD → QM/MM → zero-point effects → proton transfer → isotope-dependent dynamics → nuclear quantum effects

Step D is expected to be especially important because phenomena such as quantum sieving may require methods that explicitly account for nuclear quantum effects, rather than simply changing hydrogen masses in a conventional QM/MM simulation.

## License

MIT
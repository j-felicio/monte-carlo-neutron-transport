# Monte Carlo Neutron Transport: Reflector Material and Thickness

**Educational PHYS 210 course project — portfolio edition.** A simplified 3D two-region Monte Carlo neutron-transport model investigating how reflector composition and thickness influence a *fission-to-fission reproduction statistic* in a homogenized uranium-dioxide core. This is **not** a reactor-design or validated criticality tool.

## What the notebook does

- Tracks individual simulated neutrons through a cubic core and outer reflector using sampled directions, interaction distances and reaction channels.
- Reads energy-dependent microscopic cross sections from tabular JANIS exports of ENDF/B-VIII data.
- Compares graphite, light water and heavy water reflectors with a common model and baseline core configuration.
- Visualizes neutron paths, reaction probabilities, generation-level statistics, Monte Carlo uncertainty, and terminal-outcome fractions.

## Files

- [`Neutron_Transport_Monte_Carlo.ipynb`](Neutron_Transport_Monte_Carlo.ipynb) — full report, model definitions, and figure-generation code.
- [`data/`](data/) — 14 cross-section CSVs consumed by the notebook (`*_es` = elastic scattering, `*_c` = radiative capture, `*_f` = fission).
- [`run_tests.py`](run_tests.py) — fast smoke tests for geometry, collision cutoffs, energy scattering and reproducibility.

## Run

Requires Python 3.10+.

```bash
python -m pip install -r requirements.txt
python run_tests.py
jupyter lab Neutron_Transport_Monte_Carlo.ipynb
```

In Jupyter choose **Kernel → Restart Kernel and Run All Cells**. Run from the repository root so that `data/` can be found. The full figure sweep can take substantially longer than the smoke tests. 

### Reproducibility

Figure 10 uses stable, explicitly set NumPy random seeds per material/thickness combination; other Monte Carlo figures currently use the notebook's global RNG state and therefore vary between runs. If repeating a result, call `np.random.seed(your_seed)` before its plot cell and document the seed. JANIS cross-section tables use endpoint clamping rather than extrapolation outside their tabulated ranges.

## Limitations and cautions

- The simulated geometry is an idealized homogeneous cube, not a real fuel-pin arrangement.
- Scattering is modeled as stationary-target elastic scattering with simplified nuclear physics. Capture and fission counts come from the provided reaction channels.
- The reported `k` is a project-specific generation-based fission-to-fission statistic, **not** a benchmarked effective multiplication factor for an operating reactor.
- Numerical collision cutoffs terminate histories. The model now reports them separately from physical captures. Large cutoff fractions can bias the estimated reproduction statistic and require sensitivity testing before interpreting results.
- This report is coursework rather than independent peer-reviewed research. Consult its References and Acknowledgements for the source material and original assistance declarations. Verify any third-party data redistribution terms before publicly publishing the CSV exports.

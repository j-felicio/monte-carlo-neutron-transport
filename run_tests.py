"""Fast, deterministic smoke checks for the educational Monte Carlo notebook."""
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
NOTEBOOK = ROOT / "Neutron_Transport_Monte_Carlo.ipynb"
notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))

# The model is developed as a notebook. Load only setup and definitions, never
# the expensive plotting cells; then execute its explicit sanity-check helpers.
namespace = {"__name__": "__notebook_smoke_tests__"}

import os
os.chdir(ROOT)
for i, cell in enumerate(notebook["cells"]):
    code = "".join(cell["source"])
    if cell["cell_type"] == "code" and "def plot_path_trace_generations_xy" in code:
        exec(compile(code, f"notebook cell {i}", "exec"), namespace)
        break
    if cell["cell_type"] == "code":
        exec(compile(code, f"notebook cell {i}", "exec"), namespace)
else:
    raise RuntimeError("Could not find the notebook's figure definitions")

for i, cell in enumerate(notebook["cells"]):
    code = "".join(cell["source"])
    if cell["cell_type"] == "code" and "def test_elastic_scatter_energy_bounds" in code:
        exec(compile(code, f"notebook cell {i}", "exec"), namespace)
        break
else:
    raise RuntimeError("Could not find the notebook's validation functions")

namespace["set_geometry"](48.0, 10.0)
namespace["current_r_material"] = "graphite"
namespace["rebuild_core"]()

namespace["test_elastic_scatter_energy_bounds"](n=300)
namespace["test_boundary_beats_collision"]()
namespace["test_numerical_cutoff_is_not_capture"]()

# A zero-thickness reflector cannot physically absorb neutrons.
measure = namespace["outcome_tallies_one_generation"]
base = measure(n_hist=150, fuel_side_cm=48.0, reflector_thickness_cm=0,
               reflector_material="graphite", seed=2026)
assert base["fractions"]["refl_absorb"] == 0.0
assert base["fractions"]["cutoff"] == 0.0
assert abs(sum(base["fractions"].values()) - 1) < 1e-12

ref = measure(n_hist=150, fuel_side_cm=48.0, reflector_thickness_cm=40,
              reflector_material="graphite", seed=2026)
repeat = measure(n_hist=150, fuel_side_cm=48.0, reflector_thickness_cm=40,
                 reflector_material="graphite", seed=2026)
assert ref["fractions"] == repeat["fractions"]
assert abs(sum(ref["fractions"].values()) - 1) < 1e-12
assert all(0 <= x <= 1 for x in ref["fractions"].values())

print("PASS: outcome proportions sum to 1, no physical captures in absent reflector")
print("PASS: outcome sampling reproducible with fixed seed")
print("All smoke tests passed.")

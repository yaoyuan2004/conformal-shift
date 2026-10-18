# Results and cached outputs

`results/` contains the small, machine-readable Stage 5–8 outputs. The prefix identifies the method or analysis; complete split-specific data is preserved alongside mean/sample-standard-deviation summaries.

- `lac_*`, `aps_*`, `raps_*`: clean thresholds and metrics, corruption metrics, set-size distributions, audits, examples, and paired comparisons.
- `label_shift_*`: class-conditional metrics, fixed target priors, baseline reconstruction audit, Monte Carlo check, split-specific scenario metrics, and paired/summary tables.
- `aps_randomization_uniforms_seed2026.npy`: saved per-image randomization used by APS/RAPS.
- `../cached_outputs/stage4_predictions/`: 20 audited model-condition `.npz` caches plus the accuracy summary, manifest, and model metadata.

Validated tables are inputs to the final analysis. Do not overwrite them by rerunning a notebook unless intentionally regenerating the corresponding stage. Expected audit sizes include 18 clean method/model/split rows, 54 corruption rows per method, 180 class-conditional rows, 126 label-shift split rows, 70 target-prior rows, and 18 baseline reconstruction rows.

Stage 9 tables and figures will be added after the workspace review. Raw CIFAR-10-C arrays are not stored locally; cached prediction outputs are.

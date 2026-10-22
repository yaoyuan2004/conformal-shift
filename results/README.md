# Results and cached outputs

`results/` contains the machine-readable Stage 5–9 outputs. The prefix identifies the method or analysis; split-specific data is preserved alongside mean/sample-standard-deviation summaries.

- `lac_*`, `aps_*`, `raps_*`: clean thresholds and metrics, corruption metrics, set-size distributions, audits, examples, and paired comparisons.
- `label_shift_*`: class-conditional metrics, fixed target priors, baseline reconstruction audit, Monte Carlo check, split-specific scenario metrics, and paired/summary tables.
- `label_shift_rotation_*`: exhaustive two-class emphasis analysis: 136 priors including balanced, 2,448 split-specific results, 816 scenario summaries, 18 all-pair overview rows, and a manifest with source/output hashes. The earlier cat/dog and airplane/automobile tables remain the detailed illustrative subset and reproduce from these complete results.
- `aps_randomization_uniforms_seed2026.npy`: saved per-image randomization used by APS/RAPS.
- `../cached_outputs/stage4_predictions/`: the 20 audited model-condition `.npz` prediction caches, plus the accuracy summary, manifest, and model metadata. The archives contain the saved logits, probabilities, labels, and source indices used by Stages 5–8.

Validated tables are inputs to the final analysis. Do not overwrite them by rerunning a notebook unless intentionally regenerating the corresponding stage. Expected audit sizes include 18 clean method/model/split rows, 54 corruption rows per method, 180 class-conditional rows, and 18 baseline reconstruction rows. The illustrative subset has 126 label-shift split rows and 70 prior rows; the complete rotation has 2,448 split rows and 1,360 prior rows.

For each rotation scenario, means and sample SDs describe the three overlapping splits. The overview then describes the 45 pair means at each level. Equal averaging across all pairs returns balanced metrics by construction; the range, quantiles, and counts below 0.90 show variation across emphasized classes. These pair summaries are not independent-sample uncertainty estimates.

The Stage 9 summary tables are included here. The CIFAR-10-C source arrays are not part of this repository; the committed Stage 4 predictions are sufficient for the downstream analyses.

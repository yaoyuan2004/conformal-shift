# Notebook guide

These notebooks contain the primary experimental workflow. The Colab exports retain their saved outputs; Google Colab commonly leaves `execution_count` unset even when outputs are present.

| Notebook | Stage | Purpose | Saved run output |
|---|---:|---|---|
| `00_environment_and_data.ipynb` | 1 | Runtime, CIFAR-10 loading, and saved disjoint splits | Yes |
| `01_train_models_local_validation.ipynb` | 2 support | Local forward/backward, smoke, overfit, and timing checks only | Yes; not the official training run |
| `01_train_models_standard_colab.ipynb` | 2 | Official 75-epoch standard ResNet-18 training | Yes; completion at epoch 75 |
| `01_train_models_augmix_colab.ipynb` | 3 | Official 75-epoch AugMix ResNet-18 training | Yes; completion at epoch 75 |
| `02_cache_model_outputs_colab.ipynb` | 4 | One-pass cache generation and audit for 20 model-condition pairs | Yes; audit passed 20/20 |
| `03_conformal_methods.ipynb` | 5–7 | LAC, APS, and RAPS calibration and corruption evaluation | Yes; thresholds, clean checks, and shifted tables shown |
| `04_label_shift_experiments.ipynb` | 8 | Class-conditional and analytically reweighted label-shift analysis | Yes; baseline audit and scenario outputs shown |
| `05_final_analysis.ipynb` | 9 | Final tables and figures from saved CSVs | Yes; executed top to bottom, source checks passed |

Stages 5–7 are combined in one executed notebook because the methods share the same cached probabilities, saved splits, and corruption conditions. Corruption evaluation is included there; it does not add another model or shift type.

## Running the notebooks

- Stage 1 reads the existing CIFAR-10 archive or extracted batches and deterministically creates the three calibration/evaluation splits. Dataset files and generated split indices stay outside Git.
- Official model training and Stage 4 cache generation use a CUDA Colab runtime. Google Drive can preserve model outputs and caches across runtime disconnects.
- Stage 4 audits for a complete cache before doing more work. If caches are incomplete, it loads CIFAR-10 and downloads the approved CIFAR-10-C arrays only when needed, then generates the missing predictions.
- Stages 5–8 use the Stage 4 predictions and save their metric tables under `results/`. The large prediction arrays remain local.
- Stage 9 reads the saved Stage 4–8 CSVs and compact metadata in `results/`. It recreates the split partition rule in memory and does not require datasets, saved split files, model weights, or prediction caches.

The local pre-training notebook is supporting evidence. It does not count toward either official 75-epoch run.

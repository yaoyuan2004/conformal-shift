# Notebook guide

These notebooks contain the primary experimental workflow. The Colab exports retain their saved outputs; Google Colab commonly leaves `execution_count` unset even when outputs are present.

| Notebook | Stage | Purpose | Saved run output |
|---|---:|---|---|
| `00_environment_and_data.ipynb` | 1 | Runtime, CIFAR-10 loading, and saved disjoint splits | Yes |
| `01_train_models_local_validation.ipynb` | 2 support | Local forward/backward, smoke, overfit, and timing checks only | Yes; not the official training run |
| `01_train_models_standard_colab.ipynb` | 2 | Official 75-epoch standard ResNet-18 training | Yes; completion at epoch 75 |
| `01_train_models_augmix_colab.ipynb` | 3 | Official 75-epoch AugMix ResNet-18 training | Yes; completion at epoch 75 |
| `02_cache_model_outputs_colab.ipynb` | 4 | One-pass cache generation and audit for 20 model-condition pairs | Yes; audit passed 20/20 |
| `03_conformal_methods.ipynb` | 5–7 | LAC, APS, and RAPS calibration and corruption evaluation | Yes; includes the APS clean-coverage flag and its independent audit |
| `04_label_shift_experiments.ipynb` | 8 | Class-conditional metrics and all 45 emphasized class-pair rotations | Yes; baseline audit, 136 priors, full rotation, and illustrative contrasts |
| `05_final_analysis.ipynb` | 9 | Final tables and figures from saved CSVs | Yes; saved summaries, figures, and source checks |

Stages 5–7 are combined in one executed notebook because the methods share the same cached probabilities, saved splits, and corruption conditions. Corruption evaluation is included there; it does not add another model or shift type.

## Running the notebooks

- The GitHub repository includes the complete Stage 4 prediction cache bundle, the three fixed split-index files, the CIFAR-10 test batch used for label checks, and the APS/RAPS randomization values. Start with Stage 5 in `03_conformal_methods.ipynb` to recompute the clean and corruption metrics, then run Stage 8 in `04_label_shift_experiments.ipynb`. These analyses reuse the saved predictions and run without GPU inference or CIFAR-10-C downloads.
- Stage 4 checks that all 20 prediction files are present and validates them in cache-only mode. If a cache is missing, it generates the missing predictions and needs the approved CIFAR-10-C arrays and fixed model checkpoints. A CUDA Colab runtime is recommended for cache generation.
- `00_environment_and_data.ipynb` uses an existing local CIFAR-10 copy or ZIP; it does not download the raw dataset. It creates the fixed split-index files in `data/splits/`. The complete CIFAR-10 dataset and input ZIPs are not stored in Git; the repository tracks only the CIFAR-10 `test_batch` needed for label checks and the three small split files.
- Official model training requires the local CIFAR-10 training data and a CUDA runtime. `02_cache_model_outputs_colab.ipynb` downloads and extracts the approved CIFAR-10-C arrays only if they are missing. Keep source datasets and downloaded archives outside Git.
- Stage 9 reads the saved Stage 4–8 CSVs and compact metadata in `results/`. It recreates the split partition rule in memory and does not require datasets, saved split files, model weights, or prediction caches. With the default `REGENERATE_FIGURES=False`, it displays newly calculated plots while retaining existing PNG/PDF files; set the option to `True` to replace the saved exports.
- The full-rotation section in Stage 8 can run on its own from the saved class-conditional metrics, baseline audit, and illustrative-result CSVs. It performs CPU reweighting for all 45 pairs and reproduces the existing example rows. Stage 9 includes the full pair-distribution figure and keeps the two detailed contrasts as examples.

The local pre-training notebook is supporting evidence. It does not count toward either official 75-epoch run.

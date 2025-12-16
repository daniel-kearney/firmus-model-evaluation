# Power Variance Analysis Results
**Generated:** 2025-12-16 11:00:32
**Framework:** Firmus Model Evaluation - Power Variance & Tiering (CV > 0.1)

## Executive Summary

### Tiering Distribution:
- **Tier 1 (Stable, CV ≤ 0.1):** 67% of models (4/6)
- **Tier 2 (Moderate, 0.1 < CV ≤ 0.15):** 17% of models (1/6)
- **Tier 3 (Unstable, CV > 0.15):** 17% of models (1/6)

### Model Results:

| Model                     |   Avg Power (W) |   Std Dev (W) |     CV | Tier                     |   Tier Number | Stability   |
|:--------------------------|----------------:|--------------:|-------:|:-------------------------|--------------:|:------------|
| DeepSeek-R1-Distill (32B) |          515.52 |         85.1  | 0.1651 | Tier 3 - High Variance   |             3 | Unstable    |
| Llama-4-Scout (17B)       |          421.23 |         52.45 | 0.1245 | Tier 2 - Medium Variance |             2 | Moderate    |
| Llama-4-Maverick (17B)    |          447.27 |         37.95 | 0.0848 | Tier 1 - Low Variance    |             1 | Stable      |
| Qwen3-32B                 |          490.39 |         36.94 | 0.0753 | Tier 1 - Low Variance    |             1 | Stable      |
| Qwen3-235B                |          682.67 |         22.1  | 0.0324 | Tier 1 - Low Variance    |             1 | Stable      |
| GPT-OSS-20B               |          483.44 |         13.62 | 0.0282 | Tier 1 - Low Variance    |             1 | Stable      |

## Key Findings:

1. **Most Stable:** GPT-OSS-20B (CV: 0.0282) and Qwen3-235B (CV: 0.0324)
2. **Requires Monitoring:** Llama-4-Scout-17B (CV: 0.1245, Tier 2)
3. **High Variance Alert:** DeepSeek-R1-Distill-32B (CV: 0.1651, Tier 3)

## Implications for Firmus Infrastructure:

- Tier 3 models require enhanced power management and monitoring
- Power provisioning must account for ±15% variance in Tier 3 models
- Tier 1 models are ideal for production workloads with predictable power budgets

## Generated Artifacts:
- `power_variance_tiering_analysis.png`
- Analysis code in notebook cells

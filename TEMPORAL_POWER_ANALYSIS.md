# Temporal Power Analysis Report
**Generated:** 2025-12-16 11:11:06
**Framework:** Firmus H200 Model Evaluation - Temporal Power Characteristics
**Author:** Daniel Kearney, CTO Firmus

---

## Executive Summary

This analysis provides critical temporal power consumption data for H200 infrastructure planning,
including power ramp rates, prefill peaks, steady-state behavior, and fall-off characteristics.

### Key Findings:

1. **Prefill Power Spikes:** Models draw 15-67% more power during prompt processing
2. **Fast Ramp Rates:** Up to 769 W/s (Qwen3-235B) - requires robust PSU design  
3. **Time to Stable:** All models reach steady-state within 2 seconds
4. **CV Correlation:** Steady-state CV matches power variance tiering (CV > 0.1 threshold)

---

## Temporal Power Metrics

| Model                     |   Ramp Rate (W/s) |   Fall Rate (W/s) |   Prefill Peak (W) |   Steady Avg (W) |   Steady StdDev (W) |   Steady CV |   Time to Stable (s) |
|:--------------------------|------------------:|------------------:|-------------------:|-----------------:|--------------------:|------------:|---------------------:|
| Qwen3-235B                |             768.9 |            -312.6 |              827.9 |            680.7 |                21.4 |      0.0315 |                    2 |
| DeepSeek-R1-Distill (32B) |             576.9 |            -232.6 |              868.7 |            519.3 |                86.8 |      0.1672 |                    2 |
| Qwen3-32B                 |             546.9 |            -220.1 |              647.2 |            492.9 |                36.4 |      0.0739 |                    2 |
| GPT-OSS-20B               |             534.9 |            -215.1 |              581.5 |            485.1 |                14.2 |      0.0293 |                    2 |
| Llama-4-Maverick (17B)    |             486.9 |            -195.1 |              594.4 |            445.3 |                37.3 |      0.0838 |                    2 |
| Llama-4-Scout (17B)       |             456.9 |            -182.6 |              597   |            424.6 |                52.1 |      0.1227 |                    2 |

---

## Critical Infrastructure Implications

### 1. PSU Sizing Requirements

**CRITICAL:** Size power supplies for **prefill peak power**, not average consumption.

- **Qwen3-235B:** 827.9W peak (27% above steady-state)
- **DeepSeek-R1-Distill-32B:** 868.7W peak (67% above steady-state) ⚠️
- **Standard margin:** Add 15-20% headroom for all models
- **High-variance models:** Add 25-30% headroom (Tier 2/3 from CV analysis)

### 2. Power Ramp Rate Analysis

**Models by Ramp Aggression:**

| Category | Ramp Rate | Models | Impact |
|----------|-----------|--------|--------|
| **Aggressive** | >700 W/s | Qwen3-235B (769 W/s) | High PSU inrush stress |
| **Moderate** | 500-700 W/s | DeepSeek, Qwen3-32B | Standard PSU sufficient |
| **Gradual** | <500 W/s | GPT-OSS, Llama models | Minimal PSU stress |

**Recommendation:** Models with ramp rates >400 W/s require:
- Enterprise-grade PSUs with high inrush current tolerance
- Enhanced power delivery monitoring
- Thermal pre-conditioning for rapid heat dissipation

### 3. Thermal Management Considerations

**Phase-Based Cooling Strategy:**

1. **Ramp-up Phase (0-1s):**
   - Cooling systems must respond to 400-769 W/s power increase
   - Liquid cooling advantage: faster thermal response

2. **Prefill Peak (1-2s):**
   - Highest thermal load (15-67% above nominal)
   - Critical for immersion cooling reservoir sizing

3. **Steady Decode (2-8s):**
   - Stable thermal profile
   - Models with CV>0.1 show ±10-15% power variance

4. **Fall-off (8-10s):**
   - Gradual power decrease (-182 to -312 W/s)
   - Cooling system inertia beneficial here

### 4. Model Tiering Integration

**Correlation with CV>0.1 Tiering:**

- **Tier 1 Models (CV≤0.1):** Stable ramp, predictable prefill, low decode variance
  - GPT-OSS-20B: CV=0.0293, Ramp=535 W/s
  - Qwen3-235B: CV=0.0315, Ramp=769 W/s ⚠️ (high ramp despite low CV)

- **Tier 2 Models (0.1<CV≤0.15):** Moderate variance, standard PSU sizing
  - Llama-4-Scout: CV=0.1227, Ramp=457 W/s

- **Tier 3 Models (CV>0.15):** High variance, enhanced monitoring required
  - DeepSeek-R1-Distill: CV=0.1672, Ramp=577 W/s

---

## Infrastructure Recommendations

### Immediate Actions:

1. ✅ **PSU Specification Update**
   - Minimum rating: 1.25× prefill peak power
   - Target: 1.3× for Tier 2/3 models
   - Qwen3-235B requires: 827.9W × 1.25 = **1,035W minimum**

2. ✅ **Power Monitoring Enhancement**
   - Sample rate: ≥10Hz (100ms intervals) to capture ramp transients
   - Alert thresholds: Prefill peak + 10%
   - CV tracking during decode phase

3. ✅ **Cooling System Validation**
   - Test thermal response to 769 W/s ramp rate
   - Validate immersion cooling for 868W peak (DeepSeek)
   - Verify steady-state capacity for 6-second decode phase

4. ✅ **Workload Scheduling Optimization**
   - Stagger model initialization to avoid cumulative PSU stress
   - Group Tier 1 models (low CV) on shared infrastructure
   - Isolate Tier 3 models (high CV + high ramp) for monitoring

### Design Guidelines:

**For New H200 Deployments:**

```
PSU Sizing Formula:
Required PSU = Prefill_Peak_Power × Safety_Factor × Derating_Factor

Where:
- Safety_Factor = 1.25 (Tier 1), 1.30 (Tier 2/3)
- Derating_Factor = 0.9 (account for PSU efficiency curve)

Example (Qwen3-235B):
PSU = 827.9W × 1.25 × (1/0.9) = 1,149W rated capacity
```

**Power Delivery Architecture:**

- Dedicated 12V rails for GPU power (minimize voltage drop during ramp)
- Current sensing on each rail (detect anomalies within 100ms)
- Redundant PSU configuration for Tier 3 models

---

## Generated Artifacts

1. `temporal_power_traces_individual.png` - Individual model power profiles
2. `temporal_power_comparison_all_models.png` - All models comparison + dP/dt analysis  
3. `TEMPORAL_POWER_ANALYSIS.md` - This comprehensive report
4. Jupyter notebook with all analysis code

---

## References

- Power variance CV analysis (linked to tiering model)
- H200 benchmark comparison (Firmus vs Open-Source)
- Energy efficiency analysis
- NVML power monitoring framework

---

## Contact

Daniel Kearney  
CTO, Firmus AI Infrastructure  
Singapore

*For questions regarding this analysis or infrastructure planning, reference document: TEMPORAL_POWER_ANALYSIS.md*

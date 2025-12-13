# Model Card Template - Energy Efficiency Declaration

## Model-to-Grid Discount Qualification

Use this template to declare your model's energy efficiency characteristics for Firmus AI Cloud's Model-to-Grid pricing program. Models with stable power profiles qualify for discounted token pricing while helping us maintain predictable infrastructure operations.

---

## Basic Model Information

**Model Name:** `[e.g., my-custom-llama-70b]`  
**Model Version:** `[e.g., v1.2.0]`  
**Architecture:** `[e.g., Llama-3, Mistral, Qwen]`  
**Parameter Count:** `[e.g., 70B, 8B]`  
**Framework:** `[e.g., PyTorch, JAX]`  
**Quantization:** `[e.g., FP16, INT8, none]`

---

## Energy Efficiency Declaration

### Expected Performance Metrics

**Average Power Consumption:** `[Watts]`  
*Measured on H200 GPU under typical inference load*

**Peak Power Consumption:** `[Watts]`  
*Maximum power draw observed during testing*

**Power Coefficient of Variation (CV):** `[0.000-1.000]`  
*CV = Standard Deviation / Mean Power*  
*Lower CV indicates more stable power profile*

**Joules per Token:** `[J/token]`  
*Average energy per generated token*

**Tokens per Joule:** `[tokens/J]`  
*Efficiency metric - higher is better*

---

## Model-to-Grid Tier Qualification

**Target Tier:** `[Tier 1 / Tier 2 / Tier 3]`

### Tier Qualification Criteria

| Tier | Discount | CV Threshold | Avg Power Threshold | Qualification |
|------|----------|--------------|---------------------|---------------|
| **Tier 1** | 20% | CV < 0.10 | < 150W | ☐ Qualified |
| **Tier 2** | 10% | CV < 0.15 | < 200W | ☐ Qualified |
| **Tier 3** | 0% | CV > 0.15 or > 200W | Standard Pricing | ☐ |

**Self-Declared Qualification:** `[Yes/No]`  
**Firmus Verification Status:** `[Pending/Verified/Failed]`

---

## Testing Methodology

### Test Environment

**Hardware:** `[e.g., H200 80GB HBM3]`  
**Driver Version:** `[e.g., 550.54.15]`  
**CUDA Version:** `[e.g., 12.4]`  
**Test Duration:** `[minutes]`  
**Number of Samples:** `[inference runs]`  
**Batch Size:** `[e.g., 1, 4, 8]`  
**Sequence Length:** `[tokens]`

### Measurement Tools

- [ ] Firmus `energy_monitor.py` (recommended)
- [ ] nvidia-smi
- [ ] DCGM
- [ ] Custom tooling: `[describe]`

### Test Workload

**Prompt Type:** `[e.g., conversational, code generation, translation]`  
**Average Input Tokens:** `[count]`  
**Average Output Tokens:** `[count]`  
**Temperature:** `[value]`  
**Top-p:** `[value]`

---

## Power Stability Analysis

### Power Profile Characteristics

**Power Variance:** `[Watts²]`  
**Standard Deviation:** `[Watts]`  
**Coefficient of Variation:** `[CV value]`  
**Power Range:** `[Min-Max Watts]`

### Known Power Variations

- **Prefill vs Decode:** `[Describe power difference between phases]`
- **Sequence Length Impact:** `[How power changes with longer sequences]`
- **Batch Size Impact:** `[Power scaling with batch size]`
- **Attention Patterns:** `[Power spikes during attention computation]`

### Power Stability Optimizations

*List any optimizations applied to improve power stability:*

- [ ] Kernel fusion
- [ ] Balanced tensor parallelism
- [ ] KV-cache optimization
- [ ] Quantization-aware training
- [ ] Custom attention implementation
- [ ] Other: `[describe]`

---

## Reproducibility

### Verification Command

```bash
# Command to reproduce energy measurements
python -m src.energy_monitor --model [model_name] --samples 20 --tokens 10
```

### Expected Output

```json
{
  "tier": "tier_1_efficient",
  "discount_percentage": 20.0,
  "power_cv": 0.085,
  "avg_power_watts": 142.3,
  "peak_power_watts": 165.8,
  "qualified": true
}
```

---

## Developer Attestation

**Developer Name/Organization:** `[Your name/org]`  
**Contact Email:** `[email@domain.com]`  
**Date Tested:** `[YYYY-MM-DD]`  
**Firmus Account ID:** `[Optional: Your Firmus account]`

### Declaration

I certify that:

- [ ] All measurements were conducted on Firmus AI Cloud H200 infrastructure or equivalent
- [ ] Test methodology follows Firmus energy measurement best practices
- [ ] Reported metrics represent typical inference workload performance
- [ ] No artificial workload manipulation was used to game qualification metrics
- [ ] I understand Firmus will verify these claims through micro-benchmark profiling

**Signature:** `[Your name]`  
**Date:** `[YYYY-MM-DD]`

---

## Firmus Verification Results

*This section will be completed by Firmus AI Cloud after verification*

**Verification Date:** `[YYYY-MM-DD]`  
**Verified By:** `[Firmus Engineer]`  
**Verification Method:** `qualify_for_discount()` micro-benchmark  
**Samples Tested:** `[count]`

### Verified Metrics

| Metric | Developer Claim | Firmus Measured | Delta | Status |
|--------|----------------|-----------------|-------|--------|
| Avg Power (W) | `[value]` | `[value]` | `[%]` | ✓/✗ |
| CV | `[value]` | `[value]` | `[%]` | ✓/✗ |
| J/token | `[value]` | `[value]` | `[%]` | ✓/✗ |

**Final Qualification:** `[Tier 1 / Tier 2 / Tier 3]`  
**Discount Approved:** `[Yes/No]`  
**Reasoning:** `[Explanation]`

---

## Additional Notes

### Model Behavior Notes

*Any additional context about model power consumption patterns:*

```
[Describe any known behaviors, edge cases, or recommendations]
```

### Sustainability Impact

**Estimated CO₂ Savings:** `[kg CO₂ per 1M tokens vs baseline]`  
**Energy Efficiency Percentile:** `[vs other models in class]`

---

## Submission

To submit this model card for Model-to-Grid qualification:

1. Complete all sections above
2. Commit to your model repository
3. Submit qualification request via Firmus dashboard
4. Wait for verification (typically 24-48 hours)
5. Receive discount tier assignment

**Questions?** Contact energy-efficiency@firmus.ai

---

*Template Version: 1.0*  
*Last Updated: 2025-12-13*  
*Firmus AI Cloud Model-to-Grid Program*

# Model Evaluation Notebooks

Complete evaluation framework for LLM assessment on Firmus AI Cloud H200 infrastructure.

## Notebooks Overview

1. **01_setup_environment.ipynb** - Environment configuration and GPU verification
2. **02_performance_benchmarking.ipynb** - Inference performance metrics
3. **03_quality_evaluation.ipynb** - Standard benchmark evaluations (MMLU, GSM8K, HumanEval)
4. **04_infrastructure_metrics.ipynb** - H200-specific metrics (power, thermal, bandwidth)
5. **05_cost_analysis.ipynb** - TCO and cost-per-token analysis

## Quick Start

```bash
# Install all dependencies
pip install -r ../requirements.txt

# Run notebooks in sequence
jupyter lab
```

## Creating Notebooks

Since Jupyter notebooks are complex JSON files, you can create them in JupyterLab:

### Method 1: Copy from Repository
Full notebook JSON files will be added to this directory.

### Method 2: Auto-generate
Run the notebook generator script:
```bash
python ../scripts/generate_notebooks.py
```

### Method 3: Manual Creation
Create new notebooks in JupyterLab and copy the code cells below.

---

## Notebook Code Reference

### 01: Setup Environment

**Cell 1 - Markdown:**
```markdown
# 01: Environment Setup for Model Evaluation

**Purpose**: Install and configure all required libraries for H200 GPU model evaluation

**Hardware**: 1× Nvidia H200 (141GB HBM3e), 14 vCPU, 122GB RAM
```

**Cell 2 - Verify GPU:**
```python
# Verify GPU availability
!nvidia-smi

import torch
print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"CUDA version: {torch.version.cuda}")
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
```

**Cell 3 - Install Requirements:**
```python
!pip install -q -r ../requirements.txt
```

**Cell 4 - Verify Libraries:**
```python
import transformers
import accelerate
import bitsandbytes
import nvitop

print(f"✅ Transformers: {transformers.__version__}")
print(f"✅ Accelerate: {accelerate.__version__}")
print(f"✅ BitsAndBytes: {bitsandbytes.__version__}")
```

**Cell 5 - Configure W&B (Optional):**
```python
import wandb
# wandb.login()  # Uncomment to track experiments
# wandb.init(project='firmus-model-eval', name='h200-setup')
```

---

### 02: Performance Benchmarking

**Cell 1 - Imports:**
```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import time
import numpy as np
from rich import print as rprint

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")
```

**Cell 2 - Load Model:**
```python
MODEL_NAME = "meta-llama/Llama-3.2-1B-Instruct"
# MODEL_NAME = "meta-llama/Llama-3.1-70B-Instruct"  # For H200

print(f"Loading model: {MODEL_NAME}")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16,
    device_map="auto"
)

print(f"✅ Model loaded")
if torch.cuda.is_available():
    print(f"GPU Memory: {torch.cuda.memory_allocated()/1e9:.2f} GB")
```

**Cell 3 - Benchmark Function:**
```python
def benchmark_inference(model, tokenizer, prompt, max_new_tokens=100, num_runs=5):
    latencies = []
    tokens_generated = []
    
    for i in range(num_runs):
        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        start_time = time.time()
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=False,
                pad_token_id=tokenizer.eos_token_id
            )
        
        end_time = time.time()
        latencies.append(end_time - start_time)
        tokens_generated.append(outputs.shape[1] - inputs.input_ids.shape[1])
    
    avg_latency = np.mean(latencies)
    avg_tokens = np.mean(tokens_generated)
    tokens_per_sec = avg_tokens / avg_latency
    
    return {
        "avg_latency_sec": avg_latency,
        "tokens_per_second": tokens_per_sec,
        "ms_per_token": (avg_latency / avg_tokens) * 1000
    }

test_prompt = "Explain the Nvidia H200 GPU architecture:"
results = benchmark_inference(model, tokenizer, test_prompt, max_new_tokens=200)

rprint(f"Tokens/sec: {results['tokens_per_second']:.2f}")
rprint(f"ms/token: {results['ms_per_token']:.2f}")
```

---

### 03: Quality Evaluation

**Cell 1 - Setup lm-eval:**
```python
from lm_eval import evaluator
from lm_eval.models.huggingface import HFLM
import torch

MODEL_NAME = "meta-llama/Llama-3.2-1B-Instruct"

model = HFLM(
    pretrained=MODEL_NAME,
    device="cuda",
    dtype=torch.float16
)
```

**Cell 2 - Run MMLU:**
```python
results_mmlu = evaluator.simple_evaluate(
    model=model,
    tasks=["mmlu"],
    num_fewshot=5,
    batch_size="auto"
)

print(f"MMLU Score: {results_mmlu['results']['mmlu']['acc']:.2%}")
```

**Cell 3 - Run GSM8K:**
```python
results_gsm8k = evaluator.simple_evaluate(
    model=model,
    tasks=["gsm8k"],
    num_fewshot=5
)

print(f"GSM8K Score: {results_gsm8k['results']['gsm8k']['acc']:.2%}")
```

---

### 04: Infrastructure Metrics

**Cell 1 - GPU Monitoring:**
```python
import nvitop
import time
import pynvml

pynvml.nvmlInit()
handle = pynvml.nvmlDeviceGetHandleByIndex(0)

for i in range(10):
    power = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000  # Watts
    temp = pynvml.nvmlDeviceGetTemperature(handle, 0)
    util = pynvml.nvmlDeviceGetUtilizationRates(handle)
    
    print(f"Power: {power:.1f}W | Temp: {temp}°C | GPU: {util.gpu}% | Mem: {util.memory}%")
    time.sleep(1)
```

**Cell 2 - Memory Bandwidth:**
```python
mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
print(f"Total Memory: {mem_info.total / 1e9:.2f} GB")
print(f"Used Memory: {mem_info.used / 1e9:.2f} GB")
print(f"Free Memory: {mem_info.free / 1e9:.2f} GB")
```

---

### 05: Cost Analysis

**Cell 1 - TCO Calculation:**
```python
H200_HOURLY_COST = 5.00  # Update with Firmus pricing

results_summary = {
    "tokens_per_second": 150,  # From benchmark
    "hours_deployed": 24,
    "total_tokens": 150 * 3600 * 24
}

total_cost = H200_HOURLY_COST * results_summary["hours_deployed"]
cost_per_1m_tokens = (total_cost / results_summary["total_tokens"]) * 1_000_000

print(f"Total Cost: ${total_cost:.2f}")
print(f"Cost per 1M tokens: ${cost_per_1m_tokens:.4f}")
```

---

## Next Steps

1. Create these notebooks in JupyterLab by copying the code above
2. Run them sequentially once Firmus H200 notebooks are operational
3. Track results in W&B or local CSV files
4. Iterate on larger models (70B, 405B) using H200's 141GB HBM3e

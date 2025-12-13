# Energy Efficiency Tracking

Comprehensive energy monitoring and efficiency analysis framework for Firmus AI Cloud H200 infrastructure.

## Overview

This framework provides real-time GPU power monitoring and energy-per-token calculations for LLM model evaluation, enabling "apples-to-apples" efficiency comparisons across different 2025 open-source models.

## Key Features

### Real-Time Monitoring

- **GPU Power Tracking**: Continuous monitoring via NVIDIA Management Library (NVML)
- **Energy Accumulation**: Precise joule calculations across inference sessions
- **Temperature Monitoring**: Thermal metrics for H200 GPUs
- **Memory Tracking**: GPU memory utilization during inference

### Energy-per-Token Normalization

- **J/token Metric**: Normalized energy consumption per output token
- **Fair Comparisons**: Compare efficiency across different model sizes and architectures
- **Statistical Analysis**: Mean, median, and percentile calculations
- **Batch Processing**: Support for varied batch sizes

### H200-Optimized Tracking

- **700W TDP Monitoring**: Specialized tracking for H200 power envelope
- **HBM3 Memory**: Energy metrics including memory operations
- **SXM5 Architecture**: Hardware-specific optimizations

## Architecture

### Core Modules

#### 1. Energy Monitor (`src/energy_monitor.py`)

```python
monitor = EnergyMonitor(gpu_id=0)
monitor.start()
# ... inference code ...
metrics = monitor.stop()
# Returns: {energy_joules, duration_seconds, avg_power_watts}
```

#### 2. Energy-Efficient Inference (`src/energy_efficient_inference.py`)

```python
inferencer = EnergyEfficientInference(model, tokenizer)
result = inferencer.generate_with_energy_tracking(prompt, max_tokens=100)
# Returns: {output, energy_joules, tokens_generated, joules_per_token}
```

## Usage

### Basic Energy Tracking

```python
from src.energy_monitor import EnergyMonitor

monitor = EnergyMonitor(gpu_id=0, sampling_interval=0.1)
monitor.start()

# Your inference code
output = model.generate(input_ids, max_length=100)

metrics = monitor.stop()
print(f"Energy consumed: {metrics['energy_joules']:.2f} J")
print(f"Average power: {metrics['avg_power_watts']:.2f} W")
```

### Energy-per-Token Analysis

```python
from src.energy_efficient_inference import EnergyEfficientInference

inferencer = EnergyEfficientInference(model, tokenizer, gpu_id=0)
result = inferencer.generate_with_energy_tracking(
    prompt="Explain quantum computing",
    max_tokens=200
)

print(f"Tokens generated: {result['tokens_generated']}")
print(f"Energy: {result['energy_joules']:.4f} J")
print(f"Efficiency: {result['joules_per_token']:.6f} J/token")
```

### Benchmark Notebook

Run the complete benchmark:

```bash
jupyter lab notebooks/06_energy_efficiency_benchmark.ipynb
```

## Metrics Explained

### Primary Metrics

**Energy (Joules)**

- Total energy consumed during inference
- Calculated: Power (W) × Time (s)
- Includes GPU core + memory operations

**Joules per Token (J/token)**

- Energy efficiency metric
- Calculated: Total Energy (J) / Output Tokens
- **Key metric for model comparison**

**Average Power (Watts)**

- Mean power draw during inference
- H200 SXM TDP: Up to 700W maximum
- Idle baseline: ~50W
- Typical LLM inference load: 90-700W depending on workload intensity

### Secondary Metrics

- **Peak Power**: Maximum instantaneous power
- **GPU Temperature**: Thermal monitoring
- **Memory Utilization**: HBM3 usage
- **Inference Latency**: Time per token

## Requirements

### Hardware

- NVIDIA H200 GPU (or compatible GPU with NVML support)
- Linux environment with CUDA drivers

### Software

```bash
pip install -r requirements.txt
# Key dependency: pynvml>=11.5.0
```

## Benchmark Results

Energy efficiency rankings will be available after running the benchmark notebook:

- Model-by-model J/token comparisons
- Power consumption profiles
- Thermal analysis
- Memory efficiency correlations

## Best Practices

### For Accurate Measurements

1. **Warm-up runs**: Execute 2-3 inference passes before measuring
2. **Consistent load**: Use same prompt lengths for fair comparison
3. **Isolated testing**: Minimize background GPU processes
4. **Multiple samples**: Run each model 5+ times for statistical significance

### Interpreting Results

- Lower J/token = more energy efficient
- Consider token quality vs efficiency tradeoff
- Normalize for batch sizes when comparing
- Account for model size in efficiency analysis

## Energy Models Comparison

Expected efficiency characteristics:

**Highly Efficient (< 0.1 J/token)**

- Smaller parameter models (< 20B)
- Optimized architectures
- Quantized models

**Moderate Efficiency (0.1-0.3 J/token)**

- Mid-size models (20-70B)
- Standard precision

**Resource-Intensive (> 0.3 J/token)**

- Large models (> 100B)
- High-quality output focus
- Dense architectures

## Monitoring Dashboard

Real-time monitoring capabilities:

```python
monitor.get_current_power()  # Instantaneous power
monitor.get_temperature()    # Current GPU temp
monitor.get_memory_info()    # Memory utilization
```

## H200-Specific Considerations

### Power Characteristics

- **TDP**: 700W maximum (SXM variant)
- **Idle**: ~50W baseline
- **Typical Load**: 90-700W for LLM inference (varies by workload)

### Memory Impact

- HBM3 memory operations contribute to total energy
- Larger models = higher memory bandwidth usage
- Consider memory efficiency in overall analysis

## Troubleshooting

### Common Issues

**"NVML not initialized"**

```bash
# Ensure NVIDIA drivers installed
nvidia-smi
pip install pynvml
```

**High variance in measurements**

- Increase sampling frequency
- Extend warm-up period
- Check for background processes

**Memory errors**

- Reduce batch size
- Enable gradient checkpointing
- Monitor with `nvidia-smi dmon`

## Contributing

When adding new energy metrics:

1. Extend `EnergyMonitor` class
2. Update benchmark notebook
3. Document new metrics in this README
4. Include validation tests

## References

- [NVIDIA Management Library (NVML) Documentation](https://developer.nvidia.com/nvidia-management-library-nvml)
- [H200 Tensor Core GPU Specifications](https://www.nvidia.com/en-us/data-center/h200/)
- [Energy-Efficient AI Best Practices](https://www.firmus.co/docs/energy-efficiency)

## License

Part of the Firmus AI Cloud Model Evaluation Framework.

**Next Steps**: Run `notebooks/06_energy_efficiency_benchmark.ipynb` to generate comprehensive energy analysis for all configured 2025 models.

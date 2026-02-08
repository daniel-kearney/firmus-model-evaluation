# Firmus Model Evaluation Framework - Improvement Proposal

**Author:** Dr. Daniel Kearney  
**Date:** February 2026  
**Purpose:** Enhance model evaluation framework to support infrastructure digital twin integration

---

## Executive Summary

This proposal outlines enhancements to the Firmus Model Evaluation framework to enable bidirectional integration with the Firmus AI Factory digital twin. The improvements focus on exporting workload profiles for infrastructure simulation while maintaining the existing energy benchmarking capabilities.

**Key additions:**
1. Workload profile export for infrastructure simulation
2. Enhanced temporal resolution for ramp/fall capture
3. Multi-GPU coordination metrics
4. Economic modeling integration
5. Grid interaction characterization

---

## 1. Workload Profile Export Module

### Objective
Enable infrastructure teams to use real model benchmarks as input to cooling, electrical, and economic simulations.

### Implementation

**New file:** `src/workload_exporter.py`

```python
@dataclass
class WorkloadProfile:
    """
    Exportable workload profile for infrastructure simulation.
    Based on real H200 benchmark data from energy_monitor.py
    """
    model_name: str
    model_size_params: int
    duration_seconds: float
    power_trace: List[Tuple[float, float]]  # (timestamp, power_watts)
    phases: Dict[str, PhaseCharacteristics]
    energy_metrics: EnergyMetrics
    thermal_profile: Optional[ThermalProfile] = None
    
    def export_json(self, filepath: str):
        """Export workload profile as JSON for external tools"""
        pass
    
    def export_csv(self, filepath: str):
        """Export power trace as CSV time-series"""
        pass
    
    def to_synthetic_generator(self) -> SyntheticWorkloadGenerator:
        """Convert to parametric model for stochastic simulation"""
        pass

@dataclass
class PhaseCharacteristics:
    """Temporal phase characteristics"""
    phase_name: str  # "idle", "ramp", "prefill", "decode", "fall"
    start_time: float
    end_time: float
    avg_power: float
    peak_power: float
    power_stdev: float
    power_cv: float
    energy_joules: float
    ramp_rate_ws: Optional[float] = None  # W/s for ramp/fall phases

class WorkloadExporter:
    """
    Export energy monitoring data as infrastructure-ready workload profiles
    """
    def __init__(self, energy_monitor: H200EnergyMonitor):
        self.monitor = energy_monitor
    
    def extract_phases(self) -> Dict[str, PhaseCharacteristics]:
        """
        Automatically detect and characterize temporal phases:
        - Idle: Power < 100W
        - Ramp: dP/dt > 100 W/s
        - Prefill: First power peak
        - Decode: Steady-state after prefill
        - Fall: dP/dt < -100 W/s
        """
        pass
    
    def create_profile(self, model_name: str, model_size: int) -> WorkloadProfile:
        """Generate complete workload profile from monitoring session"""
        pass
```

### Integration Points
- Call `WorkloadExporter` after each benchmark run
- Auto-export profiles to `workload_profiles/` directory
- Include in benchmark summary reports

---

## 2. Enhanced Temporal Resolution

### Current State
- Sampling interval: 25ms (40 Hz)
- Sufficient for energy integration
- **Insufficient for ramp rate capture** (577-769 W/s ramps)

### Proposed Enhancement

**Adaptive sampling:**
```python
class H200EnergyMonitor:
    def __init__(self, 
                 gpu_index: int = 0, 
                 sampling_interval: float = 0.025,
                 high_res_mode: bool = False):
        """
        Args:
            high_res_mode: Enable 10ms sampling for ramp capture
        """
        if high_res_mode:
            self.sampling_interval = 0.010  # 100 Hz
            print("High-resolution mode: 10ms sampling for ramp analysis")
```

**Derivative calculation:**
```python
def calculate_power_derivatives(self) -> List[float]:
    """
    Calculate dP/dt for ramp rate analysis.
    Returns: List of power derivatives in W/s
    """
    derivatives = []
    for i in range(len(self.power_samples) - 1):
        dt = self.timestamps[i+1] - self.timestamps[i]
        dP = self.power_samples[i+1] - self.power_samples[i]
        derivatives.append(dP / dt)
    return derivatives
```

### Use Cases
- PSU inrush current validation
- Cooling system transient response testing
- Grid frequency regulation capability assessment

---

## 3. Multi-GPU Coordination Metrics

### Objective
Model power supply headroom and cooling capacity under multi-tenant workloads.

### Implementation

**New file:** `src/multi_gpu_coordinator.py`

```python
class MultiGPUCoordinator:
    """
    Coordinate energy monitoring across multiple GPUs to model
    aggregate infrastructure load and inter-workload interference.
    """
    def __init__(self, gpu_indices: List[int]):
        self.monitors = [H200EnergyMonitor(i) for i in gpu_indices]
    
    def start_coordinated_monitoring(self):
        """Start all monitors with synchronized timestamps"""
        pass
    
    def get_aggregate_power(self) -> float:
        """Sum instantaneous power across all GPUs"""
        pass
    
    def calculate_diversity_factor(self) -> float:
        """
        Diversity factor = Peak_aggregate / Sum(Peak_individual)
        Used for PSU sizing with concurrent workloads
        """
        pass
    
    def detect_thermal_interference(self) -> Dict[int, float]:
        """
        Measure temperature rise correlation between adjacent GPUs
        Returns: {gpu_id: thermal_coupling_coefficient}
        """
        pass
```

### Integration
- Add `--multi-gpu` flag to benchmark scripts
- Export aggregate power traces for rack-level simulation
- Include diversity factor in infrastructure sizing reports

---

## 4. Economic Modeling Integration

### Objective
Calculate cost per token and Model-to-Grid discount impact on TCO.

### Implementation

**Extend `EnergyMetrics` dataclass:**
```python
@dataclass
class EnergyMetrics:
    # ... existing fields ...
    
    # Economic metrics
    energy_cost_usd: Optional[float] = None  # Based on kWh rate
    cost_per_million_tokens: Optional[float] = None
    model_to_grid_discount_pct: Optional[float] = None
    discounted_cost_per_million_tokens: Optional[float] = None
```

**New method in `H200EnergyMonitor`:**
```python
def calculate_economics(self, 
                       tokens_generated: int,
                       kwh_rate_usd: float = 0.12,  # Singapore avg
                       apply_discount: bool = True) -> EnergyMetrics:
    """
    Calculate economic metrics including Model-to-Grid discounts.
    
    Args:
        tokens_generated: Total tokens generated
        kwh_rate_usd: Electricity rate in USD/kWh
        apply_discount: Apply Model-to-Grid tier discount
    
    Returns:
        EnergyMetrics with economic fields populated
    """
    metrics = self.calculate_metrics(tokens_generated)
    
    # Base energy cost
    kwh = metrics.total_energy_joules / 3_600_000
    energy_cost = kwh * kwh_rate_usd
    cost_per_million_tokens = (energy_cost / tokens_generated) * 1_000_000
    
    # Apply Model-to-Grid discount if qualified
    discount_pct = 0.0
    if apply_discount:
        qualification = self.qualify_for_discount()
        discount_pct = qualification.discount_percentage
    
    discounted_cost = cost_per_million_tokens * (1 - discount_pct / 100)
    
    metrics.energy_cost_usd = energy_cost
    metrics.cost_per_million_tokens = cost_per_million_tokens
    metrics.model_to_grid_discount_pct = discount_pct
    metrics.discounted_cost_per_million_tokens = discounted_cost
    
    return metrics
```

---

## 5. Grid Interaction Characterization

### Objective
Measure power quality metrics for grid integration and demand response.

### Implementation

**New file:** `src/grid_metrics.py`

```python
@dataclass
class GridMetrics:
    """Power quality and grid interaction metrics"""
    avg_power_kw: float
    peak_power_kw: float
    power_factor: float
    total_harmonic_distortion: float
    ramp_rate_kw_per_min: float
    demand_response_capability: str  # "high", "medium", "low"
    frequency_regulation_score: float  # 0-1 based on ramp flexibility

class GridCharacterizer:
    """
    Analyze workload suitability for grid services:
    - Demand response
    - Frequency regulation
    - Load following
    """
    def __init__(self, energy_monitor: H200EnergyMonitor):
        self.monitor = energy_monitor
    
    def assess_demand_response_capability(self) -> str:
        """
        Classify workload flexibility for demand response:
        - High: Can pause/resume with <5% performance impact
        - Medium: Can reduce power 20-50% during decode
        - Low: Requires continuous full power
        """
        pass
    
    def calculate_frequency_regulation_score(self) -> float:
        """
        Score 0-1 based on ability to modulate power quickly.
        High ramp rates + low thermal inertia = better regulation.
        """
        pass
```

---

## 6. Documentation Enhancements

### New Documents

**`WORKLOAD_EXPORT_GUIDE.md`**
- How to export workload profiles
- Integration with firmus-ai-factory
- Example use cases

**`MULTI_GPU_BENCHMARKING.md`**
- Coordinated monitoring setup
- Diversity factor calculation
- Thermal interference analysis

**`ECONOMIC_ANALYSIS.md`**
- Cost per token calculations
- Model-to-Grid discount impact
- TCO modeling for different tiers

### Updated Documents

**`README_ENERGY.md`**
- Add workload export section
- Link to infrastructure integration guide
- Include economic metrics examples

---

## 7. Example Workflows

### Workflow 1: Export Workload for Cooling Simulation

```python
from src.energy_monitor import H200EnergyMonitor
from src.workload_exporter import WorkloadExporter

# Run benchmark
monitor = H200EnergyMonitor(gpu_index=0, high_res_mode=True)
monitor.start_monitoring()

# ... run inference ...

metrics = monitor.calculate_metrics(tokens_generated=10000)

# Export for infrastructure simulation
exporter = WorkloadExporter(monitor)
profile = exporter.create_profile(
    model_name="DeepSeek-R1-Distill-Qwen-32B",
    model_size=32_000_000_000
)

# Save for firmus-ai-factory
profile.export_json("workload_profiles/deepseek_32b_10h.json")
profile.export_csv("workload_profiles/deepseek_32b_power_trace.csv")
```

### Workflow 2: Multi-GPU Rack Simulation

```python
from src.multi_gpu_coordinator import MultiGPUCoordinator

# Monitor 8 GPUs in a rack
coordinator = MultiGPUCoordinator(gpu_indices=list(range(8)))
coordinator.start_coordinated_monitoring()

# ... run concurrent workloads ...

diversity_factor = coordinator.calculate_diversity_factor()
print(f"PSU sizing diversity factor: {diversity_factor:.2f}")
# Output: 0.85 (peak aggregate is 85% of sum of individual peaks)

aggregate_trace = coordinator.get_aggregate_power_trace()
# Export for electrical infrastructure simulation
```

### Workflow 3: Economic Analysis with Discounts

```python
monitor = H200EnergyMonitor(gpu_index=0)
monitor.start_monitoring()

# ... run inference ...

metrics = monitor.calculate_economics(
    tokens_generated=1_000_000,
    kwh_rate_usd=0.12,
    apply_discount=True
)

print(f"Base cost: ${metrics.cost_per_million_tokens:.2f}/M tokens")
print(f"Discount: {metrics.model_to_grid_discount_pct}%")
print(f"Final cost: ${metrics.discounted_cost_per_million_tokens:.2f}/M tokens")
```

---

## Implementation Priority

### Phase 1 (Immediate)
1. ✅ Workload profile export module
2. ✅ Enhanced temporal resolution (high-res mode)
3. ✅ Economic metrics integration

### Phase 2 (Q1 2026)
4. Multi-GPU coordination
5. Grid interaction characterization
6. Documentation updates

### Phase 3 (Q2 2026)
7. Automated CI/CD for profile export
8. Integration testing with firmus-ai-factory
9. Customer-facing workload library

---

## Success Metrics

1. **Workload profiles exported:** >50 model configurations
2. **Infrastructure simulation accuracy:** <5% error vs real measurements
3. **Economic model adoption:** Used in 100% of customer quotes
4. **Grid integration:** 3+ demand response pilot programs

---

## Conclusion

These improvements transform the model evaluation framework from a standalone benchmarking tool into a bidirectional integration with infrastructure digital twins. Real workload data flows into simulation, enabling accurate capacity planning, economic modeling, and grid integration analysis.

The proposed changes maintain backward compatibility while adding critical capabilities for infrastructure teams.

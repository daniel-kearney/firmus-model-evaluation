"""Energy Analysis Module - Separates metrics calculation from data collection.

Pure analysis functions that operate on collected power samples and timestamps.
"""

import statistics
from typing import List, Tuple, Optional
from dataclasses import dataclass
import json


@dataclass
class EnergyMetrics:
    """Comprehensive energy metrics."""
    total_energy_joules: float
    tokens_generated: int
    joules_per_token: float
    tokens_per_joule: float
    avg_power_watts: float
    peak_power_watts: float
    duration_seconds: float
    prefill_energy_joules: float
    prefill_duration_seconds: float
    decode_energy_joules: float
    decode_duration_seconds: float
    wh_per_1k_queries: float
    power_variance_cv: float
    model_name: Optional[str] = None
    run_id: Optional[str] = None
    
    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


def calculate_energy(power_samples: List[float], timestamps: List[float]) -> float:
    """Calculate total energy using trapezoidal integration."""
    if len(power_samples) < 2:
        return 0.0
    
    total_energy_j = 0.0
    for i in range(len(power_samples) - 1):
        dt = timestamps[i+1] - timestamps[i]
        avg_power = (power_samples[i] + power_samples[i+1]) / 2
        total_energy_j += avg_power * dt
    
    return total_energy_j


def calculate_metrics(
    power_samples: List[float],
    timestamps: List[float],
    tokens_generated: int,
    prefill_sample_count: int = 0,
    tokens_per_query: int = 100,
    model_name: Optional[str] = None,
    run_id: Optional[str] = None
) -> EnergyMetrics:
    """Calculate comprehensive energy metrics.
    
    Args:
        power_samples: List of power readings in watts
        timestamps: Corresponding timestamps
        tokens_generated: Total tokens generated
        prefill_sample_count: Number of samples in prefill phase
        tokens_per_query: Tokens per query for scalability metric
        model_name: Optional model identifier
        run_id: Optional run identifier for tracking
    """
    if len(power_samples) < 2:
        raise ValueError("Need at least 2 samples")
    
    total_energy_j = calculate_energy(power_samples, timestamps)
    duration = timestamps[-1] - timestamps[0]
    
    # Power statistics
    avg_power = statistics.mean(power_samples)
    peak_power = max(power_samples)
    power_stdev = statistics.stdev(power_samples) if len(power_samples) > 1 else 0.0
    power_cv = (power_stdev / avg_power) if avg_power > 1.0 else 0.0
    
    # Efficiency metrics
    joules_per_token = total_energy_j / tokens_generated if tokens_generated > 0 else 0.0
    tokens_per_joule = tokens_generated / total_energy_j if total_energy_j > 0 else 0.0
    wh_per_1k_queries = (joules_per_token * tokens_per_query * 1000) / 3600
    
    # Phase attribution
    prefill_energy = 0.0
    prefill_duration = 0.0
    if prefill_sample_count > 0 and prefill_sample_count < len(power_samples):
        prefill_samples = power_samples[:prefill_sample_count]
        prefill_times = timestamps[:prefill_sample_count]
        prefill_energy = calculate_energy(prefill_samples, prefill_times)
        prefill_duration = timestamps[prefill_sample_count-1] - timestamps[0]
    
    decode_energy = total_energy_j - prefill_energy
    decode_duration = duration - prefill_duration
    
    return EnergyMetrics(
        total_energy_joules=total_energy_j,
        tokens_generated=tokens_generated,
        joules_per_token=joules_per_token,
        tokens_per_joule=tokens_per_joule,
        avg_power_watts=avg_power,
        peak_power_watts=peak_power,
        duration_seconds=duration,
        prefill_energy_joules=prefill_energy,
        prefill_duration_seconds=prefill_duration,
        decode_energy_joules=decode_energy,
        decode_duration_seconds=decode_duration,
        wh_per_1k_queries=wh_per_1k_queries,
        power_variance_cv=power_cv,
        model_name=model_name,
        run_id=run_id
    )

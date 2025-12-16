#!/usr/bin/env python3
"""
Enhanced Temporal Power Visualization - Highly Distinguishable Colors
Generates temporal power analysis plots with colorblind-friendly palette
Author: Daniel Kearney, CTO Firmus
Date: 2025-12-16
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Set professional style
sns.set_style('whitegrid')
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['font.size'] = 10

# Temporal power data from TEMPORAL_POWER_ANALYSIS.md
models_data = {
    'Qwen3-235B': {
        'ramp_rate': 768.9, 'fall_rate': -312.6, 'prefill_peak': 827.9,
        'steady_avg': 680.7, 'steady_std': 21.4, 'cv': 0.0315
    },
    'DeepSeek-R1-Distill-32B': {
        'ramp_rate': 576.9, 'fall_rate': -232.6, 'prefill_peak': 868.7,
        'steady_avg': 519.3, 'steady_std': 86.8, 'cv': 0.1672
    },
    'Qwen3-32B': {
        'ramp_rate': 546.9, 'fall_rate': -220.1, 'prefill_peak': 647.2,
        'steady_avg': 492.9, 'steady_std': 36.4, 'cv': 0.0739
    },
    'GPT-OSS-20B': {
        'ramp_rate': 534.9, 'fall_rate': -215.1, 'prefill_peak': 581.5,
        'steady_avg': 485.1, 'steady_std': 14.2, 'cv': 0.0293
    },
    'Llama-4-Maverick-17B': {
        'ramp_rate': 486.9, 'fall_rate': -195.1, 'prefill_peak': 594.4,
        'steady_avg': 445.3, 'steady_std': 37.3, 'cv': 0.0838
    },
    'Llama-4-Scout-17B': {
        'ramp_rate': 456.9, 'fall_rate': -182.6, 'prefill_peak': 597.0,
        'steady_avg': 424.6, 'steady_std': 52.1, 'cv': 0.1227
    }
}

# COLORBLIND-FRIENDLY PALETTE
colors = {
    'Qwen3-235B': '#D55E00',
    'DeepSeek-R1-Distill-32B': '#0072B2',
    'Qwen3-32B': '#009E73',
    'GPT-OSS-20B': '#F0E442',
    'Llama-4-Maverick-17B': '#CC79A7',
    'Llama-4-Scout-17B': '#56B4E9'
}

def generate_power_trace(model_data, duration=10, sample_rate=100):
    time = np.linspace(0, duration, duration * sample_rate)
    power = np.zeros_like(time)
    ramp_mask = time < 1.0
    power[ramp_mask] = 200 + model_data['ramp_rate'] * time[ramp_mask]
    prefill_mask = (time >= 1.0) & (time < 2.0)
    power[prefill_mask] = model_data['prefill_peak']
    decode_mask = (time >= 2.0) & (time < 8.0)
    np.random.seed(42)
    variance = np.random.normal(0, model_data['steady_std'], len(time[decode_mask]))
    power[decode_mask] = model_data['steady_avg'] + variance
    fall_mask = time >= 8.0
    fall_time = time[fall_mask] - 8.0
    power[fall_mask] = np.maximum(model_data['steady_avg'] + model_data['fall_rate'] * fall_time, 200)
    return time, power

# Individual subplots
fig, axes = plt.subplots(3, 2, figsize=(16, 12))
axes = axes.flatten()

for idx, (model_name, model_data) in enumerate(models_data.items()):
    ax = axes[idx]
    time, power = generate_power_trace(model_data)
    ax.plot(time, power, color=colors[model_name], linewidth=3.5, alpha=0.9)
    ax.axvspan(0, 1, alpha=0.08, color='yellow')
    ax.axvspan(1, 2, alpha=0.08, color='red')
    ax.axvspan(2, 8, alpha=0.08, color='green')
    ax.axvspan(8, 10, alpha=0.08, color='blue')
    textstr = f'Peak: {model_data["prefill_peak"]:.0f}W\nAvg: {model_data["steady_avg"]:.0f}W\nCV: {model_data["cv"]:.4f}\nRamp: {model_data["ramp_rate"]:.0f} W/s'
    ax.text(0.02, 0.98, textstr, transform=ax.transAxes, verticalalignment='top', 
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor=colors[model_name], linewidth=2), 
            fontsize=9, fontweight='bold')
    ax.set_xlabel('Time (seconds)', fontweight='bold', fontsize=11)
    ax.set_ylabel('Power (W)', fontweight='bold', fontsize=11)
    ax.set_title(f'{model_name}', fontweight='bold', fontsize=13, color=colors[model_name], pad=10)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xlim(0, 10)
    ax.set_ylim(150, 900)
    ax.axhline(y=model_data['steady_avg'], color=colors[model_name], linestyle='--', linewidth=2, alpha=0.4)

plt.suptitle('Temporal Power Analysis - Individual Models (Enhanced Colors)', fontsize=16, fontweight='bold', y=0.995)
plt.tight_layout()
plt.savefig('temporal_power_traces_individual_ENHANCED.png', dpi=300, bbox_inches='tight')
print("✅ Saved: temporal_power_traces_individual_ENHANCED.png")

# Combined comparison
fig2, ax2 = plt.subplots(figsize=(15, 9))
for model_name, model_data in models_data.items():
    time, power = generate_power_trace(model_data)
    ax2.plot(time, power, color=colors[model_name], linewidth=3.5, label=model_name, alpha=0.9)

ax2.set_xlabel('Time (seconds)', fontweight='bold', fontsize=13)
ax2.set_ylabel('Power Consumption (W)', fontweight='bold', fontsize=13)
ax2.set_title('Temporal Power Comparison - All Models\n(Colorblind-Friendly Palette)', fontweight='bold', fontsize=15, pad=15)
ax2.grid(True, alpha=0.3, linestyle='--', linewidth=1)
ax2.legend(loc='upper right', fontsize=11, framealpha=0.95, edgecolor='black', fancybox=True, shadow=True)
ax2.set_xlim(0, 10)
ax2.set_ylim(150, 900)

phase_y = 870
for x, label, color in [(0.5, 'Ramp', 'yellow'), (1.5, 'Prefill', 'red'), (5, 'Steady Decode', 'green'), (9, 'Fall-off', 'blue')]:
    ax2.text(x, phase_y, label, fontsize=11, fontweight='bold', ha='center', bbox=dict(boxstyle='round', facecolor=color, alpha=0.3))

plt.tight_layout()
plt.savefig('temporal_power_comparison_all_models_ENHANCED.png', dpi=300, bbox_inches='tight')
print("✅ Saved: temporal_power_comparison_all_models_ENHANCED.png")
plt.show()

print("\n" + "="*70)
print("ENHANCED TEMPORAL POWER VISUALIZATION COMPLETE")
print("="*70)
print("\nColorblind-Friendly Palette:")
for model, color in colors.items():
    print(f"  • {model}: {color}")
print("\nOutput Files:")
print("  1. temporal_power_traces_individual_ENHANCED.png")
print("  2. temporal_power_comparison_all_models_ENHANCED.png")
print("="*70)

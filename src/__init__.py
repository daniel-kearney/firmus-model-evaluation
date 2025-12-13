"""Firmus Model Evaluation Framework

Utility modules for model evaluation on H200 infrastructure.
"""

__version__ = "0.1.0"
__author__ = "Firmus AI Team"

# Import key utilities for easier access
try:
    from .model_loader import ModelLoader
    from .metrics import PerformanceMetrics, QualityMetrics
    from .infrastructure import GPUMonitor, ResourceTracker
    from .cost_calculator import CostAnalyzer
except ImportError:
    # Modules not yet created, will be available after implementation
    pass

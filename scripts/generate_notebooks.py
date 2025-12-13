#!/usr/bin/env python3
"""Generate Jupyter notebook files from notebook templates.

This script creates .ipynb files in the notebooks/ directory
based on the code examples provided in notebooks/README.md.

Usage:
    python scripts/generate_notebooks.py
"""

import json
import os
from pathlib import Path


NOTEBOOK_TEMPLATES = {
    "01_setup_environment": {
        "title": "Environment Setup and GPU Verification",
        "description": "Configure environment and verify H200 GPU access"
    },
    "02_performance_benchmarking": {
        "title": "Performance Benchmarking",
        "description": "Test inference performance metrics"
    },
    "03_quality_evaluation": {
        "title": "Quality Evaluation",
        "description": "Run standard benchmark evaluations"
    },
    "04_infrastructure_metrics": {
        "title": "Infrastructure Metrics",
        "description": "Monitor H200-specific metrics"
    },
    "05_cost_analysis": {
        "title": "Cost Analysis",
        "description": "Calculate TCO and cost per token"
    }
}


def create_notebook(name: str, title: str, description: str) -> dict:
    """Create a basic Jupyter notebook structure."""
    return {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [f"# {title}\n", f"\n{description}"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": ["# Add your code here"]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.10.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }


def main():
    """Generate notebook files."""
    # Get notebooks directory
    notebooks_dir = Path(__file__).parent.parent / "notebooks"
    notebooks_dir.mkdir(exist_ok=True)
    
    print(f"Generating notebooks in: {notebooks_dir}")
    
    for name, info in NOTEBOOK_TEMPLATES.items():
        notebook_path = notebooks_dir / f"{name}.ipynb"
        
        if notebook_path.exists():
            print(f"  Skipping {name}.ipynb (already exists)")
            continue
        
        notebook = create_notebook(name, info["title"], info["description"])
        
        with open(notebook_path, 'w') as f:
            json.dump(notebook, f, indent=2)
        
        print(f"  Created {name}.ipynb")
    
    print("\nDone! See notebooks/README.md for code examples to add.")


if __name__ == "__main__":
    main()

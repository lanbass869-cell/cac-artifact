# Cross-Agent Memory Contradiction — Reproducibility Makefile
# Quick start: pip install -r requirements.txt && make all

PYTHON ?= python3

.PHONY: all quick help clean

all: conflictbank detector downstream counterfactual
	@echo "=== All experiments completed ==="

quick: conflictbank
	@echo "=== Quick verification (ConflictBank F1) done ==="

conflictbank:
	@echo "--- ConflictBank temporal conflict (n=2000, target F1=0.897) ---"
	$(PYTHON) evaluate_conflictbank.py

detector:
	@echo "--- Controlled benchmark 4-method comparison (target F1=0.813) ---"
	$(PYTHON) evaluate_detectors.py

downstream:
	@echo "--- Cross-entity downstream (73pp, n=11) ---"
	$(PYTHON) cross_entity_downstream.py

counterfactual:
	@echo "--- Counterfactual supersession analysis (52-61%) ---"
	$(PYTHON) counterfactual.py

help:
	@echo "Available targets:"
	@echo "  make all           - Run all experiments"
	@echo "  make quick         - Just ConflictBank F1 (fastest)"
	@echo "  make conflictbank  - ConflictBank n=2000"
	@echo "  make detector      - Controlled benchmark"
	@echo "  make downstream    - 73pp downstream"
	@echo "  make counterfactual- Supersession prevention"

clean:
	rm -rf __pycache__ .pytest_cache

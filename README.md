# Cross-Agent Memory Contradiction — Reproducibility Artifact

This artifact package reproduces the measurement, classification, and downstream experiments in "When Agents Disagree: Measuring and Resolving Cross-Agent Memory Contradictions in Shared Multi-Agent Memory".

## Contents

| File | Description |
|------|-------------|
| `scan_contradictions.py` | Phase 1: Scans all active facts grouped by entity, detects cross-source polarity clashes |
| `classify_contradictions.py` | Phase 2: Classifies clash pairs into 4 types (temporal flip / entity FP / self-agent / needs review) |
| `downstream_contradiction_test.py` | Phase 4: Tests downstream LLM answer quality with contradictory vs resolved memory contexts |
| `generate_synthetic_db.py` | Generates a synthetic SQLite database matching the production schema for standalone testing |
| `synthetic_memory.db` | Pre-generated synthetic database (102 active facts, 16 entities, 13 contradiction pairs) |
| `requirements.txt` | Python dependencies |
| `Makefile` | One-command reproduction |

## Quick Start

```bash
# Generate synthetic DB (or use the pre-generated one)
python generate_synthetic_db.py

# Run scan on synthetic DB
MEM_DB=./synthetic_memory.db python scan_contradictions.py

# Run classification
python classify_contradictions.py

# Run downstream experiment (requires LLM API at http://127.0.0.1:8813)
python downstream_contradiction_test.py
```

## Method

The scan pipeline:
1. Groups active facts by entity via the `fact_entities` table
2. Extracts (entity, polarity) pairs from clauses using a Chinese/English status-word lexicon
3. Detects cross-source pairs with opposite polarity on the same entity
4. Requires at least one identifier-like entity (containing underscore, digit, or ≥4 ASCII chars)

The classifier:
- Score ≥ 6 → temporal status flip (genuine contradiction)
- Score = 3 with generic/short entity → entity polarity false positive
- All other → needs human review

## Expected Output

On the synthetic database:
- Active facts: 102
- Entities: 16
- Cross-source pairs: 16
- Contradiction pairs: 13 (81.25% — synthetic data is designed with known conflicts)

On production data (not included):
- Active facts: 1,768
- Cross-source pairs: 24,907
- Contradiction pairs: 198 (0.79% candidates)
- Genuine temporal flips: 11 (0.044%)

## License

Apache-2.0

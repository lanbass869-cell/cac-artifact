# -*- coding: utf-8 -*-
"""evaluate_conflictbank.py — Evaluate entity-level polarity detection on ConflictBank temporal_conflict subset.
Task: Given (claim, evidence) pairs, detect if they conflict. Compare with ground truth label.
Methods: 1) Our entity-level polarity clash 2) Governance _polarity 3) Simple word overlap
"""
import json, os, sys, re
sys.path.insert(0, r'E:/RUANJIAN/memory_hub')
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from governance import _POS, _NEG, _polarity

# Load temporal_conflict + default (negative class) rows
rows = []
with open(r'E:\RUANJIAN\workdocs\memtether\cac-artifact\conflictbank_sample.jsonl', encoding='utf-8') as f:
    for line in f:
        rows.append(json.loads(line))

# Filter: temporal_conflict (positive) + default (negative) for binary classification
positive = [r for r in rows if r['category'] == 'temporal_conflict']
negative = [r for r in rows if r['category'] == 'default']
print(f'Temporal conflict (positive): {len(positive)}')
print(f'Default (negative): {len(negative)}')

# Take equal-sized sample
min_n = min(len(positive), len(negative), 500)
eval_set = positive[:min_n] + negative[:min_n]
random.shuffle(eval_set) if 'random' in dir() else None
import random
random.seed(42)
random.shuffle(eval_set)
print(f'Eval set: {len(eval_set)} ({min_n} positive + {min_n} negative)')

# Method 1: Simple polarity word detection
def method_polarity_words(claim, evidence):
    """Detect conflict if claim and evidence have opposite polarity on same subject."""
    p_claim = sum(1 for w in _POS if w in claim)
    n_claim = sum(1 for w in _NEG if w in claim)
    p_evid = sum(1 for w in _POS if w in evidence)
    n_evid = sum(1 for w in _NEG if w in evidence)
    # Conflict if one has positive and other has negative
    return (p_claim > 0 and n_evid > 0) or (n_claim > 0 and p_evid > 0)

# Method 2: Subject overlap + opposite dates/numbers
def method_temporal_overlap(claim, evidence):
    """Detect conflict if claim and evidence mention same subject but different dates/numbers."""
    # Extract years
    years_claim = set(re.findall(r'\b(19|20)\d{2}\b', claim))
    years_evid = set(re.findall(r'\b(19|20)\d{2}\b', evidence))
    # Extract numbers
    nums_claim = set(re.findall(r'\b\d+\b', claim))
    nums_evid = set(re.findall(r'\b\d+\b', evidence))
    # If same subject but different years/numbers = potential temporal conflict
    if years_claim and years_evid and years_claim != years_evid:
        return True
    if nums_claim and nums_evid:
        diff = nums_claim.symmetric_difference(nums_evid)
        if len(diff) > 0 and len(nums_claim & nums_evid) > 0:
            return True
    return False

# Method 3: Combined
def method_combined(claim, evidence):
    return method_polarity_words(claim, evidence) or method_temporal_overlap(claim, evidence)

# Method 4: Entity overlap + negation
def method_entity_negation(claim, evidence):
    """Check if same entity appears with opposite polarity."""
    # Extract capitalized words as entity proxies
    ents_claim = set(re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', claim))
    ents_evid = set(re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', evidence))
    shared_ents = ents_claim & ents_evid
    if not shared_ents:
        return False
    # Check polarity
    return has_opposite_polarity_en(claim, evidence)

def has_opposite_polarity_en(text_a, text_b):
    """English polarity detection."""
    pos_en = ['available', 'works', 'success', 'active', 'supported', 'enabled', 'correct', 'valid']
    neg_en = ['failed', 'banned', 'invalid', 'disabled', 'unavailable', 'deprecated', 'retired', 'error']
    pa = sum(1 for w in pos_en if w in text_a.lower())
    na = sum(1 for w in neg_en if w in text_a.lower())
    pb = sum(1 for w in pos_en if w in text_b.lower())
    nb = sum(1 for w in neg_en if w in text_b.lower())
    return (pa > 0 and nb > 0) or (na > 0 and pb > 0)

# Evaluate all methods
def evaluate(method_fn, name):
    tp = fp = tn = fn = 0
    for r in eval_set:
        is_conflict = r['category'] == 'temporal_conflict'
        detected = method_fn(r['claim'], r['evidence'])
        if is_conflict and detected: tp += 1
        elif not is_conflict and detected: fp += 1
        elif not is_conflict and not detected: tn += 1
        else: fn += 1
    p = tp / max(tp+fp, 1)
    r_ = tp / max(tp+fn, 1)
    f1 = 2*p*r_ / max(p+r_, 1e-8)
    acc = (tp+tn) / max(len(eval_set), 1)
    print(f'  {name:30s} P={p:.3f} R={r_:.3f} F1={f1:.3f} Acc={acc:.3f} (TP={tp} FP={fp} TN={tn} FN={fn})')
    return {'method': name, 'precision': round(p,3), 'recall': round(r_,3), 'f1': round(f1,3), 'accuracy': round(acc,3), 'tp':tp, 'fp':fp, 'tn':tn, 'fn':fn}

print(f'\n=== ConflictBank temporal_conflict detection ({len(eval_set)} samples) ===')
results = []
results.append(evaluate(method_polarity_words, 'Chinese polarity words'))
results.append(evaluate(method_temporal_overlap, 'Temporal/numeric overlap'))
results.append(evaluate(method_combined, 'Combined'))
results.append(evaluate(method_entity_negation, 'Entity + English polarity'))
results.append(evaluate(lambda c,e: has_opposite_polarity_en(c,e), 'English polarity only'))

# Save results
out = r'E:\RUANJIAN\workdocs\memtether\cac-artifact\conflictbank_evaluation.json'
json.dump({'total_samples': len(eval_set), 'positive': min_n, 'negative': min_n, 'results': results},
          open(out, 'w', encoding='utf-8'), indent=2)
print(f'\nSaved: {out}')

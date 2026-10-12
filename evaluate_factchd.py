# -*- coding: utf-8 -*-
"""evaluate_factchd.py — Evaluate temporal-numeric overlap on FactCHD"""
import json, sys, os, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

fp = r'E:\RUANJIAN\workdocs\memtether\cac-artifact\factchd\test_case_sample.jsonl'
data = [json.loads(line) for line in open(fp, encoding='utf-8')]
print(f'FactCHD test: {len(data)} records')
from collections import Counter
print(f'Labels: {dict(Counter(d["label"] for d in data))}')
print(f'Categories: {dict(Counter(d.get("category","?") for d in data))}')

def extract_numbers(text):
    return set(re.findall(r'\b\d+\b', text))

def temporal_overlap(response, evidence_texts):
    """Detect temporal/numeric conflict between response and evidence."""
    nums_resp = extract_numbers(response)
    all_evid_nums = set()
    for evid_item in evidence_texts:
        text = evid_item[-1] if isinstance(evid_item, (list, tuple)) and len(evid_item) >= 2 else str(evid_item)
        all_evid_nums |= extract_numbers(text)
    # Conflict if response has numbers that differ from evidence numbers
    if nums_resp and all_evid_nums:
        # Check if response mentions a number NOT in evidence
        wrong_nums = nums_resp - all_evid_nums
        # And shares some numbers with evidence (same entity/topic)
        shared = nums_resp & all_evid_nums
        if wrong_nums and shared:
            return True  # Partial match = likely wrong value
    return False

# Evaluate
tp=fp=tn=fn=0
for d in data:
    gt = d['label'] == 'NON-FACTUAL'
    pred = temporal_overlap(d['response'], d['evidence'])
    if gt and pred: tp+=1
    elif not gt and pred: fp+=1
    elif not gt and not pred: tn+=1
    else: fn+=1

p = tp/max(tp+fp,1)
r = tp/max(tp+fn,1)
f1 = 2*p*r/max(p+r,1e-8)
acc = (tp+tn)/len(data)
print(f'\n=== FactCHD (n={len(data)}) ===')
print(f'Temporal-numeric overlap: P={p:.3f} R={r:.3f} F1={f1:.3f} Acc={acc:.3f} (TP={tp} FP={fp} TN={tn} FN={fn})')

# Save results
out = r'E:\RUANJIAN\workdocs\memtether\cac-artifact\factchd\evaluation.json'
json.dump({'n': len(data), 'precision': round(p,3), 'recall': round(r,3), 'f1': round(f1,3),
           'accuracy': round(acc,3), 'tp':tp, 'fp':fp, 'tn':tn, 'fn':fn},
          open(out,'w',encoding='utf-8'), indent=2)
print(f'Saved: {out}')

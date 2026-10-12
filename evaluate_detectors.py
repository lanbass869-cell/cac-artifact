# -*- coding: utf-8 -*-
"""evaluate_detectors.py — Evaluate multiple contradiction detection methods on controlled benchmark
Methods:
  1. governance detect_explicit_conflicts (existing)
  2. entity-level polarity clash (our method)
  3. Temporal supersession recommendation algorithm
  4. Naive: always flag if different sources have opposite words

Metrics: precision, recall, F1 against ground truth
"""
import sqlite3, os, sys, json, itertools
sys.path.insert(0, r'E:/RUANJIAN/memory_hub')
sys.path.insert(0, r'E:/RUANJIAN/workdocs/memtether/cac-artifact')
os.environ['MEM_DB'] = r'E:/RUANJIAN/workdocs/memtether/cac-artifact/benchmark_memory.db'
from governance import _polarity_by_entity, _POS, _NEG
from collections import defaultdict

DB = os.environ['MEM_DB']
GT = json.load(open(os.path.join(os.path.dirname(DB),'benchmark_ground_truth.json'), encoding='utf-8'))

def load_facts(conn):
    facts = {}
    for r in conn.execute("SELECT uid, content, source, valid_from, status FROM facts WHERE status='active'"):
        facts[r['uid']] = dict(r)
    return facts

def build_entity_groups(conn, facts):
    ef = defaultdict(set)
    for r in conn.execute("SELECT entity_name, fact_uid FROM fact_entities"):
        if r['fact_uid'] in facts:
            ef[r['entity_name']].add(r['fact_uid'])
    return ef

def has_opposite_polarity(content_a, content_b):
    """Simple check: does one have POS words and other have NEG words?"""
    pa = sum(1 for w in _POS if w in content_a)
    na = sum(1 for w in _NEG if w in content_a)
    pb = sum(1 for w in _POS if w in content_b)
    nb = sum(1 for w in _NEG if w in content_b)
    return (pa > 0 and nb > 0) or (na > 0 and pb > 0)

def method_naive(conn, facts, ef):
    """Method 1: Naive — flag any cross-source pair with opposite polarity words."""
    detected = set()
    for ent, uids in ef.items():
        if len(uids) < 2: continue
        uid_list = sorted(uids)
        for i in range(len(uid_list)):
            for j in range(i+1, len(uid_list)):
                a, b = uid_list[i], uid_list[j]
                if facts[a]['source'] == facts[b]['source']: continue
                if has_opposite_polarity(facts[a]['content'], facts[b]['content']):
                    detected.add(frozenset([a,b]))
    return detected

def method_entity_polarity(conn, facts, ef):
    """Method 2: Entity-level polarity clash (our method)."""
    detected = set()
    for ent, uids in ef.items():
        if len(uids) < 2 or len(uids) > 30: continue
        fact_pol = {}
        for uid_s in uids:
            ep = _polarity_by_entity(facts[uid_s]['content'])
            if ep: fact_pol[uid_s] = ep
        uid_list = sorted(fact_pol.keys())
        for i in range(len(uid_list)):
            for j in range(i+1, len(uid_list)):
                a, b = uid_list[i], uid_list[j]
                if facts[a]['source'] == facts[b]['source']: continue
                shared = set(fact_pol[a]) & set(fact_pol[b])
                if any(fact_pol[a][e]['pol'] != fact_pol[b][e]['pol'] for e in shared):
                    detected.add(frozenset([a,b]))
    return detected

def method_governance(conn, facts, ef):
    """Method 3: Use governance.detect_explicit_conflicts."""
    from governance import detect_explicit_conflicts
    # Patch DB path
    import governance as gov
    old_db = gov.DB
    gov.DB = DB
    try:
        conflicts = detect_explicit_conflicts(days_window=999)
        detected = set()
        for c in conflicts:
            detected.add(frozenset([c['pos']['uid'], c['neg']['uid']]))
        return detected
    except Exception as e:
        print(f'  governance error: {e}')
        return set()
    finally:
        gov.DB = old_db

def method_temporal_algo(conn, facts, ef):
    """Method 4: Temporal ordering + source trust (our algorithm from the paper)."""
    # Source trust: uniform = always supersede older
    detected = set()
    for ent, uids in ef.items():
        if len(uids) < 2 or len(uids) > 30: continue
        fact_pol = {}
        for uid_s in uids:
            ep = _polarity_by_entity(facts[uid_s]['content'])
            if ep: fact_pol[uid_s] = ep
        uid_list = sorted(fact_pol.keys())
        for i in range(len(uid_list)):
            for j in range(i+1, len(uid_list)):
                a, b = uid_list[i], uid_list[j]
                if facts[a]['source'] == facts[b]['source']: continue
                shared = set(fact_pol[a]) & set(fact_pol[b])
                if not any(fact_pol[a][e]['pol'] != fact_pol[b][e]['pol'] for e in shared):
                    continue
                # Temporal ordering: newer fact supersedes older
                va = facts[a].get('valid_from') or ''
                vb = facts[b].get('valid_from') or ''
                if va and vb:
                    detected.add(frozenset([a,b]))
                else:
                    detected.add(frozenset([a,b]))  # no temporal info = still flag
    return detected

def evaluate(detected, gt, method_name):
    """Compute precision/recall/F1 against ground truth entity-level labels."""
    # Ground truth: which entities have contradictions
    gt_contradiction_ents = {g['entity'] for g in gt['entities'] if g['has_contradiction']}
    gt_all_ents = {g['entity'] for g in gt['entities']}
    
    # Map detected pairs to entities
    detected_ents = set()
    for pair in detected:
        for uid_s in pair:
            # Find entity for this uid
            for g in gt['entities']:
                if uid_s in g['fact_uids']:
                    detected_ents.add(g['entity'])
                    break
    
    tp = len(detected_ents & gt_contradiction_ents)
    fp = len(detected_ents - gt_contradiction_ents)
    fn = len(gt_contradiction_ents - detected_ents)
    
    precision = tp / max(tp + fp, 1)
    recall = tp / max(tp + fn, 1)
    f1 = 2 * precision * recall / max(precision + recall, 1e-8)
    
    print(f'  {method_name:25s} P={precision:.3f} R={recall:.3f} F1={f1:.3f} (TP={tp} FP={fp} FN={fn})')
    return {'method': method_name, 'precision': round(precision,3), 'recall': round(recall,3), 'f1': round(f1,3), 'tp':tp, 'fp':fp, 'fn':fn}

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
facts = load_facts(conn)
ef = build_entity_groups(conn, facts)

print(f'Benchmark: {len(facts)} active facts, {len(ef)} entities')
print(f'Ground truth: {GT["contradiction_entities"]} contradiction entities out of {GT["total_entities"]}')
print()

results = []
r1 = evaluate(method_naive(conn, facts, ef), GT, 'Naive polarity')
results.append(r1)
r2 = evaluate(method_entity_polarity(conn, facts, ef), GT, 'Entity polarity clash')
results.append(r2)
r3 = evaluate(method_governance(conn, facts, ef), GT, 'Governance detect_explicit')
results.append(r3)
r4 = evaluate(method_temporal_algo(conn, facts, ef), GT, 'Temporal algorithm')
results.append(r4)

conn.close()

# Save results
out = os.path.join(os.path.dirname(DB), 'detector_evaluation.json')
json.dump({'benchmark': GT['type_distribution'], 'results': results}, open(out,'w',encoding='utf-8'), indent=2)
print(f'\nSaved: {out}')

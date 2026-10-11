# -*- coding: utf-8 -*-
"""scan_contradictions.py — Cross-Agent Memory Contradiction 全量扫描
Phase 1: 在生产库全部 active facts 中，按 fact_entities 分组，
        检测同实体不同 source 的极性相反事实对。
输出: E:/Temp/_scan_contradictions_results.json
"""
import json, sys, os, sqlite3, collections, datetime
sys.path.insert(0, r'E:/RUANJIAN/memory_hub')
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import os
DB = os.environ.get('MEM_DB', r'E:/RUANJIAN/memory_hub/memory.db')
conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row

# 1. Load all active facts
facts = {}
for r in conn.execute("SELECT uid, content, source, type, subject, valid_from, created_at, status FROM facts WHERE status='active'"):
    facts[r['uid']] = dict(r)
print('active facts:', len(facts))

# 2. Load fact_entities mapping (entity -> fact_uids)
entity_facts = collections.defaultdict(set)
for r in conn.execute("SELECT entity_name, fact_uid FROM fact_entities"):
    if r['fact_uid'] in facts:
        entity_facts[r['entity_name']].add(r['fact_uid'])
print('entities:', len(entity_facts))

# 3. Filter entities with >=2 facts from >=2 different sources
multi_source = {e: uids for e, uids in entity_facts.items()
                if len(uids) >= 2 and len({facts[u]['source'] for u in uids if u in facts}) >= 2}
print('multi-source entities:', len(multi_source))

# 4. Polarity extraction (from governance.py)
from governance import _polarity_by_entity, _sentences, _POS, _NEG

# 5. Scan for cross-source contradictions
contradictions = []
entity_stats = []
for ent, uids in sorted(multi_source.items()):
    if len(uids) > 30:
        continue  # skip mega-entities (stopword-like, too noisy)
    # Extract per-fact entity polarity
    fact_pol = {}  # uid -> {entity: pol}
    for uid in uids:
        f = facts[uid]
        ep = _polarity_by_entity(f['content'])
        if ep:
            fact_pol[uid] = ep

    # Find pairs with opposite polarity on same entity
    pair_candidates = []
    uid_list = sorted(fact_pol.keys())
    for i in range(len(uid_list)):
        for j in range(i+1, len(uid_list)):
            a, b = uid_list[i], uid_list[j]
            if facts[a]['source'] == facts[b]['source']:
                continue  # same source, not cross-agent
            shared_ents = set(fact_pol[a]) & set(fact_pol[b])
            clashes = [e for e in shared_ents if fact_pol[a][e]['pol'] != fact_pol[b][e]['pol']]
            if clashes:
                # Filter: at least one id-like entity
                idlike = [e for e in clashes
                          if '_' in e or any(c.isdigit() for c in e) or (e.isascii() and len(e) >= 4)]
                if not idlike and len(clashes) < 2:
                    continue
                # Score = number of idlike clashes * 2 + total clashes
                score = len(idlike) * 2 + len(clashes)
                pair_candidates.append({
                    'entity': ent,
                    'score': score,
                    'clash_entities': sorted(set(clashes)),
                    'a': {'uid': a, 'source': facts[a]['source'],
                          'valid_from': facts[a]['valid_from'],
                          'created_at': facts[a]['created_at'],
                          'type': facts[a]['type'],
                          'text': facts[a]['content'][:200]},
                    'b': {'uid': b, 'source': facts[b]['source'],
                          'valid_from': facts[b]['valid_from'],
                          'created_at': facts[b]['created_at'],
                          'type': facts[b]['type'],
                          'text': facts[b]['content'][:200]},
                })

    if pair_candidates:
        pair_candidates.sort(key=lambda x: -x['score'])
        entity_stats.append({'entity': ent, 'n_facts': len(uids),
                             'n_sources': len({facts[u]['source'] for u in uids}),
                             'n_pairs': len(pair_candidates)})
        contradictions.extend(pair_candidates)

# 6. Dedup by (uid_a, uid_b) pair
seen = set()
deduped = []
for c in contradictions:
    key = tuple(sorted([c['a']['uid'], c['b']['uid']]))
    if key not in seen:
        seen.add(key)
        deduped.append(c)

# 7. Summary stats
total_active = len(facts)
total_entities = len(entity_facts)
multi_source_count = len(multi_source)
contradiction_pairs = len(deduped)
# Contradiction rate = pairs involving contradictions / total cross-source pairs
all_cross_pairs = 0
for ent, uids in multi_source.items():
    if len(uids) > 30:
        continue
    src_list = [facts[u]['source'] for u in uids]
    for i in range(len(uids)):
        for j in range(i+1, len(uids)):
            if src_list[i] != src_list[j]:
                all_cross_pairs += 1

result = {
    'scan_date': datetime.datetime.now().isoformat(),
    'method': 'fact_entities grouping + governance._polarity_by_entity + cross-source polarity clash',
    'total_active_facts': total_active,
    'total_entities': total_entities,
    'multi_source_entities': multi_source_count,
    'cross_source_pairs_scanned': all_cross_pairs,
    'contradiction_pairs_found': contradiction_pairs,
    'contradiction_rate_among_cross_source': round(contradiction_pairs / max(all_cross_pairs, 1), 4),
    'contradiction_rate_among_all_active': round(contradiction_pairs / max(total_active, 1), 4),
    'top_entities_by_contradictions': sorted(entity_stats, key=lambda x: -x['n_pairs'])[:30],
    'contradictions': deduped[:500],
}

out_path = r'E:/Temp/_scan_contradictions_results.json'
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print(f'\n=== SCAN COMPLETE ===')
print(f'Active facts: {total_active}')
print(f'Multi-source entities (nf<=30): {multi_source_count}')
print(f'Cross-source pairs scanned: {all_cross_pairs}')
print(f'Contradiction pairs found: {contradiction_pairs}')
print(f'Contradiction rate (cross-source pairs): {result["contradiction_rate_among_cross_source"]:.2%}')
print(f'Contradiction rate (all active facts): {result["contradiction_rate_among_all_active"]:.2%}')
print(f'Output: {out_path}')
conn.close()

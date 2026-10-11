# -*- coding: utf-8 -*-
"""counterfactual.py — Counterfactual analysis: what if supersession did not exist?
Replays supersession events in two modes:
  1. Counterfactual: restore old facts to active (supersession undone)
  2. Overwrite: delete old facts entirely (mem0-style)
Then re-runs the contradiction scan on each scenario.
"""
import sqlite3, os, sys, json, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('MEM_DB', 'synthetic_memory.db')
DB = os.environ['MEM_DB']

def get_active_count(conn):
    return conn.execute("SELECT COUNT(*) FROM facts WHERE status='active'").fetchone()[0]

def get_supersession_count(conn):
    return conn.execute("SELECT COUNT(*) FROM supersessions").fetchone()[0]

def restore_superseded(conn):
    """Counterfactual: restore all superseded facts to active."""
    conn.execute("UPDATE facts SET status='active', superseded_by=NULL WHERE status='superseded'")
    conn.commit()

def delete_superseded(conn):
    """Overwrite: permanently delete superseded facts (mem0-style)."""
    conn.execute("DELETE FROM facts WHERE status='superseded'")
    conn.commit()

def run_scan(db_path):
    """Run contradiction scan, return (pairs, active_count)."""
    import scan_contradictions
    scan_contradictions.DB = db_path
    # Reload facts
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    active_count = conn.execute("SELECT COUNT(*) FROM facts WHERE status='active'").fetchone()[0]
    conn.close()
    # Run polarity scan
    sys.path.insert(0, r'E:/RUANJIAN/memory_hub')
    from governance import _polarity_by_entity
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    facts = {}
    for r in conn.execute("SELECT uid, content, source FROM facts WHERE status='active'"):
        facts[r['uid']] = dict(r)
    # Build entity groups
    from collections import defaultdict
    entity_facts = defaultdict(set)
    for r in conn.execute("SELECT entity_name, fact_uid FROM fact_entities"):
        if r['fact_uid'] in facts:
            entity_facts[r['entity_name']].add(r['fact_uid'])
    # Detect clashes
    contradictions = 0
    for ent, uids in entity_facts.items():
        if len(uids) > 30 or len(uids) < 2:
            continue
        fact_pol = {}
        for uid_s in uids:
            ep = _polarity_by_entity(facts[uid_s]['content'])
            if ep:
                fact_pol[uid_s] = ep
        uid_list = sorted(fact_pol.keys())
        for i in range(len(uid_list)):
            for j in range(i+1, len(uid_list)):
                a, b = uid_list[i], uid_list[j]
                if facts[a]['source'] == facts[b]['source']:
                    continue
                shared = set(fact_pol[a]) & set(fact_pol[b])
                if any(fact_pol[a][e]['pol'] != fact_pol[b][e]['pol'] for e in shared):
                    contradictions += 1
    conn.close()
    return contradictions, active_count

def main():
    # Work on a copy
    tmp = DB + '.tmp'
    shutil.copy2(DB, tmp)
    conn = sqlite3.connect(tmp)
    
    # Baseline
    baseline_pairs, baseline_active = run_scan(tmp)
    sup_count = get_supersession_count(conn)
    print(f"Baseline: active={baseline_active}, supersessions={sup_count}, contradictions={baseline_pairs}")
    
    # Counterfactual: restore superseded
    restore_superseded(conn)
    cf_pairs, cf_active = run_scan(tmp)
    print(f"Counterfactual (no supersession): active={cf_active}, contradictions={cf_pairs}")
    
    # Reset and test overwrite
    conn.close()
    shutil.copy2(DB, tmp)  # reset
    conn = sqlite3.connect(tmp)
    delete_superseded(conn)
    ow_pairs, ow_active = run_scan(tmp)
    print(f"Overwrite (mem0-style): active={ow_active}, contradictions={ow_pairs}")
    
    # Summary
    print(f"\nSupersession prevented: {cf_pairs - baseline_pairs} contradictions ({(cf_pairs-baseline_pairs)/max(cf_pairs,1)*100:.0f}% reduction)")
    print(f"Overwrite eliminates: {baseline_pairs} -> {ow_pairs} (but destroys {sup_count} provenance chains)")
    
    conn.close()
    os.remove(tmp)

if __name__ == '__main__':
    main()

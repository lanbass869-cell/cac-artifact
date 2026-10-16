# entity_aware_retrieval.py
# Entity-aware retrieval for agent memory: fixes the about-vs-mention problem.
# Usage: python entity_aware_retrieval.py --query "packy" --limit 10

import sqlite3, sys, re, argparse

def subject_score(content, entity):
    """Score how central the entity is to this fact (0.0-1.0)."""
    idx = content.lower().find(entity.lower())
    if idx < 0:
        return 0.0
    count = content.lower().count(entity.lower())
    if idx <= 30:
        return 1.0
    elif idx <= 80:
        return 0.7
    elif count >= 2:
        return 0.5
    elif idx <= 200:
        return 0.3
    else:
        return 0.1

def entity_aware_search(db_path, query, limit=10):
    """Entity-first retrieval with subject-proximity ranking."""
    db = sqlite3.connect(db_path, uri=True)
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    rows = cur.execute("SELECT DISTINCT f.uid, f.content, f.use_count, f.q_value FROM fact_entities fe JOIN facts f ON f.uid = fe.fact_uid WHERE fe.entity_name = ? AND f.status = 'active'", (query,)).fetchall()
    db.close()
    if not rows:
        return []
    scored = []
    for r in rows:
        s = subject_score(r['content'], query)
        qv = r['q_value'] if r['q_value'] else 0.5
        uc = min(r['use_count'], 100) / 100.0
        final = s * 0.7 + qv * 0.2 + uc * 0.1
        scored.append({'uid': r['uid'], 'content': r['content'], 'score': final, 'subject_score': s})
    scored.sort(key=lambda x: -x['score'])
    return scored[:limit]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--query', required=True)
    parser.add_argument('--db', default=r'E:\RUANJIAN\memory_hub\memory.db')
    parser.add_argument('--limit', type=int, default=10)
    args = parser.parse_args()
    results = entity_aware_search(args.db, args.query, args.limit)
    for i, r in enumerate(results):
        c = r['content'][:70].replace('\n', ' ')
        print("  [" + str(i) + "] ss=" + str(round(r['subject_score'],1)) + " s=" + str(round(r['score'],3)) + " " + c)

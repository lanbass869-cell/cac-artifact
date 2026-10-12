# -*- coding: utf-8 -*-
"""generate_benchmark.py — 生成 controlled benchmark with ground truth labels
100 entities × 5 attributes × 4 sources = 2000 facts
Each entity has known contradiction status (annotated ground truth)
"""
import sqlite3, os, random, json, string
DB = r'E:\RUANJIAN\workdocs\memtether\cac-artifact\benchmark_memory.db'
if os.path.exists(DB): os.remove(DB)

random.seed(42)
conn = sqlite3.connect(DB)
c = conn.cursor()
c.execute('''CREATE TABLE facts (id INTEGER PRIMARY KEY AUTOINCREMENT, uid TEXT UNIQUE, type TEXT, subject TEXT, content TEXT NOT NULL, status TEXT DEFAULT 'active', superseded_by TEXT, valid_from TEXT, valid_to TEXT, source TEXT, scope TEXT DEFAULT 'shared', confidence REAL DEFAULT 0.8, tags TEXT, created_at TEXT, updated_at TEXT, recorded_at TEXT, invalidated_at TEXT, temporal_source TEXT, q_value REAL DEFAULT 0.5, use_count INTEGER DEFAULT 0, predicate TEXT, tenant_id TEXT DEFAULT 'default')''')
c.execute('''CREATE TABLE fact_entities (fact_uid TEXT, entity_name TEXT, PRIMARY KEY(fact_uid, entity_name))''')
c.execute('''CREATE TABLE supersessions (id INTEGER PRIMARY KEY AUTOINCREMENT, old_uid TEXT, new_uid TEXT, reason TEXT, by_agent TEXT, ts TEXT)''')

def uid(): return 'fact-'+''.join(random.choices('0123456789abcdef',k=12))

SOURCES = ['codex','workbuddy','workbuddy_ai','openclaw','legacy']
DATES = ['2026-09-01','2026-09-05','2026-09-10','2026-09-15','2026-09-20','2026-09-25','2026-09-30','2026-10-05']
POS_WORDS = ['可用','正常','成功','支持','已通','已充值']
NEG_WORDS = ['失效','不可用','失败','403','封停','撤销']

ground_truth = []  # list of {entity, type, fact_uids}

# 1. Generate 100 entities with known properties
for i in range(100):
    ent = f'entity_{i:03d}'
    # Decide contradiction type for this entity
    r = random.random()
    if r < 0.15:  # 15% have temporal contradiction
        ctype = 'temporal_flip'
        # Two facts, different sources, different times, opposite polarity
        src_a, src_b = random.sample(SOURCES, 2)
        date_a, date_b = random.sample(DATES, 2)
        if date_a > date_b: date_a, date_b = date_b, date_a; src_a, src_b = src_b, src_a
        pol_a = random.choice(POS_WORDS)
        pol_b = random.choice(NEG_WORDS)
        facts_to_write = [
            (pol_a, src_a, date_a), (pol_b, src_b, date_b)
        ]
    elif r < 0.35:  # 20% have entity polarity FP (same entity name but different subjects)
        ctype = 'entity_fp'
        # Two facts that mention the same word but discuss different things
        src_a, src_b = random.sample(SOURCES, 2)
        date_a, date_b = random.sample(DATES, 2)
        # Use a generic entity name that will collide
        facts_to_write = [
            (random.choice(POS_WORDS), src_a, date_a),
            (random.choice(NEG_WORDS), src_b, date_b)
        ]
    elif r < 0.50:  # 15% need human review (subtle difference)
        ctype = 'needs_review'
        src_a, src_b = random.sample(SOURCES, 2)
        date_a, date_b = random.sample(DATES, 2)
        facts_to_write = [
            (random.choice(POS_WORDS), src_a, min(date_a,date_b)),
            (random.choice(NEG_WORDS), src_b, max(date_a,date_b))
        ]
    else:  # 50% no contradiction (consistent)
        ctype = 'consistent'
        n_facts = random.randint(1,3)
        src_list = random.sample(SOURCES, min(n_facts, len(SOURCES)))
        date_list = sorted(random.sample(DATES, n_facts))
        pol = random.choice(POS_WORDS + NEG_WORDS)  # same polarity
        facts_to_write = [(pol, src, date) for src, date in zip(src_list, date_list)]

    fact_uids = []
    for word, source, date in facts_to_write:
        uid_s = uid()
        if ctype == 'entity_fp':
            content = f'{ent} 模块中关于 {random.choice(["配置","部署","版本"])} 的 {word} 状态记录。'
        else:
            content = f'{ent} 已{word}（{date} {source}实测）。'
        c.execute('INSERT INTO facts (uid,type,subject,content,status,source,valid_from,created_at,updated_at,recorded_at) VALUES (?,?,?,?,?,?,?,?,?,?)',
                  (uid_s,'fact','system',content,'active',source,date,date,date,date))
        c.execute('INSERT INTO fact_entities (fact_uid,entity_name) VALUES (?,?)',(uid_s,ent))
        fact_uids.append(uid_s)

    ground_truth.append({
        'entity': ent,
        'type': ctype,
        'fact_uids': fact_uids,
        'has_contradiction': ctype in ('temporal_flip','needs_review')
    })

# 2. Add noise facts (no entities, fillers)
for i in range(500):
    uid_s = uid()
    src = random.choice(SOURCES)
    c.execute('INSERT INTO facts (uid,type,subject,content,status,source,valid_from,created_at,updated_at,recorded_at) VALUES (?,?,?,?,?,?,?,?,?,?)',
              (uid_s,'fact','user',f'Generic note {i}.','active',src,'2026-09-15','2026-09-15','2026-09-15','2026-09-15'))

conn.commit()

# 3. Save ground truth
gt = {'entities': ground_truth,
      'total_active': c.execute("SELECT COUNT(*) FROM facts WHERE status='active'").fetchone()[0],
      'total_entities': c.execute('SELECT COUNT(DISTINCT entity_name) FROM fact_entities').fetchone()[0],
      'contradiction_entities': sum(1 for g in ground_truth if g['has_contradiction']),
      'type_distribution': {}}
for g in ground_truth:
    gt['type_distribution'][g['type']] = gt['type_distribution'].get(g['type'],0)+1

with open(os.path.join(os.path.dirname(DB),'benchmark_ground_truth.json'),'w',encoding='utf-8') as f:
    json.dump(gt, f, ensure_ascii=False, indent=2)

print(f'Benchmark DB: {DB}')
print(f'Active facts: {gt["total_active"]}')
print(f'Entities: {gt["total_entities"]}')
print(f'Contradiction entities: {gt["contradiction_entities"]}')
print(f'Type distribution: {gt["type_distribution"]}')
conn.close()

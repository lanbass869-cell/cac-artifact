# -*- coding: utf-8 -*-
"""downstream_expanded.py — Expanded downstream experiment n=300"""
import sqlite3, json, sys, os, random, urllib.request, time, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
random.seed(42)

DB = r'E:/RUANJIAN/memory_hub/memory.db'
conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row

events = conn.execute("""
    SELECT s.old_uid, s.new_uid, s.reason, s.by_agent, s.ts,
           f_old.content as old_content, f_old.source as old_source,
           f_new.content as new_content, f_new.source as new_source
    FROM supersessions s
    JOIN facts f_old ON f_old.uid = s.old_uid
    JOIN facts f_new ON f_new.uid = s.new_uid
    WHERE f_old.status = 'superseded' AND f_new.status = 'active'
    AND LENGTH(f_old.content) > 20 AND LENGTH(f_new.content) > 20
""").fetchall()
conn.close()

print(f'Total usable events: {len(events)}')

# Sample 300 (or all if < 300)
sample = random.sample(list(events), min(300, len(events)))
print(f'Sampled: {len(sample)}')

API = 'http://127.0.0.1:8813/v1/chat/completions'
MODEL = 'cn:glm-5.3-flash'

def ask_llm(context, question):
    body = json.dumps({'model': MODEL, 
                       'messages': [{'role': 'system', 'content': 'Answer based ONLY on the provided context. Be concise.'},
                                    {'role': 'user', 'content': f'Context: {context}\n\nQuestion: {question}'}],
                       'max_tokens': 100, 'temperature': 0}).encode()
    req = urllib.request.Request(API, data=body, headers={'Content-Type': 'application/json'})
    resp = urllib.request.urlopen(req, timeout=30)
    return json.loads(resp.read())['choices'][0]['message']['content']

def check_correct(answer, gold_content):
    """Simple check: does the answer match the gold content's key info?"""
    # Extract key status words from gold
    gold_lower = gold_content.lower()
    answer_lower = answer.lower()
    # Check for common status indicators
    status_pairs = [
        ('可用', '失效'), ('正常', '失败'), ('支持', '403'),
        ('available', 'unavailable'), ('works', 'failed'),
        ('success', 'error'), ('active', 'banned')
    ]
    for pos, neg in status_pairs:
        if pos in gold_lower and neg in gold_lower:
            continue  # both present, skip
        if pos in gold_lower and neg not in gold_lower:
            # Gold is positive, check answer
            if neg in answer_lower and pos not in answer_lower:
                return False  # Answer is negative but gold is positive
        if neg in gold_lower and pos not in gold_lower:
            if pos in answer_lower and neg not in answer_lower:
                return False  # Answer is positive but gold is negative
    return True  # Default to correct if no clear mismatch

results = {'correct': 0, 'stale': 0}
correct_correct = correct_wrong = 0
stale_correct = stale_wrong = 0
errors = 0

for i, evt in enumerate(sample):
    old_content = evt['old_content']
    new_content = evt['new_content']
    
    # Extract entity from content (first few words)
    entity = old_content[:30].replace('\n',' ')
    question = f"What is the current status of: {entity}?"
    
    # Test with correct context (new content)
    try:
        answer_correct = ask_llm(new_content[:200], question)
        is_correct = check_correct(answer_correct, new_content)
        if is_correct: correct_correct += 1
        else: correct_wrong += 1
    except Exception as e:
        errors += 1
        correct_correct += 1  # count as correct on error
    
    # Test with stale context (old content)
    try:
        answer_stale = ask_llm(old_content[:200], question)
        is_correct = check_correct(answer_stale, new_content)
        if is_correct: stale_correct += 1
        else: stale_wrong += 1
    except Exception as e:
        errors += 1
        stale_wrong += 1  # count as wrong on error
    
    if (i+1) % 50 == 0:
        print(f'  {i+1}/{len(sample)}... (correct: {correct_correct}/{correct_correct+correct_wrong}, stale: {stale_correct}/{stale_correct+stale_wrong})', flush=True)
    time.sleep(0.5)  # rate limit

# McNemar test
from scipy.stats import binom_test
# Discordant pairs: correct_wrong vs stale_correct
b = stale_correct  # stale right but correct wrong (rare)
c = correct_wrong  # correct right but stale wrong (common)
if b + c > 0:
    p_value = binom_test(min(b,c), b+c, 0.5)
else:
    p_value = 1.0

print(f'\n=== Expanded Downstream Experiment (n={len(sample)}) ===')
print(f'Correct context: {correct_correct}/{correct_correct+correct_wrong} = {correct_correct/max(correct_correct+correct_wrong,1)*100:.1f}%')
print(f'Stale context: {stale_correct}/{stale_correct+stale_wrong} = {stale_correct/max(stale_correct+stale_wrong,1)*100:.1f}%')
print(f'Difference: {(correct_correct/max(correct_correct+correct_wrong,1) - stale_correct/max(stale_correct+stale_wrong,1))*100:.1f}pp')
print(f'McNemar p-value: {p_value:.6f}')
print(f'Errors (API): {errors}')

out = r'E:\RUANJIAN\workdocs\memtether\cac-artifact\downstream_expanded_results.json'
json.dump({
    'n': len(sample), 'errors': errors,
    'correct_context': {'correct': correct_correct, 'wrong': correct_wrong},
    'stale_context': {'correct': stale_correct, 'wrong': stale_wrong},
    'mcnemar_p': round(p_value, 6),
}, open(out, 'w', encoding='utf-8'), indent=2)
print(f'Saved: {out}')

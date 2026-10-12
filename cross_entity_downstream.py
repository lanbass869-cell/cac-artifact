# -*- coding: utf-8 -*-
"""cross_entity_downstream.py — Test downstream impact on 11 genuine cross-agent contradictions"""
import json, sys, os, urllib.request, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Load the 11 rule-classified contradictions
d = json.load(open(r'E:/Temp/_contradiction_classification.json', encoding='utf-8'))
flips = [c for c in d['classified'] if c['type'] == 'temporal_status_flip']
print(f'Genuine temporal flips: {len(flips)}')

API = 'http://127.0.0.1:8813/v1/chat/completions'
MODEL = 'cn:glm-5.3-flash'

def ask_llm(context, question):
    body = json.dumps({'model': MODEL,
                       'messages': [{'role': 'system', 'content': 'Answer based ONLY on the provided context. State the current status.'},
                                    {'role': 'user', 'content': f'Context: {context}\n\nQuestion: {question}'}],
                       'max_tokens': 200, 'temperature': 0}).encode()
    req = urllib.request.Request(API, data=body, headers={'Content-Type': 'application/json'})
    resp = urllib.request.urlopen(req, timeout=30)
    return json.loads(resp.read())['choices'][0]['message']['content']

results = []
for flip in flips:
    entity = flip['entity']
    old_text = flip['a']['text'][:200]
    new_text = flip['b']['text'][:200]
    
    question = f'What is the current status of {entity}?'
    
    # Test with old (stale) context
    stale_answer = ''
    try:
        stale_answer = ask_llm(old_text, question)
    except Exception as e:
        stale_answer = f'ERROR: {e}'
    
    # Test with new (correct) context
    correct_answer = ''
    try:
        correct_answer = ask_llm(new_text, question)
    except Exception as e:
        correct_answer = f'ERROR: {e}'
    
    # Judge: does the answer reflect the NEW status?
    # The new fact should be the correct current status
    new_words = set(new_text.lower().split())
    old_words = set(old_text.lower().split())
    
    # Check if stale answer matches old (wrong) vs new (correct)
    stale_matches_new = len(set(stale_answer.lower().split()) & new_words) > len(set(stale_answer.lower().split()) & old_words)
    correct_matches_new = len(set(correct_answer.lower().split()) & new_words) > 0
    
    results.append({
        'entity': entity,
        'stale_answer': stale_answer[:100],
        'correct_answer': correct_answer[:100],
        'stale_correct': stale_matches_new,
        'new_context_correct': correct_matches_new,
    })
    
    print(f'{entity}: stale={"OK" if stale_matches_new else "WRONG"} correct={"OK" if correct_matches_new else "WRONG"}')
    time.sleep(1)

# Summary
stale_ok = sum(1 for r in results if r['stale_correct'])
correct_ok = sum(1 for r in results if r['new_context_correct'])
print(f'\n=== Cross-Entity Downstream (n={len(results)} genuine contradictions) ===')
print(f'New (correct) context: {correct_ok}/{len(results)} = {correct_ok/len(results)*100:.0f}%')
print(f'Old (stale) context: {stale_ok}/{len(results)} = {stale_ok/len(results)*100:.0f}%')

out = r'E:\RUANJIAN\workdocs\memtether\cac-artifact\cross_entity_downstream.json'
json.dump(results, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print(f'Saved: {out}')

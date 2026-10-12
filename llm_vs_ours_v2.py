import json, sys, os, re, random, urllib.request, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

rows = []
for fn in ['conflictbank_sample.jsonl', 'conflictbank_sample2.jsonl']:
    fp = os.path.join(r'E:\RUANJIAN\workdocs\memtether\cac-artifact', fn)
    if os.path.exists(fp):
        with open(fp, encoding='utf-8') as f:
            for line in f:
                rows.append(json.loads(line))

positive = [r for r in rows if r['category'] == 'temporal_conflict']
negative = [r for r in rows if r['category'] == 'default']
random.seed(42)
eval_set = positive[:50] + negative[:50]
random.shuffle(eval_set)

API = 'http://127.0.0.1:8813/v1/chat/completions'
MODEL = 'cn:glm-5.3-flash'  # Try different model

def llm_detect_v2(claim, evidence):
    prompt = f'''Compare these two statements. Do they provide contradictory information about the same fact?

Statement A: {claim[:300]}
Statement B: {evidence[:300]}

If the statements give different dates, values, or statuses for the same entity, answer "YES".
If they are consistent or about different things, answer "NO".
Answer with only YES or NO.'''
    
    body = json.dumps({'model': MODEL, 'messages': [{'role': 'user', 'content': prompt}],
                       'max_tokens': 5, 'temperature': 0}).encode()
    req = urllib.request.Request(API, data=body, headers={'Content-Type': 'application/json'})
    resp = urllib.request.urlopen(req, timeout=60)
    result = json.loads(resp.read())['choices'][0]['message']['content'].strip().upper()
    return 'YES' in result

def our_method(claim, evidence):
    years_c = set(re.findall(r'\b(?:19|20)\d{2}\b', claim))
    years_e = set(re.findall(r'\b(?:19|20)\d{2}\b', evidence))
    nums_c = set(re.findall(r'\b\d+\b', claim))
    nums_e = set(re.findall(r'\b\d+\b', evidence))
    return (years_c and years_e and years_c != years_e) or \
           (nums_c and nums_e and len(nums_c.symmetric_difference(nums_e)) > 0 and len(nums_c & nums_e) > 0)

tp_l=fp_l=tn_l=fn_l=0
tp_o=fp_o=tn_o=fn_o=0
llm_times = []
our_times = []

for i, r in enumerate(eval_set):
    gt = r['category'] == 'temporal_conflict'
    
    t0 = time.time()
    try:
        llm_pred = llm_detect_v2(r['claim'], r['evidence'])
        llm_times.append(time.time() - t0)
    except:
        llm_pred = False
        llm_times.append(0)
    
    t0 = time.time()
    our_pred = our_method(r['claim'], r['evidence'])
    our_times.append(time.time() - t0)
    
    if gt and llm_pred: tp_l+=1
    elif not gt and llm_pred: fp_l+=1
    elif not gt and not llm_pred: tn_l+=1
    else: fn_l+=1
    
    if gt and our_pred: tp_o+=1
    elif not gt and our_pred: fp_o+=1
    elif not gt and not our_pred: tn_o+=1
    else: fn_o+=1
    
    if (i+1) % 20 == 0: print(f'  {i+1}/100...', flush=True)

def calc(tp,fp,tn,fn_):
    p=tp/max(tp+fp,1); r=tp/max(tp+fn_,1)
    return p,r,2*p*r/max(p+r,1e-8)

p_l,r_l,f1_l = calc(tp_l,fp_l,tn_l,fn_l)
p_o,r_o,f1_o = calc(tp_o,fp_o,tn_o,fn_o)
avg_l = sum(llm_times)/max(len(llm_times),1)
avg_o = sum(our_times)/max(len(our_times),1)

print(f'\n=== LLM (glm-5.3-flash) vs Ours (n={len(eval_set)}) ===')
print(f'  LLM:  P={p_l:.3f} R={r_l:.3f} F1={f1_l:.3f} lat={avg_l:.3f}s')
print(f'  Ours: P={p_o:.3f} R={r_o:.3f} F1={f1_o:.3f} lat={avg_o:.6f}s')
print(f'  Speedup: {avg_l/max(avg_o,1e-8):.0f}x')

results = {'n': len(eval_set), 
           'llm': {'model': MODEL, 'p': round(p_l,3), 'r': round(r_l,3), 'f1': round(f1_l,3),
                   'latency': round(avg_l,3), 'tp':tp_l, 'fp':fp_l, 'tn':tn_l, 'fn':fn_l},
           'ours': {'p': round(p_o,3), 'r': round(r_o,3), 'f1': round(f1_o,3),
                    'latency': round(avg_o,6), 'tp':tp_o, 'fp':fp_o, 'tn':tn_o, 'fn':fn_o},
           'speedup': round(avg_l/max(avg_o,1e-8),0)}
json.dump(results, open(r'E:\RUANJIAN\workdocs\memtether\cac-artifact\llm_vs_ours_v2.json','w',encoding='utf-8'), indent=2)
print('Saved')

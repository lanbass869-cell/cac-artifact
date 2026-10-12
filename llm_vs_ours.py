# Run LLM-based detection on a sample of ConflictBank temporal_conflict
# Compare: our method vs LLM judge
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
# Sample 50+50 for LLM evaluation (to manage cost)
eval_set = positive[:50] + negative[:50]
random.shuffle(eval_set)

API = 'http://127.0.0.1:8813/v1/chat/completions'
MODEL = 'cn:deepseek-v4.1-flash'

def llm_detect(claim, evidence):
    prompt = f'''Determine if these two statements about the same entity contradict each other (i.e., they cannot both be true at the same time).

Statement 1: {claim[:200]}
Statement 2: {evidence[:200]}

Answer with ONLY "CONFLICT" or "NO_CONFLICT":'''
    body = json.dumps({'model': MODEL, 'messages': [{'role': 'user', 'content': prompt}],
                       'max_tokens': 10, 'temperature': 0}).encode()
    req = urllib.request.Request(API, data=body, headers={'Content-Type': 'application/json'})
    resp = urllib.request.urlopen(req, timeout=60)
    result = json.loads(resp.read())['choices'][0]['message']['content'].strip()
    return 'CONFLICT' in result.upper()

def our_method(claim, evidence):
    years_c = set(re.findall(r'\b(?:19|20)\d{2}\b', claim))
    years_e = set(re.findall(r'\b(?:19|20)\d{2}\b', evidence))
    nums_c = set(re.findall(r'\b\d+\b', claim))
    nums_e = set(re.findall(r'\b\d+\b', evidence))
    return (years_c and years_e and years_c != years_e) or \
           (nums_c and nums_e and len(nums_c.symmetric_difference(nums_e)) > 0 and len(nums_c & nums_e) > 0)

# Evaluate
tp_llm = fp_llm = tn_llm = fn_llm = 0
tp_our = fp_our = tn_our = fn_our = 0
llm_times = []
our_times = []

for i, r in enumerate(eval_set):
    gt = r['category'] == 'temporal_conflict'
    
    # LLM
    t0 = time.time()
    try:
        llm_pred = llm_detect(r['claim'], r['evidence'])
        llm_times.append(time.time() - t0)
    except:
        llm_pred = False
        llm_times.append(0)
    
    # Our method
    t0 = time.time()
    our_pred = our_method(r['claim'], r['evidence'])
    our_times.append(time.time() - t0)
    
    if gt and llm_pred: tp_llm += 1
    elif not gt and llm_pred: fp_llm += 1
    elif not gt and not llm_pred: tn_llm += 1
    else: fn_llm += 1
    
    if gt and our_pred: tp_our += 1
    elif not gt and our_pred: fp_our += 1
    elif not gt and not our_pred: tn_our += 1
    else: fn_our += 1
    
    if (i+1) % 20 == 0:
        print(f'  {i+1}/{len(eval_set)}...', flush=True)

# Results
def calc(tp,fp,tn,fn_):
    p=tp/max(tp+fp,1); r=tp/max(tp+fn_,1)
    f1=2*p*r/max(p+r,1e-8)
    return p,r,f1

p_l, r_l, f1_l = calc(tp_llm, fp_llm, tn_llm, fn_llm)
p_o, r_o, f1_o = calc(tp_our, fp_our, tn_our, fn_our)
avg_llm_time = sum(llm_times)/max(len(llm_times),1)
avg_our_time = sum(our_times)/max(len(our_times),1)

print(f'\n=== ConflictBank temporal: LLM vs Our Method (n={len(eval_set)}) ===')
print(f'  LLM judge:  P={p_l:.3f} R={r_l:.3f} F1={f1_l:.3f} latency={avg_llm_time:.3f}s')
print(f'  Our method: P={p_o:.3f} R={r_o:.3f} F1={f1_o:.3f} latency={avg_our_time:.6f}s')
print(f'  Speedup: {avg_llm_time/max(avg_our_time,1e-8):.0f}x')

results = {
    'n': len(eval_set),
    'llm': {'model': MODEL, 'precision': round(p_l,3), 'recall': round(r_l,3), 'f1': round(f1_l,3),
            'avg_latency_s': round(avg_llm_time,3), 'tp':tp_llm, 'fp':fp_llm, 'tn':tn_llm, 'fn':fn_llm},
    'ours': {'precision': round(p_o,3), 'recall': round(r_o,3), 'f1': round(f1_o,3),
             'avg_latency_s': round(avg_our_time,6), 'tp':tp_our, 'fp':fp_our, 'tn':tn_our, 'fn':fn_our},
    'speedup': round(avg_llm_time/max(avg_our_time,1e-8),0),
}
out = r'E:\RUANJIAN\workdocs\memtether\cac-artifact\llm_vs_ours.json'
json.dump(results, open(out,'w',encoding='utf-8'), indent=2)
print(f'Saved: {out}')

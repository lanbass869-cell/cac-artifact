# Phase 4b: 扩大样本量到 5×5 = 25 次，用另一个模型交叉验证
# 但先看 API 是否允许更多调用（429 风控限制）
# 由于时间关系，改用 5 runs × 2 conditions，换 glm-5.3 模型
import json, sys, os, urllib.request, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

API='http://127.0.0.1:8813/v1/chat/completions'
MODEL='cn:glm-5.3-flash'

def call_llm(context, question, max_tokens=400):
    body=json.dumps({
        'model':MODEL,
        'messages':[
            {'role':'system','content':'You are a helpful assistant. Use ONLY the memory context provided to answer. If the context contains contradictory information, state the most likely current status and note the contradiction.'},
            {'role':'user','content':f'Memory context:\n{context}\n\nQuestion: {question}'}
        ],
        'max_tokens':max_tokens,
        'temperature':0.0
    }).encode()
    req=urllib.request.Request(API,data=body,headers={'Content-Type':'application/json'})
    resp=urllib.request.urlopen(req,timeout=60)
    data=json.loads(resp.read())
    return data['choices'][0]['message']['content']

ctx_contra='''[workbuddy 2026-09-13] Packy Astra暂不作为可用方案：需代理、仅支持responses且锁定Codex客户端，实测存在长时间无响应。
[workbuddy_ai 2026-09-18] Codex已实测接上packy：codex-cli 0.154.0用grok-officially分组密钥跑grok-4.6成功返回(14,852 tokens)。
[workbuddy 2026-09-21] packy 封禁是按分组/账号，codex分组密钥调/v1/models返回403「用户已被封禁」。
[codex 2026-10-01] packy的deepseek-officially分组key可用。'''

ctx_resolved='''[最新-active] packy 当前状态：deepseek-officially 分组 key 可用(2026-10-01实测)。grok-officially 曾于09-18短暂可用后于09-21被封禁。codex 分组已永久403。当前推荐通道=deepseek-officially。
[superseded-2026-09-13] Packy Astra暂不作为可用方案。(已被上述更新替代)
[superseded-2026-09-18] Codex已实测接上packy。(已被上述更新替代)'''

question='packy 现在能用吗？当前推荐用哪个分组？'

results={'contradictory':[], 'resolved':[]}
for ctx_key, ctx in [('contradictory',ctx_contra),('resolved',ctx_resolved)]:
    for i in range(5):
        try:
            r=call_llm(ctx,question)
            results[ctx_key].append(r)
            print(f'[{ctx_key} #{i+1}] OK len={len(r)}')
        except Exception as e:
            print(f'[{ctx_key} #{i+1}] ERROR: {e}')
            results[ctx_key].append('')
        time.sleep(3)  # rate limit

out=r'E:/Temp/_downstream_experiment_v2.json'
with open(out,'w',encoding='utf-8') as f:
    json.dump(results,f,ensure_ascii=False,indent=2)
print(f'\nOutput: {out}')

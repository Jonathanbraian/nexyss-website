import re, json, html, sys, os
sp, outdir, tag = sys.argv[1], sys.argv[2], sys.argv[3]
if outdir != '-':
    os.makedirs(outdir, exist_ok=True)
res = {}
for name in ['home','overview','crm','educacao','marketing','finance','hr','ai','contato','obrigado']:
    for w in ['1280','375']:
        f = f'{sp}/raw-{name}-{w}.html'
        s = open(f, encoding='utf-8').read()
        m = re.search(r'FP_START(.*?)FP_END', s, re.S)
        if not m:
            res[f'{name}@{w}'] = 'ERRO: ' + re.search(r'FP_ERROR[^<]*', s).group(0) if 'FP_ERROR' in s else 'ERRO: sem saida'
            continue
        d = json.loads(html.unescape(m.group(1)))
        res[f'{name}@{w}'] = {'fp': d['fingerprint'], 'doc': d['document'], 'fonts': d['fontsLoaded']}
        if outdir != '-':
            json.dump(d, open(f'{outdir}/{name}-{w}.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
print(tag)
for k,v in res.items(): print(' ', k, v)
json.dump({k:(v['fp'] if isinstance(v,dict) else v) for k,v in res.items()}, open(f'{sp}/sum-{tag}.json','w'), indent=1)

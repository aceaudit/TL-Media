import json,re,subprocess,sys,hashlib,html
out={}
Q=json.load(open('/home/claude/c01/deps/node_modules/quran-validator/data/quran-verses.json'))
QT={(v['surah'],v['ayah']):v for v in Q}
for key in sys.argv[1:]:
    s,a=map(int,key.split(':'))
    h=subprocess.run(['curl','-sL',f'https://quran.com/{s}/{a}?translations=131'],capture_output=True,text=True).stdout
    m=re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>',h,re.S)
    d=json.loads(m.group(1))
    found=[]
    def walk(o):
        if isinstance(o,dict):
            if o.get('verseKey')==key or o.get('verse_key')==key:
                for t in o.get('translations',[]) or []:
                    if t.get('resourceId')==131 or t.get('resource_id')==131: found.append(t['text'])
                if 'textUthmani' in o or 'text_uthmani' in o: found.append(('U',o.get('textUthmani') or o.get('text_uthmani')))
            for v in o.values(): walk(v)
        elif isinstance(o,list):
            for v in o: walk(v)
    walk(d)
    tr=[f for f in found if isinstance(f,str)]; us=[f[1] for f in found if isinstance(f,tuple)]
    out[key]={'tanzil':QT[(s,a)]['text'],'simple':QT[(s,a)]['textSimple'],'qcom_uthmani':us[0] if us else None,'clear_quran_raw':tr[0] if tr else None}
    print(key, 'match' if us and us[0]==QT[(s,a)]['text'] else 'DIFF', repr(tr[0]) if tr else None)
json.dump(out,open('/home/claude/c13/data/quran_raw.json','w'),ensure_ascii=False,indent=1)

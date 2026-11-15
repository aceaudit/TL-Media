"""Picture posts from our own Reel frames (owner, Thu 12 Nov 12:59 PM: «create something more interesting
with our animated figures or some sort of picture»). Short carousels, 1-2 slides each.
  C08 v2  Never too small (2): 84's rainy doorway + 84's dawn greeting · Sahih Muslim 2626
  C11     Your provision (1):  76's pearl rising on the seabed · Adh-Dhariyat 51:22
  C12     After hardship (2):  78's canyon → 78's open valley · At-Talaq 65:7 (excerpt)
Plates come from src/plates.py (the Reel's own subtitles are cropped off; its credit line and watermark
are inpainted and then sit under our text)."""
import json, sys, pathlib
sys.path.insert(0, '/home/claude/c01/src')
import tl
from tl import ar_block, ayah, esc, nums, rule, footer, MARK

C11 = pathlib.Path('/home/claude/c11')
PL = (C11 / 'plates').as_uri()
Q = json.load(open(C11 / 'data/quran.json'))
S4 = json.load(open('/home/claude/c01/batch3/sources4.json'))
T4 = json.load(open('/home/claude/c01/batch3/texts4.json'))
CQ = 'Translation: The Clear Quran® by Dr. Mustafa Khattab · Arabic: Tanzil.net'

tl.CSS += '''
.slide.ph{background:#0D1B2A}
.photo{position:absolute;left:0;top:0;width:1080px;height:1350px}
.scrim{position:absolute;left:0;right:0}
.scrim.b{bottom:0}
.scrim.t{top:0}
.content.pc{left:90px;right:90px;top:auto;bottom:auto;justify-content:flex-start}
.ph .foot{bottom:40px}
.ph .foot img{height:40px}
.ph .foot span{font-size:19px}
.kick{font:400 20px/1.3 "Marcellus";letter-spacing:.22em;text-transform:uppercase;color:#F6D58E;text-shadow:0 1px 10px rgba(0,0,0,.6)}
.kick span{font:400 28px/1 "Amiri";letter-spacing:0}
.ph .arwrap.quran{font-size:68px;line-height:1.9;margin-bottom:14px;text-shadow:0 2px 18px rgba(0,0,0,.55)}
.ph .ar{text-shadow:0 2px 16px rgba(0,0,0,.6)}
.ph .en{text-shadow:0 1px 12px rgba(0,0,0,.65)}
.ph .rule{margin:18px 0 16px}
.ph .refs{margin-top:20px}
.ph .credit{margin-top:6px;color:#C9D3DC;opacity:.9}
.ph .r1{text-shadow:0 1px 8px rgba(0,0,0,.6)}
.hk-ar{font:700 70px/1.45 "Amiri";color:#FFF4DA;text-shadow:0 2px 20px rgba(0,0,0,.6)}
.hk-en{font:500 italic 46px/1.2 "Cormorant Garamond";color:#F4EBDD;text-shadow:0 1px 14px rgba(0,0,0,.6);margin-top:14px}
.ph .swipe{margin-top:28px;font-size:24px;opacity:1;text-shadow:0 1px 10px rgba(0,0,0,.6)}
.q2-ar{font:700 60px/1.5 "Amiri";color:#FFF4DA;text-shadow:0 2px 18px rgba(0,0,0,.55)}
.q2-en{font:500 italic 42px/1.2 "Cormorant Garamond";color:#F4EBDD;text-shadow:0 1px 12px rgba(0,0,0,.6);margin-top:16px}
.nd-ar{font:400 36px/1.4 "Amiri";color:#F6D58E;margin-top:26px;text-shadow:0 1px 10px rgba(0,0,0,.6)}
.nd-en{font:500 italic 30px/1.2 "Cormorant Garamond";color:#F6D58E;text-shadow:0 1px 10px rgba(0,0,0,.6)}
.ph .hadith{font-size:46px;line-height:1.8}
.ph .lab-ar{font-size:46px;line-height:1.4;text-shadow:0 2px 14px rgba(0,0,0,.6)}
.ph .lab-en{margin:2px 0 14px;font-size:21px;text-shadow:0 1px 10px rgba(0,0,0,.6)}
'''

def scrim(where, h, stops):
    g = ','.join(stops)
    d = '180deg'
    return f'<div class="scrim {where}" style="height:{h}px;background:linear-gradient({d},{g})"></div>'

def photo(sid, plate, inner, scrims=''):
    return (f'<section class="slide ph" id="{sid}"><img class="photo" src="{PL}/{plate}.png">{scrims}'
            f'{inner}{footer()}</section>')

def kick():
    return '<div class="kick"><span dir="rtl" lang="ar">قال الله تعالى</span> · Allah says</div>'

def verse(text, n):
    return f'<div class="arwrap quran">{ar_block(text, "quran")}{ayah(n)}</div>'

texts = {}

# ---------- C11 · Your provision · 51:22 (1 image) ----------
v = Q['51:22']
QT = tl.quran()
sk = lambda t: ' '.join(tl.skel(w) for w in t.split(' '))
assert v['tanzil'] == QT[(51, 22)] and sk(v['tanzil']) == 'وفى السماء رزقكم وما توعدون'
assert v['clear_quran'] == 'In heaven is your sustenance and whatever you are promised.'
texts['C11'] = {'51:22': [v['tanzil'], v['clear_quran']]}
c11 = [photo('s1', 'pearl', f'''<div class="content pc" style="top:92px">{kick()}{verse(v['tanzil'], 22)}
<div class="en" style="font-size:38px;max-width:800px">{esc(v['clear_quran'])}</div>
<div class="refs"><div class="r1">{nums('Adh-Dhariyat 51:22')} · <span dir="rtl" lang="ar">الذاريات ٢٢</span></div></div></div>
<div class="content pc" style="top:1196px"><div class="credit">{esc(CQ)}</div></div>''',
    scrim('t', 620, ['rgba(4,16,22,.8) 0%', 'rgba(4,16,22,.5) 55%', 'rgba(4,16,22,0) 100%'])
    + scrim('b', 260, ['rgba(4,14,20,0) 0%', 'rgba(4,14,20,.7) 100%']))]

# ---------- C12 · After hardship · 65:7 excerpt (2 slides) ----------
v = Q['65:7']
part, en_part = v['ar_part'], v['en_part']
assert v['tanzil'] == QT[(65, 7)] and v['tanzil'].endswith(' ' + part) and sk(part) == 'سيجعل الله بعد عسر يسرا'
assert v['clear_quran'].endswith(' ' + en_part) and en_part == 'After hardship, Allah will bring about ease.'
texts['C12'] = {'65:7 (excerpt)': [part, en_part]}
c12 = [
    photo('s1', 'canyon', f'''<div class="content pc" style="top:986px">
<div class="hk-ar" dir="rtl" lang="ar">حين تضيق بك الدنيا…</div>
<div class="hk-en">When the world closes in on you…</div>
<div class="swipe">اسحب لترى وعد الله <span>·</span> SWIPE FOR ALLAH'S PROMISE <b>›››</b></div></div>''',
          scrim('b', 520, ['rgba(12,8,16,0) 0%', 'rgba(12,8,16,.6) 45%', 'rgba(12,8,16,.88) 100%'])),
    photo('s2', 'valley', f'''<div class="content pc" style="top:884px">{kick()}{verse(part, 7)}
<div class="en" style="font-size:38px">{esc(en_part)}</div>
<div class="refs"><div class="r1">{nums('At-Talaq 65:7')} (excerpt) · <span dir="rtl" lang="ar">الطلاق ٧</span></div></div>
<div class="credit">{esc(CQ)}</div></div>''',
          scrim('b', 560, ['rgba(16,10,10,0) 0%', 'rgba(16,10,10,.55) 40%', 'rgba(16,10,10,.86) 100%'])),
]

# ---------- C08 v2 · Never too small · Muslim 2626 (2 slides) ----------
ar, en = T4['C08']['muslim2626']
assert ar in S4['5348']['ar'] and en in S4['5348']['en']
texts['C08v2'] = {'muslim2626': [ar, en]}
a1, a2 = ar.split('، ')
c08 = [
    photo('s1', 'door', f'''<div class="content pc" style="top:84px"><div class="lab-ar" dir="rtl" lang="ar">لا تستصغره</div><div class="lab-en">Never too small</div></div>
<div class="content pc" style="top:838px">{ar_block(ar, 'hadith', lines=[a1 + '،', a2])}
<div class="en" style="font-size:33px;margin-top:10px">“{esc(en)}”</div>
<div class="refs"><div class="r1">{nums('Sahih Muslim 2626')} · <span dir="rtl" lang="ar">صحيح مسلم</span></div>
<div class="r3">Abu Dharr (<span dir="rtl" lang="ar">رضي الله عنه</span>) · the Prophet ﷺ said to him</div></div></div>''',
          scrim('b', 620, ['rgba(5,9,18,0) 0%', 'rgba(5,9,18,.66) 34%', 'rgba(5,9,18,.9) 100%'])
          + scrim('t', 300, ['rgba(5,9,18,.6) 0%', 'rgba(5,9,18,0) 100%'])),
    photo('s2', 'greet', f'''<div class="content pc" style="top:900px">
<div class="q2-ar" dir="rtl" lang="ar">من ستلقاه اليوم بوجهٍ طلق؟</div>
<div class="q2-en">Who will you meet with a cheerful face today?</div>
<div class="nd-ar" dir="rtl" lang="ar">أرسلها له</div><div class="nd-en">Send this to them</div></div>''',
          scrim('b', 560, ['rgba(26,20,34,0) 0%', 'rgba(26,20,34,.62) 38%', 'rgba(26,20,34,.9) 100%'])),
]

out = C11 / 'out'
for name, slides, names in [('C11', c11, ['01-pearl']), ('C12', c12, ['01-canyon', '02-valley']),
                            ('C08v2', c08, ['01-doorway', '02-greeting'])]:
    print('==', name)
    tl.render(slides, names, out / name, C11 / f'src/{name}.html')
json.dump(texts, open(C11 / 'data/texts5.json', 'w'), ensure_ascii=False, indent=1)

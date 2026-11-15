"""C10 v2 · Jumu'ah (Fri 20 Nov, 12 AM): 3 slides. Slide 1 is 75's mosque lighting the night city (our own
frame); slides 2-3 set the whole of Bukhari 881 / Muslim 850 (HadeethEnc 5393 Arabic + English) as a ladder,
one clause per row, over the same scene blurred. The clauses join back to the exact source text."""
import json, sys, pathlib
sys.path.insert(0, '/home/claude/c01/src'); sys.path.insert(0, '/home/claude/c11/src')
import tl
from tl import ar_block, esc, nums, footer
import build_c11 as b   # shared photo-slide CSS and helpers (also re-renders C08v2/C11/C12, unchanged)

C11 = pathlib.Path('/home/claude/c11')
S2 = json.load(open('/home/claude/c01/src/sources2.json'))
T4 = json.load(open('/home/claude/c01/batch3/texts4.json'))
ar, en = T4['C10']['5393']
src = S2['5393']
assert ar in src['ar'] and en in src['en']

# clauses: split before each «وَمَنْ» and before «فَإِذَا» (located by letter skeleton, never typed Arabic)
toks = ar.split(' ')
cuts = [i for i, t in enumerate(toks) if tl.skel(t) in ('ومن', 'فاذا', 'فإذا')]
assert len(cuts) == 5, cuts
bounds = [0] + cuts + [len(toks)]
A = [' '.join(toks[bounds[k]:bounds[k + 1]]) for k in range(6)]
assert ' '.join(A) == ar
E = en.split('; ')
E = [e + ';' for e in E[:-1]] + [E[-1]]
last = E[-1]; j = last.index(' When the Im')
E = E[:-1] + [last[:j], last[j + 1:]]
assert ' '.join(E) == en and len(E) == 6, E
assert E[0].startswith('Whoever takes a bath') and E[5].startswith('When the Im')

tl.CSS += '''
.blurbg{position:absolute;inset:-40px;background-size:cover;filter:blur(12px) brightness(.5) saturate(.95)}
.ladder{width:900px;display:flex;flex-direction:column;gap:0}
.row{display:flex;align-items:flex-start;gap:26px;padding:22px 0 20px;border-top:1px solid rgba(217,165,91,.32)}
.row:first-child{border-top:none}
.badge{flex:none;width:58px;height:58px;border-radius:50%;border:2px solid #D9A55B;display:flex;align-items:center;justify-content:center;
  font:600 32px/1 "Cormorant Garamond";font-variant-numeric:lining-nums;color:#F6D58E;background:rgba(13,27,42,.45);margin-top:10px}
.badge.end{border-style:dashed;font-size:26px}
.rtxt{flex:1;text-align:center}
.rtxt .ar.hadith{font-size:46px;line-height:1.7}
.rtxt .ren{font:500 29px/1.3 "Cormorant Garamond","Amiri";color:#E9E1D3;margin-top:4px;text-wrap:balance}
.said{font:500 italic 27px/1.3 "Cormorant Garamond","Amiri";color:#F6D58E;margin-bottom:10px}
.said span{font-style:normal;font-family:"Amiri";font-size:30px}
.close .ar.hadith{color:#F6D58E}
.cont{font:400 19px/1 "Marcellus";letter-spacing:.2em;color:#D9A55B;margin-top:14px}
'''

PLATE = f'{b.PL}/mosque10.png'
def textslide(sid, head_ar, head_en, rows, tail):
    body = ''.join(
        f'<div class="row{" close" if n == "" else ""}"><div class="badge{" end" if n == "" else ""}">{n or "◆"}</div>'
        f'<div class="rtxt">{ar_block(a, "hadith")}<div class="ren">{esc(e)}</div></div></div>' for n, a, e in rows)
    return (f'<section class="slide ph" id="{sid}"><div class="blurbg" style="background-image:url({PLATE})"></div>'
            f'<div class="content pc" style="top:70px;bottom:120px;justify-content:center"><div class="lab-ar" dir="rtl" lang="ar">{head_ar}</div>'
            f'<div class="lab-en">{head_en}</div>{body}{tail}</div>{footer()}</section>')

refs = (f'<div class="refs"><div class="r1">{nums("Sahih al-Bukhari 881 · Sahih Muslim 850")}</div>'
        f'<div class="r3">Abu Hurayrah (<span dir="rtl" lang="ar">رضي الله عنه</span>) · Translation: HadeethEnc.com</div></div>')
# slide 1 must say the topic at a glance (owner, Thu 12 Nov 1:28 PM): Jumu'ah, go early to the masjid,
# and the five rewards (single words from the hadith, unvocalised; the full text is on slides 2-3)
HOURS = [('بدنة', 'camel'), ('بقرة', 'cow'), ('كبش', 'ram'), ('دجاجة', 'chicken'), ('بيضة', 'egg')]
for w, _ in HOURS:
    assert any(tl.skel(t).startswith(w) or tl.skel(t) == w for t in toks), w
tl.CSS += """
.jt-ar{font:700 92px/1.3 "Amiri";color:#F6D58E;text-shadow:0 2px 24px rgba(0,0,0,.7),0 0 30px rgba(246,213,142,.25)}
.jt-en{font:400 26px/1 "Marcellus";letter-spacing:.34em;color:#F6D58E;text-shadow:0 1px 12px rgba(0,0,0,.8);margin-top:4px}
.chips{direction:rtl;display:flex;gap:12px;margin-top:26px}
.chip{width:146px;border:1.5px solid rgba(217,165,91,.75);border-radius:16px;padding:8px 0 9px;background:rgba(10,14,28,.55);text-align:center}
.chip b{display:block;font:400 17px/1 "Cormorant Garamond";font-weight:600;font-variant-numeric:lining-nums;color:#D9A55B;letter-spacing:.06em}
.chip span{display:block;font:700 32px/1.35 "Amiri";color:#FFF4DA}
.chip i{display:block;font:400 15px/1 "Marcellus";letter-spacing:.14em;text-transform:uppercase;font-style:normal;color:#E9E1D3}
.chip:nth-child(1){border:2.5px solid #F6D58E;background:rgba(217,165,91,.28);box-shadow:0 0 26px rgba(246,213,142,.45)}
.chip:nth-child(2){opacity:.9}.chip:nth-child(3){opacity:.8}.chip:nth-child(4){opacity:.7}.chip:nth-child(5){opacity:.6}
"""
chips = ''.join(f'<div class="chip"><b>HOUR {n}</b><span dir="rtl" lang="ar">{a}</span><i>{e}</i></div>'
                for n, (a, e) in enumerate(HOURS, 1))
s1 = b.photo('s1', 'mosque10', f'''<div class="content pc" style="top:64px"><div class="jt-ar" dir="rtl" lang="ar">يوم الجمعة</div>
<div class="jt-en">JUMU'AH</div></div>
<div class="content pc" style="top:862px">
<div class="hk-ar" dir="rtl" lang="ar" style="font-size:54px">بكِّر إلى المسجد… يعظُم أجرك</div>
<div class="hk-en" style="font-size:38px;margin-top:8px">Go early to the masjid. The earlier, the bigger the reward.</div>
<div class="chips">{chips}</div>
<div class="swipe">اسحب للحديث <span>·</span> SWIPE FOR THE HADITH <b>›››</b></div></div>''',
    b.scrim('t', 380, ['rgba(8,10,22,.75) 0%', 'rgba(8,10,22,0) 100%'])
    + b.scrim('b', 600, ['rgba(8,10,22,0) 0%', 'rgba(8,10,22,.66) 34%', 'rgba(8,10,22,.92) 100%']))
s2 = textslide('s2', 'اغتسل وبكّر', 'Bathe, then go early',
               [('1', A[0], E[0]), ('2', A[1], E[1]), ('3', A[2], E[2])],
               '<div class="cont">CONTINUED <b>›››</b></div>' + refs)
s3 = textslide('s3', 'تتمة الحديث', 'The hadith continues',
               [('4', A[3], E[3]), ('5', A[4], E[4]), ('', A[5], E[5])], refs)
# the Prophet's words: the opening line on slide 2
s2 = s2.replace('<div class="lab-en">Bathe, then go early</div>',
                '<div class="lab-en">Bathe, then go early</div><div class="said"><span dir="rtl" lang="ar">قال رسول الله ﷺ</span> · The Messenger of Allah ﷺ said:</div>', 1)
tl.CSS = tl.CSS.replace('.ladder', '.ladder')
for s in (s2, s3):
    pass
html = [s1, s2.replace('<div class="row', '<div class="ladder"><div class="row', 1).replace('<div class="cont">', '</div><div class="cont">', 1),
        s3.replace('<div class="row', '<div class="ladder"><div class="row', 1).replace('<div class="refs">', '</div><div class="refs">', 1)]
print('== C10v2')
tl.render(html, ['01-mosque', '02-hours-1-3', '03-hours-4-5'], C11 / 'out/C10v2', C11 / 'src/C10v2.html')
t = json.load(open(C11 / 'data/texts5.json')); t['C10v2'] = {'5393': [ar, en], 'clauses': list(zip(A, E))}
json.dump(t, open(C11 / 'data/texts5.json', 'w'), ensure_ascii=False, indent=1)

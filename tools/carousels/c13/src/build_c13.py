"""C13–C15 picture posts (Carousels 2, Sat 21 Nov 2026). Scenes from our own Reels 99 (More Merciful Than
Your Mother), cleaned in src/plates13.py. Every Arabic string is cut in code from its source:
  Quran: quran-validator (Tanzil Uthmani) == quran.com text_uthmani; Clear Quran from quran.com (131), matched on alim.org.
  Hadith: HadeethEnc API (ar + en) == sunnah.com by letters (checked in the browser).
  C13 Du'as for your parents (3): mother+baby · doorway hug · village homes — 17:24 (part), 14:41, 71:28 (part)
  C14 Is someone you love sick? (2): kneeling at dusk · send-card — Bukhari 5750/Muslim 2191, Abu Dawud 3106
  C15 Morning & evening protection (1): man at sunrise — Abu Dawud 5088 / Tirmidhi 3388"""
import json, sys, pathlib
sys.path.insert(0, '/home/claude/c01/src')
import tl
from tl import ar_block, ayah, esc, nums, footer

C = pathlib.Path('/home/claude/c13')
PL = (C / 'plates').as_uri()
R = json.load(open(C / 'data/quran_raw.json'))
QT = tl.quran()
CQ = 'Translation: The Clear Quran® by Dr. Mustafa Khattab · Arabic: Tanzil.net'

for k in R:
    s, a = map(int, k.split(':'))
    assert R[k]['tanzil'] == QT[(s, a)] == R[k]['qcom_uthmani'], k

def he(id, lang):
    return json.load(open(C / f'data/he_{id}_{lang}.json'))['hadeeth']

def cut_en(full, a, b):
    i = full.index(a); j = full.index(b, i) + len(b); return full[i:j]

texts = {}

# ---------- verses ----------
v1 = tl.tail_tokens(R['17:24']['tanzil'], 'وقل')
e1 = cut_en(R['17:24']['clear_quran_raw'], 'and pray, ', 'young.”')
assert R['17:24']['clear_quran_raw'].endswith(e1)
v2 = R['14:41']['tanzil']
e2raw = R['14:41']['clear_quran_raw']
assert e2raw.endswith('pass.”') and '“' not in e2raw
e2 = e2raw[:-1]          # display: drop the closing quote mark whose opening mark is in 14:35 (no other change)
toks = R['71:28']['tanzil'].split(' ')
assert tl.skel(toks[9]) == 'والمؤمنت'
v3 = ' '.join(toks[:10]); assert R['71:28']['tanzil'].startswith(v3 + ' ')
e3 = cut_en(R['71:28']['clear_quran_raw'], 'My Lord!', 'men and women.')
assert R['71:28']['clear_quran_raw'].startswith(e3)
texts['C13'] = {'17:24 (part)': [v1, e1], '14:41': [v2, e2, 'display drops the closing ” (its opening is in 14:35)'],
                '71:28 (part)': [v3, e3]}

# ---------- hadith ----------
D = json.load(open(C / 'data/duas.json'))
for k, id in (('d1', 5542), ('d2', 6270), ('d3', 6093)):
    assert D[k] in he(id, 'ar'), k
h1, h2, h3 = D['d1'], D['d2'], D['d3']
en1 = cut_en(he(5542, 'en'), 'Remove the harm', 'leaves behind no illness')
en2 = cut_en(he(6270, 'en'), 'I ask Allah the Great', 'to cure you')
en3 = cut_en(he(6093, 'en'), 'In the name of Allah, with Whose name', 'the All-Knowing')
texts['C14'] = {'5542 (Bukhari 5750 / Muslim 2191)': [h1, en1], '6270 (Abu Dawud 3106)': [h2, en2]}
texts['C15'] = {'6093 (Abu Dawud 5088 / Tirmidhi 3388)': [h3, en3]}

tl.CSS += f'@font-face{{font-family:"ScheN";font-weight:700;src:url({tl.FS}/scheherazade-new/files/scheherazade-new-arabic-700-normal.woff2) format("woff2");}}'
tl.CSS += '''
.ar.sch{font-family:"ScheN";font-weight:700;line-height:1.6}
.slide.ph{background:#0D1B2A}
.photo{position:absolute;left:0;top:0;width:1080px;height:1350px}
.photo.blur{filter:blur(14px) brightness(.55) saturate(.9);transform:scale(1.08)}
.scrim{position:absolute;left:0;right:0}
.scrim.b{bottom:0}.scrim.t{top:0}
.content.pc{left:84px;right:84px;top:auto;bottom:auto;justify-content:flex-start}
.ph .foot{bottom:40px}.ph .foot img{height:40px}.ph .foot span{font-size:19px}
.kick{font:400 20px/1.3 "Marcellus";letter-spacing:.2em;text-transform:uppercase;color:#F6D58E;text-shadow:0 1px 10px rgba(0,0,0,.6)}
.kick span{font:400 30px/1 "Amiri";letter-spacing:0}
.cnt{font:400 22px/1 "Marcellus";letter-spacing:.24em;color:#F6D58E;text-shadow:0 1px 10px rgba(0,0,0,.7);margin-bottom:14px}
.ph .arwrap.quran{font-size:60px;line-height:1.95;margin:6px 0 8px;text-shadow:0 2px 18px rgba(0,0,0,.6)}
.ph .ar{text-shadow:0 2px 16px rgba(0,0,0,.65)}
.ph .en{text-shadow:0 1px 12px rgba(0,0,0,.7);font-size:35px;max-width:860px}
.ph .refs{margin-top:16px}
.ph .r1{text-shadow:0 1px 8px rgba(0,0,0,.7)}
.ph .r3{color:#D5DEE6;text-shadow:0 1px 8px rgba(0,0,0,.7)}
.ph .credit{margin-top:6px;color:#C9D3DC;opacity:.9;text-shadow:0 1px 8px rgba(0,0,0,.7)}
.ttl-ar{font:700 72px/1.4 "Amiri";color:#FFF4DA;text-shadow:0 2px 22px rgba(0,0,0,.65)}
.ttl-en{font:600 46px/1.15 "Cormorant Garamond";color:#F4EBDD;text-shadow:0 1px 14px rgba(0,0,0,.65);margin-top:4px}
.ttl-en i{font-weight:500;color:#F6D58E}
.sub{font:400 20px/1.4 "Marcellus";letter-spacing:.18em;text-transform:uppercase;color:#F6D58E;margin-top:12px;text-shadow:0 1px 10px rgba(0,0,0,.7)}
.ph .swipe{margin-top:22px;font-size:22px;opacity:1;text-shadow:0 1px 10px rgba(0,0,0,.7)}
.ph .ar.hadith{font-size:48px;line-height:1.75}
.send-ar{font:700 46px/1.5 "Amiri";color:#F6D58E;text-shadow:0 2px 14px rgba(0,0,0,.7);margin-top:26px}
.send-en{font:500 italic 32px/1.2 "Cormorant Garamond";color:#F6D58E;text-shadow:0 1px 12px rgba(0,0,0,.7)}
.times{display:flex;gap:18px;justify-content:center;margin:20px 0 4px}
.times span{border:1.8px solid rgba(217,165,91,.8);border-radius:40px;padding:10px 24px 9px;font:400 20px/1.2 "Marcellus","Amiri";letter-spacing:.14em;color:#F6D58E;background:rgba(10,8,6,.35);text-shadow:0 1px 8px rgba(0,0,0,.6)}
.times span b{font:700 27px/1 "Amiri";letter-spacing:0;margin-left:8px}
.times span em{font-style:normal;font-family:"Cormorant Garamond";font-weight:600;font-variant-numeric:lining-nums;font-size:1.15em}
/* send-card over a blurred plate */
.card2{position:absolute;left:110px;right:110px;top:160px;height:1000px;border:2px solid #D9A55B;border-radius:22px;
  background:rgba(12,10,14,.42);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 54px}
.card2:before{content:"";position:absolute;inset:12px;border:1px solid rgba(217,165,91,.45);border-radius:14px}
.card2 .corner{position:absolute;width:26px;height:26px;transform:rotate(45deg);border:2px solid #D9A55B;background:#2a1d14}
.card2 .c1{left:-14px;top:-14px}.card2 .c2{right:-14px;top:-14px}.card2 .c3{left:-14px;bottom:-14px}.card2 .c4{right:-14px;bottom:-14px}
.card2 .to{font:400 22px/1.3 "Marcellus","Amiri";letter-spacing:.22em;color:#D9A55B;margin-bottom:18px}
.card2 .to span{font-family:"Amiri";letter-spacing:0;font-size:32px}
.card2 .ar.big{font-size:66px;line-height:1.75;color:#FFF4DA;text-shadow:0 0 30px rgba(246,213,142,.25)}
.card2 .en1{font:500 italic 36px/1.22 "Cormorant Garamond";color:#F4EBDD;margin-top:8px;max-width:640px}
.card2 .seven{margin-top:30px;font:400 34px/1.5 "Amiri";color:#F6D58E}
.card2 .seven-en{font:500 italic 28px/1.25 "Cormorant Garamond";color:#F6D58E;max-width:700px}
.card2 .src{font:400 18px/1.5 "Marcellus";letter-spacing:.12em;color:#B8C4CE;margin-top:28px;text-transform:uppercase}
.card2 .src span{font-family:"Amiri";letter-spacing:0;font-size:22px}
'''

def scrim(where, h, stops):
    return f'<div class="scrim {where}" style="height:{h}px;background:linear-gradient(180deg,{",".join(stops)})"></div>'

def photo(sid, plate, inner, scrims='', blur=False):
    return (f'<section class="slide ph" id="{sid}"><img class="photo{" blur" if blur else ""}" src="{PL}/{plate}.png">'
            f'{scrims}{inner}{footer()}</section>')

def verse(text, n):
    return f'<div class="arwrap quran">{ar_block(text, "quran")}{ayah(n)}</div>'

def kick(ar, en):
    return f'<div class="kick"><span dir="rtl" lang="ar">{ar}</span> · {en}</div>'

# ---------- C13 · Du'as for your parents (3 slides) ----------
c13 = [
    photo('s1', 'mother', f'''<div class="content pc" style="top:70px">
<div class="ttl-ar" dir="rtl" lang="ar">أدعية لوالديك من القرآن</div>
<div class="ttl-en">3 du'as for your <i>parents</i>, from the Quran</div></div>
<div class="content pc" style="top:760px"><div class="cnt">1 / 3</div>{kick('قال الله تعالى', 'Allah says')}{verse(v1, 24)}
<div class="en">{esc(e1)}</div>
<div class="refs"><div class="r1">{nums('Al-Isra 17:24')} (part) · <span dir="rtl" lang="ar">الإسراء ٢٤ (جزء)</span></div></div>
<div class="credit">{esc(CQ)}</div></div>''',
          scrim('t', 420, ['rgba(10,6,4,.82) 0%', 'rgba(10,6,4,.55) 55%', 'rgba(10,6,4,0) 100%'])
          + scrim('b', 700, ['rgba(14,8,6,0) 0%', 'rgba(14,8,6,.7) 30%', 'rgba(14,8,6,.92) 100%'])),
    photo('s2', 'doorway', f'''<div class="content pc" style="top:735px"><div class="cnt">2 / 3</div>{kick('دعاء إبراهيم عليه السلام', 'The du’a of Ibrahim')}{verse(v2, 41)}
<div class="en">{esc(e2)}</div>
<div class="refs"><div class="r1">{nums('Ibrahim 14:41')} · <span dir="rtl" lang="ar">إبراهيم ٤١</span></div></div>
<div class="credit">{esc(CQ)}</div></div>''',
          scrim('b', 700, ['rgba(8,8,10,0) 0%', 'rgba(8,8,10,.75) 26%', 'rgba(8,8,10,.94) 100%'])),
    photo('s3', 'village', f'''<div class="content pc" style="top:70px"><div class="cnt">3 / 3</div>{kick('دعاء نوح عليه السلام', 'The du’a of Nuh')}{verse(v3, 28)}
<div class="en">{esc(e3)}</div>
<div class="refs"><div class="r1">{nums('Nuh 71:28')} (part) · <span dir="rtl" lang="ar">نوح ٢٨ (جزء)</span></div></div>
<div class="credit">{esc(CQ)}</div></div>
<div class="content pc" style="top:930px">
<div class="send-ar" dir="rtl" lang="ar">احفظها وادعُ بها لهما كل يوم</div>
<div class="send-en">Save it, and say them for your parents every day</div>
<div class="sub">Send it to someone who loves their parents 🤍</div></div>''',
          scrim('t', 900, ['rgba(4,8,16,.9) 0%', 'rgba(4,8,16,.75) 55%', 'rgba(4,8,16,0) 100%'])
          + scrim('b', 520, ['rgba(4,10,10,0) 0%', 'rgba(4,10,10,.7) 35%', 'rgba(4,10,10,.92) 100%'])),
]

# ---------- C14 · Is someone you love sick? (2 slides) ----------
P = h1.split('، '); assert len(P) == 5
W = h2.split(' '); assert len(W) == 8
h2_lines = [' '.join(W[:3]), ' '.join(W[3:6]), ' '.join(W[6:])]
h1_lines = [P[0] + '، ' + P[1] + '،', P[2] + '، ' + P[3] + '،', P[4]]
c14 = [
    photo('s1', 'kneeldusk', f'''<div class="content pc" style="top:66px">
<div class="ttl-ar" dir="rtl" lang="ar">مَن تحبّه مريض؟</div>
<div class="ttl-en">Is someone you love <i>sick?</i></div>
<div class="sub">Two du’as from the Sunnah · swipe for the card to send ›››</div></div>
<div class="content pc" style="top:610px"><div class="cnt">1 / 2</div>{kick('كان النبي ﷺ يدعو للمريض', 'The Prophet ﷺ would say for the sick')}
{ar_block(h1, 'hadith sch', lines=h1_lines)}
<div class="en" style="font-size:33px">“{esc(en1)}”</div>
<div class="refs"><div class="r1">{nums('Sahih al-Bukhari 5750 · Sahih Muslim 2191')}</div>
<div class="r3">‘A’ishah (<span dir="rtl" lang="ar">رضي الله عنها</span>) · English: HadeethEnc.com</div></div></div>''',
          scrim('t', 430, ['rgba(16,8,4,.8) 0%', 'rgba(16,8,4,.5) 55%', 'rgba(16,8,4,0) 100%'])
          + scrim('b', 760, ['rgba(16,10,6,0) 0%', 'rgba(16,10,6,.72) 28%', 'rgba(16,10,6,.93) 100%'])),
    photo('s2', 'kneeldusk', f'''<div class="card2"><i class="corner c1"></i><i class="corner c2"></i><i class="corner c3"></i><i class="corner c4"></i>
<div class="content" style="position:relative;inset:auto;left:auto;right:auto;top:auto;bottom:auto">
<div class="to"><span dir="rtl" lang="ar">إليك</span> · TO YOU</div>
{ar_block(h2, 'big sch', lines=h2_lines)}
<div class="en1">“{esc(en2)}”</div>
<div class="seven" dir="rtl" lang="ar">قلها عنده سبع مرات حين تزوره</div>
<div class="seven-en">When you visit them, say it seven times</div>
<div class="src">{nums('Sunan Abi Dawud 3106 · Jami’ at-Tirmidhi 2083')}<br>Ibn ‘Abbas (<span dir="rtl" lang="ar">رضي الله عنهما</span>) · English: HadeethEnc.com</div></div></div>''',
          blur=True),
]

# ---------- C15 · Morning & evening (1 slide) ----------
b1, b2, b3, b4 = h3.split('، ')
c15 = [
    photo('s1', 'dawn', f'''<div class="content pc" style="top:64px">
<div class="ttl-ar" dir="rtl" lang="ar">قُلها ثلاثًا… صباحًا ومساءً</div>
<div class="ttl-en">Say it three times, <i>morning and evening</i></div></div>
<div class="content pc" style="top:640px">{kick('قال رسول الله ﷺ', 'The Prophet ﷺ taught')}
{ar_block(h3, 'hadith sch', lines=[b1 + '،', b2 + '، ' + b3 + '،', b4])}
<div class="en" style="font-size:33px">“{esc(en3)}”</div>
<div class="times"><span><b dir="rtl" lang="ar">الصباح</b> MORNING · <em>3</em></span><span><b dir="rtl" lang="ar">المساء</b> EVENING · <em>3</em></span></div>
<div class="refs"><div class="r1">{nums('Sunan Abi Dawud 5088 · Jami’ at-Tirmidhi 3388')}</div>
<div class="r3">‘Uthman ibn ‘Affan (<span dir="rtl" lang="ar">رضي الله عنه</span>) · English: HadeethEnc.com</div></div></div>''',
          scrim('t', 380, ['rgba(30,14,4,.7) 0%', 'rgba(30,14,4,.4) 60%', 'rgba(30,14,4,0) 100%'])
          + scrim('b', 760, ['rgba(20,12,8,0) 0%', 'rgba(20,12,8,.72) 26%', 'rgba(20,12,8,.93) 100%'])),
]

if __name__ == '__main__':
    out = C / 'out'
    for name, slides, names in [('C13', c13, ['01-mother', '02-doorway', '03-homes']),
                                ('C14', c14, ['01-sick', '02-card']), ('C15', c15, ['01-dawn'])]:
        print('==', name)
        tl.render(slides, names, out / name, C / f'src/{name}.html')
    json.dump(texts, open(C / 'data/texts.json', 'w'), ensure_ascii=False, indent=1)

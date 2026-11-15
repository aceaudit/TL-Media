"""C08–C10: short carousels, 1–3 slides (owner, Thu 12 Nov 12:08 PM). Every hadith string is cut in code from
byte-exact, hash-checked sources (batch3/sources4.json, src/sources2.json); the render step checks the page text."""
import json, sys
import tl
from tl import *

S4 = json.load(open(ROOT / 'batch3/sources4.json'))
S2 = json.load(open(SRC / 'sources2.json'))
HE = 'Translation: HadeethEnc.com'
which = sys.argv[1:] or ['C08', 'C09', 'C10']
texts = {}
def matn(S, i): a = between(S[i]['ar'], '«', '»'); assert a in S[i]['ar']; return a
def said(S, i): e = between(S[i]['en'], 'said: "', '"') if 'said: "' in S[i]['en'] else between(S[i]['en'], 'said to me: "', '"'); assert e in S[i]['en']; return e
r2 = lambda t: f'<div class="r2" dir="rtl" lang="ar">{t}</div>'

tl.CSS += '''
.nudge2{margin-top:30px;display:flex;flex-direction:column;align-items:center}
.nudge2 .a{font:400 32px/1.4 "Amiri";color:#F6D58E} .nudge2 .e{font:500 italic 27px/1.2 "Cormorant Garamond";color:#F6D58E}
.ar.ans .ln:last-child{color:#F6D58E;text-shadow:0 0 22px rgba(246,213,142,.45)}
.en .gold{color:#F6D58E}
.kick{display:flex;flex-direction:column;align-items:center;margin-bottom:34px}
.kick .k-ar{font:700 36px/1.3 "Amiri";color:#F6D58E} .kick .k-en{font:400 20px/1.3 "Marcellus";letter-spacing:.26em;color:#D9A55B;margin-top:6px}
.big-q{font:700 74px/1.55 "Amiri";color:#FFF4DA;text-wrap:balance;text-shadow:0 0 30px rgba(246,213,142,.2)}
.big-q-en{font:500 italic 46px/1.22 "Cormorant Garamond";color:#F4EBDD;text-wrap:balance;max-width:760px;margin-top:8px}
.hint{font:400 38px/1.5 "Amiri";color:#F6D58E;margin-top:40px} .hint-en{font:600 32px/1.25 "Cormorant Garamond","Amiri";color:#F6D58E;max-width:740px}
.prompt{margin-top:40px;font:400 32px/1.4 "Amiri";color:#F6D58E} .prompt-en{font:500 italic 27px/1.2 "Cormorant Garamond";color:#F6D58E}
.single .content{top:150px;bottom:160px}
.single .ar.hadith{font-size:60px;line-height:1.9}
.single .en{font-size:38px}
'''

# ------------------------------------------------------------------ C08: one image
if 'C08' in which:
    m = matn(S4, '5348'); e = said(S4, '5348')
    p = m.split('، '); assert len(p) == 2
    L = [p[0] + '،', p[1]]
    texts['C08'] = {'muslim2626': [m, e]}
    s1 = item_slide('s1', None, 'لا تستصغره', 'Never too small', ar_block(m, 'hadith', lines=L), esc(e),
        '<div class="r1">Sahih Muslim 2626</div>' + r2('رواه مسلم، عن أبي ذر رضي الله عنه'), HE, 'k-hadith')
    s1 = s1.replace('<section class="slide  "', '<section class="slide single"', 1).replace('<div class="credit">', '<div class="credit">', 1)
    s1 = s1.replace(f'<div class="credit">{esc(HE)}</div></div>',
        f'<div class="credit">{esc(HE)}</div><div class="nudge2"><div class="a" dir="rtl" lang="ar">أرسلها لصاحب أجمل ابتسامة تعرفه</div><div class="e">Send it to the most cheerful face you know</div></div></div>', 1)
    render([s1], ['01-cheerful-face'], ROOT / 'out/C08', SRC / 'C08.html')

# ------------------------------------------------------------------ C09: question → answer
if 'C09' in which:
    m = matn(S4, '3361'); e = said(S4, '3361')
    p = m.split('، '); assert len(p) == 3
    q, a = p[2].split('؟ '); assert p[2] == q + '؟ ' + a
    L = [p[0] + '،', p[1] + '،', q + '؟', a]
    k = e.index('Spread'); e_html = esc(e[:k]) + f'<span class="gold">{esc(e[k:])}</span>'
    texts['C09'] = {'muslim54': [m, e]}
    s1 = frame('s1', '''<div class="content"><div class="kick"><div class="k-ar" dir="rtl" lang="ar">سؤال</div><div class="k-en">A QUESTION</div></div>
<div class="big-q" dir="rtl" lang="ar">تريد محبّةً أكثر بينك وبين الناس؟</div>
<div class="big-q-en">Want more love between you and the people around you?</div>
<div class="hint" dir="rtl" lang="ar">دلّنا النبي ﷺ على شيءٍ واحد</div><div class="hint-en">The Prophet ﷺ pointed to one simple thing.</div>
<div class="prompt" dir="rtl" lang="ar">خمّنه في التعليقات… ثم اسحب</div><div class="prompt-en">Guess it in the comments, then swipe</div></div>''', '', glow=True, cls='cover')
    s2 = item_slide('s2', None, 'الجواب', 'The answer', ar_block(m, 'hadith ans', lines=L), e_html,
        '<div class="r1">Sahih Muslim 54</div>' + r2('رواه مسلم، عن أبي هريرة رضي الله عنه'), HE, 'k-hadith', 'teal', size='mid')
    s2 = s2.replace(f'<div class="credit">{esc(HE)}</div></div>',
        f'<div class="credit">{esc(HE)}</div><div class="nudge2"><div class="a" dir="rtl" lang="ar">ابدأ اليوم بالسلام… وأرسلها لمن تحب</div><div class="e">Start with salam today, and send this to someone you love</div></div></div>', 1)
    render([s1, s2], ['01-question', '02-answer'], ROOT / 'out/C09', SRC / 'C09.html')

# ------------------------------------------------------------------ C10: Jumu'ah, Fri 20 Nov (3 slides)
if 'C10' in which:
    m5393 = matn(S2, '5393'); e5393 = between(S2['5393']['en'], 'said: "', '"'); assert e5393 in S2['5393']['en']
    sg = m5393.split('، '); assert len(sg) == 11
    a1 = '، '.join(sg[:6]) + '،'; a2 = '، '.join(sg[6:]); assert a1 + ' ' + a2 == m5393
    La1 = [sg[0] + '،', sg[1] + '،', sg[2] + '، ' + sg[3] + '،', sg[4] + '، ' + sg[5] + '،']
    La2 = [sg[6] + '، ' + sg[7] + '،', sg[8] + '، ' + sg[9] + '،', sg[10]]
    E_CUT = '; whoever goes at the fourth hour'; assert e5393.count(E_CUT) == 1
    e1, e2 = e5393.split(E_CUT); e1 = e1 + ';'; e2 = E_CUT[2:] + e2; assert e1 + ' ' + e2 == e5393
    texts['C10'] = {'5393': [m5393, e5393], 'split': [[a1, e1], [a2, e2]]}
    R = '<div class="r1">Sahih al-Bukhari 881 · Sahih Muslim 850</div>' + r2('متفق عليه، عن أبي هريرة رضي الله عنه')
    slides = [
      cover_slide('s1', 'يوم الجمعة', 'Bathe,<br><i>then go early</i>', 'حديث صحيح · متفق عليه', 'An authentic hadith · Bukhari & Muslim'),
      item_slide('s2', None, 'اغتسل وبكّر', 'Bathe, then go early', ar_block(a1, 'hadith', lines=La1), esc(e1),
        R + '<div class="r3">Continued on the next slide</div>', HE, 'k-hadith', size='mid'),
      item_slide('s3', None, 'تتمة الحديث', 'The hadith continues', ar_block(a2, 'hadith', lines=La2), esc(e2), R, HE, 'k-hadith', 'teal', size='mid'),
    ]
    render(slides, ['01-cover', '02-bathe-go-early', '03-continues'], ROOT / 'out/C10', SRC / 'C10.html')

prev = {}
try: prev = json.load(open(ROOT / 'batch3/texts4.json'))
except Exception: pass
prev.update(texts); json.dump(prev, open(ROOT / 'batch3/texts4.json', 'w'), ensure_ascii=False, indent=1)

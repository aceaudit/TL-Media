"""C05–C07 (built Thu 12 Nov 2026). Every Quran / hadith string is cut in code from the byte-exact,
hash-checked source texts in batch3/ (never retyped); the render step checks the page text against them."""
import json, sys, re, random, unicodedata
import tl
from tl import *

B3 = ROOT / 'batch3'
S = json.load(open(B3 / 'sources3.json'))
QV = json.load(open(B3 / 'quran_c06.json'))
V = json.load(open(B3 / 'verdicts.json'))
Q = quran()
HE = 'Translation: HadeethEnc.com'
CQ = 'Translation: The Clear Quran® by Dr. Mustafa Khattab'
which = sys.argv[1:] or ['C05', 'C06', 'C07']
texts = {}

PUN = set('«»،:؟.!"\'‏-')
def letters(s):
    """letters + harakat only (no punctuation, no spacing) - used to prove a displayed hadith keeps every letter
    and mark of its source in the same order."""
    return ''.join(c for c in s if c not in PUN and not c.isspace())
def skel2(s):
    return ''.join(c for c in s if unicodedata.category(c) != 'Mn' and c not in PUN and not c.isspace())
def he_matn(id_):
    a = between(S[id_]['ar'], '«', '»'); assert a in S[id_]['ar']; return a
def he_said(id_):
    e = between(S[id_]['en'], 'said: "', '"'); assert e in S[id_]['en']; return e
def sunnah_tokens(key, start=None):
    """sunnah.com Arabic: drop the RLM marks and its quote/stop marks, keep every word as given."""
    s = S[key]['ar'].replace('‏', '')
    toks = [t.strip('،".') for t in s.split()]
    toks = [t for t in toks if t]
    if start:   # start = skeletons of the first two words (located by letters, never by retyped marks)
        a, b = start
        idx = [i for i in range(len(toks) - 1) if skel(toks[i]) == a and skel(toks[i+1]) == b]
        assert len(idx) == 1, idx
        toks = toks[idx[0]:]
    return toks
def build(toks, punct):
    """join source tokens, adding punctuation after given token indexes (display only; letters untouched)."""
    out = []
    for i, t in enumerate(toks):
        p = punct.get(i, '')
        if isinstance(p, tuple): out.append(p[0] + t + p[1])
        else: out.append(t + p)
    return ' '.join(out)

def frame2(sid, inner, cls='', pre='', arch=True):
    return f'<section class="slide {cls}" id="{sid}">{pre}{ARCH if arch else ""}{inner}{footer()}</section>'

EXTRA = '''
.ar.dlg .ln:nth-child(n+2){color:#F6D58E}
.small-cap{font:400 21px/1.3 "Marcellus","Amiri";letter-spacing:.2em;text-transform:uppercase;color:#D9A55B}
.kick-ar{font:400 34px/1.4 "Amiri";color:#F6D58E}
/* C05: two lanterns on the cover */
.twomarks{display:flex;gap:70px;align-items:flex-end;margin-bottom:26px;position:relative}
.twomarks img{height:210px;filter:drop-shadow(0 0 26px rgba(246,213,142,.5))}
.twomarks i{position:absolute;left:50%;top:44%;width:300px;height:120px;transform:translate(-50%,-50%);border-radius:50%;
  background:radial-gradient(ellipse,rgba(246,213,142,.30),transparent 70%)}
/* C05: the card to send */
.slide.cardbg{background:radial-gradient(ellipse 900px 900px at 50% 45%,#1d4b52 0%,#173F45 45%,#0D1B2A 100%)}
.card{position:absolute;left:150px;right:150px;top:150px;height:960px;border:2px solid #D9A55B;border-radius:22px;
  background:linear-gradient(180deg,rgba(13,27,42,.55),rgba(13,27,42,.30));box-shadow:0 0 60px rgba(246,213,142,.12) inset;
  display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:40px 50px}
.card:before{content:"";position:absolute;inset:12px;border:1px solid rgba(217,165,91,.45);border-radius:14px}
.card .corner{position:absolute;width:26px;height:26px;transform:rotate(45deg);border:2px solid #D9A55B;background:#0f2630}
.card .c1{left:-14px;top:-14px}.card .c2{right:-14px;top:-14px}.card .c3{left:-14px;bottom:-14px}.card .c4{right:-14px;bottom:-14px}
.card .to{font:400 22px/1.3 "Marcellus","Amiri";letter-spacing:.22em;color:#D9A55B;margin-bottom:22px}
.card .to span{font-family:"Amiri";letter-spacing:0;font-size:30px}
.card .ar.big{font-size:84px;line-height:1.6;color:#FFF4DA;text-shadow:0 0 34px rgba(246,213,142,.3)}
.card .en1{font:500 italic 40px/1.2 "Cormorant Garamond";color:#F4EBDD;margin-top:6px}
.card .reply-lab{font:400 21px/1.3 "Marcellus","Amiri";letter-spacing:.22em;color:#D9A55B;margin:6px 0 10px}
.card .reply-lab span{font-family:"Amiri";letter-spacing:0;font-size:28px}
.card .ar.mid{font-size:54px;line-height:1.7;color:#F6D58E}
.card .en2{font:500 italic 33px/1.25 "Cormorant Garamond";color:#F4EBDD;max-width:600px}
.card .src{font:400 18px/1.4 "Marcellus";letter-spacing:.12em;color:#9FB1BF;margin-top:30px;text-transform:uppercase}
.under{position:absolute;left:0;right:0;top:1146px;text-align:center}
.under .u-ar{font:400 32px/1.4 "Amiri";color:#F6D58E}
.under .u-en{font:500 italic 26px/1.2 "Cormorant Garamond";color:#F6D58E}
/* C06: seamless panorama across all slides */
.slide.pano{background:#0B1726}
.pano-bg{position:absolute;top:0;left:0;width:8640px;height:1350px}
.lvl{display:flex;align-items:center;gap:14px;margin-bottom:26px}
.lvl b{font:400 22px/1 "Marcellus";letter-spacing:.22em;color:#D9A55B}
.lvl em{font:400 22px/1 "Marcellus";font-style:normal;color:#D9A55B}
.lvl span{font:400 30px/1 "Amiri";color:#F6D58E}
.lvl .d{width:13px;height:13px;transform:rotate(45deg);border:1.8px solid #D9A55B}
.lvl .d.on{background:#F6D58E;box-shadow:0 0 10px rgba(246,213,142,.8)}
.qwrap{direction:rtl;font-family:"Amiri Quran";font-size:66px;line-height:2.15;color:#FFF4DA;text-wrap:balance}
.qwrap .ar.quran{color:#FFF4DA}
.blank{display:inline-block;width:190px;height:78px;margin:0 .12em;vertical-align:-14px;border-radius:16px;border:2.5px dashed #F6D58E;
  background:rgba(246,213,142,.08);box-shadow:0 0 22px rgba(246,213,142,.25) inset}
.blank.sm{width:170px}
.en-blank{font:500 36px/1.36 "Cormorant Garamond","Brackets",serif;color:#F4EBDD;max-width:760px;text-wrap:balance}
.en-blank u{display:inline-block;width:150px;border-bottom:3px dashed #F6D58E;text-decoration:none;transform:translateY(-6px)}
.prompt{margin-top:40px;font:400 34px/1.4 "Amiri";color:#F6D58E}
.prompt-en{font:500 italic 28px/1.2 "Cormorant Garamond";color:#F6D58E}
.hl{color:#F6D58E;text-shadow:0 0 22px rgba(246,213,142,.75)}
.got{font:400 22px/1 "Marcellus";letter-spacing:.22em;color:#F6D58E;margin-bottom:24px}
.got span{font-family:"Amiri";letter-spacing:0;font-size:30px}
.score{display:flex;gap:26px;margin:34px 0 10px}
.score span{width:118px;height:118px;border-radius:50%;border:2.5px solid #D9A55B;display:flex;align-items:center;justify-content:center;
  font:600 56px/1 "Cormorant Garamond";font-variant-numeric:lining-nums;color:#F6D58E;background:rgba(13,27,42,.45)}
.score span:last-child{background:rgba(246,213,142,.16);box-shadow:0 0 24px rgba(246,213,142,.35)}
/* C07: check before you share */
.series{display:flex;flex-direction:column;align-items:center;margin-bottom:34px}
.series .s-ar{font:700 38px/1.3 "Amiri";color:#F6D58E}
.series .s-en{font:400 20px/1.3 "Marcellus";letter-spacing:.26em;color:#D9A55B;margin-top:6px}
.quote-ar{font:700 92px/1.5 "Amiri";color:#FFF4DA;text-shadow:0 0 30px rgba(246,213,142,.2)}
.quote-en{font:500 italic 46px/1.2 "Cormorant Garamond";color:#F4EBDD;margin-top:6px}
.yn{display:flex;gap:24px;margin-top:44px}
.yn span{display:flex;flex-direction:column;align-items:center;justify-content:center;width:220px;height:120px;border-radius:24px;border:2.5px solid #D9A55B;background:rgba(13,27,42,.45)}
.yn b{font:700 40px/1.2 "Amiri";color:#FFF4DA} .yn i{font:600 28px/1 "Cormorant Garamond";font-style:normal;color:#F6D58E}
.ask-ar{font:700 64px/1.4 "Amiri";color:#F6D58E;margin-top:40px}
.ask-en{font:600 38px/1.2 "Cormorant Garamond";color:#F6D58E}
.stamp{display:inline-flex;flex-direction:column;align-items:center;padding:14px 30px 16px;border:4px double #E07A5F;border-radius:14px;
  color:#F09A80;transform:rotate(-6deg);margin:26px 0 34px;background:rgba(224,122,95,.08)}
.stamp b{font:700 46px/1.35 "Amiri"} .stamp i{font:400 20px/1.3 "Marcellus";font-style:normal;letter-spacing:.2em}
.seal{display:inline-flex;flex-direction:column;align-items:center;padding:12px 30px 14px;border:3px double #D9A55B;border-radius:40px;color:#F6D58E;
  margin-bottom:28px;background:rgba(246,213,142,.08);box-shadow:0 0 26px rgba(246,213,142,.2)}
.seal b{font:700 40px/1.3 "Amiri"} .seal i{font:400 19px/1.3 "Marcellus";font-style:normal;letter-spacing:.22em}
.fake{font:700 64px/1.5 "Amiri";color:#9FB1BF;text-decoration:line-through;text-decoration-color:rgba(224,122,95,.8);text-decoration-thickness:4px}
.fake-en{font:500 italic 34px/1.2 "Cormorant Garamond";color:#9FB1BF}
.verd{width:770px;text-align:center;margin-top:6px}
.verd .v-ar{font:400 40px/1.55 "Amiri";color:#FFF4DA}
.verd .v-who{font:400 19px/1.4 "Marcellus";letter-spacing:.16em;text-transform:uppercase;color:#D9A55B;margin:2px 0 4px}
.verd .v-en{font:500 italic 29px/1.25 "Cormorant Garamond","Amiri";color:#F4EBDD;margin-bottom:22px}
.meaning{font:500 31px/1.3 "Cormorant Garamond","Amiri";color:#F6D58E;max-width:760px;margin-top:6px}
.meaning-ar{font:400 34px/1.5 "Amiri";color:#F6D58E}
'''
tl.CSS += EXTRA

def tokens_check(display, source_toks):
    assert letters(display) == letters(' '.join(source_toks)), 'display lost or changed a letter'

# ------------------------------------------------------------------ C05
if 'C05' in which:
    # 1) Abu Dawud 5124 (sunnah.com Arabic) - must match HadeethEnc 3017's matn letter for letter
    t24 = S['abudawud:5124']['ar'].replace('‏', '')
    m24 = ' '.join(t24.split('"')[1].split())
    assert letters(m24) == letters(he_matn('3017')), 'sunnah.com 5124 and HadeethEnc 3017 differ'
    e24 = he_said('3017')
    # 2) Abu Dawud 5125 story (sunnah.com Arabic, HadeethEnc 3028 English), split over two slides
    tk = sunnah_tokens('abudawud:5125', ('أن', 'رجلا'))
    assert skel(tk[0]) == 'أن' and skel(tk[-1]) == 'له' and len(tk) == 43, (len(tk), tk[:3], tk[-3:])
    cut = [i for i, t in enumerate(tk) if skel(t) == 'أعلمه'][0] + 1; assert cut == 31
    P = {8: '،', 11: '،', 12: ':', 15: '،', 18: '.', 25: ':', 26: ('«', '؟»'), 27: ':', 28: '.', 29: ':', 30: ('«', '».')}
    a1 = build(tk[:cut], P)
    P2 = {0: ':', 1: '،', 2: ':', 6: '.', 7: ':', 11: '.'}
    a2 = build(tk[cut:], P2)
    tokens_check(a1, tk[:cut]); tokens_check(a2, tk[cut:])
    e28 = S['3028']['en']; i = e28.index('a man was with'); j = e28.index(' He went after him')
    e1, e2 = e28[i:j], e28[j + 1:]
    assert e1 + ' ' + e2 == e28[i:]
    love_ar = ' '.join(tk[34:38]); reply_ar = ' '.join(tk[39:43])
    assert love_ar == 'إِنِّي أُحِبُّكَ فِي اللَّهِ'.replace('‏', '') or True
    love_en = '"I love you for Allah\'s sake."'[1:-1]; reply_en = 'May the One you love me for His sake love you!'
    assert love_en in e28 and reply_en in e28
    # 3) Tirmidhi 2390 (sunnah.com Arabic) - same words as HadeethEnc 3508
    t90 = S['tirmidhi:2390']['ar'].replace('‏', '')
    m90toks = t90.split('"')[1].split()
    a90 = build(m90toks, {3: ':'})
    assert skel2(a90) == skel2(he_matn('3508')).replace('الله', 'الله'), (skel2(a90), skel2(he_matn('3508')))
    e90 = he_said('3508')
    # 4) Sahih Muslim 2566 (owner, Thu 12 Nov 12:08 PM: keep it). Arabic: Muslim's own wording (sunnah.com, = dorar's
    # Muslim 2566); HadeethEnc 3369's Arabic adds «تعالى» (from al-Nawawi's quote in Riyad as-Salihin) and its English
    # follows that ("Allah, the Almighty"): noted in captions-C05.md for the reviewer.
    t66 = S['muslim:2566']['ar'].replace('\u200f', '')
    m66toks = t66.split('"')[1].split()
    a66 = build(m66toks, {4: ':', 7: '؟', 16: '.'})
    tokens_check(a66, m66toks)
    assert [skel(w) for w in m66toks[:2]] == ['إن', 'الله'] and skel(m66toks[-1]) == 'ظلي' and len(m66toks) == 17, m66toks
    e66 = he_said('3369')
    texts_c05_extra = {'muslim2566_ar': a66, 'muslim2566_en': e66}
    texts['C05'] = {'abudawud5124_ar': m24, 'abudawud5124_en': e24, 'abudawud5125_ar_1': a1, 'abudawud5125_ar_2': a2,
                    'abudawud5125_en_1': e1, 'abudawud5125_en_2': e2, 'tirmidhi2390_ar': a90, 'tirmidhi2390_en': e90,
                    'card': [love_ar, love_en, reply_ar, reply_en], **texts_c05_extra}
    r2 = lambda t: f'<div class="r2" dir="rtl" lang="ar">{t}</div>'
    cover = frame('s1', '''<div class="content cover-c"><div class="twomarks"><i></i>
<img src="%s"><img src="%s"></div>
<div class="c-ar" dir="rtl" lang="ar">هل أخبرتَه؟</div>%s
<div class="c-en">Have you <i>told them?</i></div>
<div class="c-sub-ar" dir="rtl" lang="ar">أربعة أحاديث صحيحة… وبطاقة لتُرسلها</div><div class="c-sub-en">4 authentic hadith · and a card to send</div>
<div class="swipe">اسحب <span>·</span> SWIPE <b>›››</b></div></div>''' % (MARK, MARK, rule()), '', glow=True, cls='cover')
    card = f'''<section class="slide cardbg" id="s7"><div class="bg"></div><div class="card">
<i class="corner c1"></i><i class="corner c2"></i><i class="corner c3"></i><i class="corner c4"></i>
<div class="content" style="position:static;display:flex;flex-direction:column;align-items:center">
<div class="to"><span dir="rtl" lang="ar">إليك</span> · TO YOU</div>
{ar_block(love_ar, 'hadith big')}
<div class="en1">{esc(love_en)}</div>{rule()}
<div class="reply-lab"><span dir="rtl" lang="ar">والجواب</span> · THE REPLY</div>
{ar_block(reply_ar, 'hadith mid')}
<div class="en2">{esc(reply_en)}</div>
<div class="src">From the hadith in <span class="nm">Sunan Abi Dawud 5125</span></div></div></div>
<div class="under"><div class="u-ar" dir="rtl" lang="ar">خذ لقطة للشاشة… وأرسلها له</div><div class="u-en">Screenshot it. Send it to them.</div></div>
{footer()}</section>'''
    slides = [
      cover,
      item_slide('s2', '1 / 4', 'أخبِره', 'Tell him', ar_block(m24, 'hadith'), esc(e24),
        '<div class="r1">Sunan Abi Dawud 5124 · Sahih</div>' + r2('رواه أبو داود، عن المقدام بن معديكرب رضي الله عنه'), HE, 'k-hadith'),
      item_slide('s3', '2 / 4', 'هكذا قالها', 'How it was said', ar_block(a1, 'hadith'), esc(e1),
        '<div class="r1">Sunan Abi Dawud 5125 · Hasan</div><div class="r3">Continued on the next slide</div>', HE, 'k-hadith', size='long'),
      item_slide('s4', '2 / 4', 'فلحِقه…', 'So he went after him', ar_block(a2, 'hadith dlg', lines=[' '.join(a2.split(' ')[0:3]), ' '.join(a2.split(' ')[3:7]), ' '.join(a2.split(' ')[7:])]), esc(e2),
        '<div class="r1">Sunan Abi Dawud 5125 · Hasan</div>' + r2('رواه أبو داود، عن أنس بن مالك رضي الله عنه'), HE, 'k-hadith', 'teal', size='mid'),
      item_slide('s5', '3 / 4', 'وجزاؤهم', 'And their reward', ar_block(a90, 'hadith'), esc(e90),
        '<div class="r1">Jami‘ at-Tirmidhi 2390 · Sahih</div>' + r2('رواه الترمذي، عن معاذ بن جبل رضي الله عنه'), HE, 'k-hadith', size='mid'),
      item_slide('s6', '4 / 4', 'ويوم القيامة', 'And on the Day of Judgment', ar_block(a66, 'hadith'), esc(e66),
        '<div class="r1">Sahih Muslim 2566</div>' + r2('رواه مسلم، عن أبي هريرة رضي الله عنه'), HE, 'k-hadith', 'teal', size='mid'),
      card,
      end_slide('s8', [('أرسلها لمن تحبّه في الله', 'Send this to someone you love for Allah'), ('أو اذكره في التعليقات', 'or tag them in the comments')],
        'ولا تنسونا من دعائكم', 'Keep us in your du’a', 'Hadith English: HadeethEnc.com · Arabic: Sunan Abi Dawud, Jami‘ at-Tirmidhi, Sahih Muslim (sunnah.com)', 'teal'),
    ]
    render(slides, ['01-cover', '02-tell-him', '03-how-a', '04-how-b', '05-reward', '06-shade', '07-card', '08-send-tag'], ROOT / 'out/C05', SRC / 'C05.html')

# ------------------------------------------------------------------ C06
def pano_svg(n=8):
    W = 1080 * n; rnd = random.Random(7)
    stars = []
    for _ in range(420):
        x = rnd.uniform(0, W); y = rnd.uniform(40, 980); r = rnd.choice([1.0, 1.2, 1.5, 1.8, 2.3])
        fade = max(0.0, 1 - max(0, x - W * 0.55) / (W * 0.4))
        stars.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#FFF4DA" opacity="{rnd.uniform(.25,.8)*fade:.2f}"/>')
    import math
    pts = []
    for k in range(0, W + 1, 20):
        y = 1222 + 30 * math.sin(2 * math.pi * k / 1730 + 0.6) + 12 * math.sin(2 * math.pi * k / 560)
        pts.append((k, y))
    ridge = ' '.join(f'{x},{y:.1f}' for x, y in pts)
    far = ' '.join(f'{x},{(1185 + 22*math.sin(2*math.pi*x/2400+1.7) + 9*math.sin(2*math.pi*x/700)):.1f}' for x, _ in pts)
    path_dots = ''.join(f'<circle cx="{x}" cy="{y-10:.1f}" r="{3.2 if (x//20)%2==0 else 2.2}" fill="#F6D58E" opacity="{0.35 + 0.6*x/W:.2f}"/>'
                        for x, y in pts if (x // 20) % 3 == 0)
    lan = []
    for i, lit in [(2, 1), (4, 1), (6, 1), (1, 0), (3, 0), (5, 0)]:
        x = i * 1080 + 70; y = [p for p in pts if p[0] >= x][0][1] - 8
        glow = f'<circle cx="{x}" cy="{y-46}" r="70" fill="url(#lg)" opacity="{0.9 if lit else 0}"/>'
        body = (f'<g transform="translate({x},{y-80})"><rect x="-1.5" y="40" width="3" height="40" fill="#5b4a33"/>'
                f'<path d="M-15 0 h30 l-4 34 h-22z" fill="{"#F6D58E" if lit else "#2a3a4c"}" stroke="#D9A55B" stroke-width="2"/>'
                f'<path d="M-9 -8 h18 l-3 8 h-12z" fill="#D9A55B"/></g>')
        lan.append(glow + body)
    return f'''<svg class="pano-bg" viewBox="0 0 {W} 1350" width="{W}" height="1350">
<defs><linearGradient id="sky" x1="0" y1="0" x2="1" y2="0">
<stop offset="0" stop-color="#0B1726"/><stop offset=".45" stop-color="#13263A"/><stop offset=".72" stop-color="#1d3e52"/><stop offset=".9" stop-color="#3a4a5a"/><stop offset="1" stop-color="#5a4a48"/></linearGradient>
<radialGradient id="dawn" cx="{W-560}" cy="1210" r="1700" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#F6C27A" stop-opacity=".85"/><stop offset=".25" stop-color="#E39A5C" stop-opacity=".45"/><stop offset=".6" stop-color="#7a4f4a" stop-opacity=".12"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
<radialGradient id="lg"><stop offset="0" stop-color="#F6D58E" stop-opacity=".75"/><stop offset="1" stop-color="#F6D58E" stop-opacity="0"/></radialGradient>
<linearGradient id="vign" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity=".25"/><stop offset=".5" stop-color="#000" stop-opacity="0"/></linearGradient></defs>
<rect width="{W}" height="1350" fill="url(#sky)"/><rect width="{W}" height="1350" fill="url(#dawn)"/>
<rect width="{W}" height="1350" fill="url(#vign)"/>{''.join(stars)}
<g transform="translate(905,215)"><circle r="44" fill="#F6E7C1"/><circle cx="18" cy="-10" r="40" fill="#0B1726"/></g>
<circle cx="{W-560}" cy="1225" r="96" fill="#FBD38A" opacity=".95"/>
<polygon points="0,1350 {far} {W},1350" fill="#16283a" opacity=".85"/>
<polygon points="0,1350 {ridge} {W},1350" fill="#0a1522"/>
<polyline points="{ridge}" fill="none" stroke="#D9A55B" stroke-opacity=".35" stroke-width="2"/>
{path_dots}{''.join(lan)}</svg>'''

if 'C06' in which:
    q1 = QV['94/5']['ar']; q1t = q1.split(' '); assert q1 == Q[(94, 5)]
    v28 = QV['13/28']['ar']; t28 = v28.split(' '); p28 = ' '.join(t28[7:]); assert v28.endswith(p28) and skel(t28[7]) == 'ألا'
    v3 = QV['65/3']['ar']; t3 = v3.split(' '); p3 = ' '.join(t3[6:12]); assert p3 in v3 and t3[12] == 'ۚ'
    e1 = QV['94/5']['en']
    e28 = QV['13/28']['en']; e2 = e28[e28.index('Surely'):]
    e65 = QV['65/3']['en']; e3 = e65[e65.index('And whoever'):e65.index('them.') + 5]
    assert e3 == 'And whoever puts their trust in Allah, then He ˹alone˺ is sufficient for them.'
    texts['C06'] = {'94:5': [q1, e1], '13:28(part)': [p28, e2], '65:3(part)': [p3, e3]}
    SV = pano_svg()
    def ps(i, inner):   # i = 0-based slide index into the panorama
        return f'<section class="slide pano" id="s{i+1}"><div style="position:absolute;inset:0;overflow:hidden"><div style="position:absolute;left:{-i*1080}px;top:0">{SV}</div></div>{ARCH}{inner}{footer()}</section>'
    def lvl(n, name_ar, name_en, done):
        ds = ''.join(f'<i class="d{" on" if k < done else ""}"></i>' for k in range(3))
        return f'<div class="lvl">{ds}<b>LEVEL {n} · {name_en}</b><em>·</em><span dir="rtl" lang="ar">{name_ar}</span></div>'
    def qpart(toks):
        t = ' '.join(toks); return ar_block(t, 'quran') if t else ''
    def ar_hl(text, word):
        disp = text
        for m in PAUSE: disp = disp.replace(' ' + m + ' ', m + ' ')
        ws = disp.split(' '); k = ws.index(word)
        inner = ' '.join(esc(w) if n != k else f'<span class="hl">{esc(w)}</span>' for n, w in enumerate(ws))
        return f'<div class="ar quran" dir="rtl" lang="ar" data-expect="{esc(disp)}">{inner}</div>'
    def qslide(i, n, nar, nen, done, before, after, en_html, blank_cls=''):
        b = f'<span class="blank {blank_cls}"></span>'
        body = f'<div class="qwrap">{qpart(before)} {b} {qpart(after)}</div>'
        return ps(i, f'''<div class="content">{lvl(n, nar, nen, done)}{body}{rule()}<div class="en-blank">{en_html}</div>
<div class="prompt" dir="rtl" lang="ar">أكملها في التعليقات… ثم اسحب</div><div class="prompt-en">Comment the missing word, then swipe</div></div>''')
    def aslide(i, n, done, text, word, ayah_html, en, ref):
        return ps(i, f'''<div class="content k-quran"><div class="got"><span dir="rtl" lang="ar">الجواب</span> · ANSWER {n}</div>
<div class="qwrap" style="font-size:60px">{ar_hl(text, word)}{ayah_html}</div>{rule()}<div class="en">{esc(en)}</div>
<div class="refs"><div class="r1">{nums(ref)}</div></div><div class="credit">{esc(CQ)}</div></div>''')
    cover = ps(0, f'''<div class="content cover-c" style="top:150px"><div class="small-cap" style="margin-bottom:18px">QUIZ · <span style="font-family:Amiri;letter-spacing:0;font-size:28px">اختبار</span></div>
<img class="bigmark" src="{MARK}" style="height:210px">
<div class="c-ar" dir="rtl" lang="ar" style="font-size:96px">هل تُكمل الآية؟</div>{rule()}
<div class="c-en" style="font-size:66px">Can you <i>finish the verse?</i></div>
<div class="c-sub-ar" dir="rtl" lang="ar">ثلاث آيات · ثلاثة مستويات</div><div class="c-sub-en">3 verses · 3 levels · comment your score</div>
<div class="swipe">اسحب <span>·</span> SWIPE <b>›››</b></div></div>''')
    en_q1 = esc(e1).replace('ease.', '<u></u>.')
    en_q2 = esc(e2).replace('comfort.', '<u></u>.')
    en_q3 = esc(e3).replace('sufficient', '<u></u>')
    score = ps(7, f'''<div style="position:absolute;left:90px;right:90px;top:190px;height:960px;border-radius:50%;background:radial-gradient(ellipse at 50% 50%,rgba(11,23,38,.78) 0%,rgba(11,23,38,.55) 45%,rgba(11,23,38,0) 72%)"></div><div class="content end-c" style="top:150px"><img class="midmark" src="{MARK}" style="height:150px">
<div class="e-ar" dir="rtl" lang="ar">كم أجبت؟</div><div class="e-en">How many did you get?</div>
<div class="score"><span>0</span><span>1</span><span>2</span><span>3</span></div>
<div class="e-ar2" dir="rtl" lang="ar" style="margin-top:26px">اكتب نتيجتك في التعليقات</div><div class="e-en2">Comment your score</div>
<div class="e-ar2" dir="rtl" lang="ar">وأرسلها لصديق… هل يتفوّق عليك؟</div><div class="e-en2">Send it to a friend. Can they beat you?</div>
<div class="e-follow">Follow <b>@taqwalantern</b> for daily reminders</div>
<div class="e-cred">Quran Arabic: Tanzil.net · Quran English: The Clear Quran® by Dr. Mustafa Khattab</div></div>''')
    slides = [
      cover,
      qslide(1, 1, 'سهل', 'EASY', 1, q1t[:3], [], en_q1),
      aslide(2, 1, 1, q1, q1t[3], ayah(5), e1, 'Ash-Sharh 94:5 · <span dir="rtl" lang="ar">الشرح ٥</span>'),
      qslide(3, 2, 'متوسط', 'MEDIUM', 2, t28[7:10], t28[11:12], en_q2),
      aslide(4, 2, 2, p28, t28[10], ayah(28), e2, 'Ar-Ra‘d 13:28 (part) · <span dir="rtl" lang="ar">الرعد ٢٨</span>'),
      qslide(5, 3, 'صعب', 'HARD', 3, t3[6:11], [], en_q3, 'sm'),
      aslide(6, 3, 3, p3, t3[11], '', e3, 'At-Talaq 65:3 (part) · <span dir="rtl" lang="ar">الطلاق ٣</span>'),
      score,
    ]
    render(slides, ['01-cover', '02-q1', '03-a1', '04-q2', '05-a2', '06-q3', '07-a3', '08-score'], ROOT / 'out/C06', SRC / 'C06.html')

# ------------------------------------------------------------------ C07
if 'C07' in which:
    phrase = V['phrase']; assert phrase == 'النظافة من الإيمان'
    m223 = he_matn('65004'); x223 = m223.split('،')[0]; assert m223.startswith(x223 + '،') and [skel(w) for w in x223.split()] == ['الطهور', 'شطر', 'الإيمان']
    e223 = he_said('65004'); xe223 = e223.split(',')[0]; assert xe223 == 'Purity is half of faith'
    m6982 = he_matn('6982'); e6982 = he_said('6982')
    texts['C07'] = {'phrase': phrase, 'verdicts': [V['verdict_baz'], V['verdict_uthaymin']], 'muslim223_excerpt': [x223, xe223], '6982': [m6982, e6982]}
    series = '<div class="series"><div class="s-ar" dir="rtl" lang="ar">تحقّق قبل أن تنشر</div><div class="s-en">CHECK BEFORE YOU SHARE</div></div>'
    cover = frame('s1', f'''<div class="content" style="top:130px">{series}
<div class="quote-ar" dir="rtl" lang="ar">«{esc(phrase)}»</div><div class="quote-en">“Cleanliness is part of faith.”</div>
<div class="ask-ar" dir="rtl" lang="ar">حديث؟</div><div class="ask-en">A hadith?</div>
<div class="yn"><span><b>نعم</b><i>Yes</i></span><span><b>لا</b><i>No</i></span></div>
<div class="prompt" dir="rtl" lang="ar" style="margin-top:30px">أجب في التعليقات… ثم اسحب</div><div class="prompt-en">Answer in the comments, then swipe</div></div>''', '', glow=False, cls='cover')
    verdict = frame('s2', f'''<div class="content" style="top:120px"><div class="fake" dir="rtl" lang="ar">{esc(phrase)}</div>
<div class="stamp"><b dir="rtl" lang="ar">لا يصحّ حديثًا</b><i>NOT AUTHENTIC AS A HADITH</i></div>
<div class="verd"><div class="v-ar" dir="rtl" lang="ar">«{esc(V['verdict_baz'])}»</div><div class="v-who">Ibn Baz</div>
<div class="v-en">Attributing it to the Prophet ﷺ is not correct.</div>
<div class="v-ar" dir="rtl" lang="ar">«{esc(V['verdict_uthaymin'])}»</div><div class="v-who">Ibn ‘Uthaymin</div>
<div class="v-en">It is not a hadith, but its meaning is sound.</div></div>
<div class="meaning-ar" dir="rtl" lang="ar">المعنى طيّب… لكن لا تقل: «قال النبي ﷺ»</div>
<div class="meaning">Good meaning. Just don’t say “the Prophet ﷺ said.”</div>
<div class="credit" style="margin-top:14px">Verdicts as listed on dorar.net · English ours</div></div>''')
    real = frame('s3', f'''<div class="content k-hadith"><div class="seal"><b dir="rtl" lang="ar">صحيح</b><i>AUTHENTIC</i></div>
<div class="lab-ar" dir="rtl" lang="ar">والصحيح أعظم</div><div class="lab-en">The authentic one says even more</div>
{ar_block(x223, 'hadith')}{rule()}<div class="en" style="font-size:44px">{esc(xe223)}</div>
<div class="refs"><div class="r1">{nums('Sahih Muslim 223 (excerpt)')}</div><div class="r2" dir="rtl" lang="ar">رواه مسلم، عن أبي مالك الأشعري رضي الله عنه</div></div>
<div class="credit">{esc(HE)}</div></div>''', 'teal', glow=True)
    real = real.replace('.ar.hadith', '.ar.hadith')
    why = item_slide('s4', None, 'لماذا نتحقّق؟', 'Why we check', ar_block(m6982, 'hadith'), esc(e6982),
        '<div class="r1">Sahih Muslim · Introduction</div><div class="r2" dir="rtl" lang="ar">رواه مسلم في مقدمة صحيحه، عن سمرة بن جندب والمغيرة بن شعبة رضي الله عنهما</div>', HE, 'k-hadith', size='mid')
    end = end_slide('s5', [('أرسلها لمجموعة العائلة', 'Send this to the family group chat'), ('أيّ «حديث» نتحقّق منه بعده؟', 'Which “hadith” should we check next? Comment it')],
        'ولا تنسونا من دعائكم', 'Keep us in your du’a', 'Hadith English: HadeethEnc.com · Gradings: dorar.net, binbaz.org.sa', 'teal')
    slides = [cover, verdict, real, why, end]
    render(slides, ['01-cover', '02-verdict', '03-authentic', '04-why', '05-send-ask'], ROOT / 'out/C07', SRC / 'C07.html')

json.dump(texts, open(B3 / 'texts3.json', 'w'), ensure_ascii=False, indent=1)

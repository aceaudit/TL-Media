"""C01 · 5 authentic du'as for anxiety · أدعية للهمّ والقلق
Builds slides.html from verified source data (never retyped), renders each slide
in Chromium at 1080x1350, checks the rendered Arabic against the sources, and
writes JPEGs (sRGB, q93) to ../out/.
"""
import json, hashlib, re, sys, pathlib, html
from playwright.sync_api import sync_playwright
from PIL import Image, ImageCms
SRGB = ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes()

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / 'src'
OUT = ROOT / 'out'; OUT.mkdir(exist_ok=True)
FS = (ROOT / 'deps/node_modules/@fontsource').as_uri()
sha = lambda s: hashlib.sha256(s.encode()).hexdigest()

S = json.load(open(SRC / 'sources.json'))
for k, v in S['hadeethenc'].items():
    assert sha(v['ar']) == v['ar_sha'] and sha(v['en']) == v['en_sha'], k
for k, v in S['qurancom'].items():
    assert sha(v['en']) == v['en_sha'], k
Q = {(x['surah'], x['ayah']): x['text'] for x in json.load(open(ROOT / 'deps/node_modules/quran-validator/data/quran-verses.json'))}
for k, v in S['qurancom'].items():
    s, a = map(int, k.split(':'))
    assert sha(Q[(s, a)]) == v['uth_sha'], 'Tanzil/QUL text differs from quran.com: ' + k

def between(s, a, b):
    i = s.index(a) + len(a); j = s.rindex(b)
    return s[i:j]

import unicodedata
def skel(w): return ''.join(c for c in w if unicodedata.category(c) != 'Mn' and c != '\u0640').replace('ٱ','ا').replace('آ','ا')
def tail_tokens(text, first_skel, prev_skel=None):
    toks = text.split(' ')
    idx = [i for i, t in enumerate(toks) if skel(t) == first_skel and (prev_skel is None or (i > 0 and skel(toks[i-1]) == prev_skel))]
    assert len(idx) == 1, (first_skel, idx, [skel(t) for t in toks])
    i = idx[0]
    part = ' '.join(toks[i:])
    assert text.endswith(part)
    return part

# ---- the five du'as, all cut from the sources in code ----
h5141, h5488 = S['hadeethenc']['5141'], S['hadeethenc']['5488']
d1_ar = between(h5141['ar'], '«', '»'); d1_en = between(h5141['en'], 'distress: "', '"')
d3_ar = between(h5488['ar'], '«', '»'); d3_en = between(h5488['en'], 'saying: "', '"')
assert d1_ar in h5141['ar'] and d1_en in h5141['en'] and d3_ar in h5488['ar'] and d3_en in h5488['en']

v2187 = Q[(21, 87)]; d2_ar = tail_tokens(v2187, 'لا', 'أن')
d2_en = between(S['qurancom']['21:87']['en'], 'he cried out, “', '”')
v3173 = Q[(3, 173)]; d5_ar = tail_tokens(v3173, 'حسبنا')
d5_en = between(S['qurancom']['3:173']['en'], 'they replied, “', '”')
d4_ar = [Q[(20, 25)], Q[(20, 26)]]
e25, e26 = S['qurancom']['20:25']['en'], S['qurancom']['20:26']['en']
assert e26.endswith(',')
d4_en = [e25, e26[:-1] + '.”']   # terminal comma → full stop + closing quote (the quotation runs on to 20:28)
for t in (d2_en, d5_en, e25, e26):
    assert '<sup' not in t

AR_DIGITS = str.maketrans('0123456789', '٠١٢٣٤٥٦٧٨٩')
def ayah(n): return f'<span class="ayah">۝{str(n).translate(AR_DIGITS)}</span>'

def esc(s): return html.escape(s, quote=True)

def ar_block(text, cls, split_at=None):
    """Arabic block; optional split into display lines at word boundaries (rejoin asserted)."""
    if split_at:
        parts = text.split(split_at)
        lines = [p + split_at.rstrip() for p in parts[:-1]] + [parts[-1]]
        assert ' '.join(lines) == text
        inner = ''.join(f'<span class="ln">{esc(l)}</span>' for l in lines)
    else:
        inner = esc(text)
    return f'<div class="ar {cls}" dir="rtl" lang="ar" data-expect="{esc(text)}" data-join="{1 if split_at else 0}">{inner}</div>'

MARK = (SRC / 'mark-gold.png').as_uri()

def footer():
    return f'<div class="foot"><img src="{MARK}"><span>@taqwalantern</span></div>'

ARCH = '''<svg class="arch" viewBox="0 0 1080 1350" aria-hidden="true">
<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#D9A55B" stop-opacity=".75"/><stop offset="1" stop-color="#D9A55B" stop-opacity=".18"/></linearGradient></defs>
<path d="M104 1196 V420 C104 300 330 214 540 118 C750 214 976 300 976 420 V1196 Z" fill="none" stroke="url(#g)" stroke-width="2.5"/>
<path d="M122 1180 V426 C122 314 340 232 540 140 C740 232 958 314 958 426 V1180 Z" fill="none" stroke="#D9A55B" stroke-opacity=".16" stroke-width="1.2"/>
<g fill="#D9A55B"><path d="M540 98 l9 13 -9 13 -9 -13z" opacity=".9"/></g>
</svg>'''

def rule(): return '<div class="rule"><i></i><b></b><i></i></div>'

def dua_slide(n, label_ar, label_en, ar_html, en_html, refs, credit, kind, tint=''):
    return f'''<section class="slide {tint}" id="s{n+1}">
<div class="bg"></div>{ARCH}
<div class="content {kind}">
  <div class="count">{n} <em>/</em> 5</div>
  <div class="lab-ar" dir="rtl" lang="ar">{esc(label_ar)}</div>
  <div class="lab-en">{esc(label_en)}</div>
  {ar_html}
  {rule()}
  <div class="en">{en_html}</div>
  <div class="refs">{refs}</div>
  <div class="credit">{esc(credit)}</div>
</div>{footer()}</section>'''

HE = 'Translation: HadeethEnc.com'
CQ = 'Translation: The Clear Quran® by Dr. Mustafa Khattab'

slides = []
# 1 · cover
slides.append(f'''<section class="slide cover" id="s1"><div class="bg"></div>{ARCH}
<div class="glow"></div>
<div class="content">
  <img class="bigmark" src="{MARK}">
  <div class="c-ar" dir="rtl" lang="ar">أدعية للهمّ والقلق</div>
  {rule()}
  <div class="c-en"><span class="n">5</span> Authentic Du’as<br><i>for Anxiety</i></div>
  <div class="c-sub-ar" dir="rtl" lang="ar">من القرآن والسنّة الصحيحة</div>
  <div class="c-sub-en">From the Quran &amp; authentic Sunnah</div>
  <div class="swipe">اسحب <span>·</span> SWIPE <b>›››</b></div>
</div>{footer()}</section>''')

slides.append(dua_slide(1, 'عند الكرب', 'In times of distress',
    ar_block(d1_ar, 'hadith s1', split_at='، '), esc(d1_en),
    '<div class="r1">Sahih al-Bukhari 6346 · Sahih Muslim 2730</div>'
    '<div class="r2" dir="rtl" lang="ar">متفق عليه، عن ابن عباس رضي الله عنهما</div>', HE, 'k-hadith'))

slides.append(dua_slide(2, 'حين تضيق بك الدنيا', 'When everything closes in',
    f'<div class="arwrap quran">{ar_block(d2_ar, "quran s2")}{ayah(87)}</div>', esc(d2_en),
    '<div class="r1">Al-Anbiya 21:87 (part) · <span dir="rtl" lang="ar">الأنبياء ٨٧</span></div>'
    '<div class="r3">The du’a of Yunus <span dir="rtl" lang="ar">عليه السلام</span> · see Jami‘ at-Tirmidhi 3505 (sahih)</div>', CQ, 'k-quran', 'teal'))

slides.append(dua_slide(3, 'إذا خشيت أن تفقد ما عندك', 'When you fear losing what you have',
    ar_block(d3_ar, 'hadith s3', split_at='، '), esc(d3_en),
    '<div class="r1">Sahih Muslim 2739</div>'
    '<div class="r2" dir="rtl" lang="ar">رواه مسلم، عن عبد الله بن عمر رضي الله عنهما</div>', HE, 'k-hadith'))

ar4 = (f'<div class="arwrap quran"><div class="vline">{ar_block(d4_ar[0], "quran s4")}{ayah(25)}</div>'
       f'<div class="vline">{ar_block(d4_ar[1], "quran s4")}{ayah(26)}</div></div>')
slides.append(dua_slide(4, 'قبل أمرٍ يُقلقك', 'Before something that worries you',
    ar4, esc(d4_en[0]) + '<br>' + esc(d4_en[1]),
    '<div class="r1">Ta-Ha 20:25–26 · <span dir="rtl" lang="ar">طه ٢٥–٢٦</span></div>'
    '<div class="r3">The du’a of Musa <span dir="rtl" lang="ar">عليه السلام</span></div>', CQ, 'k-quran', 'teal'))

slides.append(dua_slide(5, 'حين يملؤك الخوف', 'When fear fills you',
    f'<div class="arwrap quran">{ar_block(d5_ar, "quran s5")}{ayah(173)}</div>', esc(d5_en),
    '<div class="r1">Al-Imran 3:173 (part) · <span dir="rtl" lang="ar">آل عمران ١٧٣</span></div>'
    '<div class="r3">Also in Sahih al-Bukhari 4563</div>', CQ, 'k-quran'))

# 7 · save / send / follow
slides.append(f'''<section class="slide end" id="s7"><div class="bg"></div>{ARCH}
<div class="glow"></div>
<div class="content">
  <img class="midmark" src="{MARK}">
  <div class="e-ar" dir="rtl" lang="ar">احفظها لوقت الضيق</div>
  <div class="e-en">Save these for the hard days</div>
  <div class="e-ar" dir="rtl" lang="ar">وأرسلها لمن يحمل همًّا</div>
  <div class="e-en">Send them to someone carrying a worry</div>
  {rule()}
  <div class="e-ar2" dir="rtl" lang="ar">ولا تنسونا من دعائكم</div>
  <div class="e-en2">Keep us in your du’a</div>
  <div class="e-follow">Follow <b>@taqwalantern</b> for daily reminders</div>
  <div class="e-cred">Quran Arabic: Tanzil.net · Quran English: The Clear Quran® by Dr. Mustafa Khattab<br>Hadith English: HadeethEnc.com</div>
</div>{footer()}</section>''')

CSS = f'''
@font-face{{font-family:"Amiri";font-weight:400;src:url({FS}/amiri/files/amiri-arabic-400-normal.woff2) format("woff2");unicode-range:U+0600-06FF,U+0750-077F,U+0870-08FF,U+FB50-FDFF,U+FE70-FEFF,U+200C-200E,U+25CC;}}
@font-face{{font-family:"Amiri";font-weight:700;src:url({FS}/amiri/files/amiri-arabic-700-normal.woff2) format("woff2");unicode-range:U+0600-06FF,U+0750-077F,U+0870-08FF,U+FB50-FDFF,U+FE70-FEFF,U+200C-200E,U+25CC;}}
@font-face{{font-family:"Amiri";font-weight:400;src:url({FS}/amiri/files/amiri-latin-400-normal.woff2) format("woff2");unicode-range:U+0000-00FF,U+2000-206F;}}
@font-face{{font-family:"Amiri Quran";src:url({FS}/amiri-quran/files/amiri-quran-arabic-400-normal.woff2) format("woff2");}}
@font-face{{font-family:"Cormorant Garamond";font-weight:500;src:url({FS}/cormorant-garamond/files/cormorant-garamond-latin-500-normal.woff2) format("woff2");}}
@font-face{{font-family:"Cormorant Garamond";font-weight:500;font-style:italic;src:url({FS}/cormorant-garamond/files/cormorant-garamond-latin-500-italic.woff2) format("woff2");}}
@font-face{{font-family:"Cormorant Garamond";font-weight:600;src:url({FS}/cormorant-garamond/files/cormorant-garamond-latin-600-normal.woff2) format("woff2");}}
@font-face{{font-family:"Marcellus";src:url({FS}/marcellus/files/marcellus-latin-400-normal.woff2) format("woff2");}}
@font-face{{font-family:"Marcellus";src:url({FS}/marcellus/files/marcellus-latin-ext-400-normal.woff2) format("woff2");unicode-range:U+0100-02AF,U+02B0-02FF,U+1E00-1EFF;}}
@font-face{{font-family:"Brackets";src:url({FS}/noto-serif/files/noto-serif-latin-ext-400-normal.woff2) format("woff2");unicode-range:U+02F9-02FA;}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#000;width:1080px}}
.slide{{width:1080px;height:1350px;position:relative;overflow:hidden;color:#F4EBDD;
  background:radial-gradient(ellipse 820px 760px at 50% 44%,#1B3046 0%,#122337 48%,#0D1B2A 100%)}}
.slide.teal{{background:radial-gradient(ellipse 820px 760px at 50% 44%,#1d4b52 0%,#173F45 40%,#0f2630 78%,#0D1B2A 100%)}}
.bg{{position:absolute;inset:0;opacity:.07;background-size:120px 120px;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Cg fill='none' stroke='%23D9A55B' stroke-width='1.2'%3E%3Crect x='35' y='35' width='50' height='50'/%3E%3Crect x='35' y='35' width='50' height='50' transform='rotate(45 60 60)'/%3E%3Cpath d='M0 60H25M95 60H120M60 0V25M60 95V120'/%3E%3C/g%3E%3C/svg%3E");
  -webkit-mask-image:radial-gradient(ellipse 600px 560px at 50% 46%,transparent 40%,#000 100%)}}
.arch{{position:absolute;inset:0;width:1080px;height:1350px}}
.glow{{position:absolute;left:290px;top:120px;width:500px;height:500px;border-radius:50%;
  background:radial-gradient(circle,rgba(246,213,142,.30) 0%,rgba(217,165,91,.10) 40%,transparent 70%)}}
.content{{position:absolute;left:150px;right:150px;top:150px;bottom:178px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}}
.count{{font:400 24px/1 "Marcellus";letter-spacing:.24em;color:#D9A55B;margin-bottom:26px}}
.count em{{font-style:normal;opacity:.5;margin:0 .1em}}
.lab-ar{{font:400 40px/1.5 "Amiri";color:#F6D58E}}
.lab-en{{font:400 20px/1.3 "Marcellus";letter-spacing:.17em;text-transform:uppercase;color:#D9A55B;margin:4px 0 34px}}
.ar{{font-family:"Amiri";font-weight:700;color:#FFF4DA;line-height:1.95;text-wrap:balance;text-shadow:0 0 24px rgba(246,213,142,.18)}}
.ar .ln{{display:block}}
.ar.hadith{{font-size:50px}}
.ar.s3{{font-size:52px}}
.arwrap.quran{{direction:rtl;display:flex;flex-direction:column;align-items:center}}
.ar.quran{{font-family:"Amiri Quran";font-weight:400;font-size:60px;line-height:2.1;display:inline}}
.arwrap.quran{{display:block;font-family:"Amiri Quran";font-size:60px;line-height:2.1;text-wrap:balance}}

.vline{{display:block;white-space:nowrap}}
.content.k-quran,.content.k-hadith{{top:170px}}
.ayah{{font-family:"Amiri Quran";color:#D9A55B;font-size:.82em;margin:0 .18em}}
.rule{{display:flex;align-items:center;gap:14px;margin:26px 0 24px}}
.rule i{{display:block;width:96px;height:1.5px;background:linear-gradient(90deg,transparent,#D9A55B)}}
.rule i:last-child{{background:linear-gradient(270deg,transparent,#D9A55B)}}
.rule b{{width:11px;height:11px;transform:rotate(45deg);background:#D9A55B}}
.en{{font:500 34px/1.36 "Cormorant Garamond","Brackets","Amiri",serif;color:#F4EBDD;text-wrap:balance;max-width:760px}}
.k-quran .en{{font-size:36px}}
.refs{{margin-top:30px}}
.r1{{font:400 21px/1.5 "Marcellus","Amiri";letter-spacing:.12em;text-transform:uppercase;color:#D9A55B}}
.r1 span{{font-family:"Amiri";letter-spacing:0;font-size:24px}}
.r2{{font:400 24px/1.6 "Amiri";color:#9FB1BF;margin-top:4px}}
.r3{{font:500 italic 23px/1.45 "Cormorant Garamond","Amiri";color:#9FB1BF;margin-top:4px}}
.r3 span{{font-style:normal;font-size:21px}}
.credit{{font:500 italic 19px/1.3 "Cormorant Garamond";color:#9FB1BF;opacity:.85;margin-top:10px}}
.foot{{position:absolute;left:0;right:0;bottom:70px;display:flex;align-items:center;justify-content:center;gap:12px}}
.foot img{{height:46px}}
.foot span{{font:400 21px/1 "Marcellus";letter-spacing:.16em;color:#D9A55B}}
/* cover */
.cover .content{{top:120px}}
.bigmark{{height:250px;filter:drop-shadow(0 0 28px rgba(246,213,142,.45));margin-bottom:22px}}
.c-ar{{font:700 112px/1.5 "Amiri";color:#FFF4DA;text-shadow:0 0 34px rgba(246,213,142,.25)}}
.cover .rule{{margin:34px 0 24px}}
.c-en{{font:600 74px/1.08 "Cormorant Garamond";color:#F4EBDD}}
.c-en i{{font-weight:500;font-style:italic;color:#F6D58E}}
.c-en .n{{color:#D9A55B}}
.c-sub-ar{{font:400 34px/1.5 "Amiri";color:#9FB1BF;margin-top:30px}}
.c-sub-en{{font:400 19px/1.4 "Marcellus";letter-spacing:.16em;text-transform:uppercase;color:#D9A55B}}
.swipe{{margin-top:34px;font:400 20px/1 "Marcellus","Amiri";letter-spacing:.2em;color:#F6D58E;opacity:.9}}
.swipe span{{opacity:.5;margin:0 .3em}} .swipe b{{font-weight:400;letter-spacing:.05em}}
/* end */
.end .content{{top:130px}}
.midmark{{height:170px;filter:drop-shadow(0 0 22px rgba(246,213,142,.45));margin-bottom:26px}}
.e-ar{{font:700 60px/1.55 "Amiri";color:#FFF4DA}}
.e-en{{font:500 italic 36px/1.2 "Cormorant Garamond";color:#F4EBDD;margin-bottom:22px}}
.e-ar2{{font:400 40px/1.5 "Amiri";color:#F6D58E}}
.e-en2{{font:500 italic 28px/1.2 "Cormorant Garamond";color:#F6D58E;margin-bottom:26px}}
.e-follow{{font:500 30px/1.3 "Cormorant Garamond";color:#F4EBDD}}
.e-follow b{{font-family:"Marcellus";font-weight:400;font-size:25px;letter-spacing:.08em;color:#D9A55B}}
.e-cred{{font:500 italic 18px/1.45 "Cormorant Garamond";color:#9FB1BF;margin-top:28px}}
'''

doc = f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{"".join(slides)}</body></html>'
(SRC / 'slides.html').write_text(doc, encoding='utf-8')

EXPECT = {'d1': d1_ar, 'd2': d2_ar, 'd3': d3_ar, 'd4a': d4_ar[0], 'd4b': d4_ar[1], 'd5': d5_ar}
CHECK_JS = r'''() => {
  const r = {fonts: {}, ar: [], overflow: [], bounds: []};
  for (const f of ['700 50px Amiri','400 60px "Amiri Quran"','500 34px "Cormorant Garamond"','400 20px Marcellus','400 20px Brackets']) r.fonts[f] = document.fonts.check(f, f.includes('Amiri')?'ﷺلا':'Aa˹');
  document.querySelectorAll('.ar').forEach(el => {
    const lines = [...el.querySelectorAll('.ln')];
    const got = lines.length ? lines.map(l=>l.textContent).join(' ') : el.textContent;
    r.ar.push({ok: got === el.dataset.expect, got});
  });
  document.querySelectorAll('.slide').forEach(s => {
    const sb = s.getBoundingClientRect();
    s.querySelectorAll('.content > *, .foot, .ar, .en, .refs').forEach(e => {
      const b = e.getBoundingClientRect();
      const L=b.left-sb.left, R=sb.right-b.right, T=b.top-sb.top, B=sb.bottom-b.bottom;
      if (L<64||R<64||T<64||B<64) r.overflow.push(s.id+' '+e.className+' '+[L,R,T,B].map(Math.round));
    });
    const c = s.querySelector('.content');
    const kids=[...c.children]; const top=Math.min(...kids.map(k=>k.getBoundingClientRect().top))-sb.top, bot=Math.max(...kids.map(k=>k.getBoundingClientRect().bottom))-sb.top;
    r.bounds.push(s.id+' content y '+Math.round(top)+'–'+Math.round(bot)+' foot top '+Math.round(s.querySelector('.foot').getBoundingClientRect().top-sb.top));
  });
  return r;
}'''

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1080, 'height': 1350}, device_scale_factor=1)
    pg.goto((SRC / 'slides.html').as_uri()); pg.wait_for_load_state('networkidle')
    pg.evaluate('document.fonts.ready.then(()=>1)')
    res = pg.evaluate(CHECK_JS)
    print(json.dumps({k: v for k, v in res.items() if k != 'ar'}, ensure_ascii=False, indent=1))
    expected = [d1_ar, d2_ar, d3_ar, d4_ar[0], d4_ar[1], d5_ar]
    assert len(res['ar']) == len(expected)
    for got, exp in zip(res['ar'], expected):
        assert got['ok'] and got['got'] == exp, ('ARABIC MISMATCH', got, exp)
    print('Arabic DOM text == source for all', len(expected), 'blocks')
    names = ['01-cover', '02-dua-distress', '03-dua-yunus', '04-dua-blessings', '05-dua-musa', '06-dua-hasbunallah', '07-save-send-follow']
    for i, n in enumerate(names):
        el = pg.locator(f'#s{i+1}')
        png = OUT / f'{n}.png'
        el.screenshot(path=str(png))
        im = Image.open(png).convert('RGB'); assert im.size == (1080, 1350), im.size
        im.save(OUT / f'{n}.jpg', 'JPEG', quality=93, subsampling=0, optimize=True, icc_profile=SRGB); png.unlink()
    b.close()
json.dump({'d1_ar': d1_ar, 'd1_en': d1_en, 'd2_ar': d2_ar, 'd2_en': d2_en, 'd3_ar': d3_ar, 'd3_en': d3_en,
           'd4_ar': d4_ar, 'd4_en': d4_en, 'd5_ar': d5_ar, 'd5_en': d5_en}, open(SRC / 'texts.json', 'w'), ensure_ascii=False, indent=1)
print('done')

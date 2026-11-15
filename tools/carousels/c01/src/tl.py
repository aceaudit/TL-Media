"""Taqwa Lantern carousel builder (shared). Slides are HTML/CSS rendered in Chromium at
1080x1350, DPR 1. Every Arabic block carries data-expect (the exact source string); after
rendering, the page text of each block is compared with it before any JPEG is written."""
import json, hashlib, html, pathlib, unicodedata
from playwright.sync_api import sync_playwright
from PIL import Image, ImageCms

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / 'src'
FS = (ROOT / 'deps/node_modules/@fontsource').as_uri()
MARK = (SRC / 'mark-gold.png').as_uri()
SRGB = ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes()
sha = lambda s: hashlib.sha256(s.encode()).hexdigest()
esc = lambda s: html.escape(s, quote=True)
AR_DIGITS = str.maketrans('0123456789', '٠١٢٣٤٥٦٧٨٩')
PAUSE = set('ۖۗۘۙۚۛۜ')

def quran():
    return {(x['surah'], x['ayah']): x['text'] for x in json.load(open(ROOT / 'deps/node_modules/quran-validator/data/quran-verses.json'))}

def between(s, a, b):
    i = s.index(a) + len(a); j = s.rindex(b)
    return s[i:j]

def skel(w):
    return ''.join(c for c in w if unicodedata.category(c) != 'Mn' and c != 'ـ').replace('ٱ', 'ا').replace('آ', 'ا')

def tail_tokens(text, first_skel, prev_skel=None):
    toks = text.split(' ')
    idx = [i for i, t in enumerate(toks) if skel(t) == first_skel and (prev_skel is None or (i > 0 and skel(toks[i-1]) == prev_skel))]
    assert len(idx) == 1, (first_skel, idx)
    part = ' '.join(toks[idx[0]:]); assert text.endswith(part)
    return part

def ayah(n):
    return f'<span class="ayah">۝{str(n).translate(AR_DIGITS)}</span>'

def ar_block(text, cls, split_at=None, lines=None):
    """Arabic block. A Quran pause mark that stands alone between spaces is attached to the end of the word
    before it, for display only (as on videos 40 and 70; no letter changes). data-expect holds the displayed
    string; here we assert it maps back to the source exactly, and the browser check compares the page to it."""
    disp = text
    for m in PAUSE:
        disp = disp.replace(' ' + m + ' ', m + ' ')
    undo = disp
    for m in PAUSE:
        undo = undo.replace(m + ' ', ' ' + m + ' ')
    assert undo == text, 'pause-mark display transform is not reversible'
    if split_at:
        parts = disp.split(split_at)
        lines = [p + split_at.rstrip() for p in parts[:-1]] + [parts[-1]]
    if lines:
        assert ' '.join(lines) == disp, ('line split does not rejoin', lines)
        inner = ''.join(f'<span class="ln">{esc(l)}</span>' for l in lines)
    else:
        inner = esc(disp)
    return f'<div class="ar {cls}" dir="rtl" lang="ar" data-expect="{esc(disp)}">{inner}</div>'

import re as _re
def nums(h):
    """Wrap ASCII digit runs (outside tags) so they render as lining figures; Marcellus' 1 reads like I."""
    return _re.sub(r'(?<![A-Za-z0-9#])([0-9][0-9:–\-]*)(?![^<]*>)', r'<span class="nm">\1</span>', h)

def footer():
    return f'<div class="foot"><img src="{MARK}"><span>@taqwalantern</span></div>'

ARCH = '''<svg class="arch" viewBox="0 0 1080 1350" aria-hidden="true">
<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#D9A55B" stop-opacity=".75"/><stop offset="1" stop-color="#D9A55B" stop-opacity=".18"/></linearGradient></defs>
<path d="M104 1196 V420 C104 300 330 214 540 118 C750 214 976 300 976 420 V1196 Z" fill="none" stroke="url(#g)" stroke-width="2.5"/>
<path d="M122 1180 V426 C122 314 340 232 540 140 C740 232 958 314 958 426 V1180 Z" fill="none" stroke="#D9A55B" stroke-opacity=".16" stroke-width="1.2"/>
<g fill="#D9A55B"><path d="M540 98 l9 13 -9 13 -9 -13z" opacity=".9"/></g>
</svg>'''

def rule(): return '<div class="rule"><i></i><b></b><i></i></div>'

def frame(sid, inner, tint='', glow=False, cls=''):
    g = '<div class="glow"></div>' if glow else ''
    return f'<section class="slide {tint} {cls}" id="{sid}"><div class="bg"></div>{ARCH}{g}{inner}{footer()}</section>'

def item_slide(sid, count, label_ar, label_en, ar_html, en_html, refs_html, credit, kind, tint='', size=''):
    c = f'<div class="count">{nums(count)}</div>' if count else ''
    la = f'<div class="lab-ar" dir="rtl" lang="ar">{esc(label_ar)}</div>' if label_ar else ''
    le = f'<div class="lab-en">{esc(label_en)}</div>' if label_en else ''
    return frame(sid, f'''<div class="content {kind} {size}">{c}{la}{le}{ar_html}{rule()}
<div class="en">{en_html}</div><div class="refs">{nums(refs_html)}</div><div class="credit">{esc(credit)}</div></div>''', tint)

def cover_slide(sid, title_ar, title_en_html, sub_ar, sub_en, swipe=True, tint=''):
    sw = '<div class="swipe">اسحب <span>·</span> SWIPE <b>›››</b></div>' if swipe else ''
    return frame(sid, f'''<div class="content cover-c"><img class="bigmark" src="{MARK}">
<div class="c-ar" dir="rtl" lang="ar">{esc(title_ar)}</div>{rule()}
<div class="c-en">{title_en_html}</div>
<div class="c-sub-ar" dir="rtl" lang="ar">{esc(sub_ar)}</div><div class="c-sub-en">{esc(sub_en)}</div>{sw}</div>''', tint, glow=True, cls='cover')

def end_slide(sid, pairs, small_ar, small_en, credits_html, tint=''):
    body = ''.join(f'<div class="e-ar" dir="rtl" lang="ar">{esc(a)}</div><div class="e-en">{esc(e)}</div>' for a, e in pairs)
    return frame(sid, f'''<div class="content end-c"><img class="midmark" src="{MARK}">{body}{rule()}
<div class="e-ar2" dir="rtl" lang="ar">{esc(small_ar)}</div><div class="e-en2">{esc(small_en)}</div>
<div class="e-follow">Follow <b>@taqwalantern</b> for daily reminders</div>
<div class="e-cred">{credits_html}</div></div>''', tint, glow=True, cls='end')

CSS = f'''
@font-face{{font-family:"Amiri";font-weight:400;src:url({FS}/amiri/files/amiri-arabic-400-normal.woff2) format("woff2");unicode-range:U+0600-06FF,U+0750-077F,U+0870-08FF,U+FB50-FDFF,U+FE70-FEFF,U+200C-200E,U+25CC;}}
@font-face{{font-family:"Amiri";font-weight:700;src:url({FS}/amiri/files/amiri-arabic-700-normal.woff2) format("woff2");unicode-range:U+0600-06FF,U+0750-077F,U+0870-08FF,U+FB50-FDFF,U+FE70-FEFF,U+200C-200E,U+25CC;}}
@font-face{{font-family:"Amiri";font-weight:400;src:url({FS}/amiri/files/amiri-latin-400-normal.woff2) format("woff2");unicode-range:U+0000-00FF,U+2000-206F;}}
@font-face{{font-family:"Amiri";font-weight:700;src:url({FS}/amiri/files/amiri-latin-400-normal.woff2) format("woff2");unicode-range:U+0000-00FF,U+2000-206F;}}
@font-face{{font-family:"Amiri Quran";src:url({FS}/amiri-quran/files/amiri-quran-arabic-400-normal.woff2) format("woff2");}}
@font-face{{font-family:"Cormorant Garamond";font-weight:500;src:url({FS}/cormorant-garamond/files/cormorant-garamond-latin-500-normal.woff2) format("woff2");}}
@font-face{{font-family:"Cormorant Garamond";font-weight:500;src:url({FS}/cormorant-garamond/files/cormorant-garamond-latin-ext-500-normal.woff2) format("woff2");unicode-range:U+0100-024F,U+1E00-1EFF;}}
@font-face{{font-family:"Cormorant Garamond";font-weight:500;font-style:italic;src:url({FS}/cormorant-garamond/files/cormorant-garamond-latin-500-italic.woff2) format("woff2");}}
@font-face{{font-family:"Cormorant Garamond";font-weight:600;src:url({FS}/cormorant-garamond/files/cormorant-garamond-latin-600-normal.woff2) format("woff2");}}
@font-face{{font-family:"Marcellus";src:url({FS}/marcellus/files/marcellus-latin-400-normal.woff2) format("woff2");}}
@font-face{{font-family:"Marcellus";src:url({FS}/marcellus/files/marcellus-latin-ext-400-normal.woff2) format("woff2");unicode-range:U+0100-02AF,U+02B0-02FF,U+1E00-1EFF;}}
@font-face{{font-family:"Brackets";src:url({FS}/noto-serif/files/noto-serif-latin-ext-400-normal.woff2) format("woff2");unicode-range:U+02F9-02FA,U+0100-024F,U+1E00-1EFF;}}
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
.content{{position:absolute;left:150px;right:150px;top:170px;bottom:178px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}}
.count{{font:400 24px/1 "Marcellus";letter-spacing:.24em;color:#D9A55B;margin-bottom:26px}}
.lab-ar{{font:400 40px/1.5 "Amiri";color:#F6D58E}}
.lab-en{{font:400 20px/1.3 "Marcellus";letter-spacing:.17em;text-transform:uppercase;color:#D9A55B;margin:4px 0 34px}}
.ar{{font-family:"Amiri";font-weight:700;color:#FFF4DA;line-height:1.95;text-wrap:balance;text-shadow:0 0 24px rgba(246,213,142,.18)}}
.ar .ln{{display:block}}
.ar.hadith{{font-size:50px}}
.long .ar.hadith{{font-size:38px;line-height:1.85}}
.long .en{{font-size:27px;line-height:1.32}}
.mid .ar.hadith{{font-size:44px}}
.mid .en{{font-size:31px}}
.arwrap.quran{{direction:rtl;display:block;font-family:"Amiri Quran";font-size:58px;line-height:2.1;text-wrap:balance}}
.ar.quran{{font-family:"Amiri Quran";font-weight:400;font-size:inherit;line-height:inherit;display:inline}}
.vline{{display:block;white-space:nowrap}}
.ayah{{font-family:"Amiri Quran";color:#D9A55B;font-size:.82em;margin:0 .18em}}
.rule{{display:flex;align-items:center;gap:14px;margin:26px 0 24px}}
.rule i{{display:block;width:96px;height:1.5px;background:linear-gradient(90deg,transparent,#D9A55B)}}
.rule i:last-child{{background:linear-gradient(270deg,transparent,#D9A55B)}}
.rule b{{width:11px;height:11px;transform:rotate(45deg);background:#D9A55B}}
.en{{font:500 34px/1.36 "Cormorant Garamond","Brackets","Amiri",serif;color:#F4EBDD;text-wrap:balance;max-width:770px}}
.k-quran .en{{font-size:36px}}
.refs{{margin-top:30px}}
.r1{{font:400 21px/1.5 "Marcellus","Amiri";letter-spacing:.12em;text-transform:uppercase;color:#D9A55B}}
.r1 span{{font-family:"Amiri";letter-spacing:0;font-size:24px}}
.r2{{font:400 24px/1.6 "Amiri";color:#9FB1BF;margin-top:4px}}
.r3{{font:500 italic 23px/1.45 "Cormorant Garamond","Amiri";color:#9FB1BF;margin-top:4px}}
.r3 span{{font-style:normal;font-size:21px}}
.credit{{font:500 italic 19px/1.3 "Cormorant Garamond";color:#9FB1BF;opacity:.85;margin-top:10px}}
.nm{{font-family:"Cormorant Garamond";font-weight:600;font-variant-numeric:lining-nums;letter-spacing:.04em;font-size:1.18em;line-height:1}}
.pick span,.choice .num i{{font-variant-numeric:lining-nums}}
.foot{{position:absolute;left:0;right:0;bottom:70px;display:flex;align-items:center;justify-content:center;gap:12px}}
.foot img{{height:46px}}
.foot span{{font:400 21px/1 "Marcellus";letter-spacing:.16em;color:#D9A55B}}
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
.end .content{{top:130px}}
.midmark{{height:170px;filter:drop-shadow(0 0 22px rgba(246,213,142,.45));margin-bottom:26px}}
.e-ar{{font:700 60px/1.55 "Amiri";color:#FFF4DA}}
.e-en{{font:500 italic 36px/1.2 "Cormorant Garamond";color:#F4EBDD;margin-bottom:22px}}
.e-ar2{{font:400 40px/1.5 "Amiri";color:#F6D58E}}
.e-en2{{font:500 italic 28px/1.2 "Cormorant Garamond";color:#F6D58E;margin-bottom:26px}}
.e-follow{{font:500 30px/1.3 "Cormorant Garamond";color:#F4EBDD}}
.e-follow b{{font-family:"Marcellus";font-weight:400;font-size:25px;letter-spacing:.08em;color:#D9A55B}}
.e-cred{{font:500 italic 18px/1.45 "Cormorant Garamond";color:#9FB1BF;margin-top:28px}}
/* first slide that carries the hook and the item */
.hooky .lab-ar{{font-weight:700;font-size:62px;line-height:1.45;color:#FFF4DA;text-shadow:0 0 30px rgba(246,213,142,.22)}}
.hooky .lab-en{{font-size:22px;margin-bottom:40px}}
/* hook + choices (1 or 2) */
.hook-kicker{{font:400 22px/1 "Marcellus";letter-spacing:.24em;text-transform:uppercase;color:#D9A55B;margin-bottom:30px}}
.hook-ar{{font:700 76px/1.6 "Amiri";color:#FFF4DA;text-wrap:balance;text-shadow:0 0 30px rgba(246,213,142,.2)}}
.hook-en{{font:500 italic 44px/1.22 "Cormorant Garamond";color:#F4EBDD;text-wrap:balance;max-width:760px;margin-top:10px}}
.q-ar{{font:400 52px/1.5 "Amiri";color:#F6D58E;margin-top:34px}}
.q-en{{font:600 34px/1.2 "Cormorant Garamond";color:#F6D58E}}
.pick{{display:flex;gap:22px;margin-top:40px}}
.pick span{{width:96px;height:96px;border-radius:50%;border:2.5px solid #D9A55B;display:flex;align-items:center;justify-content:center;font:600 46px/1 "Cormorant Garamond";color:#F6D58E;background:rgba(13,27,42,.35)}}
.choice{{width:760px;border:2px solid rgba(217,165,91,.65);border-radius:28px;padding:28px 34px 30px;background:rgba(13,27,42,.45);display:flex;align-items:center;gap:30px;text-align:left;margin:14px 0}}
.choice .num{{flex:none;width:110px;height:110px;border-radius:50%;border:2.5px solid #D9A55B;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#F6D58E}}
.choice .num b{{font:700 44px/1 "Amiri"}} .choice .num i{{font:600 30px/1 "Cormorant Garamond";font-style:normal;opacity:.85}}
.choice .txt{{flex:1}}
.choice .t-ar{{font:700 42px/1.5 "Amiri";color:#FFF4DA;text-align:right}}
.choice .t-en{{font:500 31px/1.22 "Cormorant Garamond";color:#F4EBDD}}
.vs{{font:400 22px/1 "Marcellus";letter-spacing:.3em;color:#D9A55B;opacity:.8;margin:6px 0}}
.nudge{{margin-top:34px;font:400 30px/1.4 "Amiri";color:#F6D58E}}
.nudge-en{{font:500 italic 27px/1.2 "Cormorant Garamond";color:#F6D58E}}
'''

CHECK_JS = r'''() => {
  const r = {ar: [], overflow: [], bounds: [], fonts: {}};
  for (const f of ['700 50px Amiri','400 58px "Amiri Quran"','500 34px "Cormorant Garamond"','400 20px Marcellus']) r.fonts[f] = document.fonts.check(f);
  document.querySelectorAll('.ar').forEach(el => {
    const lines = [...el.querySelectorAll('.ln')];
    let got = lines.length ? lines.map(l=>l.textContent).join(' ') : el.textContent;
    got = got.replace(/ /g,' ');
    r.ar.push({ok: got === el.dataset.expect, got, exp: el.dataset.expect});
  });
  document.querySelectorAll('.slide').forEach(s => {
    const sb = s.getBoundingClientRect();
    s.querySelectorAll('.content *').forEach(e => {
      const b = e.getBoundingClientRect(); if (!b.width) return;
      const L=b.left-sb.left, R=sb.right-b.right, T=b.top-sb.top, B=sb.bottom-b.bottom;
      if (L<64||R<64||T<64||B<64) r.overflow.push(s.id+' '+e.className+' '+[L,R,T,B].map(Math.round));
    });
    const c = s.querySelector('.content'); const kids=[...c.children];
    const top=Math.min(...kids.map(k=>k.getBoundingClientRect().top))-sb.top, bot=Math.max(...kids.map(k=>k.getBoundingClientRect().bottom))-sb.top;
    const foot = s.querySelector('.foot').getBoundingClientRect().top-sb.top;
    r.bounds.push(s.id+' content y '+Math.round(top)+'–'+Math.round(bot)+' foot '+Math.round(foot)+(bot>foot-30?'  !! TOO CLOSE TO FOOTER':''));
  });
  return r;
}'''

def render(slides, names, outdir, html_path):
    outdir = pathlib.Path(outdir); outdir.mkdir(parents=True, exist_ok=True)
    doc = f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{"".join(slides)}</body></html>'
    pathlib.Path(html_path).write_text(doc, encoding='utf-8')
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 1080, 'height': 1350}, device_scale_factor=1)
        pg.goto(pathlib.Path(html_path).as_uri()); pg.wait_for_load_state('networkidle')
        pg.evaluate('document.fonts.ready.then(()=>1)')
        res = pg.evaluate(CHECK_JS)
        for x in res['ar']:
            assert x['ok'], ('ARABIC MISMATCH', x)
        print('fonts', res['fonts'])
        print('\n'.join(res['bounds']))
        if res['overflow']: print('OVERFLOW', res['overflow'])
        print('Arabic DOM text == source for all', len(res['ar']), 'blocks')
        for i, n in enumerate(names):
            png = outdir / f'{n}.png'
            pg.locator(f'#s{i+1}').screenshot(path=str(png))
            im = Image.open(png).convert('RGB'); assert im.size == (1080, 1350)
            im.save(outdir / f'{n}.jpg', 'JPEG', quality=93, subsampling=0, optimize=True, icc_profile=SRGB); png.unlink()
        b.close()
    return res

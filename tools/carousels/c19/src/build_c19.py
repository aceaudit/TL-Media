"""C16–C19 (Wed 25 Nov 2026): plain designed carousels in the C01/C03/C05 style (no Reel frames), after the
owner's «by simple i meant consider no animation or simple animation». Every Arabic and English string is cut in
code from HadeethEnc API files (curl) or from sunnah.com excerpts moved over with per-string SHA-256 checks
(c19/data/sunnah_ex.json). The render step checks every Arabic block in the page against its source string."""
import json, sys, pathlib
import tl
from tl import *

D = pathlib.Path('/home/claude/c19/data'); D16 = pathlib.Path('/home/claude/c16/data')
OUT = pathlib.Path('/home/claude/c19/out')
SX = json.load(open(D / 'sunnah_ex.json'))
def he(i, lang): return json.load(open(D / f'he_{i}_{lang}.json'))['hadeeth']
def cut(s, a, b):
    i = s.index(a); j = s.index(b, i) + len(b); return s[i:j]
HE = 'Translation: HadeethEnc.com'; SN = 'Translation: Sunnah.com'
r1 = lambda t: f'<div class="r1">{t}</div>'
r2 = lambda t: f'<div class="r2" dir="rtl" lang="ar">{t}</div>'
which = sys.argv[1:] or ['C16', 'C17', 'C18', 'C19']
texts = {}

tl.CSS += f'@font-face{{font-family:"ScheN";font-weight:700;src:url({tl.FS}/scheherazade-new/files/scheherazade-new-arabic-700-normal.woff2) format("woff2");}}'
tl.CSS += '''
.ar.hadith{font-family:"ScheN","Amiri";font-weight:700;font-size:56px;line-height:1.75}
.big .ar.hadith{font-size:72px;line-height:1.6}
.mid .ar.hadith{font-size:48px}
.small .ar.hadith{font-size:42px;line-height:1.75}
.small .en{font-size:30px}
.lab-ar{font-size:44px}
.en .tr{display:block;font-style:italic;color:#F6D58E;font-size:.82em;margin-bottom:6px}
.en .ctx{display:block;font-size:.8em;color:#C9BBA6;margin-bottom:4px}
'''

def sentence_en(s):
    """English in parentheses after a transliteration, e.g. "(With Your name, O Allah, I die and I live)" → text."""
    assert s.startswith('(') and s.endswith(')'); return s[1:-1]

# ---------------------------------------------------------------- C16: before you sleep (6 slides)
if 'C16' in which:
    a1 = SX['b6324_ar']; e1 = sentence_en(SX['b6324_en']) + '.'
    h5879a, h5879e = he(5879, 'ar'), he(5879, 'en')
    a2 = cut(h5879a, 'كان إذا أخذ', 'ومسح بهما جسده'); e2 = cut(h5879e, 'Whenever the Messenger', 'over his body.')
    h6076a, h6076e = he(6076, 'ar'), he(6076, 'en')
    a3 = cut(h6076a, 'إِذَا أَخَذْتُمَا', 'خَيْرٌ لَكُمَا مِنْ خَادِمٍ'); e3 = cut(h6076e, 'When you go to bed', 'better for you than a servant.')
    h6167a, h6167e = he(6167, 'ar'), he(6167, 'en')
    a4 = between(h6167a, '«', '»'); e4 = cut(h6167e, '(O Allah, protect', 'Your servants)')[1:-1] + '.'
    for a, s in ((a1, None), (a2, h5879a), (a3, h6076a), (a4, h6167a)):
        if s: assert a in s
    p3 = a3.split('، '); assert len(p3) == 4, p3
    i0 = p3[0].index(' -'); i1 = p3[0].index('- ') + 1
    L3 = [p3[0][:i1], p3[0][i1+1:] + '، ' + p3[1] + '،', p3[2] + '،', p3[3]]
    texts['C16'] = {'bukhari6324': [a1, e1], 'he5879': [a2, e2], 'he6076': [a3, e3], 'he6167': [a4, e4]}
    slides = [
      cover_slide('s1', 'قبل أن تنام', 'Before you<br><i>go to sleep</i>', 'أربع سنن نبوية', '4 Sunnahs of the Prophet ﷺ'),
      item_slide('s2', '1 / 4', 'حين تضع رأسك', 'As you lie down', ar_block(a1, 'hadith'),
        esc(e1),
        r1('Sahih al-Bukhari 6324') + r2('رواه البخاري، عن حذيفة رضي الله عنه'), SN, 'k-hadith', size='big'),
      item_slide('s3', '2 / 4', 'المعوّذات', 'Al-Ikhlas · Al-Falaq · An-Nas', ar_block(a2, 'hadith', split_at='، '), esc(e2),
        r1('Sahih al-Bukhari 6319 · 5017') + r2('رواه البخاري، عن عائشة رضي الله عنها'), HE, 'k-hadith', 'teal'),
      item_slide('s4', '3 / 4', 'خير من خادم', '33 · 33 · 34', ar_block(a3, 'hadith', lines=L3), esc(e3),
        r1('Sahih al-Bukhari 5361 · Sahih Muslim 2727') + r2('متفق عليه، عن علي رضي الله عنه'), HE, 'k-hadith', size='small'),
      item_slide('s5', '4 / 4', 'ويدك تحت رأسك', 'Hand under your head', ar_block(a4, 'hadith'), esc(e4),
        r1('Jami‘ at-Tirmidhi 3398 · Sunan Abi Dawud 5045') + r2('رواه الترمذي، عن حذيفة رضي الله عنه'), HE, 'k-hadith', 'teal'),
      end_slide('s6', [('احفظها لتقرأها الليلة', 'Save it for tonight'), ('وأرسلها لمن تحب', 'Send it to someone you love')],
        'ولا تنسونا من دعائكم', 'Keep us in your du’a', 'Hadith English: Sunnah.com · HadeethEnc.com'),
    ]
    render(slides, ['01-cover', '02-bismika', '03-muawwidhat', '04-tasbih', '05-qini', '06-save-send'], OUT / 'C16', OUT / 'C16.html')

# ---------------------------------------------------------------- C17: Jumu'ah, the khutbah (3 slides)
if 'C17' in which:
    m = json.load(open(D16 / 'matn.json'))['jumuah']
    he3107 = json.load(open(D16 / 'he_3107_en.json'))['hadeeth']
    e = cut(he3107, 'If you say', 'idle talk.')
    P = m.split('، '); assert len(P) == 4, P
    L = [P[0] + '،', P[1] + '، ' + P[2] + '،', P[3]]
    texts['C17'] = {'he3107': [m, e]}
    slides = [
      cover_slide('s1', 'في خطبة الجمعة', 'At the Friday khutbah:<br><i>even this one word</i>', 'حديث صحيح · متفق عليه', 'An authentic hadith · Bukhari and Muslim'),
      item_slide('s2', None, 'وصيّة نبوية', 'A teaching of the Prophet ﷺ', ar_block(m, 'hadith', lines=L), esc(e),
        r1('Sahih Muslim 851 · Sahih al-Bukhari 934') + r2('متفق عليه، عن أبي هريرة رضي الله عنه'), HE, 'k-hadith', size='mid'),
      end_slide('s3', [('احفظها لكل جمعة', 'Save it for every Friday'), ('وأرسلها لمن تصلي معه الجمعة', 'Send it to someone you pray Jumu’ah with')],
        'ولا تنسونا من دعائكم', 'Keep us in your du’a', 'Hadith English: HadeethEnc.com', 'teal'),
    ]
    render(slides, ['01-cover', '02-khutbah', '03-save-send'], OUT / 'C17', OUT / 'C17.html')

# ---------------------------------------------------------------- C18: when it rains (5 slides)
if 'C18' in which:
    a1 = SX['n1523_ar']; e1 = sentence_en(SX['n1523_en']) + '.'
    a2 = SX['b846_ar']; e2 = '“…' + SX['b846_en'] + '…”'
    h3174a, h3174e = he(3174, 'ar'), he(3174, 'en')
    q = h3174a.split('«')[2].split('»')[0]; a3 = q.split('، ')[0]; assert skel(a3).replace(' ', '') == 'اللهمحوالينا'+'ولاعلينا'; e3 = cut(h3174e, 'O Allah, around us', 'not upon us') + '.'
    assert a3 in h3174a and e3[:-1] in h3174e
    texts['C18'] = {'nasai1523': [a1, e1], 'bukhari846': [a2, e2], 'he3174_excerpt': [a3, e3], 'bukhari1032': SX['b1032_ar']}
    slides = [
      cover_slide('s1', 'إذا نزل المطر', 'When it<br><i>starts to rain</i>', 'ثلاثة أذكار من السنة', '3 from the Sunnah'),
      item_slide('s2', '1 / 3', 'حين ترى المطر', 'When you see rain', ar_block(a1, 'hadith'),
        esc(e1),
        r1('Sunan an-Nasa’i 1523 · Sahih al-Bukhari 1032') + r2('عن عائشة رضي الله عنها'), SN, 'k-hadith', size='big'),
      item_slide('s3', '2 / 3', 'بعد المطر', 'After the rain', ar_block(a2, 'hadith'),
        f'<span class="ctx">Allah said, in a hadith qudsi:</span>{esc(e2)}',
        r1('Sahih al-Bukhari 846 · Sahih Muslim 71') + r2('متفق عليه، عن زيد بن خالد الجهني رضي الله عنه'), SN, 'k-hadith', 'teal', size='big'),
      item_slide('s4', '3 / 3', 'إذا اشتدّ المطر', 'When the rain is too much', ar_block(a3, 'hadith'),
        esc(e3),
        r1('Sahih al-Bukhari 1014 · Sahih Muslim 897 (excerpt)') + r2('متفق عليه، عن أنس رضي الله عنه'), HE, 'k-hadith', size='big'),
      end_slide('s5', [('احفظها للمطر القادم', 'Save it for the next rain'), ('وأرسلها لمن عندهم مطر الآن', 'Send it to someone where it’s raining now')],
        'ولا تنسونا من دعائكم', 'Keep us in your du’a', 'Hadith English: Sunnah.com · HadeethEnc.com', 'teal'),
    ]
    render(slides, ['01-cover', '02-when-you-see-rain', '03-after-rain', '04-heavy-rain', '05-save-send'], OUT / 'C18', OUT / 'C18.html')

# ---------------------------------------------------------------- C19: newlyweds send-card (3 slides)
if 'C19' in which:
    M = json.load(open(D16 / 'matn.json'))
    a = M['wed']; full_en = M['wed_en_full_tirmidhi1091']
    e = cut(full_en, 'May Allah bless you', 'goodness between you.')
    w = a.split(' '); assert len(w) == 9
    L = [' '.join(w[:5]), ' '.join(w[5:])]
    texts['C19'] = {'abudawud2130': [a, e]}
    slides = [
      cover_slide('s1', 'تعرف أحدًا تزوّج حديثًا؟', 'Know someone<br><i>who just got married?</i>', 'أرسل له هذا الدعاء', 'Send them this du’a'),
      item_slide('s2', None, 'كان النبي ﷺ يقول للمتزوّج', 'What the Prophet ﷺ said to the newlywed', ar_block(a, 'hadith', lines=L),
        esc(e),
        r1('Sunan Abi Dawud 2130 · Jami‘ at-Tirmidhi 1091') + r2('عن أبي هريرة رضي الله عنه'), SN, 'k-hadith', size='big'),
      end_slide('s3', [('أرسلها لمن تزوّج حديثًا', 'Send it to someone who just got married'), ('واحفظها للعرس القادم', 'Save it for the next wedding')],
        'ولا تنسونا من دعائكم', 'Keep us in your du’a', 'Hadith English: Sunnah.com', 'teal'),
    ]
    render(slides, ['01-cover', '02-the-dua', '03-send-save'], OUT / 'C19', OUT / 'C19.html')

json.dump(texts, open(OUT / ('texts-' + '-'.join(which) + '.json'), 'w'), ensure_ascii=False, indent=1)

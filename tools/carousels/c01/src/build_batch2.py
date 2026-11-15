import json, sys
from tl import *
S = json.load(open(SRC / 'sources2.json'))
for k, v in S.items():
    if k.startswith('Q'): assert sha(v['ar']) == v['uth_sha']
Q = quran()
HE = 'Translation: HadeethEnc.com'
CQ = 'Translation: The Clear Quran® by Dr. Mustafa Khattab'
def matn(id_): 
    a = between(S[id_]['ar'], '«', '»'); assert a in S[id_]['ar']; return a
def en_said(id_):
    e = between(S[id_]['en'], 'said: "', '"'); assert e in S[id_]['en']; return e
texts = {}
which = sys.argv[1:] or ['C02', 'C03', 'C04']

if 'C02' in which:
    v86 = Q[(12, 86)]; assert v86 == S['Q12:86']['ar']
    v87 = Q[(12, 87)]; assert v87 == S['Q12:87']['ar']
    p87 = tail_tokens(v87, 'ولا', 'وأخيه')
    e86s = S['Q12:86']['en']; assert e86s.startswith('He replied, “') and e86s.endswith('know.')
    e86 = e86s + '”'            # quotation continues into 12:87; closed here (terminal punctuation only)
    e87s = S['Q12:87']['en']; i = e87s.index('And do not lose hope'); assert e87s.endswith('faith.”')
    e87 = e87s[i:-1]            # the part matching the Arabic; the closing ” belongs to the speech begun in 12:86
    texts['C02'] = {'12:86_ar': v86, '12:86_en': e86, '12:87part_ar': p87, '12:87part_en': e87}
    slides = [
      cover_slide('s1', 'لمن تشكو همّك؟', 'Who do you take<br><i>your grief to?</i>',
        'من سورة يوسف', 'From Surah Yusuf'),
      item_slide('s2', None, 'حين اشتدّ حزنه', 'When his grief grew heavy',
        f'<div class="arwrap quran">{ar_block(v86, "quran")}{ayah(86)}</div>', esc(e86),
        '<div class="r1">Yusuf 12:86 · <span dir="rtl" lang="ar">يوسف ٨٦</span></div>'
        '<div class="r3">The words of Ya‘qub <span dir="rtl" lang="ar">عليه السلام</span></div>', CQ, 'k-quran'),
      item_slide('s3', None, 'ثم قال لأبنائه', 'Then he told his sons',
        f'<div class="arwrap quran">{ar_block(p87, "quran")}{ayah(87)}</div>', esc(e87),
        '<div class="r1">Yusuf 12:87 (part) · <span dir="rtl" lang="ar">يوسف ٨٧</span></div>', CQ, 'k-quran', 'teal'),
      end_slide('s4', [('اشكُ همّك إلى الله', 'Take your grief to Allah'), ('ولا تيأس من رحمته', 'and never lose hope in His mercy')],
        'وأرسلها لمن يحمل حزنًا', 'Send this to someone carrying grief',
        'Quran Arabic: Tanzil.net · Quran English: The Clear Quran® by Dr. Mustafa Khattab'),
    ]
    render(slides, ['01-cover', '02-yaqub-grief', '03-no-despair', '04-save-send-follow'], ROOT / 'out/C02', SRC / 'C02.html')

if 'C03' in which:
    # One reminder per Friday (owner, Wed 11 Nov 1:41 PM). Fajr (Bukhari 891), ghusl + going early (Bukhari 881,
    # two slides) and the khutbah (Bukhari 934) wait for later Fridays: their specs are in build_batch2_v1.py.
    m3711, e3711 = matn('3711'), en_said('3711')
    parts = m3711.split('، ')
    L3711 = [parts[0] + '،', parts[1] + '، ' + parts[2] + '،', parts[3] + '،', parts[4]]
    texts['C03'] = {'3711': [m3711, e3711]}
    r2 = lambda t: f'<div class="r2" dir="rtl" lang="ar">{t}</div>'
    slides = [
      cover_slide('s1', 'يوم الجمعة', 'Why Friday is<br><i>the best day</i>',
        'حديث صحيح · رواه مسلم', 'An authentic hadith · Sahih Muslim'),
      item_slide('s2', None, 'خير يوم', 'The best day', ar_block(m3711, 'hadith', lines=L3711), esc(e3711),
        '<div class="r1">Sahih Muslim 854</div>' + r2('رواه مسلم، عن أبي هريرة رضي الله عنه'), HE, 'k-hadith', size='mid'),
      end_slide('s3', [('احفظها لكل جمعة', 'Save it for every Friday'), ('وأرسلها لمن تحب', 'Send it to someone you love')],
        'ولا تنسونا من دعائكم', 'Keep us in your du’a', 'Hadith English: HadeethEnc.com', 'teal'),
    ]
    render(slides, ['01-cover', '02-best-day', '03-save-send-follow'], ROOT / 'out/C03', SRC / 'C03.html')

if 'C04' in which:
    m5351, e5351 = matn('5351'), en_said('5351')
    texts['C04'] = {'5351': [m5351, e5351]}
    hook = frame('s1', '''<div class="content">
<div class="hook-kicker">Which one are you?</div>
<div class="lab-ar" dir="rtl" lang="ar" style="margin-bottom:26px">أيّهما أنت؟</div>
<div class="hook-ar" dir="rtl" lang="ar">أهانك أحدُهم أمام الجميع</div>
<div class="hook-en">Someone humiliates you in front of everyone.</div>
<div class="q-ar" dir="rtl" lang="ar">ماذا تفعل؟</div><div class="q-en">What do you do?</div>
<div class="pick"><span>1</span><span>2</span></div>
<div class="swipe">اسحب <span>·</span> SWIPE <b>›››</b></div></div>''', glow=True)
    choices = frame('s2', '''<div class="content">
<div class="hook-kicker">Choose one</div>
<div class="choice"><div class="num"><b>١</b><i>1</i></div><div class="txt"><div class="t-ar" dir="rtl" lang="ar">تردّ الإهانة بأشدّ منها</div><div class="t-en">You hit back, even harder.</div></div></div>
<div class="vs">OR · <span style="font-family:Amiri;letter-spacing:0;font-size:26px">أو</span></div>
<div class="choice"><div class="num"><b>٢</b><i>2</i></div><div class="txt"><div class="t-ar" dir="rtl" lang="ar">تملك نفسك وتمضي</div><div class="t-en">You keep control of yourself and walk away.</div></div></div>
<div class="nudge" dir="rtl" lang="ar">اكتب ١ أو ٢ في التعليقات، ثم اسحب</div>
<div class="nudge-en">Comment 1 or 2, then swipe for the answer</div></div>''', 'teal')
    slides = [hook, choices,
      item_slide('s3', None, 'الجواب', 'The answer', ar_block(m5351, 'hadith', split_at='، '), esc(e5351),
        '<div class="r1">Sahih al-Bukhari 6114 · Sahih Muslim 2609</div><div class="r2" dir="rtl" lang="ar">متفق عليه، عن أبي هريرة رضي الله عنه</div>', HE, 'k-hadith'),
      end_slide('s4', [('أيّهما كنت؟', 'Which one were you?'), ('أرسلها لمن يحتاجها', 'Send it to someone who needs it')],
        'ولا تنسونا من دعائكم', 'Keep us in your du’a', 'Hadith English: HadeethEnc.com', 'teal'),
    ]
    render(slides, ['01-hook', '02-choices', '03-answer', '04-save-send-follow'], ROOT / 'out/C04', SRC / 'C04.html')

prev = json.load(open(SRC / 'texts2.json')) if (SRC / 'texts2.json').exists() else {}
prev.update(texts); json.dump(prev, open(SRC / 'texts2.json', 'w'), ensure_ascii=False, indent=1)
print('done', which)

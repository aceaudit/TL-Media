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
      item_slide('s1', None, 'لمن تشكو همّك؟', 'Who do you take your grief to?',
        f'<div class="arwrap quran">{ar_block(v86, "quran")}{ayah(86)}</div>', esc(e86),
        '<div class="r1">Yusuf 12:86 · <span dir="rtl" lang="ar">يوسف ٨٦</span></div>'
        '<div class="r3">The words of Ya‘qub <span dir="rtl" lang="ar">عليه السلام</span></div>', CQ, 'k-quran hooky'),
      item_slide('s2', None, 'ثم قال لأبنائه', 'Then he told his sons',
        f'<div class="arwrap quran">{ar_block(p87, "quran")}{ayah(87)}</div>', esc(e87),
        '<div class="r1">Yusuf 12:87 (part) · <span dir="rtl" lang="ar">يوسف ٨٧</span></div>', CQ, 'k-quran', 'teal'),
      end_slide('s3', [('اشكُ همّك إلى الله', 'Take your grief to Allah'), ('ولا تيأس من رحمته', 'and never lose hope in His mercy')],
        'وأرسلها لمن يحمل حزنًا', 'Send this to someone carrying grief',
        'Quran Arabic: Tanzil.net · Quran English: The Clear Quran® by Dr. Mustafa Khattab'),
    ]
    render(slides, ['01-yaqub-grief', '02-no-despair', '03-save-send-follow'], ROOT / 'out/C02', SRC / 'C02.html')

if 'C03' in which:
    m3711, e3711 = matn('3711'), en_said('3711')
    m5320 = matn('5320'); e5320 = S['5320']['en'].split('reported: ', 1)[1]; assert e5320 in S['5320']['en']
    m5393, e5393 = matn('5393'), en_said('5393')
    m3107, e3107 = matn('3107'), en_said('3107')
    # Bukhari 881 is too long for one slide: split at the fourth hour, Arabic and English at the same point
    sg = m5393.split('، '); assert len(sg) == 11
    a1 = '، '.join(sg[:6]) + '،'; a2 = '، '.join(sg[6:])
    assert a1 + ' ' + a2 == m5393
    La1 = [sg[0] + '،', sg[1] + '،', sg[2] + '، ' + sg[3] + '،', sg[4] + '، ' + sg[5] + '،']
    La2 = [sg[6] + '، ' + sg[7] + '،', sg[8] + '، ' + sg[9] + '،', sg[10]]
    E_CUT = '; whoever goes at the fourth hour'
    assert e5393.count(E_CUT) == 1
    e1, e2 = e5393.split(E_CUT); e1 = e1 + ';'; e2 = E_CUT[2:] + e2
    assert e1 + ' ' + e2 == e5393
    # display lines at the hadith's own commas (rejoin asserted in ar_block)
    L3711 = None
    parts = m3711.split('، ')
    L3711 = [parts[0] + '،', parts[1] + '، ' + parts[2] + '،', parts[3] + '،', parts[4]]
    p3107 = m3107.split('، ')
    L3107 = [p3107[0] + '،', p3107[1] + '، ' + p3107[2] + '،', p3107[3]]
    texts['C03'] = {'3711': [m3711, e3711], '5320': [m5320, e5320], '5393': [m5393, e5393], '5393_split': [[a1, e1], [a2, e2]], '3107': [m3107, e3107]}
    r2 = lambda t: f'<div class="r2" dir="rtl" lang="ar">{t}</div>'
    R881 = '<div class="r1">Sahih al-Bukhari 881 · Sahih Muslim 850</div>' + r2('متفق عليه، عن أبي هريرة رضي الله عنه')
    slides = [
      cover_slide('s1', 'يوم الجمعة', '<span class="n">4</span> Authentic Hadith<br><i>for Your Friday</i>',
        'من صحيح البخاري ومسلم', 'From Sahih al-Bukhari & Sahih Muslim'),
      item_slide('s2', '1 <em>/</em> 4', 'خير يوم', 'The best day', ar_block(m3711, 'hadith', lines=L3711), esc(e3711),
        '<div class="r1">Sahih Muslim 854</div>' + r2('رواه مسلم، عن أبي هريرة رضي الله عنه'), HE, 'k-hadith', size='mid'),
      item_slide('s3', '2 <em>/</em> 4', 'فجر الجمعة', 'Fajr on Friday', ar_block(m5320, 'hadith'), esc(e5320),
        '<div class="r1">Sahih al-Bukhari 891 · Sahih Muslim 880</div>' + r2('متفق عليه، عن أبي هريرة رضي الله عنه'), HE, 'k-hadith', 'teal', size='mid'),
      item_slide('s4', '3 <em>/</em> 4', 'اغتسل وبكّر', 'Bathe, then go early', ar_block(a1, 'hadith', lines=La1), esc(e1),
        R881 + '<div class="r3">Continued on the next slide</div>', HE, 'k-hadith', size='mid'),
      item_slide('s5', '3 <em>/</em> 4', 'تتمة الحديث', 'The hadith continues', ar_block(a2, 'hadith', lines=La2), esc(e2),
        R881, HE, 'k-hadith', size='mid'),
      item_slide('s6', '4 <em>/</em> 4', 'أنصت للخطبة', 'Listen to the khutbah in silence', ar_block(m3107, 'hadith', lines=L3107), esc(e3107),
        '<div class="r1">Sahih Muslim 851 · Sahih al-Bukhari 934</div>' + r2('متفق عليه، عن أبي هريرة رضي الله عنه'), HE, 'k-hadith', 'teal'),
      end_slide('s7', [('احفظها لكل جمعة', 'Save it for every Friday'), ('وأرسلها لمن تحب', 'Send it to someone you love')],
        'ولا تنسونا من دعائكم', 'Keep us in your du’a', 'Hadith English: HadeethEnc.com'),
    ]
    render(slides, ['01-cover', '02-best-day', '03-fajr', '04-ghusl-early-a', '05-ghusl-early-b', '06-khutbah-silence', '07-save-send-follow'], ROOT / 'out/C03', SRC / 'C03.html')

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

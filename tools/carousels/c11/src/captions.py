"""Captions, alt text, first comments and Buffer payloads for C08 v2, C10 v2, C11, C12 (picture posts).
Quran words in TikTok search lines are taken by code from the Tanzil data (textSimple), never typed."""
import json, sys, pathlib
sys.path.insert(0, '/home/claude/c01/src')
import tl

ROOT = pathlib.Path('/home/claude/c11')
QV = {(x['surah'], x['ayah']): x for x in json.load(open('/home/claude/c01/deps/node_modules/quran-validator/data/quran-verses.json'))}
simple_51_22 = QV[(51, 22)]['textSimple']
t65 = QV[(65, 7)]['textSimple']; simple_65_7 = t65[t65.index('سيجعل'):]
assert tl.skel(simple_65_7.split(' ')[0]) == 'سيجعل' and len(simple_65_7.split(' ')) == 5

IG, TT = '6ad6fb5e778b240e2f652c68', '6ad6fbb2778b240e2f652ea3'
RAW = 'https://raw.githubusercontent.com/aceaudit/TL-Media/main/carousels'

P = {}
P['C08'] = dict(
    folder='C08-never-too-small', files=['01-doorway.jpg', '02-greeting.jpg'], src='C08v2',
    title='لا تستصغره · Never too small',
    alt=['Animated scene on a rainy night: a faceless young man hands a bag of bread to his neighbour at a lit doorway. Text: Never too small. A hadith in Arabic with English: "Do not belittle any good deed, even if it be meeting your brother with a cheerful face." Sahih Muslim 2626, narrated by Abu Dharr.',
         'Animated scene at dawn on the same street: the young man walks past his neighbour, who stands at his door with his hand on his heart. Text: Who will you meet with a cheerful face today? Send this to them.'],
    ig='''لا تستصغره 🤍
Never too small.

A bag of bread in the rain. A warm greeting at the door. Don't belittle any good you can do today, even meeting someone with a cheerful face.

Send this to the most cheerful face you know 🤍
Follow @taqwalantern for daily reminders.

Sahih Muslim 2626, narrated by Abu Dharr (رضي الله عنه). Translation: HadeethEnc.com. Scenes from our Reel "When Allah Loves a Servant".

#hadith #goodcharacter #islamicreminders #islam #حديث''',
    tt='''«لا تستصغره» 🤍
حديث عن المعروف والابتسامة وطلاقة الوجه عند لقاء الناس
أرسلها لصاحب أجمل ابتسامة تعرفها 🤍
📖 صحيح مسلم 2626
Hadith about small good deeds and a cheerful face
#المعروف #الابتسامة #حسن_الخلق #مقاطع_دينية #حديث''',
    first='''اذكر صاحب أجمل ابتسامة تعرفه 👇
Tag the most cheerful face you know 👇''',
    sound='Reel 06 "Which One Are You" (rain, wind, footsteps; brotherhood) · backup Reel 08 "The Thorny Branch"',
    when='Wed 18 Nov 9:00 AM')

P['C11'] = dict(
    folder='C11-your-provision', files=['01-pearl.jpg'], src='C11',
    title='رزقك مكتوب · Your provision is written',
    alt=['Animated scene on the seabed: a glowing pearl rises from an open shell as light falls from above. Text: Allah says: "In heaven is your sustenance and whatever you are promised." Surah Adh-Dhariyat 51:22, in Arabic with English.'],
    ig='''رزقك مكتوب 🤍
Your provision is already written.

Allah tells us our sustenance is in heaven, along with all He has promised. Do your part, then let your heart rest.

Save this for the days you worry about rizq 🤍
Follow @taqwalantern for daily reminders.

Surah Adh-Dhariyat 51:22. Translation: The Clear Quran® by Dr. Mustafa Khattab. Arabic text: Tanzil.net. Scene from our Reel "It Will Never Pass You By".

#quran #rizq #islamicreminders #islam #القرآن''',
    tt=f'''«رزقك مكتوب» 🤍
آية عن الرزق والطمأنينة: {simple_51_22}
أرسلها لمن يقلق على رزقه 🤍
📖 الذاريات 22
Quran verse about rizq and provision
#الرزق #التوكل_على_الله #طمأنينة #مقاطع_دينية #القرآن_الكريم''',
    first='''اكتب دعاءً بالرزق لمن تحب 👇
Write a du'a for someone's provision 👇''',
    sound='Reel 20 "Like the Foam of the Sea" (surf, wind) · backup Reel 21 "Within Your Capacity"',
    when='Thu 19 Nov 9:00 AM')

P['C12'] = dict(
    folder='C12-after-hardship', files=['01-canyon.jpg', '02-valley.jpg'], src='C12',
    title='حين تضيق بك الدنيا · After hardship',
    alt=['Animated scene: a faceless young man in white stands in a narrow purple canyon beside a heavy sack, his hands raised in du\'a. Text: When the world closes in on you… Swipe for Allah\'s promise.',
         'The canyon has opened onto a green valley at sunrise. He walks out along a winding path with his arm raised, the sack left behind. Text: Allah says: "After hardship, Allah will bring about ease." Surah At-Talaq 65:7 (excerpt), in Arabic with English.'],
    ig='''حين تضيق بك الدنيا… 🤍
When the world closes in on you…

Swipe. Allah says: "After hardship, Allah will bring about ease." The walls you see now are not the end of the road.

Send this to someone carrying a heavy load right now 🤍
Follow @taqwalantern for daily reminders.

Surah At-Talaq 65:7 (excerpt). Translation: The Clear Quran® by Dr. Mustafa Khattab. Arabic text: Tanzil.net. Scenes from our Reel "Relief Will Come".

#quran #hardship #islamicreminders #islam #القرآن''',
    tt=f'''«حين تضيق بك الدنيا» 🤍
آية عن الفرج بعد الضيق: {simple_65_7}
أرسلها لمن يحمل هما ثقيلا الآن 🤍
📖 الطلاق 7 (جزء)
Quran verse about hardship and ease
#الفرج #الصبر #حسن_الظن_بالله #مقاطع_دينية #القرآن_الكريم''',
    first='''تمرّ بضيق؟ اكتب «يا رب» 🤍
Going through something? Comment «يا رب» 🤍''',
    sound='Reel 03 "With Hardship Comes Ease" (rain, thunder → dawn birds) · backup Reel 17 "Never Lose Hope"',
    when='Sat 21 Nov 9:00 AM')

P['C10'] = dict(
    folder='C10-jumuah-go-early', files=['01-mosque.jpg', '02-hours-1-3.jpg', '03-hours-4-5.jpg'], src='C10v2',
    title='يوم الجمعة: اغتسل وبكّر · Jumu\'ah',
    alt=['Animated scene at night: a mosque glows over a sleeping city, threads of golden light spreading from its minaret to every home. Title: Jumu\'ah. Text: Go early to the masjid; the earlier, the bigger the reward. Five labels, hour 1 to hour 5: camel, cow, ram, chicken, egg. Swipe for the hadith.',
         'Bathe, then go early. The Messenger of Allah ﷺ said, in Arabic with English, numbered by hour: 1, whoever takes a bath on Friday, like the bath taken from sexual impurity, and then goes is like one who offers a camel; 2, at the second hour a cow; 3, at the third hour a horned ram. Sahih al-Bukhari 881, Sahih Muslim 850.',
         'The hadith continues: 4, at the fourth hour a chicken; 5, at the fifth hour an egg. When the Imam comes out, the angels come to listen to the Dhikr. Sahih al-Bukhari 881, Sahih Muslim 850, narrated by Abu Hurayrah.'],
    ig='''يوم الجمعة… بكّر إلى المسجد 🤍
Jumu'ah: go early. The earlier, the bigger the reward.

From a camel in the first hour down to an egg in the fifth. Then the Imam comes out, and the angels come to listen.

Save it for Friday morning, and send it to someone you'll see at Jumu'ah 🤍
Follow @taqwalantern for daily reminders.

Sahih al-Bukhari 881 · Sahih Muslim 850, narrated by Abu Hurayrah (رضي الله عنه). Translation: HadeethEnc.com. Scene from our Reel "Leaving the Prayer".

#jumuah #hadith #islamicreminders #islam #الجمعة''',
    tt='''«بكر إلى الجمعة يعظم أجرك» 🤍
حديث عن فضل التبكير إلى صلاة الجمعة والاغتسال يوم الجمعة
أرسلها لمن ستراه في الجمعة 🤍
📖 صحيح البخاري 881 · صحيح مسلم 850
Hadith about going early to Jumu'ah
#يوم_الجمعة #صلاة_الجمعة #السنة #مقاطع_دينية #حديث''',
    first='''ستبكّر هذه الجمعة؟ اكتب: إن شاء الله 🤍
Going early this Friday? Comment «إن شاء الله» 🤍''',
    sound='Reel 09 "The Best Day" (our Friday sound; dawn birds, soft wind) · backup Reel 21 "Within Your Capacity"',
    when='Fri 20 Nov 12:00 AM')

for k, p in P.items():
    tags = [w for w in p['tt'].split() if w.startswith('#')]
    assert len(tags) == 5 and all(not any('a' <= c.lower() <= 'z' for c in t) for t in tags), (k, tags)
    ig_tags = [w for w in p['ig'].split() if w.startswith('#')]
    assert len(ig_tags) == 5, (k, ig_tags)
    assert len(p['alt']) == len(p['files'])
    assets = [{'image': {'url': f"{RAW}/{p['folder']}/{f}", 'metadata': {'altText': a}}} for f, a in zip(p['files'], p['alt'])]
    payload = {
        'instagram': {'channelId': IG, 'schedulingType': 'automatic', 'mode': 'shareNow', 'text': p['ig'], 'assets': assets,
                      'metadata': {'instagram': {'type': 'post', 'shouldShareToFeed': True, 'firstComment': p['first']}}},
        'tiktok': {'channelId': TT, 'schedulingType': 'automatic', 'mode': 'shareNow', 'text': p['tt'], 'assets': assets,
                   'metadata': {'tiktok': {'title': p['title']}}}}
    json.dump(payload, open(ROOT / f'post-payload-{k}.json', 'w'), ensure_ascii=False, indent=1)
json.dump(P, open(ROOT / 'data/captions.json', 'w'), ensure_ascii=False, indent=1)
print('payloads written:', list(P))
print(P['C11']['tt']); print(P['C12']['tt'])

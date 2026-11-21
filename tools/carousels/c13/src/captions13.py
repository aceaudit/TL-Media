"""Captions, alt text and docs for C13–C15. Quran/hadith English inside captions is cut by code from the
saved source files (quran.com 131 / HadeethEnc); Arabic lines in captions are our own words only."""
import json, pathlib, hashlib
C = pathlib.Path('/home/claude/c13')
R = json.load(open(C / 'data/quran_raw.json'))
T = json.load(open(C / 'data/texts.json'))
he = lambda id, l: json.load(open(C / f'data/he_{id}_{l}.json'))
sha = lambda s: hashlib.sha256(s.encode()).hexdigest()[:8] + '…'

def cut(full, a, b):
    i = full.index(a); j = full.index(b, i) + len(b); return full[i:j]

CQ = 'Translation from The Clear Quran® by Dr. Mustafa Khattab. Arabic text: Tanzil Project (tanzil.net).'
FOLLOW = 'Follow @taqwalantern for daily reminders.'
SCENE = 'Scenes from our Reel "More Merciful Than Your Mother".'
q6270 = cut(he(6270, 'en')['hadeeth'], 'Whoever visits', 'of that sickness.')
q6093 = cut(he(6093, 'en')['hadeeth'], 'Whoever says three times', 'until the evening.')
q5542 = 'When the Messenger of Allah'  # narrative intro is not quoted

cap = {}
cap['C13'] = {
 'instagram': f'''«أدعية لوالديك من القرآن» 🤍
3 du'as for your parents, from the Quran.

ثلاثة أدعية من كتاب الله، اجعلها وِردًا لك في كل صلاة لوالديك.
Three du'as from the Quran for your parents. Make them part of every prayer.

احفظها، وأرسلها لمن يحب والديه 🤍
Save this, and send it to someone who loves their parents.
{FOLLOW}

Slide 1: Al-Isra 17:24 (part). Slide 2: Ibrahim 14:41, the du'a of Ibrahim (عليه السلام). Slide 3: Nuh 71:28 (part), the du'a of Nuh (عليه السلام). {CQ} {SCENE}

#بر_الوالدين #دعاء #القرآن_الكريم #parents #dua''',
 'first_comment': 'اكتب دعاءً لوالديك 👇\nWrite a du\'a for your parents 👇',
}
cap['C14'] = {
 'instagram': f'''«مَن تحبّه مريض؟» 🤍
Is someone you love sick?

دعاءان صحيحان من السنة، لمن تحب حين يمرض.
Two authentic du'as from the Sunnah for someone you love who is unwell. Visit them if you can: the second du'a is said seven times in their presence. If you can't, make du'a for them and let them know.

احفظها، وأرسل البطاقة لمن تحب وهو مريض 🤍
Save this, and send the card to someone you love who is unwell.
{FOLLOW}

Slide 1: Sahih al-Bukhari 5750 · Sahih Muslim 2191 (‘A’ishah, رضي الله عنها). Slide 2: Sunan Abi Dawud 3106 · Jami' at-Tirmidhi 2083 (Ibn ‘Abbas, رضي الله عنهما), graded sahih: “{q6270}” Hadith English: HadeethEnc.com. {SCENE}

#دعاء #الشفاء #السنة_النبوية #dua #sunnah''',
 'first_comment': 'اكتب دعاءً لكل مريض 👇\nWrite a du\'a for everyone who is sick 👇',
}
cap['C15'] = {
 'instagram': f'''«قُلها ثلاثًا… صباحًا ومساءً» 🤍
Say it three times, morning and evening.

ذِكرٌ قصير من السنة لا يأخذ منك إلا ثوانيَ، فلا تتركه.
A short dhikr from the Sunnah that takes only seconds. The Prophet ﷺ said: “{q6093}”

احفظها لتقولها كل يوم، وأرسلها لمن تحب 🤍
Save this to say it every day, and send it to someone you love.
{FOLLOW}

Sunan Abi Dawud 5088 · Jami' at-Tirmidhi 3388 (‘Uthman ibn ‘Affan, رضي الله عنه), graded sahih (al-Albani; HadeethEnc). Hadith English: HadeethEnc.com. Scene from our Reel "More Merciful Than Your Mother".

#أذكار_الصباح #أذكار_المساء #ذكر #dhikr #sunnah''',
 'first_comment': 'هل تقولها كل يوم؟ 👇\nDo you say it every day? 👇',
 'facebook': f'''«قُلها ثلاثًا… صباحًا ومساءً» 🤍
Say it three times, morning and evening.

ذِكرٌ قصير من السنة للصباح والمساء.

A morning and evening dhikr from the Sunnah. The Prophet ﷺ said: “{q6093}”

Which morning or evening dhikr has stayed with you the longest?
Follow Taqwa Lantern for daily reminders 🤍

Sunan Abi Dawud 5088 · Jami' at-Tirmidhi 3388 (‘Uthman ibn ‘Affan, رضي الله عنه), graded sahih (al-Albani; HadeethEnc). Hadith English: HadeethEnc.com. Scene from our Reel "More Merciful Than Your Mother".

#أذكار_الصباح #dhikr #sunnah''',
 'fb_first_comment': '📖 سنن أبي داود 5088 · جامع الترمذي 3388 · Sunan Abi Dawud 5088 · Jami\' at-Tirmidhi 3388',
}
alt = {
 'C13': ['Animated scene: a mother in a blue robe and white headscarf holds her sleeping baby by a lantern at night. Title: Du\'as for your parents, from the Quran. Du\'a 1 of 3: "and pray, My Lord! Be merciful to them as they raised me when I was young." Al-Isra 17:24, in Arabic with English.',
         'Animated scene: a father in white kneels in a glowing doorway and embraces his young son. Du\'a 2 of 3, the du\'a of Ibrahim: "Our Lord! Forgive me, my parents, and the believers on the Day when the judgment will come to pass." Ibrahim 14:41, in Arabic with English.',
         'Animated scene: small houses with lit windows by a river at night. Du\'a 3 of 3, the du\'a of Nuh: "My Lord! Forgive me, my parents, and whoever enters my house in faith, and all believing men and women." Nuh 71:28, in Arabic with English. Save it and say them for your parents every day.'],
 'C14': ['Animated scene: a man in white kneels alone on a plain at dusk, a small lit house in the distance. Title: Is someone you love sick? The du\'a the Prophet said for the sick: "Remove the harm, Lord of the people, and heal, for You are the Healer. There is no healing except Your healing, a healing that leaves behind no illness." Sahih al-Bukhari 5750, Sahih Muslim 2191, in Arabic with English.',
         'A gold-bordered card to send over a blurred dusk scene. To you: "I ask Allah the Great, Lord of the great Throne, to cure you." When you visit them, say it seven times. Sunan Abi Dawud 3106, Jami\' at-Tirmidhi 2083.'],
 'C15': ['Animated scene: a man in white stands alone at sunrise on an open plain. Title: Say it three times, morning and evening. "In the name of Allah, with Whose name nothing in the earth or the heaven can cause harm, and He is the All-Hearing, the All-Knowing." Morning 3 times, evening 3 times. Sunan Abi Dawud 5088, Jami\' at-Tirmidhi 3388, in Arabic with English.'],
}
for k in cap:
    for f in ('instagram', 'facebook'):
        if f in cap[k]:
            s = cap[k][f]; tags = s.strip().split('\n')[-1].split()
            assert all(t.startswith('#') for t in tags) and len(tags) == (5 if f == 'instagram' else 3), (k, f, tags)
            assert '@' not in s or f == 'instagram'
            assert len(s) < 2200, (k, f, len(s))
json.dump({'cap': cap, 'alt': alt}, open(C / 'data/captions.json', 'w'), ensure_ascii=False, indent=1)
for k in cap: print(k, {f: len(v) for f, v in cap[k].items()})

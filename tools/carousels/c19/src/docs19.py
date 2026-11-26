import json
C=json.load(open('/home/claude/c19/data/captions.json'))
B=lambda s:'```\n'+s+'\n```'
HOW='''## How it was made
- **Style:** plain designed slides in the C01/C03/C05 look (gold arch on Night / Deep teal, girih texture, lantern mark), no Reel frames. Owner, Wed 25 Nov 11:07 PM: «Can be multiple images, by simple i meant consider no animation or simple animation. Do an analysis and give me posts that you think will do good».
- **Why:** sends and saves per person reached (ShortSync / Buffer, read Wed 25 Nov): the plain text carousels C05 (7.1% sends), C01 (3.1% sends, 3.8% saves) and C03 (1.7%) lead; every picture post from a Reel sits at 0.1–0.6% sends. Instagram weighs sends per reach most for reaching non-followers, and re-shows an unswiped carousel from slide 2.
- **Build:** `c01/src/build_c19.py` (tl.py template), Chromium at 1080×1350; hadith Arabic in Scheherazade New bold; every Arabic block checked in the page against its source string; per-slide bounds checked against the footer. One du'a per slide: label, Arabic, English, reference.'''
def doc(k,title,intro,slides,ver,src):
    c=C[k]; alt='\n'.join(f'{i+1}. {a}' for i,a in enumerate(c['alt']))
    return f'''# {k} — {title} (carousel, {len(c['alt'])} slides)

_{intro}_

## Slides
{slides}

{HOW}

## Verification
{ver}

## Sources
{src}

## Alt text
{alt}

## Instagram sound (owner adds it in the app right after posting)
- **Use / backup:** {c['sound']}

## First comment (ShortSync posts it)
{B(c['fc'])}

## Caption (Instagram only: multi-slide, so no Facebook)
{B(c['ig'])}

## Status
- Wed 25 Nov 2026, ~11:55 PM (Carousels 2): built, verified, QC'd; sent to the owner for approval. **Not uploaded or scheduled.** Proposed: **{c['slot']}** Toronto, ShortSync, Instagram.
'''
T=lambda rows:'| # | Slide |\n|---|---|\n'+'\n'.join(f'| {i+1} | {r} |' for i,r in enumerate(rows))
d={}
d['C16']=doc('C16',"Before you sleep · قبل أن تنام","Carousels 2, Wed 25 Nov 2026. Replaces the unapproved single image «دعاء موسى» (held for later; files in `/home/claude/c16/out/C16`). Format: a saveable list like C01.",
T(['Cover «قبل أن تنام» · Before you go to sleep · 4 Sunnahs of the Prophet ﷺ','1/4 As you lie down: Bukhari 6324','2/4 Al-Ikhlas · Al-Falaq · An-Nas: Bukhari 6319 (HadeethEnc 5879)','3/4 33 · 33 · 34: Bukhari 5361 · Muslim 2727 (HadeethEnc 6076)','4/4 Hand under your head: Tirmidhi 3398 (HadeethEnc 6167) · Abu Dawud 5045','Save for tonight / send / follow']),
'''- **1 (Bukhari 6324):** Arabic and English (the bracketed meaning) cut by code from sunnah.com, moved with per-string SHA-256. dorar: al-Bukhari [sahih]; al-Arna'ut «إسناده صحيح على شرط الشيخين»; al-Albani sahih (Mukhtasar ash-Shama'il 217).
- **2 (HadeethEnc 5879, first narration = Bukhari 6319):** Arabic and English by code (excerpt from «كان إذا أخذ» to «جسده»; no Quran text on the slide, only the surah names in English). Graded sahih (HadeethEnc); letters match sunnah.com Bukhari 6319.
- **3 (HadeethEnc 6076):** excerpt of the Prophet's words by code; HadeethEnc «صحيح — متفق عليه»; its wording (tasbih, tahmid 33, takbir 34) is Bukhari 5361 on sunnah.com. Bukhari 3113 / Muslim 2727 put the takbir first: same counts.
- **4 (HadeethEnc 6167):** Arabic and English by code; «تجمع أو تبعث» is the narrator's doubt, shown as given. HadeethEnc sahih; sunnah.com Tirmidhi 3398: Sahih (Darussalam). Abu Dawud 5045 (Hafsah) has «يوم تبعث عبادك», said three times.''',
'''| Item | Source 1 | Source 2 |
|---|---|---|
| 1 | https://sunnah.com/bukhari:6324 | dorar.net (al-Bukhari 6324; al-Arna'ut, Musnad 23271; al-Albani, Mukhtasar ash-Shama'il 217) |
| 2 | https://hadeethenc.com/en/browse/hadith/5879 | https://sunnah.com/bukhari:6319 · /bukhari:5017 |
| 3 | https://hadeethenc.com/en/browse/hadith/6076 | https://sunnah.com/bukhari:5361 · /muslim:2727a |
| 4 | https://hadeethenc.com/en/browse/hadith/6167 | https://sunnah.com/tirmidhi:3398 · /abudawud:5045 |''')
d['C17']=doc('C17',"Jumu'ah: at the khutbah · في خطبة الجمعة","Carousels 2, Wed 25 Nov 2026. Replaces the single-image draft; same hadith, in the C03 format (C03: 21.3K reach, 370 sends). One reminder per Friday (owner, 11 Nov).",
T(["Cover «في خطبة الجمعة» · At the Friday khutbah: even this one word · Bukhari and Muslim","The hadith (HadeethEnc 3107): Muslim 851 · Bukhari 934","Save for every Friday / send to someone you pray Jumu'ah with / follow"]),
'''- **Arabic:** HadeethEnc 3107 by code, the Prophet's words only (partly vocalised in the source; shown as given). Letters match sunnah.com Muslim 851a; Bukhari 934 has the same words in another order.
- **English:** HadeethEnc 3107 by code. **Grading:** «صحيح — متفق عليه».
- ⚠ The colon in the Arabic is drawn by the fallback font (checked by eye).''',
'''| Item | Source 1 | Source 2 |
|---|---|---|
| The hadith | https://hadeethenc.com/en/browse/hadith/3107 | https://sunnah.com/muslim:851a · https://sunnah.com/bukhari:934 |''')
d['C18']=doc('C18',"When it rains · إذا نزل المطر","Carousels 2, Wed 25 Nov 2026. Seasonal: the rains are starting across the Arab world. A saveable list people send when it rains.",
T(['Cover «إذا نزل المطر» · When it starts to rain · 3 from the Sunnah','1/3 When you see rain: Nasa\'i 1523 (Bukhari 1032 shorter)','2/3 After the rain: Bukhari 846 · Muslim 71','3/3 When the rain is too much: Bukhari 1014 · Muslim 897 (excerpt, HadeethEnc 3174)','Save for the next rain / send to someone where it\'s raining now / follow']),
'''- **1:** Arabic and English («O Allah, make it beneficial rain») by code from sunnah.com Nasa'i 1523 (Sahih, Darussalam); dorar: al-Albani sahih (Sahih an-Nasa'i 1522, Sahih al-Jami' 4725), al-'Iraqi «إسناده صحيح». Bukhari 1032 has the shorter wording without «اللهم» (HadeethEnc 65527 quotes it with «اللهم», so we use Nasa'i's text and cite both).
- **2:** the phrase cut by code from sunnah.com Bukhari 846; English is sunnah.com's sentence for it (Allah's words in the hadith qudsi), shown with «Allah said, in a hadith qudsi:» (our framing line). dorar: Muslim 71 [sahih]; al-Albani sahih (Sahih al-Jami' 7028).
- **3:** HadeethEnc 3174 (agreed upon), the first clause of the du'a only, marked excerpt; English by code.
- ⚠ For the reviewer: slide 2 shows the phrase people say after rain, with the hadith qudsi that praises it; slide 1 uses Nasa'i's wording rather than Bukhari's shorter one.''',
'''| Item | Source 1 | Source 2 |
|---|---|---|
| 1 | https://sunnah.com/nasai:1523 · https://sunnah.com/bukhari:1032 | dorar.net (al-Albani, Sahih an-Nasa'i 1522; Sahih al-Jami' 4725) · https://hadeethenc.com/en/browse/hadith/65527 |
| 2 | https://sunnah.com/bukhari:846 · https://sunnah.com/muslim:71 | dorar.net (Muslim 71; al-Albani, Sahih al-Jami' 7028) |
| 3 | https://hadeethenc.com/en/browse/hadith/3174 | https://sunnah.com/bukhari:1014 · https://sunnah.com/muslim:897a |''')
d['C19']=doc('C19',"Know someone who just got married? · تعرف أحدًا تزوّج حديثًا؟","Carousels 2, Wed 25 Nov 2026. The send-card format of C05 (7.1% sends, the best rate so far). Replaces the single-image draft.",
T(['Cover «تعرف أحدًا تزوّج حديثًا؟» · Know someone who just got married? · Send them this du\'a','The du\'a card: Abu Dawud 2130 · Tirmidhi 1091','Send / save for the next wedding / follow']),
'''- **Arabic:** sunnah.com Abu Dawud 2130 (browser fetch, base64 + SHA-256 checked), the du'a only. Same words in Tirmidhi 1091.
- **English:** sunnah.com Tirmidhi 1091 by code. **Grading:** Sahih (al-Albani, Abu Dawud 2130); Sahih (Darussalam, Tirmidhi 1091); dorar: al-Nawawi «إسناده صحيح», al-Hakim «صحيح على شرط مسلم».
- The label «كان النبي ﷺ يقول للمتزوّج» is our own wording of the narration's setting.
- ⚠ For the reviewer: the du'a is worded to a man («لكَ… عليكَ»), as narrated; kept exactly.''',
'''| Item | Source 1 | Source 2 |
|---|---|---|
| The du'a | https://sunnah.com/abudawud:2130 · https://sunnah.com/tirmidhi:1091 | dorar.net (al-Nawawi, al-Adhkar 356; al-Hakim 2783; al-Albani) |''')
for k,v in d.items(): open(f'/home/claude/c19/docs/captions-{k}.md','w').write(v)
print('ok')

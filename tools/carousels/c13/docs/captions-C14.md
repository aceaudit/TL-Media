# C14 — Is someone you love sick? · مَن تحبّه مريض؟ (picture carousel, 2 slides: du'a + card to send)

_Carousels 2, Sat 21 Nov 2026. Built on what worked: C05's send-card (highest share rate so far, ~7% of reach) and C01's practical du'a format, as a 2-slide picture post._

## Slides
| # | Picture | Text | Reference |
|---|---|---|---|
| 1 | Reel 99 at 10.5 s: a man in white kneels alone on a plain at dusk, a lit house far off | Title «مَن تحبّه مريض؟ · Is someone you love sick?» · "Two du'as from the Sunnah · swipe for the card to send" · 1 / 2 · كان النبي ﷺ يدعو للمريض · The Prophet ﷺ would say for the sick · the du'a | Sahih al-Bukhari 5750 · Sahih Muslim 2191 (‘A’ishah رضي الله عنها) |
| 2 | Same scene, blurred, under a gold-bordered card | إليك · TO YOU · the du'a · «قلها عنده سبع مرات حين تزوره / When you visit them, say it seven times» | Sunan Abi Dawud 3106 · Jami' at-Tirmidhi 2083 (Ibn ‘Abbas رضي الله عنهما) |

## How the pictures were made
- Frames from our own Reel 99 "More Merciful Than Your Mother" (1080×1920 master from Drive, via the device bridge) with ffmpeg; the Reel's subtitles are cropped away, and its on-screen words, credit box and watermark are removed (OpenCV inpainting on text pixels; a per-row blend for smooth skies) — `src/plates13.py`. No AI image tools. Faceless figures; no prophets, Companions or angels; no glowing outlines (Reel 96/97 frames were rejected for their glow).
- Text set in HTML (Amiri, Amiri Quran, Scheherazade New for hadith, Cormorant Garamond, Marcellus), rendered in Chromium at 1080×1350; every Arabic block's page text is compared with its source string before the JPEG is written (sRGB, q93). Builder: `src/build_c13.py`.

## Verification
- **Slide 1 Arabic** (excerpt: the du'a only, self-contained): HadeethEnc 5542 (Arabic API, by code): «أَذْهِبِ الْبَاسَ، رَبَّ النَّاسِ، وَاشْفِ أَنْتَ الشَّافِي، لَا شِفَاءَ إِلَّا شِفَاؤُكَ، شِفَاءً لَا يُغَادِرُ سَقَمًا». sunnah.com (browser fetch, letter compare): matches Muslim 2191a and Bukhari 5750 (Bukhari 5743 has «اشفه» instead of «واشف», so it is not cited). Grading: HadeethEnc «صحيح — متفق عليه»; in both Sahihs.
- **Slide 1 English:** HadeethEnc 5542, the bracketed translation of the du'a, by code: "Remove the harm, Lord of the people, and heal, for You are the Healer. There is no healing except Your healing, a healing that leaves behind no illness".
- **Slide 2 Arabic** (excerpt: the du'a only): HadeethEnc 6270: «أَسْأَلُ اللَّهَ الْعَظِيمَ رَبَّ الْعَرْشِ الْعَظِيمِ أَنْ يَشْفِيَكَ» — exact (diacritics included) on sunnah.com Abu Dawud 3106 and Tirmidhi 2083. Grading: Sahih (al-Albani, on sunnah.com) · Sahih (Darussalam, Tirmidhi 2083) · HadeethEnc «صحيح».
- **Slide 2 English:** HadeethEnc 6270, by code: "I ask Allah the Great, Lord of the great Throne, to cure you". The full hadith English is quoted in the caption (by code).
- Framing lines are ours: «كان النبي ﷺ يدعو للمريض» (from the narration's own setting), «قلها عنده سبع مرات حين تزوره» (as the hadith says: seven times, in his presence).
- ⚠ **For the reviewer:** the promise in Abu Dawud 3106 is for saying it seven times *in the sick person's presence*. The card is offered for sending, so the card itself says "when you visit them, say it seven times" and the caption says to visit if you can; nothing claims the promise for a text message.

## Sources
| Item | Source 1 | Source 2 |
|---|---|---|
| Du'a 1 | https://sunnah.com/muslim:2191a · https://sunnah.com/bukhari:5750 | https://hadeethenc.com/en/browse/hadith/5542 |
| Du'a 2 | https://sunnah.com/abudawud:3106 · https://sunnah.com/tirmidhi:2083 | https://hadeethenc.com/en/browse/hadith/6270 |

## QC
- Rendered Arabic == source for both blocks (DOM check). Set in Scheherazade New bold (every mark visible; Amiri bold hides some tashkeel). HarfBuzz: no missing glyphs. Zoomed: shadda and kasra of رَبَّ / الشَّافِي, maddah-less الْبَاسَ as in the source. Text inside margins, clear of the footer.

## Alt text
1. Animated scene: a man in white kneels alone on a plain at dusk, a small lit house in the distance. Title: Is someone you love sick? The du'a the Prophet said for the sick: "Remove the harm, Lord of the people, and heal, for You are the Healer. There is no healing except Your healing, a healing that leaves behind no illness." Sahih al-Bukhari 5750, Sahih Muslim 2191, in Arabic with English.
2. A gold-bordered card to send over a blurred dusk scene. To you: "I ask Allah the Great, Lord of the great Throne, to cure you." When you visit them, say it seven times. Sunan Abi Dawud 3106, Jami' at-Tirmidhi 2083.

## Instagram sound (owner adds it in the app right after posting)
- **Use / backup:** Reel 17 "Never Lose Hope" (rain easing → dawn birds) · backup Reel 01 "Patience and Prayer" (soft rain)

## First comment (ShortSync posts it)
```
اكتب دعاءً لكل مريض 👇
Write a du'a for everyone who is sick 👇
```

## Captions
**Instagram** (no Facebook: multi-slide)
```
«مَن تحبّه مريض؟» 🤍
Is someone you love sick?

دعاءان صحيحان من السنة، لمن تحب حين يمرض.
Two authentic du'as from the Sunnah for someone you love who is unwell. Visit them if you can: the second du'a is said seven times in their presence. If you can't, make du'a for them and let them know.

احفظها، وأرسل البطاقة لمن تحب وهو مريض 🤍
Save this, and send the card to someone you love who is unwell.
Follow @taqwalantern for daily reminders.

Slide 1: Sahih al-Bukhari 5750 · Sahih Muslim 2191 (‘A’ishah, رضي الله عنها). Slide 2: Sunan Abi Dawud 3106 · Jami' at-Tirmidhi 2083 (Ibn ‘Abbas, رضي الله عنهما), graded sahih: “Whoever visits a sick person whose time of death has not yet come, and says seven times in his presence: 'As’alullāh al-‘azhīm Rabb al-‘arshi al-‘azhīm an yashfiyak (I ask Allah the Great, Lord of the great Throne, to cure you),' except that Allah will cure him of that sickness.” Hadith English: HadeethEnc.com. Scenes from our Reel "More Merciful Than Your Mother".

#دعاء #الشفاء #السنة_النبوية #dua #sunnah
```

## Status
- Sat 21 Nov 2026, ~1:45 AM (Carousels 2): built, verified, QC'd; sent to the owner for approval. **Not uploaded or scheduled.** Proposed: **Mon 23 Nov 9:00 AM Toronto**, ShortSync, Instagram only.

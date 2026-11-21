# C15 — Morning & evening protection · قُلها ثلاثًا صباحًا ومساءً (picture post, 1 image)

_Carousels 2, Sat 21 Nov 2026. Built on what worked: C11 (single image, best of the picture posts so far) and C01's save-worthy du'a. Goes to Instagram and Facebook (1 slide)._

## Slide
| # | Picture | Text | Reference |
|---|---|---|---|
| 1 | Reel 99 at 53 s: a man in white stands alone at sunrise on an open plain | Title «قُلها ثلاثًا… صباحًا ومساءً · Say it three times, morning and evening» · قال رسول الله ﷺ · The Prophet ﷺ taught · the dhikr · pills «الصباح MORNING · 3» «المساء EVENING · 3» | Sunan Abi Dawud 5088 · Jami' at-Tirmidhi 3388 (‘Uthman ibn ‘Affan رضي الله عنه) |

## How the pictures were made
- Frames from our own Reel 99 "More Merciful Than Your Mother" (1080×1920 master from Drive, via the device bridge) with ffmpeg; the Reel's subtitles are cropped away, and its on-screen words, credit box and watermark are removed (OpenCV inpainting on text pixels; a per-row blend for smooth skies) — `src/plates13.py`. No AI image tools. Faceless figures; no prophets, Companions or angels; no glowing outlines (Reel 96/97 frames were rejected for their glow).
- Text set in HTML (Amiri, Amiri Quran, Scheherazade New for hadith, Cormorant Garamond, Marcellus), rendered in Chromium at 1080×1350; every Arabic block's page text is compared with its source string before the JPEG is written (sRGB, q93). Builder: `src/build_c13.py`.

## Verification
- **Arabic** (excerpt: the dhikr only, self-contained): HadeethEnc 6093 (Arabic API, by code): «بِسْمِ اللَّهِ الَّذِي لَا يَضُرُّ مَعَ اسْمِهِ شَيْءٌ، فِي الْأَرْضِ، وَلَا فِي السَّمَاءِ، وَهُوَ السَّمِيعُ الْعَلِيمُ». sunnah.com (browser fetch, letter compare): matches Tirmidhi 3388; Abu Dawud 5088 the same words (sunnah.com spells شَىْءٌ with alif maqsura). HadeethEnc's wording (لم تصبه فجأة بلاء) is Abu Dawud's, so Abu Dawud is cited first.
- **English:** HadeethEnc 6093, by code: "In the name of Allah, with Whose name nothing in the earth or the heaven can cause harm, and He is the All-Hearing, the All-Knowing". The promise (HadeethEnc English, by code) is quoted in the captions, not on the image.
- **Grading:** Sahih (al-Albani, Abu Dawud 5088 on sunnah.com) · Hasan (Darussalam, Tirmidhi 3388) · HadeethEnc «صحيح».
- "Morning ×3 · evening ×3" is our framing of the hadith (three times; in the morning, and the evening).

## Sources
| Item | Source 1 | Source 2 |
|---|---|---|
| The dhikr | https://sunnah.com/abudawud:5088 · https://sunnah.com/tirmidhi:3388 | https://hadeethenc.com/en/browse/hadith/6093 |

## QC
- Rendered Arabic == source (DOM check). Scheherazade New bold: the tanween of شَيْءٌ reads clearly (Amiri bold draws it like a hamza). HarfBuzz: no missing glyphs. Text clear of the figure and the footer.

## Alt text
1. Animated scene: a man in white stands alone at sunrise on an open plain. Title: Say it three times, morning and evening. "In the name of Allah, with Whose name nothing in the earth or the heaven can cause harm, and He is the All-Hearing, the All-Knowing." Morning 3 times, evening 3 times. Sunan Abi Dawud 5088, Jami' at-Tirmidhi 3388, in Arabic with English.

## Instagram sound (owner adds it in the app right after posting)
- **Use / backup:** Reel 21 "Within Your Capacity" (wind, dawn birds) · backup Reel 09 "The Best Day" (dawn birds)

## First comments (ShortSync posts them)
Instagram:
```
هل تقولها كل يوم؟ 👇
Do you say it every day? 👇
```
Facebook:
```
📖 سنن أبي داود 5088 · جامع الترمذي 3388 · Sunan Abi Dawud 5088 · Jami' at-Tirmidhi 3388
```

## Captions
**Instagram**
```
«قُلها ثلاثًا… صباحًا ومساءً» 🤍
Say it three times, morning and evening.

ذِكرٌ قصير من السنة لا يأخذ منك إلا ثوانيَ، فلا تتركه.
A short dhikr from the Sunnah that takes only seconds. The Prophet ﷺ said: “Whoever says three times: 'In the name of Allah, with Whose name nothing in the earth or the heaven can cause harm, and He is the All-Hearing, the All-Knowing' will not suffer sudden affliction until the morning; and whoever says it in the morning three times will not suffer sudden affliction until the evening.”

احفظها لتقولها كل يوم، وأرسلها لمن تحب 🤍
Save this to say it every day, and send it to someone you love.
Follow @taqwalantern for daily reminders.

Sunan Abi Dawud 5088 · Jami' at-Tirmidhi 3388 (‘Uthman ibn ‘Affan, رضي الله عنه), graded sahih (al-Albani; HadeethEnc). Hadith English: HadeethEnc.com. Scene from our Reel "More Merciful Than Your Mother".

#أذكار_الصباح #أذكار_المساء #ذكر #dhikr #sunnah
```

**Facebook** (formula in `claude/hashtags.md`; no engagement bait)
```
«قُلها ثلاثًا… صباحًا ومساءً» 🤍
Say it three times, morning and evening.

ذِكرٌ قصير من السنة للصباح والمساء.

A morning and evening dhikr from the Sunnah. The Prophet ﷺ said: “Whoever says three times: 'In the name of Allah, with Whose name nothing in the earth or the heaven can cause harm, and He is the All-Hearing, the All-Knowing' will not suffer sudden affliction until the morning; and whoever says it in the morning three times will not suffer sudden affliction until the evening.”

Which morning or evening dhikr has stayed with you the longest?
Follow Taqwa Lantern for daily reminders 🤍

Sunan Abi Dawud 5088 · Jami' at-Tirmidhi 3388 (‘Uthman ibn ‘Affan, رضي الله عنه), graded sahih (al-Albani; HadeethEnc). Hadith English: HadeethEnc.com. Scene from our Reel "More Merciful Than Your Mother".

#أذكار_الصباح #dhikr #sunnah
```

## Status
- Sat 21 Nov 2026, ~1:45 AM (Carousels 2): built, verified, QC'd; sent to the owner for approval. **Not uploaded or scheduled.** Proposed: **Tue 24 Nov 9:00 AM Toronto**, ShortSync, Instagram + Facebook (1 slide).

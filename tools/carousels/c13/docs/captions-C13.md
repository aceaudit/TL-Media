# C13 — Du'as for your parents · أدعية لوالديك من القرآن (picture carousel, 3 slides)

_Carousels 2, Sat 21 Nov 2026. Built on what worked: C01's "du'as for …" list (best saves and shares so far) as a short picture carousel (owner: 1–3 slides, pictures from our Reels; slide 1 names the topic)._

## Slides
| # | Picture | Text | Reference |
|---|---|---|---|
| 1 | Reel 99 at 34 s: a mother holds her sleeping baby by a lantern | Title «أدعية لوالديك من القرآن · 3 du'as for your parents, from the Quran» · 1 / 3 · قال الله تعالى · Allah says · the verse | Al-Isra 17:24 (part), from «وَقُل» |
| 2 | Reel 99 at 23.3 s: a father kneels in a glowing doorway and embraces his son | 2 / 3 · دعاء إبراهيم عليه السلام · The du'a of Ibrahim · the verse | Ibrahim 14:41 (whole verse) |
| 3 | Reel 99 at 22.6 s: houses with lit windows by a river at night | 3 / 3 · دعاء نوح عليه السلام · The du'a of Nuh · the verse · «احفظها وادعُ بها لهما كل يوم / Save it, and say them for your parents every day» · Send it to someone who loves their parents 🤍 | Nuh 71:28 (part), up to «وَٱلْمُؤْمِنَـٰتِ» |

## How the pictures were made
- Frames from our own Reel 99 "More Merciful Than Your Mother" (1080×1920 master from Drive, via the device bridge) with ffmpeg; the Reel's subtitles are cropped away, and its on-screen words, credit box and watermark are removed (OpenCV inpainting on text pixels; a per-row blend for smooth skies) — `src/plates13.py`. No AI image tools. Faceless figures; no prophets, Companions or angels; no glowing outlines (Reel 96/97 frames were rejected for their glow).
- Text set in HTML (Amiri, Amiri Quran, Scheherazade New for hadith, Cormorant Garamond, Marcellus), rendered in Chromium at 1080×1350; every Arabic block's page text is compared with its source string before the JPEG is written (sRGB, q93). Builder: `src/build_c13.py`.

## Verification
- **Arabic:** Tanzil Uthmani (quran-validator data) by code; identical to quran.com `text_uthmani` (api.quran.com v4) for all three verses (byte compare). Excerpts cut by whole words in code: 17:24 from «وَقُل»; 71:28 up to «وَٱلْمُؤْمِنَـٰتِ» (10 words).
- **English (The Clear Quran, quran.com translation 131, extracted by code):** 17:24 part «and pray, “My Lord! Be merciful to them as they raised me when I was young.”» · 14:41 «Our Lord! Forgive me, my parents, and the believers on the Day when the judgment will come to pass.» (display drops the closing ” whose opening quote is in 14:35; nothing else changed) · 71:28 part «My Lord! Forgive me, my parents, and whoever enters my house in faith, and ˹all˺ believing men and women.». Same wording on alim.org (Mustafa Khattab; alim shows ˹all˺ as 'all').
- Labels are ours: «قال الله تعالى» on 17:24 (Allah's command, "and pray…"); 14:41 is Ibrahim's du'a, 71:28 is Nuh's du'a (عليهما السلام), as the verses' context says. No prophet is depicted.

## Sources
| Item | Source 1 | Source 2 |
|---|---|---|
| 17:24 (part) | Tanzil Uthmani · https://quran.com/17/24?translations=131 | https://www.alim.org/quran/compare/surah/17/24/ |
| 14:41 | Tanzil Uthmani · https://quran.com/14/41?translations=131 | https://www.alim.org/quran/compare/surah/14/41/ |
| 71:28 (part) | Tanzil Uthmani · https://quran.com/71/28?translations=131 | https://www.alim.org/quran/compare/surah/71/28/ |

## QC
- Rendered Arabic == source for all 3 verse blocks (DOM check). HarfBuzz (Amiri Quran): no missing glyphs. Verses viewed zoomed: every mark present (shadda of رَّبِّ, the dagger alif of وَلِوَٰلِدَىَّ, ayah ornaments ٢٤ / ٤١ / ٢٨). All text inside the margins, clear of the footer. Title without tanween (Amiri bold).

## Alt text
1. Animated scene: a mother in a blue robe and white headscarf holds her sleeping baby by a lantern at night. Title: Du'as for your parents, from the Quran. Du'a 1 of 3: "and pray, My Lord! Be merciful to them as they raised me when I was young." Al-Isra 17:24, in Arabic with English.
2. Animated scene: a father in white kneels in a glowing doorway and embraces his young son. Du'a 2 of 3, the du'a of Ibrahim: "Our Lord! Forgive me, my parents, and the believers on the Day when the judgment will come to pass." Ibrahim 14:41, in Arabic with English.
3. Animated scene: small houses with lit windows by a river at night. Du'a 3 of 3, the du'a of Nuh: "My Lord! Forgive me, my parents, and whoever enters my house in faith, and all believing men and women." Nuh 71:28, in Arabic with English. Save it and say them for your parents every day.

## Instagram sound (owner adds it in the app right after posting)
- **Use / backup:** Reel 19 "I Am Near" (crickets, night wind: du'a, night) · backup Reel 01 "Patience and Prayer" (soft rain)

## First comment (ShortSync posts it)
```
اكتب دعاءً لوالديك 👇
Write a du'a for your parents 👇
```

## Captions
**Instagram** (no Facebook: multi-slide)
```
«أدعية لوالديك من القرآن» 🤍
3 du'as for your parents, from the Quran.

ثلاثة أدعية من كتاب الله، اجعلها وِردًا لك في كل صلاة لوالديك.
Three du'as from the Quran for your parents. Make them part of every prayer.

احفظها، وأرسلها لمن يحب والديه 🤍
Save this, and send it to someone who loves their parents.
Follow @taqwalantern for daily reminders.

Slide 1: Al-Isra 17:24 (part). Slide 2: Ibrahim 14:41, the du'a of Ibrahim (عليه السلام). Slide 3: Nuh 71:28 (part), the du'a of Nuh (عليه السلام). Translation from The Clear Quran® by Dr. Mustafa Khattab. Arabic text: Tanzil Project (tanzil.net). Scenes from our Reel "More Merciful Than Your Mother".

#بر_الوالدين #دعاء #القرآن_الكريم #parents #dua
```

## Status
- Sat 21 Nov 2026, ~1:45 AM (Carousels 2): built, verified, QC'd; sent to the owner for approval. **Not uploaded or scheduled.** Proposed: **Sun 22 Nov 9:00 AM Toronto**, ShortSync, Instagram only.

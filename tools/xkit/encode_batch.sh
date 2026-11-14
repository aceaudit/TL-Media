#!/bin/bash
# usage: encode_batch.sh file1.mp4 file2.mp4 ...  (names as in TL-Media history)
mkdir -p "${XK:-/home/claude/xkit}/out" "${XK:-/home/claude/xkit}/src"
cd "${TLM:-/home/claude/tl-media}"
for f in "$@"; do
  n=${f%.mp4}; n=$(echo "$n" | sed -E 's/-v[0-9]+$//')
  out=${XK:-/home/claude/xkit}/out/x-$n.mp4
  [ -s "$out" ] && { echo "skip $n"; continue; }
  if git cat-file -e origin/main:$f 2>/dev/null; then ref=origin/main; else c=$(git log origin/main --no-renames -n1 --format=%h -- $f); ref=$c^; fi
  git show $ref:$f > ${XK:-/home/claude/xkit}/src/cur.mp4 || { echo "FAIL get $f"; continue; }
  d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 ${XK:-/home/claude/xkit}/src/cur.mp4)
  ffmpeg -nostdin -v error -y -i ${XK:-/home/claude/xkit}/src/cur.mp4 -c:v libx264 -preset veryfast -profile:v high -crf 21 -maxrate 10M -bufsize 20M -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 -c:a aac -b:a 160k -ar 48000 -movflags +faststart "$out" && echo "done $n $d $(stat -c %s $out)"
  rm -f ${XK:-/home/claude/xkit}/src/cur.mp4
done

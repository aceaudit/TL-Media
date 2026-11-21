"""Clean 1080x1350 plates for C13-C15 from our own Reel frames (99, 96, 97).
Text from the Reels (subtitles, on-screen words, credit line, watermark) is removed:
- 'light' bands: inpaint pixels lighter than the local background (text is always lighter);
- 'interp' rects: replace with a per-row linear blend of the pixels left and right of the rect (smooth skies)."""
import subprocess, json, sys
import numpy as np, cv2
V = '/home/claude/tl-media'; OUT = '/home/claude/c13/plates'
def frame(v, t):
    raw = f'{OUT}/raw-{v}-{t}.png'
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',f'{V}/{v}.mp4','-frames:v','1',raw],check=True)
    return cv2.imread(raw)
def light(im, y0, y1, th=9, x0=0, x1=1080):
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    a, b = max(0, y0-40), min(g.shape[0], y1+40)
    band = g[a:b]; bg = cv2.medianBlur(band, 41)
    d = ((band.astype(int)-bg.astype(int)) > th).astype(np.uint8)[y0-a:y1-a]
    m = np.zeros(g.shape, np.uint8); m[y0:y1, x0:x1] = d[:, x0:x1]
    return m
def interp(im, y0, y1, x0, x1, w=24):
    out = im.copy().astype(np.float32)
    L = im[y0:y1, max(0,x0-w):x0].mean(1); R = im[y0:y1, x1:x1+w].mean(1)
    t = np.linspace(0, 1, x1-x0)[None, :, None]
    out[y0:y1, x0:x1] = L[:, None, :]*(1-t) + R[:, None, :]*t
    return out.astype(np.uint8)
if __name__ == '__main__':
    jobs = json.load(open(sys.argv[1]))
    for j in jobs:
        im = frame(j['v'], j['t'])
        for r in j.get('interp', []): im = interp(im, *r)
        mask = np.zeros(im.shape[:2], np.uint8)
        for b in j.get('light', []): mask |= light(im, *b)
        mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11)))
        out = cv2.inpaint(im, mask*255, 11, cv2.INPAINT_TELEA) if mask.any() else im
        y0 = j['y0']; crop = out[y0:y0+1350]; assert crop.shape[:2] == (1350, 1080)
        cv2.imwrite(f"{OUT}/{j['name']}.png", crop); cv2.imwrite(f"{OUT}/{j['name']}-mask.png", mask[y0:y0+1350]*255)
        print(j['name'], int(mask.sum()))

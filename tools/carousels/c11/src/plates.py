"""Clean plates from our own Reel frames: remove the Reel's burned-in subtitles, credit line and
watermark (inpainting), then crop a 1080x1350 window. Our own text is laid over these later."""
import subprocess, sys, glob, json
import numpy as np, cv2
V = '/home/claude/tl-media'
OUT = '/home/claude/c11/plates'
BANDS = [(1436, 1510, 9), (1512, 1625, 8)]   # credit line(s) and watermark; the subtitle band is cropped away

def frame(v, t):
    p = glob.glob(f'{V}/{v}-*.mp4')[0]
    raw = f'{OUT}/raw-{v}-{t}.png'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(t), '-i', p, '-frames:v', '1', raw], check=True)
    return cv2.imread(raw)

def clean(im):
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    mask = np.zeros(g.shape, np.uint8)
    for y0, y1, th in BANDS:
        band = g[y0 - 40:y1 + 40]
        bg = cv2.medianBlur(band, 41)
        # the Reel's text is always lighter than what is behind it (cream, gold, or dimmed grey)
        d = ((band.astype(int) - bg.astype(int)) > th).astype(np.uint8)[40:-40]
        d[:, :30] = 0; d[:, -30:] = 0
        mask[y0:y1] |= d
    mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11)))
    out = cv2.inpaint(im, mask * 255, 11, cv2.INPAINT_TELEA)
    return out, mask

if __name__ == '__main__':
    jobs = json.loads(sys.argv[1])   # [[name, video, time, y0]]
    for name, v, t, y0 in jobs:
        im = frame(v, t)
        out, mask = clean(im)
        cv2.imwrite(f'{OUT}/{name}-full.png', out)
        cv2.imwrite(f'{OUT}/{name}-mask.png', mask * 255)
        crop = out[y0:y0 + 1350]
        assert crop.shape[:2] == (1350, 1080)
        cv2.imwrite(f'{OUT}/{name}.png', crop)
        print(name, v, t, 'masked px', int(mask.sum()))

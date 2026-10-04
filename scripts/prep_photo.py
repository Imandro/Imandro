"""Uso: python scripts/prep_photo.py foto.jpg [salida.png]
Recorta cabeza y hombros, separa el sujeto del fondo (rembg si está instalado,
si no GrabCut de OpenCV), realza contraste local (CLAHE) y deja el fondo en blanco."""
import sys
import cv2
import numpy as np

src = sys.argv[1]; dst = sys.argv[2] if len(sys.argv) > 2 else "source-prepped.png"
img = cv2.imread(src)
h, w = img.shape[:2]
img = img[int(h * 0.07):int(h * 0.50), int(w * 0.10):int(w * 0.90)]   # cabeza y hombros
img = cv2.resize(img, None, fx=1000 / img.shape[1], fy=1000 / img.shape[1], interpolation=cv2.INTER_AREA)
h, w = img.shape[:2]
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

try:                                         # opción 1: rembg (mejor calidad)
    from rembg import remove
    fg = remove(img)[:, :, 3] > 128
except Exception:                            # opción 2: GrabCut
    bg = np.median(np.concatenate([gray[:30, :30].ravel(), gray[:30, -30:].ravel()]))
    mask = np.where(np.abs(gray.astype(float) - bg) < 22, cv2.GC_PR_BGD, cv2.GC_PR_FGD).astype("uint8")
    mask[:25, :] = cv2.GC_BGD; mask[:, :12] = np.where(mask[:, :12] == cv2.GC_PR_BGD, cv2.GC_BGD, mask[:, :12])
    mask[:, -12:] = np.where(mask[:, -12:] == cv2.GC_PR_BGD, cv2.GC_BGD, mask[:, -12:])
    mask[int(h * .55):, int(w * .30):int(w * .70)] = cv2.GC_FGD          # torso central
    mask[int(h * .25):int(h * .50), int(w * .35):int(w * .65)] = cv2.GC_FGD  # cara
    cv2.grabCut(img, mask, None, np.zeros((1, 65)), np.zeros((1, 65)), 6, cv2.GC_INIT_WITH_MASK)
    fg = (mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD)
    fg = cv2.morphologyEx(fg.astype("uint8"), cv2.MORPH_OPEN, np.ones((5, 5), "uint8")) > 0
    fg = cv2.morphologyEx(fg.astype("uint8"), cv2.MORPH_CLOSE, np.ones((9, 9), "uint8")) > 0

# contraste local + nitidez
g = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(6, 6)).apply(gray)
blur = cv2.GaussianBlur(g, (0, 0), 3)
g = cv2.addWeighted(g, 1.8, blur, -0.8, 0)
g = (255 * (np.clip(g, 0, 255) / 255) ** 1.35).astype("uint8")
g[~fg] = 255
cv2.imwrite(dst, g)
print("OK:", dst, g.shape[::-1])

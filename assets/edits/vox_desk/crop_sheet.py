#!/usr/bin/env python3
"""Crop the objects of a photo sheet (plain white background) into separate RGB files, reading order: top row left to right, then the next row.
usage: crop_sheet.py SHEET.png OUTDIR name1 name2 ...   Then cut each out: ~/.venvs/doordhan-cut/bin/python pipeline/cutout.py OUTDIR/name.png OUT.png"""
import sys, os, numpy as np, cv2
sheet, outdir, names = sys.argv[1], sys.argv[2], sys.argv[3:]
im = cv2.imread(sheet, cv2.IMREAD_COLOR); g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
non = (g < 246).astype(np.uint8) * 255; non = cv2.morphologyEx(non, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8)); big = cv2.dilate(non, np.ones((61, 61), np.uint8))
n, lab, st, cen = cv2.connectedComponentsWithStats(big, 8)
comps = sorted([i for i in range(1, n) if st[i, cv2.CC_STAT_AREA] > 30000], key=lambda i: st[i, cv2.CC_STAT_AREA], reverse=True)[:len(names)]
rows = sorted(comps, key=lambda i: cen[i][1]); k = len(names) // 2 if len(names) > 3 else len(names)
order = sorted(rows[:k], key=lambda i: cen[i][0]) + sorted(rows[k:], key=lambda i: cen[i][0])
os.makedirs(outdir, exist_ok=True)
for name, i in zip(names, order):
    x, y, w, h = st[i, 0], st[i, 1], st[i, 2], st[i, 3]; m = 30
    cv2.imwrite(os.path.join(outdir, name + ".png"), im[max(0, y - m):y + h + m, max(0, x - m):x + w + m]); print(name, w, h)

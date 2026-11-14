import json, datetime as dt, numpy as np
from PIL import Image
G = json.load(open('geo.json')); out = {}
def idx(g, date):
    t = int(dt.datetime(*date, tzinfo=dt.timezone.utc).timestamp()); ts = [b[0] for b in g['bars']]
    return min(range(len(ts)), key=lambda i: abs(ts[i] - t))
for k, g in G.items():
    im = np.asarray(Image.open(f'{k}_w.png').convert('RGB')).astype(int); r, gg = im[..., 0], im[..., 1]
    col = ((r - gg > 60) & (r > 150)) | ((gg - r > 40) & (gg > 120)); col[:100, :] = False; col[:, 640:] = False
    ys, xs = np.nonzero(col[:760]); top = ys.min(); xt = xs[ys == top].mean()
    (p1, y1), (p2, y2) = sorted((float(p), v) for p, v in g['yOf'].items()); a = (y2 - y1) / (p2 - p1); b = y1 - a * p1
    vis = g['bars'][g['i0']:g['iLast'] + 1]; imax = int(np.argmax([v[2] for v in vis])) + g['i0']; hmax = g['bars'][imax][2]
    header = top - (a * hmax + b); xoff = xt - (g['x0'] + (imax - g['i0']) * g['bs'])
    X = lambda i, g=g, xoff=xoff: g['x0'] + (i - g['i0']) * g['bs'] + xoff; Y = lambda p, a=a, b=b, header=header: a * p + b + header
    out[k] = {"img": f"img/{k}_w2.png", "w": 724, "h": 906, "header": round(header, 1), "xoff": round(xoff, 1),
              "lastX": X(g['iLast']), "lastY": Y(g['last'])}
    print(k, 'header', round(header, 1), 'xoff', round(xoff, 1), 'lastX', round(X(g['iLast'])))
    globals()[f'X_{k}'], globals()[f'Y_{k}'], globals()[f'I_{k}'] = X, Y, (lambda d, g=g: idx(g, d))
R = 640
out['centum']['marks'] = {"res": {"x1": X_centum(I_centum((2026, 9, 7))), "x2": R, "y": Y_centum(5000)},
                          "sup": {"x1": X_centum(I_centum((2026, 6, 8))), "x2": R, "y": Y_centum(3450)}}
out['mtar']['marks'] = {"run": {"x1": X_mtar(I_mtar((2026, 3, 16))), "y1": Y_mtar(3309), "x2": X_mtar(I_mtar((2026, 6, 15))), "y2": Y_mtar(8714)},
                        "box": {"x1": X_mtar(I_mtar((2026, 5, 18))) - 3, "x2": R, "y1": Y_mtar(8450), "y2": Y_mtar(5250)}}
out['cgpower']['marks'] = {"res": {"x1": X_cgpower(I_cgpower((2026, 6, 1))), "x2": R, "y": Y_cgpower(975)},
                           "sup": {"x1": X_cgpower(I_cgpower((2026, 9, 28))), "x2": R, "y": Y_cgpower(775)}}
out['kaynes']['marks'] = {"res": {"x1": X_kaynes(I_kaynes((2026, 7, 27))), "x2": R, "y": Y_kaynes(4000)},
                          "sup": {"x1": X_kaynes(I_kaynes((2026, 5, 11))), "x2": R, "y": Y_kaynes(3050)}}
for k in out: print(k, {m: {kk: round(vv) for kk, vv in v.items()} for m, v in out[k].get('marks', {}).items()})
json.dump(out, open('../rm/public/data/charts.json', 'w'), indent=1)

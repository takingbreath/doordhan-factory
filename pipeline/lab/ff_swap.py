"""Face-only swap with FaceFusion's models (yoloface, arcface, hyperswap/inswapper, bisenet, gfpgan).

Every pixel outside the swapped face region comes from the source video.
usage: ff_swap.py SOURCE_FACE.png TARGET.mp4 OUT.mp4 [--swapper hyperswap|inswapper] [--enhance 0.8] [--start 0] [--dur 10]
"""
import argparse, os, subprocess, sys, tempfile
import cv2, numpy as np, onnxruntime as ort

M = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models')
T = {
    'arcface_112_v2': np.array([[0.34191607, 0.46157411], [0.65653393, 0.45983393], [0.500225, 0.64050536], [0.37097589, 0.82469196], [0.63151696, 0.82325089]]),
    'arcface_128': np.array([[0.36167656, 0.40387734], [0.63696719, 0.40235469], [0.50019687, 0.56044219], [0.38710391, 0.72160547], [0.61507734, 0.72034453]]),
    'ffhq_512': np.array([[0.37691676, 0.46864664], [0.62285697, 0.46912813], [0.50123859, 0.61331904], [0.39308822, 0.72541100], [0.61150205, 0.72490465]]),
}
opt = ort.SessionOptions(); opt.log_severity_level = 3
def sess(n): return ort.InferenceSession(os.path.join(M, n + '.onnx'), opt, providers=['CPUExecutionProvider'])

def warp(frame, kps, tmpl, size):
    A = cv2.estimateAffinePartial2D(kps, T[tmpl] * size, method=cv2.RANSAC, ransacReprojThreshold=100)[0]
    return cv2.warpAffine(frame, A, (size, size), borderMode=cv2.BORDER_REPLICATE, flags=cv2.INTER_AREA), A

class Detector:
    def __init__(s): s.m = sess('yoloface_8n')
    def __call__(s, frame, thr=0.5):
        h, w = frame.shape[:2]; r = min(640 / h, 640 / w)
        img = cv2.resize(frame, (int(w * r), int(h * r)))
        can = np.zeros((640, 640, 3), np.float32); can[:img.shape[0], :img.shape[1]] = img
        x = ((can - 127.5) / 128.0).transpose(2, 0, 1)[None]
        o = s.m.run(None, {'input': x})[0][0].T
        o = o[o[:, 4] > thr]
        if not len(o): return None
        b = o[np.argmax(o[:, 2] * o[:, 3])]   # largest face: one person per shot
        kps = b[5:].reshape(5, 3)[:, :2] / r
        return kps, float(b[4]), float(b[2] / r)

class Embedder:
    def __init__(s): s.m = sess('arcface_w600k_r50')
    def __call__(s, frame, kps):
        c, _ = warp(frame, kps, 'arcface_112_v2', 112)
        x = (c[:, :, ::-1] / 127.5 - 1).transpose(2, 0, 1)[None].astype(np.float32)
        e = s.m.run(None, {'input': x})[0].ravel()
        return e, e / np.linalg.norm(e)

class Swapper:
    def __init__(s, kind):
        s.kind = kind
        if kind == 'hyperswap':
            s.m, s.size = sess('hyperswap_1a_256'), 256
        else:
            import onnx
            s.m, s.size = sess('inswapper_128'), 128
            s.emap = onnx.numpy_helper.to_array(onnx.load(os.path.join(M, 'inswapper_128.onnx')).graph.initializer[-1])
    def source(s, emb, normed):
        if s.kind == 'hyperswap': return normed.reshape(1, -1).astype(np.float32)
        v = emb.reshape(1, -1) @ s.emap; return (v / np.linalg.norm(v)).astype(np.float32)
    def __call__(s, crop, src):
        rgb = crop[:, :, ::-1] / 255.0
        if s.kind == 'hyperswap':
            x = ((rgb - 0.5) / 0.5).transpose(2, 0, 1)[None].astype(np.float32)
            out, mask = s.m.run(None, {'source': src, 'target': x})
            out = (out[0].transpose(1, 2, 0) * 0.5 + 0.5)
            return (np.clip(out, 0, 1) * 255)[:, :, ::-1].astype(np.uint8), np.clip(mask[0, 0], 0, 1)
        out = s.m.run(None, {'target': rgb.transpose(2, 0, 1)[None].astype(np.float32), 'source': src})[0]
        return (np.clip(out[0].transpose(1, 2, 0), 0, 1) * 255)[:, :, ::-1].astype(np.uint8), None

class Parser:   # bisenet face regions: keep the source's hair, hands and anything over the face
    KEEP = [1, 2, 3, 4, 5, 10, 11, 12, 13]   # skin, brows, eyes, nose, mouth, lips
    def __init__(s): s.m = sess('bisenet_resnet_34')
    def __call__(s, crop):
        x = cv2.resize(crop, (512, 512))[:, :, ::-1] / 255.0
        x = ((x - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]).transpose(2, 0, 1)[None].astype(np.float32)
        lab = s.m.run(None, {'input': x})[0][0].argmax(0)
        m = np.isin(lab, s.KEEP).astype(np.float32)
        m = cv2.GaussianBlur(cv2.erode(m, np.ones((5, 5))), (0, 0), 5)
        return cv2.resize(m, crop.shape[1::-1])

class Enhancer:
    def __init__(s): s.m = sess('gfpgan_1.4')
    def __call__(s, frame, kps, blend):
        c, A = warp(frame, kps, 'ffhq_512', 512)
        x = ((c[:, :, ::-1] / 255.0 - 0.5) / 0.5).transpose(2, 0, 1)[None].astype(np.float32)
        o = s.m.run(None, {'input': x})[0][0].transpose(1, 2, 0)
        o = (np.clip((o + 1) / 2, 0, 1) * 255)[:, :, ::-1].astype(np.uint8)
        return paste(frame, cv2.addWeighted(c, 1 - blend, o, blend, 0), A, box_mask(512, 0.1))

def box_mask(size, blur=0.3, pad=0.0):
    m = np.ones((size, size), np.float32); b = max(1, int(size * blur * 0.5)); p = int(size * pad)
    m[:max(b, p)] = 0; m[-max(b, 1):] = 0; m[:, :b] = 0; m[:, -b:] = 0
    return cv2.GaussianBlur(m, (0, 0), b * 0.5) if b > 1 else m

def paste(frame, crop, A, mask):
    h, w = frame.shape[:2]; inv = cv2.invertAffineTransform(A)
    big = cv2.warpAffine(crop, inv, (w, h), borderMode=cv2.BORDER_REPLICATE)
    m = cv2.warpAffine(mask, inv, (w, h))[:, :, None]
    return (big * m + frame * (1 - m)).astype(np.uint8)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('source'); ap.add_argument('target'); ap.add_argument('out')
    ap.add_argument('--swapper', default='hyperswap'); ap.add_argument('--enhance', type=float, default=0.8)
    ap.add_argument('--start', type=float, default=0); ap.add_argument('--dur', type=float, default=0)
    a = ap.parse_args()
    det, emb, sw, par = Detector(), Embedder(), Swapper(a.swapper), Parser()
    enh = Enhancer() if a.enhance > 0 else None
    src_img = cv2.imread(a.source); d = det(src_img)
    if d is None: sys.exit('no face in source image')
    e, en = emb(src_img, d[0]); src = sw.source(e, en)
    cap = cv2.VideoCapture(a.target); fps = cap.get(cv2.CAP_PROP_FPS)
    cap.set(cv2.CAP_PROP_POS_MSEC, a.start * 1000)
    w, h = int(cap.get(3)), int(cap.get(4)); n = int(a.dur * fps) if a.dur else 10 ** 9
    tmp = tempfile.mkdtemp(); silent = os.path.join(tmp, 'v.mp4')
    vw = cv2.VideoWriter(silent, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
    i = miss = 0
    while i < n:
        ok, f = cap.read()
        if not ok: break
        d = det(f)
        if d is None: miss += 1
        else:
            crop, A = warp(f, d[0], 'arcface_128', sw.size)
            out, smask = sw(crop, src)
            m = box_mask(sw.size, 0.3) * par(crop)
            if smask is not None: m = m * cv2.GaussianBlur(smask, (0, 0), 2)
            f = paste(f, out, A, m)
            if enh: f = enh(f, d[0], a.enhance)
        vw.write(f); i += 1
        if i % 30 == 0: print(f'{i} frames, {miss} without a face', flush=True)
    vw.release()
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', silent, '-ss', str(a.start), '-t', str(i / fps), '-i', a.target,
                    '-map', '0:v', '-map', '1:a?', '-c:v', 'libx264', '-crf', '16', '-pix_fmt', 'yuv420p', '-c:a', 'aac', a.out], check=True)
    print(f'done: {i} frames, {miss} without a face ->', a.out)

if __name__ == '__main__':
    main()

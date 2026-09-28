"""Shared face analysis for the QC tools: MediaPipe Face Landmarker (478 points, blendshapes, head pose) and an
AuraFace-v1 identity embedding (ArcFace-style, Apache-2.0, from Hugging Face fal/AuraFace-v1; the InsightFace
buffalo models are non-commercial, so not used). Models live in assets/models (git-ignored); fetch them with
pipeline/fetch_models.sh."""
import math, os, subprocess
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANDMARKER = os.path.join(ROOT, "assets", "models", "face_landmarker.task")
EMBEDDER = os.path.join(ROOT, "assets", "models", "auraface_glintr100.onnx")
ARC_TEMPLATE = np.array([[38.2946, 51.6963], [73.5318, 51.5014], [56.0252, 71.7366],
                         [41.5493, 92.3655], [70.7299, 92.2041]], np.float32)
_lm = None; _emb = None


def load_rgb(path, t=None, width=720):
    """an image file, or a video frame at time t, as an RGB array scaled to `width`"""
    from PIL import Image
    if os.path.splitext(path)[1].lower() in (".png", ".jpg", ".jpeg", ".webp"):
        im = Image.open(path).convert("RGB")
    else:
        from common import FFMPEG
        raw = subprocess.run([FFMPEG, "-v", "error", "-ss", f"{t or 0:.3f}", "-i", path, "-frames:v", "1",
                              "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
        import io
        im = Image.open(io.BytesIO(raw)).convert("RGB")
    if width and im.width != width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    return np.asarray(im)


def landmarker():
    global _lm
    if _lm is None:
        from mediapipe.tasks.python import vision, BaseOptions
        _lm = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=LANDMARKER), running_mode=vision.RunningMode.IMAGE,
            num_faces=4, output_face_blendshapes=True, output_facial_transformation_matrixes=True,
            min_face_detection_confidence=0.3))
    return _lm


def analyse(rgb):
    """all faces in the image, largest first: points (px), box, blendshapes, pose (deg)"""
    import mediapipe as mp
    res = landmarker().detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(rgb)))
    H, W = rgb.shape[:2]; faces = []
    for i, lms in enumerate(res.face_landmarks):
        p = np.array([[q.x * W, q.y * H] for q in lms])
        x0, y0 = p.min(0); x1, y1 = p.max(0)
        bs = {c.category_name: c.score for c in res.face_blendshapes[i]} if res.face_blendshapes else {}
        R = np.array(res.facial_transformation_matrixes[i])[:3, :3] if res.facial_transformation_matrixes else np.eye(3)
        pitch = math.degrees(math.atan2(R[2, 1], R[2, 2]))
        yaw = math.degrees(math.asin(max(-1, min(1, -R[2, 0]))))
        roll = math.degrees(math.atan2(R[1, 0], R[0, 0]))
        faces.append({"points": p, "box": (x0, y0, x1, y1), "area": (x1 - x0) * (y1 - y0), "blend": bs,
                      "pose": {"yaw": yaw, "pitch": pitch, "roll": roll}})
    return sorted(faces, key=lambda f: -f["area"])


def five_points(p):
    """eye centres (iris), nose tip, mouth corners, ordered image-left then image-right"""
    eyes = sorted([p[468], p[473]], key=lambda q: q[0])
    mouth = sorted([p[61], p[291]], key=lambda q: q[0])
    return np.array([eyes[0], eyes[1], p[1], mouth[0], mouth[1]], np.float32)


def embed(rgb, face):
    import cv2, onnxruntime as ort
    global _emb
    if _emb is None:
        _emb = ort.InferenceSession(EMBEDDER, providers=["CPUExecutionProvider"])
    M, _ = cv2.estimateAffinePartial2D(five_points(face["points"]), ARC_TEMPLATE, method=cv2.LMEDS)
    crop = cv2.warpAffine(rgb, M, (112, 112), borderValue=0).astype(np.float32)
    x = ((crop - 127.5) / 127.5).transpose(2, 0, 1)[None]
    v = _emb.run(None, {_emb.get_inputs()[0].name: x})[0][0]
    return v / np.linalg.norm(v)


def gaze(face):
    """where the eyes point, from the eyeLook blendshapes (0..1 each), in image terms: left/right as seen in the
    frame, plus down/up. The subject's right eye looking out and left eye looking in both mean image-left."""
    b = face["blend"]
    g = lambda *k: float(np.mean([b.get(x, 0.0) for x in k]))
    return {"left": g("eyeLookOutRight", "eyeLookInLeft"), "right": g("eyeLookInRight", "eyeLookOutLeft"),
            "down": g("eyeLookDownLeft", "eyeLookDownRight"), "up": g("eyeLookUpLeft", "eyeLookUpRight")}


def mouth_open(face):
    """inner-lip gap / mouth width (0 closed; talking peaks ~0.2-0.3)"""
    p = face["points"]
    return float(np.linalg.norm(p[13] - p[14]) / (np.linalg.norm(p[61] - p[291]) + 1e-6))

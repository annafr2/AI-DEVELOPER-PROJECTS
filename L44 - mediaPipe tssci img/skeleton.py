"""
skeleton.py — MediaPipe Pose extraction using Tasks API (mediapipe >= 0.10).
Downloads the pose landmarker model automatically on first run.
"""
import os
import urllib.request
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python as mp_tasks
from mediapipe.tasks.python import vision as mp_vision
from PIL import Image
from config import CONNECTIONS, SKELETON_GIF

# Pose Landmarker model (lite = ~5 MB, fast)
MODEL_PATH = "pose_landmarker.task"
MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/"
    "pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task"
)


def _ensure_model() -> None:
    """Download the .task model file if it is not already present."""
    if not os.path.exists(MODEL_PATH):
        print(f"Downloading pose landmarker model → {MODEL_PATH}  (~5 MB) ...")
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
        print("Model downloaded.")


def _build_landmarker() -> mp_vision.PoseLandmarker:
    """Create a PoseLandmarker instance for frame-by-frame (IMAGE mode) inference."""
    _ensure_model()
    opts = mp_vision.PoseLandmarkerOptions(
        base_options=mp_tasks.BaseOptions(model_asset_path=MODEL_PATH),
        running_mode=mp_vision.RunningMode.IMAGE,
        num_poses=1,
        min_pose_detection_confidence=0.5,
        min_pose_presence_confidence=0.5,
        min_tracking_confidence=0.5,
    )
    return mp_vision.PoseLandmarker.create_from_options(opts)


def extract_skeletons(video_path: str) -> list:
    """
    Run MediaPipe Pose on every frame (Tasks API).
    Returns list of dicts: {landmarks: np.array (33, 3), frame_idx: int}
    Columns: [x_norm, y_norm, visibility]  — values in [0, 1]
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError(f"Cannot open video: {video_path}")

    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Video has {total} frames. Processing with MediaPipe...")

    results = []
    frame_idx = 0
    landmarker = _build_landmarker()

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        detection = landmarker.detect(mp_img)

        lm = np.zeros((33, 3), dtype=np.float32)
        if detection.pose_landmarks:
            for i, lmk in enumerate(detection.pose_landmarks[0][:33]):
                vis = float(getattr(lmk, "visibility", 1.0) or 0.0)
                lm[i] = [lmk.x, lmk.y, vis]

        results.append({
            "landmarks": lm,
            "frame_idx": frame_idx,
            "shape": frame.shape,
        })
        frame_idx += 1
        if frame_idx % 30 == 0:
            print(f"  Processed {frame_idx}/{total} frames...")

    landmarker.close()
    cap.release()
    print(f"Extracted {len(results)} frames from video.")
    return results


def draw_skeleton_on_frame(frame: np.ndarray, landmarks: np.ndarray) -> np.ndarray:
    """Draw skeleton landmarks and connections on a copy of the BGR frame."""
    h, w = frame.shape[:2]
    overlay = frame.copy()
    for a, b in CONNECTIONS:
        if landmarks[a, 2] > 0.3 and landmarks[b, 2] > 0.3:
            pt1 = (int(landmarks[a, 0] * w), int(landmarks[a, 1] * h))
            pt2 = (int(landmarks[b, 0] * w), int(landmarks[b, 1] * h))
            cv2.line(overlay, pt1, pt2, (255, 200, 0), 2)
    for i in range(33):
        if landmarks[i, 2] > 0.3:
            cv2.circle(overlay,
                       (int(landmarks[i, 0] * w), int(landmarks[i, 1] * h)),
                       4, (0, 255, 128), -1)
    return overlay


def save_skeleton_gif(
    skeleton_data: list,
    video_path: str,
    output_path=SKELETON_GIF,
    max_frames: int = 60,
) -> None:
    """Save a GIF of skeleton overlaid on sampled original video frames."""
    cap = cv2.VideoCapture(video_path)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    indices = np.linspace(0, total - 1, min(max_frames, total), dtype=int)

    pil_frames = []
    for idx in indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(idx))
        ret, bgr = cap.read()
        if not ret or int(idx) >= len(skeleton_data):
            continue
        lm = skeleton_data[int(idx)]["landmarks"]
        overlay = draw_skeleton_on_frame(bgr, lm)
        rgb = cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB)
        pil_frames.append(Image.fromarray(rgb).resize((320, 240)))

    cap.release()
    if pil_frames:
        pil_frames[0].save(
            output_path, save_all=True,
            append_images=pil_frames[1:], loop=0, duration=80,
        )
        print(f"Skeleton GIF saved: {output_path}")

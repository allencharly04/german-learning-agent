"""
camera_vision.py — Real-time German vision assistant

Mode 1 — Live Object Detection: streamlit-webrtc + YOLO processes every Nth frame,
          overlays German labels with article colour coding in real time.

Mode 2 — OCR Translation: capture a frame, run EasyOCR, translate German text.

Mode 3 — Photo upload: fallback for when webcam isn't available.

Install:
    pip install ultralytics easyocr opencv-python-headless Pillow numpy
    pip install streamlit-webrtc av

For mobile (HTTPS required for camera):
    openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/CN=localhost"
    streamlit run app.py --server.sslCertFile cert.pem --server.sslKeyFile key.pem
"""

import os
import io
import json
import threading
import numpy as np
from PIL import Image, ImageDraw

# ── German translations for COCO-80 + extended common objects ─────────────────
COCO_DE = {
    "person": ("die Person", "die", "Person"),
    "bicycle": ("das Fahrrad", "das", "Fahrrad"),
    "car": ("das Auto", "das", "Auto"),
    "motorcycle": ("das Motorrad", "das", "Motorrad"),
    "airplane": ("das Flugzeug", "das", "Flugzeug"),
    "bus": ("der Bus", "der", "Bus"),
    "train": ("der Zug", "der", "Zug"),
    "truck": ("der Lastwagen", "der", "Lastwagen"),
    "boat": ("das Boot", "das", "Boot"),
    "traffic light": ("die Ampel", "die", "Ampel"),
    "fire hydrant": ("der Hydrant", "der", "Hydrant"),
    "stop sign": ("das Stoppschild", "das", "Stoppschild"),
    "bench": ("die Bank", "die", "Bank"),
    "bird": ("der Vogel", "der", "Vogel"),
    "cat": ("die Katze", "die", "Katze"),
    "dog": ("der Hund", "der", "Hund"),
    "horse": ("das Pferd", "das", "Pferd"),
    "sheep": ("das Schaf", "das", "Schaf"),
    "cow": ("die Kuh", "die", "Kuh"),
    "elephant": ("der Elefant", "der", "Elefant"),
    "bear": ("der Bär", "der", "Bär"),
    "zebra": ("das Zebra", "das", "Zebra"),
    "giraffe": ("die Giraffe", "die", "Giraffe"),
    "backpack": ("der Rucksack", "der", "Rucksack"),
    "umbrella": ("der Regenschirm", "der", "Regenschirm"),
    "handbag": ("die Handtasche", "die", "Handtasche"),
    "tie": ("die Krawatte", "die", "Krawatte"),
    "suitcase": ("der Koffer", "der", "Koffer"),
    "bottle": ("die Flasche", "die", "Flasche"),
    "wine glass": ("das Weinglas", "das", "Weinglas"),
    "cup": ("die Tasse", "die", "Tasse"),
    "fork": ("die Gabel", "die", "Gabel"),
    "knife": ("das Messer", "das", "Messer"),
    "spoon": ("der Löffel", "der", "Löffel"),
    "bowl": ("die Schüssel", "die", "Schüssel"),
    "banana": ("die Banane", "die", "Banane"),
    "apple": ("der Apfel", "der", "Apfel"),
    "sandwich": ("das Sandwich", "das", "Sandwich"),
    "orange": ("die Orange", "die", "Orange"),
    "broccoli": ("der Brokkoli", "der", "Brokkoli"),
    "carrot": ("die Karotte", "die", "Karotte"),
    "hot dog": ("das Hotdog", "das", "Hotdog"),
    "pizza": ("die Pizza", "die", "Pizza"),
    "donut": ("der Donut", "der", "Donut"),
    "cake": ("der Kuchen", "der", "Kuchen"),
    "chair": ("der Stuhl", "der", "Stuhl"),
    "couch": ("das Sofa", "das", "Sofa"),
    "potted plant": ("die Topfpflanze", "die", "Topfpflanze"),
    "bed": ("das Bett", "das", "Bett"),
    "dining table": ("der Esstisch", "der", "Esstisch"),
    "toilet": ("die Toilette", "die", "Toilette"),
    "tv": ("der Fernseher", "der", "Fernseher"),
    "laptop": ("der Laptop", "der", "Laptop"),
    "mouse": ("die Maus", "die", "Maus"),
    "remote": ("die Fernbedienung", "die", "Fernbedienung"),
    "keyboard": ("die Tastatur", "die", "Tastatur"),
    "cell phone": ("das Handy", "das", "Handy"),
    "microwave": ("die Mikrowelle", "die", "Mikrowelle"),
    "oven": ("der Backofen", "der", "Backofen"),
    "toaster": ("der Toaster", "der", "Toaster"),
    "sink": ("das Waschbecken", "das", "Waschbecken"),
    "refrigerator": ("der Kühlschrank", "der", "Kühlschrank"),
    "book": ("das Buch", "das", "Buch"),
    "clock": ("die Uhr", "die", "Uhr"),
    "vase": ("die Vase", "die", "Vase"),
    "scissors": ("die Schere", "die", "Schere"),
    "teddy bear": ("der Teddybär", "der", "Teddybär"),
    "hair drier": ("der Föhn", "der", "Föhn"),
    "toothbrush": ("die Zahnbürste", "die", "Zahnbürste"),
    "sports ball": ("der Ball", "der", "Ball"),
    "skateboard": ("das Skateboard", "das", "Skateboard"),
    "surfboard": ("das Surfbrett", "das", "Surfbrett"),
    "tennis racket": ("der Tennisschläger", "der", "Tennisschläger"),
    "skis": ("die Skier", "die", "Skier"),
    "snowboard": ("das Snowboard", "das", "Snowboard"),
    "kite": ("der Drachen", "der", "Drachen"),
    "baseball bat": ("der Baseballschläger", "der", "Baseballschläger"),
    "frisbee": ("die Frisbee", "die", "Frisbee"),
    "parking meter": ("der Parkscheinautomat", "der", "Parkscheinautomat"),
    "stop sign": ("das Stoppschild", "das", "Stoppschild"),
    "traffic light": ("die Ampel", "die", "Ampel"),
}

# Article → BGR colour for OpenCV drawing
ARTICLE_BGR = {
    "der": (217, 141, 91),   # blue
    "die": (126, 83, 212),   # pink/purple
    "das": (106, 158, 91),   # green
    "":    (182, 89, 155),   # fallback purple
}

# ── Lazy model loaders (thread-safe) ─────────────────────────────────────────
_yolo_model = None
_yolo_lock = threading.Lock()

_ocr_reader = None
_ocr_lock = threading.Lock()


def get_yolo():
    global _yolo_model
    with _yolo_lock:
        if _yolo_model is None:
            try:
                from ultralytics import YOLO
                _yolo_model = YOLO("yolov8n.pt")
                _yolo_model.fuse()  # speed optimisation
            except Exception as e:
                return None, str(e)
    return _yolo_model, None


def get_ocr():
    global _ocr_reader
    with _ocr_lock:
        if _ocr_reader is None:
            try:
                import easyocr
                _ocr_reader = easyocr.Reader(
                    ['de', 'en'], gpu=False, verbose=False
                )
            except Exception as e:
                return None, str(e)
    return _ocr_reader, None


# ── Frame processor for streamlit-webrtc ─────────────────────────────────────
class GermanVisionTransformer:
    """
    VideoTransformerBase for streamlit-webrtc.
    Runs YOLO every `process_every` frames, caches boxes between frames
    for smooth overlay without stutter.
    """

    def __init__(self, process_every=3, conf=0.40):
        self.process_every = process_every
        self.conf = conf
        self.frame_count = 0
        self.last_detections = []   # cached from last YOLO run
        self.latest_frame = None    # store latest numpy frame for capture
        self._lock = threading.Lock()

    def recv(self, frame):
        import av
        import cv2

        img = frame.to_ndarray(format="bgr24")
        self.frame_count += 1

        # Store latest frame for snapshot capture
        with self._lock:
            self.latest_frame = img.copy()

        # Run YOLO every Nth frame
        if self.frame_count % self.process_every == 0:
            model, err = get_yolo()
            if model and not err:
                results = model(img, conf=self.conf, verbose=False)
                dets = []
                seen = set()
                for r in results:
                    for box in r.boxes:
                        label_en = model.names[int(box.cls[0])].lower()
                        if label_en in seen:
                            continue
                        seen.add(label_en)
                        de_info = COCO_DE.get(label_en)
                        if de_info:
                            label_de, article, word = de_info
                        else:
                            label_de, article, word = label_en, "", label_en
                        x1, y1, x2, y2 = [int(v) for v in box.xyxy[0].tolist()]
                        conf_val = float(box.conf[0])
                        dets.append({
                            "label_de": label_de,
                            "label_en": label_en,
                            "article": article,
                            "word": word,
                            "conf": conf_val,
                            "bbox": (x1, y1, x2, y2),
                        })
                with self._lock:
                    self.last_detections = dets

        # Draw cached detections on every frame (smooth)
        with self._lock:
            dets_to_draw = list(self.last_detections)

        annotated = self._draw_boxes(img, dets_to_draw)
        return av.VideoFrame.from_ndarray(annotated, format="bgr24")

    def _draw_boxes(self, img, detections):
        import cv2

        for det in detections:
            x1, y1, x2, y2 = det["bbox"]
            article = det["article"]
            color = ARTICLE_BGR.get(article, ARTICLE_BGR[""])
            label = det["label_de"]
            conf_pct = int(det["conf"] * 100)

            # Bounding box
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

            # Label background
            text = f"{label} ({conf_pct}%)"
            (tw, th), baseline = cv2.getTextSize(
                text, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 1
            )
            label_y = max(y1 - 4, th + 4)
            cv2.rectangle(
                img,
                (x1, label_y - th - baseline - 4),
                (x1 + tw + 8, label_y + baseline - 4),
                color, -1
            )
            # Text
            cv2.putText(
                img, text,
                (x1 + 4, label_y - 4),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55,
                (255, 255, 255), 1, cv2.LINE_AA
            )

            # Article indicator dot top-right of box
            dot_colors = {
                "der": (217, 141, 91),
                "die": (126, 83, 212),
                "das": (106, 158, 91),
            }
            if article in dot_colors:
                cv2.circle(img, (x2 - 8, y1 + 8), 6, dot_colors[article], -1)

        # Legend bottom-left
        legend = [("der", (217,141,91)), ("die",(126,83,212)), ("das",(106,158,91))]
        lx, ly = 10, img.shape[0] - 10
        for art, col in reversed(legend):
            cv2.circle(img, (lx + 6, ly - 6), 6, col, -1)
            cv2.putText(img, art, (lx + 16, ly), cv2.FONT_HERSHEY_SIMPLEX,
                       0.5, (255,255,255), 1, cv2.LINE_AA)
            ly -= 22

        return img

    def get_latest_frame(self):
        with self._lock:
            if self.latest_frame is not None:
                return self.latest_frame.copy()
        return None

    def get_latest_detections(self):
        with self._lock:
            return list(self.last_detections)


# ── Still image detection (upload / snapshot) ─────────────────────────────────
def detect_objects_still(pil_image, conf=0.35):
    """Run YOLO on a still PIL image. Returns (detections, error)."""
    model, err = get_yolo()
    if err:
        return [], f"YOLO not available: {err}"

    img_array = np.array(pil_image.convert("RGB"))
    # Convert RGB → BGR for YOLO
    import cv2
    img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

    results = model(img_bgr, conf=conf, verbose=False)
    detections = []
    seen = set()
    for r in results:
        for box in r.boxes:
            label_en = model.names[int(box.cls[0])].lower()
            if label_en in seen:
                continue
            seen.add(label_en)
            de_info = COCO_DE.get(label_en)
            if de_info:
                label_de, article, word = de_info
            else:
                label_de, article, word = label_en, "", label_en
            x1, y1, x2, y2 = [int(v) for v in box.xyxy[0].tolist()]
            detections.append({
                "label_de": label_de,
                "label_en": label_en,
                "article": article,
                "word": word,
                "confidence": round(float(box.conf[0]), 2),
                "bbox": [x1, y1, x2, y2],
            })
    return detections, None


def draw_still_boxes(pil_image, detections):
    """Draw boxes on a PIL image and return annotated PIL image."""
    import cv2
    img = np.array(pil_image.convert("RGB"))
    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    transformer = GermanVisionTransformer()
    annotated = transformer._draw_boxes(img_bgr, [
        {**d, "conf": d["confidence"], "bbox": tuple(d["bbox"])}
        for d in detections
    ])
    return Image.fromarray(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB))


# ── OCR + Translation ─────────────────────────────────────────────────────────
def read_text_from_image(pil_image):
    reader, err = get_ocr()
    if err:
        return [], f"EasyOCR not available: {err}"

    img_array = np.array(pil_image.convert("RGB"))
    results = reader.readtext(img_array, paragraph=False)

    texts = []
    for (bbox_pts, text, conf) in results:
        if conf > 0.3 and len(text.strip()) > 1:
            xs = [p[0] for p in bbox_pts]
            ys = [p[1] for p in bbox_pts]
            texts.append({
                "text": text.strip(),
                "confidence": round(conf, 2),
                "bbox": [int(min(xs)), int(min(ys)), int(max(xs)), int(max(ys))]
            })
    return texts, None


def translate_texts(texts, llm_module):
    if not texts:
        return texts
    german_words = [t["text"] for t in texts]
    batch = "\n".join([f"{i+1}. {w}" for i, w in enumerate(german_words)])
    prompt = f"""Translate these German words/phrases to English.
They are text fragments from a real-world image (labels, signs, menus, ingredients).
Reply ONLY with a JSON array: [{{"de": "original", "en": "translation"}}]
No extra text, no markdown.

{batch}"""
    msgs = [{"role": "user", "content": prompt}]
    system = "You are a precise German-English translator. Reply only with valid JSON arrays."
    try:
        response = llm_module.chat(msgs, system=system).strip()
        if response.startswith("```"):
            response = response.split("```")[1]
            if response.startswith("json"):
                response = response[4:]
        translations = json.loads(response)
        trans_map = {item["de"]: item["en"] for item in translations}
        for t in texts:
            t["translation"] = trans_map.get(t["text"], t["text"])
    except Exception:
        for t in texts:
            t["translation"] = "(translation unavailable)"
    return texts


def draw_ocr_boxes(pil_image, texts):
    img = pil_image.convert("RGBA")
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for item in texts:
        x1, y1, x2, y2 = item["bbox"]
        draw.rectangle([x1, y1, x2, y2], outline=(186, 117, 23, 255), width=2)
        label = f"→ {item.get('translation', '')}"
        if label and label != "→ ":
            lw = len(label) * 7 + 12
            draw.rectangle([x1, y2, x1 + lw, y2 + 20], fill=(186, 117, 23, 220))
            draw.text((x1 + 6, y2 + 2), label, fill=(255, 255, 255, 255))
    return Image.alpha_composite(img, overlay).convert("RGB")


# ── Helpers ───────────────────────────────────────────────────────────────────
def to_pil(source):
    if isinstance(source, Image.Image):
        return source
    if hasattr(source, "read"):
        return Image.open(source)
    return Image.open(io.BytesIO(source))


def numpy_to_pil(frame_bgr):
    import cv2
    rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    return Image.fromarray(rgb)


def check_dependencies():
    status = {}
    for pkg, key in [("ultralytics", "yolo"), ("easyocr", "easyocr"),
                     ("cv2", "opencv"), ("streamlit_webrtc", "webrtc"), ("av", "av")]:
        try:
            __import__(pkg)
            status[key] = True
        except ImportError:
            status[key] = False
    return status

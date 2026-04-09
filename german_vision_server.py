"""
German Vision Server — adapted from agent 6 (camera object agent)
- YOLO-World detects 200+ objects
- Returns German labels + articles alongside English
- WebSocket server: browser sends JPEG frames, server returns detections
- Detections saved to german.db SRS deck via /save_word HTTP endpoint

Run:
    python german_vision_server.py
Then visit http://192.168.0.35:8764 in your browser (or phone)
"""

import asyncio
import websockets
import json
import numpy as np
import cv2
import socket
import logging
import time
import base64
import sqlite3
import os
from datetime import date
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from ultralytics import YOLOWorld

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

# ── Config ────────────────────────────────────────────────────────────────────
MODEL_PATH = "yolov8s-worldv2.pt"
CONFIDENCE = 0.28
MAX_DETS   = 25
WS_PORT    = 8765
HTTP_PORT  = 8764
DB_PATH    = os.path.join(os.path.dirname(__file__), "data", "german.db")
# ─────────────────────────────────────────────────────────────────────────────

# ── German label dictionary — all 200+ YOLO-World vocab entries ───────────────
# Format: "english_label": ("die/der/das GermanWord", "article")
GERMAN = {
    # People & body
    "person":       ("die Person",        "die"),
    "man":          ("der Mann",          "der"),
    "woman":        ("die Frau",          "die"),
    "child":        ("das Kind",          "das"),
    "hand":         ("die Hand",          "die"),
    "face":         ("das Gesicht",       "das"),
    "finger":       ("der Finger",        "der"),
    # Fruit & veg
    "apple":        ("der Apfel",         "der"),
    "banana":       ("die Banane",        "die"),
    "orange":       ("die Orange",        "die"),
    "grape":        ("die Traube",        "die"),
    "strawberry":   ("die Erdbeere",      "die"),
    "lemon":        ("die Zitrone",       "die"),
    "watermelon":   ("die Wassermelone",  "die"),
    "mango":        ("die Mango",         "die"),
    "avocado":      ("die Avocado",       "die"),
    "peach":        ("der Pfirsich",      "der"),
    "pear":         ("die Birne",         "die"),
    "carrot":       ("die Karotte",       "die"),
    "broccoli":     ("der Brokkoli",      "der"),
    "potato":       ("die Kartoffel",     "die"),
    "tomato":       ("die Tomate",        "die"),
    "cucumber":     ("die Gurke",         "die"),
    "corn":         ("der Mais",          "der"),
    "onion":        ("die Zwiebel",       "die"),
    "garlic":       ("der Knoblauch",     "der"),
    "pepper":       ("die Paprika",       "die"),
    "lettuce":      ("der Salat",         "der"),
    "mushroom":     ("der Pilz",          "der"),
    # Baked goods & fast food
    "bread":        ("das Brot",          "das"),
    "toast":        ("der Toast",         "der"),
    "croissant":    ("das Croissant",     "das"),
    "bagel":        ("der Bagel",         "der"),
    "pizza":        ("die Pizza",         "die"),
    "burger":       ("der Burger",        "der"),
    "hot dog":      ("das Hotdog",        "das"),
    "sandwich":     ("das Sandwich",      "das"),
    "wrap":         ("der Wrap",          "der"),
    "pasta":        ("die Pasta",         "die"),
    "rice":         ("der Reis",          "der"),
    "noodles":      ("die Nudeln",        "die"),
    "soup":         ("die Suppe",         "die"),
    "salad":        ("der Salat",         "der"),
    "egg":          ("das Ei",            "das"),
    "cake":         ("der Kuchen",        "der"),
    "cookie":       ("der Keks",          "der"),
    "donut":        ("der Donut",         "der"),
    "muffin":       ("der Muffin",        "der"),
    "chocolate bar":("die Schokolade",    "die"),
    "cheese":       ("der Käse",          "der"),
    "butter":       ("die Butter",        "die"),
    "yogurt":       ("der Joghurt",       "der"),
    "ice cream":    ("das Eis",           "das"),
    # Packaged food
    "pringles can": ("die Pringles-Dose", "die"),
    "chips bag":    ("die Chipstüte",     "die"),
    "cereal box":   ("die Müslischachtel","die"),
    "instant noodles packet": ("die Instantnudeln", "die"),
    "rice packet":  ("die Reispackung",   "die"),
    "snack bag":    ("die Snacktüte",     "die"),
    "candy":        ("die Süßigkeit",     "die"),
    "granola bar":  ("der Müsliriegel",   "der"),
    "biscuit packet":("die Kekspackung",  "die"),
    "chocolate box":("die Pralinenschachtel","die"),
    "popcorn bag":  ("die Popcorntüte",   "die"),
    "fish tin":     ("die Fischdose",     "die"),
    "canned food":  ("die Konserve",      "die"),
    "jar":          ("das Glas",          "das"),
    # Drinks
    "water bottle": ("die Wasserflasche", "die"),
    "plastic bottle":("die Plastikflasche","die"),
    "glass bottle": ("die Glasflasche",   "die"),
    "wine bottle":  ("die Weinflasche",   "die"),
    "beer can":     ("die Bierdose",      "die"),
    "soda can":     ("die Sodadose",      "die"),
    "energy drink can":("die Energydrinkdose","die"),
    "cup":          ("die Tasse",         "die"),
    "mug":          ("der Becher",        "der"),
    "coffee cup":   ("die Kaffeetasse",   "die"),
    "tea cup":      ("die Teetasse",      "die"),
    "drinking glass":("das Trinkglas",    "das"),
    "wine glass":   ("das Weinglas",      "das"),
    "juice box":    ("der Saftkarton",    "der"),
    "milk carton":  ("der Milchkarton",   "der"),
    "thermos":      ("die Thermoskanne",  "die"),
    "flask":        ("die Flasche",       "die"),
    "kettle":       ("der Wasserkocher",  "der"),
    "pitcher":      ("der Krug",          "der"),
    # Kitchen
    "plate":        ("der Teller",        "der"),
    "bowl":         ("die Schüssel",      "die"),
    "tray":         ("das Tablett",       "das"),
    "pan":          ("die Pfanne",        "die"),
    "pot":          ("der Topf",          "der"),
    "cutting board":("das Schneidebrett", "das"),
    "spoon":        ("der Löffel",        "der"),
    "fork":         ("die Gabel",         "die"),
    "knife":        ("das Messer",        "das"),
    "chopsticks":   ("die Stäbchen",      "die"),
    "spatula":      ("der Spatel",        "der"),
    "toaster":      ("der Toaster",       "der"),
    "microwave":    ("die Mikrowelle",    "die"),
    "blender":      ("der Mixer",         "der"),
    "coffee machine":("die Kaffeemaschine","die"),
    "refrigerator": ("der Kühlschrank",   "der"),
    "oven":         ("der Backofen",      "der"),
    "sink":         ("das Waschbecken",   "das"),
    # Electronics
    "laptop":       ("der Laptop",        "der"),
    "computer monitor":("der Monitor",    "der"),
    "keyboard":     ("die Tastatur",      "die"),
    "mouse":        ("die Maus",          "die"),
    "smartphone":   ("das Smartphone",    "das"),
    "mobile phone": ("das Handy",         "das"),
    "tablet":       ("das Tablet",        "das"),
    "headphones":   ("die Kopfhörer",     "die"),
    "earphones":    ("die Ohrhörer",      "die"),
    "bluetooth speaker":("der Lautsprecher","der"),
    "camera":       ("die Kamera",        "die"),
    "television":   ("der Fernseher",     "der"),
    "remote control":("die Fernbedienung","die"),
    "charger":      ("das Ladegerät",     "das"),
    "power bank":   ("die Powerbank",     "die"),
    "usb cable":    ("das USB-Kabel",     "das"),
    "usb drive":    ("der USB-Stick",     "der"),
    "printer":      ("der Drucker",       "der"),
    "router":       ("der Router",        "der"),
    "smartwatch":   ("die Smartwatch",    "die"),
    "calculator":   ("der Taschenrechner","der"),
    # Furniture & room
    "chair":        ("der Stuhl",         "der"),
    "sofa":         ("das Sofa",          "das"),
    "couch":        ("das Sofa",          "das"),
    "stool":        ("der Hocker",        "der"),
    "bench":        ("die Bank",          "die"),
    "table":        ("der Tisch",         "der"),
    "desk":         ("der Schreibtisch",  "der"),
    "shelf":        ("das Regal",         "das"),
    "bookcase":     ("das Bücherregal",   "das"),
    "bed":          ("das Bett",          "das"),
    "pillow":       ("das Kissen",        "das"),
    "blanket":      ("die Decke",         "die"),
    "door":         ("die Tür",           "die"),
    "window":       ("das Fenster",       "das"),
    "curtain":      ("der Vorhang",       "der"),
    "lamp":         ("die Lampe",         "die"),
    "mirror":       ("der Spiegel",       "der"),
    "clock":        ("die Uhr",           "die"),
    "picture frame":("der Bilderrahmen",  "der"),
    "vase":         ("die Vase",          "die"),
    "plant":        ("die Pflanze",       "die"),
    "trash can":    ("der Mülleimer",     "der"),
    "box":          ("die Schachtel",     "die"),
    "basket":       ("der Korb",          "der"),
    # Personal items & clothing
    "backpack":     ("der Rucksack",      "der"),
    "handbag":      ("die Handtasche",    "die"),
    "wallet":       ("das Portemonnaie",  "das"),
    "suitcase":     ("der Koffer",        "der"),
    "glasses":      ("die Brille",        "die"),
    "sunglasses":   ("die Sonnenbrille",  "die"),
    "watch":        ("die Uhr",           "die"),
    "ring":         ("der Ring",          "der"),
    "hat":          ("der Hut",           "der"),
    "cap":          ("die Mütze",         "die"),
    "helmet":       ("der Helm",          "der"),
    "shoe":         ("der Schuh",         "der"),
    "sneaker":      ("der Sneaker",       "der"),
    "boot":         ("der Stiefel",       "der"),
    "sandal":       ("die Sandale",       "die"),
    "jacket":       ("die Jacke",         "die"),
    "coat":         ("der Mantel",        "der"),
    "shirt":        ("das Hemd",          "das"),
    "hoodie":       ("der Hoodie",        "der"),
    "scarf":        ("der Schal",         "der"),
    "umbrella":     ("der Regenschirm",   "der"),
    # Stationery & books
    "book":         ("das Buch",          "das"),
    "notebook":     ("das Notizbuch",     "das"),
    "magazine":     ("die Zeitschrift",   "die"),
    "newspaper":    ("die Zeitung",       "die"),
    "pen":          ("der Stift",         "der"),
    "pencil":       ("der Bleistift",     "der"),
    "marker":       ("der Marker",        "der"),
    "highlighter":  ("der Textmarker",    "der"),
    "scissors":     ("die Schere",        "die"),
    "tape":         ("das Klebeband",     "das"),
    "ruler":        ("das Lineal",        "das"),
    "eraser":       ("der Radiergummi",   "der"),
    "folder":       ("der Ordner",        "der"),
    "binder":       ("der Ringordner",    "der"),
    # Tools
    "hammer":       ("der Hammer",        "der"),
    "screwdriver":  ("der Schraubenzieher","der"),
    "wrench":       ("der Schraubenschlüssel","der"),
    "drill":        ("die Bohrmaschine",  "die"),
    "flashlight":   ("die Taschenlampe",  "die"),
    "battery":      ("die Batterie",      "die"),
    # Health & hygiene
    "toothbrush":   ("die Zahnbürste",    "die"),
    "toothpaste":   ("die Zahnpasta",     "die"),
    "soap":         ("die Seife",         "die"),
    "shampoo":      ("das Shampoo",       "das"),
    "medicine bottle":("die Medizinflasche","die"),
    "thermometer":  ("das Thermometer",   "das"),
    "tissue box":   ("die Taschentücher", "die"),
    "toilet paper": ("das Toilettenpapier","das"),
    "towel":        ("das Handtuch",      "das"),
    # Outdoor & vehicles
    "car":          ("das Auto",          "das"),
    "bicycle":      ("das Fahrrad",       "das"),
    "motorcycle":   ("das Motorrad",      "das"),
    "bus":          ("der Bus",           "der"),
    "truck":        ("der Lastwagen",     "der"),
    "traffic light":("die Ampel",         "die"),
    "stop sign":    ("das Stoppschild",   "das"),
    "tree":         ("der Baum",          "der"),
    "flower":       ("die Blume",         "die"),
    "rock":         ("der Stein",         "der"),
    "bird":         ("der Vogel",         "der"),
    "cat":          ("die Katze",         "die"),
    "dog":          ("der Hund",          "der"),
    "rabbit":       ("das Kaninchen",     "das"),
    # Sports
    "ball":         ("der Ball",          "der"),
    "football":     ("der Fußball",       "der"),
    "basketball":   ("der Basketball",    "der"),
    "tennis ball":  ("der Tennisball",    "der"),
    "dumbbell":     ("die Hantel",        "die"),
    "yoga mat":     ("die Yogamatte",     "die"),
    # Misc
    "key":          ("der Schlüssel",     "der"),
    "coin":         ("die Münze",         "die"),
    "banknote":     ("der Geldschein",    "der"),
    "credit card":  ("die Kreditkarte",   "die"),
    "lighter":      ("das Feuerzeug",     "das"),
    "candle":       ("die Kerze",         "die"),
    "toy":          ("das Spielzeug",     "das"),
    "stuffed animal":("das Kuscheltier",  "das"),
    "guitar":       ("die Gitarre",       "die"),
    "headset":      ("das Headset",       "das"),
}

# Article → BGR colour for OpenCV overlays
ARTICLE_BGR = {
    "der": (217, 141, 91),   # blue
    "die": (180,  80, 200),  # pink/purple
    "das": (91,  158, 106),  # green
    "":    (160, 160, 160),  # grey fallback
}

VOCABULARY = list(GERMAN.keys())

log.info(f"Loading YOLO-World: {MODEL_PATH}")
model = YOLOWorld(MODEL_PATH)
model.set_classes(VOCABULARY)
log.info(f"Model ready — {len(VOCABULARY)} categories")

connected_clients = set()

# ── WebSocket handler ─────────────────────────────────────────────────────────
async def handle_client(websocket):
    addr = websocket.remote_address
    log.info(f"Client connected: {addr}")
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            if isinstance(message, (bytes, bytearray)):
                img_bytes = message
            else:
                payload   = json.loads(message)
                img_bytes = base64.b64decode(payload.get("image",""))

            nparr = np.frombuffer(img_bytes, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if frame is None:
                continue

            t0      = time.time()
            results = model(frame, conf=CONFIDENCE, max_det=MAX_DETS, verbose=False)[0]
            ms      = round((time.time()-t0)*1000)

            detections = []
            if results.boxes is not None:
                boxes  = results.boxes.xyxy.cpu().numpy()
                confs  = results.boxes.conf.cpu().numpy()
                clsids = results.boxes.cls.cpu().numpy().astype(int)

                for box, conf, cls_id in zip(boxes, confs, clsids):
                    x1, y1, x2, y2 = map(int, box)
                    label_en = VOCABULARY[cls_id] if cls_id < len(VOCABULARY) else "object"
                    de_info  = GERMAN.get(label_en, (label_en, ""))
                    label_de, article = de_info
                    colour   = ARTICLE_BGR.get(article, ARTICLE_BGR[""])

                    detections.append({
                        "label_en": label_en,
                        "label_de": label_de,
                        "article":  article,
                        "conf":     round(float(conf), 2),
                        "x1": x1, "y1": y1, "x2": x2, "y2": y2,
                        "colour":   list(colour),
                    })

            await websocket.send(json.dumps({
                "detections": detections,
                "count":      len(detections),
                "ms":         ms,
            }))

    except websockets.exceptions.ConnectionClosedOK:
        log.info(f"Disconnected: {addr}")
    except Exception as e:
        log.error(f"Error {addr}: {e}", exc_info=True)
    finally:
        connected_clients.discard(websocket)


# ── HTTP: serve UI + /save_word endpoint ─────────────────────────────────────
class UIHandler(BaseHTTPRequestHandler):
    use_ssl = False  # set by run_http()

    def log_message(self, *args):
        pass  # suppress HTTP logs

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type","text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(get_html(UIHandler.use_ssl).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/save_word":
            length  = int(self.headers.get("Content-Length", 0))
            body    = json.loads(self.rfile.read(length))
            label_en = body.get("label_en","")
            label_de = body.get("label_de","")
            article  = body.get("article","")

            saved = _save_to_db(label_en, label_de, article)
            self.send_response(200)
            self.send_header("Content-Type","application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True, "saved": saved}).encode())
        else:
            self.send_response(404)
            self.end_headers()


def _save_to_db(label_en, label_de, article):
    """Save a word to the German agent's SRS deck."""
    try:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        existing = conn.execute(
            "SELECT id FROM words WHERE german=?", (label_de,)
        ).fetchone()
        if existing:
            conn.close()
            return False  # already in deck

        example_de = f"{article} {label_de.split()[-1]} ist hier.".strip() if article else f"Das ist {label_de}."
        conn.execute(
            "INSERT INTO words (german,english,article,example_de,example_en,topic,added_date) VALUES (?,?,?,?,?,?,?)",
            (label_de, label_en, article, example_de, f"The {label_en} is here.", "camera_live", str(date.today()))
        )
        # Schedule first SRS review
        word_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        conn.execute(
            "INSERT INTO reviews (word_id,rating,interval_days,ease_factor,next_review) VALUES (?,?,?,?,?)",
            (word_id, 0, 1, 2.5, str(date.today()))
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        log.error(f"DB save error: {e}")
        return False


# ── HTML UI ───────────────────────────────────────────────────────────────────
def get_html(use_ssl=False):
    ip = get_local_ip()
    ws_scheme = "wss" if use_ssl else "ws"
    return f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>German Vision — Live</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: #0f0f13; color: #e0ddd4; font-family: system-ui, sans-serif; }}

  header {{ background: #16161d; border-bottom: 1px solid #2a2a3a;
            padding: 12px 20px; display: flex; align-items: center; gap: 12px; }}
  header h1 {{ font-size: 1.1rem; font-weight: 500; }}
  .status {{ font-size: 0.75rem; color: #888; margin-left: auto; }}
  .dot {{ width:8px; height:8px; border-radius:50%; display:inline-block;
          margin-right:4px; background:#e24b4b; }}
  .dot.on {{ background:#5b9e6a; }}

  .layout {{ display: flex; height: calc(100vh - 50px); }}

  .cam-wrap {{ flex: 1; position: relative; background: #000; overflow: hidden; }}
  canvas#overlay {{ position:absolute; top:0; left:0; width:100%; height:100%;
                    pointer-events:none; }}
  video {{ width:100%; height:100%; object-fit:cover; display:block; }}

  .panel {{ width: 320px; background: #13131b; border-left: 1px solid #2a2a3a;
            overflow-y: auto; display: flex; flex-direction: column; }}

  .stats {{ padding: 12px 16px; border-bottom: 1px solid #2a2a3a;
            display: flex; gap: 16px; font-size: 0.8rem; color: #888; }}
  .stat-val {{ font-size: 1.1rem; font-weight: 500; color: #e0ddd4; display:block; }}

  .legend {{ padding: 10px 16px; border-bottom: 1px solid #2a2a3a;
             display: flex; gap: 12px; font-size: 0.75rem; }}
  .leg {{ display:flex; align-items:center; gap:5px; }}
  .leg-dot {{ width:10px;height:10px;border-radius:50%; }}

  .det-list {{ flex:1; padding: 8px; }}
  .det-item {{ background:#1a1a24; border-radius:10px; padding:10px 12px;
               margin-bottom:6px; display:flex; align-items:center;
               justify-content:space-between; border-left:3px solid; }}
  .det-de {{ font-weight:500; font-size:0.95rem; }}
  .det-en {{ font-size:0.75rem; color:#888; margin-top:2px; }}
  .det-conf {{ font-size:0.7rem; color:#666; }}
  .btn-add {{ background:none; border:1px solid #3a3a5a; color:#9999cc;
              border-radius:6px; padding:4px 10px; cursor:pointer;
              font-size:0.75rem; white-space:nowrap; transition:all 0.15s; }}
  .btn-add:hover {{ background:#22223a; color:#c0c0ee; }}
  .btn-add.saved {{ background:#1a3020; border-color:#5b9e6a; color:#5b9e6a; }}
  .btn-add:disabled {{ opacity:0.5; cursor:default; }}

  .empty {{ color:#555; font-size:0.85rem; text-align:center;
            padding:40px 20px; line-height:1.8; }}

  @media (max-width: 600px) {{
    .layout {{ flex-direction: column; height: auto; }}
    .panel {{ width: 100%; border-left: none; border-top: 1px solid #2a2a3a;
              max-height: 50vh; }}
    .cam-wrap {{ height: 50vh; }}
  }}
</style>
</head>
<body>

<header>
  <span style="font-size:1.3rem">📷</span>
  <h1>German Vision — Live Detection</h1>
  <div class="status">
    <span class="dot" id="dot"></span>
    <span id="status-text">Connecting...</span>
  </div>
</header>

<div class="layout">
  <div class="cam-wrap">
    <video id="video" autoplay muted playsinline></video>
    <canvas id="overlay"></canvas>
  </div>

  <div class="panel">
    <div class="stats">
      <div><span class="stat-val" id="obj-count">0</span>objects</div>
      <div><span class="stat-val" id="fps-val">—</span>fps</div>
      <div><span class="stat-val" id="ms-val">—</span>ms</div>
    </div>
    <div class="legend">
      <div class="leg"><div class="leg-dot" style="background:#5b8dd9"></div>der</div>
      <div class="leg"><div class="leg-dot" style="background:#b450c8"></div>die</div>
      <div class="leg"><div class="leg-dot" style="background:#5b9e6a"></div>das</div>
    </div>
    <div class="det-list" id="det-list">
      <div class="empty">Point your camera at objects.<br>German labels appear here.<br><br>Tap <strong>+ Deck</strong> to save a word<br>to your SRS flashcard deck.</div>
    </div>
  </div>
</div>

<script>
const WS_URL  = "{ws_scheme}://{ip}:{WS_PORT}";
const SAVE_URL = "/save_word";
const SKIP_EVERY = 2;  // process every Nth frame (1 = all frames)

let ws, video, overlay, ctx;
let frameCount = 0, lastDetections = [];
let fpsFrames = 0, fpsLast = performance.now();

// Article → hex colour
const ART_COLOR = {{ der:"#5b8dd9", die:"#b450c8", das:"#5b9e6a", "":"#999" }};

async function startCamera() {{
  video   = document.getElementById("video");
  overlay = document.getElementById("overlay");
  ctx     = overlay.getContext("2d");

  try {{
    const stream = await navigator.mediaDevices.getUserMedia({{
      video: {{ facingMode: "environment", width:{{ideal:1280}}, height:{{ideal:720}} }},
      audio: false
    }});
    video.srcObject = stream;
    video.onloadedmetadata = () => {{
      overlay.width  = video.videoWidth;
      overlay.height = video.videoHeight;
      requestAnimationFrame(processLoop);
    }};
  }} catch(e) {{
    document.getElementById("status-text").textContent = "Camera denied: " + e.message;
  }}
}}

function connectWS() {{
  ws = new WebSocket(WS_URL);
  ws.binaryType = "arraybuffer";

  ws.onopen = () => {{
    document.getElementById("dot").classList.add("on");
    document.getElementById("status-text").textContent = "Connected";
  }};
  ws.onclose = () => {{
    document.getElementById("dot").classList.remove("on");
    document.getElementById("status-text").textContent = "Reconnecting...";
    setTimeout(connectWS, 2000);
  }};
  ws.onerror = () => {{
    document.getElementById("status-text").textContent = "Connection error";
  }};
  ws.onmessage = (evt) => {{
    const data = JSON.parse(evt.data);
    lastDetections = data.detections || [];
    document.getElementById("obj-count").textContent = data.count;
    document.getElementById("ms-val").textContent = data.ms;
    drawOverlay(lastDetections);
    updatePanel(lastDetections);
  }};
}}

function processLoop() {{
  requestAnimationFrame(processLoop);

  // FPS counter
  fpsFrames++;
  const now = performance.now();
  if (now - fpsLast > 1000) {{
    document.getElementById("fps-val").textContent = fpsFrames;
    fpsFrames = 0; fpsLast = now;
  }}

  frameCount++;
  if (frameCount % SKIP_EVERY !== 0) return;
  if (!ws || ws.readyState !== WebSocket.OPEN) return;
  if (video.videoWidth === 0) return;

  // Draw frame to hidden canvas, encode as JPEG, send
  const tmp = document.createElement("canvas");
  tmp.width  = video.videoWidth;
  tmp.height = video.videoHeight;
  tmp.getContext("2d").drawImage(video, 0, 0);
  tmp.toBlob(blob => {{
    blob.arrayBuffer().then(buf => ws.send(buf));
  }}, "image/jpeg", 0.7);
}}

function drawOverlay(detections) {{
  ctx.clearRect(0, 0, overlay.width, overlay.height);
  detections.forEach(det => {{
    const col = ART_COLOR[det.article] || "#999";
    const x1=det.x1, y1=det.y1, x2=det.x2, y2=det.y2;
    const w=x2-x1, h=y2-y1;

    // Box
    ctx.strokeStyle = col;
    ctx.lineWidth   = 2.5;
    ctx.strokeRect(x1, y1, w, h);

    // Article dot (top-right corner)
    ctx.fillStyle = col;
    ctx.beginPath();
    ctx.arc(x2-8, y1+8, 6, 0, Math.PI*2);
    ctx.fill();

    // Label background
    const label = det.label_de + " (" + Math.round(det.conf*100) + "%)";
    ctx.font = "bold 13px system-ui";
    const tw = ctx.measureText(label).width;
    ctx.fillStyle = col + "dd";
    ctx.fillRect(x1, y1 - 24, tw + 12, 22);

    // Label text
    ctx.fillStyle = "#fff";
    ctx.fillText(label, x1 + 6, y1 - 7);
  }});
}}

function updatePanel(detections) {{
  const list = document.getElementById("det-list");
  if (!detections.length) {{
    list.innerHTML = '<div class="empty">No objects detected.<br>Try pointing at everyday objects.</div>';
    return;
  }}
  list.innerHTML = detections.map((det, i) => {{
    const col = ART_COLOR[det.article] || "#999";
    const art = det.article ? det.article + " " : "";
    return `<div class="det-item" style="border-left-color:${{col}}">
      <div>
        <div class="det-de">${{art}}${{det.label_de}}</div>
        <div class="det-en">${{det.label_en}}</div>
      </div>
      <div style="display:flex;flex-direction:column;align-items:flex-end;gap:4px">
        <div class="det-conf">${{Math.round(det.conf*100)}}%</div>
        <button class="btn-add" id="btn-${{i}}"
          onclick="saveWord(${{i}}, '${{det.label_en}}', '${{det.label_de}}', '${{det.article}}')">
          + Deck
        </button>
      </div>
    </div>`;
  }}).join("");
}}

async function saveWord(idx, label_en, label_de, article) {{
  const btn = document.getElementById("btn-" + idx);
  if (!btn) return;
  btn.disabled = true;
  btn.textContent = "Saving...";
  try {{
    const resp = await fetch(SAVE_URL, {{
      method: "POST",
      headers: {{"Content-Type":"application/json"}},
      body: JSON.stringify({{label_en, label_de, article}})
    }});
    const data = await resp.json();
    btn.textContent = data.saved ? "✓ Saved" : "Already in deck";
    btn.classList.add("saved");
  }} catch(e) {{
    btn.textContent = "Error";
    btn.disabled = false;
  }}
}}

// Init
connectWS();
startCamera();
</script>
</body>
</html>"""


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "localhost"


def run_http(ssl_ctx=None):
    UIHandler.use_ssl = ssl_ctx is not None
    server = HTTPServer(("0.0.0.0", HTTP_PORT), UIHandler)
    if ssl_ctx:
        server.socket = ssl_ctx.wrap_socket(server.socket, server_side=True)
    server.serve_forever()


async def main():
    import ssl as ssl_module

    ip = get_local_ip()

    # Auto-detect cert files in project folder
    base = os.path.dirname(os.path.abspath(__file__))
    cert_file = os.path.join(base, "cert.pem")
    key_file  = os.path.join(base, "key.pem")
    use_ssl   = os.path.exists(cert_file) and os.path.exists(key_file)

    if use_ssl:
        ssl_ctx = ssl_module.SSLContext(ssl_module.PROTOCOL_TLS_SERVER)
        ssl_ctx.load_cert_chain(cert_file, key_file)
        scheme    = "https"
        ws_scheme = "wss"
    else:
        ssl_ctx   = None
        scheme    = "http"
        ws_scheme = "ws"

    log.info("=" * 55)
    log.info("  German Vision Server — YOLO-World Edition")
    log.info("=" * 55)
    log.info(f"  Open in browser : {scheme}://{ip}:{HTTP_PORT}")
    log.info(f"  WebSocket       : {ws_scheme}://{ip}:{WS_PORT}")
    log.info(f"  SSL             : {'YES — camera will work on mobile' if use_ssl else 'NO  — run gen_cert.bat to enable mobile camera'}")
    log.info(f"  Words save to   : {DB_PATH}")
    log.info("=" * 55)

    if not use_ssl:
        log.warning("  No cert.pem found. Camera may be blocked on Android Chrome.")
        log.warning("  Run gen_cert.bat to generate a self-signed certificate.")

    # HTTP server in background thread
    t = threading.Thread(target=run_http, args=(ssl_ctx,), daemon=True)
    t.start()

    # WebSocket server (also with SSL if available)
    ws_kwargs = dict(
        max_size=10_000_000,
        ping_interval=20,
        ping_timeout=30,
    )
    if use_ssl:
        ws_kwargs["ssl"] = ssl_ctx

    async with websockets.serve(handle_client, "0.0.0.0", WS_PORT, **ws_kwargs):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())

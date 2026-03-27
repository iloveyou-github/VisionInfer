import queue
import threading

# Global Control Flag
EXIT_FLAG = False
input_thread = None
input_queue = queue.Queue()
preview_stop_event = threading.Event()
preview_thread_handle = None
ollama_process = None

# Global Parameters
DEFAULT_PROMPT = "Briefly describe the frame content (within 50 words)"

# Frame Deduplication Related
LAST_FRAME_FEATURE = None
DEDUP_THRESHOLD = 1.0

# Resolution Cache
RESOLUTION_CACHE = {}
FRAME_QUEUE = queue.Queue(maxsize=1)
FRAME_INFO_QUEUE = queue.Queue(maxsize=1)
FRAME_THREAD = None
FRAME_THREAD_RUNNING = False
FRAME_INTERVAL = 1.0

# Motion Detection
MOTION_PREV_FRAME = None
MOTION_THRESHOLD = 500

# VOD-related (Video on Demand Related)
vod_current_offset = 0
vod_step = 30
vod_start_offset = 0
FFMPEG_PIDS = []

# Yolo relate
YOLO_MODEL = ''
YOLO_TASK  = ''
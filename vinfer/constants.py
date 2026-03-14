import queue
import threading

# 全局控制标识
EXIT_FLAG = False
input_thread = None
input_queue = queue.Queue()
preview_stop_event = threading.Event()
preview_thread_handle = None
ollama_process = None

# 帧去重相关
LAST_FRAME_FEATURE = None
DEDUP_THRESHOLD = 1.0

# 分辨率缓存
RESOLUTION_CACHE = {}
FRAME_QUEUE = queue.Queue(maxsize=1)
FRAME_INFO_QUEUE = queue.Queue(maxsize=1)
FRAME_THREAD = None
FRAME_THREAD_RUNNING = False
FRAME_INTERVAL = 1.0

# 运动检测
MOTION_PREV_FRAME = None
MOTION_THRESHOLD = 500

# VOD相关
vod_current_offset = 0
vod_step = 30
vod_start_offset = 0
FFMPEG_PIDS = []
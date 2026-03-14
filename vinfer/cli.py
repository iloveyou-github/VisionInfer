import argparse

def add_common_arguments(parser):
    """Add common arguments for all subcommands"""
    # Model parameter (default qwen3.5-2b)
    parser.add_argument(
        "--model", "-m",
        type=str,
        default="qwen3.5:2b",
        help="Ollama model name"
    )
    # Compression resolution (default 480x360)
    parser.add_argument(
        "--compress-size", "-s",
        type=str,
        default="480x360",
        help="Frame compression resolution (format: widthxheight)"
    )
    # JPG quality
    parser.add_argument(
        "--jpg-quality", "-q",
        type=int,
        default=70,
        help="JPG compression quality (0-100)"
    )
    # Motion gating
    parser.add_argument(
        "--motion-gate", "-g",
        action="store_true",
        help="Enable motion gating (infer only when motion detected)"
    )
    # Motion threshold
    parser.add_argument(
        "--motion-threshold", "-T",
        type=int,
        default=500,
        help="Minimum pixel threshold for motion detection"
    )
    # Deduplication
    parser.add_argument(
        "--dedup", "-D",
        action="store_true",
        help="Enable L2 similar frame deduplication (disabled if motion-gate is on)"
    )
    # Inference interval
    parser.add_argument(
        "--interval", "-i",
        type=float,
        default=1.0,
        help="Inference interval (seconds/frame)"
    )
    # Debug mode
    parser.add_argument(
        "--debug", "-d",
        action="store_true",
        help="Enable debug logging (verbose output)"
    )

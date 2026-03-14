import time
import ollama
from .constants import EXIT_FLAG

def infer_frame(args, raw_image_data, timeout: int = 30):
    import ollama
    client = ollama.Client()
    if args.debug:
        print(f"🔍 Calling Ollama inference (image size: {len(raw_image_data)/1024:.1f}KB)")
    start_infer = time.time()
    
    try:
        prompt = "Briefly describe the frame content (within 50 words)"
        stream = client.chat(
            model=args.model,
            messages=[{"role": "user", "content": prompt, "images": [raw_image_data]}],
            stream=True,
            think=False,
            keep_alive="24h",
            options={
                "max_tokens": 200,
                "temperature": 0.0,
                "num_ctx": 512
            }
        )
        
        result = ""
        for chunk in stream:
            if 'message' in chunk and 'content' in chunk['message']:
                result += chunk['message']['content']
        
        infer_cost = time.time() - start_infer
        return result.strip(), infer_cost
    
    except Exception as e:
        return f"Inference failed: {str(e)}", time.time() - start_infer
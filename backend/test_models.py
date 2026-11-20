import httpx
import time

models = [
    'gemma3:4b',
    'qwen3.5:2b',
    'qwen2.5-coder:3b',
    'qwen3.5:4b',
    'llama3.1:latest'
]

print("=== TESTING ALL LOCAL OLLAMA MODELS ===")
for m in models:
    t0 = time.time()
    try:
        r = httpx.post(
            'http://127.0.0.1:11434/api/generate',
            json={'model': m, 'prompt': 'State your name, model, and what software tasks you can do.', 'stream': False},
            timeout=120.0
        )
        dt = time.time() - t0
        txt = r.json().get('response', '').strip().replace('\n', ' ')
        print(f"[{m}] SUCCESS in {dt:.2f}s:")
        print(f"   -> {txt[:120]}...\n")
    except Exception as e:
        print(f"[{m}] FAILED: {e}\n")

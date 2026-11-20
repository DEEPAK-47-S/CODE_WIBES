# CODE WIBES TECHNOLOGIES — Model Registry & Capability Architecture

**Hardware Baseline:** Windows 11 Home, AMD Ryzen 7 7445HS, NVIDIA RTX 4050 Laptop GPU (6GB VRAM), 16GB RAM.  
**Inference Engine:** Local Ollama (`http://127.0.0.1:11434`)  
**Scheduler Constraint:** Strict single-inference concurrency (`max_concurrent_models = 1`).  

---

## 1. Registered Models & Capability Matrix

| Model Identifier | Parameter Size | Quantization | Context Budget | Primary Task Category | Fallback Position |
|---|---|---|---|---|---|
| `qwen3.5:4b` | 4.2B | Q4_K_M | 8192 | Central Orchestration (NEXUS), Strategy | Primary General |
| `qwen2.5-coder:3b` | 3.1B | Q4_K_M | 8192 | Full-Stack Coding, Database, QA | Primary Engineering |
| `gemma3:4b` | 3.9B | Q4_K_M | 8192 | UI/UX Design Systems, Multimodal Vision | Primary Creative |
| `granite4.2:3b` | 3.7B | Q4_K_M | 8192 | Operations, Business Logic, Compliance | Primary Governance |
| `phi4-mini:latest` | 3.8B | Q4_K_M | 8192 | Reasoning, Planning, DevOps | Secondary Engineering |
| `qwen3.5:2b` | 1.9B | Q8_0 | 8192 | Lightweight Classification, Docs, Triage | Fast Lightweight |
| `llama3.1:latest` | 8.0B | Q4_K_M | 8192 | Sales Outreach, Lead Generation, Voice | Heavy Fallback |
| `lfm3:latest` | 1.7B | Q4_K_M | 4096 | Fast Triage, Rapid Formatting | Ultra-Lightweight |

---

## 2. Dynamic Discovery & Benchmarking

The system automatically probes Ollama endpoints:
- `GET /api/tags`: Discovers newly installed models, sizes, and digests.
- `POST /api/show`: Inspects model architecture, template, and parameters.
- `POST /api/v1/models/{name}/benchmark`: Executes a standardized 5-word test to calculate real-world latency (ms) and throughput (tokens/sec) on the RTX 4050 GPU.

---

## 3. Safe Context Sizing

While models advertise 131,072 to 262,144 tokens, running large contexts directly exhausts the 6GB VRAM on laptop GPUs.
- **Enforced Default Runtime Context:** `8,192 tokens`.
- Context continuation is achieved through persistent PostgreSQL checkpoints, **not** through dangerous 128K context allocations that cause CUDA OOM errors.

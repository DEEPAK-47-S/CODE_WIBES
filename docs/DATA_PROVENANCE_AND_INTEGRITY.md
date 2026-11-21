# CODE WIBES TECHNOLOGIES — Data Provenance & Integrity Policy

## 1. Zero Fake Data Mandate
Under company operational standards set by Founder **DEEPAKUMAR.S**, **zero mock, fabricated, or synthetic client/financial data is permitted in production systems**:
- **No Fake Customers / Leads**: Simulated listings or offline hallucinated businesses (e.g. fabricated names, dummy phone numbers like `+91 44 2800 0000`, placeholder emails) are strictly prohibited from being persisted to CRM tables (`leads`).
- **No Fake Financials**: Pipeline valuations must reflect genuine quote submissions or calculated qualified estimates, never simulated revenue.
- **No Fabricated Testimonials**: Only verified customer reviews and delivered projects are eligible for public display.
- **Empty State Integrity**: When no verified external data exists (e.g. absent Google Maps API key), the system renders clear empty states with actionable configuration instructions rather than populating dummy rows.

---

## 2. Provenance Metadata Specification
Every persisted lead, proposal, memory record, and deliverable carries explicit data provenance:

| Field | Type | Allowed Values / Description |
|---|---|---|
| `source_type` | `String` | `FOUNDER_PROVIDED`, `EXTERNAL_API`, `AI_GENERATED`, `SYSTEM_GENERATED`, `CUSTOMER_SUBMITTED` |
| `source_reference` | `String` | Official Google Place ID (`place_id`), URL, Contact Form ID, or API origin |
| `verification_status`| `String` | `VERIFIED`, `UNVERIFIED`, `SYNTHESIZED` |
| `created_by` | `String` | Originating identity (`FOUNDER_DEEPAK`, `PUBLIC_WEB_FORM`, or specific Agent code e.g. `NEXUS-00`, `HUNTER`) |

---

## 3. Google Places API (New) Discovery Compliance
1. **Official Endpoints Only**: Lead harvesting queries the Google Places API (New) via `https://places.googleapis.com/v1/places:searchText`.
2. **Canonical Deduplication**: Unique constraint index on `leads.place_id`. Discovered businesses matching an existing `place_id` are skipped automatically.
3. **Google Attribution**: Records populated from Google Places have `google_attribution_required = true` to comply with Google Maps Platform policies.
4. **Offline Fallback Guarantee**: If `GOOGLE_MAPS_API_KEY` is omitted, the harvester returns an empty array with diagnostic status `CONFIG_REQUIRED` without writing fabricated data to PostgreSQL.

---

## 4. Single-Worker GPU Execution Lock (RTX 4050 6GB)
To prevent VRAM thrashing and Out-Of-Memory (OOM) crashes on local hardware:
- All Ollama model queries are guarded by a global `asyncio.Lock` (`_GPU_INFERENCE_LOCK`).
- Models execute strictly sequentially (`max_concurrent_models = 1`).
- Context windows are capped at 8192 tokens (`num_ctx: 8192`).
- Tasks reaching the 70% threshold (~5700 tokens) automatically snapshot state to `task_checkpoints` in PostgreSQL before continuation.

---

## 5. Automated Data Sanitization Routine
A dedicated database sanitization script (`backend/scripts/sanitize_data.py`) purges any prototype dummy records and retrofits canonical provenance metadata onto verified rows.

# CODE WIBES TECHNOLOGIES — Lead Discovery & Google Places Policy Compliance

**Core Principle:** Compliant, official discovery. No browser-based scraping of Google Maps. Place IDs are stored long-term as exempt identifiers; live Place Details are retrieved when views require them.

---

## 1. Compliance Architecture

1. **Official Google Places API (New)**:
   - Uses `https://places.googleapis.com/v1/places:searchText` with official server-side API keys.
   - Enforces FieldMasking (`displayName`, `formattedAddress`, `nationalPhoneNumber`, `websiteUri`, `rating`, `userRatingCount`).
2. **Place ID Deduplication**:
   - The `leads.place_id` column has a unique database index in PostgreSQL.
   - Re-running discoveries never creates duplicate lead records; existing entries are refreshed without duplicating CRM rows.
3. **Mandatory Google Attribution**:
   - When Google Places data is displayed, the required Google logo/attribution is rendered.
4. **Offline AI Crawler Simulation**:
   - When offline or when the API key is unconfigured, the system explicitly marks records as `source: "AI Simulated Discovery"`. Fake Google Place IDs are never fabricated.

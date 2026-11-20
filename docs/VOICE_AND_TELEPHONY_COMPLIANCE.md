# CODE WIBES TECHNOLOGIES — Voice Telephony & India TRAI Compliance

**Core Principle:** Public discovery does not equal consent. Finding a phone number on Google Maps does not grant legal authorization for automated AI marketing calls under Indian law.

---

## 1. Regulatory Requirements (TRAI / TCCCPR)

In India, commercial communications (calls/SMS) require:
1. **Principal Entity & Header Registration** on telecom DLT portals (Jio, Airtel, Vodafone Idea, BSNL).
2. **Approved Voice Script Templates**: Telephony providers require pre-registered voice templates.
3. **Customer Preference & DND Scrubbing**: Must scrub against national Do-Not-Disturb registries prior to campaign execution.
4. **Time Window Restrictions**: Commercial communications are legally restricted to 09:00 AM – 09:00 PM local time.

---

## 2. Technical Safeguards in CODE WIBES

1. **Disabled by Default**:
   - `allow_production_calling` is hard-locked to `False` in PostgreSQL `company_settings`.
   - Production dialers will abort with `BLOCKED_COMPLIANCE` if triggered.
2. **Strict Test Mode**:
   - Calls in development mode are permitted strictly to the Founder's verified phone (`founder_verified_phone`) or simulated test endpoints.
3. **Immediate Opt-Out Suppression**:
   - If a prospect says "Stop calling" or requests opt-out, the `VoiceService.record_opt_out()` method updates the lead status to `do_not_contact` and `consent_status` to `opt_out`.
   - All subsequent dial attempts to that number are blocked instantly.
4. **Founder Alert Voice Channel**:
   - A dedicated critical alert channel configured to notify Founder Deepak for high-severity production outages or security triggers.

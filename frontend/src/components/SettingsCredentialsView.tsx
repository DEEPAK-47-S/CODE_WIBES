import React, { useState, useEffect } from 'react';
import { Key, Save, CheckCircle2, Eye, EyeOff } from 'lucide-react';
import { fetchCompanySettings, updateCompanySettings } from '../api';

export function SettingsCredentialsView() {
  const [showSecrets, setShowSecrets] = useState<{ [key: string]: boolean }>({});
  const [saving, setSaving] = useState(false);
  const [savedSuccess, setSavedSuccess] = useState(false);

  // Form Fields
  const [googleMapsKey, setGoogleMapsKey] = useState('');
  const [elevenLabsKey, setElevenLabsKey] = useState('');
  const [elevenLabsVoiceId, setElevenLabsVoiceId] = useState('');
  const [twilioSid, setTwilioSid] = useState('');
  const [twilioToken, setTwilioToken] = useState('');
  const [twilioPhone, setTwilioPhone] = useState('');
  const [whatsappToken, setWhatsappToken] = useState('');
  const [whatsappPhoneId, setWhatsappPhoneId] = useState('');
  const [razorpayKeyId, setRazorpayKeyId] = useState('');
  const [razorpaySecret, setRazorpaySecret] = useState('');
  const [cloudLlmKey, setCloudLlmKey] = useState('');

  const loadSettings = async () => {
    try {
      const data = await fetchCompanySettings();
      setGoogleMapsKey((data as any).google_maps_api_key || '');
      setElevenLabsKey((data as any).elevenlabs_api_key || '');
      setElevenLabsVoiceId((data as any).elevenlabs_voice_id || '');
      setTwilioSid((data as any).twilio_account_sid || '');
      setTwilioToken((data as any).twilio_auth_token || '');
      setTwilioPhone((data as any).twilio_phone_number || '');
      setWhatsappToken((data as any).whatsapp_api_token || '');
      setWhatsappPhoneId((data as any).whatsapp_phone_number_id || '');
      setRazorpayKeyId((data as any).razorpay_key_id || '');
      setRazorpaySecret((data as any).razorpay_key_secret || '');
      setCloudLlmKey((data as any).cloud_llm_api_key || '');
    } catch {
      console.error('Failed to load settings');
    }
  };

  useEffect(() => {
    loadSettings();
  }, []);

  const toggleShow = (field: string) => {
    setShowSecrets((prev) => ({ ...prev, [field]: !prev[field] }));
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setSavedSuccess(false);
    try {
      await updateCompanySettings({
        google_maps_api_key: googleMapsKey,
        elevenlabs_api_key: elevenLabsKey,
        elevenlabs_voice_id: elevenLabsVoiceId,
        twilio_account_sid: twilioSid,
        twilio_auth_token: twilioToken,
        twilio_phone_number: twilioPhone,
        whatsapp_api_token: whatsappToken,
        whatsapp_phone_number_id: whatsappPhoneId,
        razorpay_key_id: razorpayKeyId,
        razorpay_key_secret: razorpaySecret,
        cloud_llm_api_key: cloudLlmKey,
      } as any);
      setSavedSuccess(true);
      setTimeout(() => setSavedSuccess(false), 4000);
      loadSettings();
    } catch {
      alert('Failed to update credentials. Please check backend.');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div style={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: '14px', padding: '24px', display: 'flex', flexDirection: 'column', gap: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h3 style={{ fontSize: '18px', fontWeight: 700, color: '#f8fafc', margin: 0, display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Key size={18} color="#38bdf8" /> API Credentials & Third-Party Integrations
          </h3>
          <p style={{ color: '#94a3b8', fontSize: '13px', margin: '4px 0 0 0' }}>
            Enter API keys from frontend. Stored securely in PostgreSQL database (`company_settings`).
          </p>
        </div>
        {savedSuccess && (
          <span style={{ background: '#065f46', color: '#34d399', fontSize: '12px', fontWeight: 700, padding: '6px 14px', borderRadius: '20px', display: 'flex', alignItems: 'center', gap: '6px' }}>
            <CheckCircle2 size={14} /> Saved in Database!
          </span>
        )}
      </div>

      <form onSubmit={handleSave} style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
        {/* Section 1: Lead Prospecting & Maps */}
        <div>
          <h4 style={{ fontSize: '13px', fontWeight: 700, color: '#38bdf8', textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: '10px' }}>
            1. Google Places & Lead Prospecting
          </h4>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '10px' }}>
            <div>
              <label style={{ display: 'block', fontSize: '12px', color: '#94a3b8', marginBottom: '4px' }}>Google Maps Places API Key</label>
              <div style={{ display: 'flex', gap: '8px' }}>
                <input
                  type={showSecrets['gmaps'] ? 'text' : 'password'}
                  value={googleMapsKey}
                  onChange={(e) => setGoogleMapsKey(e.target.value)}
                  placeholder="AIzaSy..."
                  style={{ flex: 1, background: '#1e293b', border: '1px solid #334155', borderRadius: '8px', padding: '10px 14px', color: 'white', fontSize: '13px', outline: 'none' }}
                />
                <button type="button" onClick={() => toggleShow('gmaps')} style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '8px', padding: '0 12px', color: '#94a3b8', cursor: 'pointer' }}>
                  {showSecrets['gmaps'] ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Section 2: Voice & Telephony */}
        <div style={{ borderTop: '1px solid #1e293b', paddingTop: '16px' }}>
          <h4 style={{ fontSize: '13px', fontWeight: 700, color: '#a78bfa', textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: '10px' }}>
            2. Voice & Telephony (ElevenLabs & Twilio)
          </h4>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px' }}>
            <div>
              <label style={{ display: 'block', fontSize: '12px', color: '#94a3b8', marginBottom: '4px' }}>ElevenLabs API Key</label>
              <input
                type="password"
                value={elevenLabsKey}
                onChange={(e) => setElevenLabsKey(e.target.value)}
                placeholder="sk_..."
                style={{ width: '100%', background: '#1e293b', border: '1px solid #334155', borderRadius: '8px', padding: '10px 14px', color: 'white', fontSize: '13px', outline: 'none' }}
              />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '12px', color: '#94a3b8', marginBottom: '4px' }}>ElevenLabs Voice ID (AriaVoice)</label>
              <input
                type="text"
                value={elevenLabsVoiceId}
                onChange={(e) => setElevenLabsVoiceId(e.target.value)}
                placeholder="21m00Tcm4TlvDq8ikWAM"
                style={{ width: '100%', background: '#1e293b', border: '1px solid #334155', borderRadius: '8px', padding: '10px 14px', color: 'white', fontSize: '13px', outline: 'none' }}
              />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '12px', color: '#94a3b8', marginBottom: '4px' }}>Twilio Account SID</label>
              <input
                type="text"
                value={twilioSid}
                onChange={(e) => setTwilioSid(e.target.value)}
                placeholder="AC..."
                style={{ width: '100%', background: '#1e293b', border: '1px solid #334155', borderRadius: '8px', padding: '10px 14px', color: 'white', fontSize: '13px', outline: 'none' }}
              />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '12px', color: '#94a3b8', marginBottom: '4px' }}>Twilio Auth Token</label>
              <input
                type="password"
                value={twilioToken}
                onChange={(e) => setTwilioToken(e.target.value)}
                placeholder="Token..."
                style={{ width: '100%', background: '#1e293b', border: '1px solid #334155', borderRadius: '8px', padding: '10px 14px', color: 'white', fontSize: '13px', outline: 'none' }}
              />
            </div>
          </div>
        </div>

        {/* Section 3: WhatsApp & Payments */}
        <div style={{ borderTop: '1px solid #1e293b', paddingTop: '16px' }}>
          <h4 style={{ fontSize: '13px', fontWeight: 700, color: '#34d399', textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: '10px' }}>
            3. WhatsApp & Payments (Razorpay)
          </h4>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px' }}>
            <div>
              <label style={{ display: 'block', fontSize: '12px', color: '#94a3b8', marginBottom: '4px' }}>WhatsApp Cloud API Token</label>
              <input
                type="password"
                value={whatsappToken}
                onChange={(e) => setWhatsappToken(e.target.value)}
                placeholder="EAA..."
                style={{ width: '100%', background: '#1e293b', border: '1px solid #334155', borderRadius: '8px', padding: '10px 14px', color: 'white', fontSize: '13px', outline: 'none' }}
              />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '12px', color: '#94a3b8', marginBottom: '4px' }}>WhatsApp Phone Number ID</label>
              <input
                type="text"
                value={whatsappPhoneId}
                onChange={(e) => setWhatsappPhoneId(e.target.value)}
                placeholder="10987654321..."
                style={{ width: '100%', background: '#1e293b', border: '1px solid #334155', borderRadius: '8px', padding: '10px 14px', color: 'white', fontSize: '13px', outline: 'none' }}
              />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '12px', color: '#94a3b8', marginBottom: '4px' }}>Razorpay Key ID</label>
              <input
                type="text"
                value={razorpayKeyId}
                onChange={(e) => setRazorpayKeyId(e.target.value)}
                placeholder="rzp_live_..."
                style={{ width: '100%', background: '#1e293b', border: '1px solid #334155', borderRadius: '8px', padding: '10px 14px', color: 'white', fontSize: '13px', outline: 'none' }}
              />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '12px', color: '#94a3b8', marginBottom: '4px' }}>Razorpay Key Secret</label>
              <input
                type="password"
                value={razorpaySecret}
                onChange={(e) => setRazorpaySecret(e.target.value)}
                placeholder="Secret..."
                style={{ width: '100%', background: '#1e293b', border: '1px solid #334155', borderRadius: '8px', padding: '10px 14px', color: 'white', fontSize: '13px', outline: 'none' }}
              />
            </div>
          </div>
        </div>

        {/* Section 4: Cloud LLM Fallback */}
        <div style={{ borderTop: '1px solid #1e293b', paddingTop: '16px' }}>
          <h4 style={{ fontSize: '13px', fontWeight: 700, color: '#f59e0b', textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: '10px' }}>
            4. Cloud Fallback AI Model Key (Gemini / Claude / DeepSeek)
          </h4>
          <div>
            <label style={{ display: 'block', fontSize: '12px', color: '#94a3b8', marginBottom: '4px' }}>Cloud AI API Key (Optional)</label>
            <input
              type="password"
              value={cloudLlmKey}
              onChange={(e) => setCloudLlmKey(e.target.value)}
              placeholder="AIzaSy... or sk-ant-..."
              style={{ width: '100%', background: '#1e293b', border: '1px solid #334155', borderRadius: '8px', padding: '10px 14px', color: 'white', fontSize: '13px', outline: 'none' }}
            />
            <span style={{ fontSize: '11px', color: '#64748b', marginTop: '4px', display: 'block' }}>
              Primary inference runs 100% locally on your RTX 4050 GPU for ₹0 cost. Cloud key is strictly a backup.
            </span>
          </div>
        </div>

        {/* Save Button */}
        <div style={{ display: 'flex', justifyContent: 'flex-end', borderTop: '1px solid #1e293b', paddingTop: '16px' }}>
          <button
            type="submit"
            disabled={saving}
            style={{ background: '#3b82f6', color: 'white', border: 'none', borderRadius: '8px', padding: '12px 24px', fontWeight: 700, fontSize: '14px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '8px', boxShadow: '0 4px 14px rgba(59,130,246,0.3)' }}
          >
            <Save size={16} />
            {saving ? 'Saving to Database...' : 'Save All Credentials to PostgreSQL'}
          </button>
        </div>
      </form>
    </div>
  );
}

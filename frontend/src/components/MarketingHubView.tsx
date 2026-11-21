import React, { useState, useEffect } from 'react';
import { Sparkles } from 'lucide-react';
import {
  fetchMarketingPosts,
  generateMarketingPost,
  publishMarketingPost,
  type MarketingPostItem,
} from '../api';

export function MarketingHubView({ onOpenApprovals: _onOpenApprovals }: { onOpenApprovals: () => void }) {
  const [platform, setPlatform] = useState<string>('linkedin');
  const [topic, setTopic] = useState<string>('Autonomous AI Software Engineering');
  const [keyInsight, setKeyInsight] = useState<string>('Strict Founder-in-the-loop governance guarantees software quality.');
  const [posts, setPosts] = useState<MarketingPostItem[]>([]);
  const [generating, setGenerating] = useState<boolean>(false);


  const loadPosts = async () => {
    try {
      const data = await fetchMarketingPosts();
      setPosts(data);
    } catch {
      console.error('Failed to load marketing posts');
    }
  };

  useEffect(() => {
    loadPosts();
  }, []);

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!topic.trim()) return;
    setGenerating(true);
    try {
      await generateMarketingPost(platform, topic, keyInsight);
      loadPosts();
      alert('Post generated and queued for Founder Approval!');
    } catch {
      alert('Failed to generate marketing post.');
    } finally {
      setGenerating(false);
    }
  };

  const handlePublish = async (postId: string) => {
    try {
      await publishMarketingPost(postId);
      loadPosts();
    } catch {
      alert('Failed to publish post.');
    }
  };

  return (
    <div style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h2 style={{ fontSize: '22px', fontWeight: 700, color: '#f8fafc', margin: 0 }}>
            Marketing, Social Media & Thought Leadership
          </h2>
          <p style={{ color: '#94a3b8', fontSize: '13px', margin: '4px 0 0 0' }}>
            Automated organic lead acquisition, tech blog drafting, and Founder-approved social campaigns.
          </p>
        </div>
        <span style={{ background: '#1e293b', border: '1px solid #334155', padding: '6px 14px', borderRadius: '20px', fontSize: '12px', color: '#f472b6' }}>
          Head of Growth: Echo (D09)
        </span>
      </div>

      {/* Campaign Generator Form */}
      <div style={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: '14px', padding: '20px' }}>
        <form onSubmit={handleGenerate} style={{ display: 'grid', gridTemplateColumns: '1fr 2fr 2fr auto', gap: '16px', alignItems: 'flex-end' }}>
          <div>
            <label style={{ display: 'block', fontSize: '12px', color: '#94a3b8', marginBottom: '6px', fontWeight: 600 }}>Platform</label>
            <select
              value={platform}
              onChange={(e) => setPlatform(e.target.value)}
              style={{ width: '100%', background: '#1e293b', border: '1px solid #334155', borderRadius: '8px', padding: '10px 14px', color: 'white', fontSize: '13px', outline: 'none' }}
            >
              <option value="linkedin">LinkedIn Post</option>
              <option value="x_twitter">X / Twitter Thread</option>
              <option value="tech_blog">Technical Blog Article</option>
            </select>
          </div>
          <div>
            <label style={{ display: 'block', fontSize: '12px', color: '#94a3b8', marginBottom: '6px', fontWeight: 600 }}>Campaign / Subject Topic</label>
            <input
              type="text"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              placeholder="e.g. Sub-Second API Architecture"
              style={{ width: '100%', background: '#1e293b', border: '1px solid #334155', borderRadius: '8px', padding: '10px 14px', color: 'white', fontSize: '13px', outline: 'none' }}
            />
          </div>
          <div>
            <label style={{ display: 'block', fontSize: '12px', color: '#94a3b8', marginBottom: '6px', fontWeight: 600 }}>Key Value Proposition / Insight</label>
            <input
              type="text"
              value={keyInsight}
              onChange={(e) => setKeyInsight(e.target.value)}
              placeholder="e.g. Zero manual QA delays"
              style={{ width: '100%', background: '#1e293b', border: '1px solid #334155', borderRadius: '8px', padding: '10px 14px', color: 'white', fontSize: '13px', outline: 'none' }}
            />
          </div>
          <button
            type="submit"
            disabled={generating}
            style={{ background: '#db2777', color: 'white', border: 'none', borderRadius: '8px', padding: '10px 20px', fontWeight: 600, fontSize: '13px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '8px' }}
          >
            <Sparkles size={15} />
            {generating ? 'Drafting...' : 'Generate & Queue'}
          </button>
        </form>
      </div>

      {/* Posts Queue List */}
      <div style={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: '14px', padding: '20px' }}>
        <h3 style={{ fontSize: '16px', fontWeight: 700, color: '#f8fafc', margin: '0 0 16px 0' }}>
          Content Library & Campaign Pipeline
        </h3>
        {posts.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '40px', color: '#64748b', fontSize: '14px' }}>
            No marketing posts drafted yet. Generate your first thought leadership campaign above.
          </div>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
            {posts.map((p) => (
              <div key={p.id} style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '10px', padding: '16px', display: 'flex', flexDirection: 'column', gap: '10px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span style={{ background: p.platform === 'linkedin' ? '#0077b5' : p.platform === 'x_twitter' ? '#1da1f2' : '#8b5cf6', color: 'white', fontSize: '11px', fontWeight: 700, padding: '3px 8px', borderRadius: '6px' }}>
                    {p.platform.toUpperCase()}
                  </span>
                  <span style={{ background: p.status === 'published' ? '#065f46' : '#78350f', color: p.status === 'published' ? '#34d399' : '#fcd34d', fontSize: '11px', fontWeight: 700, padding: '3px 8px', borderRadius: '6px' }}>
                    {p.status.toUpperCase()}
                  </span>
                </div>
                <h4 style={{ fontSize: '14px', fontWeight: 700, color: '#f8fafc', margin: 0 }}>{p.title}</h4>
                <p style={{ fontSize: '12px', color: '#cbd5e1', lineHeight: '1.5', margin: 0, whiteSpace: 'pre-wrap' }}>
                  {p.content_text.length > 220 ? `${p.content_text.slice(0, 220)}...` : p.content_text}
                </p>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px' }}>
                  {p.hashtags.map((h, idx) => (
                    <span key={idx} style={{ fontSize: '11px', color: '#60a5fa' }}>{h}</span>
                  ))}
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderTop: '1px solid #334155', paddingTop: '10px', marginTop: 'auto' }}>
                  <span style={{ fontSize: '11px', color: '#94a3b8' }}>Author: {p.created_by_agent}</span>
                  {p.status !== 'published' ? (
                    <button
                      onClick={() => handlePublish(p.id)}
                      style={{ background: '#059669', color: 'white', border: 'none', borderRadius: '6px', padding: '5px 12px', fontSize: '11px', fontWeight: 600, cursor: 'pointer' }}
                    >
                      Founder Publish Now
                    </button>
                  ) : (
                    <span style={{ fontSize: '11px', color: '#34d399', fontWeight: 600 }}>✓ Live Published</span>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

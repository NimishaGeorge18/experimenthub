import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { getExperiment, updateStatus, getAnalytics } from '../api/experiments';

const statusColors = {
  draft: { bg: '#fff8e1', color: '#f59e0b' },
  running: { bg: '#e8f5e9', color: '#22c55e' },
  paused: { bg: '#fff3e0', color: '#f97316' },
  completed: { bg: '#ede9fe', color: '#7c3aed' }
};

const VARIANT_COLORS = ['#667eea', '#f97316', '#22c55e', '#ef4444'];

export default function ExperimentDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [experiment, setExperiment] = useState(null);
  const [analytics, setAnalytics] = useState(null);
  const [eventType, setEventType] = useState('purchase');
  const [loading, setLoading] = useState(true);
  const [analyticsLoading, setAnalyticsLoading] = useState(false);

  useEffect(() => {
    getExperiment(id)
      .then(res => setExperiment(res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [id]);

  const fetchAnalytics = () => {
    setAnalyticsLoading(true);
    getAnalytics(id, eventType)
      .then(res => setAnalytics(res.data))
      .catch(console.error)
      .finally(() => setAnalyticsLoading(false));
  };

  const handleStatusChange = async (newStatus) => {
    try {
      const res = await updateStatus(id, newStatus);
      setExperiment(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) return <div style={styles.center}>Loading...</div>;
  if (!experiment) return <div style={styles.center}>Experiment not found.</div>;

  const nextActions = {
    draft: [{ label: '▶ Start Experiment', status: 'running', color: '#22c55e' }],
    running: [
      { label: '⏸ Pause', status: 'paused', color: '#f97316' },
      { label: '✓ Complete', status: 'completed', color: '#7c3aed' }
    ],
    paused: [
      { label: '▶ Resume', status: 'running', color: '#22c55e' },
      { label: '✓ Complete', status: 'completed', color: '#7c3aed' }
    ],
    completed: []
  };

  return (
    <div style={styles.page}>
      <div style={styles.navbar}>
        <h1 style={styles.brand} onClick={() => navigate('/experiments')}>ExperimentHub</h1>
      </div>

      <div style={styles.content}>
        <button onClick={() => navigate('/experiments')} style={styles.back}>← Back to Experiments</button>

        {/* Header */}
        <div style={styles.header}>
          <div>
            <h2 style={styles.title}>{experiment.name}</h2>
            {experiment.description && <p style={styles.desc}>{experiment.description}</p>}
          </div>
          <span style={{ ...styles.badge, background: statusColors[experiment.status]?.bg, color: statusColors[experiment.status]?.color }}>
            {experiment.status}
          </span>
        </div>

        {/* Status Actions */}
        {nextActions[experiment.status]?.length > 0 && (
          <div style={styles.actions}>
            {nextActions[experiment.status].map(action => (
              <button key={action.status} onClick={() => handleStatusChange(action.status)}
                style={{ ...styles.actionBtn, background: action.color }}>
                {action.label}
              </button>
            ))}
          </div>
        )}

        {/* Variants */}
        <div style={styles.card}>
          <h3 style={styles.cardTitle}>Variants</h3>
          <div style={styles.variantGrid}>
            {experiment.variants.map((v, i) => (
              <div key={v.id} style={{ ...styles.variantCard, borderLeft: `4px solid ${VARIANT_COLORS[i]}` }}>
                <p style={styles.variantName}>{v.name}</p>
                <p style={styles.variantSplit}>{(v.traffic_split * 100).toFixed(0)}% traffic</p>
                {v.description && <p style={styles.variantDesc}>{v.description}</p>}
              </div>
            ))}
          </div>
        </div>

        {/* Analytics */}
        <div style={styles.card}>
          <h3 style={styles.cardTitle}>Analytics</h3>
          <div style={styles.analyticsControls}>
            <input
              value={eventType}
              onChange={e => setEventType(e.target.value)}
              style={styles.eventInput}
              placeholder="Event type (e.g. purchase)"
            />
            <button onClick={fetchAnalytics} style={styles.analyzeBtn} disabled={analyticsLoading}>
              {analyticsLoading ? 'Loading...' : 'Analyze'}
            </button>
          </div>

          {analytics && (
            <>
              {/* Winner Banner */}
              {analytics.winner && (
                <div style={styles.winner}>
                  🏆 Winner: <strong>{analytics.winner}</strong>
                </div>
              )}
              {!analytics.winner && (
                <div style={styles.noWinner}>No conversions recorded yet for "{analytics.event_type}"</div>
              )}

              {/* Bar Chart */}
              <div style={{ marginTop: '24px' }}>
                <p style={styles.chartLabel}>Conversion Rate (%)</p>
                <ResponsiveContainer width="100%" height={280}>
                  <BarChart data={analytics.results} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                    <XAxis dataKey="variant_name" />
                    <YAxis unit="%" />
                    <Tooltip formatter={(val) => `${val}%`} />
                    <Bar dataKey="conversion_rate" radius={[6, 6, 0, 0]}>
                      {analytics.results.map((_, i) => (
                        <Cell key={i} fill={VARIANT_COLORS[i]} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>

              {/* Stats Table */}
              <table style={styles.table}>
                <thead>
                  <tr>
                    <th style={styles.th}>Variant</th>
                    <th style={styles.th}>Users</th>
                    <th style={styles.th}>Conversions</th>
                    <th style={styles.th}>Rate</th>
                  </tr>
                </thead>
                <tbody>
                  {analytics.results.map((r, i) => (
                    <tr key={r.variant_id}>
                      <td style={styles.td}>
                        <span style={{ ...styles.dot, background: VARIANT_COLORS[i] }} />
                        {r.variant_name}
                      </td>
                      <td style={styles.td}>{r.total_users}</td>
                      <td style={styles.td}>{r.conversions}</td>
                      <td style={{ ...styles.td, fontWeight: '700', color: VARIANT_COLORS[i] }}>
                        {r.conversion_rate}%
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

const styles = {
  page: { minHeight: '100vh', background: '#f0f2f5' },
  navbar: { background: '#fff', padding: '16px 32px', boxShadow: '0 2px 8px rgba(0,0,0,0.08)' },
  brand: { fontSize: '22px', fontWeight: '800', color: '#667eea', cursor: 'pointer' },
  content: { padding: '40px 32px', maxWidth: '860px', margin: '0 auto' },
  back: { background: 'none', border: 'none', color: '#667eea', fontSize: '14px', fontWeight: '600', marginBottom: '24px', padding: 0, cursor: 'pointer' },
  header: { display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '24px' },
  title: { fontSize: '28px', fontWeight: '800', color: '#1a1a1a' },
  desc: { color: '#888', marginTop: '8px', fontSize: '15px' },
  badge: { padding: '6px 14px', borderRadius: '20px', fontSize: '13px', fontWeight: '600', whiteSpace: 'nowrap' },
  actions: { display: 'flex', gap: '12px', marginBottom: '24px' },
  actionBtn: { padding: '10px 20px', color: '#fff', border: 'none', borderRadius: '8px', fontSize: '14px', fontWeight: '600', cursor: 'pointer' },
  card: { background: '#fff', borderRadius: '12px', padding: '24px', boxShadow: '0 2px 12px rgba(0,0,0,0.06)', marginBottom: '24px' },
  cardTitle: { fontSize: '16px', fontWeight: '700', marginBottom: '20px', color: '#1a1a1a' },
  variantGrid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '16px' },
  variantCard: { padding: '16px', background: '#f9f9f9', borderRadius: '8px' },
  variantName: { fontWeight: '700', fontSize: '15px', color: '#1a1a1a' },
  variantSplit: { fontSize: '13px', color: '#888', marginTop: '4px' },
  variantDesc: { fontSize: '13px', color: '#aaa', marginTop: '4px' },
  analyticsControls: { display: 'flex', gap: '12px', marginBottom: '20px' },
  eventInput: { padding: '10px 16px', border: '2px solid #e8e8e8', borderRadius: '8px', fontSize: '14px', flex: 1, outline: 'none' },
  analyzeBtn: { padding: '10px 24px', background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: '#fff', border: 'none', borderRadius: '8px', fontSize: '14px', fontWeight: '600', cursor: 'pointer' },
  winner: { background: '#f0fdf4', border: '1px solid #86efac', borderRadius: '8px', padding: '14px 20px', color: '#166534', fontSize: '15px' },
  noWinner: { background: '#f9f9f9', borderRadius: '8px', padding: '14px 20px', color: '#aaa', fontSize: '14px' },
  chartLabel: { fontSize: '13px', color: '#aaa', marginBottom: '8px' },
  table: { width: '100%', borderCollapse: 'collapse', marginTop: '24px' },
  th: { textAlign: 'left', padding: '12px 16px', background: '#f9f9f9', fontSize: '13px', fontWeight: '600', color: '#666' },
  td: { padding: '12px 16px', borderTop: '1px solid #f5f5f5', fontSize: '14px', color: '#1a1a1a' },
  dot: { display: 'inline-block', width: '10px', height: '10px', borderRadius: '50%', marginRight: '8px' },
  center: { display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100vh', color: '#aaa' }
};

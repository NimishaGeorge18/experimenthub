import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getExperiments } from '../api/experiments';

const statusColors = {
  draft: { bg: '#fff8e1', color: '#f59e0b' },
  running: { bg: '#e8f5e9', color: '#22c55e' },
  paused: { bg: '#fff3e0', color: '#f97316' },
  completed: { bg: '#ede9fe', color: '#7c3aed' }
};

export default function Experiments() {
  const [experiments, setExperiments] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    getExperiments()
      .then(res => setExperiments(res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <div style={styles.page}>
      {/* Navbar */}
      <div style={styles.navbar}>
        <h1 style={styles.brand}>ExperimentHub</h1>
        <div style={styles.navRight}>
          <button onClick={() => navigate('/experiments/new')} style={styles.newBtn}>
            + New Experiment
          </button>
          <button onClick={handleLogout} style={styles.logoutBtn}>
            Logout
          </button>
        </div>
      </div>

      {/* Content */}
      <div style={styles.content}>
        <h2 style={styles.title}>All Experiments</h2>
        <p style={styles.subtitle}>{experiments.length} experiment{experiments.length !== 1 ? 's' : ''} total</p>

        {loading ? (
          <p style={styles.empty}>Loading...</p>
        ) : experiments.length === 0 ? (
          <div style={styles.emptyState}>
            <p style={styles.emptyText}>No experiments yet.</p>
            <button onClick={() => navigate('/experiments/new')} style={styles.newBtn}>
              Create your first experiment
            </button>
          </div>
        ) : (
          <div style={styles.grid}>
            {experiments.map(exp => (
              <div
                key={exp.id}
                style={styles.card}
                onClick={() => navigate(`/experiments/${exp.id}`)}
              >
                <div style={styles.cardHeader}>
                  <h3 style={styles.cardTitle}>{exp.name}</h3>
                  <span style={{
                    ...styles.badge,
                    background: statusColors[exp.status]?.bg,
                    color: statusColors[exp.status]?.color
                  }}>
                    {exp.status}
                  </span>
                </div>
                {exp.description && (
                  <p style={styles.cardDesc}>{exp.description}</p>
                )}
                <div style={styles.cardFooter}>
                  <span style={styles.variantCount}>
                    {exp.variants.length} variants
                  </span>
                  <span style={styles.viewLink}>View details →</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

const styles = {
  page: { minHeight: '100vh', background: '#f0f2f5' },
  navbar: { background: '#fff', padding: '16px 32px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', boxShadow: '0 2px 8px rgba(0,0,0,0.08)' },
  brand: { fontSize: '22px', fontWeight: '800', color: '#667eea' },
  navRight: { display: 'flex', gap: '12px' },
  newBtn: { padding: '10px 20px', background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: '#fff', border: 'none', borderRadius: '8px', fontSize: '14px', fontWeight: '600' },
  logoutBtn: { padding: '10px 20px', background: '#f5f5f5', color: '#666', border: 'none', borderRadius: '8px', fontSize: '14px', fontWeight: '600' },
  content: { padding: '40px 32px', maxWidth: '1100px', margin: '0 auto' },
  title: { fontSize: '28px', fontWeight: '800', color: '#1a1a1a' },
  subtitle: { color: '#888', marginTop: '4px', marginBottom: '32px' },
  grid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', gap: '20px' },
  card: { background: '#fff', borderRadius: '12px', padding: '24px', boxShadow: '0 2px 12px rgba(0,0,0,0.06)', cursor: 'pointer', transition: 'transform 0.2s', border: '1px solid #f0f0f0' },
  cardHeader: { display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px' },
  cardTitle: { fontSize: '16px', fontWeight: '700', color: '#1a1a1a', flex: 1, marginRight: '12px' },
  badge: { padding: '4px 10px', borderRadius: '20px', fontSize: '12px', fontWeight: '600', whiteSpace: 'nowrap' },
  cardDesc: { fontSize: '14px', color: '#888', marginBottom: '16px', lineHeight: '1.5' },
  cardFooter: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '16px', paddingTop: '16px', borderTop: '1px solid #f5f5f5' },
  variantCount: { fontSize: '13px', color: '#aaa' },
  viewLink: { fontSize: '13px', color: '#667eea', fontWeight: '600' },
  emptyState: { textAlign: 'center', padding: '80px 0' },
  emptyText: { color: '#aaa', fontSize: '18px', marginBottom: '24px' },
  empty: { color: '#aaa', textAlign: 'center', marginTop: '80px' }
};

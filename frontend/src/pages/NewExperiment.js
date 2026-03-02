import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createExperiment } from '../api/experiments';

export default function NewExperiment() {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [variants, setVariants] = useState([
    { name: 'Control', traffic_split: 0.5 },
    { name: 'Treatment', traffic_split: 0.5 }
  ]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const updateVariant = (index, field, value) => {
    const updated = [...variants];
    updated[index] = { ...updated[index], [field]: value };
    setVariants(updated);
  };

  const addVariant = () => {
    setVariants([...variants, { name: '', traffic_split: 0 }]);
  };

  const removeVariant = (index) => {
    if (variants.length <= 2) return;
    setVariants(variants.filter((_, i) => i !== index));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    const total = variants.reduce((sum, v) => sum + parseFloat(v.traffic_split || 0), 0);
    if (Math.abs(total - 1.0) > 0.01) {
      setError(`Traffic splits must add up to 1.0 (currently ${total.toFixed(2)})`);
      setLoading(false);
      return;
    }
    try {
      const res = await createExperiment({ name, description, variants });
      navigate(`/experiments/${res.data.id}`);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create experiment.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.page}>
      <div style={styles.navbar}>
        <h1 style={styles.brand} onClick={() => navigate('/experiments')}>ExperimentHub</h1>
      </div>

      <div style={styles.content}>
        <button onClick={() => navigate('/experiments')} style={styles.back}>← Back</button>
        <h2 style={styles.title}>New Experiment</h2>

        <form onSubmit={handleSubmit} style={styles.form}>
          <div style={styles.section}>
            <h3 style={styles.sectionTitle}>Basic Info</h3>
            <div style={styles.field}>
              <label style={styles.label}>Experiment Name *</label>
              <input value={name} onChange={e => setName(e.target.value)} style={styles.input} placeholder="e.g. Checkout Button Test" required />
            </div>
            <div style={styles.field}>
              <label style={styles.label}>Description</label>
              <textarea value={description} onChange={e => setDescription(e.target.value)} style={styles.textarea} placeholder="What are you testing and why?" rows={3} />
            </div>
          </div>

          <div style={styles.section}>
            <h3 style={styles.sectionTitle}>Variants</h3>
            <p style={styles.hint}>Traffic splits must add up to 1.0 (100%)</p>
            {variants.map((v, i) => (
              <div key={i} style={styles.variantRow}>
                <input value={v.name} onChange={e => updateVariant(i, 'name', e.target.value)} style={{...styles.input, flex: 2}} placeholder={`Variant ${i + 1} name`} required />
                <input type="number" value={v.traffic_split} onChange={e => updateVariant(i, 'traffic_split', parseFloat(e.target.value))} style={{...styles.input, flex: 1}} step="0.1" min="0" max="1" required />
                {variants.length > 2 && (
                  <button type="button" onClick={() => removeVariant(i)} style={styles.removeBtn}>✕</button>
                )}
              </div>
            ))}
            <button type="button" onClick={addVariant} style={styles.addBtn}>+ Add Variant</button>
          </div>

          {error && <p style={styles.error}>{error}</p>}

          <button type="submit" style={loading ? {...styles.submitBtn, opacity: 0.7} : styles.submitBtn} disabled={loading}>
            {loading ? 'Creating...' : 'Create Experiment'}
          </button>
        </form>
      </div>
    </div>
  );
}

const styles = {
  page: { minHeight: '100vh', background: '#f0f2f5' },
  navbar: { background: '#fff', padding: '16px 32px', boxShadow: '0 2px 8px rgba(0,0,0,0.08)' },
  brand: { fontSize: '22px', fontWeight: '800', color: '#667eea', cursor: 'pointer' },
  content: { padding: '40px 32px', maxWidth: '680px', margin: '0 auto' },
  back: { background: 'none', border: 'none', color: '#667eea', fontSize: '14px', fontWeight: '600', marginBottom: '24px', padding: 0 },
  title: { fontSize: '28px', fontWeight: '800', marginBottom: '32px' },
  form: { display: 'flex', flexDirection: 'column', gap: '24px' },
  section: { background: '#fff', borderRadius: '12px', padding: '24px', boxShadow: '0 2px 12px rgba(0,0,0,0.06)' },
  sectionTitle: { fontSize: '16px', fontWeight: '700', marginBottom: '20px', color: '#1a1a1a' },
  field: { display: 'flex', flexDirection: 'column', gap: '6px', marginBottom: '16px' },
  label: { fontSize: '14px', fontWeight: '600', color: '#444' },
  input: { padding: '12px 16px', border: '2px solid #e8e8e8', borderRadius: '8px', fontSize: '15px', outline: 'none' },
  textarea: { padding: '12px 16px', border: '2px solid #e8e8e8', borderRadius: '8px', fontSize: '15px', outline: 'none', resize: 'vertical' },
  hint: { fontSize: '13px', color: '#aaa', marginBottom: '16px' },
  variantRow: { display: 'flex', gap: '12px', alignItems: 'center', marginBottom: '12px' },
  removeBtn: { padding: '8px 12px', background: '#fee2e2', color: '#ef4444', border: 'none', borderRadius: '8px', fontWeight: '700' },
  addBtn: { background: 'none', border: '2px dashed #e8e8e8', borderRadius: '8px', padding: '10px', width: '100%', color: '#aaa', fontSize: '14px', marginTop: '8px' },
  submitBtn: { padding: '16px', background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: '#fff', border: 'none', borderRadius: '8px', fontSize: '16px', fontWeight: '600' },
  error: { color: '#e53e3e', fontSize: '14px', textAlign: 'center' }
};

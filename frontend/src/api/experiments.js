import client from './client';

export const getExperiments = () => 
  client.get('/experiments/');

export const getExperiment = (id) => 
  client.get(`/experiments/${id}`);

export const createExperiment = (data) => 
  client.post('/experiments/', data);

export const updateStatus = (id, status) => 
  client.patch(`/experiments/${id}/status`, { status });

export const getAnalytics = (id, eventType) =>
  client.get(`/analytics/${id}?event_type=${eventType}`);
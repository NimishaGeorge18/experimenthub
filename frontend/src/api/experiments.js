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

export const assignVisitor = (experimentId, userId) =>
  client.post(`/assignments/${experimentId}`, { user_id: userId });

export const trackEvent = (userId, experimentId, eventType) =>
  client.post('/events/', {
    user_id: userId,
    experiment_id: Number(experimentId),
    event_type: eventType
  });
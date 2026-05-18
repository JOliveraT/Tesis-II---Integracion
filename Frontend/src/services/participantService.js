import apiClient from './apiClient';

export const participantService = {
  list(params = {}) { return apiClient.get('/participants/', { params }).then(r => r.data); },
  create(payload) { return apiClient.post('/participants/', payload).then(r => r.data); },
  bulkCreate(payload) { return apiClient.post('/participants/bulk', payload).then(r => r.data); },
  removeFromRaffle(raffleId, participantId, reason) {
    return apiClient.patch(`/raffles/${raffleId}/participants/${participantId}/remove`, { reason }).then(r => r.data);
  },
  importRedemptions(payload) { return apiClient.post('/redemptions/twitch', payload).then(r => r.data); },
};

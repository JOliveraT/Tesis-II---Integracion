import apiClient from './apiClient';

export const raffleService = {
  list() { return apiClient.get('/raffles/').then(r => r.data); },
  create(payload) { return apiClient.post('/raffles/', payload).then(r => r.data); },
  calculateScore(raffleId) { return apiClient.post(`/scoring/calculate/${raffleId}`).then(r => r.data); },
  selectWinner(raffleId) { return apiClient.post(`/winner/select/${raffleId}`).then(r => r.data); },
  startClaim(raffleId, claim_timeout_seconds = 30) { return apiClient.post(`/winner/start-claim/${raffleId}`, { claim_timeout_seconds }).then(r => r.data); },
  confirmWinner(raffleId) { return apiClient.post(`/winner/confirm/${raffleId}`).then(r => r.data); },
  expireWinner(raffleId) { return apiClient.post(`/winner/expire/${raffleId}`).then(r => r.data); },
  getById(raffleId) { return apiClient.get(`/raffles/${raffleId}/summary`).then(r => r.data); },
};

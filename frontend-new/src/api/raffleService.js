import { apiClient } from './apiClient';
export const raffleService = {
  list: () => apiClient.get('/raffles/'),
  create: (payload) => apiClient.post('/raffles/', payload),
  summary: (raffleId) => apiClient.get(`/raffles/${raffleId}/summary`),
  calculateScore: (raffleId) => apiClient.post(`/scoring/calculate/${raffleId}`, {}),
  selectWinner: (raffleId) => apiClient.post(`/winner/select/${raffleId}`, {}),
  startClaim: (raffleId, claim_timeout_seconds) => apiClient.post(`/winner/start-claim/${raffleId}`, { claim_timeout_seconds }),
  confirmWinner: (raffleId) => apiClient.post(`/winner/confirm/${raffleId}`, {}),
  expireClaim: (raffleId) => apiClient.post(`/winner/expire/${raffleId}`, {})
};

import { apiClient } from './apiClient';
export const participantService = {
  list: () => apiClient.get('/participants/'),
  create: (payload) => apiClient.post('/participants/', payload)
};

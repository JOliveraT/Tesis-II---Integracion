import { apiClient } from './apiClient';
export const messagesService = {
  list: () => apiClient.get('/messages/'),
  create: (payload) => apiClient.post('/messages/', payload)
};

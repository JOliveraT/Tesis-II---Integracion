import apiClient from './apiClient';

export const messagesService = {
  list(params = {}) { return apiClient.get('/messages/', { params }).then(r => r.data); },
};

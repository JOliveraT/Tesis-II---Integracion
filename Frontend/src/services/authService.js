import apiClient from './apiClient';

export const authService = {
  signUp(payload) { return apiClient.post('/auth/signup', payload).then((r) => r.data); },
  login(payload) { return apiClient.post('/auth/login', payload).then((r) => r.data); },
  me() { return apiClient.get('/auth/me').then((r) => r.data); },
};

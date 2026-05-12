import { apiClient } from './apiClient';

export const authService = {
  signUp: (payload) => apiClient.post('/auth/signup', payload),
  signIn: (payload) => apiClient.post('/auth/login', payload),
  me: () => apiClient.get('/auth/me'),
  getTwitchAuthUrl: () => apiClient.get('/twitch/auth-url')
};

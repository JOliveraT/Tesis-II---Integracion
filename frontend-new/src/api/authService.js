import { apiClient } from './apiClient';
export const authService = {
  getAuthUrl: () => apiClient.get('/twitch/auth-url'),
  callback: (code) => apiClient.get(`/twitch/callback?code=${encodeURIComponent(code)}`),
  me: () => apiClient.get('/twitch/me')
};

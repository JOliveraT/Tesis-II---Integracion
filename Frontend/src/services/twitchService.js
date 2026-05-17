import apiClient from './apiClient';

export const twitchService = {
  getAuthUrl() { return apiClient.get('/twitch/auth-url').then((r) => r.data); },
  callback(code) { return apiClient.get('/twitch/callback', { params: { code } }).then((r) => r.data); },
  getMe() { return apiClient.get('/twitch/me').then((r) => r.data); },
  disconnect() { return apiClient.delete('/twitch/disconnect').then((r) => r.data); },
};

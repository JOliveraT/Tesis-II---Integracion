import { apiClient } from './apiClient';
export const twitchService = {
  me: () => apiClient.get('/twitch/me'),
  authUrl: () => apiClient.get('/twitch/auth-url')
};

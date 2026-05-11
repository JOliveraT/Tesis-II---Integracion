import apiClient from './apiClient';

export const twitchService = {
  getMe() { return apiClient.get('/twitch/me').then(r => r.data); },
};

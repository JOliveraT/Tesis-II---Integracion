import apiClient from './apiClient';

export const authService = {
  async getAuthUrl() {
    const { data } = await apiClient.get('/twitch/auth-url');
    return data;
  },
  async getMe() {
    const { data } = await apiClient.get('/twitch/me');
    return data;
  },
  async callback(code) {
    const { data } = await apiClient.get('/twitch/callback', { params: { code } });
    return data;
  },
};

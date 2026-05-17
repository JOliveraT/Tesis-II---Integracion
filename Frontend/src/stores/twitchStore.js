import { defineStore } from 'pinia';
import { twitchService } from '@/services/twitchService';

export const useTwitchStore = defineStore('twitch', {
  state: () => ({ connected: false, channel: null, loading: false }),
  actions: {
    async refreshConnection() {
      this.loading = true;
      try {
        const data = await twitchService.getMe();
        this.connected = Boolean(data?.connected);
        this.channel = data?.channel || null;
        return data;
      } finally {
        this.loading = false;
      }
    },
    async loadProfile() {
      return this.refreshConnection();
    },
    async getAuthUrl() {
      return twitchService.getAuthUrl();
    },
    async unlinkChannel() {
      const data = await twitchService.disconnect();
      this.connected = false;
      this.channel = null;
      return data;
    }
  },
});

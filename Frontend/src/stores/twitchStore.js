import { defineStore } from 'pinia';
import { twitchService } from '@/services/twitchService';

export const useTwitchStore = defineStore('twitch', {
  state: () => ({ connected: false, profile: null, loading: false }),
  actions: {
    async loadProfile() {
      this.loading = true;
      try {
        const data = await twitchService.getMe();
        this.connected = Boolean(data?.connected);
        this.profile = data?.channel || null;
      } finally { this.loading = false; }
    },
    async linkChannel() {
      const data = await twitchService.getAuthUrl();
      if (data?.auth_url) window.location.href = data.auth_url;
    }
  },
});

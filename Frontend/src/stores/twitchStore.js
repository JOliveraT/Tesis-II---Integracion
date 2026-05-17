import { defineStore } from 'pinia';
import { twitchService } from '@/services/twitchService';

export const useTwitchStore = defineStore('twitch', {
  state: () => ({ connected: false, channel: null, tokenSaved: false, token_saved: false, loading: false }),
  actions: {
    async refreshConnection() {
      this.loading = true;
      try {
        const data = await twitchService.getMe();
        this.connected = Boolean(data?.connected);
        this.channel = data?.channel || null;
        const hasToken = Boolean(data?.token_saved ?? data?.tokenSaved);
        this.tokenSaved = hasToken;
        this.token_saved = hasToken;
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
    applyCallbackResult(payload) {
      this.connected = Boolean(payload?.connected);
      this.channel = payload?.channel || null;
      const hasToken = Boolean(payload?.token_saved ?? payload?.tokenSaved);
      this.tokenSaved = hasToken;
      this.token_saved = hasToken;
      return payload;
    },
    async completeCallback(code) {
      const data = await twitchService.callback(code);
      this.applyCallbackResult(data);
      return data;
    },
    async unlinkChannel() {
      const data = await twitchService.disconnect();
      this.connected = false;
      this.channel = null;
      this.tokenSaved = false;
      this.token_saved = false;
      return data;
    }
  },
});

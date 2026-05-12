import { defineStore } from 'pinia';
import { twitchService } from '../api/twitchService';

export const useTwitchStore = defineStore('twitch', {
  state: () => ({ connected: false, channel: null, authUrl: '' }),
  actions: {
    async refresh() {
      const data = await twitchService.me();
      this.connected = data.connected;
      this.channel = data.channel || null;
    },
    async fetchAuthUrl() {
      const data = await twitchService.authUrl();
      this.authUrl = data.auth_url;
      return data.auth_url;
    },
    async startLinking() {
      const url = await this.fetchAuthUrl();
      window.location.href = url;
    }
  }
});

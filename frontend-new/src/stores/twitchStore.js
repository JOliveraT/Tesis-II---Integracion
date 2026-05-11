import { defineStore } from 'pinia';
import { twitchService } from '../api/twitchService';

export const useTwitchStore = defineStore('twitch', {
  state: () => ({ connected: false, channel: null }),
  actions: {
    async refresh() {
      const data = await twitchService.me();
      this.connected = data.connected;
      this.channel = data.channel;
    }
  }
});

import { defineStore } from 'pinia';
import { twitchService } from '@/services/twitchService';

export const useTwitchStore = defineStore('twitch', {
  state: () => ({ profile: null }),
  actions: { async loadProfile() { this.profile = await twitchService.getMe(); } },
});

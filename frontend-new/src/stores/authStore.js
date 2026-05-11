import { defineStore } from 'pinia';
import { authService } from '../api/authService';

export const useAuthStore = defineStore('auth', {
  state: () => ({ channel: null, authUrl: '', loading: false }),
  actions: {
    async fetchAuthUrl() { this.authUrl = (await authService.getAuthUrl()).auth_url; },
    async fetchMe() { this.channel = (await authService.me()).channel; },
    async callback(code) { return authService.callback(code); }
  }
});

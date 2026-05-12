import { defineStore } from 'pinia';
import { authService } from '@/services/authService';

export const useAuthStore = defineStore('auth', {
  state: () => ({ user: null, token: localStorage.getItem('auth_token') || '', loading: false }),
  getters: { isAuthenticated: (s) => Boolean(s.token) },
  actions: {
    async signUp(payload) {
      this.loading = true;
      try {
        const data = await authService.signUp(payload);
        this.token = data.token;
        this.user = data.user;
        localStorage.setItem('auth_token', data.token);
        return data;
      } finally { this.loading = false; }
    },
    async login(payload) {
      this.loading = true;
      try {
        const data = await authService.login(payload);
        this.token = data.token;
        this.user = data.user;
        localStorage.setItem('auth_token', data.token);
        return data;
      } finally { this.loading = false; }
    },
    async fetchMe() {
      if (!this.token) return null;
      const data = await authService.me();
      this.user = data.user;
      return this.user;
    },
    logout() { this.user = null; this.token = ''; localStorage.removeItem('auth_token'); }
  },
});

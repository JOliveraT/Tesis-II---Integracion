import { defineStore } from 'pinia';
import { authService } from '../api/authService';

export const useAuthStore = defineStore('auth', {
  state: () => ({ user: null, token: localStorage.getItem('auth_token') || '', loading: false, error: '' }),
  getters: {
    isAuthenticated: (s) => Boolean(s.token)
  },
  actions: {
    async signUp(payload) {
      this.loading = true;
      this.error = '';
      try {
        const data = await authService.signUp(payload);
        if (data.access_token) {
          this.token = data.access_token;
          localStorage.setItem('auth_token', data.access_token);
        }
        this.user = data.user || null;
        return data;
      } finally { this.loading = false; }
    },
    async signIn(payload) {
      this.loading = true;
      this.error = '';
      try {
        const data = await authService.signIn(payload);
        this.token = data.access_token;
        localStorage.setItem('auth_token', data.access_token);
        this.user = data.user || null;
        return data;
      } finally { this.loading = false; }
    },
    async fetchMe() {
      if (!this.token) return null;
      this.user = await authService.me();
      return this.user;
    },
    logout() {
      this.token = '';
      this.user = null;
      localStorage.removeItem('auth_token');
    }
  }
});

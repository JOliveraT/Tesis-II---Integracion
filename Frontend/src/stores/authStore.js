import { defineStore } from 'pinia';
import { authService } from '@/services/authService';

export const useAuthStore = defineStore('auth', {
  state: () => ({ user: null, loading: false }),
  getters: { isAuthenticated: (s) => !!s.user },
  actions: {
    async fetchMe() {
      this.loading = true;
      try { this.user = await authService.getMe(); } catch { this.user = null; }
      this.loading = false;
    },
  },
});

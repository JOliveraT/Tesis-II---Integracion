import { defineStore } from 'pinia';
import { authService } from '@/services/authService';
import apiClient from '@/services/apiClient';

export const useAuthStore = defineStore('auth', {
  state: () => ({ user: null, token: '', loading: false }),
  getters: { isAuthenticated: (s) => Boolean(s.token && s.user) },
  actions: {
    loadTokenFromLocalStorage() {
      const token = localStorage.getItem('auth_token') || '';
      this.token = token;
      if (token) {
        apiClient.defaults.headers.common.Authorization = `Bearer ${token}`;
      } else {
        delete apiClient.defaults.headers.common.Authorization;
      }
      return token;
    },
    _setSession(data) {
      this.token = data.token;
      this.user = data.user;
      localStorage.setItem('auth_token', data.token);
      apiClient.defaults.headers.common.Authorization = `Bearer ${data.token}`;
    },
    async signUp(payload) {
      this.loading = true;
      try {
        const data = await authService.signUp(payload);
        this._setSession(data);
        return data;
      } finally { this.loading = false; }
    },
    async login(payload) {
      this.loading = true;
      try {
        const data = await authService.login(payload);
        this._setSession(data);
        return data;
      } finally { this.loading = false; }
    },
    async checkSession() {
      const token = this.token || this.loadTokenFromLocalStorage();
      if (!token) return null;
      try {
        const data = await authService.me();
        this.user = data.user;
        return this.user;
      } catch (error) {
        if (error?.response?.status === 401) {
          this.logout(false);
          return null;
        }
        throw error;
      }
    },
    logout(redirectToSignin = true) {
      this.user = null;
      this.token = '';
      localStorage.removeItem('auth_token');
      delete apiClient.defaults.headers.common.Authorization;
      if (redirectToSignin && window.location.pathname !== '/signin') {
        window.location.href = '/signin';
      }
    }
  },
});

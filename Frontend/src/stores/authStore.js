import { defineStore } from 'pinia';
import axios from 'axios';
import { authService } from '@/services/authService';
import apiClient from '@/services/apiClient';

export const useAuthStore = defineStore('auth', {
  state: () => ({ user: null, token: localStorage.getItem('auth_token') || '', loading: false }),
  getters: { isAuthenticated: (s) => Boolean(s.token) },
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
    async signUp(payload) {
      this.loading = true;
      try {
        const data = await authService.signUp(payload);
        this.token = data.token;
        this.user = data.user;
        localStorage.setItem('auth_token', data.token);
        apiClient.defaults.headers.common.Authorization = `Bearer ${data.token}`;
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
        apiClient.defaults.headers.common.Authorization = `Bearer ${data.token}`;
        return data;
      } finally { this.loading = false; }
    },
    async checkSession() {
      if (!this.token) return null;

      try {
        const data = await authService.me();
        this.user = data.user;
        return this.user;
      } catch (error) {
        const isUnauthorized = axios.isAxiosError(error) && error.response?.status === 401;

        if (isUnauthorized) {
          this.logout();
          return null;
        }

        throw error;
      }
    },
    async fetchMe() {
      return this.checkSession();
    },
    logout() {
      this.user = null;
      this.token = '';
      localStorage.removeItem('auth_token');
      delete apiClient.defaults.headers.common.Authorization;
    }
  },
});

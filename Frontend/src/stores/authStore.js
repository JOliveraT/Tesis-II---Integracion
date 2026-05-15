import { defineStore } from 'pinia';
import axios from 'axios';
import { authService } from '@/services/authService';
import apiClient from '@/services/apiClient';

const AUTH_TOKEN_KEY = 'auth_token';
const AUTH_USER_KEY = 'auth_user';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: '',
    rememberMe: false,
    loading: false,
  }),
  getters: {
    isAuthenticated: (state) => Boolean(state.token),
  },
  actions: {
    setSession({ user, token }, rememberMe = false) {
      this.user = user ?? null;
      this.token = token ?? '';
      this.rememberMe = Boolean(rememberMe);

      localStorage.removeItem(AUTH_TOKEN_KEY);
      sessionStorage.removeItem(AUTH_TOKEN_KEY);
      localStorage.removeItem(AUTH_USER_KEY);
      sessionStorage.removeItem(AUTH_USER_KEY);

      if (this.token) {
        const storage = this.rememberMe ? localStorage : sessionStorage;
        storage.setItem(AUTH_TOKEN_KEY, this.token);
        if (this.user) storage.setItem(AUTH_USER_KEY, JSON.stringify(this.user));
        apiClient.defaults.headers.common.Authorization = `Bearer ${this.token}`;
      } else {
        delete apiClient.defaults.headers.common.Authorization;
      }
    },

    loadTokenFromStorage() {
      const localToken = localStorage.getItem(AUTH_TOKEN_KEY);
      const sessionToken = sessionStorage.getItem(AUTH_TOKEN_KEY);
      const token = localToken || sessionToken || '';
      const rememberMe = Boolean(localToken);
      const rawUser = (rememberMe ? localStorage : sessionStorage).getItem(AUTH_USER_KEY);

      this.token = token;
      this.rememberMe = token ? rememberMe : false;
      this.user = rawUser ? JSON.parse(rawUser) : this.user;

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
        this.setSession(data, true);
        return data;
      } finally {
        this.loading = false;
      }
    },

    async login(payload, rememberMe = false) {
      this.loading = true;
      try {
        const data = await authService.login(payload);
        this.setSession(data, rememberMe);
        return data;
      } finally {
        this.loading = false;
      }
    },

    async checkSession() {
      if (!this.token) {
        this.loadTokenFromStorage();
      }

      if (!this.token) return null;

      try {
        const data = await authService.me();
        this.user = data.user;

        const storage = this.rememberMe ? localStorage : sessionStorage;
        if (this.user) storage.setItem(AUTH_USER_KEY, JSON.stringify(this.user));

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
      this.rememberMe = false;
      localStorage.removeItem(AUTH_TOKEN_KEY);
      sessionStorage.removeItem(AUTH_TOKEN_KEY);
      localStorage.removeItem(AUTH_USER_KEY);
      sessionStorage.removeItem(AUTH_USER_KEY);
      delete apiClient.defaults.headers.common.Authorization;
    },
  },
});

import { defineStore } from 'pinia';
import { raffleService } from '../api/raffleService';

export const useRaffleStore = defineStore('raffles', {
  state: () => ({ raffles: [], selectedRaffleId: '', summary: null, pollingId: null }),
  actions: {
    async loadRaffles() { this.raffles = await raffleService.list(); if (!this.selectedRaffleId && this.raffles[0]) this.selectedRaffleId = this.raffles[0].id; },
    async loadSummary() { if (!this.selectedRaffleId) return; this.summary = await raffleService.summary(this.selectedRaffleId); },
    startPolling() { this.stopPolling(); this.pollingId = setInterval(() => this.loadSummary(), 3000); },
    stopPolling() { if (this.pollingId) clearInterval(this.pollingId); this.pollingId = null; }
  }
});

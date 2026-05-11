import { defineStore } from 'pinia';
import { raffleService } from '@/services/raffleService';

export const useRaffleStore = defineStore('raffle', {
  state: () => ({ raffles: [], currentRaffle: null, pollingId: null, winnerState: null }),
  actions: {
    async loadRaffles() { this.raffles = await raffleService.list(); },
    async syncRaffle(raffleId) { this.currentRaffle = await raffleService.getById(raffleId); this.winnerState = this.currentRaffle?.winner_state || null; },
    startPolling(raffleId, intervalMs = 3000) {
      this.stopPolling();
      this.pollingId = setInterval(() => this.syncRaffle(raffleId), intervalMs);
    },
    stopPolling() { if (this.pollingId) clearInterval(this.pollingId); this.pollingId = null; },
  },
});

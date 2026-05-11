<script setup>
import { computed } from 'vue';
import { useRaffleStore } from '../stores/raffleStore';
import { raffleService } from '../api/raffleService';
const store = useRaffleStore();
const status = computed(() => store.summary?.raffle?.status || '-');
const result = computed(() => store.summary?.current_result || null);
const run = async () => { await raffleService.calculateScore(store.selectedRaffleId); await raffleService.selectWinner(store.selectedRaffleId); await store.loadSummary(); };
</script>
<template><div class='card'><h3>Draw</h3><p>Estado: {{ status }}</p><button class='btn' @click='run' :disabled='!store.selectedRaffleId'>Seleccionar ganador backend</button><p v-if='result'>Candidato: {{ result.winner_username }} / {{ result.claim_status }}</p></div></template>

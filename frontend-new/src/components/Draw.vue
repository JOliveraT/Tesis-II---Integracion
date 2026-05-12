<script setup>
import { computed, ref } from 'vue';
import { useRaffleStore } from '../stores/raffleStore';
import { useTwitchStore } from '../stores/twitchStore';
import { raffleService } from '../api/raffleService';
const store = useRaffleStore();
const twitch = useTwitchStore();
const showModal = ref(false);
const status = computed(() => store.summary?.raffle?.status || '-');
const result = computed(() => store.summary?.current_result || null);
const run = async () => {
  if (!twitch.connected) {
    showModal.value = true;
    return;
  }
  await raffleService.calculateScore(store.selectedRaffleId);
  await raffleService.selectWinner(store.selectedRaffleId);
  await store.loadSummary();
};
</script>
<template>
  <div class='card'>
    <h3>Draw</h3><p>Estado: {{ status }}</p>
    <button class='btn' @click='run' :disabled='!store.selectedRaffleId'>Seleccionar ganador backend</button>
    <p v-if='result'>Candidato: {{ result.winner_username }} / {{ result.claim_status }}</p>
  </div>
  <div v-if='showModal' class='overlay'>
    <section class='card modal'>
      <h3>Vincula Twitch primero</h3>
      <p>Debes vincular tu canal para iniciar sorteos.</p>
      <button class='btn' @click='twitch.startLinking()'>Vincular canal</button>
      <button class='btn ghost' @click='showModal=false'>Cerrar</button>
    </section>
  </div>
</template>

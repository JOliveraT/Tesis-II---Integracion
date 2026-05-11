<script setup>
import { computed } from 'vue';
import { useRaffleStore } from '../stores/raffleStore';
import AnimacionSorteo from './AnimacionSorteo.vue';
const store = useRaffleStore();
const winnerName = computed(() => store.summary?.current_result?.winner_username || '');
const stateLabel = computed(() => store.summary?.current_result?.claim_status || store.summary?.raffle?.status || '');
</script>
<template><AnimacionSorteo :winner-name='winnerName' :state-label='stateLabel' /></template>

<script setup>
import { onMounted,onUnmounted } from 'vue';
import NavbarDefault from '../components/NavbarDefault.vue';
import Draw from '../components/Draw.vue';
import AnimacionSorteoView from '../components/AnimacionSorteoView.vue';
import { useRaffleStore } from '../stores/raffleStore';
const store = useRaffleStore();
onMounted(async()=>{await store.loadRaffles(); await store.loadSummary(); store.startPolling();});
onUnmounted(()=>store.stopPolling());
</script>
<template><NavbarDefault /><main class='layout'><Draw /><AnimacionSorteoView /></main></template>

<script setup>
import { reactive } from 'vue';
import { useRaffleStore } from '../stores/raffleStore';
import { raffleService } from '../api/raffleService';
const store = useRaffleStore();
const form = reactive({ title:'', prize_title:'', prize_description:'', command:'!sorteo', confirmation_mode:'chat', claim_timeout_seconds:30 });
const create = async()=>{ await raffleService.create(form); await store.loadRaffles(); };
</script>
<template><section class='card'><h3>Raffles</h3><input v-model='form.title' placeholder='Título'/><input v-model='form.prize_title' placeholder='Premio'/><button class='btn' @click='create'>Crear</button><ul><li v-for='r in store.raffles' :key='r.id'>{{ r.title }} - {{ r.status }}</li></ul></section></template>

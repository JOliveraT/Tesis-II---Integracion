<script setup>
import { reactive, ref } from 'vue';
import { useRaffleStore } from '../stores/raffleStore';
import { participantService } from '../api/participantService';
const store = useRaffleStore(); const created = ref('');
const form = reactive({ raffle_id:'', username:'', display_name:'', twitch_user_id:'', entry_source:'chat', entry_content:'!sorteo'});
const add = async()=>{ form.raffle_id = store.selectedRaffleId; const data = await participantService.create(form); created.value = data.participant?.username || ''; await store.loadSummary(); };
</script>
<template><section class='card'><h3>Participants</h3><input v-model='form.username' placeholder='username'/><input v-model='form.display_name' placeholder='display name'/><button class='btn' @click='add'>Agregar backend</button><p v-if='created'>Creado: {{ created }}</p></section></template>

<script setup>
import { onMounted } from 'vue';
import { useAuthStore } from '../stores/authStore';
const auth = useAuthStore();
onMounted(() => auth.fetchAuthUrl());
</script>
<template><section class='card'><h3>Login con Twitch</h3><a class='btn' :href='auth.authUrl'>Conectar Twitch</a></section></template>

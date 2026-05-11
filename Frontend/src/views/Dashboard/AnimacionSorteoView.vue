<template>
  <AnimacionSorteo :participantes="participantes" :premio="premio" @finalizado="notificarGanador" />
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import AnimacionSorteo from '@/components/AnimacionSorteo.vue';

const route = useRoute();

const participantes = ref([]);
const premio = ref('');

onMounted(() => {
  const query = route.query;
  if (query.names) {
    participantes.value = query.names.split(',');
  }
  if (query.prize) {
    premio.value = query.prize;
  }
});

function notificarGanador(nombre) {
  if (window.opener) {
    window.opener.postMessage({ ganador: nombre }, '*');
    setTimeout(() => {
      window.close();
    }, 2500);
  }
}
</script>

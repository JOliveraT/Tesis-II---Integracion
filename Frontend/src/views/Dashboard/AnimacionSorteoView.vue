<template>
  <AnimacionSorteo
    :participantes="participantes"
    :premio="premio"
    :forcedWinner="winner"
    @finalizado="finalizarAnimacion"
  />
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import AnimacionSorteo from '@/components/AnimacionSorteo.vue';

const route = useRoute();

const participantes = ref([]);
const premio = ref('');
const winner = ref('');

onMounted(() => {
  const query = route.query;
  if (query.names) {
    participantes.value = query.names.split(',');
  }
  if (query.prize) {
    premio.value = query.prize;
  }
  if (query.winner) {
    winner.value = query.winner;
  }
});

function finalizarAnimacion(nombreAnimacion) {
  const ganadorFinal = winner.value || nombreAnimacion;
  if (!ganadorFinal) {
    console.warn('[AnimacionSorteoView] La animación finalizó sin ganador válido.');
    return;
  }
  if (window.opener) {
    window.opener.postMessage({ ganador: ganadorFinal }, '*');
    setTimeout(() => {
      window.close();
    }, 2500);
  }
}
</script>

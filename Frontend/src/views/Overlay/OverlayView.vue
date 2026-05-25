<template>
  <div class="overlay-root">
    <AnimacionSorteo
      v-if="currentState === 'raffle_animation'"
      :participantes="participants"
      :premio="prize"
      :forcedWinner="winner"
      @finalizado="onAnimationFinished"
    />

    <div v-else-if="currentState === 'winner_direct'" class="winner-card">
      <h2>🎉 Ganador</h2>
      <p class="winner-name">{{ winner || 'Sin ganador' }}</p>
      <p class="winner-prize">Premio: {{ prize || 'Sin premio' }}</p>
    </div>
  </div>
</template>

<script>
import AnimacionSorteo from '@/components/AnimacionSorteo.vue';
import { overlayService } from '@/services/overlayService';

export default {
  name: 'OverlayView',
  components: { AnimacionSorteo },
  data() {
    return {
      currentState: 'idle',
      payload: {},
      pollIntervalId: null,
    };
  },
  computed: {
    overlayToken() {
      return this.$route.params.overlayToken;
    },
    participants() {
      return Array.isArray(this.payload?.participants) ? this.payload.participants : [];
    },
    winner() {
      return this.payload?.winner || '';
    },
    prize() {
      return this.payload?.prize || '';
    },
  },
  async mounted() {
    await this.fetchState();
    this.pollIntervalId = window.setInterval(() => {
      this.fetchState();
    }, 2000);
  },
  beforeUnmount() {
    if (this.pollIntervalId) {
      window.clearInterval(this.pollIntervalId);
      this.pollIntervalId = null;
    }
  },
  methods: {
    async fetchState() {
      try {
        const state = await overlayService.getOverlayState(this.overlayToken);
        this.currentState = state?.current_state || 'idle';
        this.payload = state?.payload || {};
      } catch (error) {
        console.warn('[OverlayView] No se pudo consultar estado de overlay:', error);
      }
    },
    onAnimationFinished() {
      // Se mantiene el estado en backend hasta siguiente actualización desde panel.
    },
  },
};
</script>

<style scoped>
.overlay-root {
  width: 100vw;
  height: 100vh;
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.winner-card {
  background: rgba(0, 0, 0, 0.75);
  color: #fff;
  border-radius: 16px;
  padding: 2rem;
  text-align: center;
  min-width: 320px;
}

.winner-name {
  font-size: 2rem;
  font-weight: 700;
  margin: 0.5rem 0;
}
</style>

<template>
  <div class="overlay-root">
    <AnimacionSorteo
      v-if="showAnimation"
      :key="animationRenderKey"
      :participantes="participants"
      :premio="prize"
      :forcedWinner="winner"
      @finalizado="onAnimationFinished"
    />

    <div v-else-if="currentState === 'winner_direct'" class="status-card">
      <h2>🎉 Ganador</h2>
      <p class="winner-name">{{ winner || 'Sin ganador' }}</p>
      <p>Premio: {{ prize || 'Sin premio' }}</p>
    </div>

    <div v-else-if="currentState === 'claim_pending'" class="status-card">
      <h2>⏳ Confirmación pendiente</h2>
      <p class="winner-name">{{ winner || 'Sin ganador' }}</p>
      <p>Premio: {{ prize || 'Sin premio' }}</p>
      <p>{{ claimMessage }}</p>
      <p class="countdown">Tiempo restante: {{ claimCountdownRemaining }}s</p>
    </div>

    <div v-else-if="currentState === 'claim_confirmed'" class="status-card">
      <h2>✅ Ganador confirmado</h2>
      <p class="winner-name">{{ winner || 'Sin ganador' }}</p>
      <p>Premio: {{ prize || 'Sin premio' }}</p>
    </div>

    <div v-else-if="currentState === 'claim_expired'" class="status-card">
      <h2>⌛ El ganador no confirmó a tiempo</h2>
      <p class="winner-name">{{ winner || 'Sin ganador' }}</p>
      <p>Premio: {{ prize || 'Sin premio' }}</p>
    </div>
  </div>
</template>

<script>
import AnimacionSorteo from '@/components/AnimacionSorteo.vue';
import { overlayService } from '@/services/overlayService';

const AUTO_HIDE_WINNER_MS = 10000;
const AUTO_HIDE_STATUS_MS = 10000;
const POLL_NORMAL_MS = 2000;
const POLL_BACKOFF_MS = 5000;

export default {
  name: 'OverlayView',
  components: { AnimacionSorteo },
  data() {
    return {
      currentState: 'idle',
      payload: {},
      pollTimeoutId: null,
      pollDelayMs: POLL_NORMAL_MS,
      consecutivePollErrors: 0,
      hideTimerId: null,
      claimCountdownIntervalId: null,
      claimCountdownRemaining: 0,
      lastAnimationKey: null,
      showAnimation: false,
      animationRenderKey: 'animation-initial',
      lastStateKeyHandled: null,
    };
  },
  computed: {
    overlayToken() { return this.$route.params.overlayToken; },
    participants() { return Array.isArray(this.payload?.participants) ? this.payload.participants : []; },
    winner() { return this.payload?.winner || ''; },
    prize() { return this.payload?.prize || ''; },
    claimMessage() { return this.payload?.message || 'El ganador debe confirmar en el chat'; },
  },
  async mounted() {
    await this.fetchState();
    this.scheduleNextPoll(this.pollDelayMs);
  },
  beforeUnmount() {
    this.clearTimers();
    this.clearPollTimer();
  },
  methods: {
    getStateKey(state) {
      const st = state?.current_state || 'idle';
      const payload = state?.payload || {};
      const raffleId = payload?.raffle_id || 'no-raffle';
      const winner = payload?.winner || 'no-winner';
      const updatedAt = state?.updated_at || 'no-updated-at';
      return `${st}::${raffleId}::${winner}::${updatedAt}`;
    },
    getAnimationKey(state) {
      const payload = state?.payload || {};
      return `${payload?.raffle_id || 'no-raffle'}::${payload?.winner || 'no-winner'}::${state?.updated_at || 'no-updated-at'}`;
    },
    clearTimers() {
      if (this.hideTimerId) { window.clearTimeout(this.hideTimerId); this.hideTimerId = null; }
      if (this.claimCountdownIntervalId) { window.clearInterval(this.claimCountdownIntervalId); this.claimCountdownIntervalId = null; }
    },
    clearPollTimer() {
      if (this.pollTimeoutId) { window.clearTimeout(this.pollTimeoutId); this.pollTimeoutId = null; }
    },
    scheduleNextPoll(delayMs) {
      this.clearPollTimer();
      this.pollTimeoutId = window.setTimeout(async () => {
        this.pollTimeoutId = null;
        await this.fetchState();
        this.scheduleNextPoll(this.pollDelayMs);
      }, delayMs);
    },
    async fetchState() {
      try {
        const state = await overlayService.getOverlayState(this.overlayToken);
        this.consecutivePollErrors = 0;
        this.pollDelayMs = POLL_NORMAL_MS;

        const nextState = state?.current_state || 'idle';
        const stateKey = this.getStateKey(state);

        this.currentState = nextState;
        this.payload = state?.payload || {};

        if (nextState === 'idle' || nextState === 'hidden') {
          this.clearTimers();
          this.showAnimation = false;
          return;
        }

        if (stateKey === this.lastStateKeyHandled) return;
        this.lastStateKeyHandled = stateKey;
        this.handleStateTransition(state);
      } catch (error) {
        this.consecutivePollErrors += 1;
        this.pollDelayMs = POLL_BACKOFF_MS;

        if (this.consecutivePollErrors <= 3) {
          console.warn('[OverlayView] No se pudo consultar estado de overlay:', error);
        }
      }
    },
    handleStateTransition(state) {
      const st = state?.current_state;
      this.clearTimers();

      if (st === 'raffle_animation') {
        const animationKey = this.getAnimationKey(state);
        if (animationKey === this.lastAnimationKey) return;
        this.lastAnimationKey = animationKey;
        this.showAnimation = false;
        this.animationRenderKey = `animation-${animationKey}`;
        this.$nextTick(() => { this.showAnimation = true; });
        return;
      }

      this.showAnimation = false;

      if (st === 'winner_direct') {
        this.scheduleAutoHide(AUTO_HIDE_WINNER_MS);
      } else if (st === 'claim_pending') {
        this.startClaimCountdown(state);
      } else if (st === 'claim_confirmed' || st === 'claim_expired') {
        this.scheduleAutoHide(AUTO_HIDE_STATUS_MS);
      }
    },
    scheduleAutoHide(delayMs) {
      this.hideTimerId = window.setTimeout(async () => {
        try { await overlayService.hideOverlay(this.overlayToken); } catch (error) { console.warn('[OverlayView] hideOverlay falló:', error); }
      }, delayMs);
    },
    startClaimCountdown(state) {
      const seconds = Number(state?.payload?.claim_timeout_seconds) || 30;
      this.claimCountdownRemaining = seconds;
      // TODO: en una fase futura, backend debe pasar a claim_confirmed al detectar confirmación real por chat antes de expirar.
      this.claimCountdownIntervalId = window.setInterval(async () => {
        this.claimCountdownRemaining -= 1;
        if (this.claimCountdownRemaining > 0) return;
        window.clearInterval(this.claimCountdownIntervalId);
        this.claimCountdownIntervalId = null;
        try {
          await overlayService.updateOverlayState({
            overlay_token: this.overlayToken,
            current_state: 'claim_expired',
            payload: {
              raffle_id: this.payload?.raffle_id,
              winner: this.payload?.winner,
              prize: this.payload?.prize,
              message: 'El ganador no confirmó a tiempo',
            },
          });
        } catch (error) {
          console.warn('[OverlayView] No se pudo pasar a claim_expired:', error);
        }
      }, 1000);
    },
    async onAnimationFinished() {
      const confirmationMode = this.payload?.confirmation_mode || 'instant';
      try {
        if (confirmationMode === 'chat_confirmation') {
          await overlayService.updateOverlayState({
            overlay_token: this.overlayToken,
            current_state: 'claim_pending',
            payload: {
              raffle_id: this.payload?.raffle_id,
              winner: this.payload?.winner,
              prize: this.payload?.prize,
              claim_timeout_seconds: Number(this.payload?.claim_timeout_seconds) || 30,
              message: 'El ganador debe confirmar en el chat',
            },
          });
          return;
        }

        await overlayService.updateOverlayState({
          overlay_token: this.overlayToken,
          current_state: 'winner_direct',
          payload: {
            raffle_id: this.payload?.raffle_id,
            winner: this.payload?.winner,
            prize: this.payload?.prize,
          },
        });
      } catch (error) {
        console.warn('[OverlayView] No se pudo actualizar estado post animación:', error);
      }
    },
  },
};
</script>

<style scoped>
.overlay-root { width: 100vw; height: 100vh; background: transparent; display: flex; align-items: center; justify-content: center; overflow: hidden; }
.status-card { background: rgba(0,0,0,.75); color:#fff; border-radius:16px; padding:2rem; text-align:center; min-width:320px; }
.winner-name { font-size: 2rem; font-weight: 700; margin: .5rem 0; }
.countdown { margin-top: .75rem; font-weight: 600; }
</style>

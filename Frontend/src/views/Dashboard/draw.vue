<template>
  <div class="draw-page-wrapper">
    <div class="draw-content" :class="{ 'is-locked': isDrawLocked }">
  <div class="container mt-4">
    <div v-if="drawError" class="alert alert-danger mb-3" role="alert">{{ drawError }}</div>
    <div v-if="drawSuccess" class="alert alert-success mb-3" role="alert">{{ drawSuccess }}</div>
    <div v-if="shouldShowRaffleTypeSelector" class="card shadow-sm mb-3">
      <div class="card-body">
        <h5 class="mb-2">Selecciona el tipo de sorteo</h5>
        <p class="text-sm mb-3">Debes crear un sorteo antes de continuar.</p>
        <div class="d-flex gap-2 flex-wrap">
          <button class="btn btn-primary" @click="createRaffleByMode('instant')" :disabled="isCreatingRaffle">
            Ganador directo
          </button>
          <button class="btn btn-outline-primary" @click="createRaffleByMode('chat_confirmation')" :disabled="isCreatingRaffle">
            Con confirmación
          </button>
        </div>
      </div>
    </div>
    <div class="row">
      <!-- Sección de Comando y Gestión (izquierda) -->
      <div class="col-lg-4 col-md-4 col-12 d-flex flex-column" style="min-height: 100%;">
        <div class="card shadow-lg flex-grow-1">
          <div class="card-body">
            <h5 class="card-title">Comando:</h5>
            <input
              type="text"
              class="form-control mb-3"
              v-model="command"
              placeholder="Escribe el comando"
              :disabled="isRaffleNotReady"
            />
  
            <h5 class="card-title mt-4">Gestionar Ingresos:</h5>
            <div class="d-flex justify-content-center mt-3">
              <button
                class="btn btn-warning me-2"
                @click="stopSort"
                :disabled="isStopped || isRaffleNotReady"
              >
                Detener
              </button>
              <button
                class="btn btn-success"
                @click="resumeSort"
                :disabled="!isStopped || isRaffleNotReady"
              >
                Reanudar
              </button>
            </div>
  
            <h5 class="mt-4">Agregar manualmente:</h5>
            <input
              type="text"
              class="form-control mb-3"
              v-model="manualInput"
              placeholder="Nombre del participante"
              :disabled="isRaffleNotReady"
            />
            <div class="d-flex justify-content-center">
              <button
                class="btn btn-primary mt-2"
                @click="addParticipant(manualInput)"
                :disabled="isRaffleNotReady || isRaffleRunning"
              >
                Agregar
              </button>
            </div>
  
            <!-- Configuración (Checkboxes) -->
            <h5 class="mt-4">Modo de Sorteo:</h5>
            <div class="form-check mb-2">
              <input
                class="form-check-input"
                type="checkbox"
                id="subsOnly"
                v-model="isOnlySubs"
                :disabled="isStopped || isRaffleNotReady"
              />
              <label class="form-check-label" for="subsOnly">Solo Subs</label>
            </div>
            <div class="form-check mb-2">
              <input
                class="form-check-input"
                type="checkbox"
                id="followers"
                v-model="isFollowers"
                :disabled="isStopped || isRaffleNotReady"
              />
              <label class="form-check-label" for="followers">Seguidores</label>
            </div>
            <div class="form-check mb-2">
              <input
                class="form-check-input"
                type="checkbox"
                id="general"
                v-model="isGeneral"
                :disabled="isStopped || isRaffleNotReady"
              />
              <label class="form-check-label" for="general">General</label>
            </div>
            <div class="form-check mb-2">
              <input
                class="form-check-input"
                type="checkbox"
                id="collaborators"
                v-model="isCollaborators"
                :disabled="isStopped || isRaffleNotReady"
              />
              <label class="form-check-label" for="collaborators">Colaboradores</label>
            </div>
  
            <!-- Rondas al Agua -->
            <h5 class="mt-4">Rondas al agua:</h5>
            <input
              type="number"
              class="form-control mb-3"
              v-model="rounds"
              min="0"
              :disabled="isStopped || isRaffleNotReady"
            />
          </div>
        </div>
      </div>
  
      <!-- Sección del Centro (Participantes) -->
      <div class="col-lg-4 col-md-4 col-12 d-flex flex-column" style="min-height: 100%;" ref="centerColumn">
        <div class="card shadow-lg flex-grow-1">
          <div class="card-body">
            <h5 class="card-title">Estamos sorteando:</h5>
            <input
              type="text"
              class="form-control mb-4"
              v-model="prize"
              placeholder="¿Qué estamos sorteando?"
              ref="prizeInput"
              :disabled="isRaffleNotReady"
            />
            <h6 class="d-flex justify-content-between">
              Participantes: {{ participants.length }}
              <button class="btn btn-danger btn-sm" @click="clearParticipants" ref="clearButton"  :disabled="isRaffleNotReady || isRaffleRunning">Limpiar</button>
            </h6>

            <!-- Lista de participantes con scroll -->
            <div
              class="participants-container"
              :style="{
                height: participantsHeight + 'px',
                overflowY: 'auto',
                border: '1px solid #ddd',
                borderRadius: '5px',
                marginBottom: '20px',
              }"
            >
              <ul class="list-group mb-0">
                <li
                  v-for="(participant, index) in participants"
                  :key="index"
                  class="list-group-item d-flex justify-content-between"
                  @click="removeParticipant(index)"
                  @mouseover="hoverParticipant(index)"
                  @mouseleave="hoverParticipant(-1)"
                  :style="{
                    cursor: 'pointer',
                    backgroundColor: hoverIndex === index ? 'rgba(255, 0, 0, 0.1)' : '',
                  }"
                >
                  {{ participant }}
                </li>
              </ul>
            </div>

            <!-- Botón de Sorteo -->
            <div class="text-center mt-3">
              <button class="btn btn-primary" @click="startSort"  :disabled="isStopped || isRaffleNotReady || isRaffleRunning || isSyncingParticipants">¡A SORTEAR!</button>
            </div>
          </div>
        </div>

         <!-- 🔥 Animación de sorteo -->
        <AnimacionSorteo
          v-if="mostrarAnimacion"
          :participantes="participants"
          :premio="prize"
          :forcedWinner="winner"
          @finalizado="onAnimacionFinalizada"
        />
      </div>
      
  
      <!-- Sección del Derecho (Ganador y Contador) -->
      <div class="col-lg-4 col-md-4 col-12 mt-4 mt-md-0 d-flex flex-column" style="min-height: 100%;">
        <div class="card shadow-lg flex-grow-1">
          <div class="card-body">
            <!-- Ganador -->
            <h5 class="card-title">Ganador:</h5>
            <input
              type="text"
              class="form-control mb-3"
              v-model="winner"
              placeholder="Nombre del ganador"
              :disabled="isRaffleNotReady"
            />

            <!-- Configuración del Contador -->
            <h5 class="card-title mt-4">Contador:</h5>
            <input
              type="number"
              class="form-control mb-3"
              v-model="countdown"
              placeholder="Segundos"
              min="1"
               :disabled="isDrawLocked || !hasActiveRaffle || isClaimStarted"
            />

            <!-- Botón de iniciar contador -->
            <div class="d-flex justify-content-center mt-3">
              <button class="btn btn-success" @click="startCountdown" :disabled="!canStartCountdown">Iniciar contador</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  </div>

    <div v-if="isDrawLocked" class="draw-lock-overlay">
      <div class="card draw-lock-card shadow-lg">
        <div class="card-body p-4">
          <h5 class="mb-2">Vincula una plataforma para usar Sorteos</h5>
          <p class="text-sm mb-4">
            Para registrar participantes desde el chat, comandos, recompensas del canal y confirmar ganadores en tiempo real, primero necesitas vincular una plataforma de streaming compatible. Actualmente puedes vincular Twitch desde tu perfil.
          </p>

          <div class="d-flex flex-wrap gap-2 justify-content-end">
            <button class="btn btn-outline-secondary mb-0" @click="goToDashboard">
              Volver al dashboard
            </button>
            <button class="btn bg-gradient-success mb-0" @click="goToConnections">
              Ir a vincular
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>
  
  <script>
import AnimacionSorteo from '@/components/AnimacionSorteo.vue';
import { raffleService } from '@/services/raffleService';
import { participantService } from '@/services/participantService';
import { useTwitchStore } from '@/stores/twitchStore';
import { useAuthStore } from '@/stores/authStore';
import { overlayService } from '@/services/overlayService';

  export default {
    components: {
      AnimacionSorteo, // ✅ REGISTRO NECESARIO
    },
    data() {
      return {
        command: "",
        prize: "",
        manualInput: "",
        participants: [],
        isStopped: false,
        winner: "",
        countdown: 10,
        isOnlySubs: false,
        isFollowers: false,
        isGeneral: true,
        isCollaborators: false,
        rounds: 0,
        hoverIndex: -1, // Indice del participante sobre el cual se pasa el mouse
        participantsHeight: 0, // Variable para almacenar la altura dinámica de la lista de participantes
        mostrarAnimacion: false,
        raffleId: null,
        confirmationMode: null,
        isCreatingRaffle: false,
        drawError: "",
        drawSuccess: "",
        manualParticipantsSynced: false,
        isSyncingParticipants: false,
        isRaffleRunning: false,
        isClaimStarted: false,
        claimExpiresAt: null,
        twitchStore: null,
        authStore: null,
      };
    },
    computed: {
      hasConnectedPlatform() {
        return Boolean(this.twitchStore?.connected);
      },
      isDrawLocked() {
        return !this.hasConnectedPlatform;
      },
      hasActiveRaffle() {
        return Boolean(this.raffleId);
      },
      shouldShowRaffleTypeSelector() {
        return !this.isDrawLocked && !this.hasActiveRaffle;
      },
      isRaffleNotReady() {
        return this.isDrawLocked || !this.hasActiveRaffle || this.isCreatingRaffle || this.isRaffleRunning;
      },
      canStartCountdown() {
        return !this.isDrawLocked && this.hasActiveRaffle && this.confirmationMode === "chat_confirmation" && Boolean(this.winner) && !this.isClaimStarted;
      },
    },
    async mounted() {
      this.twitchStore = useTwitchStore();
      this.authStore = useAuthStore();
      this.authStore.loadTokenFromStorage();
      if (!this.authStore?.token || !this.authStore?.user) {
        this.$router.push('/signin');
        return;
      }
      if (typeof this.twitchStore.refreshConnection === 'function') {
        await this.twitchStore.refreshConnection();
      }
      // Calcular la altura dinámica cuando el componente se monte
      this.updateParticipantsHeight();

      window.addEventListener('message', (event) => {
        const ganadorAnimacion = event?.data?.ganador;
        if (!ganadorAnimacion) return;
        if (!this.winner) {
          this.winner = ganadorAnimacion;
          return;
        }
        if (ganadorAnimacion === this.winner) return;
        console.warn(
          '[draw.vue] Se ignoró un ganador distinto enviado por la animación.',
          { ganadorBackend: this.winner, ganadorAnimacion }
        );
      });
    },
    methods: {
      goToConnections() {
        this.$router.push({ name: 'Profile', query: { tab: 'connections' } }).catch(() => {
          this.$router.push('/dashboard-layout/profile?tab=connections');
        });
      },
      goToDashboard() {
        this.$router.push({ name: 'Dashboard' }).catch(() => {
          this.$router.push('/dashboard-layout');
        });
      },
      guardDrawActions() {
        return !this.isDrawLocked;
      },
      extractRaffleId(response) {
        return response?.raffle?.id
          || response?.data?.raffle?.id
          || response?.data?.id
          || response?.data?.[0]?.id
          || response?.data?.data?.raffle?.id
          || response?.data?.data?.id
          || response?.data?.data?.[0]?.id
          || response?.payload?.raffle?.id
          || response?.payload?.id
          || response?.payload?.[0]?.id
          || response?.id
          || null;
      },
      extractWinnerName(response) {
        const winnerName = response?.winner?.username
          || response?.winner?.display_name
          || response?.winner_name
          || response?.winner_username
          || response?.username
          || response?.display_name
          || response?.data?.winner?.username
          || response?.data?.winner?.display_name
          || response?.data?.winner_name
          || response?.data?.winner_username
          || response?.data?.username
          || response?.data?.display_name
          || response?.data?.[0]?.winner_username
          || response?.data?.[0]?.winner_name
          || response?.data?.[0]?.username
          || response?.data?.[0]?.display_name
          || response?.data?.[0]?.participant?.username
          || response?.data?.[0]?.participant?.display_name
          || response?.participant?.username
          || response?.participant?.display_name
          || '';
        return typeof winnerName === 'string' ? winnerName.trim() : '';
      },
      async createRaffleByMode(mode) {
        if (!this.guardDrawActions() || this.isCreatingRaffle) return;
        this.drawError = "";
        this.drawSuccess = "";
        this.isCreatingRaffle = true;
        try {
          const payload = {
            title: this.prize || "Sorteo",
            prize_title: this.prize || "Premio",
            prize_description: this.prize || "Premio",
            command: this.command || "!sorteo",
            confirmation_mode: mode,
            claim_timeout_seconds: Number(this.countdown) || 25,
          };
          const raffleResp = await raffleService.create(payload);
          const raffleId = this.extractRaffleId(raffleResp);
          if (!raffleId) {
            throw new Error("No se recibió el ID del sorteo creado.");
          }
          this.raffleId = raffleId;
          this.confirmationMode = mode;
          this.manualParticipantsSynced = false;
          this.isRaffleRunning = false;
          this.isClaimStarted = false;
          this.drawSuccess = "Sorteo creado correctamente.";
        } catch (error) {
          this.drawError = "No se pudo crear el sorteo. Intenta nuevamente.";
        } finally {
          this.isCreatingRaffle = false;
        }
      },
      addParticipant(name) {
        if (!this.guardDrawActions()) return;
        if (!this.hasActiveRaffle) { this.drawError = "Primero selecciona el tipo de sorteo."; return; }
        if (this.isRaffleRunning) return;
        const cleaned = (name || "").trim();
        if (!cleaned) return;
        const exists = this.participants.some((p) => p.trim().toLowerCase() === cleaned.toLowerCase());
        if (exists) { this.drawError = "Ese participante ya fue agregado."; return; }
        this.drawError = "";
        this.participants.push(cleaned);
        this.manualInput = "";
        this.manualParticipantsSynced = false;
      },
      removeParticipant(index) {
        if (!this.guardDrawActions() || this.isRaffleRunning) return;
        this.participants.splice(index, 1);
        this.manualParticipantsSynced = false;
      },
      stopSort() {
        if (!this.guardDrawActions()) return;
        this.isStopped = true;
      },
      resumeSort() {
        if (!this.guardDrawActions()) return;
        this.isStopped = false;
      },
      async startCountdown() {
        if (!this.guardDrawActions()) return;
        if (this.confirmationMode !== "chat_confirmation") { this.drawError = "El contador solo aplica a sorteos con confirmación."; return; }
        if (!this.raffleId || !this.winner) { this.drawError = "Debes tener un ganador antes de iniciar contador."; return; }
        this.drawError = "";
        await raffleService.startClaim(this.raffleId, Number(this.countdown) || 25);
        this.isClaimStarted = true;
      },
      clearParticipants() {
        if (!this.guardDrawActions() || this.isRaffleRunning) return;
        this.participants = [];
        this.manualParticipantsSynced = false;
        // TODO: cuando existan participantes sincronizados desde backend, usar soft-remove para los que ya estén persistidos.
      },
      async getOverlayTokenForStreamer() {
        if (this.overlayToken) return this.overlayToken;
        try {
          const data = await overlayService.getMyOverlay();
          this.overlayToken = data?.overlay_token || '';
          return this.overlayToken;
        } catch (error) {
          console.warn('[draw.vue] No se pudo obtener overlay token real:', error);
          return '';
        }
      },

      async startSort() {
        if (!this.guardDrawActions()) return;
        if (!this.hasActiveRaffle) {
          this.drawError = "Primero selecciona el tipo de sorteo.";
          return;
        }
        if (!this.participants.length) {
          this.drawError = "Agrega al menos un participante antes de sortear.";
          return;
        }
        this.drawError = "";
        this.drawSuccess = "";
        this.isRaffleRunning = true;
        try {
          if (!this.manualParticipantsSynced) {
            this.isSyncingParticipants = true;
            await participantService.bulkCreate({
              raffle_id: this.raffleId,
              participants: this.participants.map((name) => ({
                username: name.trim().toLowerCase().replace(/\s+/g, "_"),
                display_name: name.trim(),
                entry_source: "manual",
              })),
            });
            this.manualParticipantsSynced = true;
          }
          await raffleService.calculateScore(this.raffleId);
          const winnerResponse = await raffleService.selectWinner(this.raffleId);
          console.log("winner/select response:", winnerResponse);
          const extractedWinnerName = this.extractWinnerName(winnerResponse);
          if (!extractedWinnerName) {
            console.warn('[draw.vue] No se pudo extraer ganador desde winner/select:', winnerResponse);
            this.drawError = "No se pudo identificar el ganador devuelto por el backend.";
            return;
          }
          this.winner = extractedWinnerName;
          this.drawSuccess = "Ganador seleccionado.";

          const prizeTitle = typeof this.prizeTitle === 'string' ? this.prizeTitle : '';
          const prizeName = (this.prize || prizeTitle || '').trim() || "Sin premio";
          const nombresURL = encodeURIComponent(this.participants.join(','));
          const premioURL = encodeURIComponent(prizeName);
          const ganadorURL = encodeURIComponent(extractedWinnerName);
          const url = `/dashboard-layout/draw/animation?names=${nombresURL}&prize=${premioURL}&winner=${ganadorURL}`;
          const width = screen.availWidth;
          const height = screen.availHeight;
          window.open(url, 'AnimacionSorteo', `width=${width},height=${height},top=0,left=0,resizable=yes,scrollbars=no`);

          const overlayToken = await this.getOverlayTokenForStreamer();
          if (overlayToken) {
            overlayService.updateOverlayState({
              overlay_token: overlayToken,
            current_state: 'raffle_animation',
            payload: {
              raffle_id: this.raffleId,
              participants: Array.isArray(this.participants) ? this.participants : [],
              winner: extractedWinnerName,
              prize: prizeName,
              confirmation_mode: this.confirmationMode || 'instant',
              claim_timeout_seconds: Number(this.countdown) || 30,
            },
            }).catch((overlayError) => {
              console.warn('[draw.vue] No se pudo actualizar overlay fijo:', overlayError);
            });
          } else {
            console.warn('[draw.vue] No hay overlay_token disponible; el sorteo continuará sin overlay fijo.');
          }
        } catch (error) {
          this.drawError = "No se pudo completar el sorteo. Revisa la conexión e intenta nuevamente.";
        } finally {
          this.isSyncingParticipants = false;
          this.isRaffleRunning = false;
        }
      },

      onAnimacionFinalizada(nombreGanador) {
        this.winner = nombreGanador;
        this.mostrarAnimacion = false;
      },
      hoverParticipant(index) {
        this.hoverIndex = index === this.hoverIndex ? -1 : index;
      },
      // Método para calcular la altura dinámica
    updateParticipantsHeight() {
      // Obtener la altura total de la sección del centro
      const centerColumn = this.$refs.centerColumn;
      const centerHeight = centerColumn ? centerColumn.clientHeight : 0;

      // Medir dinámicamente la altura de los elementos dentro de la sección central
      const prizeInputHeight = this.$refs.prizeInput ? this.$refs.prizeInput.clientHeight : 0;
      const clearButtonHeight = this.$refs.clearButton ? this.$refs.clearButton.clientHeight : 0;
      
      // Altura de otros elementos (como el título, márgenes, etc.)
      const otherElementsHeight = prizeInputHeight + clearButtonHeight + 210; // 40px es el margen adicional por si lo necesitas ajustar


      // Establecer la altura dinámica del contenedor de participantes
      this.participantsHeight = centerHeight - otherElementsHeight;
    },
    },
    watch: {
    // Recalcular la altura de los participantes cuando el tamaño de la ventana cambie
    '$route'(to, from) {
      this.updateParticipantsHeight();
    },
    '$nextTick'() {
      this.updateParticipantsHeight();
    },
  },
  };
  </script>
  
  <style scoped>
  /* Estilo para los inputs con borde ligero y margen interno */
  .form-control {
    border: 1px solid #ced4da;
    padding-left: 15px;
  }
  
  /* Estilo para las tarjetas */
  .card {
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
  
  /* Contenedor de participantes con scroll */
  .participants-container {
    overflow-y: auto;
    border: 1px solid #ddd;
    border-radius: 5px;
    margin-bottom: 20px;
  }
  
  /* Columna responsiva */
  @media (max-width: 768px) {
    .col-md-4 {
      flex: 0 0 100%;
    }
  }
  .list-group-item {
  margin: 0 !important;
  padding-left: 20px ;
  padding-right: 10px;
  padding-top: 5px;
  padding-bottom: 5px;
  }
  .draw-page-wrapper {
    position: relative;
  }

  .draw-content.is-locked {
    filter: blur(3px);
    pointer-events: none;
    user-select: none;
  }

  .draw-lock-overlay {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 1.5rem;
    z-index: 20;
    background: rgba(15, 23, 42, 0.22);
  }

  .draw-lock-card {
    max-width: 620px;
    width: 100%;
    border-radius: 0.9rem;
  }
  </style>
  

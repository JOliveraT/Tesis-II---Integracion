<template>
  <div class="draw-page-wrapper">
    <div class="draw-content" :class="{ 'is-locked': isDrawLocked }">
  <div class="container mt-4">
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
              :disabled="isDrawLocked"
            />
  
            <h5 class="card-title mt-4">Gestionar Ingresos:</h5>
            <div class="d-flex justify-content-center mt-3">
              <button
                class="btn btn-warning me-2"
                @click="stopSort"
                :disabled="isStopped || isDrawLocked"
              >
                Detener
              </button>
              <button
                class="btn btn-success"
                @click="resumeSort"
                :disabled="!isStopped || isDrawLocked"
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
              :disabled="isDrawLocked"
            />
            <div class="d-flex justify-content-center">
              <button
                class="btn btn-primary mt-2"
                @click="addParticipant(manualInput)"
                :disabled="isDrawLocked"
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
                :disabled="isStopped || isDrawLocked"
              />
              <label class="form-check-label" for="subsOnly">Solo Subs</label>
            </div>
            <div class="form-check mb-2">
              <input
                class="form-check-input"
                type="checkbox"
                id="followers"
                v-model="isFollowers"
                :disabled="isStopped || isDrawLocked"
              />
              <label class="form-check-label" for="followers">Seguidores</label>
            </div>
            <div class="form-check mb-2">
              <input
                class="form-check-input"
                type="checkbox"
                id="general"
                v-model="isGeneral"
                :disabled="isStopped || isDrawLocked"
              />
              <label class="form-check-label" for="general">General</label>
            </div>
            <div class="form-check mb-2">
              <input
                class="form-check-input"
                type="checkbox"
                id="collaborators"
                v-model="isCollaborators"
                :disabled="isStopped || isDrawLocked"
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
              :disabled="isStopped || isDrawLocked"
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
              :disabled="isDrawLocked"
            />
            <h6 class="d-flex justify-content-between">
              Participantes: {{ participants.length }}
              <button class="btn btn-danger btn-sm" @click="clearParticipants" ref="clearButton" :disabled="isDrawLocked">Limpiar</button>
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
              <button class="btn btn-primary" @click="startSort" :disabled="isStopped || isDrawLocked">¡A SORTEAR!</button>
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
              :disabled="isDrawLocked"
            />

            <!-- Configuración del Contador -->
            <h5 class="card-title mt-4">Contador:</h5>
            <input
              type="number"
              class="form-control mb-3"
              v-model="countdown"
              placeholder="Segundos"
              min="1"
              :disabled="isDrawLocked"
            />

            <!-- Botón de iniciar contador -->
            <div class="d-flex justify-content-center mt-3">
              <button class="btn btn-success" @click="startCountdown" :disabled="isDrawLocked">Iniciar contador</button>
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
        if (event.data && event.data.ganador) {
          this.winner = event.data.ganador;
        }
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
      addParticipant(name) {
        if (!this.guardDrawActions()) return;
        if (name.trim() !== "") {
          this.participants.push(name);
          this.manualInput = ""; // Limpiar después de agregar
        }
      },
      removeParticipant(index) {
        if (!this.guardDrawActions()) return;
        this.participants.splice(index, 1);
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
        if (!this.raffleId) return;
        await raffleService.startClaim(this.raffleId);
      },
      clearParticipants() {
        if (!this.guardDrawActions()) return;
        this.participants = [];
      },
      async startSort() {
        if (!this.guardDrawActions()) return;
        // TODO: reforzar también en backend que los endpoints de sorteo validen que el usuario tenga una plataforma compatible vinculada.
        if (this.participants.length > 0) {
          const raffleResp = await raffleService.create({ title: this.prize || 'Sorteo', prize_title: this.prize || 'Premio', prize_description: this.prize || 'Premio', command: this.command || '!sorteo', confirmation_mode: 'chat', claim_timeout_seconds: this.countdown || 30 });
          this.raffleId = raffleResp?.raffle?.id || raffleResp?.id;
          for (const name of this.participants) { await participantService.create({ raffle_id: this.raffleId, username: name.toLowerCase().replace(/\s+/g,'_'), display_name: name, entry_source: 'manual' }); }
          await raffleService.calculateScore(this.raffleId);
          const winnerResponse = await raffleService.selectWinner(this.raffleId);
          this.winner = winnerResponse?.winner_name || this.winner;

          const nombresURL = encodeURIComponent(this.participants.join(','));
          const premioURL = encodeURIComponent(this.prize || '');

          const url = `/dashboard-layout/draw/animation?names=${nombresURL}&prize=${premioURL}`;

          // Obtener el tamaño de pantalla disponible
          const width = screen.availWidth;
          const height = screen.availHeight;
          const left = 0;
          const top = 0;

          // Abrir ventana casi a pantalla completa
          window.open(
            url,
            'AnimacionSorteo',
            `width=${width},height=${height},top=${top},left=${left},resizable=yes,scrollbars=no`
          );
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
  

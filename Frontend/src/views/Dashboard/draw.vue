<template>
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
            />
  
            <h5 class="card-title mt-4">Gestionar Ingresos:</h5>
            <div class="d-flex justify-content-center mt-3">
              <button
                class="btn btn-warning me-2"
                @click="stopSort"
                :disabled="isStopped"
              >
                Detener
              </button>
              <button
                class="btn btn-success"
                @click="resumeSort"
                :disabled="!isStopped"
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
            />
            <div class="d-flex justify-content-center">
              <button
                class="btn btn-primary mt-2"
                @click="addParticipant(manualInput)"
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
                :disabled="isStopped"
              />
              <label class="form-check-label" for="subsOnly">Solo Subs</label>
            </div>
            <div class="form-check mb-2">
              <input
                class="form-check-input"
                type="checkbox"
                id="followers"
                v-model="isFollowers"
                :disabled="isStopped"
              />
              <label class="form-check-label" for="followers">Seguidores</label>
            </div>
            <div class="form-check mb-2">
              <input
                class="form-check-input"
                type="checkbox"
                id="general"
                v-model="isGeneral"
                :disabled="isStopped"
              />
              <label class="form-check-label" for="general">General</label>
            </div>
            <div class="form-check mb-2">
              <input
                class="form-check-input"
                type="checkbox"
                id="collaborators"
                v-model="isCollaborators"
                :disabled="isStopped"
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
              :disabled="isStopped"
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
            />
            <h6 class="d-flex justify-content-between">
              Participantes: {{ participants.length }}
              <button class="btn btn-danger btn-sm" @click="clearParticipants" ref="clearButton">Limpiar</button>
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
              <button class="btn btn-primary" @click="startSort" :disabled="isStopped">¡A SORTEAR!</button>
            </div>
          </div>
        </div>

         <!-- 🔥 Animación de sorteo -->
        <AnimacionSorteo
          v-if="mostrarAnimacion"
          :participantes="participants"
          :premio="prize"
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
            />

            <!-- Configuración del Contador -->
            <h5 class="card-title mt-4">Contador:</h5>
            <input
              type="number"
              class="form-control mb-3"
              v-model="countdown"
              placeholder="Segundos"
              min="1"
            />

            <!-- Botón de iniciar contador -->
            <div class="d-flex justify-content-center mt-3">
              <button class="btn btn-success" @click="startCountdown">Iniciar contador</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
  
  <script>
  import AnimacionSorteo from '@/components/AnimacionSorteo.vue';

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
      };
    },
    mounted() {
      // Calcular la altura dinámica cuando el componente se monte
      this.updateParticipantsHeight();

      window.addEventListener('message', (event) => {
        if (event.data && event.data.ganador) {
          this.winner = event.data.ganador;
        }
      });
    },
    methods: {
      addParticipant(name) {
        if (name.trim() !== "") {
          this.participants.push(name);
          this.manualInput = ""; // Limpiar después de agregar
        }
      },
      removeParticipant(index) {
        this.participants.splice(index, 1);
      },
      stopSort() {
        this.isStopped = true;
      },
      resumeSort() {
        this.isStopped = false;
      },
      startCountdown() {
        const interval = setInterval(() => {
          if (this.countdown <= 0) {
            clearInterval(interval);
          } else {
            this.countdown--;
          }
        }, 1000);
      },
      clearParticipants() {
        this.participants = [];
      },
      startSort() {
        if (this.participants.length > 0) {
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
  </style>
  
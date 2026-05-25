<template>
  <div class="overlay">
    <div class="fondo"></div>

    <!-- Nubes largas detrás -->
    <div class="clouds clouds-largas"></div>

    <!-- Nubes cortas encima -->
    <div class="clouds clouds-cortas"></div>

    <div class="ground">
      <div
        v-for="item in nombresConPosicion"
        :key="item.index"
        class="name"
        :class="{ gone: eliminatedIndices.includes(item.index) }"
        :style="{
          left: positions[item.index].x + 'px',
          bottom: positions[item.index].y + 'px',
          transform: 'scale(' + positions[item.index].scale + ')'
        }"
      >
        {{ item.name }}
      </div>
    </div>

    <div v-if="huracanActive" class="huracan"></div>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick, onMounted } from 'vue';
import { gsap } from 'gsap';

const props = defineProps({
  participantes: {
    type: Array,
    required: true
  },
  premio: {
    type: String,
    required: false
  },
  forcedWinner: {
    type: String,
    required: false,
    default: ''
  }
});

const emit = defineEmits(['finalizado']);
// Audios
const audioSorteo = new Audio('/sorteo.mp3');
const audioGanador = new Audio('/ganador.mp3');
// Configura volúmenes (0 a 1)
audioSorteo.volume = 0.5;   // volumen del sonido de sorteo
audioGanador.volume = 0.7;  // volumen del sonido del ganador
audioSorteo.loop = true;
const yaGanadorSeleccionado = ref(false); // ⛔ Evita que se reinicie audio y animación


const names = ref([]);
const positions = ref([]);
const eliminatedIndices = ref([]);
const safeIndices = ref([]);
const nombresAEliminar = ref([]);
const huracanActive = ref(false);
const huracanDirection = ref('derecha');
const winnerIndex = ref(null);
const forcedWinnerIndex = ref(null);

const movimientosErraticos = [
  { x: 200, duration: 0.8 },
  { x: -150, duration: 0.8 },
  { x: 300, duration: 1 }
];
const porcentajesEliminacion = [0.3, 0.4, 0.5];

// 👇 computed para evitar el error de "index"
const nombresConPosicion = computed(() => {
  return names.value
    .map((name, index) => ({ name, index }))
    .filter(({ index }) => positions.value[index]);
});

function seleccionarNombresAEliminar() {
  const forzarGanador = forcedWinnerIndex.value !== null;
  const indicesElegibles = forzarGanador
    ? safeIndices.value.filter((idx) => idx !== forcedWinnerIndex.value)
    : [...safeIndices.value];
  if (!indicesElegibles.length) {
    nombresAEliminar.value = [];
    return;
  }

  const porcentaje = porcentajesEliminacion[Math.floor(Math.random() * porcentajesEliminacion.length)];
  let totalEliminar = Math.max(1, Math.floor(safeIndices.value.length * porcentaje));
  const minSobrevivientes = forzarGanador ? 1 : 1;
  const maxEliminablesPorSobrevivencia = Math.max(0, safeIndices.value.length - minSobrevivientes);
  totalEliminar = Math.min(totalEliminar, maxEliminablesPorSobrevivencia, indicesElegibles.length);
  if (totalEliminar <= 0) {
    nombresAEliminar.value = [];
    return;
  }

  const indices = [...indicesElegibles];
  nombresAEliminar.value = [];
  for (let i = 0; i < totalEliminar; i++) {
    const idx = indices.splice(Math.floor(Math.random() * indices.length), 1)[0];
    nombresAEliminar.value.push(idx);
  }
}

function eliminarNombre(idx) {
  eliminatedIndices.value.push(idx);
  const selector = `.name:nth-child(${idx + 1})`;
  const element = document.querySelector(selector);
  if (!element) return;

  element.classList.remove('temblor');
  const probabilidadEspecial = Math.random() < 0.1;

  if (probabilidadEspecial) {
    element.style.zIndex = 999;
    gsap.to(selector, {
      scale: 4,
      rotation: (Math.random() - 0.5) * 60,
      opacity: 0,
      duration: 1.4,
      ease: 'power4.in',
      transformOrigin: 'center center',
      onComplete: () => { element.style.display = 'none'; }
    });
  } else {
    gsap.to(selector, {
      x: `+=${Math.random() * 400 - 200}`,
      y: `-=300`,
      rotation: 2160,
      opacity: 0,
      duration: 2.5,
      ease: 'back.in',
      onComplete: () => { element.style.display = 'none'; }
    });
  }
}

function checkHuracanEliminacion() {
  const huracanElement = document.querySelector('.huracan');
  if (!huracanElement) return;

  const huracanRect = huracanElement.getBoundingClientRect();
  const huracanCenterX = huracanRect.left + huracanRect.width / 2;
  const huracanCenterY = huracanRect.top + huracanRect.height / 2;
  const huracanRadius = huracanRect.width / 2;

  safeIndices.value.forEach(index => {
    const selector = `.name:nth-child(${index + 1})`;
    const element = document.querySelector(selector);
    if (!element) return;

    const rect = element.getBoundingClientRect();
    const nameCenterX = rect.left + rect.width / 2;
    const nameCenterY = rect.top + rect.height / 2;
    const nameRadius = Math.max(rect.width, rect.height) / 2;

    const dx = huracanCenterX - nameCenterX;
    const dy = huracanCenterY - nameCenterY;
    const distance = Math.sqrt(dx * dx + dy * dy);

    if (distance < huracanRadius + nameRadius && nombresAEliminar.value.includes(index) && !eliminatedIndices.value.includes(index)) {
      eliminarNombre(index);
      safeIndices.value = safeIndices.value.filter(j => j !== index);
    }

    const temblorDistancia = huracanRadius + nameRadius + 100;
    if (distance < temblorDistancia) element.classList.add('temblor');
    else element.classList.remove('temblor');
  });

  if (safeIndices.value.length === 1 && winnerIndex.value === null) {
        // ⏹️ Detener sorteo.mp3
    if (!audioSorteo.paused) {
        audioSorteo.pause();
        audioSorteo.currentTime = 0;
    }

    // ▶️ Iniciar ganador.mp3
    audioGanador.play().catch(() => {
        console.warn('No se pudo reproducir la música del ganador automáticamente.');
    });

    winnerIndex.value = forcedWinnerIndex.value !== null ? forcedWinnerIndex.value : safeIndices.value[0];
      // ✅ Marcar que ya se eligió ganador para evitar reinicios
    yaGanadorSeleccionado.value = true;
    despedirHuracanYMostrarGanador(winnerIndex.value);
  }
}

function startHuracanRecorrido() {
  if (yaGanadorSeleccionado.value) return; // Detener cualquier ejecución futura
  if (safeIndices.value.length === 1) {
    winnerIndex.value = forcedWinnerIndex.value !== null ? forcedWinnerIndex.value : safeIndices.value[0];
    yaGanadorSeleccionado.value = true;
    despedirHuracanYMostrarGanador(winnerIndex.value);
    return;
  }

    // ▶️ Iniciar música de sorteo
  if (audioSorteo.paused) {
    audioSorteo.play().catch(() => {
      console.warn('El navegador bloqueó la reproducción automática del audio.');
    });
  }

  seleccionarNombresAEliminar();
  huracanActive.value = true;

  const inicioX = huracanDirection.value === 'derecha' ? window.innerWidth + 300 : -800;
  const finalX = huracanDirection.value === 'derecha' ? -800 : window.innerWidth + 300;

  gsap.set('.huracan', { x: inicioX, opacity: 1 });

  const saltos = [];
  const numSaltos = Math.floor(Math.random() * 3) + 1;
  let actualX = inicioX;
  for (let i = 0; i < numSaltos; i++) {
    const movimiento = movimientosErraticos[Math.floor(Math.random() * movimientosErraticos.length)];
    actualX += movimiento.x;
    saltos.push({ x: actualX, duration: movimiento.duration });
  }
  saltos.push({ x: finalX, duration: 2 });

  const tl = gsap.timeline({
    onUpdate: checkHuracanEliminacion,
    onComplete: () => {
      huracanDirection.value = huracanDirection.value === 'derecha' ? 'izquierda' : 'derecha';
      setTimeout(startHuracanRecorrido, 1200);
    }
  });

  saltos.forEach(salto => {
    tl.to('.huracan', { x: salto.x, duration: salto.duration, ease: 'power1.inOut' });
  });
}

function despedirHuracanYMostrarGanador(index) {
  if (index === null || index < 0 || index >= names.value.length) {
    console.warn('[AnimacionSorteo] Índice de ganador inválido. Se usará fallback seguro.');
    const fallback = safeIndices.value[0];
    if (fallback === undefined) {
      emit('finalizado', props.forcedWinner || '');
      return;
    }
    winnerIndex.value = fallback;
    index = fallback;
  }

  gsap.to('.huracan', {
    opacity: 0,
    duration: 1,
    onComplete: () => {
      animateGanador(index);
    }
  });

  setTimeout(() => {
    const ganador = forcedWinnerIndex.value !== null
      ? props.forcedWinner
      : names.value[index];
    emit('finalizado', ganador || '');
  }, 4000);
}

function animateGanador(index) {
  const selector = `.name:nth-child(${index + 1})`;
  const element = document.querySelector(selector);
  if (!element) return;

  const currentX = gsap.getProperty(element, 'x') || 0;
  const currentY = gsap.getProperty(element, 'y') || 0;
  const rect = element.getBoundingClientRect();
  const centerX = window.innerWidth / 2 - rect.width / 2;
  const centerY = window.innerHeight / 2 - rect.height / 2;

  gsap.to(element, {
    x: centerX - rect.left + currentX,
    y: centerY - rect.top + currentY,
    scale: 3,
    duration: 3,
    ease: 'power4.out',
    color: 'transparent',
    '-webkit-text-stroke': '3px yellow',
    textShadow: '0 0 20px yellow, 0 0 40px yellow',
    opacity: 1,
    onComplete: () => {
      document.querySelectorAll('.name').forEach((el, idx) => {
        if (idx !== index) el.style.display = 'none';
      });
    }
  });
}

function createRaindrops(count) {
  for (let i = 0; i < count; i++) {
    const drop = document.createElement('div');
    drop.className = 'raindrop';
    drop.style.left = `${Math.random() * window.innerWidth}px`;
    drop.style.animationDelay = `${Math.random()}s`;
    document.querySelector('.overlay').appendChild(drop);
  }
}

// Lógica para iniciar animación al recibir nombres
watch(() => props.participantes, async (val) => {
  if (val.length && !names.value.length) {
    names.value = [...val];
    if (props.forcedWinner) {
      const index = names.value.findIndex((name) => name === props.forcedWinner);
      if (index === -1) {
        console.warn('[AnimacionSorteo] forcedWinner no se encontró en la lista de participantes.', props.forcedWinner);
        forcedWinnerIndex.value = null;
      } else {
        forcedWinnerIndex.value = index;
      }
    } else {
      forcedWinnerIndex.value = null;
    }
    const total = names.value.length;

    positions.value = names.value.map((_, i) => {
      const franja = i % 3;
      let y = 150, scale = 1;
      if (franja === 0) { y = 200; scale = 0.8; }
      else if (franja === 2) { y = 100; scale = 1.2; }
      return { x: (window.innerWidth / (total + 1)) * (i + 1), y, scale };
    });

    safeIndices.value = names.value.map((_, i) => i);
    await nextTick();
    startHuracanRecorrido();
  }
});

onMounted(() => {
  createRaindrops(150);
});
</script>

<style scoped>
/* Usa rutas desde /public */
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  color: white;
}

.fondo {
  position: absolute;
  top: 0; left: 0;
  width: 100%;
  height: 100%;
  background: url('/fondo.png') no-repeat center center;
  background-size: cover;
  z-index: -1;
}

.clouds {
  position: absolute;
  top: 0;
  left: 0;
  width: 1000%;
  height: 40%;
  background-size: auto 100%;
  background-repeat: repeat-x;
  animation: moveClouds 120s linear infinite;
}

.clouds-largas {
  background-image: url('/nube_larga.png');
  z-index: 1;
  opacity: 0.7;
  animation-duration: 90s;
}

.clouds-cortas {
  background-image: url('/nube_corta.png');
  z-index: 2;
  opacity: 0.9;
  animation-duration: 120s;
}

@keyframes moveClouds {
  from { transform: translateX(0); }
  to { transform: translateX(-50%); }
}

.ground {
  position: absolute;
  width: 100%;
  height: 200px;
  bottom: 0;
}

.name {
  position: absolute;
  font-family: 'Bangers', cursive;
  font-size: 3em;
  color: white;
  -webkit-text-stroke: 1px black;
  text-shadow: 1px 1px 2px black;
  transition: opacity 0.5s, transform 0.5s;
  z-index: 2;
}

.gone {
  opacity: 0;
  transform: translateY(-200px) rotate(720deg);
}

.huracan {
  position: absolute;
  width: 800px;
  height: 800px;
  background: url('/tornado2.gif') no-repeat center center;
  background-size: contain;
  left: -300px;
  top: calc(100% - 400px);
  transform: translateY(-50%);
  z-index: 3;
}

.temblor {
  animation: temblar 0.2s infinite alternate;
}

@keyframes temblar {
  0% { transform: translate(0, 0) rotate(0deg); }
  100% { transform: translate(2px, -2px) rotate(1deg); }
}

.raindrop {
  position: absolute;
  width: 2px;
  height: 10px;
  background: #00f;
  opacity: 0.5;
  animation: rain 1s linear infinite;
}

@keyframes rain {
  0% { transform: translateY(-10px); }
  100% { transform: translateY(100vh); }
}
</style>

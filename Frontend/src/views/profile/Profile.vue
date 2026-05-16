<template>
  <div class="container-fluid py-4">
    <div
      class="page-header min-height-300 border-radius-xl mt-4"
      style="
        background-image: url('https://images.unsplash.com/photo-1531512073830-ba890ca4eba2?auto=format&fit=crop&w=1920&q=80');
      "
    >
      <span class="mask bg-gradient-success opacity-6"></span>
    </div>

    <div class="card card-body mx-3 mx-md-4 mt-n6">
      <div v-if="loading" class="py-5 text-center text-muted">Cargando perfil...</div>

      <template v-else-if="currentUser">
        <div class="row gx-4 align-items-start">
          <div class="col-12 col-lg d-flex align-items-center mb-3 mb-lg-0">
            <div class="col-auto">
              <div class="avatar avatar-xl position-relative bg-gradient-dark text-white d-flex align-items-center justify-content-center">
                <span class="fw-bold fs-5">{{ initials }}</span>
              </div>
            </div>
            <div class="col-auto my-auto ms-3">
              <div class="h-100">
                <h5 class="mb-1">{{ currentUser.display_name || 'Usuario Pixel Gift' }}</h5>
                <p class="mb-0 font-weight-normal text-sm">{{ currentUser.email || 'Correo no disponible' }}</p>
                <p class="mb-0 text-xs text-muted" v-if="formattedCreatedAt">Cuenta creada: {{ formattedCreatedAt }}</p>
              </div>
            </div>
          </div>

          <div class="col-12 col-lg-auto ms-lg-auto">
            <div class="nav-wrapper position-relative end-0">
              <ul ref="tabsContainerRef" class="nav nav-pills nav-fill p-1 bg-transparent profile-tabs" role="tablist">
                <div class="moving-tab position-absolute nav-link" :style="movingTabStyle" aria-hidden="true">
                  <span>-</span>
                </div>
                <li class="nav-item" ref="tabItemRefs">
                  <button class="px-0 py-1 mb-0 nav-link d-flex align-items-center justify-content-center gap-1" :class="tabClass('app')" @click="setActiveTab('app')" type="button">
                    <svg :class="iconClass('app')" width="16px" height="16px" viewBox="0 0 42 42" version="1.1" xmlns="http://www.w3.org/2000/svg">
                      <g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                        <g transform="translate(-2319.000000, -291.000000)" fill="#FFFFFF" fill-rule="nonzero">
                          <g transform="translate(1716.000000, 291.000000)">
                            <g transform="translate(603.000000, 0.000000)">
                              <path class="color-background" d="M22.7597136,19.3090182 L38.8987031,11.2395234 C39.3926816,10.9925342 39.592906,10.3918611 39.3459167,9.89788265 C39.249157,9.70436312 39.0922432,9.5474453 38.8987261,9.45068056 L20.2741875,0.1378125 L20.2741875,0.1378125 C19.905375,-0.04725 19.469625,-0.04725 19.0995,0.1378125 L3.1011696,8.13815822 C2.60720568,8.38517662 2.40701679,8.98586148 2.6540352,9.4798254 C2.75080129,9.67332903 2.90771305,9.83023153 3.10122239,9.9269862 L21.8652864,19.3090182 C22.1468139,19.4497819 22.4781861,19.4497819 22.7597136,19.3090182 Z" />
                              <path class="color-background" d="M23.625,22.429159 L23.625,39.8805372 C23.625,40.4328219 24.0727153,40.8805372 24.625,40.8805372 C24.7802551,40.8805372 24.9333778,40.8443874 25.0722402,40.7749511 L41.2741875,32.673375 L41.2741875,32.673375 C41.719125,32.4515625 42,31.9974375 42,31.5 L42,14.241659 C42,13.6893742 41.5522847,13.241659 41,13.241659 C40.8447549,13.241659 40.6916418,13.2778041 40.5527864,13.3472318 L24.1777864,21.5347318 C23.8390024,21.7041238 23.625,22.0503869 23.625,22.429159 Z" opacity="0.7" />
                              <path class="color-background" d="M20.4472136,21.5347318 L1.4472136,12.0347318 C0.953235098,11.7877425 0.352562058,11.9879669 0.105572809,12.4819454 C0.0361450918,12.6208008 6.47121774e-16,12.7739139 0,12.929159 L0,30.1875 L0,30.1875 C0,30.6849375 0.280875,31.1390625 0.7258125,31.3621875 L19.5528096,40.7750766 C20.0467945,41.0220531 20.6474623,40.8218132 20.8944388,40.3278283 C20.963859,40.1889789 21,40.0358742 21,39.8806379 L21,22.429159 C21,22.0503869 20.7859976,21.7041238 20.4472136,21.5347318 Z" opacity="0.7" />
                            </g>
                          </g>
                        </g>
                      </g>
                    </svg>
                    <span class="ms-1">App</span>
                  </button>
                </li>
                <li class="nav-item" ref="tabItemRefs">
                  <button class="px-0 py-1 mb-0 nav-link d-flex align-items-center justify-content-center gap-1" :class="tabClass('messages')" @click="setActiveTab('messages')" type="button">
                    <svg :class="iconClass('messages')" width="16px" height="16px" viewBox="0 0 40 44" version="1.1" xmlns="http://www.w3.org/2000/svg">
                      <g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                        <g transform="translate(-1870.000000, -591.000000)" fill="#FFFFFF" fill-rule="nonzero">
                          <g transform="translate(1716.000000, 291.000000)">
                            <g transform="translate(154.000000, 300.000000)">
                              <path class="color-background" d="M40,40 L36.3636364,40 L36.3636364,3.63636364 L5.45454545,3.63636364 L5.45454545,0 L38.1818182,0 C39.1854545,0 40,0.814545455 40,1.81818182 L40,40 Z" opacity="0.603585379" />
                              <path class="color-background" d="M30.9090909,7.27272727 L1.81818182,7.27272727 C0.814545455,7.27272727 0,8.08727273 0,9.09090909 L0,41.8181818 C0,42.8218182 0.814545455,43.6363636 1.81818182,43.6363636 L30.9090909,43.6363636 C31.9127273,43.6363636 32.7272727,42.8218182 32.7272727,41.8181818 L32.7272727,9.09090909 C32.7272727,8.08727273 31.9127273,7.27272727 30.9090909,7.27272727 Z M18.1818182,34.5454545 L7.27272727,34.5454545 L7.27272727,30.9090909 L18.1818182,30.9090909 L18.1818182,34.5454545 Z M25.4545455,27.2727273 L7.27272727,27.2727273 L7.27272727,23.6363636 L25.4545455,23.6363636 L25.4545455,27.2727273 Z M25.4545455,20 L7.27272727,20 L7.27272727,16.3636364 L25.4545455,16.3636364 L25.4545455,20 Z" />
                            </g>
                          </g>
                        </g>
                      </g>
                    </svg>
                    Messages
                  </button>
                </li>
                <li class="nav-item" ref="tabItemRefs">
                  <button class="px-0 py-1 mb-0 nav-link d-flex align-items-center justify-content-center gap-1" :class="tabClass('settings')" @click="setActiveTab('settings')" type="button">
                    <svg :class="iconClass('settings')" width="16px" height="16px" viewBox="0 0 40 40" version="1.1" xmlns="http://www.w3.org/2000/svg">
                      <g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                        <g transform="translate(-2020.000000, -442.000000)" fill="#FFFFFF" fill-rule="nonzero">
                          <g transform="translate(1716.000000, 291.000000)">
                            <g transform="translate(304.000000, 151.000000)">
                              <polygon class="color-background" opacity="0.596981957" points="18.0883333 15.7316667 11.1783333 8.82166667 13.3333333 6.66666667 6.66666667 0 0 6.66666667 6.66666667 13.3333333 8.82166667 11.1783333 15.315 17.6716667" />
                              <path class="color-background" d="M31.5666667,23.2333333 C31.0516667,23.2933333 30.53,23.3333333 30,23.3333333 C29.4916667,23.3333333 28.9866667,23.3033333 28.48,23.245 L22.4116667,30.7433333 L29.9416667,38.2733333 C32.2433333,40.575 35.9733333,40.575 38.275,38.2733333 L38.275,38.2733333 C40.5766667,35.9716667 40.5766667,32.2416667 38.275,29.94 L31.5666667,23.2333333 Z" opacity="0.596981957" />
                              <path class="color-background" d="M33.785,11.285 L28.715,6.215 L34.0616667,0.868333333 C32.82,0.315 31.4483333,0 30,0 C24.4766667,0 20,4.47666667 20,10 C20,10.99 20.1483333,11.9433333 20.4166667,12.8466667 L2.435,27.3966667 C0.95,28.7083333 0.0633333333,30.595 0.00333333333,32.5733333 C-0.0583333333,34.5533333 0.71,36.4916667 2.11,37.89 C3.47,39.2516667 5.27833333,40 7.20166667,40 C9.26666667,40 11.2366667,39.1133333 12.6033333,37.565 L27.1533333,19.5833333 C28.0566667,19.8516667 29.01,20 30,20 C35.5233333,20 40,15.5233333 40,10 C40,8.55166667 39.685,7.18 39.1316667,5.93666667 L33.785,11.285 Z" />
                            </g>
                          </g>
                        </g>
                      </g>
                    </svg>
                    Settings
                  </button>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <Transition name="profile-tab" mode="out-in">
          <div :key="activeTab" class="tab-content mt-4">
            <div v-if="activeTab === 'app'" class="row">
              <div class="col-12 col-xl-6">
                <div class="card card-plain h-100">
                  <div class="p-3 pb-0 card-header">
                    <h6 class="mb-0">Información de cuenta</h6>
                  </div>
                  <div class="p-3 card-body">
                    <ul class="list-group">
                      <li class="text-sm border-0 list-group-item ps-0">
                        <strong class="text-dark">ID de usuario:</strong> &nbsp; {{ currentUser.id || '-' }}
                      </li>
                      <li class="text-sm border-0 list-group-item ps-0">
                        <strong class="text-dark">Nombre visible:</strong> &nbsp; {{ currentUser.display_name || '-' }}
                      </li>
                      <li class="text-sm border-0 list-group-item ps-0">
                        <strong class="text-dark">Correo:</strong> &nbsp; {{ currentUser.email || '-' }}
                      </li>
                      <li class="text-sm border-0 list-group-item ps-0">
                        <strong class="text-dark">Fecha de creación:</strong> &nbsp; {{ formattedCreatedAt || '-' }}
                      </li>
                    </ul>
                  </div>
                </div>
              </div>

              <div class="col-12 col-xl-6 mt-4 mt-xl-0">
                <div class="card card-plain h-100">
                  <div class="p-3 pb-0 card-header">
                    <h6 class="mb-0">Conexiones</h6>
                  </div>
                  <div class="p-3 card-body">
                    <ul class="list-group">
                      <li class="text-sm border-0 list-group-item ps-0 d-flex justify-content-between">
                        <span><strong class="text-dark">Twitch</strong></span>
                        <span class="badge bg-gradient-warning">Pendiente de integración</span>
                      </li>
                      <li class="text-sm border-0 list-group-item ps-0 d-flex justify-content-between">
                        <span><strong class="text-dark">Redes sociales</strong></span>
                        <span class="badge bg-gradient-secondary">Próximamente</span>
                      </li>
                      <li class="text-sm border-0 list-group-item ps-0 d-flex justify-content-between">
                        <span><strong class="text-dark">Kick / YouTube</strong></span>
                        <span class="badge bg-gradient-secondary">Próximamente</span>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>

            <div v-else-if="activeTab === 'messages'" class="row g-4">
              <div class="col-12 col-xl-6">
                <div class="card h-100">
                  <div class="card-header pb-0 p-3">
                    <h6 class="mb-1">Vincular plataformas</h6>
                    <p class="text-sm mb-0">Conecta tu cuenta para publicar y sincronizar actividad.</p>
                  </div>
                  <div class="card-body p-3">
                    <div v-for="platform in platformConnections" :key="platform.key" class="connection-item d-flex align-items-center justify-content-between mb-3">
                      <div>
                        <p class="mb-0 fw-bold text-dark">{{ platform.label }}</p>
                        <p class="text-xs text-muted mb-0">{{ platform.description }}</p>
                      </div>
                      <button
                        class="btn btn-sm mb-0"
                        :class="platform.connected ? 'btn-outline-danger' : 'btn-outline-success'"
                        :disabled="platform.pending"
                        @click="handleToggleConnection('platform', platform.key)"
                      >
                        {{ platform.pending ? 'Procesando...' : platform.connected ? 'Desvincular' : 'Vincular' }}
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <div class="col-12 col-xl-6">
                <div class="card h-100">
                  <div class="card-header pb-0 p-3">
                    <h6 class="mb-1">Redes sociales</h6>
                    <p class="text-sm mb-0">Gestiona perfiles para branding y comunicación.</p>
                  </div>
                  <div class="card-body p-3">
                    <div v-for="social in socialConnections" :key="social.key" class="connection-item d-flex align-items-center justify-content-between mb-3">
                      <div>
                        <p class="mb-0 fw-bold text-dark">{{ social.label }}</p>
                        <p class="text-xs text-muted mb-0">{{ social.description }}</p>
                      </div>
                      <button
                        class="btn btn-sm mb-0"
                        :class="social.connected ? 'btn-outline-danger' : 'btn-outline-success'"
                        :disabled="social.pending"
                        @click="handleToggleConnection('social', social.key)"
                      >
                        {{ social.pending ? 'Procesando...' : social.connected ? 'Desvincular' : 'Vincular' }}
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div v-else class="row g-4">
              <div class="col-12 col-xl-6">
                <div class="card h-100">
                  <div class="card-header pb-0 p-3">
                    <h6 class="mb-1">Ajustes de cuenta</h6>
                    <p class="text-sm mb-0">Actualiza tu perfil y seguridad.</p>
                  </div>
                  <div class="card-body p-3">
                    <div class="mb-3">
                      <label class="form-label">Nickname / display_name</label>
                      <input v-model="editableProfile.display_name" type="text" class="form-control" placeholder="Nuevo nombre visible" />
                    </div>
                    <button class="btn bg-gradient-success btn-sm" @click="handleUpdateDisplayName">Guardar nickname</button>

                    <hr class="horizontal dark my-4" />

                    <div class="mb-3">
                      <label class="form-label">Nueva contraseña</label>
                      <input v-model="editableProfile.password" type="password" class="form-control" placeholder="••••••••" />
                    </div>
                    <button class="btn btn-outline-dark btn-sm" @click="handlePasswordChange">Cambiar contraseña</button>
                  </div>
                </div>
              </div>

              <div class="col-12 col-xl-6">
                <div class="card h-100">
                  <div class="card-header pb-0 p-3">
                    <h6 class="mb-1">Suscripciones y preferencias</h6>
                    <p class="text-sm mb-0">Bloques listos para conectar con backend más adelante.</p>
                  </div>
                  <div class="card-body p-3">
                    <ul class="list-group">
                      <li class="list-group-item border-0 px-0 d-flex justify-content-between">
                        <span class="text-sm">Suscripción de pago</span>
                        <span class="badge bg-gradient-secondary">Placeholder</span>
                      </li>
                      <li class="list-group-item border-0 px-0 d-flex justify-content-between">
                        <span class="text-sm">Notificaciones por correo</span>
                        <span class="badge bg-gradient-info">Próximo paso</span>
                      </li>
                      <li class="list-group-item border-0 px-0 d-flex justify-content-between">
                        <span class="text-sm">Privacidad de perfil</span>
                        <span class="badge bg-gradient-info">Próximo paso</span>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </Transition>
      </template>
    </div>
  </div>
</template>

<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, reactive, ref, watch } from 'vue';
import { useAuthStore } from '@/stores/authStore';

const authStore = useAuthStore();
const loading = ref(true);
const activeTab = ref('app');
const isDarkMode = ref(false);
const tabsContainerRef = ref(null);
const tabItemRefs = ref([]);
const movingTabStyle = ref({
  width: '0px',
  transform: 'translate3d(0px, 0px, 0px)'
});
let themeObserver = null;

const currentUser = computed(() => authStore.user);

const editableProfile = reactive({
  display_name: '',
  password: ''
});

const platformConnections = ref([
  { key: 'twitch', label: 'Twitch', description: 'Streaming y eventos en vivo.', connected: false, pending: false },
  { key: 'discord', label: 'Discord', description: 'Comunidad y notificaciones.', connected: false, pending: false },
  { key: 'youtube', label: 'YouTube', description: 'Contenido de video.', connected: false, pending: false }
]);

const socialConnections = ref([
  { key: 'instagram', label: 'Instagram', description: 'Contenido corto y branding visual.', connected: false, pending: false },
  { key: 'facebook', label: 'Facebook', description: 'Página y anuncios.', connected: false, pending: false },
  { key: 'x', label: 'X / Twitter', description: 'Noticias rápidas y comunidad.', connected: false, pending: false }
]);

const initials = computed(() => {
  const name = currentUser.value?.display_name?.trim();
  if (!name) return 'PG';
  const parts = name.split(/\s+/).slice(0, 2);
  return parts.map((p) => p[0]?.toUpperCase() || '').join('') || 'PG';
});

const formattedCreatedAt = computed(() => {
  const value = currentUser.value?.created_at;
  if (!value) return '';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return new Intl.DateTimeFormat('es-ES', { dateStyle: 'medium' }).format(date);
});

const setActiveTab = (tab) => {
  activeTab.value = tab;
};

const tabClass = (tab) => ({
  active: activeTab.value === tab,
  'text-white': activeTab.value === tab,
  'tab-label-dark': activeTab.value !== tab && !isDarkMode.value,
  'tab-label-light': activeTab.value !== tab && isDarkMode.value
});

const iconClass = (tab) => {
  if (activeTab.value === tab) return 'text-white';
  return isDarkMode.value ? 'text-white' : 'text-dark';
};

const syncTheme = () => {
  isDarkMode.value = document.body.classList.contains('dark-version');
};

const updateMovingTab = async () => {
  await nextTick();
  const index = ['app', 'messages', 'settings'].indexOf(activeTab.value);
  const currentItem = tabItemRefs.value?.[index];
  if (!currentItem) return;
  const offset = currentItem.offsetLeft;
  const width = currentItem.offsetWidth;
  movingTabStyle.value = {
    width: `${width}px`,
    transform: `translate3d(${offset}px, 0px, 0px)`
  };
};

const handleToggleConnection = (type, key) => {
  const list = type === 'platform' ? platformConnections.value : socialConnections.value;
  const item = list.find((entry) => entry.key === key);
  if (!item) return;

  item.pending = true;

  // TODO: Reemplazar por llamada real al backend (ej: /api/profile/connections/toggle)
  setTimeout(() => {
    item.connected = !item.connected;
    item.pending = false;
  }, 500);
};

const handleUpdateDisplayName = () => {
  // TODO: Integrar endpoint backend para actualizar display_name
  console.log('Actualizar display_name', editableProfile.display_name);
};

const handlePasswordChange = () => {
  // TODO: Integrar endpoint backend para cambio de contraseña
  console.log('Cambiar contraseña', editableProfile.password);
};

watch(
  () => currentUser.value,
  (user) => {
    editableProfile.display_name = user?.display_name || '';
  },
  { immediate: true }
);

watch(activeTab, () => {
  updateMovingTab();
});

onMounted(async () => {
  syncTheme();
  themeObserver = new MutationObserver(syncTheme);
  themeObserver.observe(document.body, { attributes: true, attributeFilter: ['class'] });
  window.addEventListener('resize', updateMovingTab);

  if (!authStore.user) {
    await authStore.checkSession();
  }
  loading.value = false;
  updateMovingTab();
});

onBeforeUnmount(() => {
  themeObserver?.disconnect();
  window.removeEventListener('resize', updateMovingTab);
});
</script>

<style scoped>
.profile-tabs {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 0.75rem;
  min-width: 280px;
}

.profile-tabs .nav-item {
  z-index: 2;
}

.profile-tabs .nav-link {
  transition: color 0.2s ease;
}

.moving-tab {
  z-index: 1;
  top: 4px;
  left: 0;
  height: calc(100% - 8px);
  border-radius: 0.5rem;
  background: linear-gradient(195deg, #66bb6a, #43a047);
  transition: transform 0.35s ease, width 0.35s ease;
  pointer-events: none;
}

.moving-tab span {
  visibility: hidden;
}

.tab-label-dark {
  color: #344767 !important;
}

.tab-label-light {
  color: rgba(255, 255, 255, 0.85) !important;
}

.connection-item {
  border: 1px solid #e9ecef;
  border-radius: 0.75rem;
  padding: 0.75rem;
  transition: all 0.2s ease;
}

.connection-item:hover {
  border-color: #82d616;
  box-shadow: 0 0.25rem 0.75rem rgba(0, 0, 0, 0.06);
}

.profile-tab-enter-active,
.profile-tab-leave-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}

.profile-tab-enter-from,
.profile-tab-leave-to {
  opacity: 0;
  transform: translateY(12px);
}
</style>

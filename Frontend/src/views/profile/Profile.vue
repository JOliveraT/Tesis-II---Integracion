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
              <ul ref="tabsWrapperRef" class="nav nav-pills nav-fill profile-tabs p-1" role="tablist">
                <div class="moving-tab" :style="movingTabStyle" aria-hidden="true"></div>
                <li class="nav-item">
                  <button :ref="(el) => setTabButtonRef('app', el)" class="nav-link mb-0 px-3 py-2 profile-tab-link" :class="{ active: activeTab === 'app' }" @click="setActiveTab('app')" type="button">
                    <span class="tab-icon" aria-hidden="true">
                      <svg width="16" height="16" viewBox="0 0 42 42" xmlns="http://www.w3.org/2000/svg">
                        <path class="color-background" d="M22.7597 19.309 38.8987 11.2395C39.3927 10.9925 39.5929 10.3919 39.3459 9.89788C39.2492 9.70436 39.0922 9.54745 38.8987 9.45068L20.2742 0.137813C19.9054 -0.04725 19.4696 -0.04725 19.0995 0.137813L3.10117 8.13816C2.60721 8.38518 2.40702 8.98586 2.65404 9.47983C2.7508 9.67333 2.90771 9.83023 3.10122 9.92699L21.8653 19.309C22.1468 19.4498 22.4782 19.4498 22.7597 19.309Z" />
                        <path class="color-background" d="M23.625 22.4292V39.8805C23.625 40.4328 24.0727 40.8805 24.625 40.8805C24.7803 40.8805 24.9334 40.8444 25.0722 40.775L41.2742 32.6734C41.7191 32.4516 42 31.9974 42 31.5V14.2417C42 13.6894 41.5523 13.2417 41 13.2417C40.8448 13.2417 40.6916 13.2778 40.5528 13.3472L24.1778 21.5347C23.839 21.7041 23.625 22.0504 23.625 22.4292Z" opacity=".7" />
                        <path class="color-background" d="M20.4472 21.5347L1.44721 12.0347C0.953235 11.7877 0.352562 11.988 0.105573 12.4819C0.0361451 12.6208 0 12.7739 0 12.9292V30.1875C0 30.6849 0.280875 31.1391 0.725813 31.3622L19.5528 40.7751C20.0468 41.0221 20.6475 40.8218 20.8944 40.3278C20.9639 40.189 21 40.0359 21 39.8806V22.4292C21 22.0504 20.786 21.7041 20.4472 21.5347Z" opacity=".7" />
                      </svg>
                    </span>
                    <span>App</span>
                  </button>
                </li>
                <li class="nav-item">
                  <button :ref="(el) => setTabButtonRef('messages', el)" class="nav-link mb-0 px-3 py-2 profile-tab-link" :class="{ active: activeTab === 'messages' }" @click="setActiveTab('messages')" type="button">
                    <span class="tab-icon" aria-hidden="true">
                      <svg width="16" height="16" viewBox="0 0 40 44" xmlns="http://www.w3.org/2000/svg">
                        <path class="color-background" d="M40 40H36.3636V3.63636H5.45455V0H38.1818C39.1855 0 40 0.814545 40 1.81818V40Z" opacity=".6" />
                        <path class="color-background" d="M30.9091 7.27273H1.81818C0.814545 7.27273 0 8.08727 0 9.09091V41.8182C0 42.8218 0.814545 43.6364 1.81818 43.6364H30.9091C31.9127 43.6364 32.7273 42.8218 32.7273 41.8182V9.09091C32.7273 8.08727 31.9127 7.27273 30.9091 7.27273ZM18.1818 34.5455H7.27273V30.9091H18.1818V34.5455ZM25.4545 27.2727H7.27273V23.6364H25.4545V27.2727ZM25.4545 20H7.27273V16.3636H25.4545V20Z" />
                      </svg>
                    </span>
                    <span>Messages</span>
                  </button>
                </li>
                <li class="nav-item">
                  <button :ref="(el) => setTabButtonRef('settings', el)" class="nav-link mb-0 px-3 py-2 profile-tab-link" :class="{ active: activeTab === 'settings' }" @click="setActiveTab('settings')" type="button">
                    <span class="tab-icon" aria-hidden="true">
                      <svg width="16" height="16" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
                        <path class="color-background" d="M18.0883 15.7317L11.1783 8.82167L13.3333 6.66667L6.66667 0L0 6.66667L6.66667 13.3333L8.82167 11.1783L15.315 17.6717Z" opacity=".6" />
                        <path class="color-background" d="M31.5667 23.2333C31.0517 23.2933 30.53 23.3333 30 23.3333C29.4917 23.3333 28.9867 23.3033 28.48 23.245L22.4117 30.7433L29.9417 38.2733C32.2433 40.575 35.9733 40.575 38.275 38.2733C40.5767 35.9717 40.5767 32.2417 38.275 29.94L31.5667 23.2333Z" opacity=".6" />
                        <path class="color-background" d="M33.785 11.285L28.715 6.215L34.0617 0.868333C32.82 0.315 31.4483 0 30 0C24.4767 0 20 4.47667 20 10C20 10.99 20.1483 11.9433 20.4167 12.8467L2.435 27.3967C0.95 28.7083 0.0633333 30.595 0.00333333 32.5733C-0.0583333 34.5533 0.71 36.4917 2.11 37.89C3.47 39.2517 5.27833 40 7.20167 40C9.26667 40 11.2367 39.1133 12.6033 37.565L27.1533 19.5833C28.0567 19.8517 29.01 20 30 20C35.5233 20 40 15.5233 40 10C40 8.55167 39.685 7.18 39.1317 5.93667L33.785 11.285Z" />
                      </svg>
                    </span>
                    <span>Settings</span>
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
const tabsWrapperRef = ref(null);
const tabButtonRefs = ref({});
const movingTabStyle = ref({ transform: 'translate3d(0px, 0, 0)', width: '0px', opacity: 0 });
const isDarkMode = ref(document.body.classList.contains('dark-version'));
let themeObserver;

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

const setTabButtonRef = (tab, el) => {
  if (el) {
    tabButtonRefs.value[tab] = el;
    return;
  }
  delete tabButtonRefs.value[tab];
};

const updateMovingTab = async () => {
  await nextTick();
  const activeButton = tabButtonRefs.value[activeTab.value];
  const wrapper = tabsWrapperRef.value;
  if (!activeButton || !wrapper) return;

  const left = activeButton.offsetLeft;
  const width = activeButton.offsetWidth;

  movingTabStyle.value = {
    transform: `translate3d(${left}px, 0, 0)`,
    width: `${width}px`,
    opacity: 1
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

onMounted(async () => {
  if (!authStore.user) {
    await authStore.checkSession();
  }
  loading.value = false;
  await updateMovingTab();
  themeObserver = new MutationObserver(() => {
    isDarkMode.value = document.body.classList.contains('dark-version');
  });
  themeObserver.observe(document.body, { attributes: true, attributeFilter: ['class'] });
  window.addEventListener('resize', updateMovingTab);
});

onBeforeUnmount(() => {
  window.removeEventListener('resize', updateMovingTab);
  themeObserver?.disconnect();
});

watch(activeTab, () => {
  updateMovingTab();
});

watch(loading, (value) => {
  if (!value) {
    updateMovingTab();
  }
});
</script>

<style scoped>
.profile-tabs {
  background: var(--bs-body-bg, rgba(255, 255, 255, 0.9));
  border-radius: 0.75rem;
  position: relative;
  isolation: isolate;
}

.profile-tabs .nav-item {
  position: relative;
  z-index: 2;
}

.profile-tab-link {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  color: var(--bs-body-color);
  transition: color 0.2s ease;
}

.profile-tab-link .tab-icon {
  display: inline-flex;
  line-height: 0;
}

.profile-tab-link .tab-icon svg {
  width: 1rem;
  height: 1rem;
}

.profile-tab-link .color-background {
  fill: currentColor;
}

.profile-tab-link.active {
  color: #fff;
}

.profile-tab-link:not(.active) {
  color: v-bind('isDarkMode ? "rgba(255, 255, 255, 0.85)" : "#344767"');
}

.moving-tab {
  position: absolute;
  top: 0.25rem;
  left: 0;
  height: calc(100% - 0.5rem);
  border-radius: 0.5rem;
  background: linear-gradient(195deg, #66bb6a, #43a047);
  transition: transform 0.3s ease, width 0.3s ease, opacity 0.2s ease;
  z-index: 1;
  box-shadow: 0 4px 12px rgba(67, 160, 71, 0.35);
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

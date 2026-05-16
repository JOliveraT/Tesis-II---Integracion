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
              <ul class="nav nav-pills nav-fill profile-tabs p-1" role="tablist">
                <li class="nav-item">
                  <button class="nav-link mb-0 px-3 py-2" :class="{ active: activeTab === 'app' }" @click="setActiveTab('app')" type="button">
                    App
                  </button>
                </li>
                <li class="nav-item">
                  <button class="nav-link mb-0 px-3 py-2" :class="{ active: activeTab === 'messages' }" @click="setActiveTab('messages')" type="button">
                    Messages
                  </button>
                </li>
                <li class="nav-item">
                  <button class="nav-link mb-0 px-3 py-2" :class="{ active: activeTab === 'settings' }" @click="setActiveTab('settings')" type="button">
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
import { computed, onMounted, reactive, ref, watch } from 'vue';
import { useAuthStore } from '@/stores/authStore';

const authStore = useAuthStore();
const loading = ref(true);
const activeTab = ref('app');

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
});
</script>

<style scoped>
.profile-tabs {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 0.75rem;
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

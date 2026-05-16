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
        <div class="row gx-4 align-items-center">
          <div class="col-auto">
            <div class="avatar avatar-xl position-relative bg-gradient-dark text-white d-flex align-items-center justify-content-center">
              <span class="fw-bold fs-5">{{ initials }}</span>
            </div>
          </div>
          <div class="col-auto my-auto">
            <div class="h-100">
              <h5 class="mb-1">{{ currentUser.display_name || 'Usuario Pixel Gift' }}</h5>
              <p class="mb-0 font-weight-normal text-sm">{{ currentUser.email || 'Correo no disponible' }}</p>
              <p class="mb-0 text-xs text-muted" v-if="formattedCreatedAt">Cuenta creada: {{ formattedCreatedAt }}</p>
            </div>
          </div>
        </div>

        <div class="row mt-4">
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
      </template>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import { useAuthStore } from '@/stores/authStore';

const authStore = useAuthStore();
const loading = ref(true);

const currentUser = computed(() => authStore.user);

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

onMounted(async () => {
  if (!authStore.user) {
    await authStore.checkSession();
  }
  loading.value = false;
});
</script>

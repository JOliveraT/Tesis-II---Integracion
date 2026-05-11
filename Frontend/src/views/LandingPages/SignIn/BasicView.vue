<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { authService } from '@/services/authService';
import { supabase } from '@/lib/supabase';

// example components
import DefaultNavbar from "@/examples/navbars/NavbarDefault.vue";
import Header from "@/examples/Header.vue";

//Vue Material Kit 2 components
import MaterialInput from "@/components/MaterialInput.vue";
import MaterialSwitch from "@/components/MaterialSwitch.vue";
import MaterialButton from "@/components/MaterialButton.vue";

// material-input
import setMaterialInput from "@/assets/js/material-input";

// Importar la imagen como un módulo
import fondoAzul from '@/assets/img/fondo-azul-hexagonos.svg';

const email = ref('');
const password = ref('');
const errorMessage = ref('');
const loading = ref(false);

const router = useRouter();
const route = useRoute();

const handleLogin = async () => {
  loading.value = true;
  errorMessage.value = '';

  if (!email.value || !password.value) {
    errorMessage.value = 'Por favor ingrese correo y contraseña';
    loading.value = false;
    return;
  }

  try {
    const { error } = await supabase.auth.signInWithPassword({
      email: email.value,
      password: password.value,
    });

    if (error) {
      errorMessage.value = error.message;
      return;
    }

    await router.replace({ name: 'Dashboard' });
  } catch (error) {
    errorMessage.value = error?.message || 'Error iniciando sesión';
  } finally {
    loading.value = false;
  }
};

const handleConnectTwitch = async () => {
  loading.value = true;
  errorMessage.value = '';
  try {
    const authUrlData = await authService.getAuthUrl();
    if (authUrlData?.auth_url) {
      window.location.href = authUrlData.auth_url;
      return;
    }
    errorMessage.value = 'No se pudo iniciar conexión con Twitch';
  } catch (error) {
    errorMessage.value = error?.response?.data?.detail || 'Error conectando Twitch';
  } finally {
    loading.value = false;
  }
};

const handleOAuthCallbackIfPresent = async () => {
  const code = route.query.code;
  const oauthError = route.query.error;

  if (oauthError) {
    errorMessage.value = `Twitch OAuth error: ${oauthError}`;
    return;
  }

  if (!code || typeof code !== 'string') return;

  loading.value = true;
  errorMessage.value = '';
  try {
    const result = await authService.callback(code);
    if (result?.connected) {
      await router.replace({ name: 'Dashboard' });
      return;
    }
    errorMessage.value = result?.message || 'No se pudo completar la conexión con Twitch.';
  } catch (error) {
    errorMessage.value = error?.response?.data?.detail || 'Error completando callback de Twitch';
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  setMaterialInput();
  await handleOAuthCallbackIfPresent();
});
</script>

<template>
  <div class="container position-sticky z-index-sticky top-0">
    <div class="row">
      <div class="col-12">
        <DefaultNavbar :sticky="true" />
      </div>
    </div>
  </div>
  <Header>
    <div
      class="page-header align-items-start min-vh-100"
      :style="{
        backgroundImage:
          'url(' + fondoAzul + ')'
      }"
      loading="lazy"
    >
      <span class="mask bg-gradient-dark opacity-6"></span>
      <div class="container my-auto">
        <div class="row">
          <div class="col-lg-4 col-md-8 col-12 mx-auto">
            <div class="card z-index-0 fadeIn3 fadeInBottom">
              <div
                class="card-header p-0 position-relative mt-n4 mx-3 z-index-2"
              >
                <div
                  class="bg-gradient-success shadow-success border-radius-lg py-3 pe-1"
                >
                  <h4
                    class="text-white font-weight-bolder text-center mt-2 mb-0"
                  >
                    INGRESAR
                  </h4>
                  <div class="row mt-3">
                    <div class="col-2 text-center ms-auto">
                      <a class="btn btn-link px-3" href="javascript:;">
                        <i class="fa fa-facebook text-white text-lg"></i>
                      </a>
                    </div>
                    <div class="col-2 text-center px-1">
                      <a class="btn btn-link px-3" href="javascript:;">
                        <i class="fa fa-github text-white text-lg"></i>
                      </a>
                    </div>
                    <div class="col-2 text-center me-auto">
                      <a class="btn btn-link px-3" href="javascript:;">
                        <i class="fa fa-google text-white text-lg"></i>
                      </a>
                    </div>
                  </div>
                </div>
              </div>
              <div class="card-body">
                <form role="form" class="text-start" @submit.prevent="handleLogin">
                  <MaterialInput
                    id="email"
                    class="input-group-outline my-3"
                    :label="{ text: 'Email', class: 'form-label' }"
                    type="email"
                    v-model= "email"
                  />
                  <MaterialInput
                    id="password"
                    class="input-group-outline mb-3"
                    :label="{ text: 'Contraseña', class: 'form-label' }"
                    type="password"
                    v-model= "password"
                  />
                  <MaterialSwitch
                    class="d-flex align-items-center mb-3"
                    id="rememberMe"
                    labelClass="mb-0 ms-3"
                    unchecked
                    >Recuerdame
                  </MaterialSwitch>
                    <!-- Mostrar errores si existen -->
                  <div v-if="errorMessage" class="text-danger text-sm mb-2">
                    {{ errorMessage }}
                  </div>

                  <div class="text-center">
                    <MaterialButton
                      class="my-4 mb-2"
                      variant="gradient"
                      color="success"
                      fullWidth
                      :disabled="loading"

                    >
                      {{ loading ? 'Ingresando...' : 'Ingresar' }}
                    </MaterialButton>
                  </div>

                  <div class="text-center">
                    <MaterialButton
                      class="mb-2"
                      variant="gradient"
                      color="info"
                      fullWidth
                      :disabled="loading"
                      @click.prevent="handleConnectTwitch"
                    >
                      Conectar con Twitch
                    </MaterialButton>
                  </div>
                  <p class="mt-4 text-sm text-center">
                    ¿No tienes una cuenta?
                    <router-link
                      :to="{ name: 'signup' }"
                      class="text-success text-gradient font-weight-bold"
                      >Registrarse
                    </router-link>
                  </p>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Header>
</template>
